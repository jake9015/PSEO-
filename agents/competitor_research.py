#!/usr/bin/env python3
"""
Competitor Research Agent
Researches AI tools and competitors for factual comparison data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import ResearchAgent, AgentMessage, AgentResponse
import google.generativeai as genai
import time


class CompetitorResearchAgent(ResearchAgent):
    """Researches competitors for factual data"""

    def __init__(self, model=None):
        super().__init__(
            name="Competitor_Research_Agent",
            role="AI Tool Market Analyst & Intelligence Gatherer",
            model=model,
            tools=['web_search', 'web_fetch']
        )
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Research competitor details"""
        start_time = time.time()
        self.log_message(message)

        task = message.task
        competitor = task.get('competitor')
        audience = task.get('audience', '')
        required_data = task.get('required_data', [])

        # Check cache first
        cache_key = f"{competitor}_{audience}"
        cached = self.get_cached(cache_key)
        if cached:
            print(f"  ✓ Using cached data for {competitor}")
            return self.create_response(
                message,
                status="completed",
                data={'competitor_data': cached},
                sources=[],
                execution_time=time.time() - start_time,
                confidence=0.9
            )

        # In production, this would use web search APIs
        # For now, using Gemini's knowledge with explicit instructions
        research_data = self._research_competitor(competitor, audience, required_data)

        # Cache results
        self.cache_research(cache_key, research_data)

        execution_time = time.time() - start_time

        return self.create_response(
            message,
            status="completed",
            data={'competitor_data': research_data},
            sources=research_data.get('sources', []),
            execution_time=execution_time,
            confidence=0.85
        )

    def _research_competitor(self, competitor: str, audience: str, required_data: list) -> dict:
        """Use Gemini to research competitor"""

        prompt = f"""You are researching {competitor} as a competitive AI content tool.

**Task**: Provide factual information about {competitor} for {audience}

**Required information:**
{', '.join(required_data)}

**Instructions:**
- Be FACTUAL and accurate
- If pricing is unknown, say "Pricing varies - check official site"
- Focus on features relevant to content creators
- Identify limitations for {audience} specifically
- Note NSFW/SFW capabilities if applicable

**Output as JSON:**
{{
  "competitor": "{competitor}",
  "features": ["feature1", "feature2", "feature3"],
  "pricing": "pricing info or 'Contact for pricing'",
  "pros": ["pro1", "pro2"],
  "cons": ["con1", "con2"],
  "limitations_for_audience": ["limitation1", "limitation2"],
  "nsfw_support": true/false,
  "ease_of_use": "Easy/Moderate/Complex",
  "target_user": "Agencies/Creators/General",
  "sources": [{{"type": "knowledge", "note": "Based on general knowledge of tool"}}]
}}

Return ONLY valid JSON, no markdown."""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.3  # Low temp for factual accuracy
                )
            )

            # Parse JSON response
            import json
            result = json.loads(response.text)
            print(f"  ✓ Competitor research complete: {competitor}")
            return result

        except Exception as e:
            print(f"  ⚠️ Error researching {competitor}: {e}")
            # Return minimal safe data
            return {
                "competitor": competitor,
                "features": ["AI content generation"],
                "pricing": "Contact for pricing",
                "pros": ["Available"],
                "cons": ["May not be optimized for creators"],
                "limitations_for_audience": ["Unknown"],
                "nsfw_support": False,
                "ease_of_use": "Unknown",
                "target_user": "General",
                "sources": [{"type": "error", "note": str(e)}]
            }
