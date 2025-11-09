# CURSOR + CLAUDE API WORKFLOW GUIDE
## Generate 678 Landing Pages for WordPress Import

---

## 🎯 OVERVIEW

**Input:** Your 6 pattern formulas + variable lists
**Process:** Python script with Claude API calls
**Output:** Complete CSV ready for WordPress import
**Cost:** ~$50-100 in Claude API credits
**Time:** 2-3 hours to run (automated)

---

## 📋 STEP-BY-STEP PROCESS

### STEP 1: Set Up Cursor Project

1. Open Cursor
2. Create new project: `sozee-landing-page-generator`
3. Create files:
   ```
   /
   ├── generate_pages.py          (main script)
   ├── patterns.json               (pattern definitions)
   ├── variables.json              (all variable lists)
   ├── content_templates.json      (prompts for Claude)
   ├── viral_hooks.json            (your TikTok hooks)
   ├── requirements.txt            (dependencies)
   └── output/
       └── sozee_landing_pages.csv (generated output)
   ```

---

### STEP 2: Install Dependencies

**requirements.txt:**
```txt
anthropic==0.18.1
pandas==2.1.4
python-dotenv==1.0.0
```

**Install:**
```bash
pip install -r requirements.txt
```

---

### STEP 3: Create Pattern & Variable Files

**patterns.json:**
```json
{
  "patterns": [
    {
      "id": 1,
      "name": "Competitor Comparison",
      "url_formula": "/sozee-vs-{competitor}-for-{audience}",
      "h1_formula": "Sozee vs {Competitor} for {Audience}",
      "variables": ["competitor", "audience"],
      "show_comparison_table": true
    },
    {
      "id": 2,
      "name": "Best Tool",
      "url_formula": "/best-{use_case}-for-{audience}",
      "h1_formula": "Best {Use_Case} for {Audience}",
      "variables": ["use_case", "audience"],
      "show_comparison_table": false
    },
    {
      "id": 3,
      "name": "Direct Tool",
      "url_formula": "/{platform}-{tool_type}",
      "h1_formula": "{Platform} {Tool_Type}",
      "variables": ["platform", "tool_type"],
      "show_comparison_table": false
    },
    {
      "id": 4,
      "name": "Alternative",
      "url_formula": "/{competitor}-alternative-for-{audience}",
      "h1_formula": "{Competitor} Alternative for {Audience}",
      "variables": ["competitor", "audience"],
      "show_comparison_table": true
    },
    {
      "id": 5,
      "name": "Review",
      "url_formula": "/sozee-review-{audience}",
      "h1_formula": "Sozee Review for {Audience}",
      "variables": ["audience"],
      "show_comparison_table": false
    },
    {
      "id": 6,
      "name": "Content Crisis",
      "url_formula": "/content-crisis-solution-for-{platform}-{audience}",
      "h1_formula": "Solve the Content Crisis for {Platform} {Audience}",
      "variables": ["platform", "audience"],
      "show_comparison_table": false
    }
  ]
}
```

**variables.json:**
```json
{
  "competitors": [
    "Higgsfield", "Krea", "Midjourney", "Runway", "Stable Diffusion",
    "DALL-E", "Leonardo.ai", "Artbreeder", "Civitai", "DreamStudio",
    "Glif", "Ideogram", "Pika", "Playground AI", "Pykaso"
  ],
  "platforms": [
    "OnlyFans", "Patreon", "FanVue", "Fansly", "MyM", "LoyalFans",
    "Slushy", "4Based", "AVN Stars", "AdmireMe", "Fanhouse", "Glow",
    "IsMyGirl", "JustFor.Fans", "ManyVids"
  ],
  "audiences": [
    "Creators", "Agencies", "Models", "Content Creators",
    "Influencers", "Management Agencies", "Content Managers", "Adult Creators"
  ],
  "use_cases": [
    "AI Photo", "AI Video", "Virtual Photoshoot", "LORA Model",
    "AI Portrait", "AI Selfie", "AI Headshot", "Profile Picture",
    "AI Lifestyle", "AI Fashion", "AI Lingerie", "AI Outfits",
    "Boudoir Photos", "Glamour Shot", "AI Cosplay", "AI Fitness",
    "AI Background", "NSFW Content", "SFW Content", "AI Feet Pics"
  ],
  "tool_types": [
    "Photo Generator", "Video Generator", "Content Studio", "LORA Trainer",
    "Face Swap Tool", "Background Generator", "Portrait Creator",
    "TikTok Clone Tool", "Photo Editor", "AI Model Trainer"
  ]
}
```

---

### STEP 4: Main Python Script

**generate_pages.py:**
```python
import os
import json
import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
import time
import random

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Load configuration files
with open('patterns.json', 'r') as f:
    patterns_config = json.load(f)

with open('variables.json', 'r') as f:
    variables = json.load(f)

with open('viral_hooks.json', 'r') as f:
    viral_hooks = json.load(f)

def generate_page_combinations():
    """Generate all possible page combinations based on patterns"""
    pages = []
    
    for pattern in patterns_config['patterns']:
        pattern_id = pattern['id']
        pattern_vars = pattern['variables']
        
        # Generate combinations based on required variables
        if pattern_vars == ['competitor', 'audience']:
            for comp in variables['competitors']:
                for aud in variables['audiences']:
                    pages.append({
                        'pattern': pattern_id,
                        'competitor': comp,
                        'audience': aud,
                        'url': pattern['url_formula'].format(
                            competitor=comp.lower().replace(' ', '-'),
                            audience=aud.lower().replace(' ', '-')
                        ),
                        'h1': pattern['h1_formula'].format(
                            Competitor=comp,
                            Audience=aud
                        )
                    })
        
        elif pattern_vars == ['use_case', 'audience']:
            for use_case in variables['use_cases']:
                for aud in variables['audiences']:
                    pages.append({
                        'pattern': pattern_id,
                        'use_case': use_case,
                        'audience': aud,
                        'url': pattern['url_formula'].format(
                            use_case=use_case.lower().replace(' ', '-'),
                            audience=aud.lower().replace(' ', '-')
                        ),
                        'h1': pattern['h1_formula'].format(
                            Use_Case=use_case,
                            Audience=aud
                        )
                    })
        
        elif pattern_vars == ['platform', 'tool_type']:
            for plat in variables['platforms']:
                for tool in variables['tool_types']:
                    pages.append({
                        'pattern': pattern_id,
                        'platform': plat,
                        'tool_type': tool,
                        'url': pattern['url_formula'].format(
                            platform=plat.lower().replace(' ', '-'),
                            tool_type=tool.lower().replace(' ', '-')
                        ),
                        'h1': pattern['h1_formula'].format(
                            Platform=plat,
                            Tool_Type=tool
                        )
                    })
        
        elif pattern_vars == ['platform', 'audience']:
            for plat in variables['platforms']:
                for aud in variables['audiences']:
                    pages.append({
                        'pattern': pattern_id,
                        'platform': plat,
                        'audience': aud,
                        'url': pattern['url_formula'].format(
                            platform=plat.lower().replace(' ', '-'),
                            audience=aud.lower().replace(' ', '-')
                        ),
                        'h1': pattern['h1_formula'].format(
                            Platform=plat,
                            Audience=aud
                        )
                    })
        
        elif pattern_vars == ['audience']:
            for aud in variables['audiences']:
                pages.append({
                    'pattern': pattern_id,
                    'audience': aud,
                    'url': pattern['url_formula'].format(
                        audience=aud.lower().replace(' ', '-')
                    ),
                    'h1': pattern['h1_formula'].format(
                        Audience=aud
                    )
                })
    
    return pages

def generate_content_with_claude(page_data, section):
    """Use Claude to generate content for a specific section"""
    
    # Build the prompt based on section and page data
    prompt = build_prompt(page_data, section)
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        content = message.content[0].text
        return content.strip()
    
    except Exception as e:
        print(f"Error generating content: {e}")
        return f"[ERROR: {section}]"

def build_prompt(page_data, section):
    """Build Claude prompt for specific section"""
    
    pattern = page_data['pattern']
    h1 = page_data['h1']
    
    # Get pattern-specific context
    pattern_info = next(p for p in patterns_config['patterns'] if p['id'] == pattern)
    pattern_name = pattern_info['name']
    
    # Extract variables
    variables_str = ", ".join([f"{k}: {v}" for k, v in page_data.items() 
                               if k not in ['pattern', 'url', 'h1']])
    
    if section == "hero_subtitle":
        prompt = f"""You're writing landing page copy for Sozee.ai, an AI content generation tool for OnlyFans creators and agencies.

Page Type: {pattern_name} (Pattern {pattern})
Page Title (H1): {h1}
Variables: {variables_str}

Write a compelling subtitle (1-2 sentences, max 150 characters) for the hero section.
The subtitle should hook the reader and clearly state the benefit.

Pattern-specific guidance:
- Pattern 1 (Comparison): Emphasize differentiation from competitor
- Pattern 2 (Best): Emphasize top ranking/recommendation
- Pattern 3 (Direct): Emphasize specific tool benefit
- Pattern 4 (Alternative): Emphasize why to switch
- Pattern 5 (Review): Emphasize honest evaluation
- Pattern 6 (Crisis): Emphasize the 1/100 problem

Output ONLY the subtitle text, nothing else."""

    elif section == "problem_agitation":
        # Select a random viral hook
        hook = random.choice(viral_hooks['hooks'])
        
        prompt = f"""You're writing landing page copy for Sozee.ai, an AI content generation tool for OnlyFans creators and agencies.

Page Type: {pattern_name} (Pattern {pattern})
Page Title: {h1}
Variables: {variables_str}

Write the problem agitation section (3-4 paragraphs + 3 bullet points).

Use this viral hook to start: "{hook}"

Then agitate the pain points relevant to this audience and pattern.
End with a transition to the solution.

Format:
[Hook headline]

[Paragraph 1: Set up the problem]

[Paragraph 2: Agitate the pain]

[Paragraph 3: Continue agitation]

• [Pain point 1]
• [Pain point 2]
• [Pain point 3]

[Transition sentence to Sozee solution]

Output the full formatted section."""

    elif section == "faq":
        prompt = f"""You're writing FAQ content for Sozee.ai landing page.

Page Type: {pattern_name} (Pattern {pattern})
Page Title: {h1}
Variables: {variables_str}

Write 5 pattern-specific FAQ questions and answers.

Pattern-specific question types:
- Pattern 1: Comparison questions (How is Sozee different from X?)
- Pattern 2: Best-of questions (What makes this the best?)
- Pattern 3: Tool questions (How does this tool work?)
- Pattern 4: Alternative questions (Why should I switch?)
- Pattern 5: Review questions (Is Sozee worth it?)
- Pattern 6: Crisis questions (What is the content crisis?)

Format each as:
Q: [Question]
A: [Answer - 2-3 sentences]

Output 5 Q&A pairs."""

    elif section == "meta_description":
        prompt = f"""Write a meta description (150-160 characters) for this landing page.

Page Title: {h1}
Pattern: {pattern_name}

Include the target keyword naturally and make it compelling for click-through.
Output ONLY the meta description, nothing else."""

    else:
        prompt = f"Generate {section} for: {h1}"
    
    return prompt

def generate_all_pages(limit=None):
    """Generate all page content"""
    
    print("🚀 Starting page generation...")
    
    # Generate all combinations
    pages = generate_page_combinations()
    
    if limit:
        pages = pages[:limit]
    
    print(f"📊 Total pages to generate: {len(pages)}")
    
    # Generate content for each page
    results = []
    
    for i, page in enumerate(pages):
        print(f"\n📄 Processing page {i+1}/{len(pages)}: {page['url']}")
        
        # Generate each section
        sections = {
            'hero_subtitle': generate_content_with_claude(page, 'hero_subtitle'),
            'problem_agitation': generate_content_with_claude(page, 'problem_agitation'),
            'faq': generate_content_with_claude(page, 'faq'),
            'meta_description': generate_content_with_claude(page, 'meta_description')
        }
        
        # Combine all data
        result = {
            **page,
            **sections,
            'meta_title': f"{page['h1']} | Sozee",
            'status': 'draft'
        }
        
        results.append(result)
        
        # Rate limiting - be nice to the API
        time.sleep(1)
        
        # Save progress every 10 pages
        if (i + 1) % 10 == 0:
            df = pd.DataFrame(results)
            df.to_csv('output/sozee_landing_pages_progress.csv', index=False)
            print(f"💾 Progress saved: {i+1} pages completed")
    
    # Save final CSV
    df = pd.DataFrame(results)
    df.to_csv('output/sozee_landing_pages.csv', index=False)
    
    print(f"\n✅ Complete! Generated {len(results)} pages")
    print(f"📁 Saved to: output/sozee_landing_pages.csv")
    
    return df

if __name__ == "__main__":
    # For testing, generate first 10 pages
    # df = generate_all_pages(limit=10)
    
    # For production, generate all pages
    df = generate_all_pages()
```

---

### STEP 5: Run the Script

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Run the generator
python generate_pages.py
```

**What happens:**
1. Script generates all 678 page combinations
2. For each page, calls Claude API to generate:
   - Hero subtitle
   - Problem agitation section
   - 5 FAQ Q&As
   - Meta description
3. Saves progress every 10 pages
4. Outputs final CSV with all content

**Estimated time:** 2-3 hours (678 pages × 4 API calls × ~10 seconds each)

**Estimated cost:** 
- 678 pages × 4 sections = 2,712 API calls
- ~500 tokens output per call = 1.35M tokens
- At $3 per million tokens = ~$4-5 total

---

### STEP 6: CSV Output Structure

**sozee_landing_pages.csv columns:**

```csv
pattern,url,h1,hero_subtitle,problem_agitation,faq,meta_title,meta_description,status,competitor,audience,platform,tool_type,use_case
1,/sozee-vs-higgsfield-for-onlyfans-creators,"Sozee vs Higgsfield for OnlyFans Creators","Both promise AI content. Only one solves the content crisis.","[Full problem section text]","[5 Q&A pairs]","Sozee vs Higgsfield for OnlyFans Creators | Sozee","Compare Sozee and Higgsfield for OnlyFans creators...",draft,Higgsfield,Creators,,,
```

---

### STEP 7: Import to WordPress

**Option A: WP All Import Plugin**
1. Install WP All Import
2. Upload sozee_landing_pages.csv
3. Map CSV columns to:
   - Post Title → h1
   - Post Content → Combine all sections
   - Custom Fields → All metadata
   - Post Status → status

**Option B: Elementor Custom Fields**
1. Install ACF Pro or Elementor Custom Fields
2. Create custom fields for each section:
   - hero_subtitle
   - problem_agitation
   - faq
   - etc.
3. Import CSV with WP All Import
4. Map to custom fields
5. Use Elementor to design template that pulls from custom fields

---

## 🆚 COMPARISON: Cursor vs Clay

| Factor | Cursor + Claude API | Clay |
|--------|---------------------|------|
| **Cost** | ~$5 one-time | $150+/month |
| **Control** | Full control | Limited by Clay features |
| **Speed** | 2-3 hours for all 678 | Similar, but batched |
| **Quality** | As good as your prompts | As good as your prompts |
| **Iteration** | Re-run script anytime | Need to set up new workflow |
| **Learning Curve** | Need basic Python | Need to learn Clay |
| **Scalability** | Infinite | Rate limits |
| **Version Control** | Git-friendly | Not code-based |

---

## 💡 WHEN TO USE CLAY INSTEAD

Use Clay if:
1. **You don't code** - Clay is more visual/no-code
2. **Need data enrichment** - Clay connects to external data sources
3. **Ongoing iteration** - You want to tweak individual pages regularly
4. **A/B testing** - Clay makes it easier to generate variations
5. **Team collaboration** - Non-technical team members can use Clay

---

## ✅ RECOMMENDED WORKFLOW

**Phase 1: Bulk Generation (Cursor)**
- Use the Python script above
- Generate all 678 pages at once
- Import to WordPress

**Phase 2: Optimization (Manual/Clay)**
- Test first 50 pages
- Measure conversion rates
- Use Clay to iterate on top-performing patterns
- Generate A/B test variations

**Why this works:**
- Fast initial deployment (get pages live ASAP)
- Low cost for bulk generation
- Use Clay only for high-value optimization

---

## 🎯 ADDITIONAL CURSOR FEATURES

**Use Cursor Composer to:**
1. Generate the entire script for you
2. Debug any errors
3. Add features (e.g., comparison tables, testimonials)
4. Customize prompts per pattern
5. Add image generation (DALL-E API)

**Prompt for Cursor:**
```
Create a Python script that:
1. Reads patterns.json and variables.json
2. Generates all page combinations
3. For each page, calls Claude API to generate:
   - Hero subtitle
   - Problem section (3-4 paragraphs)
   - 5 FAQ Q&As
   - Meta description
4. Outputs a CSV ready for WordPress import
5. Include error handling and progress saving
```

---

## 🚀 QUICK START

1. Copy the files above into Cursor
2. Add your Anthropic API key to `.env`
3. Run: `python generate_pages.py --limit 10` (test with 10 pages)
4. Review output
5. Run: `python generate_pages.py` (generate all 678)
6. Import CSV to WordPress

**Total time:** 
- Setup: 30 minutes
- Generation: 2-3 hours (automated)
- Import: 30 minutes

**Total cost:** ~$5 in API credits

---

## 📊 ALTERNATIVE: Manual + Template

If you want even more control:

1. **Use Cursor to generate structure only** (URLs, variables, H1s)
2. **Create 6 master templates** (one per pattern) in Elementor
3. **Manually write content for top 50 pages** using templates
4. **Use Claude/Clay to scale the rest** once you validate conversion

This hybrid approach:
- Highest quality on priority pages
- Learn what converts before scaling
- Lower upfront cost

---

## 🎓 RECOMMENDED APPROACH

For Sozee specifically:

1. **Week 1:** Use Cursor + Claude API to generate first 50 priority pages
2. **Week 2:** Import, publish, drive test traffic
3. **Week 3:** Analyze which patterns convert best
4. **Week 4:** Use Clay to generate variations of top performers
5. **Month 2:** Scale to all 678 pages using refined prompts

This gives you:
✅ Fast time-to-market
✅ Data-driven decisions
✅ Quality control
✅ Low cost (~$10 total)
✅ Scalability

---

Want me to help you set up the Cursor project or write the viral_hooks.json file?
