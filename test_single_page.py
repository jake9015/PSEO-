#!/usr/bin/env python3
"""
Single Page Test Script
Tests content generation for a specific keyword/topic and validates quality
"""

import json
import os
from dotenv import load_dotenv
from pseo_orchestrator import PSEOOrchestrator

# Load environment
load_dotenv()


def test_competitor_comparison():
    """Test: Sozee vs Higgsfield for OnlyFans Agencies"""

    print("\n" + "="*80)
    print("TEST 1: Competitor Comparison (Bottom-Funnel)")
    print("Keyword: 'sozee vs higgsfield for onlyfans agencies'")
    print("="*80)

    # Load configuration
    with open('config/patterns.json', 'r') as f:
        patterns = json.load(f)

    with open('config/variables.json', 'r') as f:
        variables = json.load(f)

    viral_hooks = []
    if os.path.exists('config/viral_hooks.json'):
        with open('config/viral_hooks.json', 'r') as f:
            hooks_data = json.load(f)
            viral_hooks = hooks_data.get('hooks', [])

    # Create config
    config = {
        'pattern_library': patterns,
        'variables': variables,
        'viral_hooks': viral_hooks,
        'gemini_api_key': os.environ.get('GEMINI_API_KEY')
    }

    # Initialize orchestrator
    orchestrator = PSEOOrchestrator(config)

    # Generate page
    page = orchestrator.generate_page(
        pattern_id='1',
        variables={
            'competitor': 'Higgsfield',
            'audience': 'OnlyFans Agencies'
        }
    )

    # Validate and display results
    validate_page_quality(page, expected_keyword='sozee vs higgsfield')

    # Save for manual review
    output_file = 'output/test_competitor_comparison.json'
    with open(output_file, 'w') as f:
        f.write(page.to_json())

    print(f"\n✅ Full page saved to: {output_file}")
    print("   Review this file to validate content quality")

    return page


def test_best_tool():
    """Test: Best AI Photo Generator for OnlyFans Creators"""

    print("\n" + "="*80)
    print("TEST 2: Best Tool (Mid-Funnel)")
    print("Keyword: 'best ai photo generator for onlyfans creators'")
    print("="*80)

    # Load configuration
    with open('config/patterns.json', 'r') as f:
        patterns = json.load(f)

    with open('config/variables.json', 'r') as f:
        variables = json.load(f)

    viral_hooks = []
    if os.path.exists('config/viral_hooks.json'):
        with open('config/viral_hooks.json', 'r') as f:
            hooks_data = json.load(f)
            viral_hooks = hooks_data.get('hooks', [])

    config = {
        'pattern_library': patterns,
        'variables': variables,
        'viral_hooks': viral_hooks,
        'gemini_api_key': os.environ.get('GEMINI_API_KEY')
    }

    orchestrator = PSEOOrchestrator(config)

    page = orchestrator.generate_page(
        pattern_id='2',
        variables={
            'tool_type': 'AI Photo Generator',
            'audience': 'OnlyFans Creators',
            'platform': 'OnlyFans'
        }
    )

    validate_page_quality(page, expected_keyword='best ai photo generator')

    output_file = 'output/test_best_tool.json'
    with open(output_file, 'w') as f:
        f.write(page.to_json())

    print(f"\n✅ Full page saved to: {output_file}")

    return page


def test_alternative_search():
    """Test: Krea Alternative for Content Creators"""

    print("\n" + "="*80)
    print("TEST 3: Alternative Search (Bottom-Funnel)")
    print("Keyword: 'krea alternative for content creators'")
    print("="*80)

    with open('config/patterns.json', 'r') as f:
        patterns = json.load(f)

    with open('config/variables.json', 'r') as f:
        variables = json.load(f)

    viral_hooks = []
    if os.path.exists('config/viral_hooks.json'):
        with open('config/viral_hooks.json', 'r') as f:
            hooks_data = json.load(f)
            viral_hooks = hooks_data.get('hooks', [])

    config = {
        'pattern_library': patterns,
        'variables': variables,
        'viral_hooks': viral_hooks,
        'gemini_api_key': os.environ.get('GEMINI_API_KEY')
    }

    orchestrator = PSEOOrchestrator(config)

    page = orchestrator.generate_page(
        pattern_id='4',
        variables={
            'competitor': 'Krea',
            'audience': 'Content Creators'
        }
    )

    validate_page_quality(page, expected_keyword='krea alternative')

    output_file = 'output/test_alternative.json'
    with open(output_file, 'w') as f:
        f.write(page.to_json())

    print(f"\n✅ Full page saved to: {output_file}")

    return page


def validate_page_quality(page, expected_keyword):
    """Validate generated page quality"""

    print("\n📊 QUALITY VALIDATION REPORT")
    print("-" * 80)

    # 1. SEO Validation
    print("\n1. SEO METADATA:")
    print(f"   Meta Title: {page.meta_title}")
    print(f"   Length: {len(page.meta_title)} chars (target: 50-60)")
    print(f"   ✓ Contains 'Sozee': {'Sozee' in page.meta_title}")
    print(f"   ✓ Contains keyword: {expected_keyword.lower() in page.meta_title.lower()}")

    print(f"\n   Meta Description: {page.meta_description}")
    print(f"   Length: {len(page.meta_description)} chars (target: 150-160)")
    print(f"   ✓ Has CTA: {any(cta in page.meta_description.lower() for cta in ['try', 'start', 'get', 'learn', 'discover'])}")

    print(f"\n   URL Slug: {page.url_slug}")
    print(f"   ✓ Lowercase: {page.url_slug == page.url_slug.lower()}")
    print(f"   ✓ No spaces: {' ' not in page.url_slug}")

    # 2. Content Completeness
    print("\n2. CONTENT COMPLETENESS:")
    print(f"   ✓ H1: {page.hero_section.get('h1', 'MISSING')}")
    print(f"   ✓ Subtitle: {'✓' if page.hero_section.get('subtitle') else '✗ MISSING'}")
    print(f"   ✓ Problem Section: {len(page.problem_agitation)} chars")
    print(f"   ✓ Solution Section: {len(page.solution_overview)} chars")
    print(f"   ✓ FAQs: {len(page.faq_json)} questions")
    print(f"   ✓ Features: {len(page.feature_sections)} sections")

    # 3. Brand Voice
    print("\n3. BRAND VOICE:")
    all_text = f"{page.problem_agitation} {page.solution_overview} {page.final_cta}"
    print(f"   ✓ Sozee mentions: {all_text.count('Sozee')}")
    print(f"   ✓ Contains 'LORA': {'LORA' in all_text or 'lora' in all_text.lower()}")
    print(f"   ✓ Contains 'OnlyFans': {'OnlyFans' in all_text}")
    print(f"   ✓ Contains 'creator': {'creator' in all_text.lower()}")

    # 4. Quality Score
    print("\n4. QUALITY METRICS:")
    print(f"   Overall Score: {page.quality_score:.2f}")
    print(f"   Status: {page.uniqueness_check}")
    print(f"   Generation Model: {page.generation_model}")
    print(f"   Agents Used: {len(page.agents_used)} agents")

    # 5. Content Preview
    print("\n5. CONTENT PREVIEW:")
    print(f"\n   Hero Section:")
    print(f"   {page.hero_section.get('h1', '')}")
    print(f"   {page.hero_section.get('subtitle', '')}")

    print(f"\n   Problem Section (first 200 chars):")
    print(f"   {page.problem_agitation[:200]}...")

    if page.faq_json:
        print(f"\n   Sample FAQ:")
        print(f"   Q: {page.faq_json[0]['question']}")
        print(f"   A: {page.faq_json[0]['answer'][:150]}...")

    # 6. Validation Summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY:")

    issues = []
    warnings = []

    # Check critical issues
    if len(page.meta_title) < 50 or len(page.meta_title) > 60:
        warnings.append(f"Meta title length: {len(page.meta_title)} (should be 50-60)")

    if len(page.meta_description) < 150 or len(page.meta_description) > 160:
        warnings.append(f"Meta description length: {len(page.meta_description)} (should be 150-160)")

    if 'Sozee' not in page.meta_title:
        issues.append("Meta title missing 'Sozee'")

    if expected_keyword.lower() not in page.meta_title.lower():
        issues.append(f"Meta title missing target keyword: {expected_keyword}")

    if not page.hero_section.get('subtitle'):
        issues.append("Missing hero subtitle")

    if len(page.problem_agitation) < 200:
        issues.append("Problem section too short")

    if len(page.faq_json) < 3:
        warnings.append(f"Only {len(page.faq_json)} FAQs (target: 5)")

    if page.quality_score < 0.7:
        issues.append(f"Low quality score: {page.quality_score}")

    # Display results
    if issues:
        print("❌ CRITICAL ISSUES:")
        for issue in issues:
            print(f"   - {issue}")

    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   - {warning}")

    if not issues and not warnings:
        print("✅ ALL CHECKS PASSED - Content is ready for publication!")
    elif not issues:
        print("✅ PASSED WITH WARNINGS - Review and publish")
    else:
        print("❌ FAILED - Fix critical issues before publishing")

    print("="*80)


def main():
    """Run all tests"""

    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                                 ║
    ║         PSEO Content Quality Test Suite                        ║
    ║         Tests single pages for different keywords              ║
    ║                                                                 ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    # Check API key
    if not os.environ.get('GEMINI_API_KEY'):
        print("❌ Error: GEMINI_API_KEY not found!")
        print("   Please set it in .env file")
        return

    # Create output directory
    os.makedirs('output', exist_ok=True)

    # Run tests
    print("\nSelect test to run:")
    print("1. Competitor Comparison (Sozee vs Higgsfield)")
    print("2. Best Tool (Best AI Photo Generator)")
    print("3. Alternative Search (Krea Alternative)")
    print("4. Run All Tests")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == '1':
        test_competitor_comparison()
    elif choice == '2':
        test_best_tool()
    elif choice == '3':
        test_alternative_search()
    elif choice == '4':
        print("\nRunning all tests sequentially...\n")
        test_competitor_comparison()
        test_best_tool()
        test_alternative_search()
    else:
        print("Invalid choice")
        return

    print("\n" + "="*80)
    print("✅ TESTING COMPLETE")
    print("="*80)
    print("\nNext steps:")
    print("1. Review the JSON files in output/ directory")
    print("2. Check that content matches your quality standards")
    print("3. Verify keyword targeting is accurate")
    print("4. If satisfied, run batch_generator.py for Week 1")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
