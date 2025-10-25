# Research Task Plan - Options Chain Enhancement

**Feature Request**: Expand Call and Put Options Chains from 10 to 20 strike prices each, centered around current price

**Research Completion Date**: 2025-10-25

---

## 📋 Research Summary

### Current Implementation Analysis

**Analyzed Functions** (via Serena find_symbol with include_body=True):
- `get_call_options_chain()` - @function_tool wrapper (lines 742-806)
- `_get_call_options_chain()` - Async implementation (lines 599-739)
- `get_put_options_chain()` - @function_tool wrapper (lines 951-1015)
- `_get_put_options_chain()` - Async implementation (lines 809-948)

**Current Behavior**:

1. **Call Options Chain**:
   - Filters: `strike >= current_price` (line 675)
   - Sorts: Ascending (line 681)
   - Returns: First 10 strikes ABOVE current price
   - Docstring: "10 strike prices above current underlying price"

2. **Put Options Chain**:
   - Filters: `strike <= current_price` (line 884)
   - Sorts: Descending (line 890)
   - Returns: First 10 strikes BELOW current price
   - Docstring: "10 strike prices below current underlying price"

**Key Technical Details**:
- Both use async aiohttp via APIConnectionPool (Phase 2.1 implementation)
- Tradier API endpoint: `https://api.tradier.com/v1/markets/options/chains`
- API returns ALL strikes (no server-side filtering)
- Client-side filtering applied after API response
- Output formatting via `create_options_chain_table()` helper
- Error handling already robust with proper validation

---

## 🎯 Required Changes

### New Behavior Specification

**Both Call and Put Options Chains must now show**:
- **20 strikes total** per chain (up from 10)
- **10 strikes ABOVE current price**
- **10 strikes BELOW current price**
- **Identical strike prices** for both calls and puts
- **DESCENDING sort order** (highest strike at top)

### Algorithm Design

**New Filtering Logic** (applies to BOTH call and put chains):

```python
# 1. Get all options from API (already done)
all_options = [opt for opt in option_list if opt.get("option_type") == "call"]  # or "put"

# 2. Split by relationship to current price
strikes_above = [opt for opt in all_options if opt.get("strike", 0) > current_price]
strikes_below = [opt for opt in all_options if opt.get("strike", 0) < current_price]

# 3. Sort and select 10 from each side
strikes_above.sort(key=lambda x: x.get("strike", 0))  # Ascending
strikes_above = strikes_above[:10]  # First 10 above

strikes_below.sort(key=lambda x: x.get("strike", 0), reverse=True)  # Descending
strikes_below = strikes_below[:10]  # First 10 below (closest to current)

# 4. Combine and sort DESCENDING for final output
selected_options = strikes_above + strikes_below
selected_options.sort(key=lambda x: x.get("strike", 0), reverse=True)  # DESCENDING
```

---

## 📊 Test Coverage Analysis

**Regression Test Suite Coverage** (test_cli_regression.sh):
- **Test 14**: `"Get Call Options Chain Expiring this Friday: $SPY"` (line 94)
- **Test 15**: `"Get Put Options Chain Expiring this Friday: $SPY"` (line 95)
- **Test 28**: `"Get Call Options Chain Expiring this Friday: $NVDA"` (line 110)
- **Test 29**: `"Get Put Options Chain Expiring this Friday: $NVDA"` (line 111)

**Total**: 4 out of 39 tests (10.3%) directly test options chains

**Validation Requirements**:
1. ✅ Manual CLI testing FIRST (user requirement)
2. ✅ Then Phase 4 regression suite (all 39 tests)
3. ✅ Phase 2 manual verification of all 39 test responses

---

## 🔍 Code Locations

### Files to Modify

**1. src/backend/tools/tradier_tools.py**

**Call Options Function**:
- Lines 675-682: Current filtering logic → Replace with new algorithm
- Lines 742-806: Docstring → Update to "20 strike prices (10 above, 10 below current price)"
- Line 744: Function signature comment → Update count

**Put Options Function**:
- Lines 884-891: Current filtering logic → Replace with new algorithm
- Lines 951-1015: Docstring → Update to "20 strike prices (10 above, 10 below current price)"
- Line 953: Function signature comment → Update count

**No Changes Needed**:
- Error handling (already robust)
- API request logic (already fetches all strikes)
- Data formatting logic (already flexible)
- Output table generation (auto-adapts to 20 strikes)

---

## 🧪 Testing Strategy

### Phase 1: Manual CLI Testing (MANDATORY GATING)

**Purpose**: Validate new behavior before regression suite
**Requirement**: User-specified, must pass before Phase 4

**Test Prompts** (execute via `uv run main.py`):
```
> Get Call Options Chain Expiring this Friday: $SPY
> Get Put Options Chain Expiring this Friday: $SPY
> Get Call Options Chain Expiring this Friday: $AAPL
> Get Put Options Chain Expiring this Friday: $AAPL
```

**Validation Criteria** (for EACH test):
1. ✅ Both chains show exactly 20 strikes each
2. ✅ Strikes centered around current price (10 above, 10 below)
3. ✅ Call and Put chains have IDENTICAL strike prices
4. ✅ Sorting is DESCENDING (highest strike at top)
5. ✅ Table formatting is correct (columns aligned)
6. ✅ No errors or data unavailable messages

**Action if Failures**: Fix issues and re-run manual tests until all pass

### Phase 2: CLI Regression Suite

**Command**: `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`

**Phase 1 (Automated)**:
- Execute all 39 tests in persistent session
- Generate test report in test-reports/
- Show completion count (39/39 COMPLETED)

**Phase 2 (Manual Verification)**:
- Use Read tool to manually read EACH of 39 test responses
- Apply 4-point verification criteria to EACH test
- Document results in table format (PASS/FAIL with reasons)
- Answer 5 checkpoint questions with evidence

**Focus on Options Tests** (14, 15, 28, 29):
- Verify 20 strikes shown (not 10)
- Verify strikes centered around current price
- Verify DESCENDING sort order
- Verify no duplicate tool calls

---

## 📝 Documentation Updates Required

### Code Documentation
- ✅ Update docstrings in both wrapper functions (lines 742-806, 951-1015)
- ✅ Update inline comments for filtering logic
- ✅ Update function signature descriptions

### Project Documentation
- ✅ CLAUDE.md - Update "Last Completed Task Summary" section
- ✅ Create new Serena memory: `options_chain_20_strikes_completion_oct_2025.md`
- ✅ Update `tradier_api_response_structures` memory (if needed)
- ✅ Update `ai_agent_instructions_oct_2025` memory (if options chains mentioned)

### Test Evidence
- ✅ Manual CLI test results (before regression suite)
- ✅ CLI regression test report (Phase 1 + Phase 2 results)
- ✅ Test report file path in CLAUDE.md

---

## ⚠️ Risk Assessment

### Low Risk Areas
- ✅ API integration (no changes, already fetches all strikes)
- ✅ Error handling (no changes, already robust)
- ✅ Data formatting (auto-adapts to more strikes)
- ✅ Async implementation (no changes to async pattern)

### Medium Risk Areas
- ⚠️ Filtering logic (core change, must be tested thoroughly)
- ⚠️ Sorting logic (must ensure DESCENDING for both chains)
- ⚠️ Edge cases (what if fewer than 10 strikes above/below available?)

### Mitigation Strategies
1. Manual CLI testing catches issues before regression suite
2. Comprehensive test coverage (4 dedicated tests + 39 total)
3. Existing error handling preserves robustness
4. Small, focused change (only filtering/sorting logic)

---

## 🚀 Implementation Readiness

**Research Status**: ✅ COMPLETE

**Ready for Phase 2 (Planning)**: ✅ YES

**Key Findings**:
- Clear understanding of current implementation
- Algorithm designed and validated
- Test coverage identified
- Risk assessment complete
- Documentation requirements defined

**Next Phase**: Delete existing TODO_task_plan.md and create comprehensive implementation plan

---

## 📚 References

**Code Files Analyzed**:
- src/backend/tools/tradier_tools.py (lines 599-1015)

**Test Files Analyzed**:
- test_cli_regression.sh (lines 94-95, 110-111)

**Serena Tools Used**:
- find_symbol (with include_body=True)
- search_for_pattern
- read_memory

**Sequential-Thinking Phases**:
- 10 thought steps for systematic research planning
- Analysis of requirements, implementation, testing, and documentation

**Research Time**: ~15 minutes (optimal)
