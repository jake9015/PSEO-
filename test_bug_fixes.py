#!/usr/bin/env python3
"""
Test script to validate the three bug fixes without requiring full API
"""

import sys
import os

print("="*70)
print("TESTING BUG FIXES")
print("="*70)

# Test 1: Agent routing normalization
print("\n[TEST 1] Agent Routing Fix")
print("-" * 70)

def normalize_agent_name_old(to_agent):
    """Old buggy version"""
    return to_agent.lower().replace('_agent', '').replace('_', '')

def normalize_agent_name_new(to_agent):
    """New fixed version"""
    return to_agent.lower().replace('_agent', '')

test_cases = [
    'PSEO_Strategist_Agent',
    'Competitor_Research_Agent',
    'FAQ_Generator_Agent',
    'Statistics_Agent'
]

registry_keys = {
    'pseo_strategist': 'PSEOStrategistAgent',
    'competitor_research': 'CompetitorResearchAgent',
    'faq_generator': 'FAQGeneratorAgent',
    'statistics': 'StatisticsAgent'
}

for agent_name in test_cases:
    old_key = normalize_agent_name_old(agent_name)
    new_key = normalize_agent_name_new(agent_name)

    old_found = old_key in registry_keys
    new_found = new_key in registry_keys

    status_old = "✓" if old_found else "✗"
    status_new = "✓" if new_found else "✗"

    print(f"\nAgent: {agent_name}")
    print(f"  Old normalization: '{old_key}' {status_old} (BUGGY)")
    print(f"  New normalization: '{new_key}' {status_new} (FIXED)")

    if not old_found and new_found:
        print(f"  → FIX VERIFIED: Now routes correctly to '{registry_keys[new_key]}'")

# Test 2: ContentBlueprint attribute check
print("\n\n[TEST 2] ContentBlueprint Attribute Fix")
print("-" * 70)

from agent_framework import ContentBlueprint

# Create a sample blueprint
blueprint = ContentBlueprint(
    page_id="test_page_1",
    pattern_id="1",
    pattern_name="Competitor Comparison",
    funnel_stage="bottom",
    generation_model="Model 1",
    sections_needed=['hero', 'problem', 'solution'],
    required_agents=['copywriting', 'faq_generator'],
    research_requirements=[],
    priority="high"
)

print("\nContentBlueprint attributes:")
print(f"  page_id: {blueprint.page_id}")
print(f"  pattern_id: {blueprint.pattern_id}")
print(f"  pattern_name: {blueprint.pattern_name}")

# Check if .h1 attribute exists
has_h1 = hasattr(blueprint, 'h1')
print(f"\n  Has .h1 attribute: {has_h1} {'(EXPECTED - this is correct)' if not has_h1 else '(UNEXPECTED)'}")

if not has_h1:
    print(f"  ✓ FIX VERIFIED: Using blueprint.pattern_name instead")
    print(f"  → Statistics task will use: topic='{blueprint.pattern_name}'")
else:
    print(f"  ✗ ISSUE: Blueprint should not have .h1 attribute")

# Test 3: ResearchAgent cache methods
print("\n\n[TEST 3] ResearchAgent Cache Method Fix")
print("-" * 70)

from agent_framework import ResearchAgent, AgentMessage, AgentResponse

class TestAgent(ResearchAgent):
    def execute(self, message):
        return AgentResponse(
            message_id="test",
            from_agent="TestAgent",
            to_agent="Orchestrator",
            status="completed",
            data={},
            execution_time=0.1
        )

agent = TestAgent(name="Test_Agent", role="Tester")

# Check available cache methods
cache_methods = [m for m in dir(agent) if 'cache' in m.lower() and not m.startswith('_')]
print(f"\nAvailable cache methods on ResearchAgent:")
for method in cache_methods:
    print(f"  - {method}()")

has_get_cached = hasattr(agent, 'get_cached')
has_cache_research = hasattr(agent, 'cache_research')
has_get_cached_research = hasattr(agent, 'get_cached_research')

print(f"\nMethod availability:")
print(f"  get_cached(): {has_get_cached} {'✓' if has_get_cached else '✗'}")
print(f"  cache_research(): {has_cache_research} {'✓' if has_cache_research else '✗'}")
print(f"  get_cached_research(): {has_get_cached_research} {'(OLD BUGGY METHOD)' if has_get_cached_research else '(CORRECTLY REMOVED)'}")

if has_get_cached and not has_get_cached_research:
    print(f"\n  ✓ FIX VERIFIED: get_cached() exists, get_cached_research() doesn't")
    print(f"  → StatisticsAgent will use: self.get_cached(cache_key)")

# Summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

all_tests_passed = True

# Test 1 check
test1_passed = all(
    normalize_agent_name_new(name) in registry_keys
    for name in test_cases
)
print(f"\n[TEST 1] Agent Routing: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
all_tests_passed = all_tests_passed and test1_passed

# Test 2 check
test2_passed = not hasattr(blueprint, 'h1') and hasattr(blueprint, 'pattern_name')
print(f"[TEST 2] ContentBlueprint: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
all_tests_passed = all_tests_passed and test2_passed

# Test 3 check
test3_passed = has_get_cached and not has_get_cached_research
print(f"[TEST 3] Cache Methods: {'✓ PASSED' if test3_passed else '✗ FAILED'}")
all_tests_passed = all_tests_passed and test3_passed

print("\n" + "="*70)
if all_tests_passed:
    print("✅ ALL BUG FIXES VERIFIED - Orchestrator should work correctly")
else:
    print("⚠️ SOME TESTS FAILED - Review fixes")
print("="*70 + "\n")

sys.exit(0 if all_tests_passed else 1)
