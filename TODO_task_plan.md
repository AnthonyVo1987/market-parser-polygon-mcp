# TODO: Service Tier Change & Test Suite Restructuring Implementation Plan

**Created:** 2025-10-08
**Status:** PLANNING PHASE COMPLETE - READY FOR IMPLEMENTATION
**Estimated Complexity:** MEDIUM (2 code changes + test validation + docs)

---

## 📋 TASK OVERVIEW

### Primary Objectives

1. **Change OpenAI service tier** from "flex" to "default" to fix rate limiting issues
2. **Restructure test suite** from 35 tests to 33 tests with improved test organization
3. **Validate changes** with 100% test pass rate before completion

### Key Changes Summary

- **Service Tier:** "flex" → "default" (better performance for prototyping)
- **Test Count:** 35 tests → 33 tests (SPY: 15→14, NVDA: 15→14, Multi: 5→5)
- **Test Structure:** Reordered sequences + dynamic date queries vs hardcoded dates
- **Multi-Ticker:** INTC replaced with GME in multi-ticker tests

---

## 🔧 PHASE 1: CODE IMPLEMENTATION

### Task 1.1: Change Service Tier in agent_service.py

**File:** `src/backend/services/agent_service.py`
**Location:** Line 367
**Tool:** Serena `mcp__serena__replace_lines` or `mcp__serena__search_for_pattern` + Edit

**Current Code (Line 367):**
```python
extra_args={"service_tier": "flex", "user": "financial_analysis_agent"},
```

**New Code:**
```python
extra_args={"service_tier": "default", "user": "financial_analysis_agent"},
```

**Implementation Steps:**
1. ✅ Use Sequential-Thinking to plan the edit approach
2. ✅ Use Serena `search_for_pattern` to locate exact line (already done during investigation)
3. ✅ Use Edit tool to replace "flex" with "default"
4. ✅ Verify change with Read tool or Serena pattern search

**Validation:** Confirm line 367 now contains `"service_tier": "default"`

---

### Task 1.2: Restructure Test Suite in test_cli_regression.sh

**File:** `test_cli_regression.sh`
**Locations:** Lines 3, 16-19, 70-109, 111-150
**Tool:** Edit tool (bash script, not Python source code)

#### Subtask 1.2.1: Update Header Comments

**Lines to Update:** 3, 16-19

**Current (Lines 3, 16-19):**
```bash
# CLI Test Regression Script - NEW 35-Test Suite with Chat History Analysis
# Tests all 35 standardized test prompts sequentially in a SINGLE CLI session
...
# - SPY Test Sequence: Tests 1-15 (15 tests)
# - NVDA Test Sequence: Tests 16-30 (15 tests)
# - Multi-Ticker Test Sequence: Tests 31-35 (5 tests)
# Total: 35 tests per loop
```

**New:**
```bash
# CLI Test Regression Script - NEW 33-Test Suite with Chat History Analysis
# Tests all 33 standardized test prompts sequentially in a SINGLE CLI session
...
# - SPY Test Sequence: Tests 1-14 (14 tests)
# - NVDA Test Sequence: Tests 15-28 (14 tests)
# - Multi-Ticker Test Sequence: Tests 29-33 (5 tests)
# Total: 33 tests per loop
```

#### Subtask 1.2.2: Replace prompts Array (Lines 70-109)

**Implementation:**
1. ✅ Use Sequential-Thinking to plan the replacement strategy
2. ✅ Use Edit tool to replace lines 70-109 with new test prompts
3. ✅ Ensure correct formatting and escaping for bash array

**New prompts Array:**
```bash
declare -a prompts=(
    # SPY Test Sequence (Tests 1-14)
    "Market Status"
    "Current Price: \$SPY"
    "Today's Closing Price: \$SPY"
    "Yesterday's Closing Price: \$SPY"
    "Last week's Performance: \$SPY"
    "Stock Price on the previous week's Friday: \$SPY"
    "Daily Stock Price bars Analysis from the last 2 trading weeks: \$SPY"
    "RSI-14: \$SPY"
    "MACD: \$SPY"
    "SMA 20/50/200: \$SPY"
    "EMA 20/50/200: SPY"
    "Support & Resistance Levels: \$SPY"
    "Technical Analysis: \$SPY"
    "Get First 3 Call Option Quotes expiring this Friday above current price (show strike prices): \$SPY"
    "Get First 3 Put Option Quotes expiring this Friday below current price (show strike prices): \$SPY"
    # NVDA Test Sequence (Tests 15-28)
    "Market Status"
    "Current Price: \$NVDA"
    "Today's Closing Price: \$NVDA"
    "Yesterday's Closing Price: \$NVDA"
    "Last week's Performance: \$NVDA"
    "Stock Price on the previous week's Friday: \$NVDA"
    "Daily Stock Price bars Analysis from the last 2 trading weeks: \$NVDA"
    "RSI-14: \$NVDA"
    "MACD: \$NVDA"
    "SMA 20/50/200: \$NVDA"
    "EMA 20/50/200: NVDA"
    "Support & Resistance Levels: \$NVDA"
    "Technical Analysis: \$NVDA"
    "Get First 3 Call Option Quotes expiring this Friday above current price (show strike prices): \$NVDA"
    "Get First 3 Put Option Quotes expiring this Friday below current price (show strike prices): \$NVDA"
    # Multi-Ticker Test Sequence (Tests 29-33)
    "Market Status"
    "Current Price: \$WDC, \$AMD, \$GME"
    "Today's Closing Price: \$WDC, \$AMD, \$GME"
    "Yesterday's Closing Price: \$WDC, \$AMD, \$GME"
    "Last week's Performance: \$WDC, \$AMD, \$GME"
    "Daily bars Analysis from the last 2 trading weeks: \$WDC, \$AMD, \$GME"
)
```

**Note:** Added "Market Status" at the beginning of Multi-Ticker sequence per requirements

#### Subtask 1.2.3: Replace test_names Array (Lines 111-150)

**Implementation:**
1. ✅ Use Sequential-Thinking to plan the replacement
2. ✅ Use Edit tool to replace lines 111-150 with new test names
3. ✅ Ensure test numbers match new prompts array (1-33 instead of 1-35)

**New test_names Array:**
```bash
declare -a test_names=(
    # SPY Test Sequence (Tests 1-14)
    "Test_1_Market_Status"
    "Test_2_SPY_Current_Price"
    "Test_3_SPY_Today_Closing_Price"
    "Test_4_SPY_Yesterday_Closing_Price"
    "Test_5_SPY_Last_Week_Performance"
    "Test_6_SPY_Previous_Week_Friday_Price"
    "Test_7_SPY_Last_2_Weeks_Daily_Bars"
    "Test_8_SPY_RSI_14"
    "Test_9_SPY_MACD"
    "Test_10_SPY_SMA_20_50_200"
    "Test_11_SPY_EMA_20_50_200"
    "Test_12_SPY_Support_Resistance"
    "Test_13_SPY_Technical_Analysis"
    "Test_14_SPY_3_Call_Options_This_Friday"
    "Test_15_SPY_3_Put_Options_This_Friday"
    # NVDA Test Sequence (Tests 15-28)
    "Test_16_Market_Status"
    "Test_17_NVDA_Current_Price"
    "Test_18_NVDA_Today_Closing_Price"
    "Test_19_NVDA_Yesterday_Closing_Price"
    "Test_20_NVDA_Last_Week_Performance"
    "Test_21_NVDA_Previous_Week_Friday_Price"
    "Test_22_NVDA_Last_2_Weeks_Daily_Bars"
    "Test_23_NVDA_RSI_14"
    "Test_24_NVDA_MACD"
    "Test_25_NVDA_SMA_20_50_200"
    "Test_26_NVDA_EMA_20_50_200"
    "Test_27_NVDA_Support_Resistance"
    "Test_28_NVDA_Technical_Analysis"
    "Test_29_NVDA_3_Call_Options_This_Friday"
    "Test_30_NVDA_3_Put_Options_This_Friday"
    # Multi-Ticker Test Sequence (Tests 29-33)
    "Test_31_Multi_Market_Status"
    "Test_32_Multi_Current_Price_WDC_AMD_GME"
    "Test_33_Multi_Today_Closing_Price_WDC_AMD_GME"
    "Test_34_Multi_Yesterday_Closing_Price_WDC_AMD_GME"
    "Test_35_Multi_Last_Week_Performance_WDC_AMD_GME"
    "Test_36_Multi_Last_2_Weeks_Daily_Bars_WDC_AMD_GME"
)
```

**Validation Steps:**
1. ✅ Verify prompts array has exactly 33 entries
2. ✅ Verify test_names array has exactly 33 entries
3. ✅ Verify array indices match (prompts[0] corresponds to test_names[0])
4. ✅ Verify header comments updated to reflect 33 tests

---

## 🧪 PHASE 2: CLI TESTING (MANDATORY CHECKPOINT)

### Task 2.1: Execute Test Suite

**Command:**
```bash
./test_cli_regression.sh
```

**Requirements:**
- ✅ All 33 tests must execute successfully
- ✅ 100% pass rate required (33/33 PASS)
- ✅ Session persistence verified (single session)
- ✅ Performance metrics acceptable (avg response time < 30s = EXCELLENT)

**Tools to Use:**
1. ✅ Sequential-Thinking to analyze test execution strategy
2. ✅ Bash tool to execute test script
3. ✅ Read tool to examine test report file

### Task 2.2: Verify Test Results

**Expected Output:**
```
Total Tests: 33
Passed: 33
Failed: 0
Success Rate: 100%
```

**Validation Checklist:**
- [ ] Test count shows 33 tests (not 35)
- [ ] All tests pass with PASS status
- [ ] No FAIL, ERROR, or TIMEOUT statuses
- [ ] Test report file generated in test-reports/
- [ ] Response times reasonable (< 60s per test)
- [ ] Session persistence confirmed (single session)

### Task 2.3: Document Test Evidence

**Required Actions:**
1. ✅ Copy test summary output to show user
2. ✅ Provide test report file path
3. ✅ Show performance metrics (min/max/avg response times)
4. ✅ Confirm 100% success rate

**If Tests Fail:**
1. ✅ Analyze failure reasons using Sequential-Thinking
2. ✅ Fix identified issues using appropriate tools
3. ✅ Re-run tests until 100% pass rate achieved
4. ✅ DO NOT proceed to next phase until tests pass

---

## 📝 PHASE 3: DOCUMENTATION UPDATES

### Task 3.1: Update CLAUDE.md

**File:** `CLAUDE.md`
**Tool:** Edit tool

**Changes Required:**
1. Update test count references: 35 → 33
2. Add service tier change note to Last Completed Task Summary

**Specific Updates:**

**Line ~392 (Testing section):**
```markdown
# Before
- **Testing**: CLI regression test suite (test_cli_regression.sh - 35 tests)

# After
- **Testing**: CLI regression test suite (test_cli_regression.sh - 33 tests)
```

**Lines 12-66 (Last Completed Task Summary):**
- Replace entire section with new task summary including:
  - Service tier change (flex → default)
  - Test suite restructuring (35 → 33 tests)
  - Test results (33/33 PASS, 100% success rate)
  - Performance metrics from test execution

**Implementation Steps:**
1. ✅ Use Sequential-Thinking to plan documentation strategy
2. ✅ Use Edit tool to update test count
3. ✅ Use Edit tool to replace Last Completed Task Summary
4. ✅ Verify all test count references updated (use grep to find any remaining "35")

### Task 3.2: Update README.md (if applicable)

**File:** `README.md`
**Tool:** Edit tool or Serena search_for_pattern

**Check for test count references:**
1. ✅ Use Serena search_for_pattern to find "35" or "35 tests"
2. ✅ Update any found references to "33 tests"

---

## 🧠 PHASE 4: SERENA MEMORY UPDATES

### Task 4.1: Update testing_procedures Memory

**File:** `.serena/memories/testing_procedures.md`
**Tool:** Serena read_memory, then Edit tool

**Updates Required:**
1. Update test count: 35 → 33
2. Update test sequence breakdown (SPY: 14, NVDA: 14, Multi: 5)
3. Add service tier change note
4. Update with latest test results

**Implementation Steps:**
1. ✅ Use Sequential-Thinking to plan memory update
2. ✅ Use Serena read_memory to review current content
3. ✅ Use Edit tool to update test information
4. ✅ Include latest test results (33/33 PASS, performance metrics)

### Task 4.2: Update tech_stack Memory

**File:** `.serena/memories/tech_stack.md`
**Tool:** Serena read_memory, then Edit tool

**Updates Required:**
1. Update test suite information (35 → 33 tests)
2. Add service tier configuration note
3. Update performance metrics if significantly changed

**Implementation Steps:**
1. ✅ Use Sequential-Thinking to plan update
2. ✅ Use Serena read_memory to review current content
3. ✅ Use Edit tool to update relevant sections

### Task 4.3: Update ai_agent_instructions_oct_2025 Memory (if applicable)

**File:** `.serena/memories/ai_agent_instructions_oct_2025.md`
**Tool:** Serena read_memory, then Edit tool

**Check if update needed:**
1. ✅ Use Serena read_memory to check content
2. ✅ If references to test suite or service tier exist, update them
3. ✅ Otherwise, skip this subtask

---

## 🔄 PHASE 5: FINAL GIT COMMIT (ATOMIC WORKFLOW)

### Task 5.1: Pre-Commit Verification

**CRITICAL: DO ALL WORK BEFORE STAGING**

**Verification Checklist:**
- [ ] agent_service.py: service_tier changed to "default"
- [ ] test_cli_regression.sh: Updated to 33 tests with new structure
- [ ] Tests executed: 33/33 PASS (100% success rate)
- [ ] CLAUDE.md: Updated with new task summary and test count
- [ ] README.md: Updated test count (if applicable)
- [ ] Serena memories: Updated testing_procedures, tech_stack
- [ ] Test report: Generated and saved in test-reports/
- [ ] All tools used systematically: Sequential-Thinking ✓, Serena tools ✓

**Commands to Run:**
```bash
git status  # Review ALL changed/new files
git diff    # Review ALL changes
```

### Task 5.2: Stage Everything At Once

**CRITICAL: First time running git add**

**Command:**
```bash
git add -A
```

**Immediate Verification:**
```bash
git status  # Verify ALL files staged, NOTHING unstaged
```

**Expected Staged Files:**
- src/backend/services/agent_service.py
- test_cli_regression.sh
- CLAUDE.md
- README.md (if updated)
- .serena/memories/testing_procedures.md
- .serena/memories/tech_stack.md
- .serena/memories/ai_agent_instructions_oct_2025.md (if updated)
- test-reports/test_cli_regression_loop1_*.log (test report)
- TODO_task_plan.md (this file - mark as completed)

### Task 5.3: Commit Immediately

**CRITICAL: Commit within 60 seconds of staging**

**Commit Message Template:**
```bash
git commit -m "$(cat <<'EOF'
[CONFIG] Change service tier to default & restructure test suite to 33 tests

Service Tier Change:
- Change OpenAI service_tier from "flex" to "default" in agent_service.py
- Reason: Fix rate limiting issues with flex tier during prototyping
- Default tier provides better performance for development

Test Suite Restructuring (35 → 33 tests):
- SPY Test Sequence: 15 → 14 tests (Tests 1-14)
- NVDA Test Sequence: 15 → 14 tests (Tests 15-28)
- Multi-Ticker Test Sequence: 5 tests (Tests 29-33, GME replaces INTC)
- Reordered test sequences for better organization
- Changed from hardcoded dates to dynamic relative dates
- Improved test sustainability (no date updates needed)

Test Results:
- Total Tests: 33/33 PASSED ✅
- Success Rate: 100%
- Performance: [INSERT AVG RESPONSE TIME]s (EXCELLENT/GOOD)
- Test Report: test-reports/test_cli_regression_loop1_*.log

Documentation Updates:
- CLAUDE.md: Updated test count (35 → 33) and Last Completed Task Summary
- README.md: Updated test count references (if applicable)
- Serena memories: Updated testing_procedures, tech_stack

Files Changed:
- Modified: src/backend/services/agent_service.py (service_tier change)
- Modified: test_cli_regression.sh (33-test restructuring)
- Modified: CLAUDE.md, README.md (documentation)
- Modified: .serena/memories/*.md (memory updates)
- Added: test-reports/test_cli_regression_loop1_*.log (test evidence)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Note:** Replace `[INSERT AVG RESPONSE TIME]` with actual value from test results

### Task 5.4: Push Immediately

**Command:**
```bash
git push
```

**Verification:**
```bash
git log -1  # Verify commit message
git status  # Verify clean working tree
```

---

## ✅ COMPLETION CRITERIA

### All Tasks Must Be Complete:

- [x] **Planning Phase:** TODO_task_plan.md created ✅
- [ ] **Implementation Phase:**
  - [ ] Service tier changed to "default" in agent_service.py
  - [ ] Test suite restructured to 33 tests in test_cli_regression.sh
  - [ ] All code changes verified
- [ ] **Testing Phase:**
  - [ ] Tests executed: ./test_cli_regression.sh
  - [ ] Results: 33/33 PASS (100% success rate)
  - [ ] Test report generated and reviewed
  - [ ] Performance metrics acceptable
- [ ] **Documentation Phase:**
  - [ ] CLAUDE.md updated
  - [ ] README.md updated (if applicable)
  - [ ] All test count references updated
- [ ] **Serena Memory Phase:**
  - [ ] testing_procedures.md updated
  - [ ] tech_stack.md updated
  - [ ] Other relevant memories updated
- [ ] **Git Commit Phase:**
  - [ ] All work verified complete
  - [ ] All files staged at once
  - [ ] Atomic commit created
  - [ ] Changes pushed to remote

---

## 🚨 CRITICAL REMINDERS

### Tool Usage Requirements:

- ✅ **Sequential-Thinking:** Use at start of EVERY phase for systematic planning
- ✅ **Serena Tools:** Use for all code analysis, symbol manipulation, pattern searches
- ✅ **Standard Tools:** Use for file operations and editing
- ✅ **NEVER stop using tools** - continuous tool usage throughout entire implementation

### Testing Requirements:

- 🔴 **MANDATORY:** Run tests BEFORE documentation updates
- 🔴 **MANDATORY:** Achieve 100% pass rate (33/33 PASS)
- 🔴 **MANDATORY:** Show test results to user
- 🔴 **Code without test execution = Code NOT implemented**

### Git Commit Requirements:

- 🔴 **NEVER stage files early** - do ALL work first
- 🔴 **Stage everything AT ONCE** - single `git add -A` command
- 🔴 **Commit IMMEDIATELY** - within 60 seconds of staging
- 🔴 **Push IMMEDIATELY** - right after commit

---

## 📊 ESTIMATED EFFORT

- **Service Tier Change:** 5 minutes (simple one-line change)
- **Test Suite Restructuring:** 15 minutes (array replacements + validation)
- **CLI Testing:** 10-15 minutes (test execution + verification)
- **Documentation Updates:** 10 minutes (CLAUDE.md, README.md)
- **Serena Memory Updates:** 5 minutes (testing_procedures, tech_stack)
- **Git Commit:** 5 minutes (verification, staging, commit, push)

**Total Estimated Time:** 50-55 minutes

---

## 🎯 SUCCESS DEFINITION

**Task is complete when:**
1. ✅ Service tier is "default" in agent_service.py
2. ✅ Test suite has 33 tests (not 35) with new structure
3. ✅ All 33 tests pass (100% success rate)
4. ✅ Documentation updated with new test count and task summary
5. ✅ Serena memories updated with latest information
6. ✅ Atomic git commit created and pushed
7. ✅ User shown test evidence (33/33 PASS, test report path)

**Task is NOT complete until ALL criteria above are met.**

---

**END OF TODO_task_plan.md**
