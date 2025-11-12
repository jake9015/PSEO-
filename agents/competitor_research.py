#!/usr/bin/env python3
"""
Competitor Research Agent
Researches AI tools and competitors for factual comparison data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import ResearchAgent, AgentMessage, AgentResponse
from utils.competitor_kb import CompetitorKnowledgeBase
import google.generativeai as genai
import time
import json
import re


class CompetitorResearchAgent(ResearchAgent):
    """Researches competitors for factual data"""

    def __init__(self, model=None):
        super().__init__(
            name="Competitor_Research_Agent",
            role="AI Tool Market Analyst & Intelligence Gatherer",
            model=model
        )
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # Initialize Knowledge Base
        self.kb = CompetitorKnowledgeBase()

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Research competitor details and save to knowledge base"""
        start_time = time.time()
        self.log_message(message)

        task = message.task
        competitor = task.get('competitor')
        audience = task.get('audience', '')
        required_data = task.get('required_data', [])

        # Check Knowledge Base first
        kb_profile = self.kb.get_profile(competitor)
        if kb_profile:
            print(f"  ✓ Using KB data for {competitor}")
            return self.create_response(
                message,
                status="completed",
                data={'competitor_data': kb_profile},
                sources=[{"type": "knowledge_base", "note": "Retrieved from competitor KB"}],
                execution_time=time.time() - start_time,
                confidence=0.95
            )

        # If not in KB, check memory cache
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

        # No KB or cache - perform fresh research
        print(f"  🔍 Researching {competitor} (not in KB)...")
        research_data = self._research_competitor(competitor, audience, required_data)

        # Save to Knowledge Base (structured profile)
        try:
            self.kb.save_profile(competitor, research_data)
        except Exception as e:
            print(f"  ⚠️ Could not save to KB: {e}")

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

    def _strip_markdown_json(self, text: str) -> str:
        """Strip markdown code blocks from JSON response"""
        text = re.sub(r'^```(?:json)?\s*\n', '', text.strip(), flags=re.MULTILINE)
        text = re.sub(r'\n```\s*$', '', text.strip(), flags=re.MULTILINE)
        return text.strip()

    def _research_competitor(self, competitor: str, audience: str, required_data: list) -> dict:
        """Use Gemini to research competitor and structure as KB profile"""

        prompt = f"""You are researching {competitor} as a competitive AI content tool.

**Task**: Create a structured competitor profile for the Knowledge Base.

**Context**: We're comparing {competitor} to Sozee for {audience}. Be FACTUAL and accurate.

**Instructions:**
1. Research {competitor}'s actual capabilities, pricing, and positioning
2. Be specific about technical requirements and limitations
3. Identify target audience and use cases
4. Note NSFW support (critical for creator platforms)
5. Include specific pricing if known, otherwise estimate range
6. Focus on facts, not marketing claims

**REQUIRED OUTPUT STRUCTURE (match this exactly):**

{{
  "category": "Tool category (e.g., 'AI Image Generator', 'AI Video Platform')",
  "target_audience": "Primary users (e.g., 'OnlyFans creators, adult content creators')",
  "positioning": "One-line market position",
  "setup": {{
    "photos_required": "Specific requirement (e.g., '10-20 training images', 'Text prompts')",
    "training_time": "Training duration (e.g., '30-60 minutes', 'Instant', 'N/A')",
    "technical_skills": "Required skills (e.g., 'Low', 'Moderate - requires setup', 'High - technical')"
  }},
  "features": {{
    "nsfw_support": true/false/"Limited/filtered",
    "creator_focus": true/false,
    "platform_focus": "Target platforms (e.g., 'OnlyFans, adult platforms', 'General social media')",
    "privacy_model": "Privacy approach (e.g., 'Private models', 'Public gallery', 'Cloud-based')",
    "content_types": ["Image", "Video", etc.],
    "hyper_realistic": "Quality description (e.g., 'Photorealistic', 'AI art style', 'Good quality')"
  }},
  "pricing": {{
    "known": true/false,
    "estimate": "$X-Y/month or one-time pricing",
    "free_trial": true/false
  }},
  "strengths": ["Key advantage 1", "Key advantage 2", "Key advantage 3"],
  "weaknesses": ["Limitation 1", "Limitation 2", "Limitation 3"]
}}

**CRITICAL**: Return ONLY valid JSON matching this structure. No markdown, no code blocks, just pure JSON.

If you're unsure about specific details:
- Pricing: Estimate range based on similar tools
- NSFW: Most mainstream tools = false/limited
- Technical skills: Based on setup complexity
- Be honest about unknowns but provide reasonable category-level info"""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.3  # Low temp for factual accuracy
                )
            )

            # Strip markdown and parse JSON
            cleaned_text = self._strip_markdown_json(response.text)
            result = json.loads(cleaned_text)

            print(f"  ✓ Competitor research complete: {competitor}")
            print(f"    Category: {result.get('category')}")
            print(f"    NSFW Support: {result.get('features', {}).get('nsfw_support')}")
            print(f"    Pricing: {result.get('pricing', {}).get('estimate')}")

            return result

        except json.JSONDecodeError as e:
            print(f"  ❌ JSON parsing error for {competitor}: {e}")
            print(f"  📄 Raw response (first 300 chars): {response.text[:300]}")
            return self._create_fallback_profile(competitor)
        except Exception as e:
            print(f"  ⚠️ Error researching {competitor}: {e}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_profile(competitor)

    def _create_fallback_profile(self, competitor: str) -> dict:
        """Create minimal fallback profile if research fails"""
        return {
            "category": "AI Content Generation Tool",
            "target_audience": "General users, creators",
            "positioning": "AI content platform",
            "setup": {
                "photos_required": "Multiple training images required",
                "training_time": "Requires model training",
                "technical_skills": "Moderate"
            },
            "features": {
                "nsfw_support": False,
                "creator_focus": False,
                "platform_focus": "General purpose",
                "privacy_model": "Cloud-based",
                "content_types": ["Images"],
                "hyper_realistic": "AI-generated aesthetic"
            },
            "pricing": {
                "known": False,
                "estimate": "$20-50/month",
                "free_trial": True
            },
            "strengths": ["AI content generation"],
            "weaknesses": ["Not creator-focused", "Training required", "Limited information available"]
        }
