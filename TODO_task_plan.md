# TODO Task Plan: Fix Options Chain 10-Strike Limit & Test Script Path Violation

## Task Summary

Fix two critical issues:
1. **CRITICAL BUG**: Options chain tools returning 174 total strikes instead of 10 per chain (flooding messages)
2. **VIOLATION**: Test script writes logs to system /tmp instead of project tmp/ folder

## Evidence & Analysis

### Issue #1: Options Chain Flooding (CRITICAL)
**Evidence**: `/tmp/cli_output_loop1_2025-10-09_10-26.log` shows:
- **174 total option strikes** found in the log file
- SPY Call Options Chain shows 24+ strikes ($670-$694+) instead of 10
- API parameter "limit": 10 is being ignored

**Root Cause**:
```python
for option in client.list_snapshot_options_chain(..., params={"limit": 10, ...}):
    options_chain.append(option)  # Appends ALL results, not just 10!
```

The for loop iterates through ALL options the API returns, ignoring the limit parameter.

**Solution**: Add explicit limit enforcement:
```python
for option in client.list_snapshot_options_chain(...):
    options_chain.append(option)
    if len(options_chain) >= 10:  # Enforce 10-strike maximum
        break
```

### Issue #2: Test Script Path Violation
**Evidence**: `test_cli_regression.sh` lines 179-180:
```bash
RAW_OUTPUT="/tmp/cli_output_loop${loop_num}_${LOOP_TIMESTAMP}.log"
INPUT_FILE="/tmp/test_input_loop${loop_num}_${LOOP_TIMESTAMP}.txt"
```

**Violation**: Writing to system-level /tmp violates project scope boundaries

**Solution**: Change to project-level tmp/ folder:
```bash
RAW_OUTPUT="./tmp/cli_output_loop${loop_num}_${LOOP_TIMESTAMP}.log"
INPUT_FILE="./tmp/test_input_loop${loop_num}_${LOOP_TIMESTAMP}.txt"
```

Add directory creation: `mkdir -p tmp` before writing files

---

## PHASE 1: Code Implementation ✅ READY

### Task 1.1: Fix get_call_options_chain - Add 10-strike limit enforcement
- **File**: `src/backend/tools/polygon_tools.py`
- **Function**: `get_call_options_chain` (lines 588-720)
- **Action**: Add `if len(options_chain) >= 10: break` inside the for loop
- **Location**: After `options_chain.append(option)` (approximately line 679)
- **Tool**: Use Serena replace_symbol_body

**Implementation**:
```python
for option in client.list_snapshot_options_chain(...):
    options_chain.append(option)
    if len(options_chain) >= 10:  # NEW: Enforce 10-strike maximum
        break
```

### Task 1.2: Fix get_put_options_chain - Add 10-strike limit enforcement
- **File**: `src/backend/tools/polygon_tools.py`
- **Function**: `get_put_options_chain` (lines 723-855)
- **Action**: Identical fix - add `if len(options_chain) >= 10: break`
- **Location**: After `options_chain.append(option)` (approximately line 814)
- **Tool**: Use Serena replace_symbol_body

### Task 1.3: Fix test_cli_regression.sh - Change /tmp to ./tmp
- **File**: `test_cli_regression.sh`
- **Lines**: 179-180
- **Action**:
  1. Change `/tmp/` to `./tmp/` in both RAW_OUTPUT and INPUT_FILE paths
  2. Add `mkdir -p tmp` before file creation (around line 182)
- **Tool**: Use standard Edit tool

**Implementation**:
```bash
# Create tmp directory if not exists
mkdir -p tmp

RAW_OUTPUT="./tmp/cli_output_loop${loop_num}_${LOOP_TIMESTAMP}.log"
INPUT_FILE="./tmp/test_input_loop${loop_num}_${LOOP_TIMESTAMP}.txt"
```

---

## PHASE 2: CLI Testing Phase 🔴 MANDATORY - DO NOT SKIP

### Task 2.1: Execute test suite
```bash
./test_cli_regression.sh
```

### Task 2.2: Verify test results
- ✅ All 36 tests must PASS (100% success rate)
- ✅ Test report generated in test-reports/
- ✅ No NoneType round() errors
- ✅ Session persistence verified
- ✅ Log files now in project tmp/ folder (not system /tmp)

### Task 2.3: **CRITICAL** - Examine actual responses for 10-strike limit

**Options Chain Tests to examine**:
- **Test 14**: SPY Call Options Chain
- **Test 15**: SPY Put Options Chain
- **Test 29**: NVDA Call Options Chain
- **Test 30**: NVDA Put Options Chain

**What to verify in ACTUAL RESPONSES**:
1. ✅ **EXACTLY 10 strikes per chain** (count the bullet points!)
2. ✅ No more than 10 strikes (e.g., not 24+ like before)
3. ✅ Proper JSON formatting with strike prices as keys
4. ✅ All fields present and properly rounded
5. ✅ No NoneType errors
6. ✅ 0.00 values where API returned None (acceptable)

**Counting method**:
```bash
# Count strikes in test output
grep -o '^\s*•\s*\$[0-9]*\.[0-9]*:' tmp/cli_output_loop1_*.log | wc -l
```

**Expected result**: Should show ~40-50 total strikes across ALL 4 options tests (10 each x 4 tests), NOT 174!

### Task 2.4: Verify log file location
```bash
# Verify logs are in project tmp/, not system /tmp
ls -lh ./tmp/cli_output_loop1_*.log
ls -lh /tmp/cli_output_loop1_*.log 2>/dev/null  # Should show: No such file
```

### Task 2.5: Show evidence to user
- Display test summary output
- Show pass/fail counts (must be 36/36 PASS)
- Provide test report file path
- **CRITICAL**: Show actual strike counts from options chain responses
- Verify log file location (project tmp/ vs system /tmp)

### Task 2.6: User checkpoint
**STOP HERE** and notify user to review test results before proceeding.

**Message to user**:
"Test results ready for review. Critical fixes implemented:
1. Options chain tools now enforce 10-strike maximum (was 174+ strikes before)
2. Test logs now output to project tmp/ folder (not system /tmp)

Please examine:
- Actual strike counts in options chain responses (should be exactly 10 each)
- Log file location verification
- Test report: [path]

Let me know if you'd like me to proceed with documentation updates and final commit."

---

## PHASE 3: Serena Memory Update Phase ⏸️ PAUSED

**DO NOT PROCEED** until user reviews and approves test results.

### Task 3.1: Update tech_stack.md
- Document the 10-strike limit bug fix
- Document the test script path fix
- Add note about explicit limit enforcement in API calls

### Task 3.2: Update testing_procedures.md (if exists)
- Document the project tmp/ folder usage
- Add validation steps for strike count verification

---

## PHASE 4: Documentation Update Phase ⏸️ PAUSED

**DO NOT PROCEED** until user reviews and approves test results.

### Task 4.1: Update CLAUDE.md
- Update Last Completed Task Summary section
- Document both bug fixes with evidence
- Include strike count comparison (174 → 40-50 total)
- Include test report reference

---

## PHASE 5: Git Commit Phase ⏸️ PAUSED

**DO NOT PROCEED** until user reviews and approves test results.

### Task 5.1: Proper atomic commit workflow
1. Verify all work complete (code, tests, docs, memories)
2. Review changes: `git status` and `git diff`
3. Stage everything at once: `git add -A`
4. Verify staging: `git status`
5. Commit immediately with proper message
6. Push immediately: `git push`

**Commit message template**:
```
[OPTIONS-FIX] Enforce 10-strike limit & fix test script path violation

Issue #1: Options chain flooding (CRITICAL)
- Add explicit 10-strike limit enforcement in get_call_options_chain
- Add explicit 10-strike limit enforcement in get_put_options_chain
- Pattern: if len(options_chain) >= 10: break
- Impact: Reduced 174 total strikes to ~40-50 (10 per chain x 4 tests)
- Evidence: Was showing 24+ strikes for single SPY call chain

Issue #2: Test script path violation
- Changed test_cli_regression.sh log paths from /tmp to ./tmp
- Added mkdir -p tmp for directory creation
- Violation: Writing to system /tmp violates project scope
- Fix: All logs now in project tmp/ folder

Validation:
- Test suite: 36/36 PASSED (100% success)
- Strike count verified: Exactly 10 per options chain
- Log location verified: project tmp/ folder
- Test report: [report-path]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Tool Usage Requirements

### Sequential-Thinking
- ✅ Used for research and analysis (8 thoughts)
- Use again for implementation verification
- Use for synthesis of test results

### Serena Tools
- ✅ find_symbol: Located both functions
- ✅ search_for_pattern: Found /tmp references in test script
- replace_symbol_body: Update get_call_options_chain with limit enforcement
- replace_symbol_body: Update get_put_options_chain with limit enforcement
- write_memory: Update tech_stack.md
- write_memory: Update testing_procedures.md (if needed)

### Standard Tools
- Edit: Update test_cli_regression.sh paths
- Bash: Execute test suite and verify results
- Bash: Count strikes in output
- Bash: Verify log file locations
- Read: Review test output files
- Edit: Update CLAUDE.md documentation

---

## Success Criteria

### Code Implementation
- ✅ Both options functions updated with 10-strike limit
- ✅ Test script updated to use project tmp/ folder
- ✅ Code compiles without syntax errors

### Testing
- ✅ 36/36 tests PASS (100% success rate)
- ✅ Each options chain shows EXACTLY 10 strikes
- ✅ Total strike count: ~40-50 (10 x 4 tests), not 174
- ✅ Log files in project tmp/, not system /tmp
- ✅ No NoneType round() errors
- ✅ Test report generated

### User Approval
- ✅ User reviews actual strike counts
- ✅ User reviews log file locations
- ✅ User confirms both bugs are fixed
- ✅ User approves proceeding to documentation/commit

### Documentation
- ✅ CLAUDE.md updated with both fixes
- ✅ Serena memories updated
- ✅ Git commit with all changes

---

## Current Status

**Phase 1: Code Implementation** - ✅ READY TO START
**Phase 2: CLI Testing** - ⏳ PENDING
**Phase 3: Serena Updates** - ⏸️ PAUSED (awaiting user approval)
**Phase 4: Documentation** - ⏸️ PAUSED (awaiting user approval)
**Phase 5: Git Commit** - ⏸️ PAUSED (awaiting user approval)

---

## Evidence Summary

**Before Fix**:
- 174 total option strikes in log file
- SPY Call Options Chain: 24+ strikes shown
- Logs written to system /tmp

**After Fix (Expected)**:
- ~40-50 total option strikes (10 per chain x 4 tests)
- SPY Call Options Chain: EXACTLY 10 strikes
- Logs written to project tmp/ folder

---

## Next Action

**PROCEED WITH PHASE 1**: Implement both fixes using Serena and standard tools.
