#!/usr/bin/env python3
"""
FAQ Generator Agent
Creates pattern-specific Q&A pairs optimized for SEO
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import BaseAgent, AgentMessage, AgentResponse
import google.generativeai as genai
import time
import json


class FAQGeneratorAgent(BaseAgent):
    """FAQ content specialist"""

    def __init__(self, model=None):
        super().__init__(
            name="FAQ_Generator_Agent",
            role="FAQ Content Specialist",
            model=model
        )
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Generate FAQ section"""
        start_time = time.time()
        self.log_message(message)

        task = message.task
        pattern_id = task.get('pattern_id', '')
        count = task.get('count', 5)
        blueprint = message.context.get('blueprint', {})
        variables = blueprint.get('pseo_variables', {})

        # Generate FAQs
        faqs = self._generate_faqs(pattern_id, variables, count)

        execution_time = time.time() - start_time

        return self.create_response(
            message,
            status="completed",
            data={'faqs': faqs},
            execution_time=execution_time,
            confidence=0.9
        )

    def _generate_faqs(self, pattern_id: str, variables: dict, count: int) -> list:
        """Generate pattern-specific FAQ pairs"""

        # Get pattern context
        pattern_context = self._get_pattern_context(pattern_id, variables)

        prompt = f"""You are creating FAQ content for a Sozee landing page.

**Page Context**: {pattern_context}
**Pattern ID**: {pattern_id}
**Variables**: {json.dumps(variables)}

**Task**: Create {count} frequently asked questions and answers.

**Requirements:**
1. Questions must be natural language queries users would actually search
2. Include long-tail keywords in questions
3. Answers should be 2-3 sentences, informative and helpful
4. Address common objections and concerns
5. Mention Sozee naturally where appropriate
6. Questions should cover:
   - Feature comparisons (if competitor mentioned)
   - Pricing and trials
   - Technical capabilities (NSFW, LORA training, etc.)
   - Use case fit
   - Getting started

**Sozee Key Features to Reference:**
- 30-minute custom LORA training
- 1-Click TikTok cloning
- SFW & NSFW content support
- Built for OnlyFans creators
- Free trial available
- No credit card required

**Output as JSON array:**
[
  {{
    "question": "Natural question with keywords?",
    "answer": "Helpful 2-3 sentence answer mentioning Sozee."
  }}
]

Return ONLY valid JSON array with exactly {count} Q&A pairs."""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.6
                )
            )

            faqs = json.loads(response.text)

            if len(faqs) != count:
                print(f"  ⚠️ Expected {count} FAQs, got {len(faqs)}")

            print(f"  ✓ Generated {len(faqs)} FAQ pairs")
            return faqs

        except Exception as e:
            print(f"  ⚠️ Error generating FAQs: {e}")
            # Return minimal fallback FAQs
            return [
                {
                    "question": "What is Sozee?",
                    "answer": "Sozee is an AI-powered content generation platform built specifically for creators. It offers custom LORA training, 1-click TikTok cloning, and both SFW and NSFW content capabilities."
                },
                {
                    "question": "Does Sozee offer a free trial?",
                    "answer": "Yes, Sozee offers a free trial with no credit card required. You can test all features including custom AI model training and content generation before committing to a paid plan."
                },
                {
                    "question": "How long does LORA training take?",
                    "answer": "Sozee's custom LORA training takes approximately 30 minutes. This allows you to create a personalized AI model that generates content matching your unique style and brand."
                }
            ][:count]

    def _get_pattern_context(self, pattern_id: str, variables: dict) -> str:
        """Generate context description for pattern"""

        pattern_descriptions = {
            '1': f"Comparing Sozee vs {variables.get('competitor', 'competitor')} for {variables.get('audience', 'creators')}",
            '2': f"Best {variables.get('tool_type', 'AI tool')} for {variables.get('audience', 'creators')} on {variables.get('platform', 'social media')}",
            '3': f"Sozee as a {variables.get('tool_type', 'content tool')} for {variables.get('use_case', 'content creation')}",
            '4': f"Sozee as an alternative to {variables.get('competitor', 'competitor')}",
            '5': f"Review of {variables.get('competitor', 'competitor')} for {variables.get('audience', 'creators')}",
            '6': f"Solving content creation challenges for {variables.get('audience', 'creators')}"
        }

        return pattern_descriptions.get(pattern_id, "Sozee AI content generation platform")
