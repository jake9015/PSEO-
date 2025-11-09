# Sozee Landing Page Generator - Project Overview

## 📁 Complete File List

```
sozee-landing-pages/
├── .cursorrules                    ✅ CRITICAL - Gives Cursor AI project context
├── .env.example                    ➡️  Copy to .env and add API key
├── README.md                       📖 Project overview
├── SETUP.md                        🚀 Step-by-step setup guide
├── requirements.txt                📦 Python dependencies
├── generate_pages.py               🐍 Main generation script
├── config/
│   ├── patterns.json              ⚙️  6 landing page pattern definitions
│   ├── variables.json             📝 All variables (competitors, platforms, etc.)
│   ├── viral_hooks.json           🎣 TikTok hooks for problem sections
│   └── content_templates.json     💬 Claude prompt templates
└── output/
    ├── sozee_landing_pages.csv    📊 Final output (generated)
    └── progress/                   💾 Progress saves (generated)
```

---

## 🎯 What Each File Does

### Required to Start

**1. `.cursorrules`** 🔴 MOST IMPORTANT
- Gives Cursor AI full context about the project
- Without this, Cursor won't understand your project
- Defines patterns, variables, brand voice, and best practices

**2. `.env`** (you create from `.env.example`)
- Contains your Anthropic API key
- Copy from `.env.example` and add your key
- NEVER commit this to Git

**3. `requirements.txt`**
- Lists Python packages needed
- Run: `pip install -r requirements.txt`
- Installs: anthropic, pandas, python-dotenv

**4. `generate_pages.py`**
- Main script that generates all pages
- Calls Claude API for each section
- Outputs CSV ready for WordPress

### Configuration Files (in config/)

**5. `patterns.json`**
- Defines 6 landing page patterns
- URL formulas, H1 formulas, variables needed
- Edit to add new patterns or modify existing

**6. `variables.json`**
- Lists all variables:
  - 15 competitors
  - 15 platforms
  - 8 audiences
  - 20 use cases
  - 10 tool types
- Edit to add new variables

**7. `viral_hooks.json`**
- 70+ viral TikTok hooks
- Used in problem agitation sections
- Script randomly selects one per page

**8. `content_templates.json`**
- Claude prompt templates for each section
- Defines brand voice, tone, structure
- Edit to customize content output

### Documentation

**9. `README.md`**
- Quick project overview
- Output structure
- Basic commands

**10. `SETUP.md`**
- Detailed setup instructions
- Troubleshooting guide
- Best practices

---

## ⚡ Quick Start Commands

### Test Generation (10 pages)
```bash
python generate_pages.py --limit 10
```

### Full Generation (678 pages)
```bash
python generate_pages.py
```

### Resume from Index 50
```bash
python generate_pages.py --start 50
```

---

## 🤖 Using Cursor AI

Cursor has full context via `.cursorrules`. Just ask:

**Example prompts:**
- "Generate the first 10 pages for me"
- "Why is this error happening?"
- "Modify the hero subtitle to be shorter"
- "Add a new competitor to variables.json"
- "Change the FAQ count from 5 to 6"
- "Show me how to customize the brand voice"

---

## 📊 Expected Output

**File:** `output/sozee_landing_pages.csv`

**Columns:**
- pattern, pattern_name, url, h1
- hero_subtitle, problem_agitation, faq
- meta_title, meta_description, status
- All variables (competitor, audience, platform, tool_type, use_case)

**Example row:**
```csv
3,Direct Tool,/onlyfans-ai-photo-generator,"OnlyFans AI Photo Generator","Turn 1 photoshoot into 10,000 photos","[problem text]","[5 Q&As]","OnlyFans AI Photo Generator | Sozee","Professional AI photo generator...","draft",,,OnlyFans,Photo Generator,
```

---

## 💰 Cost Breakdown

**Per page:**
- 4 API calls (hero, problem, FAQ, meta)
- ~500 tokens output per call
- 2,000 tokens total per page

**All 678 pages:**
- 2,712 API calls
- 1.35M output tokens
- Cost: ~$4-5 at $3/M tokens

---

## ⏱️ Time Estimate

**Setup:** 30 minutes
- Install dependencies: 5 min
- Configure API key: 5 min
- Test with 10 pages: 5 min
- Review output: 15 min

**Full Generation:** 2-3 hours (automated)
- 678 pages × 4 API calls × 1 second delay
- Script runs unattended
- Saves progress every 10 pages

**Total:** ~3 hours from zero to 678 pages

---

## 🎯 Critical Files for Cursor Context

When you open the project in Cursor, make sure these files exist:

1. ✅ `.cursorrules` - Without this, Cursor doesn't understand the project
2. ✅ `config/patterns.json` - Defines what pages to generate
3. ✅ `config/variables.json` - Defines all possible values
4. ✅ `config/content_templates.json` - Defines how to prompt Claude

---

## 🔄 Typical Workflow

```
1. Open project in Cursor
   ↓
2. Cursor reads .cursorrules (automatic)
   ↓
3. You: "Generate 10 test pages"
   ↓
4. Cursor: [Runs generate_pages.py --limit 10]
   ↓
5. Review output CSV
   ↓
6. Customize prompts if needed
   ↓
7. Generate all 678 pages
   ↓
8. Import to WordPress
```

---

## 📝 Customization Points

### Easy (No Coding)
- Add variables: Edit `config/variables.json`
- Change prompts: Edit `config/content_templates.json`
- Add viral hooks: Edit `config/viral_hooks.json`
- Modify patterns: Edit `config/patterns.json`

### Medium (Basic Python)
- Change section structure: Edit `generate_pages.py`
- Add new sections: Modify `build_prompt()` function
- Change save frequency: Modify progress save logic

### Advanced (Experienced)
- Add comparison tables: Generate structured data
- Add images: Integrate image generation API
- Async generation: Use asyncio for speed
- Custom validation: Add quality checks

---

## ⚠️ Important Notes

### DO commit to Git:
- All files EXCEPT `.env` and `output/`
- Add to `.gitignore`:
  ```
  .env
  output/
  __pycache__/
  *.pyc
  ```

### DON'T edit directly:
- `.cursorrules` (unless you know what you're doing)
- `generate_pages.py` (unless you're comfortable with Python)

### DO edit freely:
- All files in `config/` folder
- These are just JSON - safe to modify

---

## 🆘 Common Issues

### Cursor doesn't understand the project
**Fix:** Make sure `.cursorrules` file exists and is in root folder

### API key not working
**Fix:** Check `.env` file has: `ANTHROPIC_API_KEY=sk-ant-...`

### Script crashes
**Fix:** Check `output/progress/` for last save, resume with `--start`

### Content quality issues
**Fix:** Edit prompts in `config/content_templates.json`

### Missing dependencies
**Fix:** Run `pip install -r requirements.txt`

---

## ✅ Pre-Flight Checklist

Before running full generation:

- [ ] `.cursorrules` exists in root folder
- [ ] `.env` created with valid API key
- [ ] `pip install -r requirements.txt` completed
- [ ] All `config/*.json` files present
- [ ] `output/` folder exists (created automatically)
- [ ] Tested with `--limit 10` successfully
- [ ] Reviewed test output for quality
- [ ] Have ~$5 API credits available

---

## 🚀 Ready to Start?

1. **Open Cursor**: Open this folder in Cursor IDE
2. **Test**: Run `python generate_pages.py --limit 10`
3. **Review**: Check `output/sozee_landing_pages.csv`
4. **Generate**: Run `python generate_pages.py` for all 678

Cursor will guide you through any issues thanks to `.cursorrules`!

---

## 📚 Additional Resources

- **Anthropic API Docs**: https://docs.anthropic.com
- **Cursor Docs**: https://cursor.sh/docs
- **WP All Import**: https://www.wpallimport.com/
- **Elementor**: https://elementor.com/

---

**Questions?** Ask Cursor AI - it has full project context!
