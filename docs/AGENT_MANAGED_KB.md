# Agent-Managed Knowledge Base System

## Overview

The PSEO system now features an **agent-managed competitor knowledge base** that automatically populates and maintains competitor profiles during page generation. This eliminates manual data entry and ensures accurate, research-based competitor information.

## Architecture

### Components

1. **CompetitorKnowledgeBase** (`utils/competitor_kb.py`)
   - Utility class for CRUD operations on `config/competitor_profiles.json`
   - Handles JSON file persistence with automatic timestamping
   - Supports deep merge for profile updates

2. **CompetitorResearchAgent** (`agents/competitor_research.py`)
   - Researches competitors using Gemini AI
   - Structures findings to match KB schema
   - **Automatically saves profiles to KB** after research
   - Checks KB before doing new research (efficiency)

3. **ComparisonTableAgent** (`agents/comparison_table.py`)
   - Loads KB profiles for comparison tables
   - Merges KB data with fresh research (research takes priority)
   - Eliminates "Not specified" values using KB fallbacks

## Workflow

```
┌─────────────────────────────────────────────────┐
│  Page Generation Request                        │
│  (competitor: "Higgsfield")                     │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│  CompetitorResearchAgent.execute()              │
│                                                  │
│  1. Check KB: Does "Higgsfield" exist?          │
│     └─ YES → Return KB profile (confidence 0.95)│
│     └─ NO  → Continue to step 2                 │
│                                                  │
│  2. Check memory cache                          │
│     └─ YES → Return cached (confidence 0.9)     │
│     └─ NO  → Continue to step 3                 │
│                                                  │
│  3. Perform fresh AI research                   │
│     └─ Structure output to match KB schema      │
│     └─ Auto-save to KB                          │
│     └─ Cache results                            │
│     └─ Return research (confidence 0.85)        │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│  ComparisonTableAgent.execute()                 │
│                                                  │
│  1. Get research data from context              │
│  2. Load KB profile for competitor              │
│  3. Merge: research + KB (research priority)    │
│  4. Generate comparison table                   │
│     └─ Use specific values where available      │
│     └─ Fall back to KB for missing data         │
│     └─ Use category-level descriptions          │
│     └─ NEVER say "Not specified"                │
└─────────────────────────────────────────────────┘
```

## Knowledge Base Schema

Each competitor profile in `config/competitor_profiles.json` follows this structure:

```json
{
  "CompetitorName": {
    "category": "AI Image Generator",
    "target_audience": "OnlyFans creators, adult content creators",
    "positioning": "Adult creator content tool",

    "setup": {
      "photos_required": "Training images required",
      "training_time": "30-60 minutes",
      "technical_skills": "Low"
    },

    "features": {
      "nsfw_support": true,
      "creator_focus": true,
      "platform_focus": "OnlyFans, adult platforms",
      "privacy_model": "Private models",
      "content_types": ["Images"],
      "hyper_realistic": "Good quality"
    },

    "pricing": {
      "known": true,
      "estimate": "$30-50/month",
      "free_trial": false
    },

    "strengths": [
      "NSFW support",
      "Creator-focused",
      "OnlyFans integration"
    ],

    "weaknesses": [
      "Requires training",
      "No instant setup",
      "Limited to images"
    ],

    "kb_metadata": {
      "added_at": "2025-11-10T12:00:00",
      "last_updated": "2025-11-10T13:00:00",
      "source": "agent_research"
    }
  }
}
```

## Key Features

### 1. Automatic Population
- **No manual data entry required**
- Agents research and save profiles automatically
- KB grows organically as pages are generated

### 2. Intelligent Caching
- **3-tier lookup**: KB → Memory Cache → Fresh Research
- Fast retrieval for known competitors
- Efficient API usage

### 3. Accurate Data
- **Research-based profiles** (not marketing claims)
- Structured output ensures consistency
- Fallback profiles for edge cases

### 4. Version Control Friendly
- **File-based storage** (`competitor_profiles.json`)
- JSON format for easy diffs
- Timestamped updates

### 5. Eliminates "Not Specified"
- **KB provides fallbacks** for missing research data
- Category-level descriptions when specifics unknown
- Comparison tables always have meaningful content

## Usage Examples

### CompetitorKnowledgeBase Utility

```python
from utils.competitor_kb import CompetitorKnowledgeBase

kb = CompetitorKnowledgeBase()

# Check if competitor exists
if kb.profile_exists("Higgsfield"):
    profile = kb.get_profile("Higgsfield")
    print(profile['category'])

# Save new profile
kb.save_profile("NewTool", {
    "category": "AI Platform",
    "setup": {...},
    "features": {...},
    "pricing": {...},
    "strengths": [...],
    "weaknesses": [...]
})

# Update existing profile
kb.update_profile("NewTool", {
    "pricing": {"estimate": "$25/month"}
})

# Get statistics
stats = kb.get_stats()
print(f"Total competitors: {stats['total_competitors']}")
```

### CompetitorResearchAgent

```python
from agents.competitor_research import CompetitorResearchAgent
from agent_framework import AgentMessage

agent = CompetitorResearchAgent()

message = AgentMessage(
    msg_id="001",
    from_agent="orchestrator",
    to_agent="competitor_research",
    task={
        'competitor': 'Foxy AI',
        'audience': 'OnlyFans creators',
        'required_data': ['pricing', 'features', 'setup']
    },
    context={},
    priority="high"
)

# Research and auto-save to KB
response = agent.execute(message)

# Second request uses KB (no new research)
response2 = agent.execute(message)
print(response2.confidence)  # 0.95 (from KB)
```

## Benefits

### For Content Quality
- ✅ **Accurate competitor data** based on AI research
- ✅ **No "Not specified" values** in comparison tables
- ✅ **Consistent formatting** across all profiles
- ✅ **SEO-optimized descriptions** using real data

### For Development
- ✅ **Zero manual maintenance** - agents handle everything
- ✅ **Version controlled** - KB changes tracked in git
- ✅ **Testable** - utility class with clear interface
- ✅ **Extensible** - easy to add new fields

### For Performance
- ✅ **Fast lookups** - KB check before research
- ✅ **Reduced API calls** - reuse existing profiles
- ✅ **Efficient caching** - 3-tier retrieval system
- ✅ **Scalable** - KB grows without performance impact

## Maintenance

### KB File Location
```
config/competitor_profiles.json
```

### Automatic Updates
- Agents add new competitors automatically
- Timestamps track when profiles were added/updated
- Total competitor count updates on every save

### Manual Intervention (Optional)
If you need to manually edit a profile:

1. Edit `config/competitor_profiles.json` directly
2. Update `kb_metadata.last_updated` to current timestamp
3. Commit changes to version control

The system will merge any manual changes with future agent research.

## Testing

Run the KB utility test:
```bash
python test_kb_utility.py
```

This tests:
- KB initialization
- Profile save/retrieve
- Profile updates
- Deep merge logic
- Statistics tracking

## Migration

### Existing Competitors
The KB ships with 16 pre-researched competitors:
- Higgsfield, Krea, Midjourney, Stability AI, Runway
- Leonardo AI, Civitai, Pykaso, Foxy AI, PhotoAI
- Fooocus, InvokeAI, ComfyUI, Automatic1111
- Supercreator, Glambase, DeepMode

### New Competitors
Any new competitor mentioned in page generation will be:
1. Researched automatically
2. Saved to KB
3. Available for all future pages

## Technical Details

### Deep Merge Logic
When updating profiles, new data takes priority:
```python
existing = {"pricing": {"known": false, "estimate": "$20"}}
update = {"pricing": {"known": true}}

result = {"pricing": {"known": true, "estimate": "$20"}}
```

### Confidence Scoring
- **KB data**: 0.95 (pre-verified)
- **Memory cache**: 0.9 (session-cached)
- **Fresh research**: 0.85 (new AI research)
- **Fallback**: 0.7 (minimal data)

### Error Handling
- **JSON parse errors**: Use fallback profile
- **File I/O errors**: Log warning, continue
- **Research failures**: Return minimal safe profile

## Future Enhancements

Potential improvements:
1. **Confidence tracking** per field (some fields more reliable)
2. **Multi-source research** (combine multiple AI queries)
3. **Validation rules** (ensure pricing format, etc.)
4. **KB analytics** (most-compared competitors, data gaps)
5. **Research scheduling** (periodic updates for stale profiles)

## Summary

The agent-managed KB system provides:
- ✅ Automatic competitor data collection
- ✅ Zero manual maintenance
- ✅ Accurate, research-based profiles
- ✅ Eliminates "Not specified" in content
- ✅ Version-controlled knowledge base
- ✅ Efficient caching and retrieval

This is a **self-sustaining system** that improves with every page generated.
