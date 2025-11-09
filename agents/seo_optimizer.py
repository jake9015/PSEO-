#!/usr/bin/env python3
"""
SEO Optimization Agent
Crafts perfect metadata and ensures SEO best practices
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import BaseAgent, AgentMessage, AgentResponse
import google.generativeai as genai
import time
import json


class SEOOptimizationAgent(BaseAgent):
    """Technical SEO expert"""

    def __init__(self, model=None):
        super().__init__(
            name="SEO_Optimization_Agent",
            role="Technical SEO Editor & Metadata Specialist",
            model=model
        )
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Generate SEO metadata"""
        start_time = time.time()
        self.log_message(message)

        task = message.task
        h1 = task.get('h1', '')
        pattern_id = task.get('pattern_id', '')
        variables = message.context.get('pseo_variables', {})

        # Generate metadata
        metadata = self._generate_metadata(h1, pattern_id, variables)

        execution_time = time.time() - start_time

        return self.create_response(
            message,
            status="completed",
            data=metadata,
            execution_time=execution_time,
            confidence=0.95
        )

    def _generate_metadata(self, h1: str, pattern_id: str, variables: dict) -> dict:
        """Generate meta title and description with pattern-specific guidance"""

        # Get pattern-specific examples
        pattern_examples = self._get_pattern_meta_examples(pattern_id, variables)

        prompt = f"""You are an SEO expert creating metadata for a Sozee landing page.

**H1**: {h1}
**Pattern**: {pattern_id}
**Variables**: {json.dumps(variables)}

**CRITICAL Requirements:**
1. **meta_title**: EXACTLY 50-60 characters (count carefully!)
   - Must include "Sozee"
   - Include primary keyword naturally
   - Compelling for click-through
   - Front-load important keywords

2. **meta_description**: EXACTLY 150-160 characters (count carefully!)
   - Include main benefit or hook
   - Natural keyword integration
   - Must include CTA phrase (e.g., "Start free trial", "Compare features", "Learn more")
   - Make it click-worthy

3. **focus_keyword**: Primary keyword phrase from H1

**PATTERN-SPECIFIC GUIDANCE:**
{pattern_examples}

**SEO Best Practices:**
- Front-load important keywords in both title and description
- Include target audience/competitor naturally
- Create urgency or curiosity in description
- Match page intent (comparison, review, alternative, etc.)
- Avoid keyword stuffing - keep natural
- Include power words: "best", "vs", "alternative", "review", "solution"

**Output as JSON:**
{{
  "meta_title": "Exact 50-60 char title with Sozee",
  "meta_description": "Exact 150-160 char description with benefit and CTA",
  "focus_keyword": "primary keyword phrase"
}}

CRITICAL: Count characters! Titles must be 50-60 chars, descriptions 150-160 chars.
Return ONLY valid JSON."""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.5
                )
            )

            metadata = json.loads(response.text)

            # Validate character counts
            if len(metadata['meta_title']) < 50 or len(metadata['meta_title']) > 60:
                print(f"  ⚠️ Meta title length: {len(metadata['meta_title'])} (should be 50-60)")
            if len(metadata['meta_description']) < 150 or len(metadata['meta_description']) > 160:
                print(f"  ⚠️ Meta description length: {len(metadata['meta_description'])} (should be 150-160)")

            print(f"  ✓ SEO metadata generated")
            return metadata

        except Exception as e:
            print(f"  ⚠️ Error generating metadata: {e}")
            # Fallback metadata
            return {
                "meta_title": f"{h1} | Sozee",
                "meta_description": f"{h1}. AI-powered content generation for creators. Start your free trial today and transform your workflow.",
                "focus_keyword": h1.lower()
            }

    def _get_pattern_meta_examples(self, pattern_id: str, variables: dict) -> str:
        """Get pattern-specific meta description examples"""

        competitor = variables.get('competitor', '[competitor]')
        audience = variables.get('audience', '[audience]')
        use_case = variables.get('use_case', '[use case]')
        platform = variables.get('platform', '[platform]')

        examples = {
            '1': f"""COMPARISON Pattern Examples:
Title: "Sozee vs {competitor} for {audience} | AI Comparison"
       (Example length: ~55 chars)

Description: "Compare Sozee and {competitor} for {audience}. See features, pricing, and which AI content tool solves the content crisis. Free trial available."
             (Target: 150-160 chars - emphasize differentiation + CTA)""",

            '2': f"""BEST TOOL Pattern Examples:
Title: "Best {use_case} for {audience} | Sozee 2025"
       (Example length: ~50-55 chars)

Description: "Discover the best {use_case} for {audience} on {platform}. Solve creator burnout with AI-powered content. Start free trial today."
             (Target: 150-160 chars - emphasize #1 ranking + benefit)""",

            '3': f"""DIRECT TOOL Pattern Examples:
Title: "{platform} {use_case} | Sozee AI Content Studio"
       (Example length: ~50-55 chars)

Description: "Professional {platform} {use_case}. Generate unlimited hyper-realistic content and scale without burnout. Start your free trial today."
             (Target: 150-160 chars - emphasize specific benefit + ease)""",

            '4': f"""ALTERNATIVE Pattern Examples:
Title: "{competitor} Alternative for {audience} | Sozee"
       (Example length: ~50-55 chars)

Description: "Looking for a {competitor} alternative? {audience} are switching to Sozee for custom LORA training and NSFW support. Compare features now."
             (Target: 150-160 chars - emphasize switching benefits)""",

            '5': f"""REVIEW Pattern Examples:
Title: "Sozee Review for {audience} | Honest AI Tool Analysis"
       (Example length: ~55-60 chars)

Description: "Honest Sozee review for {audience}. Pros, cons, pricing, and features. Is Sozee worth it for AI content creation? Read our analysis."
             (Target: 150-160 chars - emphasize honesty + thoroughness)""",

            '6': f"""CONTENT CRISIS Pattern Examples:
Title: "Content Crisis Solution for {platform} {audience} | Sozee"
       (Example length: ~55-60 chars)

Description: "Solve the content crisis for {platform} {audience}. Generate unlimited AI content and scale without creator burnout. See how Sozee solves 1/100 problem."
             (Target: 150-160 chars - emphasize problem + solution)"""
        }

        return examples.get(pattern_id, "Create compelling SEO metadata")
