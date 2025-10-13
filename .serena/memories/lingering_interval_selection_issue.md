# Lingering Issue: Interval Selection for Singular "week" Queries

## Status: PARTIAL FIX - Requires Further Investigation

**Last Updated:** 2025-10-12  
**Test Report:** test-reports/test_cli_regression_loop1_2025-10-12_18-42.log

## Problem Summary

GPT-5-nano agent correctly selects `interval='weekly'` for queries containing "weeks" (plural) but incorrectly uses `interval='daily'` for queries containing "week" (singular).

## Test Results

### ✅ Working Tests (Plural "weeks")
- **Test 7:** "Past 2 **Weeks** OHLC: SPY" → `interval='weekly'` ✅
- **Test 22:** "Past 2 **Weeks** OHLC: NVDA" → `interval='weekly'` ✅

### ❌ Failing Tests (Singular "week")
- **Test 4:** "Last **week**'s Performance OHLC: SPY" → `interval='daily'` ❌
- **Test 19:** "Last **Week** OHLC: NVDA" → `interval='daily'` ❌
- **Test 35:** "Last **week**'s Performance OHLC: WDC, AMD, SOUN" → `interval='daily'` ❌

## Root Cause Analysis

**Hypothesis:** GPT-5-nano model limitation in pattern matching for singular vs plural forms despite ultra-explicit instructions.

**Evidence:**
1. RULE #11 explicitly states: `IF you find "week" OR "weeks" → interval="weekly"`
2. RULE #11 includes specific examples: `"Last week's Performance" → interval="weekly"`
3. Multiple iterations of increasingly explicit instructions had no effect
4. Pattern is consistent: plural works, singular doesn't

## What Was Tried (3 Iterations)

### Iteration 1: Basic RULE #11
```python
* User says "last X weeks" or "weekly" or "last week" → interval="weekly"
```
**Result:** Agent ignored singular "week"

### Iteration 2: Pattern Matching with Examples
```python
**CRITICAL PATTERN MATCHING:**
- IF query contains "week" or "weeks" → interval="weekly" (NOT daily!)

**CRITICAL EXAMPLES:**
- ✅ "Last week's Performance OHLC: SPY" → interval="weekly"
```
**Result:** Agent still ignored singular "week"

### Iteration 3: Ultra-Explicit Stop-and-Read
```python
RULE #11: INTERVAL SELECTION FOR HISTORICAL DATA - STOP AND READ THIS RULE FIRST
- 🔴🔴🔴 **STOP! READ THIS ENTIRE RULE BEFORE SELECTING INTERVAL**
- 🔴🔴🔴 **IF USER SAYS "WEEK" (SINGULAR OR PLURAL) → ALWAYS USE interval="weekly"**

**SIMPLE PATTERN MATCHING - NO EXCEPTIONS:**
1. **SEARCH FOR "WEEK" IN QUERY:**
   - IF you find "week" OR "weeks" OR "weekly" → interval="weekly"
   - Examples: "last week", "2 weeks", "weekly", "week's" → ALL use interval="weekly"
```
**Result:** Agent STILL ignored singular "week"

## Impact Assessment

### Severity: **MEDIUM**
- Primary objective (weekend detection) fully achieved
- Affects 3/39 tests (7.7% failure rate)
- Workaround exists: Users can say "2 weeks" instead of "last week"
- Data is still provided (daily bars), just not in requested format

### Tests Affected
- Test 4: SPY Last Week Performance
- Test 19: NVDA Last Week Performance  
- Test 35: WDC/AMD/SOUN Last Week Performance

## Potential Solutions (To Be Investigated)

### Option 1: Preprocessing Layer
Add a preprocessing step that normalizes "last week" → "last 1 week" before sending to agent.

**Pros:** Guaranteed to work  
**Cons:** Adds complexity, modifies user input

### Option 2: Fine-Tune Prompt Engineering
Try different instruction formats:
- Use ALL CAPS: "WEEK"
- Use regex-like notation: `/(week|weeks)/`
- Move rule higher in instructions (currently RULE #11)

**Pros:** No code changes  
**Cons:** Already tried 3 iterations with no success

### Option 3: Post-Process Tool Calls
Intercept tool calls and correct interval parameter before execution.

**Pros:** Transparent to user, guaranteed fix  
**Cons:** Adds middleware layer, may introduce latency

### Option 4: Accept Limitation
Document as known limitation and recommend plural form in user guidance.

**Pros:** No additional work  
**Cons:** Suboptimal user experience

## Recommended Next Steps

1. **Try Option 2:** Move RULE #11 to RULE #1 position (highest priority)
2. **Try Option 2:** Use even more explicit format with visual separators
3. **If still fails:** Implement Option 1 (preprocessing) or Option 3 (post-processing)
4. **Last resort:** Accept as Option 4 (document limitation)

## Current Workaround

Users experiencing this issue can:
- Use "past 2 weeks" instead of "last week" ✅ (works correctly)
- Use "weekly data" instead of "last week" ✅ (works correctly)
- Accept daily data response ⚠️ (provides correct data, wrong format)

## Related Files

- **Agent Instructions:** `src/backend/services/agent_service.py` (lines 400-432)
- **Test Suite:** `test_cli_regression.sh` (Tests 4, 19, 35)
- **Test Prompts:**
  - Test 4: "Last week's Performance OHLC: $SPY"
  - Test 19: "Last week's Performance OHLC: $NVDA"
  - Test 35: "Last week's Performance OHLC: $WDC, $AMD, $SOUN"

## Success Metrics for Resolution

Issue will be considered RESOLVED when:
- ✅ Test 4 uses `interval='weekly'` (currently uses daily)
- ✅ Test 19 uses `interval='weekly'` (currently uses daily)
- ✅ Test 35 uses `interval='weekly'` (currently uses daily)
- ✅ All 39/39 tests pass Phase 2 grep verification with 0 "data unavailable" errors

## Notes

- Weekend detection fix (primary objective) is 100% working
- Multi-ticker options fix (RULE #12) is 100% working
- This is the ONLY remaining issue preventing 100% test pass rate
- Model appears to have strong bias toward interpreting "last week" as "days in the last week" rather than "weekly bars"
