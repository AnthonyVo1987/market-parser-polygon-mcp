# Research Task Plan - get_options_chain_both Consolidation Tool

**Feature Request**: Create new consolidated tool 'get_options_chain_both' that fetches both call and put options chains in a single tool call

**Research Completion Date**: 2025-10-25

---

## 📋 Research Summary

### Feature Requirements Analysis

**Core Requirement**: Create a single tool that consolidates two separate options chain tool calls into one comprehensive call, reducing redundant API requests and duplicate code.

**Key Requirements**:
1. **New Tool**: `get_options_chain_both()` - Returns both call and put options chains in one response
2. **Output Format**: Single response with BOTH full call and put options chains matching existing table formatting
3. **Backward Compatibility**: Keep existing `get_call_options_chain()` and `get_put_options_chain()` tools unchanged
4. **AI Agent Instructions**: Update rules to include new tool and move "ANALYZE CHAT HISTORY" to Rule #1
5. **Test Suite**: Update test_cli_regression.sh to test the new consolidated tool
6. **Manual CLI Testing**: MANDATORY GATING CHECKPOINT before Phase 4 regression testing

---

## 🔍 Current Implementation Analysis

### Existing Tools Architecture

**Call Options Chain** (src/backend/tools/tradier_tools.py):
- **Async Implementation**: `_get_call_options_chain()` (lines 599-749)
- **Wrapper**: `get_call_options_chain()` (decorated with @function_tool)
- **Functionality**:
  - Fetches all options from Tradier API
  - Filters for call options only
  - Selects 20 strikes centered around current price (10 above + 10 below)
  - Sorts DESCENDING (highest strike first)
  - Returns formatted markdown table via create_options_chain_table()

**Put Options Chain** (src/backend/tools/tradier_tools.py):
- **Async Implementation**: `_get_put_options_chain()` (lines 820-970)
- **Wrapper**: `get_put_options_chain()` (decorated with @function_tool)
- **Functionality**:
  - Identical API call and filtering pattern as call options
  - Filters for put options only
  - Selects 20 strikes centered around current price (10 above + 10 below)
  - Sorts DESCENDING (highest strike first)
  - Returns formatted markdown table via create_options_chain_table()

### Code Analysis - Shared Components

**Tradier API Call Pattern** (IDENTICAL in both functions):
```python
url = "https://api.tradier.com/v1/markets/options/chains"
headers = create_tradier_headers(api_key)
params = {
    "symbol": ticker,
    "expiration": expiration_date,
    "greeks": "true",
}

pool = get_connection_pool()
session = await pool.get_session()

async with session.get(url, headers=headers, params=params) as response:
    data = await response.json()

options_data = data.get("options", {})
option_list = options_data.get("option", [])
```

**Observation**: Both functions make THE SAME API CALL to fetch ALL options (calls + puts). The only difference is the filtering step.

**Filtering Logic** (20 strikes centered, DESCENDING sort):
```python
# Split into strikes above and below current price
strikes_above = [opt for opt in options if opt.get("strike", 0) > current_price]
strikes_below = [opt for opt in options if opt.get("strike", 0) < current_price]

# Sort and select 10 from each side
strikes_above.sort(key=lambda x: x.get("strike", 0))  # Ascending
strikes_above = strikes_above[:10]  # First 10 above

strikes_below.sort(key=lambda x: x.get("strike", 0), reverse=True)  # Descending
strikes_below = strikes_below[:10]  # First 10 below (closest to current)

# Combine and sort DESCENDING for final output
options = strikes_above + strikes_below
options.sort(key=lambda x: x.get("strike", 0), reverse=True)  # DESCENDING
```

**Formatting Helper** (src/backend/tools/formatting_helpers.py, lines 72-147):
- Function: `create_options_chain_table()`
- Parameters: ticker, option_type ("call" or "put"), expiration_date, current_price, options list
- Returns: Formatted markdown table with header, price info, and table rows
- **Reusable**: Can be called twice (once for calls, once for puts)

### Key Insight: Massive Code Duplication

**Current Pattern**:
1. Call get_call_options_chain() → Makes API call, filters calls, returns table
2. Call get_put_options_chain() → Makes SAME API call, filters puts, returns table
3. Result: **TWO API calls** for the SAME data (options list contains both calls and puts)

**Optimal Pattern**:
1. Call get_options_chain_both() → Makes ONE API call, filters BOTH calls and puts, returns BOTH tables
2. Result: **ONE API call** fetches both chains

**Code Consolidation Opportunity**:
- ~250 lines of nearly identical code (error handling, API call, validation)
- Only difference: Filter for "call" vs "put" option_type
- Can be consolidated into single function with dual filtering

---

## 🎯 Implementation Strategy

### Architecture Decision: Hybrid Approach (Option C)

**Selected Approach**: Create new unified function that makes ONE API call and processes both chains

**Rationale**:
1. **Single API Call**: Most efficient - fetches all options once
2. **Code Reuse**: Leverage existing formatting helper and filtering logic
3. **Maintainability**: Clear separation of concerns
4. **Performance**: ~50% faster than sequential calls (one API round-trip vs two)

### New Function Design

**Async Implementation**: `_get_options_chain_both()`
- Make ONE API call to Tradier (same endpoint as existing functions)
- Parse response once
- Filter for call options, apply 20-strike centered filtering
- Filter for put options, apply 20-strike centered filtering
- Format both chains using create_options_chain_table() twice
- Combine into single response with two separate tables

**Wrapper Function**: `get_options_chain_both()`
- Decorated with @function_tool for OpenAI Agents SDK
- Parameters: ticker (str), current_price (float), expiration_date (str)
- Returns: Formatted string with both tables
- Docstring: Clear description for AI agent tool selection

### Output Format Design

**Response Structure**:
```
📊 SPY Call Options Chain (Expiring 2025-10-25)
Current Price: $677.25

| Strike ($) | Bid ($) | Ask ($) | Delta | Vol     | OI     | IV  | Gamma |
|-----------|---------|---------|-------|---------|--------|-----|-------|
| 687       | ...     | ...     | ...   | ...     | ...    | ... | ...   |
... (20 rows)

Source: Tradier

📊 SPY Put Options Chain (Expiring 2025-10-25)
Current Price: $677.25

| Strike ($) | Bid ($) | Ask ($) | Delta | Vol     | OI     | IV  | Gamma |
|-----------|---------|---------|-------|---------|--------|-----|-------|
| 687       | ...     | ...     | ...   | ...     | ...    | ... | ...   |
... (20 rows)

Source: Tradier
```

**Key Features**:
- Two separate tables (one for calls, one for puts)
- Both tables use IDENTICAL strike prices (same 20 strikes)
- Both tables sorted DESCENDING (highest strike first)
- Each table matches existing format exactly
- Clear visual separation between call and put chains

---

## 📝 AI Agent Instructions Updates

### Current Structure Analysis

**File**: `.serena/memories/ai_agent_instructions_oct_2025.md`

**Current Rule Structure**:
- RULE #1: Single Ticker Selection
- RULE #2: Multiple Tickers = PARALLEL calls
- RULE #3: Options Selection
- RULE #4: Market Status & Date/Time
- RULE #5: OHLC Data with Display Requirements
- RULE #6: Work with Available Data
- RULE #7: Market Closed = Still Provide Data
- RULE #8: Technical Analysis - Check Chat History First
- RULE #9: Chat History Analysis - Avoid Redundant Calls ⭐ (CURRENT LOCATION)

**Problem**: "ANALYZE CHAT HISTORY" is buried as RULE #9, sometimes missed by agent

### Required Changes

**Change 1: Restructure Rules - Move RULE #9 to RULE #1**

**NEW Rule Structure**:
- **RULE #1**: 🔴 ANALYZE CHAT HISTORY BEFORE MAKING TOOL CALLS - AVOID REDUNDANT CALLS (MOVED FROM #9)
- **RULE #2**: Single Ticker Selection (was #1)
- **RULE #3**: Multiple Tickers = PARALLEL calls (was #2)
- **RULE #4**: Options Selection - NEW TOOL get_options_chain_both() ⭐ (was #3, UPDATED)
- **RULE #5**: Market Status & Date/Time (was #4)
- **RULE #6**: OHLC Data with Display Requirements (was #5)
- **RULE #7**: Work with Available Data (was #6)
- **RULE #8**: Market Closed = Still Provide Data (was #7)
- **RULE #9**: Technical Analysis - Check Chat History First (was #8)

**Change 2: Update RULE #4 (Options Selection)**

**OLD RULE #3**:
```
**RULE #3: Options Selection**
- Options contracts → use `get_options_quote_single()`
- Always show strike prices and expiration dates clearly
- Uses Polygon.io Direct API
```

**NEW RULE #4**:
```
**RULE #4: Options Chain Selection** ⭐ UPDATED

**For BOTH Call AND Put Options Chains (Recommended):**
- Use `get_options_chain_both(ticker, current_price, expiration_date)`
- Returns BOTH call and put options chains in ONE response
- Single API call, more efficient than separate calls
- Shows 20 strikes for each chain (10 above + 10 below current price)
- Identical strike prices for both call and put chains
- Examples: "Show me call and put options for SPY", "Get both options chains for NVDA"

**For ONLY Call Options OR ONLY Put Options (Specific):**
- Call options only → use `get_call_options_chain(ticker, current_price, expiration_date)`
- Put options only → use `get_put_options_chain(ticker, current_price, expiration_date)`
- Shows 20 strikes centered around current price (10 above + 10 below)
- Use when user explicitly requests ONLY calls or ONLY puts

**For Single Option Contracts:**
- Single option quote → use `get_options_quote_single()`
- Uses Polygon.io Direct API

**Decision Tree:**
- User asks for "both" or "call and put" → USE get_options_chain_both()
- User asks for "call options" → USE get_call_options_chain()
- User asks for "put options" → USE get_put_options_chain()
- User asks for "options chain" (ambiguous) → USE get_options_chain_both() (default to comprehensive)
```

**Change 3: Update Tool Count**

**Current**: "Total Tools: 11 (1 Finnhub + 10 Polygon Direct API)"

**NEW**: "Total Tools: 12 (1 Finnhub + 10 Polygon Direct API + 1 Tradier Consolidated)"

Wait, that's wrong. Let me recalculate:
- Finnhub: 1 tool (get_stock_quote)
- Polygon: 10 tools (as listed)
- Tradier: Currently get_call_options_chain + get_put_options_chain = 2 tools
- NEW Tradier: get_options_chain_both = 1 NEW tool (keeping old 2 for backward compat)
- **NEW Total**: 11 + 1 = 12 tools

Actually, looking back at the instructions, I see Tradier tools aren't listed in the "11 SUPPORTED TOOLS" section. Let me check what the actual 11 tools are:

From the instructions:
- Finnhub: 1 (get_stock_quote)
- Polygon: 10 (market_status, options_quote_single, 3 OHLC, 4 TA indicators)

The Tradier tools (call/put options chains) are NOT in the "11 tools" count. They must be considered separate. So adding get_options_chain_both would make it 12 total tools in practice.

Let me revise: The instructions focus on the "11 SUPPORTED TOOLS" which are Finnhub + Polygon. The Tradier options chain tools are additional. So I should add a new section for Tradier tools in the instructions.

**Change 4: Add Tradier Tools Section**

**NEW Section after Polygon Tools**:
```
**Tradier API (3 tools):** ⭐ NEW

**Options Chains:**
10. `get_options_chain_both(ticker, current_price, expiration_date)` - Both call and put options chains (RECOMMENDED)
11. `get_call_options_chain(ticker, current_price, expiration_date)` - Call options chain only
12. `get_put_options_chain(ticker, current_price, expiration_date)` - Put options chain only
```

This would make the total 14 tools (1 Finnhub + 10 Polygon + 3 Tradier).

Actually, let me re-read the instructions more carefully to understand the current tool organization...

Looking at the current instructions, I see:
- "Total Tools: 11" mentioned at line 105
- Finnhub: 1 tool listed (get_stock_quote)
- Polygon: 9 tools listed (not 10!)
  - get_market_status_and_date_time
  - get_options_quote_single
  - get_OHLC_bars_custom_date_range
  - get_OHLC_bars_specific_date
  - get_OHLC_bars_previous_close
  - get_ta_sma
  - get_ta_ema
  - get_ta_rsi
  - get_ta_macd

That's 1 + 9 = 10 tools listed. But it says "Total Tools: 11".

The Tradier options chain tools must be the missing tool(s). Looking at test_cli_regression.sh, tests 14-15 and 29-30 use "Get Call Options Chain" and "Get Put Options Chain", confirming these tools exist.

So current count is:
- 1 Finnhub
- 9 Polygon
- 2 Tradier (call + put chains) = **12 tools total** (not 11 as stated)

There's a discrepancy in the documentation. The instructions say 11 but there are actually 12 tools. I'll need to correct this and add the new consolidated tool, making it 13 total.

**Corrected Tool Count**:
- **Current**: 12 tools (1 Finnhub + 9 Polygon + 2 Tradier) - documentation incorrectly says 11
- **NEW**: 13 tools (1 Finnhub + 9 Polygon + 3 Tradier)

---

## 🧪 Testing Strategy

### Phase 3: Manual CLI Testing (MANDATORY GATING CHECKPOINT)

**Purpose**: Validate new tool before running full regression suite

**Test Prompts** (execute via `uv run main.py`):
1. "Get both Call and Put Options Chains Expiring this Friday: $SPY"
2. "Show me call and put options for $AAPL expiring this Friday"
3. "I need the full options chain for $NVDA this Friday"
4. "Get call and put options chains for $AMD expiring this Friday"

**Validation Criteria** (for EACH test):
1. ✅ Agent calls get_options_chain_both() (NOT separate call/put chain tools)
2. ✅ Both call and put options chains displayed in response
3. ✅ Each chain shows exactly 20 strikes
4. ✅ Strikes centered around current price (10 above, 10 below)
5. ✅ Call and put chains have IDENTICAL strike prices
6. ✅ Both chains sorted DESCENDING (highest strike first)
7. ✅ Proper table formatting with all columns (Strike, Bid, Ask, Delta, Vol, OI, IV, Gamma)
8. ✅ No errors or "data unavailable" messages
9. ✅ Response includes TWO separate tables (one for calls, one for puts)

**Success Criteria**:
- All 4 manual tests MUST pass all 9 validation criteria
- If ANY test fails, fix issues and re-run ALL manual tests
- Only proceed to Phase 4 regression testing after 100% manual test pass rate

### Phase 4: CLI Regression Suite Updates

**Test Suite File**: `test_cli_regression.sh`

**Current Options Chain Tests**:
- Test 14: "Get Call Options Chain Expiring this Friday: $SPY"
- Test 15: "Get Put Options Chain Expiring this Friday: $SPY"
- Test 29: "Get Call Options Chain Expiring this Friday: $NVDA"
- Test 30: "Get Put Options Chain Expiring this Friday: $NVDA"

**Proposed NEW Tests** (add to test suite):
- **NEW Test 16**: "Get both Call and Put Options Chains Expiring this Friday: $SPY"
- **NEW Test 31**: "Get both Call and Put Options Chains Expiring this Friday: $NVDA"

**Test Suite Changes**:
- Current: 39 tests
- NEW: 41 tests (39 + 2 new consolidated options chain tests)
- Renumber tests 16-39 to 17-41 to accommodate new test at position 16
- Keep existing tests 14-15 and 29-30 unchanged (backward compatibility)

**Test Array Structure** (after line 95):
```bash
# SPY Test Sequence (Tests 1-17) - UPDATED with NEW Test 16
...
"Get Call Options Chain Expiring this Friday: \$SPY"        # Test 14
"Get Put Options Chain Expiring this Friday: \$SPY"         # Test 15
"Get both Call and Put Options Chains Expiring this Friday: \$SPY"  # NEW Test 16
"Analyze the Options Chain WITH NO TOOL CALLS..."           # Test 17 (was 16)
# NVDA Test Sequence (Tests 18-32) - UPDATED with NEW Test 31
...
"Get Call Options Chain Expiring this Friday: \$NVDA"       # Test 29
"Get Put Options Chain Expiring this Friday: \$NVDA"        # Test 30
"Get both Call and Put Options Chains Expiring this Friday: \$NVDA"  # NEW Test 31
"Analyze the Options Chain WITH NO TOOL CALLS..."           # Test 32 (was 31)
# Multi-Ticker Test Sequence (Tests 33-41) - renumbered from 32-39
...
```

### Phase 4: Regression Testing Validation

**Command**: `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`

**Phase 1 (Automated)**:
- Execute all 41 tests in persistent session (was 39)
- Generate test report in test-reports/
- Show completion count (41/41 COMPLETED)

**Phase 2 (Manual Verification)**:
- Use Read tool to manually read EACH of 41 test responses (was 39)
- Apply 4-point verification criteria to EACH test:
  1. ✅ Does the response address the query?
  2. ✅ Were the RIGHT tools called (not duplicate/unnecessary calls)?
  3. ✅ Is the data correct (no cross-ticker contamination)?
  4. ✅ Are there any errors?

**Focus Areas for NEW Tests** (16, 31):
- Verify get_options_chain_both() called (NOT separate call/put tools)
- Verify BOTH call and put chains displayed
- Verify 20 strikes each, identical strikes, DESCENDING sort
- Verify proper table formatting with all columns
- Verify no duplicate tool calls

**Success Criteria**:
- 41/41 tests COMPLETED in Phase 1
- 41/41 tests PASSED all 4 criteria in Phase 2
- New tests 16 and 31 specifically validate consolidated tool behavior
- Existing tests 14, 15, 29, 30 still pass (backward compatibility)

---

## 📊 Risk Assessment

### Low Risk Areas
- ✅ **API Integration**: Same Tradier API endpoint as existing tools, no changes
- ✅ **Error Handling**: Can reuse existing error handling patterns
- ✅ **Data Formatting**: Reusing create_options_chain_table() helper, no changes
- ✅ **Async Pattern**: Following established async/await pattern with APIConnectionPool
- ✅ **Backward Compatibility**: Existing tools remain unchanged, fully functional

### Medium Risk Areas
- ⚠️ **Code Consolidation**: New function combines logic from two existing functions
- ⚠️ **AI Agent Behavior**: Agent must learn to prefer new consolidated tool
- ⚠️ **Test Suite Changes**: Adding 2 new tests, renumbering 7 existing tests
- ⚠️ **Instructions Restructuring**: Moving RULE #9 to RULE #1 may affect agent behavior

### Mitigation Strategies
1. **Thorough Manual CLI Testing**: 4 manual tests MUST pass before regression suite
2. **Comprehensive Test Coverage**: 2 new tests + 4 existing tests = 6 total options chain tests
3. **Backward Compatibility**: Keep existing tools unchanged, agent can still use them
4. **Clear Documentation**: Update instructions with clear decision tree for tool selection
5. **Small, Focused Changes**: Each change is isolated and testable

---

## 📝 Documentation Requirements

### Code Documentation
- ✅ Docstring for `_get_options_chain_both()` async implementation
- ✅ Docstring for `get_options_chain_both()` @function_tool wrapper
- ✅ Inline comments explaining dual filtering logic
- ✅ Function signature documentation

### Project Documentation
- ✅ **CLAUDE.md**: Update "Last Completed Task Summary" section
- ✅ **ai_agent_instructions_oct_2025.md**: Restructure rules, add new tool, update tool count
- ✅ **.serena/memories/options_chain_both_tool_completion_oct_2025.md**: Create comprehensive memory (NEW)
- ✅ **research_task_plan.md**: This file (NEW)
- ✅ **TODO_task_plan.md**: Detailed implementation plan (NEW, to be created in Phase 2)

### Test Evidence
- ✅ Manual CLI test results (4 tests, all criteria met)
- ✅ CLI regression test report (Phase 1 + Phase 2 results)
- ✅ Test report file path in CLAUDE.md
- ✅ Performance metrics (response times, test pass rates)

---

## 🚀 Implementation Readiness

**Research Status**: ✅ COMPLETE

**Ready for Phase 2 (Planning)**: ✅ YES

**Key Findings**:
1. ✅ Clear understanding of current implementation (both call and put functions analyzed)
2. ✅ Identified massive code duplication (~250 lines of nearly identical code)
3. ✅ Optimal architecture designed (hybrid approach with single API call)
4. ✅ Output format defined (two separate tables in one response)
5. ✅ AI Agent Instructions structure analyzed (RULE #9 needs to become RULE #1)
6. ✅ Test suite structure understood (need to add 2 tests, renumber 7 tests)
7. ✅ Manual testing strategy defined (4 tests with 9 validation criteria each)
8. ✅ Risk assessment complete (mostly low risk, some medium risk areas)
9. ✅ Documentation requirements identified

**Code Consolidation Benefits**:
- 🚀 **50% Fewer API Calls**: One API call instead of two for full options chain
- 🧹 **Cleaner Code**: Eliminate ~250 lines of duplicate code
- ⚡ **Faster Responses**: Single API round-trip vs two sequential calls
- 🎯 **Better Agent Behavior**: Prefer consolidated tool, reduce redundant calls
- 📊 **Improved UX**: Users get complete options picture in one response

**Next Phase**: Delete existing TODO_task_plan.md and create comprehensive implementation plan

---

## 📚 References

**Code Files Analyzed**:
- src/backend/tools/tradier_tools.py (lines 599-970) - call and put options chain functions
- src/backend/tools/formatting_helpers.py (lines 72-147) - table formatting helper
- .serena/memories/ai_agent_instructions_oct_2025.md - AI agent rules and tool descriptions
- test_cli_regression.sh - 39-test suite structure

**Serena Tools Used**:
- find_symbol (with include_body=True) - Analyzed function implementations
- search_for_pattern - Located AI agent instructions file
- find_file - Located instruction and agent-related files

**Sequential-Thinking Analysis**:
- 10 thought steps for systematic research planning
- Analyzed requirements, implementation options, output format, testing strategy
- Identified optimal architecture (hybrid approach with single API call)

**Research Time**: ~25 minutes (optimal for comprehensive analysis)

---

## 🎯 Phase 2 Preview - Implementation Plan Outline

**Next Steps** (to be detailed in TODO_task_plan.md):

**Phase 2: Planning**
- Task 2.1: Use Sequential-Thinking to plan implementation approach
- Task 2.2: Create detailed TODO_task_plan.md with all implementation tasks
- Task 2.3: Define success criteria for each task
- Task 2.4: Plan testing and validation workflow

**Phase 3: Implementation**
- Task 3.1: Create `_get_options_chain_both()` async function
- Task 3.2: Create `get_options_chain_both()` @function_tool wrapper
- Task 3.3: Update AI agent instructions (restructure rules, add new tool)
- Task 3.4: Update test_cli_regression.sh (add 2 tests, renumber 7 tests)
- Task 3.5: Update agent tool registration in agent_service.py
- Task 3.6: **MANDATORY**: Manual CLI testing (4 tests, GATING CHECKPOINT)

**Phase 4: Testing**
- Task 4.1: Run full CLI regression suite (41 tests)
- Task 4.2: Phase 2 manual verification (all 41 test responses)
- Task 4.3: Document test results

**Phase 5: Documentation & Commit**
- Task 5.1: Update CLAUDE.md
- Task 5.2: Create Serena memory file
- Task 5.3: Update all documentation
- Task 5.4: Atomic git commit

---

## ⚠️ Critical Reminders

**🔴 GATING CHECKPOINT**: Phase 3 Manual CLI Testing is MANDATORY before Phase 4
- 4 manual tests MUST pass ALL 9 validation criteria
- Fix issues and re-test until 100% pass rate achieved
- Phase 4 regression suite CANNOT proceed without manual test success

**🔴 PROPER TOOL USAGE**: MUST use Sequential-Thinking and Serena tools throughout implementation
- Sequential-Thinking: Use for planning, complex reasoning, decision-making
- Serena find_symbol: Use for code analysis and targeted reads
- Serena replace_symbol_body: Use for function body replacements
- Serena insert_after_symbol: Use for adding new functions
- Standard Read/Write/Edit: Use for documentation updates only when Serena doesn't support the operation

**🔴 ATOMIC COMMIT WORKFLOW**: Stage ALL changes at once immediately before committing
- DO NOT stage files early during development
- Complete ALL work first (code, tests, docs, configs)
- Run `git add -A` ONCE at the end
- Verify staging with `git status`
- Commit within 60 seconds
- Push immediately

---

**Research Phase Complete** ✅
**Ready for Phase 2: Planning** ✅
