# TODO Task Plan: Retire Individual Options Chain Tools - Implementation Checklist

**Date:** 2025-10-27
**Task:** Systematic removal of `get_call_options_chain` and `get_put_options_chain` tools
**Approach:** Use Sequential-Thinking + Serena tools for all code modifications

---

## Overview

**Objective:** Retire legacy individual options chain tools in favor of the consolidated `get_options_chain_both` tool

**Impact:**
- Remove 4 functions (~500 lines of code)
- Update 4 files
- Reduce tool count from 8 → 6
- Reduce test count from 41 → 37
- Simplify RULE #9 AI instructions

**Validation:**
- Manual CLI testing (4 prompts)
- Full regression testing (37 tests with Phase 2 verification)

---

## 🔴 CRITICAL: MANDATORY TOOL USAGE ENFORCEMENT

**YOU MUST use Sequential-Thinking and Serena tools throughout this implementation:**

- **START each major section** with Sequential-Thinking for systematic approach
- **Use Serena tools** for code analysis and modifications
- **Use Sequential-Thinking** repeatedly for complex reasoning
- **Use Standard Edit tool** only when Serena doesn't support the operation
- **VERIFY** after each modification using pattern search

**NEVER proceed to next step without completing current step verification**

---

## Phase 3: Implementation Checklist

### Section 1: Pre-Implementation Verification

**Purpose:** Ensure research findings are accurate before making changes

- [ ] **Step 1.1:** Use Sequential-Thinking to review research findings
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Analyze research_task_plan.md for completeness
  - **Verify:** All 4 files identified, all references found

- [ ] **Step 1.2:** Verify project is activated
  - **Tool:** `mcp__serena__get_current_config`
  - **Action:** Check active project is market-parser-polygon-mcp
  - **Verify:** Project activated successfully

- [ ] **Step 1.3:** Confirm no uncommitted changes
  - **Tool:** Bash `git status`
  - **Action:** Check working directory is clean
  - **Verify:** No modified files (clean state)

---

### Section 2: Remove Tools from tradier_tools.py

**Purpose:** Remove 4 legacy tool functions using Serena tools

#### Remove get_call_options_chain functions

- [ ] **Step 2.1:** Use Sequential-Thinking to plan function removal approach
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Analyze optimal order for removing functions
  - **Verify:** Removal strategy clear

- [ ] **Step 2.2:** Find and remove `_get_call_options_chain` function
  - **Tool:** `mcp__serena__find_symbol`
  - **Parameters:**
    - `name_path`: `_get_call_options_chain`
    - `relative_path`: `src/backend/tools/tradier_tools.py`
    - `include_body`: true
  - **Action:** Locate function for removal
  - **Verify:** Function found at expected line (~600)

- [ ] **Step 2.3:** Identify line range for `_get_call_options_chain`
  - **Tool:** Sequential-Thinking or Read to determine exact boundaries
  - **Action:** Note start_line and end_line from Step 2.2
  - **Verify:** Exact line range identified

- [ ] **Step 2.4:** Remove `_get_call_options_chain` using Edit tool
  - **Tool:** `Edit` (Serena doesn't support full function deletion)
  - **Action:** Remove function by replacing it with empty string between identified boundaries
  - **Alternative:** Use Read + Edit to remove the entire function block
  - **Verify:** Function removed, no syntax errors

- [ ] **Step 2.5:** Find and remove `get_call_options_chain` wrapper function
  - **Tool:** `mcp__serena__find_symbol`
  - **Parameters:**
    - `name_path`: `get_call_options_chain`
    - `relative_path`: `src/backend/tools/tradier_tools.py`
    - `include_body`: true
  - **Action:** Locate wrapper function
  - **Verify:** Function found at expected line (~754)

- [ ] **Step 2.6:** Remove `get_call_options_chain` wrapper using Edit tool
  - **Tool:** `Edit`
  - **Action:** Remove function completely
  - **Verify:** Function removed, no syntax errors

#### Remove get_put_options_chain functions

- [ ] **Step 2.7:** Find and remove `_get_put_options_chain` function
  - **Tool:** `mcp__serena__find_symbol`
  - **Parameters:**
    - `name_path`: `_get_put_options_chain`
    - `relative_path`: `src/backend/tools/tradier_tools.py`
    - `include_body`: true
  - **Action:** Locate function for removal
  - **Verify:** Function found at expected line (~821)

- [ ] **Step 2.8:** Remove `_get_put_options_chain` using Edit tool
  - **Tool:** `Edit`
  - **Action:** Remove function completely
  - **Verify:** Function removed, no syntax errors

- [ ] **Step 2.9:** Find and remove `get_put_options_chain` wrapper function
  - **Tool:** `mcp__serena__find_symbol`
  - **Parameters:**
    - `name_path`: `get_put_options_chain`
    - `relative_path`: `src/backend/tools/tradier_tools.py`
    - `include_body`: true
  - **Action:** Locate wrapper function
  - **Verify:** Function found at expected line (~1270)

- [ ] **Step 2.10:** Remove `get_put_options_chain` wrapper using Edit tool
  - **Tool:** `Edit`
  - **Action:** Remove function completely
  - **Verify:** Function removed, no syntax errors

#### Update docstring references

- [ ] **Step 2.11:** Remove old tool references from get_options_chain_both docstring
  - **Tool:** `Edit`
  - **Action:** Find and update lines 1244, 1245, 1262 references
  - **Remove references to:**
    - "User explicitly asks for ONLY call options → use get_call_options_chain()"
    - "User explicitly asks for ONLY put options → use get_put_options_chain()"
    - Performance comparison to separate calls
  - **Verify:** Docstring updated, no old tool references remain

#### Final verification for tradier_tools.py

- [ ] **Step 2.12:** Search for any remaining references
  - **Tool:** `mcp__serena__search_for_pattern`
  - **Patterns to search:**
    - `get_call_options_chain`
    - `get_put_options_chain`
  - **Expected:** No matches found
  - **Verify:** All references removed

- [ ] **Step 2.13:** Verify file syntax is valid
  - **Tool:** Bash `uv run python -m py_compile src/backend/tools/tradier_tools.py`
  - **Action:** Check for Python syntax errors
  - **Verify:** No compilation errors

---

### Section 3: Update __init__.py Exports

**Purpose:** Remove imports and exports of old tools

- [ ] **Step 3.1:** Use Sequential-Thinking to plan import removal
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Determine exact lines to remove
  - **Verify:** Clear understanding of changes needed

- [ ] **Step 3.2:** Read current __init__.py to locate exact lines
  - **Tool:** `Read`
  - **Parameters:** `file_path`: `src/backend/tools/__init__.py`
  - **Action:** Identify import and __all__ lines
  - **Verify:** Lines 6, 8, 17, 18 contain old tool references

- [ ] **Step 3.3:** Remove get_call_options_chain import
  - **Tool:** `Edit`
  - **Action:** Remove line 6: `get_call_options_chain,`
  - **Verify:** Import removed

- [ ] **Step 3.4:** Remove get_put_options_chain import
  - **Tool:** `Edit`
  - **Action:** Remove line 8: `get_put_options_chain,`
  - **Verify:** Import removed

- [ ] **Step 3.5:** Remove get_call_options_chain from __all__
  - **Tool:** `Edit`
  - **Action:** Remove line 17: `"get_call_options_chain",`
  - **Verify:** Export removed

- [ ] **Step 3.6:** Remove get_put_options_chain from __all__
  - **Tool:** `Edit`
  - **Action:** Remove line 18: `"get_put_options_chain",`
  - **Verify:** Export removed

- [ ] **Step 3.7:** Verify no remaining references in __init__.py
  - **Tool:** `mcp__serena__search_for_pattern`
  - **Patterns:** `get_call_options_chain`, `get_put_options_chain`
  - **Expected:** No matches
  - **Verify:** All references removed

---

### Section 4: Update agent_service.py

**Purpose:** Remove imports, tool registrations, and simplify RULE #9

#### Remove imports

- [ ] **Step 4.1:** Use Sequential-Thinking to plan agent_service.py updates
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Review all changes needed in service layer
  - **Verify:** Clear plan for imports, RULE #9, tool registration

- [ ] **Step 4.2:** Read imports section to locate exact lines
  - **Tool:** `Read`
  - **Parameters:**
    - `file_path`: `src/backend/services/agent_service.py`
    - `offset`: 1
    - `limit`: 20
  - **Action:** Identify import lines
  - **Verify:** Lines 8, 12 contain old tool imports

- [ ] **Step 4.3:** Remove get_call_options_chain import (line 8)
  - **Tool:** `Edit`
  - **Action:** Remove import statement
  - **Verify:** Import removed

- [ ] **Step 4.4:** Remove get_put_options_chain import (line 12)
  - **Tool:** `Edit`
  - **Action:** Remove import statement
  - **Verify:** Import removed

#### Simplify RULE #9

- [ ] **Step 4.5:** Read current RULE #9 section
  - **Tool:** `Read`
  - **Parameters:**
    - `file_path`: `src/backend/services/agent_service.py`
    - `offset`: 334
    - `limit`: 75
  - **Action:** Review full RULE #9 structure (lines 334-405)
  - **Verify:** Current structure understood

- [ ] **Step 4.6:** Use Sequential-Thinking to design new RULE #9
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Plan simplified RULE #9 with single tool approach
  - **Verify:** New structure clear and comprehensive

- [ ] **Step 4.7:** Replace RULE #9 header
  - **Tool:** `Edit`
  - **Old:** "OPTIONS CHAIN = PREFER get_options_chain_both, FALLBACK to specific tools"
  - **New:** "OPTIONS CHAIN = Use get_options_chain_both for ALL options requests"
  - **Verify:** Header updated

- [ ] **Step 4.8:** Remove "FOR ONLY CALL OPTIONS" section (lines 346-349)
  - **Tool:** `Edit`
  - **Action:** Remove entire section including examples
  - **Verify:** Section removed

- [ ] **Step 4.9:** Remove "FOR ONLY PUT OPTIONS" section (lines 351-354)
  - **Tool:** `Edit`
  - **Action:** Remove entire section including examples
  - **Verify:** Section removed

- [ ] **Step 4.10:** Update decision tree (lines 376-381)
  - **Tool:** `Edit`
  - **Old Decision Tree:**
    ```
    - "call and put options" → get_options_chain_both()
    - "full options chain" → get_options_chain_both()
    - "options for [ticker]" (ambiguous) → get_options_chain_both() (DEFAULT)
    - "ONLY call options" → get_call_options_chain()
    - "ONLY put options" → get_put_options_chain()
    ```
  - **New Decision Tree:**
    ```
    - "call options" → get_options_chain_both() (returns both, user can focus on calls)
    - "put options" → get_options_chain_both() (returns both, user can focus on puts)
    - "both options" → get_options_chain_both()
    - "full options chain" → get_options_chain_both()
    - "options for [ticker]" → get_options_chain_both()
    ```
  - **Verify:** Decision tree simplified

- [ ] **Step 4.11:** Update critical mistakes section (line 390)
  - **Tool:** `Edit`
  - **Old:** "Making TWO separate calls (get_call_options_chain + get_put_options_chain) when get_options_chain_both exists"
  - **New:** "Not using get_options_chain_both for options chain requests"
  - **Verify:** Mistake updated

- [ ] **Step 4.12:** Remove old tool references from line 416
  - **Tool:** `Edit`
  - **Old:** "Using get_call_options_chain or get_put_options_chain when user only wants expiration dates"
  - **New:** "Using get_options_chain_both when user only wants expiration dates"
  - **Verify:** Reference updated

- [ ] **Step 4.13:** Update tool listing (lines 466-467)
  - **Tool:** `Edit`
  - **Action:** Remove lines referencing old tools
  - **Old:**
    ```
    - get_call_options_chain(ticker, current_price, expiration_date) - ONE ticker only
    - get_put_options_chain(ticker, current_price, expiration_date) - ONE ticker only
    ```
  - **Remove both lines** (get_options_chain_both already listed)
  - **Verify:** Tool listing updated

#### Update tool registration

- [ ] **Step 4.14:** Read create_agent() function
  - **Tool:** `Read`
  - **Parameters:**
    - `file_path`: `src/backend/services/agent_service.py`
    - `offset`: 708
    - `limit`: 30
  - **Action:** Review tools list (lines 718-727)
  - **Verify:** Old tools at lines 725-726

- [ ] **Step 4.15:** Remove get_call_options_chain from tools list (line 725)
  - **Tool:** `Edit`
  - **Action:** Remove line: `get_call_options_chain,`
  - **Verify:** Tool removed from registration

- [ ] **Step 4.16:** Remove get_put_options_chain from tools list (line 726)
  - **Tool:** `Edit`
  - **Action:** Remove line: `get_put_options_chain,`
  - **Verify:** Tool removed from registration

- [ ] **Step 4.17:** Update tool count comment (line 727)
  - **Tool:** `Edit`
  - **Old:** `]  # 6 Tradier + 2 Polygon = 8 tools total`
  - **New:** `]  # 4 Tradier + 2 Polygon = 6 tools total`
  - **Verify:** Comment accurate

#### Final verification for agent_service.py

- [ ] **Step 4.18:** Search for any remaining references
  - **Tool:** `mcp__serena__search_for_pattern`
  - **Patterns:** `get_call_options_chain`, `get_put_options_chain`
  - **Expected:** No matches found
  - **Verify:** All references removed

- [ ] **Step 4.19:** Verify file syntax is valid
  - **Tool:** Bash `uv run python -m py_compile src/backend/services/agent_service.py`
  - **Action:** Check for Python syntax errors
  - **Verify:** No compilation errors

---

### Section 5: Update test_cli_regression.sh

**Purpose:** Remove 4 test prompts and renumber remaining tests

- [ ] **Step 5.1:** Use Sequential-Thinking to plan test suite updates
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Determine test removal and renumbering strategy
  - **Verify:** Clear plan for test updates

- [ ] **Step 5.2:** Read test_cli_regression.sh to locate test prompts
  - **Tool:** `Read`
  - **Parameters:** `file_path`: `test_cli_regression.sh`
  - **Action:** Identify lines 94, 95, 111, 112
  - **Verify:** Tests 14, 15, 30, 31 found

- [ ] **Step 5.3:** Remove Test 14 (line 94)
  - **Tool:** `Edit`
  - **Old:** `"Get Call Options Chain Expiring this Friday: $SPY"`
  - **Action:** Remove entire line
  - **Verify:** Test removed

- [ ] **Step 5.4:** Remove Test 15 (line 95)
  - **Tool:** `Edit`
  - **Old:** `"Get Put Options Chain Expiring this Friday: $SPY"`
  - **Action:** Remove entire line
  - **Verify:** Test removed

- [ ] **Step 5.5:** Remove Test 30 (line 111)
  - **Tool:** `Edit`
  - **Old:** `"Get Call Options Chain Expiring this Friday: $NVDA"`
  - **Action:** Remove entire line
  - **Verify:** Test removed

- [ ] **Step 5.6:** Remove Test 31 (line 112)
  - **Tool:** `Edit`
  - **Old:** `"Get Put Options Chain Expiring this Friday: $NVDA"`
  - **Action:** Remove entire line
  - **Verify:** Test removed

- [ ] **Step 5.7:** Update test count references in script header
  - **Tool:** `Edit`
  - **Action:** Find and replace "41 tests" → "37 tests" in comments
  - **Verify:** Test count updated

- [ ] **Step 5.8:** Verify script syntax is valid
  - **Tool:** Bash `bash -n test_cli_regression.sh`
  - **Action:** Check for bash syntax errors
  - **Verify:** No syntax errors

---

### Section 6: Manual CLI Testing (Pre-Phase 4 Validation)

**Purpose:** Validate agent correctly uses get_options_chain_both for all scenarios BEFORE running full regression

🔴 **CRITICAL:** Manual testing MUST PASS before proceeding to Phase 4 regression testing

- [ ] **Step 6.1:** Use Sequential-Thinking to plan manual testing approach
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Design test prompts to cover all scenarios
  - **Verify:** Test plan comprehensive

- [ ] **Step 6.2:** Test Prompt 1 - Call options request
  - **Tool:** Bash `uv run main.py`
  - **Prompt:** "Get call options for SPY expiring this Friday"
  - **Expected:**
    - ✅ Agent calls get_options_chain_both (NOT old tools)
    - ✅ Response includes both call AND put tables
    - ✅ Tables properly formatted with markdown
    - ✅ No errors
  - **Verify:** ALL success criteria met

- [ ] **Step 6.3:** Test Prompt 2 - Put options request
  - **Tool:** Bash `uv run main.py`
  - **Prompt:** "Show me put options for NVDA this Friday"
  - **Expected:**
    - ✅ Agent calls get_options_chain_both (NOT old tools)
    - ✅ Response includes both call AND put tables
    - ✅ Tables properly formatted with markdown
    - ✅ No errors
  - **Verify:** ALL success criteria met

- [ ] **Step 6.4:** Test Prompt 3 - Both options request (explicit)
  - **Tool:** Bash `uv run main.py`
  - **Prompt:** "Both call and put options for AMD this Friday"
  - **Expected:**
    - ✅ Agent calls get_options_chain_both
    - ✅ Response includes both tables
    - ✅ Tables properly formatted
    - ✅ No errors
  - **Verify:** ALL success criteria met

- [ ] **Step 6.5:** Test Prompt 4 - Ambiguous options request
  - **Tool:** Bash `uv run main.py`
  - **Prompt:** "Options chain for AAPL expiring Oct 31"
  - **Expected:**
    - ✅ Agent calls get_options_chain_both
    - ✅ Response includes both tables
    - ✅ Tables properly formatted
    - ✅ No errors
  - **Verify:** ALL success criteria met

- [ ] **Step 6.6:** Document manual test results
  - **Action:** Record response times, tool calls, formatting
  - **Verify:** 4/4 tests passed

🔴 **GATE:** Do NOT proceed to Phase 4 if ANY manual test fails. Fix issues and re-run manual tests.

---

## Phase 4: Regression Testing

### Section 7: Execute Full CLI Regression Test Suite

**Purpose:** Validate all 37 tests pass with new consolidated approach

🔴 **MANDATORY:** Both Phase 1 (automated) and Phase 2 (manual verification) REQUIRED

#### Phase 1: Automated Response Generation

- [ ] **Step 7.1:** Use Sequential-Thinking to review testing requirements
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Review CLAUDE.md testing section for Phase 1 & 2 requirements
  - **Verify:** Testing workflow understood

- [ ] **Step 7.2:** Execute CLI regression test suite
  - **Tool:** Bash `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`
  - **Action:** Run full 37-test suite
  - **Expected:** 37/37 COMPLETED (responses received)
  - **Note:** "COMPLETED" means responses received, NOT validation passed
  - **Verify:** Test report generated

- [ ] **Step 7.3:** Display Phase 1 results to user
  - **Action:** Show completion counts, response times, test report path
  - **Verify:** User sees Phase 1 summary

#### Phase 2: MANDATORY Manual Verification of ALL 37 Tests

🔴 **CRITICAL:** You MUST manually read and verify EACH of the 37 test responses using the Read tool

**Grep commands are INSUFFICIENT - they miss:**
- Duplicate/unnecessary tool calls
- Wrong tool selection
- Data inconsistencies
- Logic errors

- [ ] **Step 7.4:** Use Sequential-Thinking to plan Phase 2 verification
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Review 4-point verification criteria from CLAUDE.md
  - **Verify:** Criteria understood:
    1. Does response address query?
    2. Were RIGHT tools called (no duplicates)?
    3. Is data correct?
    4. Are there any errors?

- [ ] **Step 7.5:** Read test report file
  - **Tool:** `Read`
  - **Parameters:** `file_path`: <test_report_path>
  - **Action:** Identify line ranges for each of the 37 tests
  - **Verify:** Can locate each test's response section

- [ ] **Step 7.6:** Manually verify Test 1
  - **Tool:** `Read` (read test 1 section from report)
  - **Apply 4-point criteria:**
    1. ✅ Response addresses query?
    2. ✅ RIGHT tools called (no duplicates)?
    3. ✅ Data correct?
    4. ✅ No errors?
  - **Document:** PASS or FAIL (with reason)
  - **Verify:** Test 1 validation complete

- [ ] **Step 7.7 - 7.42:** Manually verify Tests 2-37
  - **Tool:** `Read` (for EACH test section)
  - **Apply 4-point criteria to EACH test**
  - **Document:** PASS/FAIL for each test
  - **Special attention to:**
    - Test 14 (formerly Test 16 - SPY both chains)
    - Test 28 (formerly Test 32 - NVDA both chains)
    - Test 15 (formerly Test 17 - SPY analysis no tool calls)
    - Test 29 (formerly Test 33 - NVDA analysis no tool calls)
  - **Verify:** ALL 37 tests manually reviewed

- [ ] **Step 7.43:** Create comprehensive test results table
  - **Action:** Document ALL 37 tests in table format
  - **Columns:** Test #, Test Name, Status, Issue (if failed), Failure Type
  - **Example:**
    ```
    | Test # | Test Name | Status | Issue | Failure Type |
    |--------|-----------|--------|-------|--------------|
    | 1 | Market_Status | ✅ PASS | - | - |
    | 2 | SPY_Price | ✅ PASS | - | - |
    | ... | ... | ... | ... | ... |
    ```
  - **Verify:** Table complete with all 37 tests

- [ ] **Step 7.44:** Answer Phase 2 checkpoint questions
  - **Questions:**
    1. ✅ Did you READ all 37 test responses manually using Read tool? **YES/NO**
    2. ✅ Did you apply all 4 verification criteria to EACH test? **YES/NO**
    3. ✅ How many tests PASSED all 4 criteria? **X/37 PASSED**
    4. ✅ How many tests FAILED (any criterion)? **X/37 FAILED**
    5. ✅ Did you document ALL failures with test #, issue, and failure type? **YES/NO + TABLE**
  - **Verify:** All questions answered with evidence

- [ ] **Step 7.45:** Display Phase 2 results to user
  - **Action:** Show test results table, checkpoint answers, failure details (if any)
  - **Verify:** User sees complete Phase 2 validation

🔴 **ENFORCEMENT:** Cannot mark task complete without:
- Reading all 37 test responses manually (Read tool, NOT grep)
- Applying all 4 criteria to each test
- Documenting ALL 37 tests in results table
- Providing failure count and details
- Answering all 5 checkpoint questions

🔴 **GATE:** If ANY test fails Phase 2 verification, fix issues and re-run BOTH Phase 1 and Phase 2.

- [ ] **Step 7.46:** Verify average response time
  - **Tool:** Grep or analyze test report
  - **Expected:** Average ≤ 15 seconds
  - **Verify:** Performance acceptable

- [ ] **Step 7.47:** Verify session persistence
  - **Tool:** Grep test report for session info
  - **Expected:** Single persistent session for all 37 tests
  - **Verify:** Session maintained

---

## Phase 5: Documentation & Git Commit

### Section 8: Update Documentation

**Purpose:** Update CLAUDE.md and memory files with task completion details

- [ ] **Step 8.1:** Use Sequential-Thinking to plan documentation updates
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Review what documentation needs updating
  - **Verify:** Clear plan for CLAUDE.md, memories

- [ ] **Step 8.2:** Update CLAUDE.md Last Completed Task Summary
  - **Tool:** `Edit`
  - **Action:** Replace content between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->`
  - **New Summary Should Include:**
    - Task title and summary
    - Changes implemented (4 files modified, functions removed)
    - Testing results (manual 4/4 + regression 37/37)
    - Files modified list
    - Documentation updated list
    - Risk assessment
    - Performance impact
  - **Verify:** Summary complete and accurate

- [ ] **Step 8.3:** Update ai_agent_instructions_oct_2025.md memory
  - **Tool:** `mcp__serena__write_memory`
  - **Memory name:** `ai_agent_instructions_oct_2025`
  - **Action:** Document updated RULE #9 (single tool approach)
  - **Verify:** Memory updated

- [ ] **Step 8.4:** Update tech_stack_oct_2025.md memory (if needed)
  - **Tool:** `mcp__serena__write_memory`
  - **Memory name:** `tech_stack_oct_2025`
  - **Action:** Update tool count: 8 → 6 tools
  - **Verify:** Memory updated

- [ ] **Step 8.5:** Clean up task plan files
  - **Action:** Keep research_task_plan.md and TODO_task_plan.md for reference
  - **Verify:** Files preserved for future reference

---

### Section 9: Atomic Git Commit

**Purpose:** Stage ALL work at once and commit atomically

🔴 **CRITICAL:** Follow EXACT workflow - DO NOT stage early

#### Step 1: DO ALL WORK FIRST (Already Complete)

- [x] All code changes complete
- [x] All tests run and passed
- [x] All documentation updated
- [x] All config files updated
- [x] All task plans complete

#### Step 2: Verify Everything Complete

- [ ] **Step 9.1:** Use Sequential-Thinking to review commit readiness
  - **Tool:** `mcp__sequential-thinking__sequentialthinking`
  - **Action:** Verify ALL work done, nothing pending
  - **Verify:** Ready for atomic commit

- [ ] **Step 9.2:** Review all changed files
  - **Tool:** Bash `git status`
  - **Expected Files:**
    - src/backend/tools/tradier_tools.py (modified)
    - src/backend/tools/__init__.py (modified)
    - src/backend/services/agent_service.py (modified)
    - test_cli_regression.sh (modified)
    - test-reports/<latest_report>.log (new)
    - CLAUDE.md (modified)
    - research_task_plan.md (new)
    - TODO_task_plan.md (new)
    - .serena/memories/*.md (modified - if updated)
  - **Verify:** ALL expected files present

- [ ] **Step 9.3:** Review all changes
  - **Tool:** Bash `git diff`
  - **Action:** Scan changes to ensure all look correct
  - **Verify:** Changes as expected

#### Step 3: Stage Everything at Once

⚠️ **THIS IS THE FIRST TIME YOU RUN `git add`** ⚠️

- [ ] **Step 9.4:** Stage ALL files in ONE command
  - **Tool:** Bash `git add -A`
  - **Action:** Stage everything at once
  - **Verify:** Command executed

#### Step 4: Verify Staging Immediately

- [ ] **Step 9.5:** Verify ALL files staged, NOTHING unstaged
  - **Tool:** Bash `git status`
  - **Expected:** All files in "Changes to be committed", NO files in "Changes not staged"
  - **Verify:** Everything staged correctly

#### Step 5: Commit Immediately (within 60 seconds)

- [ ] **Step 9.6:** Create atomic commit
  - **Tool:** Bash
  - **Command:**
    ```bash
    git commit -m "$(cat <<'EOF'
    [REFACTOR] Retire individual options chain tools - Consolidate to single unified tool

    **Summary:** Successfully retired get_call_options_chain and get_put_options_chain
    legacy tools in favor of consolidated get_options_chain_both tool. Achieved code
    simplification (~500 lines removed), reduced tool count (8→6), and streamlined AI
    agent instructions (RULE #9). All manual (4/4) and regression (37/37) tests passed.

    **Code Changes:**
    - Removed 4 functions from src/backend/tools/tradier_tools.py
      - _get_call_options_chain (async implementation)
      - get_call_options_chain (@function_tool wrapper)
      - _get_put_options_chain (async implementation)
      - get_put_options_chain (@function_tool wrapper)
    - Updated src/backend/tools/__init__.py
      - Removed 2 imports (get_call_options_chain, get_put_options_chain)
      - Removed 2 __all__ exports
    - Updated src/backend/services/agent_service.py
      - Removed 2 imports
      - Simplified RULE #9: Single tool approach (removed fallback options)
      - Removed 2 tool registrations
      - Updated tool count comment: 8 → 6 tools
    - Updated test_cli_regression.sh
      - Removed 4 redundant test prompts (Tests 14, 15, 30, 31)
      - Updated test count: 41 → 37 tests

    **AI Agent Instructions (RULE #9 Updates):**
    - Header: "OPTIONS CHAIN = Use get_options_chain_both for ALL options requests"
    - Removed separate sections for call/put specific tools
    - Simplified decision tree: All options requests → get_options_chain_both()
    - Updated critical mistakes section
    - Removed fallback language

    **Testing Results:**
    - ✅ Manual CLI: 4/4 PASSED (call, put, both, ambiguous queries)
    - ✅ Phase 1: 37/37 COMPLETED (100% response generation)
    - ✅ Phase 2: 37/37 PASSED (manual verification of all test responses)
    - ✅ Test Report: test-reports/<report_file_name>
    - ✅ Average Response Time: <X.XX>s (EXCELLENT)
    - ✅ Session Persistence: 1 persistent session for all 37 tests
    - ✅ Zero failures, zero errors, zero data issues

    **Documentation Updated:**
    - ✅ CLAUDE.md (Last Completed Task Summary)
    - ✅ research_task_plan.md (comprehensive research findings)
    - ✅ TODO_task_plan.md (detailed implementation checklist)
    - ✅ .serena/memories/ai_agent_instructions_oct_2025.md (RULE #9 update)
    - ✅ .serena/memories/tech_stack_oct_2025.md (tool count update)

    **Impact Summary:**
    - Code Reduction: ~500 lines removed
    - Tool Count: 8 → 6 tools
    - Test Count: 41 → 37 tests (redundant tests removed)
    - Agent Instructions: Simplified from 3 approaches → 1 unified approach
    - Performance: Maintained excellent response times (<15s avg)

    **Risk Assessment:** VERY LOW
    - Clean removal with no backward compatibility issues
    - Consolidated tool already validated in production
    - Comprehensive testing (manual + regression)
    - Zero test failures with new implementation

    🤖 Generated with [Claude Code](https://claude.com/claude-code)

    Co-Authored-By: Claude <noreply@anthropic.com>
    EOF
    )"
    ```
  - **Note:** Replace `<report_file_name>` and `<X.XX>s` with actual values
  - **Verify:** Commit successful

#### Step 6: Push Immediately

- [ ] **Step 9.7:** Push to remote repository
  - **Tool:** Bash `git push`
  - **Action:** Push commit to remote
  - **Verify:** Push successful

---

## Completion Checklist

### All Phases Complete When:

- [x] **Phase 1: Research** - Complete
  - [x] All tool references identified
  - [x] Research plan documented

- [ ] **Phase 2: Planning** - Complete
  - [ ] TODO task plan reviewed and approved by user

- [ ] **Phase 3: Implementation** - Complete
  - [ ] All 4 files modified (tradier_tools.py, __init__.py, agent_service.py, test_cli_regression.sh)
  - [ ] All functions removed (4 total)
  - [ ] All imports/exports updated
  - [ ] RULE #9 simplified
  - [ ] Tool registration updated
  - [ ] Manual CLI testing passed (4/4)

- [ ] **Phase 4: Testing** - Complete
  - [ ] Phase 1: 37/37 tests completed (response generation)
  - [ ] Phase 2: 37/37 tests manually verified (4-point criteria)
  - [ ] Test results table created
  - [ ] Checkpoint questions answered
  - [ ] Performance metrics acceptable

- [ ] **Phase 5: Documentation & Commit** - Complete
  - [ ] CLAUDE.md updated
  - [ ] Memory files updated
  - [ ] Atomic git commit created
  - [ ] Changes pushed to remote

---

## Success Criteria

**Task is COMPLETE when ALL of the following are TRUE:**

- ✅ All 4 legacy tool functions removed from tradier_tools.py
- ✅ All imports and exports updated in __init__.py
- ✅ RULE #9 simplified to single tool approach
- ✅ Tool registration updated (6 tools)
- ✅ Test suite updated (37 tests)
- ✅ Manual CLI testing passed (4/4 prompts)
- ✅ Phase 4 regression testing passed (37/37 tests)
- ✅ Phase 2 manual verification completed (all 37 tests reviewed)
- ✅ Documentation updated (CLAUDE.md, memories)
- ✅ Atomic git commit created with all changes
- ✅ Changes pushed to remote repository

---

**Plan Status:** ✅ READY FOR USER APPROVAL
**Next Action:** Present plan to user for review and approval before proceeding to Phase 3
