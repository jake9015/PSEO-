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
import re


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

    def _strip_markdown_json(self, text: str) -> str:
        """Strip markdown code blocks from JSON response"""
        # Remove ```json ... ``` or ``` ... ``` blocks
        text = re.sub(r'^```(?:json)?\s*\n', '', text.strip(), flags=re.MULTILINE)
        text = re.sub(r'\n```\s*$', '', text.strip(), flags=re.MULTILINE)
        return text.strip()

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
        """Generate all content sections using pattern-specific templates"""

        # Load pattern configuration
        pattern_config = self._load_pattern_config(blueprint.get('pattern_id'))
        variables = blueprint.get('pseo_variables', {})
        pattern_id = str(blueprint.get('pattern_id'))

        # Build H1 from formula
        h1 = self._build_h1(pattern_config, variables)

        # Get pattern-specific context
        pattern_angle = self._get_pattern_angle(pattern_id, variables)

        # Generate pattern-specific sections
        pattern_sections = self._generate_pattern_sections(pattern_id, variables, research_data, h1, pattern_config)

        # Select viral hook
        import random
        viral_hook = random.choice(self.viral_hooks) if self.viral_hooks else "Transform your content creation"

        # Load content templates
        content_templates = self._load_content_templates()

        prompt = f"""You are an expert copywriter for Sozee.ai, creating PSEO landing page content.

**PATTERN CONTEXT:**
- Pattern: {blueprint.get('pattern_name', 'Unknown')} (Pattern {blueprint.get('pattern_id')})
- H1 Title: {h1}
- Eyebrow: {pattern_config.get('eyebrow', '')}
- Pattern Angle: {pattern_angle}

**TARGET VARIABLES:**
{self._format_variables(variables)}

**VIRAL HOOK TO USE:**
{viral_hook}
(Use this as the opening sentence or headline of the problem section)

**RESEARCH DATA:**
{self._format_research_data(research_data)}

**PATTERN-SPECIFIC COPYWRITING STRATEGY:**
{pattern_angle}

For this pattern, emphasize:
{self._get_pattern_emphasis(blueprint.get('pattern_id'), variables)}

**SOZEE KEY DIFFERENTIATORS:**
- **3 PHOTOS MINIMUM** - Instant likeness reconstruction, no training, no waiting
- **THE CONTENT CRISIS SOLUTION** - Solves the 100:1 demand ratio (fans want 100x more content)
- **HYPER-REALISTIC** - Indistinguishable from real photoshoots, not "AI art"
- **TOTAL PRIVACY** - Your likeness is yours alone, isolated models never used for training
- **INFINITE CONTENT ENGINE** - 3 photos → unlimited photos/videos forever
- **MONETIZATION-FIRST DESIGN** - Built for creator businesses, not AI art hobbyists
- **SFW & NSFW CAPABILITIES** - Complete creative freedom, no censorship
- **AGENCY WORKFLOWS** - Team access, approval flows, multi-creator support
- 1-Click TikTok Cloning (replicate viral content instantly)
- Built specifically for OnlyFans/Fansly/FanVue creator platforms
- No technical skills required
- Instant custom fan request fulfillment

**THE CONTENT CRISIS (Core Problem Framework):**
Traditional creator economy: Fans demand 100 pieces of content, creators can produce 1.
This 100:1 ratio creates burnout, unstable revenue, and business failure.
Sozee breaks the link between physical availability and content production.
- Traditional: 1 photoshoot → 10-20 photos
- Sozee: 3 photos → infinite content forever
- Result: Creators scale without burnout, agencies never run out, virtual influencers stay consistent

**BRAND VOICE:**
Direct, confident, slightly edgy. Speak to the Content Crisis and creator burnout.
Use "you" language. Be specific with numbers (3 photos, 100:1 ratio, infinite content).
Phrases to use: "The Content Crisis", "We multiply creators, not replace them", "Content that never dries up", "Your likeness is yours alone"

**WRITING GUIDELINES:**
- Keep paragraphs SHORT (2-4 sentences max)
- Use specific examples from research data
- Include real pain points identified for {variables.get('audience', 'creators')}
- Emphasize OUTCOMES over features ("scale without burnout" not "AI generation")
- Vary sentence structure (avoid template-itis)
- Natural keyword integration (no stuffing)

**CTAs FROM PATTERN:**
- Primary: {pattern_config.get('primary_cta', 'Get Started Free')}
- Secondary: {pattern_config.get('secondary_cta', 'See How It Works')}

**OUTPUT AS JSON:**
{{
  "hero": {{
    "h1": "{h1}",
    "eyebrow": "{pattern_config.get('eyebrow', '')}",
    "subtitle": "Compelling subtitle under 150 chars (pattern-specific angle)",
    "primary_cta": "{pattern_config.get('primary_cta', 'Get Started Free')}",
    "secondary_cta": "{pattern_config.get('secondary_cta', 'See How It Works')}"
  }},
  "problem": "Full problem agitation section in Markdown (start with viral hook, 3-4 paragraphs + 3 bullets)",
  "solution": "Solution overview section in Markdown (Sozee value prop + 3 benefits)",
  "features": [
    {{"title": "Feature 1", "content": "Benefit-focused description"}},
    {{"title": "Feature 2", "content": "Benefit-focused description"}}
  ],
  "comparison_table": {self._get_comparison_table_instruction(blueprint.get('pattern_id'))},
  "final_cta": "Final call to action section (reinforce pattern angle)"
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

            # Strip markdown code blocks before parsing
            cleaned_text = self._strip_markdown_json(response.text)
            content = json.loads(cleaned_text)

            # Add pattern-specific sections
            content['pattern_sections'] = pattern_sections

            print(f"  ✓ Content generation complete ({len(pattern_sections)} pattern-specific sections)")
            return content

        except json.JSONDecodeError as e:
            print(f"  ❌ JSON parsing error: {e}")
            print(f"  📄 Raw response (first 500 chars): {response.text[:500]}")
            return self._create_fallback_content(h1, variables, research_data, viral_hook, pattern_config)
        except Exception as e:
            print(f"  ❌ Error generating content: {e}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_content(h1, variables, research_data, viral_hook, pattern_config)

    def _create_fallback_content(self, h1: str, variables: dict, research_data: dict, viral_hook: str, pattern_config: dict) -> dict:
        """Create improved fallback content using research data and correct H1"""

        competitor = variables.get('competitor', '')
        audience = variables.get('audience', 'creators')

        # Extract research insights if available
        audience_data = research_data.get('Audience_Insight_Agent', {})
        competitor_data = research_data.get('Competitor_Research_Agent', {})

        pain_points = audience_data.get('pain_points', [])
        pain_point_text = pain_points[0] if pain_points else "Content creation bottlenecks slow down growth"

        # Build pattern-specific problem section
        if competitor:
            problem = f"""# The Challenge with {competitor}

{viral_hook}

Many {audience} struggle with traditional AI tools that don't understand the creator economy. The Content Crisis is real: fans demand 100x more content than creators can produce.

**Common pain points:**
- Content production bottlenecks
- Inconsistent quality and likeness
- Time-consuming workflows
- Limited creative freedom"""
        else:
            problem = f"""# The Challenge

{viral_hook}

{audience} face the Content Crisis: fans want 100 pieces of content, but you can only produce 1. This creates burnout, unstable revenue, and growth limits.

**The reality:**
- Traditional photoshoots: 1 session → 10-20 photos
- Audience demands: 50-100+ posts per week
- Result: Creator burnout and business instability"""

        # Build solution section
        solution = f"""## How Sozee Solves This

Sozee breaks the link between physical availability and content production. Upload just 3 photos and generate unlimited hyper-realistic content forever.

**Key benefits:**
- **3 photos minimum** - Instant likeness reconstruction, no training
- **Hyper-realistic output** - Indistinguishable from real photoshoots
- **Complete privacy** - Your likeness is yours alone
- **SFW & NSFW** - Full creative freedom for {audience}"""

        # Build features
        features = [
            {
                "title": "Instant Setup (3 Photos)",
                "content": "No training, no waiting. Upload 3 photos and start generating unlimited content immediately."
            },
            {
                "title": "Hyper-Realistic Content",
                "content": "Generate photos and videos indistinguishable from real photoshoots. Perfect likeness consistency every time."
            },
            {
                "title": "Built for Creators",
                "content": f"Designed specifically for {audience} with OnlyFans/Fansly workflows, NSFW support, and monetization-first features."
            }
        ]

        return {
            "hero": {
                "h1": h1,
                "eyebrow": pattern_config.get('eyebrow', ''),
                "subtitle": f"Generate unlimited hyper-realistic content from just 3 photos. Built for {audience}.",
                "primary_cta": pattern_config.get('primary_cta', 'Get Started Free'),
                "secondary_cta": pattern_config.get('secondary_cta', 'See How It Works')
            },
            "problem": problem,
            "solution": solution,
            "features": features,
            "comparison_table": [],
            "final_cta": f"Ready to solve the Content Crisis? Start your free trial and see why {audience} are switching to Sozee."
        }

    def _generate_pattern_sections(self, pattern_id: str, variables: dict, research_data: dict, h1: str, pattern_config: dict) -> dict:
        """Generate pattern-specific sections based on section_templates.json"""

        # Load section templates
        section_templates = self._load_section_templates()
        pattern_sections_config = section_templates.get('patterns', {}).get(pattern_id, {})

        if not pattern_sections_config:
            print(f"  ⚠️ No section templates found for pattern {pattern_id}")
            return {}

        sections_config = pattern_sections_config.get('sections', [])
        generated_sections = {}

        # Generate each pattern-specific section (excluding hero, faq, final_cta which are handled elsewhere)
        for section_config in sections_config:
            section_id = section_config.get('id')

            # Skip sections handled by other agents or already generated
            if section_id in ['hero', 'faq', 'final_cta']:
                continue

            # Skip sections without generation prompts (they're handled by other agents)
            if 'generation_prompt' not in section_config:
                continue

            # Generate section content
            section_content = self._generate_section_content(
                section_config,
                variables,
                research_data,
                pattern_config
            )

            if section_content:
                generated_sections[section_id] = section_content

        print(f"  ✓ Generated {len(generated_sections)} pattern-specific sections")
        return generated_sections

    def _generate_section_content(self, section_config: dict, variables: dict, research_data: dict, pattern_config: dict) -> dict:
        """Generate content for a specific section"""

        section_id = section_config.get('id')
        section_name = section_config.get('name')
        generation_prompt = section_config.get('generation_prompt', '')
        content_requirements = section_config.get('content_requirements', {})
        components = section_config.get('components', [])

        # Replace variables in prompts
        generation_prompt = self._replace_variables(generation_prompt, variables)

        # Build prompt for AI
        prompt = f"""You are an expert copywriter for Sozee.ai creating a specific landing page section.

**SECTION: {section_name}** (ID: {section_id})

**TASK:**
{generation_prompt}

**SECTION REQUIREMENTS:**
{json.dumps(content_requirements, indent=2)}

**COMPONENTS TO GENERATE:**
{', '.join(components)}

**VARIABLES:**
{self._format_variables(variables)}

**RESEARCH DATA:**
{self._format_research_data(research_data)}

**SOZEE KEY FACTS:**
- 3 photos minimum - instant likeness reconstruction (no training, no waiting)
- Hyper-realistic AI content generation (indistinguishable from real photoshoots)
- 1-Click TikTok Cloning (replicate viral content instantly)
- Built specifically for OnlyFans/creator platforms
- SFW & NSFW capabilities (complete flexibility)
- Solves the "100:1 content crisis" (fans want 100x more content than creators can produce)
- Total privacy - your likeness is yours alone, isolated models never used for training
- No technical skills required
- Pricing: Creators $15/week, Agencies $33/week

**OUTPUT FORMAT (JSON):**
{{
  "heading": "Section heading (8-12 words, benefit-focused)",
  "subheading": "Optional subheading or intro (2-3 sentences)" | null,
  "content": [
    {{
      "item_heading": "Heading for this item" | null,
      "item_body": "Body content for this item (markdown supported)",
      "icon_suggestion": "icon name" | null
    }}
  ],
  "visual_style": "{content_requirements.get('visual_style', 'default')}",
  "cta_text": "Optional CTA text" | null
}}

Return ONLY valid JSON matching this structure."""

        try:
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.8
                )
            )

            # Strip markdown code blocks before parsing
            cleaned_text = self._strip_markdown_json(response.text)
            section_content = json.loads(cleaned_text)
            return section_content

        except json.JSONDecodeError as e:
            print(f"  ❌ JSON parsing error in section {section_id}: {e}")
            print(f"  📄 Raw response (first 300 chars): {response.text[:300]}")
            return {}
        except Exception as e:
            print(f"  ❌ Error generating section {section_id}: {e}")
            return {}

    def _load_section_templates(self) -> dict:
        """Load section templates from section_templates.json"""
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'section_templates.json')
        try:
            with open(template_path, 'r') as f:
                templates = json.load(f)
                # Validate that templates were loaded
                if not templates or 'patterns' not in templates:
                    raise ValueError("Section templates file is empty or missing 'patterns' key")
                return templates
        except FileNotFoundError:
            raise FileNotFoundError(f"Section templates file not found at: {template_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in section templates file: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading section templates: {e}")

    def _replace_variables(self, text: str, variables: dict) -> str:
        """Replace {variable} placeholders in text"""
        for var_name, var_value in variables.items():
            text = text.replace(f"{{{var_name}}}", var_value)
            # Also try capitalized version
            text = text.replace(f"{{{var_name.capitalize()}}}", var_value)
        return text

    def _load_pattern_config(self, pattern_id: str) -> dict:
        """Load pattern configuration from patterns.json"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'patterns.json')
        try:
            with open(config_path, 'r') as f:
                patterns_data = json.load(f)
                for pattern in patterns_data.get('patterns', []):
                    if str(pattern.get('id')) == str(pattern_id):
                        return pattern
        except Exception as e:
            print(f"  ⚠️ Could not load pattern config: {e}")
        return {}

    def _load_content_templates(self) -> dict:
        """Load content templates from content_templates.json"""
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'content_templates.json')
        try:
            with open(template_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"  ⚠️ Could not load content templates: {e}")
        return {}

    def _build_h1(self, pattern_config: dict, variables: dict) -> str:
        """Build H1 from pattern formula"""
        h1_formula = pattern_config.get('h1_formula', 'Sozee AI Content Studio')

        # Replace variables in formula
        h1 = h1_formula
        for var_name, var_value in variables.items():
            # Try multiple placeholder formats to match pattern formulas
            placeholders = [
                f'{{{var_name}}}',  # {competitor}
                f'{{{var_name.capitalize()}}}',  # {Competitor}
                f'{{{var_name.upper()}}}',  # {COMPETITOR}
                f'{{{var_name.replace("_", " ").title().replace(" ", "_")}}}',  # {Use_Case}
                f'{{{var_name.replace("_", " ").title()}}}',  # {Use Case}
            ]

            for placeholder in placeholders:
                if placeholder in h1:
                    h1 = h1.replace(placeholder, var_value)

        return h1

    def _get_pattern_angle(self, pattern_id: str, variables: dict) -> str:
        """Get pattern-specific copywriting angle"""
        competitor = variables.get('competitor', '')
        audience = variables.get('audience', 'creators')
        use_case = variables.get('use_case', '')

        angles = {
            '1': f"COMPARISON ANGLE: Emphasize how Sozee differs from {competitor}. Show side-by-side feature comparison. Highlight Sozee's creator-specific advantages (instant setup with 3 photos, hyper-realistic output, NSFW support, OnlyFans optimization, total privacy).",
            '2': f"BEST TOOL ANGLE: Position Sozee as the #1 ranked {use_case} for {audience}. Support with specific advantages. Use authoritative language ('the best', 'top-rated', 'recommended').",
            '3': f"DIRECT TOOL ANGLE: Explain exactly what Sozee does and why it's perfect for {audience}. Focus on specific use case benefits. Be clear and benefit-focused.",
            '4': f"ALTERNATIVE ANGLE: Explain why {audience} are switching from {competitor} to Sozee. Address {competitor}'s limitations directly. Position Sozee as the better choice.",
            '5': f"REVIEW ANGLE: Provide honest, balanced evaluation of Sozee for {audience}. Include pros, cons, and recommendations. Be trustworthy and authoritative.",
            '6': f"CONTENT CRISIS ANGLE: Emphasize the 1/100 supply/demand problem. Show how Sozee specifically solves creator burnout and content bottlenecks. Use urgent language around the crisis."
        }

        return angles.get(pattern_id, "Focus on Sozee's value proposition and benefits.")

    def _get_pattern_emphasis(self, pattern_id: str, variables: dict) -> str:
        """Get what to emphasize for each pattern"""
        competitor = variables.get('competitor', '')

        emphasis = {
            '1': f"• Why Sozee is better than {competitor} for creators\n• Specific feature differences (LORA, NSFW, ease of use)\n• Creator-specific advantages\n• Pricing comparison if available",
            '2': "• Why Sozee ranks #1\n• Unique creator-focused features\n• Success stories or results\n• What makes it better than alternatives",
            '3': "• Specific benefits for this platform\n• How easy it is to use\n• Speed and quality of results\n• Perfect use case fit",
            '4': f"• Why users are leaving {competitor}\n• What {competitor} lacks\n• Migration ease\n• Immediate benefits of switching",
            '5': "• Honest pros and cons\n• Who it's perfect for\n• Value for money\n• Recommendation strength",
            '6': "• The 1/100 crisis reality\n• Creator burnout epidemic\n• How Sozee uniquely solves it\n• Dramatic before/after outcomes"
        }

        return emphasis.get(pattern_id, "• Key benefits\n• Use case fit\n• Call to action")

    def _get_comparison_table_instruction(self, pattern_id: str) -> str:
        """Return comparison table instruction based on pattern"""
        if pattern_id in ['1', '4']:  # Comparison, Alternative
            return '''[
    {"feature": "Setup Time", "sozee": "3 photos, instant setup", "competitor": "Use competitor data"},
    {"feature": "NSFW Support", "sozee": "Full support", "competitor": "Use competitor data"},
    {"feature": "Creator Focus", "sozee": "Built for OnlyFans", "competitor": "Use competitor data"},
    {"feature": "Privacy", "sozee": "Your likeness is yours alone", "competitor": "Use competitor data"}
  ]'''
        else:
            return '[]'

    def _format_variables(self, variables: dict) -> str:
        """Format variables for prompt"""
        return '\n'.join([f"- {key.replace('_', ' ').title()}: {value}" for key, value in variables.items()])

    def _format_research_data(self, research_data: dict) -> str:
        """Format research data for prompt"""
        if not research_data:
            return "No research data available"

        formatted = []
        for agent_name, data in research_data.items():
            formatted.append(f"\n**From {agent_name}:**")
            formatted.append(json.dumps(data, indent=2)[:1000])

        return '\n'.join(formatted)
