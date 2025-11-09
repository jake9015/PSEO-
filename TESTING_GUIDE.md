# PSEO Content Quality Testing Guide

## 🎯 How to Test Content for a Specific Keyword

### Quick Test (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key in .env
echo "GEMINI_API_KEY=your-key-here" > .env

# 3. Run the test script
python test_single_page.py
```

### What to Test

The test script will generate pages for 3 different keyword types:

1. **Bottom-Funnel (Comparison):** "sozee vs higgsfield for onlyfans agencies"
2. **Mid-Funnel (Best Tool):** "best ai photo generator for onlyfans creators"
3. **Bottom-Funnel (Alternative):** "krea alternative for content creators"

### Quality Validation Checklist

The script automatically validates:

#### ✅ **SEO Quality**
- [ ] Meta title 50-60 characters
- [ ] Meta description 150-160 characters
- [ ] Title contains "Sozee" brand
- [ ] Title contains target keyword
- [ ] URL slug is lowercase, no spaces
- [ ] Description has clear CTA

#### ✅ **Content Completeness**
- [ ] H1 matches search intent
- [ ] Compelling subtitle present
- [ ] Problem section (200+ chars)
- [ ] Solution section (150+ chars)
- [ ] 5 FAQ pairs generated
- [ ] 2-3 feature sections

#### ✅ **Brand Voice**
- [ ] Multiple "Sozee" mentions
- [ ] References key features (LORA, TikTok clone, etc.)
- [ ] Mentions target audience naturally
- [ ] Confident but empathetic tone

#### ✅ **Factual Accuracy** (Model 2 only)
- [ ] Competitor info is accurate
- [ ] No hallucinated pricing
- [ ] Features are real
- [ ] Research sources logged

#### ✅ **Uniqueness**
- [ ] No generic marketing fluff
- [ ] Varied sentence structure
- [ ] Specific examples used
- [ ] Natural keyword integration

## 📊 Expected Output

### Example: "Sozee vs Higgsfield for OnlyFans Agencies"

**Meta Title:**
```
Sozee vs Higgsfield for Agencies | AI Content Comparison 2025
```
✅ 58 chars, has brand, has keyword

**Meta Description:**
```
Compare Sozee vs Higgsfield for OnlyFans agencies. See features, pricing, and why agencies choose Sozee's custom LORA training. Start free trial today.
```
✅ 157 chars, has CTA

**H1:**
```
Sozee vs Higgsfield for OnlyFans Agencies
```
✅ Matches search intent exactly

**Content Preview:**
```
# The Agency Challenge

Managing content creation for dozens of creators is overwhelming.
Your team spends hours coordinating photoshoots, editing content,
and trying to keep up with demand...

[Uses specific pain points from Audience Insight Agent]
```

**FAQ Example:**
```
Q: Does Sozee work better than Higgsfield for OnlyFans agencies?
A: Sozee is specifically built for adult content creation with
   NSFW support and 30-minute LORA training, while Higgsfield
   focuses on general video generation. Agencies choose Sozee
   for its creator-specific features.
```

**Quality Score:** 0.92 (APPROVED)

## 🔍 Manual Review Steps

After running the test script:

### 1. Read the JSON Output
```bash
cat output/test_competitor_comparison.json | python -m json.tool
```

### 2. Check These Elements

**Does the content answer the search intent?**
- Comparison pages: Shows clear differences
- Best tool pages: Explains why Sozee is #1
- Alternative pages: Addresses why users switch

**Is the keyword naturally integrated?**
- Not keyword-stuffed
- Flows conversationally
- Uses variations naturally

**Does it convert?**
- Clear value proposition
- Addresses objections
- Strong CTAs throughout

**Is it unique?**
- Different from other pages
- Uses specific details
- Avoids template language

### 3. Test Search Ranking Potential

**On-Page SEO:**
- Title tag optimized
- Meta description compelling
- URL structure clean
- H1 matches intent
- Internal linking opportunities

**Content Quality:**
- Comprehensive (800+ words)
- Answers related questions (FAQ)
- Uses semantic keywords naturally
- No thin content

**User Experience:**
- Scannable sections
- Clear hierarchy
- Quick value communication
- Mobile-friendly structure

## 📈 Quality Score Guide

**0.9-1.0:** Excellent - Ready for immediate publication
**0.8-0.89:** Good - Minor tweaks, publish
**0.7-0.79:** Acceptable - Review warnings, fix before publishing
**<0.7:** Reject - Regenerate with different prompts

## 🧪 Testing Different Keywords

Want to test a custom keyword? Modify `test_single_page.py`:

```python
# Test your own keyword
page = orchestrator.generate_page(
    pattern_id='1',  # Pattern ID (1-6)
    variables={
        'competitor': 'YourCompetitor',
        'audience': 'YourAudience'
    }
)

validate_page_quality(page, expected_keyword='your keyword here')
```

## 🚨 Red Flags to Watch For

### Content Issues
❌ Generic phrases: "revolutionize", "game-changer", "cutting-edge"
❌ Repetitive sentence starts
❌ Vague claims without specifics
❌ Missing brand mentions
❌ No clear CTA

### SEO Issues
❌ Title too long/short
❌ Description not compelling
❌ Missing target keyword
❌ URL has spaces or capitals

### Factual Issues (Model 2)
❌ Fake pricing claims
❌ Made-up competitor features
❌ Unsourced statistics
❌ Hallucinated capabilities

## ✅ Green Flags (Good Quality)

### Content Quality
✅ Specific pain points mentioned
✅ Varied sentence structure
✅ Natural keyword usage
✅ Clear value differentiation
✅ Emotional triggers used
✅ Addresses objections

### SEO Quality
✅ Perfect meta lengths
✅ Compelling click-worthy title
✅ Action-oriented description
✅ Clean URL structure

### Research Quality (Model 2)
✅ Accurate competitor info
✅ Real features compared
✅ Sources documented
✅ No hallucinations

## 🎯 When to Proceed with Batch Generation

**Proceed to Week 1 (10 pages) if:**
- ✅ Quality score consistently 0.8+
- ✅ Keywords naturally integrated
- ✅ Meta data within limits
- ✅ Content is unique and compelling
- ✅ No factual errors detected

**Hold and adjust if:**
- ❌ Quality scores below 0.7
- ❌ Content feels template-y
- ❌ Keywords forced or stuffed
- ❌ Meta data consistently off
- ❌ Factual inaccuracies

## 🔧 Tuning for Better Results

If content quality is low:

### Increase Uniqueness
Edit `agents/copywriting.py`:
```python
temperature=0.9  # Increase from 0.8 for more variety
```

### Improve Research Depth
Edit `agents/competitor_research.py`:
```python
# Add more required_data fields
required_data = [
    'features_list',
    'pricing_tiers',
    'pros_cons',
    'audience_fit',
    'nsfw_support',
    'api_access',  # Add more
    'integration_options'
]
```

### Strengthen Brand Voice
Edit `agents/copywriting.py` prompt:
```python
**Brand Voice**: Even more confident. Focus on specific numbers:
- 30-minute LORA training (not "fast")
- 1/100 content supply/demand ratio (not "high demand")
- Built for OnlyFans (not "creators generally")
```

### Adjust SEO Requirements
Edit `agents/seo_optimizer.py`:
```python
# Stricter validation
if len(metadata['meta_title']) < 55 or len(metadata['meta_title']) > 60:
    # Regenerate instead of warning
```

## 📞 Support

Questions about quality?
1. Run `python test_single_page.py` first
2. Review output JSON files manually
3. Check quality score and warnings
4. Adjust agent prompts if needed
5. Re-test before batch generation

## 🚀 Next Steps After Testing

1. **Test passes:** Run `python batch_generator.py --phase week_1`
2. **Manual QA Week 1:** Review all 10 pages
3. **Monitor Search Console:** Check for indexing issues
4. **Adjust if needed:** Tune agents based on results
5. **Scale up:** Week 2, 3, 4-6

---

**Remember:** Quality over quantity. Get 10 perfect pages before generating 678.
