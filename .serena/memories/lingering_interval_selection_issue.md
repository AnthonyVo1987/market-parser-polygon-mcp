# Lingering Interval Selection Issue - RESOLVED ✅

**Status**: RESOLVED (2025-10-15)

## Original Problem
Tests 4, 19, 35 were failing - agent responding with daily interval instead of weekly when user said "last week" (singular).

## Root Cause (Previous Investigation)
Initially thought to be a model bias issue with GPT-5-nano not following RULE #11 for singular "week".

## ACTUAL ROOT CAUSE (RESOLVED)
**Was NOT a model issue - was a CODE BUG in tradier_tools.py!**

The true issue: Tradier API returns DIFFERENT structures for different intervals:
- Daily: `{"history": {"day": [array of dicts]}}`
- Weekly/Monthly: `{"history": {"day": {single dict}}}`

Code at line 360 in tradier_tools.py assumed `bars_data` was always an array:
```python
bars_data = history_data.get("day", [])
for bar in bars_data:  # ← When dict, iterates over KEYS (strings)
    formatted_bars.append(_format_tradier_history_bar(bar))  # ← Tries string.get()
```

Result: `'str' object has no attribute 'get'` error when processing weekly/monthly.

## The Fix (Committed 2025-10-15)
Added isinstance() check at tradier_tools.py lines 343-345:
```python
bars_data = history_data.get("day", [])
# Handle weekly/monthly: single dict vs daily: array of dicts
if isinstance(bars_data, dict):
    bars_data = [bars_data]
```

## Verification
- ✅ Tests 4, 19, 35: NOW WORKING with weekly interval
- ✅ All 39 tests: PASS (100% pass rate)
- ✅ Phase 2 grep verification: 0 "'str' object" errors
- ✅ 6 manual CLI prompts: 6/6 PASS

## Key Lessons
1. Always verify API response structure for ALL supported parameters
2. Type safety: Add isinstance() checks when API can return multiple types
3. Don't assume the model is wrong - verify code handles all cases correctly
4. Generic error messages mask the real issue - debug with exact error text

## Memory Impact
This was misdiagnosed as a model issue in the previous task. It was actually a tool-level bug that was invisible until we got the exact error message and traced back to the Tradier API response format.

**Status**: ✅ RESOLVED with code fix (isinstance check)
**Commit**: e6cdda2 ([INTERVAL-FIX] Weekly/Monthly Interval Bug Fix + Error Transparency Rule)
