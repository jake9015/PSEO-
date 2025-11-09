# Sozee Landing Page Generator

Automated generation of 678 SEO-optimized landing pages using Claude API.

## 📁 Project Structure

```
sozee-landing-pages/
├── README.md                      (this file)
├── .env                           (your API key - DO NOT COMMIT)
├── .gitignore                     (ignore sensitive files)
├── requirements.txt               (Python dependencies)
├── generate_pages.py              (main script)
├── config/
│   ├── patterns.json              (6 landing page patterns)
│   ├── variables.json             (all variable lists)
│   ├── viral_hooks.json           (TikTok hooks)
│   ├── content_templates.json     (Claude prompt templates)
│   └── faq_bank.json              (pattern-specific FAQs)
├── output/
│   ├── sozee_landing_pages.csv    (final output)
│   └── progress/                  (auto-saved progress)
└── docs/
    └── landing_page_structure.md  (reference guide)
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
Create a `.env` file:
```
ANTHROPIC_API_KEY=your-key-here
```

### 3. Test with 10 Pages
```bash
python generate_pages.py --limit 10
```

### 4. Generate All 678 Pages
```bash
python generate_pages.py
```

## 📊 Output

CSV file with these columns:
- pattern, url, h1, hero_subtitle, problem_agitation, faq
- meta_title, meta_description, status
- All variables (competitor, audience, platform, etc.)

## 💰 Cost Estimate

- 678 pages × 4 API calls = 2,712 calls
- ~500 tokens per call = 1.35M tokens
- At $3/million tokens = **$4-5 total**

## ⏱️ Time Estimate

- Setup: 15 minutes
- Generation: 2-3 hours (automated)
- Review: 1 hour

## 🔧 Customization

Edit these files to customize output:
- `config/content_templates.json` - Modify Claude prompts
- `config/viral_hooks.json` - Add/remove hooks
- `config/patterns.json` - Adjust pattern formulas
- `config/variables.json` - Add new variables

## 📝 Import to WordPress

Use WP All Import plugin:
1. Upload `sozee_landing_pages.csv`
2. Map columns to custom fields
3. Assign Elementor template
4. Import all at once

## 🆘 Troubleshooting

**Error: "API key not found"**
- Check .env file exists
- Verify ANTHROPIC_API_KEY is set

**Error: "Rate limit exceeded"**
- Script includes 1-second delay between calls
- Anthropic has generous rate limits

**Error: "Module not found"**
- Run: `pip install -r requirements.txt`

## 📞 Support

Questions? Check the docs/ folder or:
- Review landing_page_structure.md
- Check content_templates.json for prompt examples
- Test with --limit 10 first
