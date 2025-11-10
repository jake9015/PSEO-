# Agent Prompts Reference

**Complete collection of all AI prompts used by the PSEO multi-agent system**

This document contains the actual prompts sent to Google Gemini API by each of the 10 specialized agents.

---

## Table of Contents

1. [PSEO Strategist Agent](#1-pseo-strategist-agent) - Blueprint Planning (No Gemini Prompt - Logic-Based)
2. [Competitor Research Agent](#2-competitor-research-agent) - Competitor Analysis
3. [Audience Insight Agent](#3-audience-insight-agent) - Psychology & Pain Points
4. [Statistics Agent](#4-statistics-agent) - Market Data & Stats
5. [Copywriting Agent](#5-copywriting-agent) - Content Generation
6. [FAQ Generator Agent](#6-faq-generator-agent) - Q&A Creation
7. [SEO Optimizer Agent](#7-seo-optimizer-agent) - Meta Tags & SEO
8. [Comparison Table Agent](#8-comparison-table-agent) - Feature Comparison
9. [Schema Markup Agent](#9-schema-markup-agent) - JSON-LD Schemas (No Gemini Prompt - Template-Based)
10. [Quality Control Agent](#10-quality-control-agent) - Content Validation

---

## 1. PSEO Strategist Agent

**Purpose:** Create blueprint and plan which agents to use

**Note:** This agent does **NOT** use Gemini API. It uses pure logic to:
- Analyze pattern requirements
- Determine funnel stage (bottom/mid/top)
- Select which agents are needed
- Identify research requirements
- Calculate priority

**Logic:**
- Patterns 1, 4, 5 → Bottom funnel → Model 2 → Full research
- Patterns 2, 3, 6 → Mid funnel → Model 1 → Optional research
- Returns `ContentBlueprint` with all planning data

---

## 2. Competitor Research Agent

**Purpose:** Research competitor tools for factual comparison data

**Prompt Template:**

```python
f"""You are researching {competitor} as a competitive AI content tool.

**Task**: Provide factual information about {competitor} for {audience}

**Required information:**
{', '.join(required_data)}

**Instructions:**
- Be FACTUAL and accurate
- If pricing is unknown, say "Pricing varies - check official site"
- Focus on features relevant to content creators
- Identify limitations for {audience} specifically
- Note NSFW/SFW capabilities if applicable

**Output as JSON:**
{{
  "competitor": "{competitor}",
  "features": ["feature1", "feature2", "feature3"],
  "pricing": "pricing info or 'Contact for pricing'",
  "pros": ["pro1", "pro2"],
  "cons": ["con1", "con2"],
  "limitations_for_audience": ["limitation1", "limitation2"],
  "nsfw_support": true/false,
  "ease_of_use": "Easy/Moderate/Complex",
  "target_user": "Agencies/Creators/General",
  "sources": [{{"type": "knowledge", "note": "Based on general knowledge of tool"}}]
}}

Return ONLY valid JSON, no markdown."""
```

**Example Filled:**
```
You are researching Higgsfield as a competitive AI content tool.

Task: Provide factual information about Higgsfield for OnlyFans Creators

Required information:
features_list, pricing_tiers, pros_cons, audience_fit, nsfw_support

Instructions:
- Be FACTUAL and accurate
- If pricing is unknown, say "Pricing varies - check official site"
- Focus on features relevant to content creators
- Identify limitations for OnlyFans Creators specifically
- Note NSFW/SFW capabilities if applicable
...
```

**Settings:**
- `max_output_tokens`: 2000
- `temperature`: 0.3 (low for factual accuracy)

**Caching:** Cached by `competitor_name + audience`

---

## 3. Audience Insight Agent

**Purpose:** Deep psychological research on target audience

**Prompt Template:**

```python
f"""You are an expert market researcher analyzing the {audience} audience.

**Your Task**: Deep dive into the psychology, pain points, and desires of {audience}.

**Required Research Areas:**
{json.dumps(required_data, indent=2)}

**Research Framework:**

1. **Pain Points** (3-5 specific pain points):
   - What daily frustrations do they face?
   - What makes their work harder?
   - What causes burnout or stress?
   - Be specific and emotional

2. **Desires & Goals** (3-5 aspirations):
   - What do they want to achieve?
   - What would success look like?
   - What are they striving for?
   - Include both practical and aspirational

3. **Objections & Fears** (3-5 common objections):
   - What makes them hesitant to try new tools?
   - What are they afraid of?
   - What past experiences make them skeptical?
   - What budget/time/effort concerns exist?

4. **Current Solutions** (2-3 tools/methods):
   - What are they currently using?
   - Why are those solutions inadequate?
   - What gaps exist in current tools?

5. **Emotional Triggers** (3-4 key emotions):
   - What emotions drive their decisions?
   - What language resonates with them?
   - What aspirational identity do they have?

6. **Content Consumption** (2-3 preferences):
   - Where do they hang out online?
   - What content format do they prefer?
   - Who do they trust for recommendations?

**Context: Sozee AI Content Platform**
- AI photo/video generation
- LORA training in 30 minutes
- Built for OnlyFans creators
- SFW & NSFW capabilities
- Solves "content burnout" crisis

**Output as JSON:**
{{
  "audience_segment": "{audience}",
  "pain_points": [
    {{
      "pain": "Specific pain point",
      "intensity": "high/medium/low",
      "frequency": "daily/weekly/monthly"
    }}
  ],
  "desires": [
    {{
      "desire": "Specific goal or aspiration",
      "motivation": "Why they want this",
      "priority": "high/medium/low"
    }}
  ],
  "objections": [
    {{
      "objection": "Specific concern or fear",
      "severity": "deal_breaker/significant/minor",
      "response": "How Sozee addresses this"
    }}
  ],
  "current_solutions": [
    {{
      "solution": "Current tool or method",
      "limitations": "What's missing or broken",
      "replacement_opportunity": "How Sozee is better"
    }}
  ],
  "emotional_triggers": [
    {{
      "emotion": "Fear/Hope/Pride/Relief/etc.",
      "trigger": "What activates this emotion",
      "messaging": "How to leverage in copy"
    }}
  ],
  "content_preferences": {{
    "platforms": ["platform1", "platform2"],
    "format": "video/text/visual",
    "tone": "casual/professional/edgy"
  }},
  "key_insights": [
    "Insight 1: Why this matters",
    "Insight 2: Strategic implication",
    "Insight 3: Content angle"
  ]
}}

Return ONLY valid JSON. Be specific and actionable."""
```

**Settings:**
- `max_output_tokens`: 3000
- `temperature`: 0.7 (balanced for creativity)

**Caching:** Cached by `audience`

---

## 4. Statistics Agent

**Purpose:** Gather credible market statistics and data

**Prompt Template:**

```python
f"""You are a market research analyst gathering CREDIBLE statistics for a landing page.

**Landing Page Topic**: {topic}
**Target Audience**: {audience}
**Platform**: {platform}
**Pattern**: Pattern {pattern_id}

**Research Focus**:
{research_focus}

**Your Task**: Find 5-8 CREDIBLE statistics that support the landing page's value proposition.

**CRITICAL REQUIREMENTS:**

1. **Credibility First**:
   - Prefer statistics from: industry reports, academic studies, major platforms, credible news sources
   - Note the source type (e.g., "Industry Report", "Platform Data", "Survey")
   - Include year/timeframe if possible
   - Be honest if exact stat is not available

2. **Relevance**:
   - Statistics must be relevant to {audience} and {platform}
   - Focus on pain points, market size, growth trends, creator economy data
   - Include both problem stats (burnout, time spent) and opportunity stats (market size, growth)

3. **Pattern-Specific Stats**:
{self._get_pattern_stat_examples(pattern_id, audience, platform)}

4. **DO NOT HALLUCINATE**:
   - If you're not confident about a specific number, use ranges or qualitative descriptions
   - Better to say "Studies show majority of creators..." than to invent "73% of creators..."
   - If no credible stat exists, focus on widely-accepted trends

**OUTPUT AS JSON:**
{{
  "key_statistics": [
    {{
      "stat": "The actual statistic (e.g., '78% of OnlyFans creators report burnout')",
      "context": "What this means for the audience",
      "source_type": "Industry Report / Platform Data / Survey / Study",
      "year": "2024" or "Recent" or "Not specified",
      "relevance": "Why this matters for this landing page",
      "credibility": "high" / "medium" / "low"
    }}
  ],
  "market_trends": [
    {{
      "trend": "Description of market trend",
      "impact": "How this affects {audience}"
    }}
  ],
  "supporting_facts": [
    "Additional supporting facts without specific numbers"
  ]
}}

Return ONLY valid JSON.
Focus on quality over quantity. 5-8 CREDIBLE stats better than 10 questionable ones."""
```

**Pattern-Specific Research Focus Examples:**

**Pattern 6 (Content Crisis):**
```
Research statistics about the CONTENT CRISIS:
- Creator burnout rates
- Content production time vs demand
- Supply/demand ratios (e.g., 1 photoshoot vs 100 posts needed)
- Impact of content volume on creator success
- Time spent on content creation
This is CRITICAL for Pattern 6 - emphasize the problem scale.
```

**Settings:**
- `max_output_tokens`: 2500
- `temperature`: 0.4 (low for factual research)

**Caching:** Cached by `pattern_id + audience + platform`

---

## 5. Copywriting Agent

**Purpose:** Generate all main landing page content

**Prompt Template:**

```python
f"""You are an expert copywriter for Sozee.ai, creating PSEO landing page content.

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
- Custom LORA Training in 30 minutes (hyper-realistic, trained on YOUR face)
- 1-Click TikTok Cloning (replicate viral content instantly)
- Built specifically for OnlyFans/creator platforms
- SFW & NSFW capabilities (complete flexibility)
- Solves the "1/100 content crisis" (1 photoshoot → 10,000+ photos)
- No technical skills required

**BRAND VOICE:**
Confident yet empathetic, slightly edgy. Speak directly to creator burnout and the content supply crisis. Use "you" language. Be specific with numbers (30 minutes, 1/100 ratio, etc.)

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
```

**Pattern Angle Examples:**

**Pattern 1 (Competitor Comparison):**
```
This is a DIRECT COMPARISON pattern. Your copy should:
- Emphasize head-to-head differences
- Be specific about what Sozee does better
- Focus on why creators are switching from [competitor]
- Include specific feature comparisons
- Maintain fair but confident tone
```

**Pattern 6 (Content Crisis):**
```
This is a PROBLEM-FOCUSED pattern. Your copy should:
- Agitate the content supply/demand crisis HARD
- Use statistics about creator burnout and time pressure
- Paint vivid picture of the 1/100 problem (1 photoshoot, need 100 posts)
- Position Sozee as the ONLY solution to scale without burnout
- Emphasize urgency and necessity of AI
```

**Settings:**
- `max_output_tokens`: 4000
- `temperature`: 0.8 (higher for creative variety)

---

## 6. FAQ Generator Agent

**Purpose:** Create 10 SEO-optimized Q&A pairs

**Prompt Template:**

```python
f"""You are creating FAQ content for a Sozee landing page.

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
```

**Pattern-Specific Question Types:**

**Pattern 1 (Comparison):**
```
COMPARISON QUESTIONS (focus on differences vs Higgsfield):
• How is Sozee different from Higgsfield?
• Is Sozee easier to use than Higgsfield?
• Can I switch from Higgsfield to Sozee easily?
• What features does Sozee have that Higgsfield doesn't?
• Which is better for OnlyFans creators - Sozee or Higgsfield?
```

**Pattern 2 (Best Tool):**
```
BEST TOOL QUESTIONS (focus on why it's #1):
• Why is Sozee the best AI photo generator for OnlyFans?
• What makes Sozee better than other AI tools?
• How does Sozee rank compared to alternatives?
```

**Settings:**
- `max_output_tokens`: 4000
- `temperature`: 0.6 (balanced)

---

## 7. SEO Optimizer Agent

**Purpose:** Generate meta titles, descriptions, and keywords

**Prompt Template:**

```python
f"""You are an SEO expert creating metadata for a Sozee landing page.

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
```

**Pattern Examples:**

**Pattern 1 (Comparison):**
```
Title: "Sozee vs Higgsfield for OnlyFans Creators | AI Comparison"
       (Example length: ~55 chars)

Description: "Compare Sozee and Higgsfield for OnlyFans Creators. See features, pricing, and which AI content tool solves the content crisis. Free trial available."
             (Target: 150-160 chars - emphasize differentiation + CTA)
```

**Settings:**
- `max_output_tokens`: 500
- `temperature`: 0.5 (moderate)

**Validation:** Checks character counts and warns if out of range

---

## 8. Comparison Table Agent

**Purpose:** Create feature-by-feature comparison tables (Patterns 1 & 4 only)

**Prompt Template:**

```python
f"""You are creating a feature comparison table for a landing page comparing Sozee vs {competitor}.

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
```

**Sozee Features (Factual Data):**
```json
{
  "lora_training": {
    "time": "30 minutes",
    "customization": "Fully custom - trained on YOUR face/body",
    "hyper_realistic": true
  },
  "content_support": {
    "sfw": true,
    "nsfw": true,
    "flexibility": "Complete content freedom"
  },
  "platform_focus": {
    "primary": "OnlyFans",
    "also_supports": ["Patreon", "FanVue", "Instagram", "TikTok"],
    "creator_first": true
  },
  "ease_of_use": {
    "technical_skills": "None required",
    "setup_time": "30 minutes (LORA training)",
    "learning_curve": "Minimal"
  },
  "pricing": {
    "creators": "$15/week",
    "agencies": "$33/week",
    "free_trial": true
  },
  "generation_speed": {
    "time_per_asset": "30 seconds",
    "volume": "Unlimited"
  },
  "special_features": {
    "tiktok_cloning": "1-click cloning",
    "content_crisis_solution": "1/100 ratio solver",
    "model_training": "Custom AI trained on you"
  }
}
```

**Settings:**
- `max_output_tokens`: 2000
- `temperature`: 0.3 (low for factual accuracy)

**Anti-Hallucination Protection:** Marks unknown competitor features as "Not specified"

---

## 9. Schema Markup Agent

**Purpose:** Generate Schema.org JSON-LD for SEO rich snippets

**Note:** This agent does **NOT** use Gemini API. It uses templates to generate:
- Organization schema (all pages)
- WebPage schema (all pages)
- BreadcrumbList schema (all pages)
- FAQPage schema (uses FAQ data from FAQ Generator)
- Product schema (patterns 1 & 4)
- SoftwareApplication schema (pattern 2)
- Review schema (pattern 5)

**Template Example:**

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How does Sozee compare to Higgsfield?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sozee is built specifically for OnlyFans creators..."
      }
    }
  ]
}
```

---

## 10. Quality Control Agent

**Purpose:** Validate all content before finalization

**Note:** This agent performs **automated checks** (no Gemini prompt) on:

**SEO Validation:**
```python
- Meta title: 50-60 chars?
- Meta description: 150-160 chars?
- 'Sozee' mentioned in title?
- URL slug valid (lowercase, no spaces)?
```

**Content Completeness:**
```python
- All required fields present?
- Hero section has H1 and subtitle?
- Problem section > 200 chars?
- Solution section > 150 chars?
```

**Brand Voice:**
```python
- 'Sozee' mentioned 3+ times?
- No excessive competitor praise?
- Tone consistent?
```

**Factual Accuracy:**
```python
- No hallucinated statistics?
- Competitor claims fair and factual?
```

**Uniqueness:**
```python
- No generic template language?
- Varied sentence structure?
```

**Scoring:**
```python
quality_score = (
    seo_score * 0.25 +
    completeness_score * 0.25 +
    brand_voice_score * 0.20 +
    accuracy_score * 0.20 +
    uniqueness_score * 0.10
)

if quality_score >= 0.8:
    status = "APPROVED"
elif quality_score >= 0.7:
    status = "APPROVED_WITH_WARNINGS"
else:
    status = "REJECTED"
```

---

## Prompt Engineering Best Practices Used

### 1. **Clear Role Definition**
Every prompt starts with: "You are an expert [role]..."

### 2. **Structured Output Requirement**
All prompts end with: "Return ONLY valid JSON" with exact schema

### 3. **Context Injection**
Prompts include:
- Pattern type and strategy
- Research data from previous agents
- Brand voice guidelines
- Specific variables (competitor, audience, etc.)

### 4. **Anti-Hallucination Guards**
- "Be FACTUAL - don't hallucinate"
- "If unknown, say 'Not specified'"
- "DO NOT invent statistics"
- Low temperature (0.3-0.5) for factual agents

### 5. **Example-Driven**
- Pattern-specific examples
- Sample question types
- Expected output formats

### 6. **Constraint Specification**
- Character limits (50-60 chars for titles)
- Count requirements (10 FAQs, 6-8 comparison rows)
- Credibility filters (high/medium/low)

### 7. **Cascading Context**
Each agent builds on previous agents' outputs:
```
Strategist → Blueprint
  ↓
Research Agents → Research Data
  ↓
Copywriting → Content (using blueprint + research)
  ↓
Supplementary → Enhanced Content (using content + research)
  ↓
Quality Control → Validation
```

---

## Temperature Settings by Agent Type

| Agent Type | Temperature | Reasoning |
|------------|-------------|-----------|
| Competitor Research | 0.3 | Factual accuracy |
| Audience Insight | 0.7 | Balance creativity & accuracy |
| Statistics | 0.4 | Factual with some interpretation |
| Copywriting | 0.8 | Creative variety in copy |
| FAQ Generator | 0.6 | Natural questions with accuracy |
| SEO Optimizer | 0.5 | Balance optimization & readability |
| Comparison Table | 0.3 | Factual comparisons only |

---

## Output Token Limits by Agent

| Agent | Max Tokens | Why |
|-------|------------|-----|
| Competitor Research | 2000 | Detailed feature analysis |
| Audience Insight | 3000 | Comprehensive psychology |
| Statistics | 2500 | Multiple stats + context |
| **Copywriting** | **4000** | **Full page content** |
| **FAQ Generator** | **4000** | **10 Q&A pairs** |
| SEO Optimizer | 500 | Just metadata |
| Comparison Table | 2000 | 6-8 feature rows |

---

## JSON Response Parsing

All agents use this pattern:

```python
response = self.genai_model.generate_content(
    prompt,
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=X,
        temperature=Y
    )
)

result = json.loads(response.text)
```

**With error handling:**
```python
try:
    result = json.loads(response.text)
except Exception as e:
    print(f"Error: {e}")
    return fallback_data
```

---

## Key Insights

### What Makes These Prompts Effective:

1. **Specificity** - Every prompt is tailored to exact pattern and variables
2. **Context-Rich** - Includes research data, brand voice, examples
3. **Structured Output** - Forces consistent JSON format
4. **Validation** - Multiple checks for quality and accuracy
5. **Cascading Intelligence** - Each agent builds on previous outputs
6. **Anti-Hallucination** - Explicit guards against fabricated data
7. **Pattern-Aware** - Different strategies for each of 6 patterns

### Why This Works:

- **No Generic Templates** - Each prompt customized per page
- **Research-Informed** - Content based on actual data, not assumptions
- **Brand Consistency** - Voice guidelines in every prompt
- **Quality Gates** - Multi-level validation before output
- **Caching Strategy** - Reuses research across similar pages

---

**Last Updated:** 2025-11-10
**Total Prompts:** 8 Gemini API prompts + 2 logic-based agents
