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
        count = task.get('count', 10)  # Updated from 5 to 10 FAQs for better SEO
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
        """Generate pattern-specific FAQ pairs using templates"""

        # Get pattern context
        pattern_context = self._get_pattern_context(pattern_id, variables)

        # Get pattern-specific question types
        question_types = self._get_pattern_question_types(pattern_id, variables)

        prompt = f"""You are creating FAQ content for a Sozee landing page.

**Page Context**: {pattern_context}
**Pattern ID**: {pattern_id}
**Variables**: {json.dumps(variables)}

**Task**: Create {count} frequently asked questions and answers.

**PATTERN-SPECIFIC QUESTION TYPES** (use these as templates):
{question_types}

**Requirements:**
1. Questions MUST be natural language queries users would actually search
2. Include long-tail keywords in questions
3. Answers should be 2-3 sentences, informative and helpful
4. Address common objections and concerns specific to this pattern
5. Mention Sozee naturally where appropriate
6. Be FACTUAL - don't hallucinate features or pricing

**Sozee Key Facts to Reference:**
- Custom LORA training: 30 minutes
- Content generation: 30 seconds per photo/video
- Hyper-realistic (trained on YOUR face/body)
- SFW & NSFW content support
- Built specifically for OnlyFans/creator platforms
- Pricing: Creators $15/week, Agencies $33/week
- Free trial available (no credit card required)
- No technical skills required
- 1-Click TikTok cloning
- Solves the 1/100 content supply/demand crisis

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
                    max_output_tokens=4000,  # Increased from 2000 to support 10 FAQs
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
            # Return fallback FAQs
            fallback_faqs = [
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
                },
                {
                    "question": "How realistic is Sozee-generated content?",
                    "answer": "Sozee generates hyper-realistic content by training a custom AI model on your specific photos. The results maintain your unique features, body type, and style for authentic-looking content."
                },
                {
                    "question": "Does Sozee support NSFW content?",
                    "answer": "Yes, Sozee fully supports both SFW and NSFW content creation, making it ideal for OnlyFans creators and adult content professionals who need unrestricted creative capabilities."
                },
                {
                    "question": "How much does Sozee cost?",
                    "answer": "Sozee offers two pricing tiers: Creators plan at $15/week and Agencies plan at $33/week. Both include unlimited content generation, custom LORA training, and all features."
                },
                {
                    "question": "Do I need technical skills to use Sozee?",
                    "answer": "No technical skills are required. Sozee is designed for creators, not developers. Simply upload photos, let the AI train, and start generating content with one click."
                },
                {
                    "question": "How fast can I generate content with Sozee?",
                    "answer": "After your initial 30-minute LORA training, you can generate new photos and videos in approximately 30 seconds each. This allows for rapid, high-volume content creation."
                },
                {
                    "question": "What is the 1/100 content crisis?",
                    "answer": "The 1/100 ratio represents the gap between content supply and demand. Fans want 100 pieces of new content, but creators can typically produce only 1 using traditional methods. Sozee solves this by enabling unlimited content generation."
                },
                {
                    "question": "Can I use Sozee for multiple platforms?",
                    "answer": "Yes, Sozee-generated content can be used across all platforms including OnlyFans, Instagram, TikTok, and other creator platforms. The content is optimized for various aspect ratios and platform requirements."
                }
            ]
            return fallback_faqs[:count]

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

    def _get_pattern_question_types(self, pattern_id: str, variables: dict) -> str:
        """Get pattern-specific FAQ question types from content templates"""

        competitor = variables.get('competitor', '[competitor]')
        audience = variables.get('audience', '[audience]')
        use_case = variables.get('use_case', '[use case]')
        platform = variables.get('platform', '[platform]')

        question_types = {
            '1': f"""COMPARISON QUESTIONS (focus on differences vs {competitor}):
• How is Sozee different from {competitor}?
• Is Sozee easier to use than {competitor}?
• Can I switch from {competitor} to Sozee easily?
• What features does Sozee have that {competitor} doesn't?
• Which is better for {platform} creators - Sozee or {competitor}?""",

            '2': f"""BEST TOOL QUESTIONS (focus on why it's #1):
• What makes Sozee the best {use_case} for {audience}?
• How does Sozee compare to other tools?
• Why should {audience} choose Sozee?
• Is Sozee really better than competitors for {use_case}?
• What do {audience} say about Sozee?""",

            '3': f"""DIRECT TOOL QUESTIONS (focus on how it works):
• How does Sozee's {use_case} feature work?
• Is Sozee optimized for {platform}?
• How realistic will my Sozee-generated content look?
• How fast can I generate content with Sozee?
• What's included in the Sozee free trial?""",

            '4': f"""ALTERNATIVE QUESTIONS (focus on switching):
• Why should I switch from {competitor} to Sozee?
• Is migrating from {competitor} to Sozee easy?
• Will I lose my existing content if I switch from {competitor}?
• How much will I save by switching to Sozee?
• What makes Sozee better than {competitor} for {audience}?""",

            '5': f"""REVIEW QUESTIONS (focus on evaluation):
• Is Sozee worth it for {audience}?
• What are Sozee's pros and cons?
• How much does Sozee cost?
• What do real {audience} say about Sozee?
• Who should NOT use Sozee?""",

            '6': f"""CONTENT CRISIS QUESTIONS (focus on the problem):
• What is the content crisis for {audience}?
• How does Sozee solve the 1/100 content supply/demand problem?
• Can I really generate unlimited content with Sozee?
• Will my fans notice if I use Sozee AI content?
• What's the ROI of Sozee for {audience}?"""
        }

        return question_types.get(pattern_id, "Create general FAQ questions about Sozee")
