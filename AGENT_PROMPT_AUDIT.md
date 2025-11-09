# Agent Prompt Audit for PSEO Landing Page Copywriting

**Date:** November 9, 2025
**Purpose:** Ensure all agent prompts are optimized for PSEO pattern-based landing page generation

---

## 🎯 Use Case Reminder

**Goal:** Generate landing page copywriting that fits specific PSEO patterns

**Patterns:**
1. Competitor Comparison - "Sozee vs {Competitor} for {Audience}"
2. Best Tool - "Best {Use_Case} for {Audience}"
3. Direct Tool - "{Platform} {Tool_Type}"
4. Alternative - "{Competitor} Alternative for {Audience}"
5. Review - "Sozee Review for {Audience}"
6. Content Crisis - "Solve the Content Crisis for {Platform} {Audience}"

---

## 📊 Audit Findings

### ✅ **GOOD: Pattern Configuration**

**File:** `config/patterns.json`

**Status:** ✅ Excellent

**Strengths:**
- Clear H1 formulas for each pattern
- Specific eyebrows per pattern ("Head-to-Head Comparison", "Better Alternative", etc.)
- Pattern-specific CTAs
- Shows comparison table flag
- All variables properly mapped

**Recommendation:** No changes needed

---

### ✅ **GOOD: Content Templates**

**File:** `config/content_templates.json`

**Status:** ✅ Excellent but UNDERUTILIZED

**Strengths:**
- Pattern-specific prompt guidance for each section
- Detailed examples per pattern
- Audience-specific pain points
- Clear formatting instructions
- Proper character/token limits

**CRITICAL ISSUE:**
❌ **These excellent templates are NOT being used by the multi-agent system!**

The multi-agent copywriting agent has its own generic prompt that doesn't leverage this detailed pattern-specific guidance.

**Recommendation:** Integrate content_templates.json into copywriting agent

---

### ⚠️ **NEEDS IMPROVEMENT: Copywriting Agent**

**File:** `agents/copywriting.py`

**Current Status:** ⚠️ Generic, not pattern-specific

**Issues Found:**

1. **Generic Prompt (Line 66-123)**
   ```python
   prompt = f"""You are an expert copywriter for Sozee.ai, creating landing page content.

   **Pattern**: {blueprint.get('pattern_name', 'Unknown')}
   **Target Audience**: {blueprint.get('pseo_variables', {}).get('audience', 'Creators')}
   ```

   ❌ **Problem:** Only mentions pattern name, doesn't use pattern-specific guidance
   ❌ **Problem:** Doesn't reference H1 formula or eyebrow from pattern config
   ❌ **Problem:** Doesn't use content_templates.json detailed instructions

2. **Missing Pattern-Specific Instructions**
   - Pattern 1 (Comparison): Should emphasize differentiation from competitor
   - Pattern 2 (Best): Should emphasize top ranking
   - Pattern 4 (Alternative): Should emphasize "why switch"
   - Pattern 6 (Crisis): Should emphasize the 1/100 problem

   ❌ **Current:** Generic "create landing page content"
   ✅ **Should be:** Pattern-specific copywriting instructions

3. **Missing H1 Context**
   ```python
   **Your Task**: Generate complete landing page content
   ```

   ❌ **Problem:** Doesn't include the actual H1 title that was generated from the pattern formula
   ✅ **Should include:** The specific H1 like "Sozee vs Higgsfield for OnlyFans Agencies"

4. **Viral Hook Usage**
   ```python
   viral_hook = random.choice(self.viral_hooks)
   **Viral Hook to Use**: {viral_hook}
   ```

   ⚠️ **Problem:** Tells agent to use it but doesn't specify HOW
   ✅ **Should specify:** "Use as opening sentence of problem section"

5. **Research Data Integration**
   ```python
   **Research Data:**
   {json.dumps(research_data, indent=2)[:2000]}
   ```

   ⚠️ **Problem:** Dumps JSON but doesn't instruct how to use it
   ✅ **Should specify:** "Use competitor features/pricing in comparison table"

**Recommendation:** Major update to integrate pattern-specific prompts from content_templates.json

---

### ⚠️ **NEEDS IMPROVEMENT: FAQ Generator**

**File:** `agents/faq_generator.py`

**Current Status:** ⚠️ Basic, not leveraging pattern templates

**Issues Found:**

1. **Generic FAQ Prompt (Lines 40-87)**
   ```python
   prompt = f"""You are creating FAQ content for a Sozee landing page.

   **Page Context**: {pattern_context}
   **Pattern ID**: {pattern_id}
   ```

   ❌ **Problem:** Creates own pattern context instead of using detailed FAQ template
   ❌ **Missing:** Pattern-specific question types from content_templates.json

   **Content templates has:**
   - Pattern 1: "How is Sozee different from {competitor}?"
   - Pattern 2: "What makes this the best {use_case} for {audience}?"
   - Pattern 4: "Why should I switch from {competitor}?"

   **Current agent:** Generic "create FAQ for pattern"

**Recommendation:** Use FAQ templates from content_templates.json

---

### ⚠️ **NEEDS IMPROVEMENT: SEO Optimizer**

**File:** `agents/seo_optimizer.py`

**Current Status:** ⚠️ Basic, not leveraging meta templates

**Issues Found:**

1. **Generic Meta Description Prompt**
   ```python
   **Output as JSON:**
   {
     "meta_title": "SEO optimized title 50-60 chars",
     "meta_description": "Compelling description 150-160 chars",
     "focus_keyword": "primary keyword"
   }
   ```

   ❌ **Problem:** No pattern-specific examples
   ❌ **Missing:** Detailed meta description guidance from content_templates.json

   **Content templates has:**
   - Pattern-specific examples
   - Benefit-focused language
   - CTA ending phrases

   **Current agent:** Generic "write meta description"

**Recommendation:** Use meta templates from content_templates.json

---

### ✅ **GOOD: PSEO Strategist**

**File:** `agents/pseo_strategist.py`

**Status:** ✅ Good

**Strengths:**
- Correctly maps patterns to strategies
- Identifies Model 1 vs Model 2
- Determines required agents per pattern
- Builds proper page IDs
- Creates research requirements

**Minor Improvements Possible:**
- Could pass pattern config (eyebrow, CTAs) to copywriting agent
- Could include H1 formula in blueprint

**Recommendation:** Minor enhancements to pass more pattern context

---

### ✅ **GOOD: Competitor Research**

**File:** `agents/competitor_research.py`

**Status:** ✅ Good for landing pages

**Strengths:**
- Researches factual data
- Focuses on features, pricing, pros/cons
- Notes NSFW support (relevant for creators)
- Identifies limitations for specific audience

**Recommendation:** No changes needed

---

### ✅ **GOOD: Audience Insight**

**File:** `agents/audience_insight.py`

**Status:** ✅ Good for landing pages

**Strengths:**
- Researches pain points (critical for landing pages)
- Identifies desires and objections
- Maps emotional triggers
- Provides current solutions (for positioning)

**Recommendation:** No changes needed

---

### ✅ **GOOD: Quality Control**

**File:** `agents/quality_control.py`

**Status:** ✅ Good

**Strengths:**
- Validates SEO metadata (title 50-60, description 150-160)
- Checks content completeness
- Verifies brand voice (Sozee mentions)
- Detects factual errors
- Checks uniqueness

**Recommendation:** No changes needed

---

## 🔧 Recommended Fixes

### Priority 1: Copywriting Agent (CRITICAL)

**Current:** Generic landing page prompt
**Should be:** Pattern-specific copywriting using content_templates.json

**Changes Needed:**

1. **Load pattern configuration**
   ```python
   # Get pattern details
   pattern_config = self._get_pattern_config(blueprint['pattern_id'])
   h1 = pattern_config['h1_formula'].format(**variables)
   eyebrow = pattern_config.get('eyebrow', '')
   ```

2. **Use content template prompts**
   ```python
   # Load content templates
   with open('config/content_templates.json') as f:
       templates = json.load(f)

   # Get pattern-specific guidance
   problem_template = templates['sections']['problem_agitation']['prompt_template']
   ```

3. **Include H1 in prompt**
   ```python
   **H1 Title**: {h1}
   **Eyebrow**: {eyebrow}
   **Pattern-Specific Angle**: {pattern_angle}
   ```

4. **Pattern-specific instructions**
   ```python
   if pattern_id == '1':  # Competitor Comparison
       angle = f"Emphasize how Sozee differs from {competitor}"
   elif pattern_id == '4':  # Alternative
       angle = f"Explain why users should switch from {competitor} to Sozee"
   ```

### Priority 2: FAQ Generator (HIGH)

**Changes Needed:**

1. **Load FAQ templates**
   ```python
   with open('config/content_templates.json') as f:
       templates = json.load(f)
   faq_template = templates['sections']['faq']
   ```

2. **Use pattern-specific question types**
   - Pattern 1: Focus on differences vs competitor
   - Pattern 2: Focus on why it's the best
   - Pattern 4: Focus on switching benefits

### Priority 3: SEO Optimizer (MEDIUM)

**Changes Needed:**

1. **Load meta templates**
   ```python
   meta_template = templates['sections']['meta_description']
   ```

2. **Use pattern-specific examples**
   - Include example for each pattern
   - Emphasize click-through optimization

---

## 📊 Impact Analysis

### Current System

**Copywriting Quality:**
- ⚠️ Generic: Doesn't differentiate between patterns
- ⚠️ Inconsistent: Each generation may interpret pattern differently
- ⚠️ Missing context: Doesn't use excellent pattern-specific guidance

**Example Output:**
```
H1: "Sozee vs Higgsfield for OnlyFans Agencies"
Subtitle: "Transform your content creation workflow" ❌ Generic
Problem: "Content creation is challenging..." ❌ Not pattern-specific
```

### After Fixes

**Copywriting Quality:**
- ✅ Pattern-specific: Emphasizes comparison/alternative/best ranking
- ✅ Consistent: Uses proven template formulas
- ✅ Contextual: Leverages detailed guidance from content_templates.json

**Example Output:**
```
H1: "Sozee vs Higgsfield for OnlyFans Agencies"
Eyebrow: "Head-to-Head Comparison" ✅ From pattern config
Subtitle: "Both promise AI content. Only one solves the content crisis." ✅ Pattern-specific
Problem: "If you're an agency, you've heard about Higgsfield..." ✅ Comparison angle
```

---

## ✅ Summary

### What's Working

1. ✅ Pattern configuration (patterns.json)
2. ✅ Content templates (content_templates.json) - excellent but unused
3. ✅ PSEO Strategist - correct pattern mapping
4. ✅ Research agents - gathering right data
5. ✅ Quality Control - validating correctly

### What Needs Fixing

1. ❌ **Copywriting Agent** - Not using pattern-specific prompts
2. ❌ **FAQ Generator** - Not using FAQ templates
3. ❌ **SEO Optimizer** - Not using meta templates

### Impact of Fixes

**Before:**
- Generic landing pages
- Inconsistent pattern adherence
- Missing pattern-specific angles

**After:**
- Pattern-specific copywriting
- Consistent with proven templates
- Proper emphasis per pattern type

---

## 🎯 Next Steps

1. **Update Copywriting Agent** (agents/copywriting.py)
   - Integrate content_templates.json
   - Add pattern-specific instructions
   - Include H1 and eyebrow in prompts

2. **Update FAQ Generator** (agents/faq_generator.py)
   - Use FAQ templates
   - Pattern-specific question types

3. **Update SEO Optimizer** (agents/seo_optimizer.py)
   - Use meta templates
   - Pattern-specific examples

4. **Test with Single Page** (test_single_page.py)
   - Verify pattern adherence
   - Check for pattern-specific language

---

**Priority:** HIGH - The excellent pattern-specific guidance in content_templates.json is not being used by the multi-agent system!
