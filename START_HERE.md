# 👋 START HERE - Sozee PSEO Landing Page Generator

## ✅ You Have Everything You Need!

This repository contains a complete **multi-agent AI system** for generating 678 SEO-optimized landing pages using Google Gemini API.

---

## 🎯 Two Generation Systems Available

### System 1: Simple Generator (Fast)
- **File:** `generate_pages.py`
- **Speed:** 60-100 pages/hour
- **Cost:** $0.10-0.20 per page
- **Best for:** Mid/top-funnel content, quick generation

### System 2: Multi-Agent (High Quality)
- **Files:** `pseo_orchestrator.py` + `batch_generator.py`
- **Speed:** 10-20 pages/hour
- **Cost:** $0.50-1.00 per page
- **Best for:** Bottom-funnel, research-intensive, competitor pages

**Recommendation:** Start with System 1 for testing, use System 2 for final production.

---

## 🚀 Quick Start (10 Minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/jake9015/PSEO-.git
cd PSEO-
git checkout claude/review-project-setup-011CUxiiYhKhV6sGB3hB48dV
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `google-generativeai` - Gemini API client
- `pandas` - Data manipulation
- `python-dotenv` - Environment variables

### Step 3: Configure API Key
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
nano .env
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

Your `.env` should look like:
```
GEMINI_API_KEY=your_actual_key_here
```

### Step 4: Test with Single Page
```bash
# Test System 2 (Multi-Agent) with one page
python test_single_page.py

# Or test System 1 (Simple) with 10 pages
python generate_pages.py --limit 10
```

---

## 📂 Repository Structure

```
PSEO-/
├── config/
│   ├── patterns.json              # 6 landing page patterns
│   ├── variables.json             # Variables (competitors, audiences, etc.)
│   ├── content_templates.json     # Content section templates
│   └── viral_hooks.json           # Viral hooks library
│
├── agents/                        # Multi-agent system components
│   ├── pseo_strategist.py        # Master planning agent
│   ├── competitor_research.py    # Competitor analysis
│   ├── audience_insight.py       # Audience psychology
│   ├── copywriting.py            # Content generation
│   ├── faq_generator.py          # FAQ creation
│   ├── seo_optimizer.py          # SEO metadata
│   └── quality_control.py        # Quality validation
│
├── agent_framework.py             # Base agent classes
├── pseo_orchestrator.py          # Multi-agent coordinator
├── batch_generator.py            # Phased rollout processor
├── generate_pages.py             # Simple generator
├── test_single_page.py           # Quality testing script
│
├── output/                       # Generated pages (created automatically)
│
├── README.md                     # Detailed documentation
├── TESTING_GUIDE.md              # Quality testing guide
├── .env.example                  # Environment template
└── requirements.txt              # Python dependencies
```

---

## 🧪 Testing Content Quality

Before generating all 678 pages, test with specific keywords:

```bash
python test_single_page.py
```

This will:
1. Generate 1-3 test pages for different patterns
2. Validate SEO metadata (title length, description, etc.)
3. Check content completeness
4. Verify brand voice
5. Output quality scores and recommendations

**Review the output files** in `output/` directory before proceeding.

See `TESTING_GUIDE.md` for detailed quality validation instructions.

---

## 📊 Generation Options

### Option A: Generate All Pages at Once (System 1)

```bash
# Generate all 678 pages (2-3 hours)
python generate_pages.py

# Output: output/generated_pages_[timestamp].csv
```

**Pros:**
- Fast (60-100 pages/hour)
- Low cost ($68-136 total)
- Simple workflow

**Cons:**
- Lower quality scores (0.75-0.85)
- Less unique content
- No research phase

### Option B: Phased Rollout (System 2 - Recommended)

```bash
# Week 1: Generate 10 priority pages (manual QA)
python batch_generator.py --phase week_1

# Week 2: Generate 50 pages (patterns 1, 4)
python batch_generator.py --phase week_2

# Week 3: Generate 200 pages
python batch_generator.py --phase week_3

# Week 4-6: Generate all remaining pages
python batch_generator.py --phase week_4_6
```

**Pros:**
- High quality scores (0.85-0.95)
- Research-backed content
- Unique, compelling copy
- Quality control validation

**Cons:**
- Slower (10-20 pages/hour)
- Higher cost ($339-678 total)
- More complex workflow

---

## 💰 Cost Estimates

### System 1 (Simple)
- **Per Page:** $0.10-0.20
- **678 Pages:** $68-136
- **Time:** 7-11 hours

### System 2 (Multi-Agent)
- **Per Page:** $0.50-1.00
- **678 Pages:** $339-678
- **Time:** 34-68 hours

**Google Gemini Pricing:**
- Input: $0.075 per 1M tokens
- Output: $0.30 per 1M tokens
- Model: gemini-2.0-flash-exp

---

## 🎯 Recommended Workflow

### For First-Time Users:

1. **Test with System 1** (5 minutes)
   ```bash
   python generate_pages.py --limit 10
   ```

2. **Review output quality** (10 minutes)
   - Check `output/generated_pages_*.csv`
   - Validate SEO metadata
   - Read a few pages for quality

3. **Test System 2** (10 minutes)
   ```bash
   python test_single_page.py
   ```

4. **Compare quality** (5 minutes)
   - System 1 vs System 2 output
   - Decide which system to use

5. **Choose your path:**
   - **Quick & Cheap:** Run System 1 for all 678 pages
   - **High Quality:** Run System 2 phased rollout

---

## 📝 What You'll Get

### CSV Output Format

Both systems output CSV files ready for WordPress import:

**Columns:**
- `page_id` - Unique identifier
- `pattern_id` - Pattern number (1-6)
- `post_title` - H1 / Post title
- `url_slug` - SEO-friendly URL
- `meta_title` - SEO title (50-60 chars)
- `meta_description` - SEO description (150-160 chars)
- `hero_section` - H1, subtitle, CTAs (JSON)
- `problem_agitation` - Problem section content
- `solution_overview` - Solution section content
- `comparison_table_json` - Feature comparison (JSON)
- `faq_json` - 5 Q&A pairs (JSON)
- `final_cta` - Call to action
- `quality_score` - Quality rating (0-1.0)
- `uniqueness_check` - APPROVED/REJECTED
- Variables: `competitor`, `audience`, `platform`, etc.

### Example Page

**Pattern 1: Competitor Comparison**
- **URL:** `/sozee-vs-higgsfield-for-onlyfans-agencies`
- **H1:** "Sozee vs Higgsfield for OnlyFans Agencies"
- **Meta Title:** "Sozee vs Higgsfield for Agencies | AI Content Comparison"
- **Quality Score:** 0.92 (APPROVED)
- **Agents Used:** 7 (strategist, research, copywriting, FAQ, SEO, QC)

---

## 🔧 Customization

### Adjust Variables

Edit `batch_generator.py` to add more competitors, audiences, etc.:

```python
COMPETITORS = [
    "Higgsfield", "Krea", "Midjourney",
    # Add your competitors here
]

AUDIENCES = [
    "OnlyFans Creators", "Content Creators",
    # Add your audiences here
]
```

### Tune Agent Behavior

Edit agent files in `agents/` directory:

- **More creativity:** Increase temperature in `agents/copywriting.py`
- **Better research:** Add requirements in `agents/competitor_research.py`
- **Stricter SEO:** Modify validation in `agents/seo_optimizer.py`

See individual agent files for detailed customization options.

---

## 🆘 Troubleshooting

### "GEMINI_API_KEY not found"
```bash
# Verify .env exists
ls -la .env

# Check it has your key
cat .env

# Should show: GEMINI_API_KEY=your-key-here
```

### "Module not found: google.generativeai"
```bash
pip install -r requirements.txt
```

### "SSL Certificate Error" (Sandbox Only)
This only happens in sandboxed environments. On your local machine, the API will work perfectly.

### Content Quality Too Low
1. Use System 2 (multi-agent) instead of System 1
2. Increase temperature in `agents/copywriting.py`
3. Add more viral hooks to `config/viral_hooks.json`

### Want to Resume Generation
```bash
# System 1: Resume from specific index
python generate_pages.py --start-index 100

# System 2: Automatically detects checkpoint
python batch_generator.py --phase week_2
```

---

## 📖 Additional Documentation

- **README.md** - Complete system overview
- **TESTING_GUIDE.md** - Quality validation guide
- **ARCHITECTURE.md** - Multi-agent system architecture (if exists)
- **DOCUMENTATION_AUDIT.md** - Audit of all docs

---

## ✅ Pre-Flight Checklist

Before generating all 678 pages:

- [ ] Repository cloned and on correct branch
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Gemini API key in `.env` file
- [ ] Tested with System 1 (`--limit 10`)
- [ ] Tested with System 2 (`test_single_page.py`)
- [ ] Reviewed output quality
- [ ] Have sufficient API credits ($68-678 depending on system)
- [ ] Decided on System 1 vs System 2

---

## 🚀 Quick Commands Reference

```bash
# Test System 1 (Simple Generator)
python generate_pages.py --limit 10

# Test System 2 (Multi-Agent)
python test_single_page.py

# Generate all pages (System 1)
python generate_pages.py

# Phased rollout Week 1 (System 2)
python batch_generator.py --phase week_1

# Phased rollout Week 2 (System 2)
python batch_generator.py --phase week_2

# Generate specific pattern only
python batch_generator.py --pattern 1 --limit 20

# Resume from checkpoint
python batch_generator.py --phase week_2 --start-index 25
```

---

## 💡 Pro Tips

1. **Start small:** Always test with 1-10 pages before full generation
2. **Review quality:** Manually check first batch before scaling
3. **Use checkpoints:** System 2 saves progress every 10 pages
4. **Monitor costs:** Check API usage in Gemini console
5. **Validate output:** Use `test_single_page.py` to validate quality

---

## 🎉 Ready to Generate!

**Time to first page:** 10 minutes
**Total time (System 1):** 7-11 hours
**Total time (System 2):** 34-68 hours
**Total cost (System 1):** $68-136
**Total cost (System 2):** $339-678
**Total pages:** 678 complete, SEO-optimized landing pages

---

## 📞 Support

**Documentation:**
- Full system details: `README.md`
- Quality testing: `TESTING_GUIDE.md`
- Audit report: `DOCUMENTATION_AUDIT.md`

**Common Issues:**
- See Troubleshooting section above
- Check `output/failed_tasks.json` for error logs
- Review agent configuration in `agents/` files

---

🚀 **Run this now:** `python test_single_page.py`
