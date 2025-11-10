#!/usr/bin/env python3
"""
Audience Insight Agent
Researches audience pain points, desires, and emotional triggers
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import ResearchAgent, AgentMessage, AgentResponse
import google.generativeai as genai
import time
import json


class AudienceInsightAgent(ResearchAgent):
    """Audience psychology and insight specialist"""

    def __init__(self, model=None):
        super().__init__(
            name="Audience_Insight_Agent",
            role="Audience Psychology & Insight Specialist",
            model=model
        )
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Research audience insights"""
        start_time = time.time()
        self.log_message(message)

        task = message.task
        audience = task.get('audience', '')
        required_data = task.get('required_data', [])

        # Check cache first
        cache_key = f"audience_{audience}"
        cached = self.get_cached(cache_key)
        if cached:
            print(f"  ✓ Using cached insights for {audience}")
            return self.create_response(
                message,
                status="completed",
                data=cached,
                execution_time=time.time() - start_time,
                confidence=0.9
            )

        # Generate fresh insights
        insights = self._research_audience(audience, required_data)

        # Cache results
        self.cache_research(cache_key, insights)

        execution_time = time.time() - start_time

        return self.create_response(
            message,
            status="completed",
            data=insights,
            sources=[{'type': 'ai_synthesis', 'model': 'gemini-2.0-flash-exp'}],
            execution_time=execution_time,
            confidence=0.85
        )

    def _research_audience(self, audience: str, required_data: list) -> dict:
        """Generate audience insights using AI research"""

        prompt = f"""You are an expert market researcher analyzing the {audience} audience.

**Your Task**: Deep dive into the psychology, pain points, and desires of {audience}.

**Required Research Areas:**
{json.dumps(required_data, indent=2)}

**Research Framework:**

1. **Pain Points** (3-5 specific pain points):
   - What daily frustrations do they face?
   - What makes their work harder?
   - What causes burnout or stress?
   - Be specific and emotional

2. **Desires & Goals** (3-5 aspirations):
   - What do they want to achieve?
   - What would success look like?
   - What are they striving for?
   - Include both practical and aspirational

3. **Objections & Fears** (3-5 common objections):
   - What makes them hesitant to try new tools?
   - What are they afraid of?
   - What past experiences make them skeptical?
   - What budget/time/effort concerns exist?

4. **Current Solutions** (2-3 tools/methods):
   - What are they currently using?
   - Why are those solutions inadequate?
   - What gaps exist in current tools?

5. **Emotional Triggers** (3-4 key emotions):
   - What emotions drive their decisions?
   - What language resonates with them?
   - What aspirational identity do they have?

6. **Content Consumption** (2-3 preferences):
   - Where do they hang out online?
   - What content format do they prefer?
   - Who do they trust for recommendations?

**Context: Sozee AI Content Platform**
- AI photo/video generation
- 3 photos minimum - instant likeness reconstruction (no training, no waiting)
- Built for OnlyFans creators
- SFW & NSFW capabilities
- Solves the "100:1 content crisis" (fans want 100x more content than creators can produce)

**Output as JSON:**
{{
  "audience_segment": "{audience}",
  "pain_points": [
    {{
      "pain": "Specific pain point",
      "intensity": "high/medium/low",
      "frequency": "daily/weekly/monthly"
    }}
  ],
  "desires": [
    {{
      "desire": "Specific goal or aspiration",
      "motivation": "Why they want this",
      "priority": "high/medium/low"
    }}
  ],
  "objections": [
    {{
      "objection": "Specific concern or fear",
      "severity": "deal_breaker/significant/minor",
      "response": "How Sozee addresses this"
    }}
  ],
  "current_solutions": [
    {{
      "solution": "Current tool or method",
      "limitations": "What's missing or broken",
      "replacement_opportunity": "How Sozee is better"
    }}
  ],
  "emotional_triggers": [
    {{
      "emotion": "Fear/Hope/Pride/Relief/etc.",
      "trigger": "What activates this emotion",
      "messaging": "How to leverage in copy"
    }}
  ],
  "content_preferences": {{
    "platforms": ["platform1", "platform2"],
    "format": "video/text/visual",
    "tone": "casual/professional/edgy"
  }},
  "key_insights": [
    "Insight 1: Why this matters",
    "Insight 2: Strategic implication",
    "Insight 3: Content angle"
  ]
}}

Return ONLY valid JSON. Be specific and actionable."""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=3000,
                    temperature=0.7
                )
            )

            insights = json.loads(response.text)
            print(f"  ✓ Audience insights generated for {audience}")
            print(f"    - {len(insights.get('pain_points', []))} pain points")
            print(f"    - {len(insights.get('desires', []))} desires")
            print(f"    - {len(insights.get('objections', []))} objections")

            return insights

        except Exception as e:
            print(f"  ⚠️ Error researching audience: {e}")
            # Return minimal fallback insights
            return {
                "audience_segment": audience,
                "pain_points": [
                    {
                        "pain": "Content creation burnout from constant demand",
                        "intensity": "high",
                        "frequency": "daily"
                    },
                    {
                        "pain": "Difficulty maintaining consistent posting schedule",
                        "intensity": "high",
                        "frequency": "weekly"
                    }
                ],
                "desires": [
                    {
                        "desire": "Automate content creation while maintaining quality",
                        "motivation": "Reduce time spent on repetitive tasks",
                        "priority": "high"
                    }
                ],
                "objections": [
                    {
                        "objection": "AI-generated content may look fake or low quality",
                        "severity": "significant",
                        "response": "Sozee creates hyper-realistic content indistinguishable from real photos using instant likeness reconstruction from just 3 photos"
                    }
                ],
                "current_solutions": [
                    {
                        "solution": "Manual photo/video creation",
                        "limitations": "Time-consuming, expensive, unsustainable",
                        "replacement_opportunity": "Sozee generates content in seconds vs hours"
                    }
                ],
                "emotional_triggers": [
                    {
                        "emotion": "Relief",
                        "trigger": "Freedom from content creation grind",
                        "messaging": "Focus on liberation from burnout"
                    }
                ],
                "content_preferences": {
                    "platforms": ["Twitter/X", "Reddit", "Discord"],
                    "format": "visual",
                    "tone": "casual"
                },
                "key_insights": [
                    f"{audience} are overwhelmed by content demands and seeking automation",
                    "Quality is paramount - generic AI content won't work",
                    "They value tools built specifically for their niche"
                ]
            }
