# Sozee Landing Page Generator - Setup Guide

## 📋 Prerequisites

- Python 3.9 or higher
- Anthropic API key (get from https://console.anthropic.com/settings/keys)
- Cursor IDE (download from https://cursor.sh)

---

## 🚀 Setup Steps

### Step 1: Get Your Anthropic API Key

1. Go to https://console.anthropic.com/settings/keys
2. Create new API key
3. Copy it (you'll need it in Step 4)

**Cost:** ~$5 for 678 pages

---

### Step 2: Download/Clone This Project

**Option A: Download ZIP**
1. Download all files from the provided folder
2. Extract to a folder like `sozee-landing-pages`

**Option B: Clone from Git (if applicable)**
```bash
git clone [your-repo-url]
cd sozee-landing-pages
```

---

### Step 3: Install Dependencies

Open terminal in the project folder and run:

```bash
# Install Python dependencies
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude API client
- `pandas` - CSV handling
- `python-dotenv` - Environment variables

---

### Step 4: Configure API Key

1. Copy the example env file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API key:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

3. Save the file

---

### Step 5: Verify Setup

Check that everything is configured:

```bash
python generate_pages.py --help
```

You should see:
```
usage: generate_pages.py [-h] [--limit LIMIT] [--start START]

Generate Sozee landing pages
...
```

---

### Step 6: Test with 10 Pages

Before generating all 678 pages, test with 10:

```bash
python generate_pages.py --limit 10
```

**What happens:**
- Generates 10 landing pages
- Takes ~2-3 minutes
- Costs ~$0.15
- Outputs to `output/sozee_landing_pages.csv`

**Check the output:**
1. Open `output/sozee_landing_pages.csv`
2. Review the content quality
3. Make sure all sections are filled

---

### Step 7: Generate All Pages (Production)

If the test looks good, generate all 678 pages:

```bash
python generate_pages.py
```

**What happens:**
- Generates all 678 pages
- Takes 2-3 hours
- Costs ~$5
- Saves progress every 10 pages
- Output: `output/sozee_landing_pages.csv`

**Progress tracking:**
- Check `output/progress/` for incremental saves
- If script crashes, you can resume from last save

---

## 📊 Understanding the Output

### CSV Structure

The output CSV has these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `pattern` | Pattern ID (1-6) | 3 |
| `pattern_name` | Pattern name | Direct Tool |
| `url` | Page URL slug | /onlyfans-ai-photo-generator |
| `h1` | Page title (H1) | OnlyFans AI Photo Generator |
| `hero_subtitle` | Hero section subtitle | Turn 1 photoshoot into 10,000 photos |
| `problem_agitation` | Full problem section | [3-4 paragraphs + bullets] |
| `faq` | 5 Q&A pairs | Q: How does...\nA: ... |
| `meta_title` | SEO title tag | OnlyFans AI Photo Generator \| Sozee |
| `meta_description` | SEO description | Professional AI photo generator... |
| `status` | Post status | draft |
| `[variables]` | Pattern variables | competitor, audience, platform, etc. |

---

## 🔧 Customization Options

### Change the Prompts

Edit `config/content_templates.json` to customize:
- Brand voice
- Section prompts
- FAQ questions
- Meta description templates

### Add More Variables

Edit `config/variables.json` to add:
- New competitors
- New platforms
- New audience types
- New use cases

### Modify Patterns

Edit `config/patterns.json` to:
- Change URL formulas
- Adjust H1 formulas
- Add new patterns

---

## 🐛 Troubleshooting

### Error: "ANTHROPIC_API_KEY not found"

**Fix:** Make sure you created `.env` file with your API key:
```bash
# Check if .env exists
ls -la .env

# If not, copy from example
cp .env.example .env

# Edit and add your key
nano .env
```

### Error: "anthropic module not found"

**Fix:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Error: API rate limit

**Fix:** The script already has 1-second delays. If you still hit limits:
1. Check your API tier at https://console.anthropic.com
2. Increase delay in `generate_pages.py` (line with `time.sleep(1)`)

### Script crashes mid-generation

**Fix:** Resume from last progress save:
```bash
# Check last saved progress
ls output/progress/

# If last save was at page 50, resume from there
python generate_pages.py --start 50
```

---

## 💡 Tips & Best Practices

### 1. Review First 50 Pages Manually

After generation:
1. Open CSV in Excel/Google Sheets
2. Review first 50 pages for quality
3. Check that variables are substituted correctly
4. Verify FAQ questions make sense

### 2. Test Different Sections

Generate 10 pages, then check:
- ✅ Hero subtitles are compelling and <150 chars
- ✅ Problem sections use viral hooks effectively
- ✅ FAQs are pattern-specific and useful
- ✅ Meta descriptions are 150-160 chars

### 3. Save Progress Files

Don't delete `output/progress/` folder:
- Contains incremental saves
- Useful for debugging
- Can resume if script crashes

### 4. Version Control

If using Git:
```bash
# Don't commit these files
echo ".env" >> .gitignore
echo "output/" >> .gitignore
```

---

## 🎯 Next Steps

After generation is complete:

### 1. Review Output
```bash
# Check output
wc -l output/sozee_landing_pages.csv
# Should show 679 lines (678 pages + header)

# View in spreadsheet
open output/sozee_landing_pages.csv
```

### 2. Import to WordPress

**Option A: WP All Import**
1. Install WP All Import plugin
2. Upload CSV
3. Map columns to post fields
4. Import all pages

**Option B: Custom Importer**
1. Create custom import script
2. Use WordPress REST API
3. Batch import pages

### 3. Set Up Elementor Template

1. Create master template in Elementor
2. Use dynamic fields to pull content from custom fields
3. Apply template to all imported pages

---

## 📚 Additional Resources

### Cursor AI Features

Use Cursor's built-in AI (Cmd+K or Ctrl+K) to:
- Debug any errors
- Modify the script
- Add new features
- Generate additional sections

### Example Cursor Prompts

```
"Add a new section called 'testimonials' that generates 3 testimonials"

"Modify the problem section to be shorter (2 paragraphs max)"

"Add error handling for when API calls fail"

"Create a function to generate comparison tables for Pattern 1"
```

### Files You Can Safely Edit

✅ `config/patterns.json` - Pattern definitions
✅ `config/variables.json` - Variable lists
✅ `config/viral_hooks.json` - Hook variations
✅ `config/content_templates.json` - Prompt templates

⚠️ Don't edit unless you know Python:
- `generate_pages.py`
- `requirements.txt`

---

## 🆘 Getting Help

### Using Cursor AI

The `.cursorrules` file gives Cursor full context about this project. Just ask:
- "Why is this error happening?"
- "How do I add a new variable?"
- "Generate a new pattern"
- "Optimize the prompts"

### Common Questions

**Q: Can I pause and resume generation?**
A: Yes! Stop the script (Ctrl+C) and resume with `--start` flag from last progress file.

**Q: How do I regenerate just one page?**
A: Modify the script to filter by URL or use `--limit 1 --start [index]`.

**Q: Can I use a different AI model?**
A: Yes, change the model name in `generate_pages.py` (line with `model="claude-sonnet..."`).

**Q: What if I want different content for some pages?**
A: Edit the CSV manually after generation, or modify the prompts in `content_templates.json`.

---

## ✅ Checklist

Before running production generation:

- [ ] Python 3.9+ installed
- [ ] `pip install -r requirements.txt` completed
- [ ] `.env` file created with API key
- [ ] Tested with `--limit 10` successfully
- [ ] Reviewed test output quality
- [ ] Have 2-3 hours for full generation
- [ ] Have ~$5 in API credits available
- [ ] WordPress site ready for import

---

## 🎉 You're Ready!

Run this command to start:

```bash
python generate_pages.py --limit 10  # Test first
python generate_pages.py             # Full generation
```

Good luck! 🚀
