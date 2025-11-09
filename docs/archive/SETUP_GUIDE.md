# CURSOR PROJECT SETUP GUIDE

## 📁 ALL FILES YOU NEED

Your Cursor project needs these exact files:

```
sozee-landing-pages/                     ← Create this folder
├── README.md                            ✅ PROVIDED
├── .env                                 ⚠️ YOU CREATE (copy from .env.example)
├── .env.example                         ✅ PROVIDED
├── .gitignore                           ✅ PROVIDED
├── requirements.txt                     ✅ PROVIDED
├── generate_pages.py                    ✅ PROVIDED
├── config/                              ← Create this folder
│   ├── patterns.json                    ✅ PROVIDED
│   ├── variables.json                   ✅ PROVIDED
│   ├── viral_hooks.json                 ✅ PROVIDED
│   └── content_templates.json           ✅ PROVIDED
├── output/                              ← Auto-created by script
│   ├── sozee_landing_pages.csv          ← Generated output
│   └── progress/                        ← Auto-saved progress
└── docs/                                ← Optional documentation
```

**Status:**
- ✅ All files provided in /mnt/user-data/outputs/cursor-project/
- ⚠️ Only need to create: `.env` file with your API key

---

## 🚀 5-MINUTE SETUP

### Step 1: Download Files (1 min)

**All project files are here:**
`/mnt/user-data/outputs/cursor-project/`

**Download the entire folder** to your local machine.

### Step 2: Open in Cursor (1 min)

1. Open Cursor (download from cursor.sh if you don't have it)
2. File → Open Folder → Select your downloaded `sozee-landing-pages` folder

### Step 3: Create .env File (1 min)

1. Copy `.env.example` to `.env`
2. Get your Anthropic API key: https://console.anthropic.com/
3. Edit `.env` and add your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ```

### Step 4: Install Dependencies (1 min)

Open terminal in Cursor (Cmd+J or Ctrl+J) and run:

```bash
pip install -r requirements.txt
```

### Step 5: Test with 10 Pages (1 min)

```bash
python generate_pages.py --limit 10
```

**That's it!** If it works, you'll see:
- Progress for 10 pages being generated
- CSV file in `output/` folder
- Each page has hero_subtitle, problem_agitation, faq, meta_description

---

## 🎯 WHAT EACH FILE DOES

### Root Files

**README.md**
- Documentation for the project
- Quick start guide
- Troubleshooting tips

**.env** (YOU CREATE THIS)
- Contains your Anthropic API key
- **NEVER commit this to Git**
- Copy from .env.example template

**.env.example**
- Template for .env file
- Shows what environment variables you need

**.gitignore**
- Tells Git what files to ignore
- Prevents committing API keys and output files

**requirements.txt**
- Python package dependencies
- anthropic==0.18.1 (Claude API)
- pandas==2.1.4 (CSV handling)
- python-dotenv==1.0.0 (env variable loading)

**generate_pages.py**
- Main script that generates all pages
- Reads config files
- Calls Claude API
- Outputs CSV

### Config Files (config/)

**patterns.json**
- Defines all 6 landing page patterns
- URL formulas, H1 formulas, CTAs
- Tells script what pages to create

**variables.json**
- All variable lists (competitors, platforms, audiences, etc.)
- Organized by priority (high/medium/low)
- Used to generate page combinations

**viral_hooks.json**
- 70+ TikTok viral hooks
- Used in problem agitation sections
- Randomly selected per page

**content_templates.json**
- Claude API prompts for each section
- Defines how content is generated
- Customize these to change output style

### Output Files (generated)

**output/sozee_landing_pages_[timestamp].csv**
- Final output with all 678 pages
- Ready to import to WordPress
- Contains all sections + metadata

**output/progress/sozee_landing_pages_progress.csv**
- Auto-saved every 10 pages
- Recovery file if script crashes

---

## 💻 USING CURSOR

### Give Cursor Context

Once files are loaded, use Cursor's AI to help:

**Cmd+K (or Ctrl+K)** - Ask Cursor to:
- "Explain how generate_pages.py works"
- "Fix this error: [paste error]"
- "Add a new section called 'testimonials'"
- "Change the viral hooks to be more aggressive"

**Cursor knows all your files** and can help you:
- Debug errors
- Customize prompts
- Add new features
- Optimize the code

### Example Cursor Prompts:

**To customize content:**
```
In content_templates.json, make the problem_agitation section 
more aggressive and urgent for agencies. Emphasize revenue loss.
```

**To add features:**
```
Add a new section to generate_pages.py that creates comparison 
tables for Pattern 1 pages. Use Claude API to generate the table data.
```

**To debug:**
```
I'm getting this error when running the script: [paste error]
What's wrong and how do I fix it?
```

---

## 🧪 TESTING COMMANDS

### Test with 10 pages (fastest)
```bash
python generate_pages.py --limit 10
```

### Test with high-priority variables only (~150 pages)
```bash
python generate_pages.py --priority-only
```

### Generate all 678 pages
```bash
python generate_pages.py
```

### Check progress during generation
```bash
# Open another terminal
cat output/progress/sozee_landing_pages_progress.csv | wc -l
```

---

## 📊 EXPECTED OUTPUT

After running successfully, you'll have a CSV with these columns:

| Column | Example |
|--------|---------|
| pattern | 1 |
| pattern_name | Competitor Comparison |
| url | /sozee-vs-higgsfield-for-onlyfans-creators |
| h1 | Sozee vs Higgsfield for OnlyFans Creators |
| eyebrow | Head-to-Head Comparison |
| hero_subtitle | Both promise AI content. Only one solves... |
| problem_agitation | [Full 3-4 paragraph section] |
| faq | [5 Q&A pairs] |
| meta_title | Sozee vs Higgsfield for OnlyFans Creators \| Sozee |
| meta_description | Compare Sozee and Higgsfield for OnlyFans... |
| primary_cta | Compare Features |
| secondary_cta | Try Sozee Free |
| show_comparison_table | true |
| status | draft |
| competitor | Higgsfield |
| audience | Creators |
| platform | (empty for this pattern) |
| tool_type | (empty for this pattern) |
| use_case | (empty for this pattern) |
| generated_at | 2025-11-09T10:30:00 |

---

## 🔧 CUSTOMIZATION

### Want different content style?

Edit: `config/content_templates.json`

**Make it more aggressive:**
```json
"prompt_template": "Write AGGRESSIVE, URGENT copy that creates FOMO..."
```

**Make it more professional:**
```json
"prompt_template": "Write professional, corporate-appropriate copy..."
```

**Add more context:**
Add this to system_context:
```json
"system_context": "Additional context: Our target revenue is $1M ARR. Our competitors are Higgsfield (complex), Krea (expensive), Midjourney (not creator-focused)..."
```

### Want different viral hooks?

Edit: `config/viral_hooks.json`

Add your own hooks to the "hooks" array.

### Want different variables?

Edit: `config/variables.json`

Add new competitors, platforms, audiences, etc.

### Want different patterns?

Edit: `config/patterns.json`

Add a new pattern with id: 7, url_formula, h1_formula, etc.

---

## ⚠️ TROUBLESHOOTING

### "API key not found"
**Fix:** Create .env file with your key
```bash
cp .env.example .env
# Edit .env and add your key
```

### "Module not found: anthropic"
**Fix:** Install dependencies
```bash
pip install -r requirements.txt
```

### "Rate limit exceeded"
**Fix:** Script already has 1-second delays. This shouldn't happen.
If it does, increase sleep time in generate_pages.py:
```python
time.sleep(2)  # Change from 1 to 2 seconds
```

### "Empty response from Claude"
**Fix:** Check your prompts in content_templates.json
Sometimes prompts are too vague or conflicting.

### Script crashes mid-generation
**Fix:** Progress is auto-saved!
Check `output/progress/` for the last saved CSV.
You can resume by:
1. Loading that CSV
2. Seeing which pages completed
3. Re-running with --limit to skip completed ones

---

## 💰 COST TRACKING

The script will show estimated cost before starting.

**To track actual costs:**
1. Go to: https://console.anthropic.com/
2. Check "Usage" tab
3. See API call costs

**Typical costs:**
- 10 test pages: ~$0.10
- 50 pages: ~$0.50
- 678 pages: ~$5

---

## 🎓 NEXT STEPS

**After generating pages:**

1. **Review output CSV**
   - Open in Excel/Google Sheets
   - Check content quality
   - Spot any errors

2. **Test import to WordPress**
   - Use WP All Import plugin
   - Import 10 pages first
   - Verify everything maps correctly

3. **Refine prompts**
   - Based on output quality
   - Edit content_templates.json
   - Regenerate with new prompts

4. **Scale up**
   - Once happy with 10-50 pages
   - Generate all 678 pages
   - Import to WordPress

---

## 📞 NEED HELP?

**Cursor can help!**
- Press Cmd+K and ask it questions
- It has context of all your files
- It can debug errors and suggest fixes

**Manual is stuck?**
- Check README.md in project folder
- All documentation is there
- Review each config file

**Want to customize something?**
- All templates are in config/
- Edit JSON files to change behavior
- Use Cursor to help with changes

---

## ✅ VERIFICATION CHECKLIST

Before running the generator, verify:

- [ ] All files from cursor-project/ folder are in place
- [ ] .env file exists with your API key
- [ ] requirements.txt dependencies installed
- [ ] Can run: `python generate_pages.py --limit 1`
- [ ] Output CSV appears in output/ folder
- [ ] Content looks good (hero_subtitle, problem, faq)

If all checked, you're ready to generate all 678 pages!

```bash
python generate_pages.py
```

---

**Time to completion:** ~2-3 hours for all 678 pages  
**Total cost:** ~$5 in API credits  
**Output:** CSV ready for WordPress import

**You're ready to go! 🚀**
