# Research Task Plan: Retire Individual Options Chain Tools

**Date:** 2025-10-27
**Task:** Retire `get_call_options_chain` and `get_put_options_chain` tools in favor of consolidated `get_options_chain_both` tool

---

## Executive Summary

Comprehensive research completed using Sequential-Thinking and Serena tools to identify all references to the legacy individual options chain tools. The `get_options_chain_both` tool (implemented in previous task) has been validated and can now fully replace the separate call/put tools, enabling code simplification and improved efficiency.

**Research Methodology:** Sequential-Thinking analysis + Serena symbol/pattern search + codebase analysis
**Research Duration:** ~15 minutes
**Sources Analyzed:** 4 files across tools, services, and test suite

---

## Research Question

**Primary Question:** Where are `get_call_options_chain` and `get_put_options_chain` referenced throughout the codebase, and what changes are needed to retire them completely?

---

## Key Findings

### 1. Code References Found (4 Files)

#### **src/backend/tools/tradier_tools.py** (Primary implementation)
- **Functions to remove (4 total):**
  - `_get_call_options_chain` (line ~600) - Async implementation (~150 lines)
  - `get_call_options_chain` (line ~754) - @function_tool wrapper (~60 lines)
  - `_get_put_options_chain` (line ~821) - Async implementation (~150 lines)
  - `get_put_options_chain` (line ~1270) - @function_tool wrapper (~60 lines)
- **Internal docstring references (3 locations):**
  - Line 1244: Reference in get_options_chain_both docstring
  - Line 1245: Reference in get_options_chain_both docstring
  - Line 1262: Performance comparison comment

**Total code removal:** ~420 lines

#### **src/backend/tools/__init__.py** (Module exports)
- **Imports to remove (2):**
  - Line 6: `get_call_options_chain`
  - Line 8: `get_put_options_chain`
- **__all__ exports to remove (2):**
  - Line 17: `"get_call_options_chain"`
  - Line 18: `"get_put_options_chain"`

**Total changes:** 4 lines removed

#### **src/backend/services/agent_service.py** (Service layer + AI instructions)
- **Imports to remove (2):**
  - Line 8: `get_call_options_chain`
  - Line 12: `get_put_options_chain`
- **RULE #9 references (12 locations):**
  - Lines 334-405: Complete RULE #9 section
  - Lines 347-349: Call options specific instructions
  - Lines 352-354: Put options specific instructions
  - Lines 380-381: Decision tree references
  - Line 390: Critical mistakes section
  - Line 416: Common mistakes reference
  - Lines 466-467: Tool listing
- **Tool registration in create_agent() (2 lines):**
  - Line 725: `get_call_options_chain,`
  - Line 726: `get_put_options_chain,`
- **Comment update:**
  - Line 727: "# 6 Tradier + 2 Polygon = 8 tools total" → "# 4 Tradier + 2 Polygon = 6 tools total"

**Total changes:** ~70 lines modified/removed

#### **test_cli_regression.sh** (Test suite)
- **Test prompts to remove (4):**
  - Test 14 (line 94): "Get Call Options Chain Expiring this Friday: $SPY"
  - Test 15 (line 95): "Get Put Options Chain Expiring this Friday: $SPY"
  - Test 30 (line 111): "Get Call Options Chain Expiring this Friday: $NVDA"
  - Test 31 (line 112): "Get Put Options Chain Expiring this Friday: $NVDA"

- **Test prompts to keep (consolidated):**
  - Test 16 (line 96): "Get both Call and Put Options Chains Expiring this Friday: $SPY"
  - Test 32 (line 113): "Get both Call and Put Options Chains Expiring this Friday: $NVDA"

- **Test prompts to keep (analysis - no tool calls):**
  - Test 17 (line 97): "Analyze the Options Chain WITH NO TOOL CALLS..."
  - Test 33 (line 114): "Analyze the Options Chain WITH NO TOOL CALLS..."

**Impact:** Test count: 41 → 37 tests (-4 tests)
**Rationale:** Consolidated tool tests (16, 32) already validate the unified approach

---

### 2. Current RULE #9 Structure Analysis

**Current Header:** "OPTIONS CHAIN = PREFER get_options_chain_both, FALLBACK to specific tools"

**Current Sections:**
1. **Recommended approach** (lines 337-344): get_options_chain_both
2. **Call-specific approach** (lines 346-349): get_call_options_chain - **TO REMOVE**
3. **Put-specific approach** (lines 351-354): get_put_options_chain - **TO REMOVE**
4. **Common sections:** Parameters, date handling, response format, decision tree, workflow

**Decision Tree (Current - lines 376-381):**
- "call and put options" → get_options_chain_both()
- "full options chain" → get_options_chain_both()
- "options for [ticker]" (ambiguous) → get_options_chain_both() (DEFAULT)
- "ONLY call options" → get_call_options_chain() - **TO REMOVE**
- "ONLY put options" → get_put_options_chain() - **TO REMOVE**

**Critical Mistakes (Line 390):**
- "Making TWO separate calls (get_call_options_chain + get_put_options_chain) when get_options_chain_both exists" - **TO UPDATE**

---

### 3. Proposed RULE #9 Simplification

**New Header:** "OPTIONS CHAIN = Use get_options_chain_both for ALL options requests"

**New Structure:**
1. **Single unified approach:** get_options_chain_both handles ALL cases
2. **Common sections:** Keep parameters, date handling, response format
3. **Simplified decision tree:** All options requests → get_options_chain_both()
4. **Updated workflow:** Remove references to separate tools

**New Decision Logic:**
- "call options" → get_options_chain_both() (returns both, user can focus on calls)
- "put options" → get_options_chain_both() (returns both, user can focus on puts)
- "both options" → get_options_chain_both()
- "full options chain" → get_options_chain_both()
- "options for [ticker]" → get_options_chain_both()

**Rationale:** Single table with 20 strikes (10 above + 10 below) covers all use cases, whether user wants calls, puts, or both

---

### 4. Impact Summary

**Code Simplification:**
- **Lines removed:** ~500 lines total
- **Functions removed:** 4 (2 async + 2 wrappers)
- **Tools reduced:** 8 → 6 tools
- **Tests reduced:** 41 → 37 tests

**Benefits:**
- ✅ Simplified codebase (fewer functions to maintain)
- ✅ Reduced complexity (single approach vs. multiple fallbacks)
- ✅ Better performance (single API call vs. potential two calls)
- ✅ Clearer AI instructions (one tool covers all cases)
- ✅ Maintained test coverage (consolidated tests validate unified approach)

**No Backward Compatibility Needed:**
- Previous task validated get_options_chain_both with 100% pass rate
- Tool has been in production and proven reliable
- Clean removal without deprecation period

---

### 5. Risk Assessment

**Risk Level:** VERY LOW

**Mitigating Factors:**
- ✅ get_options_chain_both already validated (41/41 tests passed)
- ✅ Consolidated tool covers ALL use cases
- ✅ Comprehensive testing planned (manual + regression)
- ✅ Systematic removal approach (Serena tools ensure completeness)
- ✅ No external dependencies affected

**Potential Issues:**
- ⚠️ Test count reduction (41 → 37) - ACCEPTABLE (redundant tests removed)
- ⚠️ Agent needs to adapt to single-tool approach - LOW RISK (instructions updated)

---

## Validation Strategy

### Manual CLI Testing (Pre-Phase 4)
**Purpose:** Validate agent correctly uses get_options_chain_both for all scenarios

**Test Prompts:**
1. "Get call options for SPY expiring this Friday"
2. "Show me put options for NVDA this Friday"
3. "Both call and put options for AMD this Friday"
4. "Options chain for AAPL expiring Oct 31"

**Success Criteria:**
- ✅ Agent calls get_options_chain_both for ALL prompts
- ✅ Response includes proper tables (calls and puts)
- ✅ Formatting matches expected markdown structure
- ✅ No errors or missing data

### Phase 4: Full CLI Regression Testing
**Test Suite:** test_cli_regression.sh (37 tests)

**Success Criteria:**
- ✅ Phase 1: 37/37 tests complete (100% response generation)
- ✅ Phase 2: Manual verification of ALL 37 test responses
- ✅ All options chain tests use get_options_chain_both
- ✅ No redundant tool calls detected
- ✅ Average response time ≤ 15 seconds

---

## Files Requiring Modification

### Primary Changes (4 files)

1. **src/backend/tools/tradier_tools.py**
   - Remove 4 functions
   - Update 3 internal docstring references
   - **Estimated changes:** ~420 lines removed

2. **src/backend/tools/__init__.py**
   - Remove 2 imports
   - Remove 2 __all__ exports
   - **Estimated changes:** 4 lines removed

3. **src/backend/services/agent_service.py**
   - Remove 2 imports
   - Simplify RULE #9 (~70 lines)
   - Remove 2 tool registrations
   - Update tool count comment
   - **Estimated changes:** ~75 lines modified/removed

4. **test_cli_regression.sh**
   - Remove 4 test prompts
   - Renumber subsequent tests
   - Update test count references
   - **Estimated changes:** 4 lines removed + renumbering

---

## Source Analysis

### Research Sources Used

1. **Serena Tools (Symbol/Pattern Search):**
   - ✅ `get_symbols_overview` - Identified all functions in tradier_tools.py
   - ✅ `search_for_pattern` - Found all references to old tools across codebase
   - **Reliability:** HIGH (official LSP-based code analysis)

2. **Grep Search:**
   - ✅ Found test prompts in test_cli_regression.sh
   - ✅ Identified RULE #9 structure in agent_service.py
   - **Reliability:** HIGH (direct file content search)

3. **Sequential-Thinking Analysis:**
   - ✅ Systematic breakdown of task requirements
   - ✅ Impact analysis and risk assessment
   - **Reliability:** HIGH (structured reasoning process)

---

## Gaps Identified

**None** - All necessary information found for complete implementation

---

## Recommendations

### Implementation Approach

1. **Use Serena Tools for Code Modifications:**
   - ✅ `find_symbol` to locate exact function boundaries
   - ✅ `replace_symbol_body` for removing functions
   - ✅ Standard Edit tool for imports and registrations

2. **Follow Systematic Order:**
   1. Remove tool functions (tradier_tools.py)
   2. Update imports and exports (__init__.py)
   3. Update service layer (agent_service.py)
   4. Update test suite (test_cli_regression.sh)
   5. Perform manual CLI validation
   6. Run Phase 4 regression testing

3. **Verification at Each Step:**
   - ✅ Verify no remaining references after each file update
   - ✅ Run manual tests before regression suite
   - ✅ Document all changes in CLAUDE.md

---

## Next Steps

**Immediate Actions:**
1. ✅ Research complete - generate TODO_task_plan.md with detailed implementation checklist
2. Present plan to user for approval
3. Upon approval, proceed to Phase 3: Implementation

**Phase 2 Deliverable:**
- Detailed granular implementation plan (TODO_task_plan.md)
- Step-by-step checklist for systematic tool usage
- Testing phase integration
- Comprehensive documentation updates

---

## Success Criteria

**Research Phase Complete When:**
- ✅ All tool references identified across codebase
- ✅ Current RULE #9 structure analyzed
- ✅ Impact assessment completed
- ✅ Validation strategy defined
- ✅ Research findings documented in this file

**Overall Task Complete When:**
- ✅ All 4 old tool functions removed
- ✅ All imports and registrations updated
- ✅ RULE #9 simplified to single-tool approach
- ✅ Test suite updated (37 tests)
- ✅ Manual CLI testing passed (4/4 prompts)
- ✅ Phase 4 regression testing passed (37/37 tests)
- ✅ Documentation updated (CLAUDE.md, memories)
- ✅ Atomic git commit with all changes

---

**Research Status:** ✅ COMPLETE
**Next Phase:** Phase 2 - Planning (Generate TODO_task_plan.md)
