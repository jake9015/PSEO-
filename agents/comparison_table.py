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
import re


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

        # Load competitor knowledge base
        self.competitor_profiles = self._load_competitor_profiles()

    def _strip_markdown_json(self, text: str) -> str:
        """Strip markdown code blocks from JSON response"""
        text = re.sub(r'^```(?:json)?\s*\n', '', text.strip(), flags=re.MULTILINE)
        text = re.sub(r'\n```\s*$', '', text.strip(), flags=re.MULTILINE)
        return text.strip()

    def _load_competitor_profiles(self) -> dict:
        """Load competitor knowledge base from config"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'competitor_profiles.json')
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                return data.get('competitors', {})
        except Exception as e:
            print(f"  ⚠️ Could not load competitor profiles: {e}")
            return {}

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

        # Get competitor profile from knowledge base
        competitor_profile = self.competitor_profiles.get(competitor, {})

        # Merge research data with knowledge base (research takes priority)
        merged_competitor_info = self._merge_competitor_data(competitor_profile, competitor_data)

        # Format competitor data for prompt
        competitor_info = json.dumps(merged_competitor_info, indent=2) if merged_competitor_info else "Using category-level comparison"

        prompt = f"""You are creating a feature comparison table for a landing page comparing Sozee vs {competitor}.

**Pattern**: Pattern {pattern_id} ({'Competitor Comparison' if pattern_id == '1' else 'Alternative'})
**Target Audience**: {audience}
**Competitor**: {competitor}

**SOZEE'S ACTUAL FEATURES** (use these EXACT values):
{json.dumps(sozee_features, indent=2)}

**COMPETITOR DATA** (research + knowledge base):
{competitor_info}

**IMPORTANT**: This data combines AI research with our competitor knowledge base. Use specific values where available. Avoid "Not specified" - use category-level comparisons instead (e.g., "Requires training" instead of "Not specified").

**Your Task**: Create a comparison table with 6-8 key features that matter most to {audience}.

**CRITICAL REQUIREMENTS:**
1. **Be 100% FACTUAL** - Only use data from Sozee features above and competitor research data
2. **Focus on differentiation** - Choose features where Sozee has clear advantages
3. **Use specific values** - "3 photos, instant" not "fast", "$15/week" not "affordable"
4. **Include these key categories**:
   - Setup Time (3 photos minimum, instant vs training time)
   - Content Type Support (SFW/NSFW)
   - Platform Focus (OnlyFans, creator-specific)
   - Ease of Use (technical skills required)
   - Privacy (isolated models, ownership)
   - Pricing (actual costs)
   - Speed (generation time)
   - Special Features (1-click TikTok cloning, etc.)

5. **For competitor data**:
   - Use specific values from research/knowledge base
   - If competitor lacks a feature, state it clearly: "No NSFW support" not "Not available"
   - Use category comparisons: "Requires training" not "Not specified"
   - For unknown pricing: "Varies" or estimate range
   - NEVER say "Not specified" - use knowledge base data or reasonable category inference

6. **Format for comparison**:
   - Highlight Sozee's creator-specific advantages
   - Make differences clear and scannable
   - Use benefit-focused language where appropriate

**OUTPUT AS JSON ARRAY:**
[
  {{
    "feature": "Feature name (e.g., 'Setup Time')",
    "sozee": "Sozee's specific value (e.g., '3 photos, instant')",
    "competitor": "Competitor's value from KB/research (e.g., 'Requires 10-20 images and 30-60 min training')",
    "sozee_advantage": true/false (Is this a clear Sozee advantage?)
  }}
]

**CRITICAL**: NEVER use "Not specified" as a value. Always use specific data from research/KB, or use descriptive category-level comparisons like "Requires training", "No NSFW support", "General purpose tool", "Standard cloud storage", etc.

Return ONLY valid JSON array with 6-8 comparison rows. NO markdown code blocks.
Prioritize features where Sozee has clear advantages for {audience}."""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.3  # Lower temp for factual accuracy
                )
            )

            # Strip markdown and parse JSON
            cleaned_text = self._strip_markdown_json(response.text)
            comparison_table = json.loads(cleaned_text)

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

        except json.JSONDecodeError as e:
            print(f"  ❌ JSON parsing error in comparison table: {e}")
            print(f"  📄 Raw response (first 300 chars): {response.text[:300] if 'response' in locals() else 'No response'}")
            # Return fallback comparison table with KB data
            return self._get_fallback_comparison_table(competitor)
        except Exception as e:
            print(f"  ⚠️ Error generating comparison table: {e}")
            import traceback
            traceback.print_exc()
            # Return fallback comparison table with factual Sozee data
            return self._get_fallback_comparison_table(competitor)

    def _merge_competitor_data(self, knowledge_base_profile: dict, research_data: dict) -> dict:
        """Merge knowledge base profile with research data (research takes priority)"""
        if not knowledge_base_profile and not research_data:
            return {}

        # Start with knowledge base as foundation
        merged = knowledge_base_profile.copy() if knowledge_base_profile else {}

        # Override with research data where available
        if research_data:
            # Research data should take priority for accuracy
            for key, value in research_data.items():
                if value:  # Only override if research has actual data
                    merged[key] = value

        return merged

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
        """Fallback comparison table using knowledge base data"""

        # Try to get competitor profile from knowledge base
        profile = self.competitor_profiles.get(competitor, {})

        # Extract competitor features or use category-level fallbacks
        setup_info = profile.get('setup', {})
        features = profile.get('features', {})
        pricing = profile.get('pricing', {})

        comp_training = setup_info.get('training_time', 'Requires model training')
        comp_photos = setup_info.get('photos_required', 'Multiple training images required')
        comp_nsfw = "Yes" if features.get('nsfw_support') else "No NSFW support"
        comp_focus = features.get('platform_focus', 'General purpose')
        comp_quality = features.get('hyper_realistic', 'AI-generated aesthetic')
        comp_privacy = features.get('privacy_model', 'Standard cloud storage')
        comp_skills = setup_info.get('technical_skills', 'Moderate technical knowledge')
        comp_pricing = pricing.get('estimate', 'Varies by plan')

        return [
            {
                "feature": "Setup Time",
                "sozee": "Instant (3 photos, no training)",
                "competitor": comp_training,
                "sozee_advantage": True
            },
            {
                "feature": "Photos Required",
                "sozee": "3 photos minimum",
                "competitor": comp_photos,
                "sozee_advantage": True
            },
            {
                "feature": "Output Quality",
                "sozee": "Hyper-realistic (indistinguishable from real)",
                "competitor": comp_quality,
                "sozee_advantage": True
            },
            {
                "feature": "NSFW Content Support",
                "sozee": "Full support (no censorship)",
                "competitor": comp_nsfw,
                "sozee_advantage": "No" in comp_nsfw
            },
            {
                "feature": "Built For",
                "sozee": "OnlyFans/Fansly/FanVue creators",
                "competitor": comp_focus,
                "sozee_advantage": True
            },
            {
                "feature": "Privacy",
                "sozee": "Your likeness is yours alone (isolated models)",
                "competitor": comp_privacy,
                "sozee_advantage": True
            },
            {
                "feature": "Technical Skills Required",
                "sozee": "None",
                "competitor": comp_skills,
                "sozee_advantage": "None" not in comp_skills
            },
            {
                "feature": "Pricing (Creators)",
                "sozee": "$15/week",
                "competitor": comp_pricing,
                "sozee_advantage": False
            }
        ]
