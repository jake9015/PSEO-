#!/usr/bin/env python3
"""
Sozee Landing Page Generator - Simple Single-API-Call Approach
==============================================================

⚠️  ALTERNATIVE IMPLEMENTATION NOTICE:
This is a simplified, single-API-call generator for fast generation (60-100 pages/hour).
For research-intensive, high-quality pages, use pseo_orchestrator.py with the multi-agent system.

Use Cases:
- Quick testing and prototyping
- Mid/top-funnel content with less research needs
- Fast generation when quality requirements are lower

For Production Use:
- Use batch_generator.py with PSEOOrchestrator for full multi-agent pipeline
- See TESTING_GUIDE.md for comparison of both approaches

Generates 678 SEO-optimized landing pages using Google Gemini API
"""

import os
import json
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import time
import random
import argparse
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Gemini client
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Load configuration files
with open('config/patterns.json', 'r') as f:
    patterns_config = json.load(f)

with open('config/variables.json', 'r') as f:
    variables_config = json.load(f)

with open('config/viral_hooks.json', 'r') as f:
    viral_hooks = json.load(f)

with open('config/content_templates.json', 'r') as f:
    content_templates = json.load(f)

def generate_page_combinations(priority_only=False):
    """
    Generate all possible page combinations based on patterns
    Args:
        priority_only: If True, only generate high_priority variable combinations
    """
    pages = []
    
    # Determine which variables to use
    if priority_only:
        competitors = variables_config['competitors']['high_priority']
        platforms = variables_config['platforms']['high_priority']
        audiences = variables_config['audiences']['high_priority']
        use_cases = variables_config['use_cases']['high_priority']
        tool_types = variables_config['tool_types']['high_priority']
    else:
        competitors = variables_config['competitors']['all']
        platforms = variables_config['platforms']['all']
        audiences = variables_config['audiences']['all']
        use_cases = variables_config['use_cases']['all']
        tool_types = variables_config['tool_types']['all']
    
    for pattern in patterns_config['patterns']:
        pattern_id = pattern['id']
        pattern_vars = pattern['variables']
        
        # Generate combinations based on required variables
        if pattern_vars == ['competitor', 'audience']:
            for comp in competitors:
                for aud in audiences:
                    pages.append(create_page_data(pattern, {
                        'competitor': comp,
                        'audience': aud
                    }))
        
        elif pattern_vars == ['use_case', 'audience']:
            for use_case in use_cases:
                for aud in audiences:
                    pages.append(create_page_data(pattern, {
                        'use_case': use_case,
                        'audience': aud
                    }))
        
        elif pattern_vars == ['platform', 'tool_type']:
            for plat in platforms:
                for tool in tool_types:
                    pages.append(create_page_data(pattern, {
                        'platform': plat,
                        'tool_type': tool
                    }))
        
        elif pattern_vars == ['platform', 'audience']:
            for plat in platforms:
                for aud in audiences:
                    pages.append(create_page_data(pattern, {
                        'platform': plat,
                        'audience': aud
                    }))
        
        elif pattern_vars == ['audience']:
            for aud in audiences:
                pages.append(create_page_data(pattern, {
                    'audience': aud
                }))
    
    return pages

def create_page_data(pattern, variables):
    """Create base page data structure"""
    # Build URL
    url = pattern['url_formula']
    h1 = pattern['h1_formula']
    
    for var_name, var_value in variables.items():
        url = url.replace(f'{{{var_name}}}', var_value.lower().replace(' ', '-'))

        # Handle capitalization in H1
        # Try .title() first for multi-word variables (use_case -> Use_Case, tool_type -> Tool_Type)
        if f'{{{var_name.title()}}}' in h1:
            h1 = h1.replace(f'{{{var_name.title()}}}', var_value)
        elif f'{{{var_name.capitalize()}}}' in h1:
            h1 = h1.replace(f'{{{var_name.capitalize()}}}', var_value)
        elif f'{{{var_name.upper()}}}' in h1:
            h1 = h1.replace(f'{{{var_name.upper()}}}', var_value)
    
    page_data = {
        'pattern_id': pattern['id'],
        'pattern_name': pattern['name'],
        'url': url,
        'h1': h1,
        'eyebrow': pattern['eyebrow'],
        'primary_cta': pattern['primary_cta'],
        'secondary_cta': pattern['secondary_cta'],
        'show_comparison_table': pattern['show_comparison_table'],
        **variables
    }
    
    return page_data

def generate_content_with_claude(page_data, section):
    """Use Claude to generate content for a specific section"""
    
    # Get the template for this section
    template_config = content_templates['sections'][section]
    prompt_template = template_config['prompt_template']
    
    # Prepare variables for prompt
    variables_str = ", ".join([f"{k}: {v}" for k, v in page_data.items() 
                               if k not in ['pattern_id', 'pattern_name', 'url', 'h1', 'eyebrow', 
                                           'primary_cta', 'secondary_cta', 'show_comparison_table']])
    
    # Special handling for problem_agitation section (needs viral hook)
    if section == "problem_agitation":
        viral_hook = random.choice(viral_hooks['hooks'])
        prompt = prompt_template.format(
            pattern_name=page_data['pattern_name'],
            pattern_id=page_data['pattern_id'],
            h1=page_data['h1'],
            variables=variables_str,
            viral_hook=viral_hook
        )
    else:
        prompt = prompt_template.format(
            pattern_name=page_data['pattern_name'],
            pattern_id=page_data.get('pattern_id', ''),
            h1=page_data['h1'],
            variables=variables_str
        )
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=template_config['max_tokens'],
                temperature=template_config.get('temperature', 0.7),
            )
        )

        content = response.text
        return content.strip()
    
    except Exception as e:
        print(f"  ⚠️  Error generating {section}: {e}")
        return f"[ERROR: {section}]"

def generate_all_pages(limit=None, priority_only=False):
    """Generate all page content"""
    
    print("\n🚀 Sozee Landing Page Generator")
    print("=" * 50)
    
    # Generate all combinations
    print("\n📋 Generating page combinations...")
    pages = generate_page_combinations(priority_only=priority_only)
    
    if limit:
        pages = pages[:limit]
        print(f"   Limited to first {limit} pages for testing")
    
    print(f"   Total pages to generate: {len(pages)}")
    
    # Estimate cost
    total_api_calls = len(pages) * 4  # 4 sections per page
    estimated_tokens = total_api_calls * 500
    estimated_cost = (estimated_tokens / 1_000_000) * 3
    print(f"   Estimated API calls: {total_api_calls:,}")
    print(f"   Estimated cost: ${estimated_cost:.2f}")
    
    # Confirm if generating many pages
    if len(pages) > 50 and not limit:
        response = input(f"\n⚠️  You're about to generate {len(pages)} pages. Continue? (y/n): ")
        if response.lower() != 'y':
            print("❌ Cancelled")
            return None
    
    print("\n🎨 Generating content...\n")
    
    # Generate content for each page
    results = []
    start_time = time.time()
    
    for i, page in enumerate(pages):
        print(f"📄 [{i+1}/{len(pages)}] {page['url']}")
        
        # Generate each section
        sections = {}
        for section_name in ['hero_subtitle', 'problem_agitation', 'faq', 'meta_description']:
            print(f"   → Generating {section_name}...", end='', flush=True)
            content = generate_content_with_claude(page, section_name)
            sections[section_name] = content
            print(" ✓")
            time.sleep(0.5)  # Brief pause between sections
        
        # Combine all data
        result = {
            'pattern': page['pattern_id'],
            'pattern_name': page['pattern_name'],
            'url': page['url'],
            'h1': page['h1'],
            'eyebrow': page['eyebrow'],
            'hero_subtitle': sections['hero_subtitle'],
            'problem_agitation': sections['problem_agitation'],
            'faq': sections['faq'],
            'meta_title': f"{page['h1']} | Sozee",
            'meta_description': sections['meta_description'],
            'primary_cta': page['primary_cta'],
            'secondary_cta': page['secondary_cta'],
            'show_comparison_table': page['show_comparison_table'],
            'status': 'draft',
            'generated_at': datetime.now().isoformat()
        }
        
        # Add all variables
        for var_name in ['competitor', 'audience', 'platform', 'tool_type', 'use_case']:
            result[var_name] = page.get(var_name, '')
        
        results.append(result)
        
        # Rate limiting - 1 second between pages (4 calls per page)
        time.sleep(1)
        
        # Save progress every 10 pages
        if (i + 1) % 10 == 0:
            df = pd.DataFrame(results)
            os.makedirs('output/progress', exist_ok=True)
            df.to_csv('output/progress/sozee_landing_pages_progress.csv', index=False)
            
            elapsed = time.time() - start_time
            avg_per_page = elapsed / (i + 1)
            remaining_pages = len(pages) - (i + 1)
            eta_seconds = remaining_pages * avg_per_page
            eta_minutes = eta_seconds / 60
            
            print(f"   💾 Progress saved: {i+1} pages | ETA: {eta_minutes:.1f} min\n")
    
    # Save final CSV
    os.makedirs('output', exist_ok=True)
    df = pd.DataFrame(results)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'output/sozee_landing_pages_{timestamp}.csv'
    df.to_csv(output_file, index=False)
    
    # Print summary
    total_time = time.time() - start_time
    print("\n" + "=" * 50)
    print(f"✅ Complete! Generated {len(results)} pages")
    print(f"⏱️  Total time: {total_time/60:.1f} minutes")
    print(f"📁 Saved to: {output_file}")
    print("\n📊 Page counts by pattern:")
    pattern_counts = df.groupby('pattern_name').size().to_dict()
    for pattern_name, count in pattern_counts.items():
        print(f"   {pattern_name}: {count} pages")
    
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Sozee landing pages')
    parser.add_argument('--limit', type=int, help='Limit number of pages to generate (for testing)')
    parser.add_argument('--priority-only', action='store_true', 
                       help='Only generate pages with high-priority variables')
    
    args = parser.parse_args()
    
    # Check for API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        print("   Create a .env file with: GEMINI_API_KEY=your-key-here")
        exit(1)
    
    # Run generator
    df = generate_all_pages(limit=args.limit, priority_only=args.priority_only)
