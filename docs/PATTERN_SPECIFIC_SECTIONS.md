# Pattern-Specific Landing Page Sections

## Overview

The PSEO system now generates **8-11 pattern-specific sections** for each landing page pattern, with **10 FAQ questions** (increased from 5) for better SEO coverage. Each pattern has unique sections tailored to its conversion strategy and search intent.

## System Architecture

### Configuration Files

1. **`config/section_templates.json`** - Defines sections for each of the 6 patterns
2. **`config/patterns.json`** - Pattern metadata (H1 formulas, CTAs, eyebrow text)
3. **`config/content_templates.json`** - AI prompt templates for content generation

### Agent Responsibilities

- **Copywriting Agent** (`agents/copywriting.py`) - Generates pattern-specific sections based on templates
- **FAQ Generator Agent** (`agents/faq_generator.py`) - Generates 10 pattern-specific FAQs (updated from 5)
- **Comparison Table Agent** (`agents/comparison_table.py`) - Generates detailed comparison tables for Patterns 1 & 4
- **Statistics Agent** (`agents/statistics_agent.py`) - Provides data for metrics-heavy sections

---

## Pattern Section Breakdown

### Pattern 1: Competitor Comparison (9 Sections)

**Search Intent:** "Which tool is better for my specific use case?"

**Sections:**
1. **Hero Section** - Head-to-head comparison positioning
2. **Quick Comparison Overview** - 3-column visual stats (Sozee | Feature | Competitor)
3. **Why Audience Are Switching** - 3-4 benefit cards showing problems with competitor → Sozee solutions
4. **Detailed Feature Comparison Table** - 8-10 features with Sozee advantages highlighted
5. **Use Case Deep Dive** - 2-3 specific scenarios where Sozee wins
6. **Problems with Competitor** - 3-4 specific pain points (empathetic but factual)
7. **Social Proof** - Testimonials from switchers, usage stats
8. **FAQ** - 10 comparison-focused questions
9. **Final CTA** - Risk-free trial + migration support

**Key Strategy:** Side-by-side comparison with clear winner positioning

---

### Pattern 2: Best Tool (9 Sections)

**Search Intent:** "What's the #1 ranked tool for my needs?"

**Sections:**
1. **Hero Section** - #1 ranking emphasis
2. **Authority Badges** - Top-rated indicators, usage stats, awards
3. **Why Sozee Ranks #1** - 5-6 competitive advantages with evidence
4. **Feature Showcase** - 4-6 standout features (name → benefit → audience impact)
5. **Comparison to Alternatives** - Generic comparison (Sozee vs "Others")
6. **Use Case Success Stories** - 3 before/after scenarios
7. **Results & ROI** - Time saved, content volume, revenue impact metrics
8. **FAQ** - 10 "best tool" focused questions
9. **Final CTA** - Join the top {audience}

**Key Strategy:** Authority positioning with social proof

---

### Pattern 3: Direct Tool (9 Sections)

**Search Intent:** "I need a tool that does X for Y platform"

**Sections:**
1. **Hero Section** - Platform-specific value prop
2. **Platform-Specific Benefits** - 4 benefits optimized for the platform
3. **How It Works** - 3-4 step visual process (Upload → Train → Generate → Post)
4. **Key Features** - 5-6 platform-relevant features
5. **Speed & Scale** - Before/after metrics (1 shoot = 50 photos vs 10,000+)
6. **Platform Integration** - Workflow fit, export formats, compatibility
7. **Use Cases** - 6-8 content type examples in visual grid
8. **FAQ** - 10 tool-focused questions
9. **Final CTA** - Start creating for {platform}

**Key Strategy:** Clear value prop + platform fit demonstration

---

### Pattern 4: Alternative (9 Sections)

**Search Intent:** "I'm unhappy with X, what's better?"

**Sections:**
1. **Hero Section** - Better alternative positioning
2. **Why Switch** - 4 specific pain points with {competitor}
3. **What Sozee Does Differently** - 4-5 side-by-side solutions (problem → Sozee fix)
4. **Feature Comparison Table** - Focus on missing features in competitor
5. **Easy Migration** - 3 steps to switch, time estimate, reassurances
6. **Pricing Comparison** - Better features, better/comparable price
7. **What You'll Gain** - 3-4 outcome cards (time, cost, capability gains)
8. **FAQ** - 10 switching-focused questions
9. **Final CTA** - Make the switch today + guarantees

**Key Strategy:** Address pain → Show better way

---

### Pattern 5: Review (11 Sections)

**Search Intent:** "Is this tool actually good for my needs?"

**Sections:**
1. **Hero Section** - Honest review positioning
2. **Quick Verdict** - Star rating, best for, not ideal for, bottom line
3. **Pros Section** - 5-7 genuine strengths with explanations
4. **Cons Section** - 2-3 honest limitations (builds trust)
5. **Feature Breakdown** - 6-8 features rated (Feature | Rating | Our Take)
6. **Who It's Perfect For** - 3-4 specific personas
7. **Who Should Look Elsewhere** - 2-3 scenarios where other tools might be better
8. **Pricing Analysis** - Cost breakdown + ROI comparison
9. **Final Verdict** - Clear recommendation with conditions
10. **FAQ** - 10 review-focused questions
11. **Final CTA** - Try it yourself to verify

**Key Strategy:** Balanced evaluation + honest assessment

---

### Pattern 6: Content Crisis (11 Sections)

**Search Intent:** "I'm drowning in content demands, help!"

**Sections:**
1. **Hero Section** - Crisis solution positioning
2. **Crisis Statistics** - 4-6 statistics about creator burnout
3. **The 1/100 Reality** - Visual supply/demand gap (fans want 100, creators make 1)
4. **Why Traditional Solutions Fail** - 3-4 reasons photoshoots don't scale
5. **The Sozee Solution** - Revolutionary approach (1 shoot → 10,000 photos)
6. **Scale Without Burnout** - 4 transformations (from problem → to solution)
7. **Real Impact** - Before/after stories, typical day comparisons
8. **How It Works** - Simple 3-step process
9. **ROI of Solving Crisis** - Time, revenue, mental health, growth metrics
10. **FAQ** - 10 crisis-focused questions
11. **Final CTA** - End your crisis today + crisis calculator

**Key Strategy:** Amplify pain → Present solution

---

## Section Content Structure

Each pattern-specific section generates structured content:

```json
{
  "heading": "Section heading (8-12 words, benefit-focused)",
  "subheading": "Optional context (2-3 sentences)",
  "content": [
    {
      "item_heading": "Heading for this item",
      "item_body": "Body content (markdown supported)",
      "icon_suggestion": "icon name for UI"
    }
  ],
  "visual_style": "UI component type (cards, table, grid, etc.)",
  "cta_text": "Optional embedded CTA"
}
```

### Visual Style Types

- `hero_split` - Split hero with image
- `hero_centered` - Centered hero
- `icon_cards_grid` - Grid of cards with icons
- `three_column_table` - 3-column comparison
- `detailed_comparison_table` - Full feature table
- `scenario_cards` - Use case scenarios
- `problem_cards` - Pain point cards
- `stat_callouts` - Statistics highlights
- `before_after_cards` - Transformation stories
- `accordion` - Expandable FAQ
- `cta_block` - Call-to-action section

---

## FAQ Generation

### Updated: 10 FAQs per Page

FAQs increased from 5 to 10 for better SEO coverage and comprehensive question answering.

**Pattern-Specific Question Types:**

**Pattern 1 (Comparison):**
- How is Sozee different from {competitor}?
- Can I migrate easily?
- Is Sozee easier to use?
- Feature differences?
- Which is better for {platform} creators?
- How long does migration take?
- Will I lose existing content?
- Pricing comparison?
- Technical skills required?
- Free trial details?

**Pattern 2 (Best Tool):**
- What makes Sozee the best {use_case}?
- How does it compare to others?
- Why choose Sozee?
- User testimonials?
- Pricing details?
- Free trial availability?
- Expected results?
- Technical requirements?
- What's included?
- Best for which audience types?

**Pattern 3 (Direct Tool):**
- How does {tool_type} work?
- Platform optimization?
- Content realism?
- Generation speed?
- NSFW support?
- Free trial details?
- Technical skills needed?
- Cost?
- Use for subscriptions?
- Supported formats?

**Pattern 4 (Alternative):**
- Why switch from {competitor}?
- Migration ease?
- Content loss concerns?
- Cost savings?
- Feature advantages?
- Can Sozee do everything {competitor} does?
- Migration support?
- Trial before switching?
- Other users' experiences?
- Time to migrate?

**Pattern 5 (Review):**
- Is Sozee worth it for {audience}?
- Pros and cons?
- Pricing?
- User reviews?
- Who shouldn't use?
- Competitor comparison?
- Free trial?
- Learning curve?
- Content realism?
- ROI?

**Pattern 6 (Crisis):**
- What is the content crisis?
- How does Sozee solve 1/100 problem?
- Unlimited content generation?
- AI detection by fans?
- ROI?
- LORA training time?
- Ongoing photoshoot needs?
- Long-term sustainability?
- Content quality?
- Cost vs traditional methods?

---

## Adding New Patterns

### Step 1: Add Pattern to `config/patterns.json`

```json
{
  "id": 7,
  "name": "New Pattern Name",
  "description": "Pattern description",
  "url_formula": "/url-{variable}-pattern",
  "h1_formula": "H1 with {Variable}",
  "variables": ["variable1", "variable2"],
  "show_comparison_table": false,
  "eyebrow": "Eyebrow Text",
  "primary_cta": "Primary CTA",
  "secondary_cta": "Secondary CTA"
}
```

### Step 2: Define Sections in `config/section_templates.json`

```json
"7": {
  "pattern_name": "New Pattern Name",
  "total_sections": 9,
  "sections": [
    {
      "id": "section_id",
      "order": 1,
      "name": "Section Display Name",
      "static": false,
      "components": ["heading", "content"],
      "content_requirements": {
        "heading": "Requirements for heading",
        "visual_style": "component_type"
      },
      "generation_prompt": "Detailed prompt for AI to generate this section's content"
    }
  ]
}
```

### Step 3: Update FAQ Question Types in `agents/faq_generator.py`

Add pattern-specific question types to `_get_pattern_question_types()` method.

---

## Static vs Dynamic Sections

### Static Sections
- **Same content across all pages** (minor variable substitution)
- Examples: How It Works, Social Proof testimonials
- Defined once, reused with template variables

### Dynamic Sections
- **AI-generated per page** based on pattern, variables, and research
- Examples: Why Switching, Use Case Deep Dive, Crisis Statistics
- Unique content for each landing page

---

## Content Requirements Per Section

Each section in `section_templates.json` specifies:

1. **Components** - What elements to generate (heading, subheading, body, etc.)
2. **Content Requirements** - Specific constraints (word count, tone, structure)
3. **Visual Style** - UI component type for frontend implementation
4. **Generation Prompt** - Detailed instructions for AI content generation

---

## Testing Pattern-Specific Sections

To test the section generation system:

```python
from agents.copywriting import CopywritingAgent
from agent_framework import AgentMessage

# Initialize agent
agent = CopywritingAgent(viral_hooks=[], model='gemini-2.0-flash-exp')

# Create test message
message = AgentMessage(
    message_id="test",
    from_agent="Test",
    to_agent="Copywriting_Agent",
    task={"sections": ["all"]},
    context={
        "blueprint": {
            "pattern_id": "1",
            "pattern_name": "Competitor Comparison",
            "pseo_variables": {
                "competitor": "Higgsfield",
                "audience": "OnlyFans Agencies"
            }
        },
        "research_data": {}
    }
)

# Execute
response = agent.execute(message)
print(response.data)
```

---

## Implementation Checklist

- [x] Created `config/section_templates.json` with all 6 patterns (8-11 sections each)
- [x] Updated `agents/faq_generator.py` to generate 10 FAQs (from 5)
- [x] Expanded `agents/copywriting.py` with pattern-specific section generation
- [x] Added `_generate_pattern_sections()` method to Copywriting Agent
- [x] Added `_generate_section_content()` method for individual sections
- [x] Updated `config/content_templates.json` to reflect 10 FAQs
- [x] Increased FAQ max_tokens from 2000 to 4000
- [x] Added 10 fallback FAQs for error handling
- [ ] Test all 6 patterns for section generation
- [ ] Validate JSON structure of generated sections
- [ ] Frontend implementation to render pattern-specific sections

---

## Next Steps

1. **Frontend Integration** - Build UI components for each visual_style type
2. **Content Validation** - Add quality checks for generated section content
3. **Performance Optimization** - Cache section templates, batch AI requests
4. **Analytics** - Track which sections drive highest engagement per pattern
5. **A/B Testing** - Test section order and content variations

---

## Key Benefits

✅ **SEO Optimized** - 10 FAQs per page (doubled from 5) for better search coverage
✅ **Pattern-Specific** - Each of 6 patterns has unique sections matching search intent
✅ **Scalable** - Add new patterns or sections via config (no code changes)
✅ **Structured** - Consistent JSON output with headings, body, visual suggestions
✅ **AI-Powered** - Leverages Gemini AI for dynamic, contextual content generation
✅ **Comprehensive** - 8-11 sections per page (up from generic 9-section structure)

---

## Questions?

See `/docs/marketing/Sozee_Landing_Page_Structure_Guide.md` for original 9-section structure.
See `/docs/marketing/Sozee_Landing_Page_Pattern_Examples.md` for pattern-by-pattern examples.
See `/AGENTS.md` for detailed agent specifications.
