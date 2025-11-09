#!/usr/bin/env python3
"""
Copywriting Agent
Synthesizes research into compelling landing page copy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import BaseAgent, AgentMessage, AgentResponse
import google.generativeai as genai
import time
import json


class CopywritingAgent(BaseAgent):
    """Expert conversion copywriter"""

    def __init__(self, viral_hooks: list, model=None):
        super().__init__(
            name="Copywriting_Agent",
            role="Expert Conversion Copywriter",
            model=model
        )
        self.viral_hooks = viral_hooks
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Generate compelling landing page copy"""
        start_time = time.time()
        self.log_message(message)

        task = message.task
        sections = task.get('sections', [])
        blueprint = message.context.get('blueprint', {})
        research_data = message.context.get('research_data', {})

        # Generate content
        content = self._generate_content(
            blueprint=blueprint,
            research_data=research_data,
            sections=sections
        )

        execution_time = time.time() - start_time

        return self.create_response(
            message,
            status="completed",
            data={'content': content},
            execution_time=execution_time,
            confidence=0.9
        )

    def _generate_content(self, blueprint: dict, research_data: dict, sections: list) -> dict:
        """Generate all content sections"""

        # Select viral hook
        import random
        viral_hook = random.choice(self.viral_hooks) if self.viral_hooks else "Transform your content creation"

        prompt = f"""You are an expert copywriter for Sozee.ai, creating landing page content.

**Pattern**: {blueprint.get('pattern_name', 'Unknown')}
**Target Audience**: {blueprint.get('pseo_variables', {}).get('audience', 'Creators')}

**Research Data:**
{json.dumps(research_data, indent=2)[:2000]}

**Viral Hook to Use**: {viral_hook}

**Sozee Key Differentiators:**
- Custom LORA Training in 30 minutes
- 1-Click TikTok Cloning
- Hyper-realistic AI photos and video
- Built specifically for OnlyFans creators
- SFW & NSFW capabilities
- Curated prompt library for creator niche

**Brand Voice**: Confident, empathetic, slightly edgy. Focus on solving "creator burnout" and the "content crisis"

**Your Task**: Generate complete landing page content

**Required Sections:**
1. Hero Section (h1, subtitle, CTAs)
2. Problem/Hook (3-4 paragraphs + bullets, start with viral hook)
3. Solution Overview (Sozee value prop + 3 benefits)
4. Feature Sections (2-3 key features explained)
5. Final CTA

**Writing Guidelines:**
- Address reader directly ("you")
- Keep paragraphs short (2-4 sentences)
- Use specific examples and numbers from research
- Emphasize outcomes over features
- Maintain empathetic yet confident tone
- Vary language (avoid template-itis)

**Output as JSON:**
{{
  "hero": {{
    "h1": "H1 title",
    "subtitle": "Compelling subtitle under 150 chars",
    "primary_cta": "Get Started Free",
    "secondary_cta": "See How It Works"
  }},
  "problem": "Full problem agitation section in Markdown",
  "solution": "Solution overview section in Markdown",
  "features": [
    {{"title": "Feature 1", "content": "Description"}},
    {{"title": "Feature 2", "content": "Description"}}
  ],
  "comparison_table": [
    {{"feature": "Feature name", "sozee": "How Sozee does it", "competitor": "How competitor does it"}}
  ],
  "final_cta": "Final call to action section"
}}

Return ONLY valid JSON."""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=4000,
                    temperature=0.8  # Higher for creative variety
                )
            )

            content = json.loads(response.text)
            print(f"  ✓ Content generation complete")
            return content

        except Exception as e:
            print(f"  ⚠️ Error generating content: {e}")
            # Return minimal content
            return {
                "hero": {
                    "h1": blueprint.get('h1', 'Sozee AI Content Studio'),
                    "subtitle": "Transform your content creation workflow",
                    "primary_cta": "Get Started Free",
                    "secondary_cta": "Learn More"
                },
                "problem": f"# The Challenge\n\n{viral_hook}",
                "solution": "Sozee solves this with AI-powered content generation.",
                "features": [],
                "comparison_table": [],
                "final_cta": "Ready to transform your content? Start your free trial today."
            }
