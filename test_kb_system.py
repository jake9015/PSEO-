#!/usr/bin/env python3
"""
Test Agent-Managed Knowledge Base System
Tests that CompetitorResearchAgent automatically populates KB
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.competitor_kb import CompetitorKnowledgeBase
from agents.competitor_research import CompetitorResearchAgent
from agent_framework import AgentMessage
import google.generativeai as genai

# Configure Gemini (use env variable)
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY not set")
    sys.exit(1)

genai.configure(api_key=api_key)

print("=" * 60)
print("Agent-Managed Knowledge Base System Test")
print("=" * 60)

# Test 1: KB Utility Functions
print("\n1️⃣  Testing KB Utility Class...")
kb = CompetitorKnowledgeBase()

# Check initial state
stats = kb.get_stats()
print(f"   Initial KB stats: {stats['total_competitors']} competitors")

# Test 2: Research Agent Auto-Save
print("\n2️⃣  Testing CompetitorResearchAgent auto-save to KB...")
print("   Researching 'TestCompetitor' (not in KB)...")

research_agent = CompetitorResearchAgent()

# Create test message
test_message = AgentMessage(
    msg_id="test_001",
    from_agent="test",
    to_agent="competitor_research",
    task={
        'competitor': 'TestCompetitor',
        'audience': 'creators',
        'required_data': ['pricing', 'features', 'setup']
    },
    context={},
    priority="high"
)

# Execute research (should auto-save to KB)
response = research_agent.execute(test_message)

print(f"   Research status: {response.status}")
print(f"   Confidence: {response.confidence}")

# Test 3: Verify KB was updated
print("\n3️⃣  Verifying KB was updated...")
kb_after = CompetitorKnowledgeBase()
stats_after = kb_after.get_stats()
print(f"   KB stats after research: {stats_after['total_competitors']} competitors")

if kb_after.profile_exists('TestCompetitor'):
    print("   ✅ TestCompetitor found in KB!")
    profile = kb_after.get_profile('TestCompetitor')
    print(f"   Category: {profile.get('category')}")
    print(f"   NSFW Support: {profile.get('features', {}).get('nsfw_support')}")
    print(f"   Pricing: {profile.get('pricing', {}).get('estimate')}")
    if 'kb_metadata' in profile:
        print(f"   Added at: {profile['kb_metadata'].get('added_at')}")
else:
    print("   ❌ TestCompetitor NOT in KB (auto-save failed)")

# Test 4: Second request should use KB (no new research)
print("\n4️⃣  Testing KB retrieval on second request...")
print("   Requesting TestCompetitor again (should use KB)...")

test_message2 = AgentMessage(
    msg_id="test_002",
    from_agent="test",
    to_agent="competitor_research",
    task={
        'competitor': 'TestCompetitor',
        'audience': 'creators',
        'required_data': ['pricing', 'features']
    },
    context={},
    priority="high"
)

response2 = research_agent.execute(test_message2)
print(f"   Response status: {response2.status}")
print(f"   Confidence: {response2.confidence} (should be 0.95 for KB data)")

if response2.confidence == 0.95:
    print("   ✅ Used KB data (confidence = 0.95)")
else:
    print("   ⚠️ May not have used KB (confidence != 0.95)")

# Test 5: Manual KB operations
print("\n5️⃣  Testing manual KB operations...")

# Test update
print("   Testing profile update...")
kb_after.update_profile('TestCompetitor', {
    'features': {
        'nsfw_support': True,
        'creator_focus': True
    },
    'custom_field': 'Manual update test'
})

updated_profile = kb_after.get_profile('TestCompetitor')
if updated_profile.get('custom_field') == 'Manual update test':
    print("   ✅ Profile update works")
else:
    print("   ❌ Profile update failed")

# Test list competitors
print("\n6️⃣  Current KB Contents...")
competitors_list = kb_after.list_competitors()
print(f"   Total competitors in KB: {len(competitors_list)}")
print(f"   Competitors: {', '.join(competitors_list[:5])}{'...' if len(competitors_list) > 5 else ''}")

print("\n" + "=" * 60)
print("✅ Knowledge Base System Test Complete")
print("=" * 60)

# Show KB file location
print(f"\n📁 KB Location: {kb_after.kb_path}")
print(f"💾 KB File Size: {os.path.getsize(kb_after.kb_path)} bytes")
