# Sozee PSEO Landing Page Generator - Project Overview

## 📦 Complete Repository Structure

```
PSEO-/
├── config/                         # Configuration files
│   ├── patterns.json              # 6 landing page pattern definitions
│   ├── variables.json             # All variables (competitors, platforms, etc.)
│   ├── viral_hooks.json           # TikTok hooks for problem sections
│   └── content_templates.json     # Gemini prompt templates
│
├── agents/                         # Multi-agent system
│   ├── __init__.py                # Agent package init
│   ├── pseo_strategist.py        # Master planning agent
│   ├── competitor_research.py    # Competitor analysis agent
│   ├── audience_insight.py       # Audience psychology agent
│   ├── copywriting.py            # Content generation agent
│   ├── faq_generator.py          # FAQ creation agent
│   ├── seo_optimizer.py          # SEO metadata agent
│   └── quality_control.py        # Quality validation agent
│
├── agent_framework.py             # Base agent classes and data structures
├── pseo_orchestrator.py          # Multi-agent orchestrator
├── batch_generator.py            # Phased rollout batch processor
├── generate_pages.py             # Simple single-agent generator
├── test_single_page.py           # Quality testing script
│
├── output/                        # Generated pages (auto-created)
│   ├── page_*.json               # Individual page files
│   ├── checkpoint.json           # Resume checkpoint
│   ├── failed_tasks.json         # Failed generation log
│   └── sozee_landing_pages_*.csv # WordPress import CSV
│
├── README.md                      # Main documentation
├── TESTING_GUIDE.md               # Quality testing guide
├── START_HERE.md                  # Quick start guide
├── DOCUMENTATION_AUDIT.md         # Docs audit report
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
└── requirements.txt               # Python dependencies
```

## 🎯 System Overview

This repository contains **two complete content generation systems**:

### System 1: Simple Generator
- **File:** `generate_pages.py`
- **API:** Google Gemini (`gemini-2.0-flash-exp`)
- **Speed:** 60-100 pages/hour
- **Cost:** $0.10-0.20/page
- **Quality:** 0.75-0.85
- **Best for:** Quick generation, mid/top-funnel

### System 2: Multi-Agent
- **Files:** `pseo_orchestrator.py` + `batch_generator.py` + 7 agents
- **API:** Google Gemini (`gemini-2.0-flash-exp`)
- **Speed:** 10-20 pages/hour
- **Cost:** $0.50-1.00/page
- **Quality:** 0.85-0.95
- **Best for:** High quality, bottom-funnel, research-intensive

---

## 💰 Complete Cost Analysis

### System 1 (Simple)
- **Per Page:** $0.10-0.20
- **678 Pages:** $68-136 total
- **Time:** 7-11 hours

### System 2 (Multi-Agent)
- **Per Page:** $0.50-1.00
- **678 Pages:** $339-678 total  
- **Time:** 34-68 hours

**Gemini Pricing:**
- Input: $0.075/1M tokens
- Output: $0.30/1M tokens

---

## 📚 For Complete Documentation

See these files for detailed information:

- **Quick Start:** `START_HERE.md` - 10-minute setup guide
- **Full Docs:** `README.md` - Complete system documentation
- **Testing:** `TESTING_GUIDE.md` - Quality validation guide
- **Audit:** `DOCUMENTATION_AUDIT.md` - Documentation status

---

**Ready to start?** See `START_HERE.md`
