# TODO Task Plan: Weekly/Monthly Interval Fix Implementation

**Date**: 2025-10-15
**Status**: Planning Complete - Ready for Implementation
**Based on**: research_task_plan.md

---

## 📋 Implementation Checklist

### ✅ Phase 1: Research (COMPLETED)
- [x] Use Sequential-Thinking for systematic root cause analysis
- [x] Locate tradier_tools.py using Serena find_file
- [x] Read get_stock_price_history() function using Serena find_symbol
- [x] Analyze Tradier API response structures
- [x] Identify bug: dict vs array handling for weekly/monthly intervals
- [x] Locate RULE #12 in agent_service.py using Serena search_for_pattern
- [x] Create comprehensive research_task_plan.md

### 🔄 Phase 2: Planning (IN PROGRESS)
- [x] Delete old TODO_task_plan.md
- [ ] Create new TODO_task_plan.md with granular implementation steps
- [ ] Define exact code changes for tradier_tools.py
- [ ] Define exact code changes for agent_service.py
- [ ] Plan testing strategy with 6 manual prompts
- [ ] Plan full 39-test regression suite execution

### 🚀 Phase 3: Implementation (PENDING)

#### **Task 3.1: Fix tradier_tools.py (Handle dict vs array)**

**Location**: src/backend/tools/tradier_tools.py, line 360

**Current Code** (lines 358-362):
```python
# Parse response
data = response.json()
history_data = data.get("history", {})
bars_data = history_data.get("day", [])

# Check if API returned data
if not bars_data:
```

**Action**: Use Serena replace_lines to update lines 360-362

**New Code**:
```python
bars_data = history_data.get("day", [])
# Handle weekly/monthly: single dict vs daily: array of dicts
if isinstance(bars_data, dict):
    bars_data = [bars_data]

# Check if API returned data
if not bars_data:
```

**Serena Command**:
```python
mcp__serena__replace_lines(
    relative_path="src/backend/tools/tradier_tools.py",
    start_line=360,
    end_line=362,
    new_content="        bars_data = history_data.get(\"day\", [])\n        # Handle weekly/monthly: single dict vs daily: array of dicts\n        if isinstance(bars_data, dict):\n            bars_data = [bars_data]\n\n        # Check if API returned data\n        if not bars_data:"
)
```

**Validation**:
- [ ] Code compiles without syntax errors
- [ ] isinstance() check correctly identifies dict type
- [ ] Single dict wrapped in list before loop
- [ ] Array handling remains unchanged

#### **Task 3.2: Update agent_service.py (Add RULE #13)**

**Location**: src/backend/services/agent_service.py, after line 461

**Context**: Insert after RULE #12 ends, before emoji formatting section (line 462)

**Action**: Use Serena insert_at_line to add new content after line 461

**New Content** (RULE #13):
```python

RULE #13: ERROR TRANSPARENCY - VERBATIM ERROR REPORTING
- 🔴 **CRITICAL**: When tool calls fail, you MUST report the EXACT verbatim error message received
- 🔴 **NEVER** use vague phrases like "API Issue", "data unavailable", or "failed to retrieve" without specifics
- 🔴 **ALWAYS** include the complete error message in your response for debugging purposes
- ✅ **CORRECT EXAMPLE**: "API Error: Failed to retrieve historical data for SPY: 'str' object has no attribute 'get'"
- ❌ **WRONG EXAMPLE**: "There was an API issue" or "Data unavailable"
- ✅ **FORMAT**: When reporting errors, use exact error JSON or message returned by the tool
- ✅ **TRANSPARENCY**: Users need exact error messages to diagnose and fix problems quickly

**WHY THIS RULE EXISTS:**
- Vague error messages waste time chasing wrong issues
- Exact errors enable immediate root cause identification
- Users cannot fix problems without knowing the actual error
- "API Issue" or "data unavailable" provides zero actionable information

**EXAMPLES OF CORRECT ERROR REPORTING:**

1. Tool returns: `{"error": "Unexpected error", "message": "Failed to retrieve: 'str' object has no attribute 'get'", "ticker": "SPY"}`
   ✅ CORRECT: "The API returned an error: Failed to retrieve historical data for SPY: 'str' object has no attribute 'get'"
   ❌ WRONG: "There was an API issue retrieving SPY data"

2. Tool returns: `{"error": "Timeout", "message": "Request timed out after 10s", "ticker": "NVDA"}`
   ✅ CORRECT: "API Timeout Error: Request timed out after 10s for NVDA"
   ❌ WRONG: "Unable to retrieve NVDA data"

3. Tool returns: `{"error": "No data", "message": "No historical data available for INVALID from 2025-01-01 to 2025-01-31", "ticker": "INVALID"}`
   ✅ CORRECT: "No historical data available for INVALID from 2025-01-01 to 2025-01-31. Verify ticker symbol and date range."
   ❌ WRONG: "Data unavailable for the requested period"

```

**Serena Command**:
```python
mcp__serena__insert_at_line(
    relative_path="src/backend/services/agent_service.py",
    line_number=461,
    content="[RULE #13 content as shown above]"
)
```

**Validation**:
- [ ] RULE #13 inserted after RULE #12
- [ ] Formatting consistent with other rules
- [ ] Examples clear and actionable
- [ ] Agent instructions updated successfully

#### **Task 3.3: Verify Code Changes**

**Using Serena Tools**:

1. **Read tradier_tools.py** to verify fix:
```python
mcp__serena__find_symbol(
    name_path="get_stock_price_history",
    relative_path="src/backend/tools/tradier_tools.py",
    include_body=True
)
```
   - [ ] Verify isinstance() check present at line ~360
   - [ ] Verify bars_data wrapped in list when dict

2. **Search agent_service.py** to verify RULE #13:
```python
mcp__serena__search_for_pattern(
    substring_pattern="RULE #13:",
    relative_path="src/backend/services/agent_service.py",
    context_lines_after=5
)
```
   - [ ] Verify RULE #13 present after RULE #12
   - [ ] Verify error transparency instructions clear

### 🧪 Phase 4: Testing (PENDING)

#### **Task 4.1: Manual CLI Testing (6 Prompts)**

**Setup**:
```bash
# Start backend CLI
uv run src/backend/main.py
```

**Test Prompts** (execute in order, document results):

1. [ ] `"Last week's Performance OHLC: $SPY"`
   - Expected: Weekly interval, OHLC data returned
   - Verify: No "'str' object" error
   - Tool call: `get_stock_price_history(ticker='SPY', interval='weekly', ...)`

2. [ ] `"Stock Price Performance the past month: $SPY"`
   - Expected: Monthly interval, OHLC data returned
   - Verify: No "'str' object" error
   - Tool call: `get_stock_price_history(ticker='SPY', interval='monthly', ...)`

3. [ ] `"Last week's Performance OHLC: $NVDA"`
   - Expected: Weekly interval, OHLC data returned
   - Verify: Consistent behavior with SPY test

4. [ ] `"Stock Price Performance the past month: $NVDA"`
   - Expected: Monthly interval, OHLC data returned
   - Verify: Consistent behavior with SPY test

5. [ ] `"Last week's Performance OHLC: $WDC, $AMD, $SOUN"`
   - Expected: 3 parallel weekly calls (RULE #12)
   - Verify: Each ticker gets separate tool call
   - Tool calls: 3x `get_stock_price_history(ticker='WDC|AMD|SOUN', interval='weekly', ...)`

6. [ ] `"Stock Price Performance the past month: $WDC, $AMD, $SOUN"`
   - Expected: 3 parallel monthly calls (RULE #12)
   - Verify: Each ticker gets separate tool call
   - Tool calls: 3x `get_stock_price_history(ticker='WDC|AMD|SOUN', interval='monthly', ...)`

**Success Criteria**:
- ✅ All 6 prompts return data successfully (no errors)
- ✅ Weekly/monthly intervals selected correctly
- ✅ Multi-ticker prompts use parallel calls
- ✅ No "'str' object has no attribute 'get'" errors
- ✅ Response time < 15s per prompt

**Documentation**:
- [ ] Save all 6 responses to file: `test-results/manual_validation_6_prompts_YYYY-MM-DD_HH-MM.log`
- [ ] Note any unexpected behavior or errors
- [ ] Record response times for each prompt

#### **Task 4.2: Full Regression Suite (39 Tests)**

**Execute Test Suite**:
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Monitor Execution**:
- [ ] Script starts successfully
- [ ] All 39 prompts execute
- [ ] Script reports "X/39 COMPLETED"
- [ ] Test report generated in test-reports/

**Expected Output**:
```
═══════════════════════════════════════════════════
📊 PERFORMANCE SUMMARY - Loop 1
═══════════════════════════════════════════════════
✅ Tests Completed: 39/39 (100.0%)
⏱️  Average Response Time: ~8-10s
📈 Performance Rating: EXCELLENT
🔍 Detailed report: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log
═══════════════════════════════════════════════════
```

#### **Task 4.3: Phase 2 Grep-Based Verification (MANDATORY)**

**Phase 2a: ERROR DETECTION (Run grep commands)**

```bash
# Command 1: Find all errors/failures
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log
```
- [ ] Run command and save output
- [ ] Count total error lines found

```bash
# Command 2: Count 'data unavailable' errors
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log
```
- [ ] Run command and record count
- [ ] Expected: 0 (all errors fixed)

```bash
# Command 3: Count completed tests
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```
- [ ] Run command and record count
- [ ] Expected: 39 (100% completion)

**Phase 2b: DOCUMENT FAILURES (If any errors found)**

If grep commands found errors, create evidence table:

| Test # | Test Name | Line # | Error Message | Tool Call |
|--------|-----------|--------|---------------|-----------|
| X | TestName | NNN | Exact error message | tool(params) |

- [ ] Grep output shows errors → Create failure table
- [ ] Grep output shows 0 errors → Document "0 failures found"

**Phase 2c: VERIFY RESPONSE CORRECTNESS (For passing tests)**

For tests without errors in Phase 2a, verify:
- [ ] Response addresses the prompt query
- [ ] Correct ticker symbols used
- [ ] Appropriate tool calls made
- [ ] Data formatting matches expected format
- [ ] No hallucinated data
- [ ] Response is complete (not truncated)

**Phase 2d: FINAL VERIFICATION (Checkpoint Questions)**

Answer ALL checkpoint questions with evidence:

1. ✅ Did you RUN the 3 mandatory grep commands in Phase 2a?
   - [ ] YES - Show grep outputs below

2. ✅ Did you DOCUMENT all failures found?
   - [ ] YES - Provide failure table OR confirm "0 failures found"

3. ✅ Failure count from `grep -c "data unavailable"`:
   - [ ] Count: _____ failures

4. ✅ Tests that generated responses:
   - [ ] Count: ___/39 COMPLETED

5. ✅ Tests that PASSED verification (no errors):
   - [ ] Count: ___/39 PASSED

**🔴 CANNOT PROCEED WITHOUT:**
- Running and showing all 3 grep command outputs
- Documenting failures OR confirming 0 failures
- Answering all 5 checkpoint questions with evidence

#### **Task 4.4: Analyze Test Results**

**Compare with Previous Results**:

| Metric | Before Fix | After Fix | Improvement |
|--------|------------|-----------|-------------|
| "'str' object" errors | X | 0 | 100% fixed |
| Weekend errors | 0 | 0 | N/A (already fixed) |
| Total errors | X | 0 | 100% fixed |
| Completion rate | 39/39 | 39/39 | Maintained |
| Pass rate | 36/39 | 39/39 | +3 tests |
| Avg response time | ~9s | ~8-10s | Maintained |

- [ ] Document metrics comparison
- [ ] Verify 100% pass rate achieved
- [ ] Confirm performance maintained

### 📝 Phase 5: Documentation (PENDING)

#### **Task 5.1: Update CLAUDE.md**

**Section to Update**: "Last Completed Task Summary" (lines 436-513)

**Action**: Replace entire section with new task summary

**New Content Structure**:
```markdown
## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
[INTERVAL-FIX] Weekly/Monthly Interval Bug Fix + Error Transparency Rule

**Problem:** Weekly/monthly get_stock_price_history() calls failing with "'str' object has no attribute 'get'" error
**Root Cause:** Tradier API returns dict for weekly/monthly (not array like daily), code didn't handle type difference
**Solution:** isinstance() check to wrap single dict in list + RULE #13 for error transparency

**Code Changes:**
1. **tradier_tools.py** (line 360-362):
   - Added isinstance() check after getting bars_data
   - Wraps single dict in list for weekly/monthly intervals
   - Normalizes data structure before loop

2. **agent_service.py** (after line 461):
   - Added RULE #13: ERROR TRANSPARENCY - VERBATIM ERROR REPORTING
   - Enforces exact error message reporting (no vague "API Issue" responses)
   - Provides examples of correct vs wrong error reporting

**Test Results:**
[Include Phase 2 grep verification evidence here]

**Success Metrics:**
- ✅ Weekly/monthly intervals: 100% FIXED
- ✅ "'str' object" errors: X→0 (100% fix rate)
- ✅ Tests passing: 36/39→39/39 (100% pass rate)
- ✅ 39/39 tests COMPLETED
- ✅ Average response time: ~Xs (EXCELLENT rating)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
<!-- LAST_COMPLETED_TASK_END -->
```

**Checklist**:
- [ ] Use Edit tool to replace lines 438-513 in CLAUDE.md
- [ ] Include actual test metrics from Phase 4
- [ ] Include grep verification evidence
- [ ] Verify markdown formatting

#### **Task 5.2: Update Serena Memories**

**Memory to Update**: `lingering_interval_selection_issue.md`

**Action**: Update or replace with resolution

**New Content**: Document that the issue was a CODE BUG not a model issue, now resolved

**Checklist**:
- [ ] Use `mcp__serena__write_memory` to update memory
- [ ] Explain that "'str' object" error was Tradier API structure issue
- [ ] Note that isinstance() check resolves the problem
- [ ] Mark issue as RESOLVED

**Optional**: Create new memory `tradier_api_response_structures.md`
- Document dict vs array behavior for different intervals
- Provide reference for future API integration work

#### **Task 5.3: Update tech_stack.md (if needed)**

**Check if updates needed**:
- [ ] Review tech_stack.md for accuracy
- [ ] Update if any technology versions changed
- [ ] Update if any new tools/patterns documented

### 🔄 Phase 6: Git Commit (PENDING)

#### **Task 6.1: Pre-Commit Verification**

**Before staging anything, verify ALL work complete**:

- [ ] Code changes: tradier_tools.py fixed
- [ ] Code changes: agent_service.py RULE #13 added
- [ ] Testing: 6 manual CLI prompts executed
- [ ] Testing: Full 39-test suite executed
- [ ] Testing: Phase 2 grep verification completed
- [ ] Documentation: CLAUDE.md updated
- [ ] Documentation: Serena memories updated
- [ ] Test reports: Generated and saved

**🚨 DO NOT STAGE FILES YET - All work must be complete first!**

#### **Task 6.2: Review All Changes**

```bash
# Review ALL changes (DO NOT stage yet)
git status
git diff
git diff --staged  # Should show nothing yet
```

**Checklist**:
- [ ] Review all modified files listed in git status
- [ ] Review all changes in git diff
- [ ] Verify no unintended changes
- [ ] Verify all intended changes present
- [ ] Confirm test reports exist in test-reports/

#### **Task 6.3: Stage Everything at Once**

**🔴 CRITICAL: This is the FIRST and ONLY time you run git add**

```bash
# Stage ALL files in ONE command
git add -A
```

- [ ] Executed: `git add -A`
- [ ] This is the FIRST time running git add
- [ ] All related files staged together

#### **Task 6.4: Verify Staging**

```bash
# Verify ALL files staged, NOTHING unstaged
git status
```

**Expected Output**: All files should be "Changes to be committed"

- [ ] Verify all modified files staged
- [ ] Verify test reports staged
- [ ] Verify documentation updates staged
- [ ] Verify NO files in "Changes not staged for commit"
- [ ] If anything missing: `git add [missing-file]`

#### **Task 6.5: Commit Immediately**

**🔴 CRITICAL: Commit within 60 seconds of staging**

```bash
git commit -m "$(cat <<'EOF'
[INTERVAL-FIX] Weekly/Monthly Interval Bug Fix + Error Transparency Rule

**Problem:** Weekly/monthly get_stock_price_history() calls failing with "'str' object has no attribute 'get'" error
**Root Cause:** Tradier API returns dict for weekly/monthly (not array like daily), code didn't handle type difference

**Solution:**
1. tradier_tools.py (line 360-362): Added isinstance() check to wrap dict in list
2. agent_service.py (after line 461): Added RULE #13 for verbatim error reporting

**Code Changes:**
- src/backend/tools/tradier_tools.py: isinstance() check for dict vs array handling
- src/backend/services/agent_service.py: RULE #13 ERROR TRANSPARENCY with examples

**Test Results:**
- 6 manual CLI prompts: 6/6 PASS (weekly/monthly with single/multi-ticker)
- Full regression suite: 39/39 COMPLETED, 39/39 PASS (100% pass rate)
- Phase 2 grep verification: 0 "'str' object" errors, 0 "data unavailable" errors
- Average response time: ~Xs (EXCELLENT rating)

**Documentation Updates:**
- CLAUDE.md: Updated Last Completed Task Summary
- Serena memories: Updated lingering_interval_selection_issue.md
- Test reports: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log

**Success Metrics:**
- Weekly/monthly intervals: 100% FIXED (0 errors)
- Pass rate improvement: 36/39→39/39 (+3 tests, 100% pass rate)
- Error transparency: RULE #13 enforces exact error messages

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

- [ ] Executed commit command
- [ ] Commit succeeded
- [ ] Within 60 seconds of staging

#### **Task 6.6: Push Immediately**

```bash
git push
```

- [ ] Executed: `git push`
- [ ] Push succeeded
- [ ] Changes now in remote repository

---

## ✅ Task Completion Criteria

**Phase 3: Implementation**
- ✅ tradier_tools.py fixed with isinstance() check
- ✅ agent_service.py updated with RULE #13
- ✅ Code changes verified with Serena tools

**Phase 4: Testing**
- ✅ 6 manual CLI prompts: 6/6 PASS
- ✅ Full 39-test suite: 39/39 COMPLETED
- ✅ Phase 2 grep verification: All 3 commands executed with evidence
- ✅ Checkpoint questions answered with proof
- ✅ 100% pass rate achieved

**Phase 5: Documentation**
- ✅ CLAUDE.md Last Completed Task Summary updated
- ✅ Serena memories updated
- ✅ Test reports saved and documented

**Phase 6: Git Commit**
- ✅ All work completed before staging
- ✅ All changes staged at once with `git add -A`
- ✅ Atomic commit created with descriptive message
- ✅ Changes pushed to remote repository

---

## 🎯 Success Metrics Target

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| "'str' object" errors | 0 | ___ | ⏳ |
| Weekend errors | 0 | ___ | ⏳ |
| Total errors | 0 | ___ | ⏳ |
| Completion rate | 39/39 | ___/39 | ⏳ |
| Pass rate | 39/39 (100%) | ___/39 | ⏳ |
| Avg response time | < 10s | ___s | ⏳ |
| Manual CLI prompts | 6/6 PASS | ___/6 | ⏳ |

---

## 🔧 Tools Required

**Serena Tools** (Primary):
- `mcp__serena__replace_lines` - Fix tradier_tools.py
- `mcp__serena__insert_at_line` - Add RULE #13 to agent_service.py
- `mcp__serena__find_symbol` - Verify code changes
- `mcp__serena__search_for_pattern` - Verify RULE #13 placement
- `mcp__serena__write_memory` - Update memories

**Standard Tools** (Fallback):
- `Edit` - Update CLAUDE.md (line-based edit for markdown)
- `Bash` - Execute tests, run grep commands, git operations

**Sequential-Thinking Tools**:
- Use throughout implementation for complex decisions
- Use before each major phase for planning
- Use during verification for comprehensive checks

---

**Status**: Ready for Phase 3 Implementation
**Next Action**: Begin Task 3.1 - Fix tradier_tools.py
