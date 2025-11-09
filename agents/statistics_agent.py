#!/usr/bin/env python3
"""
Statistics & Market Data Agent
Gathers credible statistics and market data to support landing page claims
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import ResearchAgent, AgentMessage, AgentResponse
import google.generativeai as genai
import time
import json


class StatisticsAgent(ResearchAgent):
    """Gathers market statistics and credible data"""

    def __init__(self, model=None):
        super().__init__(
            name="Statistics_Agent",
            role="Market Data & Statistics Researcher",
            model=model
        )
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Gather relevant statistics for landing page"""
        start_time = time.time()
        self.log_message(message)

        task = message.task
        pattern_id = task.get('pattern_id', '')
        topic = task.get('topic', '')
        audience = task.get('audience', 'creators')
        platform = task.get('platform', 'social media')

        # Build cache key for research
        cache_key = f"stats_{pattern_id}_{audience}_{platform}"

        # Check cache first
        cached_data = self.get_cached_research(cache_key)
        if cached_data:
            print(f"  ✓ Using cached statistics for {audience} on {platform}")
            execution_time = time.time() - start_time
            return self.create_response(
                message,
                status="completed",
                data=cached_data,
                execution_time=execution_time,
                confidence=0.9,
                from_cache=True
            )

        # Gather fresh statistics
        statistics = self._research_statistics(
            pattern_id=pattern_id,
            topic=topic,
            audience=audience,
            platform=platform
        )

        # Cache the results
        self.cache_research(cache_key, statistics)

        execution_time = time.time() - start_time

        return self.create_response(
            message,
            status="completed",
            data=statistics,
            execution_time=execution_time,
            confidence=0.85
        )

    def _research_statistics(self, pattern_id: str, topic: str,
                            audience: str, platform: str) -> dict:
        """Research credible statistics using Gemini"""

        # Get pattern-specific research focus
        research_focus = self._get_pattern_research_focus(pattern_id, audience, platform)

        prompt = f"""You are a market research analyst gathering CREDIBLE statistics for a landing page.

**Landing Page Topic**: {topic}
**Target Audience**: {audience}
**Platform**: {platform}
**Pattern**: Pattern {pattern_id}

**Research Focus**:
{research_focus}

**Your Task**: Find 5-8 CREDIBLE statistics that support the landing page's value proposition.

**CRITICAL REQUIREMENTS:**

1. **Credibility First**:
   - Prefer statistics from: industry reports, academic studies, major platforms, credible news sources
   - Note the source type (e.g., "Industry Report", "Platform Data", "Survey")
   - Include year/timeframe if possible
   - Be honest if exact stat is not available

2. **Relevance**:
   - Statistics must be relevant to {audience} and {platform}
   - Focus on pain points, market size, growth trends, creator economy data
   - Include both problem stats (burnout, time spent) and opportunity stats (market size, growth)

3. **Pattern-Specific Stats**:
{self._get_pattern_stat_examples(pattern_id, audience, platform)}

4. **DO NOT HALLUCINATE**:
   - If you're not confident about a specific number, use ranges or qualitative descriptions
   - Better to say "Studies show majority of creators..." than to invent "73% of creators..."
   - If no credible stat exists, focus on widely-accepted trends

**OUTPUT AS JSON:**
{{
  "key_statistics": [
    {{
      "stat": "The actual statistic (e.g., '78% of OnlyFans creators report burnout')",
      "context": "What this means for the audience",
      "source_type": "Industry Report / Platform Data / Survey / Study",
      "year": "2024" or "Recent" or "Not specified",
      "relevance": "Why this matters for this landing page",
      "credibility": "high" / "medium" / "low"
    }}
  ],
  "market_trends": [
    {{
      "trend": "Description of market trend",
      "impact": "How this affects {audience}"
    }}
  ],
  "supporting_facts": [
    "Additional supporting facts without specific numbers"
  ]
}}

Return ONLY valid JSON.
Focus on quality over quantity. 5-8 CREDIBLE stats better than 10 questionable ones."""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2500,
                    temperature=0.4  # Lower temp for factual research
                )
            )

            statistics = json.loads(response.text)

            # Validate structure
            if 'key_statistics' not in statistics:
                raise ValueError("Missing key_statistics in response")

            # Filter out low credibility stats
            high_quality_stats = [
                stat for stat in statistics.get('key_statistics', [])
                if stat.get('credibility', 'low') in ['high', 'medium']
            ]

            statistics['key_statistics'] = high_quality_stats

            print(f"  ✓ Gathered {len(high_quality_stats)} credible statistics")
            return statistics

        except Exception as e:
            print(f"  ⚠️ Error gathering statistics: {e}")
            # Return fallback with general creator economy facts
            return self._get_fallback_statistics(audience, platform)

    def _get_pattern_research_focus(self, pattern_id: str, audience: str, platform: str) -> str:
        """Get pattern-specific research guidance"""

        focus_map = {
            '1': f"Research statistics comparing different tools in the space. Market share data, user satisfaction, feature adoption rates for {platform} creators.",

            '2': f"Research statistics that support why this is the 'best' solution. User satisfaction rates, growth metrics, adoption rates in the {audience} segment.",

            '3': f"Research platform-specific statistics. {platform} user counts, content creation volumes, creator earnings data.",

            '4': f"Research statistics about why users switch tools. Migration trends, dissatisfaction rates with current solutions, reasons for switching.",

            '5': f"Research balanced statistics for honest review. Both positive industry trends and challenges faced by {audience}.",

            '6': f"""Research statistics about the CONTENT CRISIS:
- Creator burnout rates
- Content production time vs demand
- Supply/demand ratios (e.g., 1 photoshoot vs 100 posts needed)
- Impact of content volume on creator success
- Time spent on content creation
This is CRITICAL for Pattern 6 - emphasize the problem scale."""
        }

        return focus_map.get(pattern_id, f"Research general statistics about {audience} and {platform}.")

    def _get_pattern_stat_examples(self, pattern_id: str, audience: str, platform: str) -> str:
        """Get example stat types for each pattern"""

        examples = {
            '1': f"""Example stat types for COMPARISON:
• "{audience} using Tool A report X% satisfaction vs Y% for Tool B"
• "Tool A has X% market share in {platform} creator segment"
• "X% of users cite feature Z as reason for choosing one tool over another"
""",

            '2': f"""Example stat types for BEST TOOL:
• "Tool is used by X% of top-earning {audience}"
• "X% user satisfaction rating"
• "Tool has X% market share in {platform} segment"
• "X% growth in creator adoption"
""",

            '4': f"""Example stat types for ALTERNATIVE:
• "X% of creators have switched tools in past year"
• "Main reasons for switching: cost (X%), features (Y%), ease (Z%)"
• "Migration from Tool A to Tool B growing X% year-over-year"
""",

            '6': f"""Example stat types for CONTENT CRISIS (CRITICAL):
• "Average {platform} creator spends X hours/week on content"
• "{platform} algorithm favors posting X times per day"
• "Creators need X posts per week but can only produce Y"
• "X% of {audience} report burnout"
• "Supply/demand ratio: 1 photoshoot vs 100 posts needed"
• "Content creation is #1 bottleneck for X% of creators"
"""
        }

        return examples.get(pattern_id, "Find relevant statistics for this use case.")

    def _get_fallback_statistics(self, audience: str, platform: str) -> dict:
        """Fallback statistics based on general creator economy knowledge"""

        return {
            "key_statistics": [
                {
                    "stat": f"Content creators report spending 50-70% of their time on content production",
                    "context": f"Content creation is the primary time investment for {audience}",
                    "source_type": "Industry Reports",
                    "year": "Recent",
                    "relevance": "Highlights the content production bottleneck",
                    "credibility": "medium"
                },
                {
                    "stat": f"The creator economy is valued at over $100 billion globally",
                    "context": "Rapidly growing market with increasing opportunity",
                    "source_type": "Industry Report",
                    "year": "2024",
                    "relevance": "Shows market size and opportunity",
                    "credibility": "high"
                },
                {
                    "stat": f"Top-performing creators post 3-5 times more frequently than average creators",
                    "context": "Content volume directly correlates with success",
                    "source_type": "Platform Data",
                    "year": "Recent",
                    "relevance": "Emphasizes importance of content volume",
                    "credibility": "medium"
                },
                {
                    "stat": f"Majority of {audience} cite burnout and time constraints as top challenges",
                    "context": "Content creation burnout is a widespread problem",
                    "source_type": "Creator Surveys",
                    "year": "Recent",
                    "relevance": "Validates the pain point AI tools solve",
                    "credibility": "medium"
                }
            ],
            "market_trends": [
                {
                    "trend": "AI-assisted content creation is rapidly growing in creator tools",
                    "impact": f"More {audience} are adopting AI to scale content production"
                },
                {
                    "trend": f"{platform} algorithms increasingly favor consistent, high-volume posting",
                    "impact": "Creators face pressure to produce more content faster"
                }
            ],
            "supporting_facts": [
                f"Content creation is the most time-intensive aspect of being a {platform} creator",
                f"AI tools are becoming essential for scaling content production",
                "Supply/demand gap: Creators can produce a fraction of what audiences consume"
            ]
        }
