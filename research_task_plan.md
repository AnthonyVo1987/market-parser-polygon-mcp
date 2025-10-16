# Research Task Plan: Weekly/Monthly Interval Fix + Error Transparency

**Date**: 2025-10-15
**Status**: Research Complete - Ready for Planning Phase

---

## 🎯 Research Objectives

1. Investigate and fix the lingering interval selection issues for weekly/monthly intervals
2. Update AI agent instructions to enforce verbatim error message reporting
3. Validate fixes with manual CLI prompts and full test suite

---

## 🔍 Phase 1: Root Cause Analysis

### **Problem Statement**

Weekly and monthly `get_stock_price_history()` calls failing with error:
```
"Failed to retrieve historical data for SPY: 'str' object has no attribute 'get'"
```

This error occurred despite the agent correctly selecting `interval="weekly"` and `interval="monthly"`.

### **Initial Hypothesis (INCORRECT)**

Initially believed this was a model issue - GPT-5-nano not following RULE #11 for interval selection.

### **Actual Root Cause (CONFIRMED)**

**This is NOT a model issue - it's a CODE BUG in `tradier_tools.py`**

### **Evidence from Tradier API Responses**

User provided actual Tradier API responses showing the structural difference:

**Weekly Interval Response:**
```json
{
  "history": {
    "day": {
      "date": "2025-10-13",
      "open": 660.65,
      "high": 670.23,
      "low": 653.17,
      "close": 665.17,
      "volume": 250042630
    }
  }
}
```

**Monthly Interval Response:**
```json
{
  "history": {
    "day": {
      "date": "2025-10-01",
      "open": 663.17,
      "high": 673.95,
      "low": 652.84,
      "close": 665.17,
      "volume": 863248440
    }
  }
}
```

**Daily Interval Response (for comparison):**
```json
{
  "history": {
    "day": [
      {"date": "2025-10-13", "open": 660.65, ...},
      {"date": "2025-10-14", "open": 662.45, ...}
    ]
  }
}
```

### **Key Discovery**

Tradier API returns **DIFFERENT data structures** based on interval:
- **Daily**: `"day"` is an **ARRAY of dicts** `[{...}, {...}]`
- **Weekly/Monthly**: `"day"` is a **SINGLE dict** `{...}`

---

## 🐛 Bug Analysis

### **Current Code (tradier_tools.py lines 358-380)**

```python
# Line 358: Parse response
data = response.json()
history_data = data.get("history", {})
bars_data = history_data.get("day", [])  # ← Bug starts here

# Line 362: Check if API returned data
if not bars_data:
    return json.dumps({"error": "No data", ...})

# Line 377-380: Format response with bars
formatted_bars = []
for bar in bars_data:  # ← Bug manifests here
    formatted_bars.append(_format_tradier_history_bar(bar))
```

### **Bug Execution Flow (Weekly/Monthly)**

1. **Line 360**: `bars_data = history_data.get("day", [])` returns a **dict** (not a list)
2. **Line 362**: `if not bars_data:` → dict is truthy, so continues
3. **Line 379**: `for bar in bars_data:` → iterates over **dict KEYS** (strings: "date", "open", "high", etc.)
4. **Line 380**: `_format_tradier_history_bar(bar)` → passes string "date" instead of dict
5. **_format_tradier_history_bar() line 407**: `bar.get("date", "")` → tries to call `.get()` on string
6. **Result**: `'str' object has no attribute 'get'` ❌

### **Why This Bug Was Hidden**

- Previous testing primarily used `interval="daily"` which returns array correctly
- Weekly/monthly intervals added later but not thoroughly tested
- Error message was generic, masking the actual cause

---

## ✅ Solution Design

### **Fix #1: tradier_tools.py (lines 360-362)**

**Current Code:**
```python
bars_data = history_data.get("day", [])
```

**Fixed Code:**
```python
bars_data = history_data.get("day", [])
# Handle weekly/monthly: single dict vs daily: array of dicts
if isinstance(bars_data, dict):
    bars_data = [bars_data]
```

**Explanation:**
- Check if `bars_data` is a dict (weekly/monthly case)
- Wrap single dict in a list to normalize data structure
- Rest of code continues to work unchanged (expects list of dicts)

### **Fix #2: agent_service.py (after line 461)**

Add **RULE #13: ERROR TRANSPARENCY** immediately after RULE #12:

```python
RULE #13: ERROR TRANSPARENCY - VERBATIM ERROR REPORTING
- 🔴 **CRITICAL**: When tool calls fail, you MUST report the EXACT verbatim error message received
- 🔴 **NEVER** use vague phrases like "API Issue", "data unavailable", or "failed to retrieve" without specifics
- 🔴 **ALWAYS** include the complete error message in your response for debugging purposes
- ✅ **CORRECT**: "API Error: Failed to retrieve historical data for SPY: 'str' object has no attribute 'get'"
- ❌ **WRONG**: "There was an API issue" or "Data unavailable"
- ✅ **FORMAT**: When reporting errors, use exact error JSON or message returned by the tool
- ✅ **TRANSPARENCY**: Users need exact error messages to diagnose and fix problems quickly
```

**Placement:** Insert after line 461 (after RULE #12 ends), before emoji formatting section.

---

## 🧪 Validation Strategy

### **Phase 1: Manual CLI Testing (6 Prompts)**

Test weekly/monthly intervals with single and multi-ticker scenarios:

1. `"Last week's Performance OHLC: $SPY"`
2. `"Stock Price Performance the past month: $SPY"`
3. `"Last week's Performance OHLC: $NVDA"`
4. `"Stock Price Performance the past month: $NVDA"`
5. `"Last week's Performance OHLC: $WDC, $AMD, $SOUN"`
6. `"Stock Price Performance the past month: $WDC, $AMD, $SOUN"`

**Expected Results:**
- ✅ All 6 prompts should return OHLC data successfully
- ✅ Agent should use `interval="weekly"` for "week" queries
- ✅ Agent should use `interval="monthly"` for "month" queries
- ✅ Multi-ticker queries should make parallel calls (RULE #12)
- ✅ No "'str' object has no attribute 'get'" errors

### **Phase 2: Full Regression Testing (39 Tests)**

Execute full test suite:
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Phase 2a: ERROR DETECTION (Grep Commands)**
```bash
# Command 1: Find all errors/failures
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log

# Command 2: Count 'data unavailable' errors
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log

# Command 3: Count completed tests
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Expected Results:**
- ✅ **39/39 COMPLETED** (100% generation rate)
- ✅ **0 "'str' object" errors** (bug fixed)
- ✅ **0 weekend-related errors** (already fixed in previous task)
- ✅ **Tests 4, 19, 35** should now use weekly interval correctly
- ✅ **Average response time < 10s** (EXCELLENT rating)

---

## 📊 Impact Analysis

### **Tests Affected**

Based on previous test results, the following tests were failing due to this bug:

| Test # | Query Pattern | Interval | Status Before Fix |
|--------|---------------|----------|-------------------|
| 4 | "Last week's" | weekly | ❌ "'str' object" error |
| 19 | "Last Week" | weekly | ❌ "'str' object" error |
| 35 | "Last week's" | weekly | ❌ "'str' object" error |
| All monthly tests | "past month" | monthly | ❌ "'str' object" error |

### **Expected Improvement**

- **Before Fix**: 11 errors (weekend + str errors)
- **After Weekend Fix**: 2 errors (str errors remain)
- **After This Fix**: 0 errors (all issues resolved)
- **Success Rate**: 36/39 → **39/39 PASS** (100%)

---

## 🔑 Key Insights

1. **API Structure Differences**: Always verify API response structure for ALL supported parameters
2. **Type Safety**: Add isinstance() checks when API can return multiple types
3. **Error Transparency**: Vague error messages delay debugging - always report exact errors
4. **Test Coverage**: Test all parameter combinations, not just common cases
5. **Code vs Model**: Don't assume model is wrong - verify code handles all cases correctly

---

## 📝 Research Findings Summary

✅ **Root cause identified**: Tradier API returns dict for weekly/monthly, array for daily
✅ **Bug location pinpointed**: tradier_tools.py line 360 (missing type check)
✅ **Solution designed**: 2-line fix with isinstance() check
✅ **Secondary issue addressed**: Error reporting transparency (RULE #13)
✅ **Validation plan created**: 6 manual tests + 39-test suite with grep verification
✅ **Impact quantified**: Fixes 3+ failing tests, achieves 100% pass rate

---

## 🚀 Next Steps

1. **Phase 2: Planning** - Create TODO_task_plan.md with granular implementation steps
2. **Phase 3: Implementation** - Apply fixes to tradier_tools.py and agent_service.py
3. **Phase 4: Testing** - Execute validation strategy (manual + regression)
4. **Phase 5: Documentation** - Update CLAUDE.md, memories, and create atomic commit

---

## 📚 Research Tools Used

- ✅ Sequential-Thinking (10 thoughts) - Systematic root cause analysis
- ✅ Serena find_file - Located tradier_tools.py
- ✅ Serena get_symbols_overview - Explored tradier_tools.py structure
- ✅ Serena find_symbol - Read get_stock_price_history() implementation
- ✅ Serena search_for_pattern - Located RULE #12 in agent_service.py
- ✅ User-provided API responses - Confirmed exact Tradier API structure

**Research Phase Complete** ✅
