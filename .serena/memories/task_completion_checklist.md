# Task Completion Checklist

## Pre-Commit Quality Checklist

Before committing ANY code changes, complete ALL items in this checklist:

### 1. Code Quality Checks

#### Python Code Quality
```bash
# Lint Python code
npm run lint:python
# Expected: 10.00/10 score, 0 errors

# Fix Python formatting
npm run lint:fix:python
# Expected: All files reformatted by black + isort
```

#### TypeScript/JavaScript Code Quality
```bash
# Lint TypeScript/React code
npm run lint:js
# Expected: Max 150 warnings, 0 errors

# Fix TypeScript/JavaScript issues
npm run lint:fix:js
# Expected: Auto-fixable issues resolved

# Format code
npm run format
# Expected: All files formatted by Prettier

# Type check
npm run type-check
# Expected: 0 TypeScript errors
```

#### All Quality Checks
```bash
# Run all checks at once
npm run check:all
# Expected: All checks passing
```

### 2. Testing (MANDATORY) - TWO-PHASE APPROACH

#### CLI Regression Testing - Phase 1: Automated Response Generation

```bash
# Run CLI regression test suite (39 tests)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Expected Phase 1 results:
# - 39/39 responses COMPLETED (100% generation rate)
# - Average response time: ~10-12 seconds
# - Test report generated in test-reports/
# - Phase 2 instructions displayed
```

#### CLI Regression Testing - Phase 2: MANDATORY Grep-Based Verification (EVIDENCE REQUIRED)

**CRITICAL:** Script can ONLY verify responses received. It CANNOT validate correctness.

Phase 2 is broken into 4 sub-phases with **MANDATORY bash commands** that MUST be executed:

##### **Phase 2a: ERROR DETECTION (MANDATORY - MUST RUN COMMANDS)**

🔴 **YOU MUST RUN these grep commands and SHOW output. Cannot proceed without evidence.**

```bash
# Command 1: Find all errors/failures
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log

# Command 2: Count 'data unavailable' errors
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log

# Command 3: Count completed tests
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Required Output**: Paste ALL grep command outputs. If you don't show grep output, Phase 2 is INCOMPLETE.

##### **Phase 2b: DOCUMENT FAILURES (MANDATORY - IF ERRORS FOUND)**

If Phase 2a grep commands found errors, create **evidence-based failure table**:

| Test # | Test Name | Line # | Error Message | Tool Call (if visible) |
|--------|-----------|--------|---------------|------------------------|
| 3 | SPY_Yesterday_Price_OHLC | 157 | data unavailable due to retrieval error | get_stock_price_history(...) |

**Required**: Show grep output + failure table with line numbers, OR confirm "0 failures found".

##### **Phase 2c: VERIFY RESPONSE CORRECTNESS (For tests without errors)**

For tests that didn't show errors in Phase 2a, verify:

1. ✅ Response directly addresses the prompt query
2. ✅ Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
3. ✅ Appropriate tool calls made (Polygon, Finnhub, Tradier)
4. ✅ Data formatting matches expected format (OHLC, tables, etc.)
5. ✅ No hallucinated data or made-up values
6. ✅ Options chains show Bid/Ask columns (NOT midpoint)
7. ✅ Technical analysis includes proper indicators
8. ✅ Response is complete (not truncated)

##### **Phase 2d: FINAL VERIFICATION (CHECKPOINT QUESTIONS)**

Answer ALL checkpoint questions with evidence:

1. ✅ Did you RUN the 3 mandatory grep commands in Phase 2a? **SHOW OUTPUT**
2. ✅ Did you DOCUMENT all failures found (or confirm 0 failures)? **PROVIDE TABLE OR "0 failures"**
3. ✅ Failure count from grep -c: **X failures**
4. ✅ Tests that generated responses: **X/39 COMPLETED**
5. ✅ Tests that PASSED verification (no errors): **X/39 PASSED**

**🔴 CANNOT MARK TASK COMPLETE WITHOUT:**
- Running and showing grep outputs
- Documenting failures with evidence (or confirming 0 failures)
- Providing failure count: `grep -c "data unavailable"`
- Answering all 5 checkpoint questions with evidence

**NEVER:**
- ❌ Skip Phase 1 test execution
- ❌ Skip Phase 2a-2d grep-based verification
- ❌ Claim completion without showing grep outputs
- ❌ Mark task "done" without evidence
- ❌ Proceed to documentation without all 4 sub-phases complete

**Pattern Recognition:**

**WRONG (What NOT to do):**
```
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN Phase 1: ./test_cli_regression.sh ✅
4. Show results: 39/39 COMPLETED ✅
5. Update documentation ✅
6. Mark task complete ❌ (NEVER performed Phase 2 with grep!)
```

**CORRECT (What TO do):**
```
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN Phase 1: chmod +x test_cli_regression.sh && ./test_cli_regression.sh ✅
4. Show Phase 1 results: 39/39 COMPLETED ✅
5. Phase 2a: RUN 3 grep commands, SHOW output ✅
6. Phase 2b: Document failures with table (or confirm 0 failures) ✅
7. Phase 2c: Verify non-error responses ✅
8. Phase 2d: Answer 5 checkpoint questions with evidence ✅
9. Update documentation with test results ✅
10. Mark task complete ✅
```

**Remember: If you haven't completed Phase 1 AND Phase 2 (all 4 sub-phases with evidence), the task is NOT complete.**

### 3. Documentation Updates

#### Update Project Documentation
```bash
# Update CLAUDE.md with Last Completed Task Summary
# Update README.md if user-facing features changed
# Update relevant .md files in docs/ if needed
```

**CLAUDE.md Last Completed Task Section:**
```markdown
## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
High Level Task Summary between 10-20 lines at MOST to give an overview
<!-- LAST_COMPLETED_TASK_END -->
```

#### Update Serena Memories (if applicable)
```bash
# If architectural changes affect Serena memories:
# - Update project_architecture.md
# - Update tech_stack.md
# - Update task_completion_checklist.md
# - Update suggested_commands.md
```

### 4. Performance Verification

#### Server Health Check
```bash
# Start servers
chmod +x start-app-xterm.sh && ./start-app-xterm.sh

# Verify backend health
curl http://127.0.0.1:8000/health
# Expected: {"status": "healthy"}

# Verify frontend
curl http://127.0.0.1:3000
# Expected: HTML response

# Or use npm script
npm run status
```

#### Performance Testing (if changes affect performance)
```bash
# Run performance baseline
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 10

# Check average response time
# Expected: ~6-8 seconds average
# Expected: 100% success rate
```

### 5. Git Workflow - PROPER ATOMIC COMMIT

**🔴 CRITICAL: Follow this EXACT workflow**

#### PROPER ATOMIC COMMIT WORKFLOW

**The Fatal Mistake: Early Staging**

**NEVER stage files early during development. Staging is the LAST step before committing.**

**What happens when you stage too early:**
1. ⏰ **Time T1**: You run `git add` (files staged)
   - Staging area = snapshot at T1
2. ⏰ **Time T2-T5**: You continue working
   - Update config files
   - Run tests (generates test reports)
   - Update documentation
3. ⏰ **Time T6**: You run `git commit`
   - **Only commits the T1 snapshot**
   - **All work after T1 is MISSING**

**Result: Incomplete, broken atomic commits** ❌

#### Correct Workflow (Follow EXACTLY)

**Step 1: DO ALL WORK FIRST** (DO NOT stage anything yet)
- ✅ Complete ALL code changes
- ✅ Run ALL tests and generate test reports
- ✅ Update ALL documentation (CLAUDE.md, README.md, etc.)
- ✅ Update ALL config files (.claude/settings.local.json, etc.)
- ✅ Update ALL Serena memories (if applicable)
- ✅ Update ALL task plans (if applicable)
- ⚠️ **DO NOT RUN `git add` YET**

**Step 2: VERIFY EVERYTHING IS COMPLETE**
```bash
git status  # Review ALL changed/new files
git diff    # Review ALL changes
```

**Step 3: STAGE EVERYTHING AT ONCE**
```bash
git add -A  # Stage ALL files in ONE command
```
- ⚠️ This is the FIRST time you run `git add`

**Step 4: VERIFY STAGING IMMEDIATELY**
```bash
git status  # Verify ALL files staged, NOTHING unstaged
```

**Step 5: COMMIT IMMEDIATELY** (within 60 seconds)
```bash
git commit -m "$(cat <<'EOF'
[CATEGORY] Brief description

- Detailed change 1
- Detailed change 2
- Test results: 39/39 tests passing, 9.14s avg
- Files changed: X files

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Step 6: PUSH IMMEDIATELY**
```bash
git push
```

#### What Belongs in an Atomic Commit

**ALL of these must be included together:**
- ✅ Code changes (backend + frontend)
- ✅ Test reports (evidence of passing tests)
- ✅ Documentation updates (CLAUDE.md, README.md, etc.)
- ✅ Memory updates (.serena/memories/)
- ✅ Config changes (.claude/settings.local.json, etc.)
- ✅ Task plan updates (TODO_task_plan.md, etc.)

#### ❌ NEVER DO THIS

- ❌ Stage files early during development
- ❌ Stage files "as you go"
- ❌ Run `git add` before ALL work is complete
- ❌ Delay between `git add` and `git commit`
- ❌ Commit without test reports
- ❌ Commit without documentation updates

**Reference:** See `.serena/memories/git_commit_workflow.md` for complete details.

**Enforcement:** Incomplete commits will be reverted and reworked.

### 6. Final Verification

#### Pre-Push Checklist
- [ ] All code quality checks passing
- [ ] All tests passing (39/39 for CLI regression)
- [ ] Test report generated and included in commit
- [ ] Documentation updated (CLAUDE.md, README.md)
- [ ] Serena memories updated (if applicable)
- [ ] Git commit follows atomic workflow
- [ ] All files staged and committed
- [ ] Commit message is descriptive and includes test results

#### Post-Push Verification
```bash
# Verify push succeeded
git log -1
# Expected: Your commit appears in log

# Verify remote is up to date
git status
# Expected: "Your branch is up to date with 'origin/master'"
```

## Common Task Workflows

### Adding New Features

1. **Implementation Phase:**
   ```bash
   # Implement feature code
   # Create/update test prompts
   # Run quality checks
   npm run lint:fix
   npm run type-check
   ```

2. **Testing Phase (MANDATORY):**
   ```bash
   # Execute Phase 1: Response generation
   chmod +x test_cli_regression.sh && ./test_cli_regression.sh
   
   # Execute Phase 2: Manual verification
   # - Check test report in test-reports/
   # - Verify each response against 8-point criteria
   # - Verify 100% correctness
   # - Note average response time
   ```

3. **Documentation Phase:**
   ```bash
   # Update CLAUDE.md Last Completed Task
   # Update README.md if needed
   # Update Serena memories if applicable
   ```

4. **Commit Phase:**
   ```bash
   # Verify ALL work complete
   git status
   git diff
   
   # Stage EVERYTHING at once
   git add -A
   
   # Verify staging
   git status
   
   # Commit immediately
   git commit -m "message with test results"
   
   # Push immediately
   git push
   ```

### Fixing Bugs

1. **Fix the bug in code**
2. **Run quality checks** (`npm run check:all`)
3. **Run tests** (`chmod +x test_cli_regression.sh && ./test_cli_regression.sh`)
4. **Verify test responses** (Phase 2 manual verification)
5. **Update documentation** (if needed)
6. **Commit with atomic workflow** (`git add -A` → `git commit` → `git push`)

### Refactoring Code

1. **Make refactoring changes**
2. **Run quality checks** (`npm run lint:fix && npm run type-check`)
3. **Run tests** (verify no regressions - both Phase 1 and Phase 2)
4. **Update documentation** (if architecture changed)
5. **Update Serena memories** (if applicable)
6. **Commit with atomic workflow**

### Updating Documentation

1. **Make documentation changes**
2. **Run markdown linting** (if available)
3. **Verify links work**
4. **Update CLAUDE.md Last Completed Task**
5. **Commit with atomic workflow**

## Quality Standards

### Required Scores
- **Python Pylint**: 10.00/10 (no errors)
- **TypeScript ESLint**: Max 150 warnings, 0 errors
- **TypeScript Compiler**: 0 errors
- **Test Success Rate**: 100% (both Phase 1 completion and Phase 2 verification)
- **Response Time**: < 10s average (target ~6-8s)

### Performance Targets
- **CLI Response Time**: 6-8s average
- **Frontend FCP**: < 300ms
- **Frontend LCP**: < 500ms
- **Test Success Rate**: 100%

## Emergency Procedures

### If Tests Fail

1. **Do NOT commit**
2. **Analyze failure**:
   ```bash
   # Check test report
   cat test-reports/test_cli_regression_*.log
   ```
3. **Fix the issue**
4. **Re-run tests** (both Phase 1 and Phase 2)
5. **Only commit when tests pass 100%**

### If Quality Checks Fail

1. **Run auto-fix**:
   ```bash
   npm run lint:fix
   npm run format
   ```
2. **Re-run checks**:
   ```bash
   npm run check:all
   ```
3. **Manually fix remaining issues**
4. **Verify all checks pass**

### If Servers Won't Start

1. **Kill existing processes**:
   ```bash
   pkill -f uvicorn
   pkill -f vite
   ```
2. **Clear ports**:
   ```bash
   lsof -i :8000 | grep -v PID | awk '{print $2}' | xargs -r kill -9
   lsof -i :3000 | grep -v PID | awk '{print $2}' | xargs -r kill -9
   ```
3. **Restart servers**:
   ```bash
   chmod +x start-app-xterm.sh && ./start-app-xterm.sh
   ```

## Summary Checklist

Before pushing ANY commit:

- [ ] ✅ All code quality checks passing
- [ ] ✅ Phase 1: All tests executed and 100% completion rate
- [ ] ✅ Phase 2: Manual verification completed for ALL test responses
- [ ] ✅ Test report generated and will be included in commit
- [ ] ✅ Documentation updated (CLAUDE.md, README.md)
- [ ] ✅ Serena memories updated (if applicable)
- [ ] ✅ ALL work complete (do not stage yet!)
- [ ] ✅ Reviewed git status and git diff
- [ ] ✅ Staged ALL files at once: `git add -A`
- [ ] ✅ Verified staging: `git status`
- [ ] ✅ Committed immediately after staging
- [ ] ✅ Pushed immediately after committing

**Remember: If you haven't completed Phase 1 AND Phase 2, the task is NOT complete.**

**Remember: Stage files ONLY immediately before committing. Never stage early!**
