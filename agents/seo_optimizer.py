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
        """Generate meta title and description"""

        prompt = f"""You are an SEO expert creating metadata for a Sozee landing page.

**H1**: {h1}
**Pattern**: {pattern_id}
**Variables**: {json.dumps(variables)}

**Requirements:**
1. **meta_title**: 50-60 characters, includes "Sozee", compelling for clicks
2. **meta_description**: 150-160 characters EXACTLY, includes CTA, targets keyword
3. **focus_keyword**: Primary keyword phrase

**SEO Guidelines:**
- Front-load important keywords
- Include target audience/competitor naturally
- Create urgency or curiosity
- Make it click-worthy
- Must match page content

**Examples:**
- "Sozee vs Higgsfield for Agencies | AI Content Tool Comparison"
- "Best AI Photo Generator for OnlyFans 2025 | Sozee Content Studio"

**Output as JSON:**
{{
  "meta_title": "50-60 char title with Sozee",
  "meta_description": "150-160 char description with CTA",
  "focus_keyword": "primary keyword phrase"
}}

Count characters carefully! Return ONLY valid JSON."""

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
