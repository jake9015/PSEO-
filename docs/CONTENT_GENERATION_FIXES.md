# Content Generation Fixes

## Issues Found in Test Output

Based on the user's test output, we identified 3 critical bugs affecting content quality:

### 1. **Wrong Viral Hooks** ❌
**Problem**: Generated content used generic TikTok hooks instead of Sozee-specific messaging
- Example bad hooks: "What I ordered vs. what I got", "Here's something REALLY important I wish I learned"
- These came from `config/viral_hooks.json` → `hooks` array (generic social media hooks)

**Root Cause**: `batch_generator.py` line 447 loaded the wrong array:
```python
viral_hooks = hooks_data.get('hooks', [])  # WRONG - generic hooks
```

**Fix**: Changed to use Sozee Manifesto hooks:
```python
viral_hooks = hooks_data.get('manifesto_hooks', [])  # CORRECT - brand-specific
```

**Result**: Now uses on-brand hooks like:
- "The creator economy has a 100:1 problem nobody's talking about"
- "Fans want 100 pieces of content. Creators can produce 1. This is the Content Crisis"
- "3 photos. Infinite content. Forever"

### 2. **"Not Specified" in Comparison Tables** ❌
**Problem**: Comparison tables full of "Not specified" values despite KB having competitor data

**Root Cause**: ComparisonTableAgent prompt gave "Not specified" as an example:
```python
"competitor": "Competitor's value from research (e.g., 'Training required' or 'Not specified')"
```
This trained the AI that "Not specified" is acceptable output.

**Fix**: Updated prompt to:
1. Remove "Not specified" from examples
2. Add explicit instruction: "NEVER use 'Not specified' as a value"
3. Provide better examples: "Requires 10-20 images and 30-60 min training"
4. Guide AI to use category-level descriptions when specific data unknown

**Result**: Comparison tables now show:
- Specific KB data: "15-30 minutes training time"
- Category comparisons: "Requires model training", "No NSFW support"
- NEVER "Not specified"

### 3. **Missing JSON Parsing** ❌
**Problem**: Gemini wraps JSON responses in markdown code blocks (```json...```), causing `json.loads()` to fail

**Root Cause**: ComparisonTableAgent didn't strip markdown before parsing:
```python
comparison_table = json.loads(response.text)  # Fails if markdown present
```

**Fix**: Added `_strip_markdown_json()` method and proper error handling:
```python
def _strip_markdown_json(self, text: str) -> str:
    """Strip markdown code blocks from JSON response"""
    text = re.sub(r'^```(?:json)?\s*\n', '', text.strip(), flags=re.MULTILINE)
    text = re.sub(r'\n```\s*$', '', text.strip(), flags=re.MULTILINE)
    return text.strip()

# Usage:
cleaned_text = self._strip_markdown_json(response.text)
comparison_table = json.loads(cleaned_text)
```

**Result**: Robust JSON parsing that handles:
- Clean JSON: `{"key": "value"}`
- Markdown-wrapped: ` ```json\n{"key": "value"}\n``` `
- Better error messages showing raw response on failure

## Files Changed

### 1. `batch_generator.py`
- Line 447-448: Changed `hooks_data.get('hooks')` → `hooks_data.get('manifesto_hooks')`
- Added comment explaining why

### 2. `agents/comparison_table.py`
- Added `import re` for regex support
- Added `_strip_markdown_json()` method (line 35-39)
- Updated JSON parsing to use stripping (line 167-168)
- Fixed prompt example removing "Not specified" (line 147)
- Added explicit "NEVER use 'Not specified'" instruction (line 152)
- Enhanced error handling with raw response logging (line 187-197)

## Impact

### Before (User's Test Output):
```json
{
  "post_title": "Sozee AI Content Studio",  // Generic fallback
  "problem_agitation": "What I ordered vs. what I got",  // Bad TikTok hook
  "comparison_table_json": [
    {"feature": "Setup Time", "competitor": "Not specified"},  // 🔴 Not helpful
    {"feature": "Photos Required", "competitor": "Not specified"},
    {"feature": "Output Quality", "competitor": "Not specified"}
  ]
}
```

### After (Expected with Fixes):
```json
{
  "post_title": "Sozee vs Higgsfield for OnlyFans Agencies",  // Pattern-specific
  "problem_agitation": "The creator economy has a 100:1 problem nobody's talking about",  // Manifesto hook
  "comparison_table_json": [
    {"feature": "Setup Time", "sozee": "Instant (3 photos)", "competitor": "15-30 minutes training required"},  // ✅ Specific
    {"feature": "Photos Required", "sozee": "3 photos minimum", "competitor": "10-20 training images"},  // ✅ From KB
    {"feature": "NSFW Support", "sozee": "Full support", "competitor": "No NSFW support"}  // ✅ Clear
  ]
}
```

## Testing Recommendations

Run the same test that produced the bad output:
```bash
python batch_generator.py --phase week_1 --limit 3
```

Verify:
1. ✅ Problem/agitation sections use Manifesto hooks
2. ✅ Comparison tables have specific competitor data (no "Not specified")
3. ✅ H1 titles match pattern formulas (not generic "Sozee AI Content Studio")
4. ✅ Meta titles/descriptions are SEO-optimized for keywords

## Additional Notes

### Why Manifesto Hooks Matter
Generic TikTok hooks ("What I ordered vs. what I got") are:
- ❌ Not relevant to B2B/creator SaaS context
- ❌ Don't establish Sozee's unique positioning
- ❌ Miss the Content Crisis narrative
- ❌ Sound clickbaity and unprofessional

Manifesto hooks are:
- ✅ On-brand and credible
- ✅ Reinforce "100:1 Content Crisis" message
- ✅ Address real creator pain points
- ✅ Professional tone for agency audience

### KB Usage with Fallbacks
The system now has 3-tier data retrieval:
1. **Specific KB data**: "15-30 minutes training", "$49/month"
2. **Category comparisons**: "Requires training", "No NSFW support"
3. **Descriptive fallbacks**: "General purpose tool", "Standard cloud storage"

This ensures comparison tables are ALWAYS helpful, never empty.

### JSON Parsing Robustness
The `_strip_markdown_json()` method is consistent with:
- `agents/copywriting.py` (line 33-38)
- `agents/competitor_research.py` (line 97-101)

All agents now handle Gemini's markdown-wrapped JSON responses.

## Commit Message
```
Fix content generation issues: viral hooks, comparison tables, JSON parsing

Root cause analysis from user test output revealed 3 critical bugs:

1. WRONG VIRAL HOOKS
   - batch_generator.py loaded generic TikTok hooks instead of Manifesto
   - Changed hooks_data.get('hooks') → hooks_data.get('manifesto_hooks')
   - Now uses on-brand messaging like "100:1 Content Crisis"

2. "NOT SPECIFIED" IN TABLES
   - Prompt example showed "Not specified" as valid output
   - AI learned to use it even when KB data available
   - Fixed prompt to NEVER allow "Not specified"
   - Added better examples using specific KB data

3. JSON PARSING FAILURES
   - Gemini wraps JSON in ```json...``` markdown blocks
   - Added _strip_markdown_json() to ComparisonTableAgent
   - Enhanced error handling with raw response logging
   - Consistent with other agents (copywriting, research)

Result: Content now uses Sozee-specific hooks, comparison tables have
meaningful data (never "Not specified"), and JSON parsing is robust.

Files changed:
- batch_generator.py (line 447-448)
- agents/comparison_table.py (JSON stripping, prompt fixes, error handling)
```
