# TODO Task Plan - Testing Migration & Playwright Removal

**Created:** October 7, 2025 Evening
**Task:** Migrate ALL testing to test_cli_regression.sh ONLY and remove ALL Playwright references
**Status:** RESEARCH COMPLETE - Ready for Implementation

---

## 🔍 AUDIT FINDINGS SUMMARY

**Total Files to Modify:** 13 files
**Critical Issues Found:** 3 contradictory/erroneous edits by user
**Playwright References Found:** 40+ references across 10 files
**Test Reports Cleanup:** ✅ Complete (30 old reports deleted, 4 new .log files remain)

---

## 📋 IMPLEMENTATION PLAN (9 Phases)

### ⚠️ CRITICAL: USE SEQUENTIAL-THINKING & SERENA TOOLS THROUGHOUT ALL PHASES

---

### PHASE 1: FIX CRITICAL ERRORS IN USER'S EDITS

**🔴 CRITICAL: Fix contradictory edits made by user**

#### Task 1.1: Delete CLI_test_regression.sh (OLD 27-test script)
- **Tool**: Bash
- **Command**: `rm -f CLI_test_regression.sh`
- **Reason**: This is the OLD 27-test script that should be deleted, NOT marked as "source of truth"
- **Validation**: Verify file no longer exists

#### Task 1.2: Fix project_architecture.md Line 335-336
- **Tool**: Serena find_symbol or Edit
- **Find**: `#### Legacy Test Suite: test_cli_regression.sh (27 tests)`
- **Replace**: `#### Legacy Test Suite: CLI_test_regression.sh (27 tests)`
- **Reason**: Wrong filename - should say CLI_test_regression.sh for legacy

#### Task 1.3: Fix project_architecture.md Line 572-573
- **Tool**: Serena find_symbol or Edit
- **Find**: `- Legacy: test_cli_regression.sh (27 tests, deprecated)`
- **Replace**: `- Legacy: CLI_test_regression.sh (27 tests, deprecated, DELETED)`
- **Reason**: Wrong filename and needs to note it's deleted

#### Task 1.4: Fix ai_agent_instructions_oct_2025.md Line 285-286
- **Tool**: Serena find_symbol or Edit
- **Find**: `- \`test_cli_regression.sh\` - Legacy 27-test suite (deprecated)`
- **Replace**: `- \`CLI_test_regression.sh\` - Legacy 27-test suite (deprecated, DELETED)`
- **Reason**: Wrong filename and needs to note it's deleted

---

### PHASE 2: REMOVE PLAYWRIGHT REFERENCES FROM CLAUDE.md

**🎯 Target:** 4 references in CLAUDE.md

#### Task 2.1: Update Testing section (Line ~395)
- **Tool**: Serena search_for_pattern + Edit
- **Find**: `- **Testing**: Playwright E2E test suite`
- **Replace**: `- **Testing**: CLI regression test suite (test_cli_regression.sh - 35 tests)`
- **Location**: Architecture section

#### Task 2.2: Remove Playwright comment (Line ~408)
- **Tool**: Serena search_for_pattern + Edit
- **Find**: `# Testing with Playwright MCP Tools only - see \`/tests/playwright/mcp_test_script_basic.md\``
- **Replace**: `# Testing: Run ./test_cli_regression.sh to execute 35-test suite`
- **Location**: Development section

#### Task 2.3: Update project structure (Line ~428)
- **Tool**: Serena search_for_pattern + Edit
- **Find**: `tests/playwright/        # E2E test suite`
- **Delete**: This entire line from project structure
- **Location**: Project Structure section

---

### PHASE 3: REMOVE PLAYWRIGHT REFERENCES FROM README.md

**🎯 Target:** 9 references in README.md + severely outdated content

#### Task 3.1: Fix start-app.sh BROKEN status (Lines 94-95)
- **Tool**: Edit
- **Find**:
```
# Option 2: Main startup script (CURRENTLY BROKEN - DO NOT USE)
# ./start-app.sh  # ⚠️ BROKEN: Script gets stuck and blocks execution
```
- **Replace**:
```
# Option 2: Main startup script (NOW WORKING - FIXED)
./start-app.sh  # ✅ WORKING: Script now exits cleanly with timeout
```
- **Reason**: Script was fixed in recent commit!

#### Task 3.2: Delete "start-app.sh (CURRENTLY BROKEN)" section (Lines 106-111)
- **Tool**: Edit
- **Delete entire section**:
```
### start-app.sh (CURRENTLY BROKEN - DO NOT USE)

- **Status**: ❌ BROKEN - Script gets stuck and blocks execution
- **Issue**: Cannot proceed to sleep 15 or Playwright testing
- **Action**: Keep script file but do not use until fixed
- **Alternative**: Use start-app-xterm.sh instead
```
- **Reason**: Outdated - script is now working

#### Task 3.3: Fix Polygon MCP reference (Line 253)
- **Tool**: Edit
- **Find**: `Polygon.io MCP integration v0.4.1`
- **Replace**: `Direct Polygon Python API integration`
- **Reason**: MCP was removed in October 2025!

#### Task 3.4: Update Testing line (Line 257)
- **Tool**: Edit
- **Find**: `- **Testing**: Playwright E2E test suite with standardized quick response prompts`
- **Replace**: `- **Testing**: CLI regression test suite (test_cli_regression.sh - 35 comprehensive tests)`

#### Task 3.5: Remove Playwright comment (Line 272)
- **Tool**: Edit
- **Find**: `# Testing with Playwright MCP Tools only - see \`/tests/playwright/mcp_test_script_basic.md\``
- **Replace**: `# Testing: Run ./test_cli_regression.sh (35 tests, persistent session)`

#### Task 3.6: Update project structure (Line 292)
- **Tool**: Edit
- **Find**: `tests/playwright/        # E2E test suite`
- **Delete**: This entire line
- **Location**: Project Structure section

#### Task 3.7: Update performance stats (Lines 32-37)
- **Tool**: Edit
- **Find**: "10-Run Performance Baseline" section with "160/160 tests"
- **Replace**: With latest test results from test_cli_regression.sh (35 tests, 11.62s avg, 100% pass rate)
- **Use data from**: test-reports/test_cli_regression_loop1_2025-10-07_20-30.log

#### Task 3.8: Add test_cli_regression.sh documentation
- **Tool**: Edit
- **Location**: After "Development" section
- **Add new section**:
```markdown
### Testing

**Primary Test Suite:** `test_cli_regression.sh` (35 comprehensive tests)

**Test Coverage:**
- SPY test sequence (15 tests): Market status, prices, TA indicators, options, OHLC
- NVDA test sequence (15 tests): Same pattern as SPY
- Multi-ticker WDC/AMD/INTC (5 tests): Parallel call validation

**Features:**
- Persistent session (all 35 tests in single CLI session)
- Chat history analysis validation
- Parallel tool call verification
- OHLC display validation
- Support/Resistance redundant call detection

**Latest Results:**
- Total: 35/35 PASSED ✅
- Success Rate: 100%
- Average: 11.62s per query (EXCELLENT)
- Range: 2.188s - 31.599s

**Run tests:**
```bash
./test_cli_regression.sh
```
```

---

### PHASE 4: REMOVE PLAYWRIGHT REFERENCES FROM AGENTS.md

**🎯 Target:** 4 references in AGENTS.md

#### Task 4.1: Update Testing section
- **Tool**: Edit
- **Find**: `- **Testing**: Playwright E2E test suite`
- **Replace**: `- **Testing**: CLI regression test suite (test_cli_regression.sh - 35 tests)`

#### Task 4.2: Remove Playwright comment
- **Tool**: Edit
- **Find**: `# Testing with Playwright MCP Tools only`
- **Replace**: `# Testing: Run ./test_cli_regression.sh`

#### Task 4.3: Update project structure
- **Tool**: Edit
- **Find**: `tests/playwright/        # E2E test suite`
- **Delete**: This entire line

---

### PHASE 5: HANDLE test_prompts.md (20+ Playwright references)

**🎯 Decision Point: Delete entire file OR rewrite**

#### Task 5.1: Sequential-Thinking Analysis
- **Tool**: Sequential-Thinking
- **Analyze**: Is test_prompts.md still useful if rewritten for CLI testing?
- **Decision**: Recommend DELETION since we have comprehensive test_cli_regression.sh documentation

#### Task 5.2: Delete test_prompts.md
- **Tool**: Bash
- **Command**: `rm -f test_prompts.md`
- **Reason**: Entire file is about Playwright GUI testing (deprecated)
- **Alternative**: If user wants CLI testing prompts, create new file

---

### PHASE 6: REMOVE PLAYWRIGHT REFERENCES FROM SMALLER FILES

#### Task 6.1: Fix START_SCRIPT_README.md
- **Tool**: Edit
- **Find**: "Status: ✅ FULLY TESTED - 5/5 successful tests with Playwright validation"
- **Replace**: "Status: ✅ FULLY TESTED - Both startup scripts working correctly"

#### Task 6.2: Fix .claude/commands/new_task.md
- **Tool**: Edit
- **Find**: "Playwright Tools: Use for Testing with Browser automation"
- **Delete**: This entire line or replace with "CLI Testing: Use test_cli_regression.sh for comprehensive testing"

---

### PHASE 7: REMOVE PLAYWRIGHT REFERENCES FROM SERENA MEMORIES

#### Task 7.1: Fix project_architecture.md
- **Tool**: Serena find_symbol + replace_symbol_body OR Edit
- **Find section**: "### E2E Testing (Playwright)"
- **Delete entire section**: Lines 350-353
- **OR Replace with**:
```markdown
### CLI Regression Testing

**Status:** Primary test suite
**Location:** `test_cli_regression.sh`
**Test Count:** 35 comprehensive tests
**Latest Results:** 35/35 PASSED (100%), 11.62s avg (EXCELLENT)
```

#### Task 7.2: Fix testing_procedures.md
- **Tool**: Edit
- **Find**: "9. **End-to-End Web Testing** - Playwright tests for full web flow"
- **Replace**: "9. **CLI Regression Testing** - Comprehensive test suite with 35 tests (test_cli_regression.sh)"

#### Task 7.3: Fix tech_stack.md
- **Tool**: Edit
- **Find**: "Testing: Playwright E2E, CLI regression tests"
- **Replace**: "Testing: CLI regression test suite (test_cli_regression.sh - 35 tests, 100% pass rate)"

---

### PHASE 8: VALIDATION & TESTING

**🔴 MANDATORY: Must run tests BEFORE claiming completion**

#### Task 8.1: Run test_cli_regression.sh
- **Tool**: Bash
- **Command**: `./test_cli_regression.sh`
- **Expected**: 35/35 tests PASS
- **Validation**:
  - 100% success rate
  - Test report generated in test-reports/
  - No errors or failures
  - Session persistence verified

#### Task 8.2: Verify all files using Sequential-Thinking
- **Tool**: Sequential-Thinking
- **Analyze**: Review ALL changes made
- **Check**: No remaining Playwright references
- **Check**: No remaining CLI_test_regression.sh references
- **Check**: All Serena memories updated correctly

#### Task 8.3: Search for remaining references
- **Tool**: Serena search_for_pattern
- **Pattern 1**: `Playwright|playwright`
- **Expected**: Only references in new_research_details.md (task description) and test-reports/
- **Pattern 2**: `CLI_test_regression`
- **Expected**: Only in new_research_details.md (task description)

---

### PHASE 9: FINAL GIT COMMIT

**🔴 CRITICAL: Follow proper atomic commit workflow**

#### Task 9.1: Verify everything complete
- **Tool**: Bash
- **Command**: `git status` then `git diff`
- **Check**: ALL work done, ALL files present

#### Task 9.2: Stage ALL files at once
- **Tool**: Bash
- **Command**: `git add -A`
- **Timing**: ONLY run this AFTER all work complete

#### Task 9.3: Verify staging
- **Tool**: Bash
- **Command**: `git status`
- **Check**: ALL files staged, NOTHING unstaged

#### Task 9.4: Commit immediately
- **Tool**: Bash
- **Command**:
```bash
git commit -m "$(cat <<'EOF'
[CLEANUP] Migrate to test_cli_regression.sh and remove Playwright references

Primary Changes:
- Deleted CLI_test_regression.sh (old 27-test script)
- Fixed Serena memory errors (project_architecture.md, ai_agent_instructions_oct_2025.md)
- Removed ALL Playwright references (40+ references across 10 files)
- Updated README.md with latest test results and fixed outdated content
- Updated CLAUDE.md, AGENTS.md with new testing information
- Deleted test_prompts.md (entire file was Playwright-specific)
- test_cli_regression.sh is now ONLY testing script (35 tests)

Files Modified:
- ✅ Deleted: CLI_test_regression.sh
- ✅ Fixed: .serena/memories/project_architecture.md (lines 335-336, 572-573)
- ✅ Fixed: .serena/memories/ai_agent_instructions_oct_2025.md (lines 285-286)
- ✅ Updated: README.md (removed Playwright, fixed outdated content)
- ✅ Updated: CLAUDE.md (removed Playwright references)
- ✅ Updated: AGENTS.md (removed Playwright references)
- ✅ Deleted: test_prompts.md (Playwright-specific file)
- ✅ Updated: START_SCRIPT_README.md (removed Playwright)
- ✅ Updated: .claude/commands/new_task.md (removed Playwright)
- ✅ Updated: .serena/memories/tech_stack.md (removed Playwright)
- ✅ Updated: .serena/memories/testing_procedures.md (removed Playwright)

Validation:
- ✅ Test Suite Run: 35/35 PASSED (100%)
- ✅ No remaining Playwright references (except task description)
- ✅ No remaining CLI_test_regression.sh references (except task description)
- ✅ All Serena memories updated correctly
- ✅ README.md now accurate and up-to-date

Testing Results:
- Total: 35/35 PASSED
- Success Rate: 100%
- Average: 11.62s (EXCELLENT)
- Test Report: test-reports/test_cli_regression_loop1_[timestamp].log

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### Task 9.5: Push immediately
- **Tool**: Bash
- **Command**: `git push`

---

## 📊 TASK SUMMARY

**Total Phases:** 9
**Total Tasks:** 40+
**Critical Fixes:** 3 user edit errors
**Playwright References:** 40+ to remove
**Files to Modify:** 13
**Files to Delete:** 2 (CLI_test_regression.sh, test_prompts.md)

---

## 🛠️ TOOL USAGE REQUIREMENTS

**MANDATORY TOOLS TO USE THROUGHOUT:**

1. **Sequential-Thinking**: START every phase, use for complex reasoning
2. **Serena Tools**: Use for symbol searches, pattern matching, code analysis
3. **Standard Read/Write/Edit**: Use for file modifications
4. **Bash**: Use for file operations, git commands, test execution
5. **TodoWrite**: Track progress through all phases

**CRITICAL RULES:**
- ✅ Use tools MULTIPLE TIMES as needed
- ✅ Use tools in ANY ORDER based on task needs
- ✅ CONTINUOUS tool usage from start to finish
- ✅ NO rigid sequencing - only logical tool usage
- ❌ NEVER stop using tools until task complete

---

## ✅ SUCCESS CRITERIA

**Task is complete ONLY when:**

1. ✅ CLI_test_regression.sh deleted
2. ✅ All 3 user edit errors fixed
3. ✅ ALL Playwright references removed (40+ references)
4. ✅ README.md updated and accurate
5. ✅ All Serena memories updated correctly
6. ✅ Test suite executed (35/35 PASS required)
7. ✅ No remaining references found in validation search
8. ✅ ALL files committed and pushed

**If ANY of these criteria are not met, the task is INCOMPLETE.**

---

## 🚨 CRITICAL CHECKPOINTS

**Before Phase 8 (Testing):**
- [ ] All Playwright references removed
- [ ] All user edit errors fixed
- [ ] CLI_test_regression.sh deleted
- [ ] README.md fully updated

**Before Phase 9 (Commit):**
- [ ] Test suite run (35/35 PASS)
- [ ] Validation searches complete
- [ ] All changes verified

**After Commit:**
- [ ] Changes pushed to remote
- [ ] All uncommitted changes cleared

---

**END OF TODO TASK PLAN**
