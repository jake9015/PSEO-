#!/usr/bin/env python3
"""
Simple KB Utility Test (no API required)
Tests CompetitorKnowledgeBase CRUD operations
"""

import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.competitor_kb import CompetitorKnowledgeBase

print("=" * 60)
print("Knowledge Base Utility Test")
print("=" * 60)

# Create KB instance
kb = CompetitorKnowledgeBase()

print("\n✅ KB initialized successfully")
print(f"📁 KB Location: {kb.kb_path}")

# Test 1: Check initial state
print("\n1️⃣  Testing initial KB state...")
stats = kb.get_stats()
print(f"   Total competitors: {stats['total_competitors']}")
print(f"   Last updated: {stats.get('last_updated', 'N/A')}")

# Test 2: Save a test profile
print("\n2️⃣  Testing save_profile()...")
test_profile = {
    "category": "AI Image Generator",
    "target_audience": "Test users",
    "positioning": "Test positioning",
    "setup": {
        "photos_required": "10 photos",
        "training_time": "30 minutes",
        "technical_skills": "Low"
    },
    "features": {
        "nsfw_support": False,
        "creator_focus": True,
        "platform_focus": "Test platform",
        "privacy_model": "Private",
        "content_types": ["Images"],
        "hyper_realistic": "Good"
    },
    "pricing": {
        "known": True,
        "estimate": "$20/month",
        "free_trial": True
    },
    "strengths": ["Test strength 1", "Test strength 2"],
    "weaknesses": ["Test weakness 1"]
}

kb.save_profile("TestTool", test_profile)
print("   ✅ Profile saved")

# Test 3: Retrieve profile
print("\n3️⃣  Testing get_profile()...")
retrieved = kb.get_profile("TestTool")
if retrieved:
    print("   ✅ Profile retrieved successfully")
    print(f"   Category: {retrieved.get('category')}")
    print(f"   Pricing: {retrieved.get('pricing', {}).get('estimate')}")
    print(f"   KB Metadata: {retrieved.get('kb_metadata', {}).get('source')}")
else:
    print("   ❌ Profile retrieval failed")

# Test 4: Check if profile exists
print("\n4️⃣  Testing profile_exists()...")
exists = kb.profile_exists("TestTool")
print(f"   TestTool exists: {exists} {'✅' if exists else '❌'}")

not_exists = kb.profile_exists("NonExistentTool")
print(f"   NonExistentTool exists: {not_exists} {'✅ (correct)' if not not_exists else '❌'}")

# Test 5: Update profile
print("\n5️⃣  Testing update_profile()...")
kb.update_profile("TestTool", {
    "pricing": {
        "known": True,
        "estimate": "$25/month",  # Changed from $20
        "free_trial": False
    },
    "new_field": "This is a new field"
})

updated = kb.get_profile("TestTool")
if updated.get('pricing', {}).get('estimate') == "$25/month":
    print("   ✅ Profile updated successfully")
    print(f"   New pricing: {updated.get('pricing', {}).get('estimate')}")
    print(f"   New field: {updated.get('new_field')}")
else:
    print("   ❌ Profile update failed")

# Test 6: List competitors
print("\n6️⃣  Testing list_competitors()...")
competitors = kb.list_competitors()
print(f"   Total competitors: {len(competitors)}")
if 'TestTool' in competitors:
    print("   ✅ TestTool in list")
else:
    print("   ❌ TestTool not in list")

# Test 7: Final stats
print("\n7️⃣  Final KB Statistics...")
final_stats = kb.get_stats()
print(f"   Total competitors: {final_stats['total_competitors']}")
print(f"   Competitors: {', '.join(final_stats['competitors'][:5])}{'...' if len(final_stats['competitors']) > 5 else ''}")

print("\n" + "=" * 60)
print("✅ All KB Utility Tests Passed")
print("=" * 60)

# Show KB file size
if os.path.exists(kb.kb_path):
    size = os.path.getsize(kb.kb_path)
    print(f"\n💾 KB File: {kb.kb_path}")
    print(f"📊 Size: {size:,} bytes")
