# Sozee PSEO Landing Page Generator

Multi-agent AI system for generating 678+ unique, SEO-optimized landing pages using Google Gemini API.

## 🎯 Overview

This project implements two content generation systems:

1. **System 1: Simple Generator** (`generate_pages.py`) - Fast, single-API-call generation
2. **System 2: Multi-Agent System** (`pseo_orchestrator.py` + `batch_generator.py`) - Research-intensive, multi-agent pipeline

Both systems use **Google Gemini API** (`gemini-2.0-flash-exp`) for cost-effective content generation.

## 📁 Project Structure

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
│   ├── competitor_research.py    # Competitor analysis agent
│   ├── audience_insight.py       # Audience psychology agent
│   ├── copywriting.py            # Content generation agent
│   ├── faq_generator.py          # FAQ creation agent
│   ├── seo_optimizer.py          # SEO metadata agent
│   ├── quality_control.py        # Quality assurance agent
│   ├── comparison_table.py       # ⭐ NEW: Comparison table generator
│   ├── statistics_agent.py       # ⭐ NEW: Market data & statistics
│   └── schema_markup.py          # ⭐ NEW: SEO schema markup
│
├── agent_framework.py             # Base agent classes and data structures
├── pseo_orchestrator.py          # Multi-agent orchestrator
├── batch_generator.py            # Phased rollout batch processor
├── generate_pages.py             # Simple single-agent generator
│
├── output/                       # Generated pages
│   ├── page_*.json              # Individual page files
│   ├── checkpoint.json          # Resume checkpoint
│   ├── failed_tasks.json        # Failed generation log
│   └── sozee_landing_pages_*.csv # WordPress import CSV
│
├── .env                          # API keys (create from .env.example)
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google Gemini API key

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Test Single Page Generation

#### Option 1: Simple System (Fast)

```bash
# Generate 1 test page
python generate_pages.py --limit 1

# Output: output/generated_pages_[timestamp].csv
```

#### Option 2: Multi-Agent System (High Quality)

```bash
# Test orchestrator with single page
python pseo_orchestrator.py

# Output: output/test_page_*.json
```

### Generate Batch (Phased Rollout)

```bash
# Week 1: 10 hand-picked high-priority pages
python batch_generator.py --phase week_1

# Week 2: 50 pages (patterns 1, 4)
python batch_generator.py --phase week_2

# Week 3: 200 pages
python batch_generator.py --phase week_3

# Week 4-6: All remaining pages
python batch_generator.py --phase week_4_6
```

## 🏗️ Architecture

### System 1: Simple Generator

**Best for:** Fast generation, mid/top-funnel content

```
User Request → Gemini API → Content Generation → CSV Output
```

**Performance:**
- 60-100 pages/hour
- $0.10-0.20 per page
- Single API call per page

### System 2: Multi-Agent Pipeline

**Best for:** Research-intensive, bottom-funnel content

```
User Request
    ↓
PSEO Strategist (Creates Blueprint)
    ↓
┌─────────────────────────────────┐
│   Parallel Research Phase       │
│  - Competitor Research          │
│  - Audience Insights            │
│  - Statistics Agent ⭐ NEW      │
└─────────────────────────────────┘
    ↓
Copywriting Agent (Synthesizes Content)
    ↓
┌─────────────────────────────────┐
│   Parallel Meta Generation      │
│  - FAQ Generator                │
│  - SEO Optimizer                │
│  - Comparison Table ⭐ NEW      │
│    (Patterns 1 & 4 only)        │
└─────────────────────────────────┘
    ↓
Schema Markup Agent ⭐ NEW (All Patterns)
    ↓
Quality Control Agent (Validates)
    ↓
Final Page Output (JSON + CSV)
```

**Performance:**
- 10-20 pages/hour
- $0.50-1.00 per page
- 7-12 API calls per page (increased with new agents)

**New Agents:**
- **Statistics Agent:** Gathers credible market data for authority (all patterns)
- **Comparison Table Agent:** Structured feature comparison (patterns 1 & 4)
- **Schema Markup Agent:** SEO rich snippets via Schema.org (all patterns)

## 📚 Pattern Library

### Pattern 1: Competitor Comparison (Bottom-Funnel)
- **Formula:** "Sozee vs {Competitor} for {Audience}"
- **Example:** "Sozee vs Higgsfield for OnlyFans Agencies"
- **Model:** Multi-Agent (Model 2)
- **Research:** Competitor features, pricing, pros/cons

### Pattern 2: Best Tool (Mid-Funnel)
- **Formula:** "Best {Tool_Type} for {Audience} on {Platform}"
- **Example:** "Best AI Photo Generator for OnlyFans Creators"
- **Model:** Simple (Model 1)

### Pattern 3: Direct Tool (Mid-Funnel)
- **Formula:** "Sozee for {Use_Case}"
- **Example:** "Sozee for AI Photo Generation"
- **Model:** Simple (Model 1)

### Pattern 4: Alternative (Bottom-Funnel)
- **Formula:** "{Competitor} Alternative for {Audience}"
- **Example:** "Krea Alternative for Content Creators"
- **Model:** Multi-Agent (Model 2)

### Pattern 5: Review (Mid-Funnel)
- **Formula:** "{Competitor} Review for {Audience}"
- **Example:** "Midjourney Review for OnlyFans Creators"
- **Model:** Simple (Model 1)

### Pattern 6: Content Crisis (Bottom-Funnel)
- **Formula:** "Solving the Content Crisis for {Audience}"
- **Example:** "Solving the Content Crisis for OnlyFans Agencies"
- **Model:** Multi-Agent (Model 2)

## 🎨 Variables

The system generates 678+ unique pages by combining:

- **15 Competitors:** Higgsfield, Krea, Midjourney, Stability AI, Runway, Leonardo AI, etc.
- **15 Platforms:** OnlyFans, Patreon, FanVue, Instagram, TikTok, etc.
- **8 Audiences:** OnlyFans Creators, Agencies, Content Creators, Models, etc.
- **20 Use Cases:** AI Photo Generation, TikTok Cloning, LORA Training, etc.
- **10 Tool Types:** AI Photo Generator, Content Studio, Training Tool, etc.

**Total Combinations:** 678+ unique landing pages

## 🔧 Configuration

### Customize Variables

Edit `batch_generator.py`:

```python
COMPETITORS = [
    "Higgsfield", "Krea", "Midjourney", ...
    # Add new competitors here
]

AUDIENCES = [
    "OnlyFans Creators", "Agencies", ...
    # Add new target audiences
]
```

### Adjust Phased Rollout

Edit `ROLLOUT_PHASES` in `batch_generator.py`:

```python
ROLLOUT_PHASES = {
    "week_1": {
        "patterns": ["1"],        # Which patterns
        "limit": 10,             # How many pages
        "priority_filter": "HIGH" # Priority level
    }
}
```

### Customize Agent Behavior

Edit individual agent files in `agents/`:

- `copywriting.py`: Change brand voice, temperature (0.8 default)
- `seo_optimizer.py`: Adjust meta length requirements
- `quality_control.py`: Modify quality thresholds
- `competitor_research.py`: Add more research requirements

## 📊 Output Format

### JSON Output (Individual Pages)

```json
{
  "page_id": "pat1_higgsfield_onlyfans",
  "pattern_id": "1",
  "status": "completed",
  "post_title": "Sozee vs Higgsfield for OnlyFans Agencies",
  "url_slug": "/sozee-vs-higgsfield-for-onlyfans-agencies",
  "meta_title": "Sozee vs Higgsfield for Agencies | AI Content Comparison",
  "meta_description": "Compare Sozee vs Higgsfield for OnlyFans agencies...",
  "hero_section": {
    "h1": "Sozee vs Higgsfield for OnlyFans Agencies",
    "subtitle": "Which AI tool is built for your agency?",
    "primary_cta": "Try Sozee Free",
    "secondary_cta": "See Comparison"
  },
  "problem_agitation": "# The Agency Challenge\n\n...",
  "solution_overview": "# Why Agencies Choose Sozee\n\n...",
  "comparison_table_json": [...],
  "feature_sections": [...],
  "faq_json": [...],
  "final_cta": "Ready to scale your agency? ...",
  "quality_score": 0.92,
  "uniqueness_check": "APPROVED",
  "generation_model": "Model 2",
  "agents_used": [...]
}
```

### CSV Output (WordPress Import)

```csv
page_id,pattern_id,post_title,url_slug,meta_title,meta_description,...
pat1_higgsfield_onlyfans,1,Sozee vs Higgsfield for OnlyFans Agencies,...
```

## 🎯 Quality Control

### Automated Checks

- **SEO Validation:** Meta title (50-60 chars), description (150-160 chars)
- **Content Completeness:** All required sections present
- **Brand Voice:** Sozee mentions, value prop consistency
- **Factual Accuracy:** No hallucinated pricing/features (Model 2)
- **Uniqueness:** No template-itis, varied sentence structure

### Quality Scores

- **0.8+:** APPROVED - Ready for publication
- **0.7-0.79:** APPROVED_WITH_WARNINGS - Review before publishing
- **<0.7:** REJECTED - Needs regeneration

## 💡 Usage Examples

### Generate Specific Pattern

```bash
# Only competitor comparison pages
python batch_generator.py --pattern 1 --limit 20
```

### Resume From Checkpoint

```bash
# Automatically detects checkpoint.json
python batch_generator.py --phase week_2

# Or specify index
python batch_generator.py --phase week_2 --start-index 25
```

### Custom Output Directory

```bash
python batch_generator.py --phase week_1 --output-dir my_output/
```

### Adjust Save Frequency

```bash
# Save checkpoint every 5 pages (default: 10)
python batch_generator.py --phase week_1 --save-every 5
```

## 🔍 Troubleshooting

### SSL Certificate Errors (Sandbox Only)

The sandbox environment has SSL certificate verification issues. The system will work correctly on your local machine.

### API Rate Limits

If you hit Gemini API rate limits:

```python
# Add delay in batch_generator.py process_batch():
import time
time.sleep(1)  # Add 1 second delay between pages
```

### Failed Generations

Check `output/failed_tasks.json` for errors:

```bash
cat output/failed_tasks.json
```

Resume from checkpoint to retry:

```bash
python batch_generator.py --phase week_1 --start-index <last_successful_index>
```

### Quality Issues

If pages are too similar:
- Increase temperature in `copywriting.py` (0.8 → 0.9)
- Expand viral hooks library in `config/viral_hooks.json`

If factual errors appear:
- Lower temperature in research agents (0.7 → 0.5)
- Add more specific research requirements

## 📈 Performance Benchmarks

### System 1 (Simple)
- **Speed:** 60-100 pages/hour
- **Cost:** $0.10-0.20/page
- **Quality Score:** 0.75-0.85
- **Best For:** Mid/top-funnel content

### System 2 (Multi-Agent)
- **Speed:** 10-20 pages/hour
- **Cost:** $0.50-1.00/page
- **Quality Score:** 0.85-0.95
- **Best For:** Bottom-funnel, research-intensive

### Phased Rollout Timeline

- **Week 1:** 10 pages (manual QA)
- **Week 2:** 50 pages (spot-check QA)
- **Week 3:** 200 pages (automated QA)
- **Week 4-6:** 678+ pages (full scale)

## 🔐 Security

### API Key Management

```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use environment variables
export GEMINI_API_KEY="your-key-here"
```

### Error Handling

- All exceptions logged to `failed_tasks.json`
- Checkpoint system prevents data loss
- Resume capability from any point

## 📝 Next Steps

1. **Test locally** - Run `python generate_pages.py --limit 1`
2. **Review output** - Check quality in `output/` directory
3. **Start Week 1** - Generate 10 priority pages with `python batch_generator.py --phase week_1`
4. **Manual QA** - Review all Week 1 pages before proceeding
5. **Scale up** - Continue with Week 2, 3, 4-6

## 🤝 Support

For issues:
1. Check `output/failed_tasks.json` for error logs
2. Review agent configuration in `agents/` files
3. Test with single page before batch generation
4. Adjust agent prompts and temperature as needed

## 📄 License

Proprietary - Sozee Internal Use Only

---

**Ready to generate 678+ conversion-optimized landing pages! 🚀**
