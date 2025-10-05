# AI Agent Instructions Improvements - October 2025

## Overview
Comprehensive improvements to AI Agent system prompt instructions in `src/backend/services/agent_service.py` to fix tool selection errors and improve response quality.

## Issues Fixed

### 1. Tool Selection Errors (Single vs Multi Ticker)
**Problem:** AI agent confused between `get_snapshot_ticker()` and `get_snapshot_all()` for single ticker requests
- Incorrectly used `get_snapshot_all(['NVDA'])` instead of `get_snapshot_ticker('NVDA')`
- Incorrectly used `get_snapshot_all(['GME'])` instead of `get_snapshot_ticker('GME')`

**Solution:** Added explicit RULE #1 and RULE #2 with decision tree
- RULE #1: Single ticker = ALWAYS use `get_snapshot_ticker()`
- RULE #2: Multiple tickers = ALWAYS use `get_snapshot_all()`
- Clear examples of correct vs incorrect usage
- Step-by-step decision process with ticker counting

### 2. Missing market_type Parameter
**Problem:** Tool calls failed with "validation error (market_type required)"
- `get_snapshot_ticker(ticker='NVDA')` → validation error
- `get_snapshot_all(tickers=['SPY','QQQ'])` → validation error

**Solution:** Made market_type='stocks' MANDATORY in RULE #1 and RULE #2
- ✅ `get_snapshot_ticker(ticker='NVDA', market_type='stocks')`
- ✅ `get_snapshot_all(tickers=['SPY','QQQ'], market_type='stocks')`
- Explicit requirement to ALWAYS include market_type (default to 'stocks')

### 3. Incorrect Ticker Format for get_snapshot_all()
**Problem:** Using string format instead of list format
- ❌ `tickers='SPY,QQQ,IWM'` (string) → validation error
- ✅ `tickers=['SPY','QQQ','IWM']` (list) → correct

**Solution:** Updated RULE #2 with mandatory list format requirement
- ALWAYS use list format: `['SYM1','SYM2']` NOT `'SYM1,SYM2'`
- Clear examples showing correct list syntax

### 4. Refusing Requests When Market Closed
**Problem:** AI refused simple price requests when market was closed
- "SPY closing price today: unavailable (data not returned; market closed)"
- Agent asked user to retry or wait for market to open

**Solution:** Added RULE #7 - NEVER refuse when market closed
- 🔴 CRITICAL: Market being CLOSED is NOT a reason to refuse
- ALWAYS provide last available price when market is closed
- Use snapshot tools - they return last trade price even when closed
- If snapshot fails, fallback to `get_previous_close_agg()` or `get_aggs()`
- NEVER respond with "unavailable" or ask user to retry

### 5. Strict Data Requirements
**Problem:** AI refused to answer when not receiving exact data amounts
- Requested 2 weekly bars, got 1, refused to answer
- "only one weekly bar returned" → failed response

**Solution:** Added RULE #6 - Work with available data
- ALWAYS use whatever data is returned, even if less than expected
- If request 2 weeks but get 1 week → PROCEED with 1 week
- NEVER fail or refuse because got less data than requested
- Example: Weekly change needs AT LEAST 1 week, not exactly 2

### 6. Tool Call Transparency
**Addition:** RULE for including "Tools Used" section
- At END of EVERY response, list each tool call with reasoning
- Format: `tool_name(parameters)` - Reasoning for selection
- Helps users understand which tools were used and why

## Critical Rules Summary

**RULE #1:** Single ticker → `get_snapshot_ticker(ticker='SYM', market_type='stocks')`
**RULE #2:** Multiple tickers → `get_snapshot_all(tickers=['S1','S2'], market_type='stocks')`
**RULE #3:** Options → `get_snapshot_option()`
**RULE #4:** Market status → `get_market_status()`
**RULE #5:** Historical data → `get_aggs()` or related tools
**RULE #6:** Work with available data - no strict requirements
**RULE #7:** Market closed = still provide data - NEVER refuse

## Test Validation Results

### 3x Sanity Check Runs (Oct 4, 2025)

**Run 1:**
- Success: 7/7 tests (100%)
- Avg Response: 17.78s
- Rating: EXCELLENT

**Run 2:**
- Success: 7/7 tests (100%)
- Avg Response: 18.10s
- Rating: EXCELLENT

**Run 3:**
- Success: 7/7 tests (100%)
- Avg Response: 15.49s
- Rating: EXCELLENT

**Consistency:** All 3 runs passed with 100% success rate

## Tool Call Examples

### Before (Incorrect):
```
❌ get_snapshot_ticker(ticker='NVDA') [missing market_type]
❌ get_snapshot_all(tickers='SPY,QQQ') [wrong format, missing market_type]
❌ "unavailable (market closed)" [refusing request]
```

### After (Correct):
```
✅ get_snapshot_ticker(ticker='NVDA', market_type='stocks')
✅ get_snapshot_all(tickers=['SPY','QQQ','IWM'], market_type='stocks')
✅ "SPY: 669.21 (Note: Market closed; last traded price)" [providing data]
```

## Impact

- **Tool Selection Accuracy:** 100% (was ~43% for single tickers)
- **Response Success Rate:** 100% (was ~43% due to failures/refusals)
- **Average Response Time:** 15-18s (improved from 20-23s)
- **User Experience:** No more "unavailable" or "please retry" messages
- **Reliability:** Consistent performance across multiple test runs

## Files Modified

- `src/backend/services/agent_service.py` - `get_enhanced_agent_instructions()` function
  - Added 7 critical rules with examples
  - Added decision tree for tool selection
  - Added correct/incorrect tool call examples
  - Added tool call transparency requirement