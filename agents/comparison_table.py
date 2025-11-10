#!/usr/bin/env python3
"""
Comparison Table Agent
Generates structured feature comparison tables for competitor vs Sozee pages
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import BaseAgent, AgentMessage, AgentResponse
import google.generativeai as genai
import time
import json


class ComparisonTableAgent(BaseAgent):
    """Specialized agent for generating comparison tables"""

    def __init__(self, model=None):
        super().__init__(
            name="Comparison_Table_Agent",
            role="Feature Comparison Specialist",
            model=model
        )
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Generate comparison table for patterns 1 & 4"""
        start_time = time.time()
        self.log_message(message)

        task = message.task
        pattern_id = task.get('pattern_id', '')
        competitor = task.get('competitor', '')
        audience = task.get('audience', 'creators')

        # Get competitor research data from context
        research_data = message.context.get('research_data', {})
        competitor_data = research_data.get('Competitor_Research_Agent', {})

        # Generate comparison table
        comparison_table = self._generate_comparison_table(
            pattern_id=pattern_id,
            competitor=competitor,
            audience=audience,
            competitor_data=competitor_data
        )

        execution_time = time.time() - start_time

        return self.create_response(
            message,
            status="completed",
            data={'comparison_table': comparison_table},
            execution_time=execution_time,
            confidence=0.95
        )

    def _generate_comparison_table(self, pattern_id: str, competitor: str,
                                   audience: str, competitor_data: dict) -> list:
        """Generate structured comparison table using competitor research data"""

        # Get Sozee's known features (factual data)
        sozee_features = self._get_sozee_features()

        # Format competitor data for prompt
        competitor_info = json.dumps(competitor_data, indent=2) if competitor_data else "No competitor data available"

        prompt = f"""You are creating a feature comparison table for a landing page comparing Sozee vs {competitor}.

**Pattern**: Pattern {pattern_id} ({'Competitor Comparison' if pattern_id == '1' else 'Alternative'})
**Target Audience**: {audience}
**Competitor**: {competitor}

**SOZEE'S ACTUAL FEATURES** (use these EXACT values):
{json.dumps(sozee_features, indent=2)}

**COMPETITOR RESEARCH DATA** (use this to fill competitor column):
{competitor_info}

**Your Task**: Create a comparison table with 6-8 key features that matter most to {audience}.

**CRITICAL REQUIREMENTS:**
1. **Be 100% FACTUAL** - Only use data from Sozee features above and competitor research data
2. **Focus on differentiation** - Choose features where Sozee has clear advantages
3. **Use specific values** - "30 minutes" not "fast", "$15/week" not "affordable"
4. **Include these key categories**:
   - LORA Training (time, customization)
   - Content Type Support (SFW/NSFW)
   - Platform Focus (OnlyFans, creator-specific)
   - Ease of Use (technical skills required)
   - Pricing (actual costs)
   - Speed (generation time)
   - Special Features (1-click TikTok cloning, etc.)

5. **For competitor data**:
   - Use research data if available
   - If feature not mentioned, use "Not specified" or "Unknown"
   - If competitor lacks feature, use "Not available" or "No"
   - DO NOT hallucinate competitor features

6. **Format for comparison**:
   - Highlight Sozee's creator-specific advantages
   - Make differences clear and scannable
   - Use benefit-focused language where appropriate

**OUTPUT AS JSON ARRAY:**
[
  {{
    "feature": "Feature name (e.g., 'LORA Training Time')",
    "sozee": "Sozee's specific value (e.g., '30 minutes')",
    "competitor": "Competitor's value from research (e.g., '2-3 hours' or 'Not specified')",
    "sozee_advantage": true/false (Is this a clear Sozee advantage?)
  }}
]

Return ONLY valid JSON array with 6-8 comparison rows.
Prioritize features where Sozee has clear advantages for {audience}."""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.3  # Lower temp for factual accuracy
                )
            )

            comparison_table = json.loads(response.text)

            # Validate table structure
            if not isinstance(comparison_table, list):
                raise ValueError("Comparison table must be an array")

            if len(comparison_table) < 6 or len(comparison_table) > 8:
                print(f"  ⚠️ Comparison table has {len(comparison_table)} rows (expected 6-8)")

            # Ensure all rows have required fields
            for row in comparison_table:
                required_fields = ['feature', 'sozee', 'competitor']
                for field in required_fields:
                    if field not in row:
                        raise ValueError(f"Missing required field: {field}")

            print(f"  ✓ Generated comparison table with {len(comparison_table)} features")
            return comparison_table

        except Exception as e:
            print(f"  ⚠️ Error generating comparison table: {e}")
            # Return fallback comparison table with factual Sozee data
            return self._get_fallback_comparison_table(competitor)

    def _get_sozee_features(self) -> dict:
        """Return Sozee's actual features from manifesto (factual data only)"""
        return {
            "setup": {
                "photos_required": "3 photos minimum",
                "training_time": "Instant (no training required)",
                "setup_time": "Immediate - no waiting",
                "technical_skills": "None required"
            },
            "output_quality": {
                "realism": "Hyper-realistic (indistinguishable from real photoshoots)",
                "consistency": "Perfect likeness consistency across unlimited content",
                "quality_level": "Professional-grade, not 'AI art'"
            },
            "content_support": {
                "sfw": True,
                "nsfw": True,
                "flexibility": "Complete creative freedom, no censorship",
                "content_types": "Photos & videos"
            },
            "privacy": {
                "model_isolation": "Your likeness is yours alone",
                "training_data_use": "Never used to train other users' models",
                "control": "Total privacy, total control"
            },
            "platform_focus": {
                "primary": "OnlyFans, Fansly, FanVue",
                "also_supports": "TikTok, Instagram, X",
                "creator_first": True,
                "monetization_workflows": True
            },
            "generation_speed": {
                "photo": "30 seconds per photo",
                "video": "30 seconds per video",
                "volume": "Unlimited content from 3 photos"
            },
            "pricing": {
                "creators": "$15/week",
                "agencies": "$33/week",
                "free_trial": "Yes (no credit card required)"
            },
            "agency_features": {
                "team_access": True,
                "approval_workflows": True,
                "multi_creator_support": True,
                "scheduling": "Built-in"
            },
            "special_features": {
                "tiktok_cloning": "1-click TikTok clone",
                "content_crisis_solution": "Solves 100:1 demand ratio",
                "infinite_content": "3 photos → infinite content forever",
                "fan_requests": "Instant custom request fulfillment",
                "prompt_libraries": "Reusable prompts and style bundles"
            },
            "positioning": {
                "focus": "Monetization-first design (not AI art)",
                "purpose": "Built for creator businesses",
                "category": "AI Content Studio for creator economy"
            }
        }

    def _get_fallback_comparison_table(self, competitor: str) -> list:
        """Fallback comparison table with factual Sozee data from manifesto"""
        return [
            {
                "feature": "Setup Time",
                "sozee": "Instant (3 photos, no training)",
                "competitor": "Not specified",
                "sozee_advantage": True
            },
            {
                "feature": "Photos Required",
                "sozee": "3 photos minimum",
                "competitor": "Not specified",
                "sozee_advantage": True
            },
            {
                "feature": "Output Quality",
                "sozee": "Hyper-realistic (indistinguishable from real)",
                "competitor": "Not specified",
                "sozee_advantage": True
            },
            {
                "feature": "NSFW Content Support",
                "sozee": "Full support (no censorship)",
                "competitor": "Not specified",
                "sozee_advantage": True
            },
            {
                "feature": "Built For",
                "sozee": "OnlyFans/Fansly/FanVue creators",
                "competitor": "General use",
                "sozee_advantage": True
            },
            {
                "feature": "Privacy",
                "sozee": "Your likeness is yours alone (isolated models)",
                "competitor": "Not specified",
                "sozee_advantage": True
            },
            {
                "feature": "Technical Skills Required",
                "sozee": "None",
                "competitor": "Not specified",
                "sozee_advantage": True
            },
            {
                "feature": "Content Generation Speed",
                "sozee": "30 seconds per photo/video",
                "competitor": "Not specified",
                "sozee_advantage": True
            },
            {
                "feature": "Pricing (Creators)",
                "sozee": "$15/week",
                "competitor": "Not specified",
                "sozee_advantage": False
            }
        ]
