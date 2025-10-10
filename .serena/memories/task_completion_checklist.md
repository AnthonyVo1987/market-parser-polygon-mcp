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

### 2. Testing (MANDATORY)

#### CLI Regression Testing
```bash
# Run CLI regression test suite (27 tests)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Expected results:
# - 27/27 tests PASSED (100% success rate)
# - Average response time: ~6-8 seconds
# - Test report generated in test-reports/
```

**CRITICAL:** Test execution is MANDATORY. You MUST:
- ✅ Execute the test suite
- ✅ Show test results to user
- ✅ Verify 100% pass rate
- ✅ Provide test report file path
- ✅ Fix any failures and re-test

**NEVER:**
- ❌ Skip test execution
- ❌ Claim completion without test results
- ❌ Mark task "done" without test evidence
- ❌ Proceed to documentation without running tests

**Pattern Recognition:**

**WRONG:**
```
1. Create 5 new tools ✅
2. Update test suite file ✅
3. Update documentation ✅
4. Mark task complete ❌ (NEVER ran tests!)
```

**CORRECT:**
```
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN test suite: chmod +x test_cli_regression.sh && ./test_cli_regression.sh ✅
4. Show results: 27/27 PASS, 100% success ✅
5. Provide test report path ✅
6. Update documentation with test results ✅
7. Mark task complete ✅
```

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
[CATEGORY] Brief task description

**Context:**
- Why this task was needed
- What architectural changes were made

**Changes Made:**
- Detailed list of all changes
- Files modified
- Test results

**Performance/Metrics (if applicable):**
- Test results (e.g., 27/27 tests passing)
- Performance metrics (e.g., 6.10s avg response time)
- Success rates

**Files Changed:**
- ✅ Modified: path/to/file1
- ✅ Added: path/to/file2
- ✅ Deleted: path/to/file3
- **Total**: X files changed

**Key Achievements:**
- ✅ Achievement 1
- ✅ Achievement 2
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
- Test results: 27/27 tests passing, 6.10s avg
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
- [ ] All tests passing (27/27 for CLI regression)
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
   # Execute tests
   chmod +x test_cli_regression.sh && ./test_cli_regression.sh
   
   # Verify results
   # - Check test report in test-reports/
   # - Verify 100% pass rate
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
4. **Update documentation** (if needed)
5. **Commit with atomic workflow** (`git add -A` → `git commit` → `git push`)

### Refactoring Code

1. **Make refactoring changes**
2. **Run quality checks** (`npm run lint:fix && npm run type-check`)
3. **Run tests** (verify no regressions)
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
- **Test Success Rate**: 100%
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
   cat test-reports/comprehensive_*.txt
   ```
3. **Fix the issue**
4. **Re-run tests**
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
- [ ] ✅ All tests executed and passing (100% success rate)
- [ ] ✅ Test report generated and will be included in commit
- [ ] ✅ Documentation updated (CLAUDE.md, README.md)
- [ ] ✅ Serena memories updated (if applicable)
- [ ] ✅ ALL work complete (do not stage yet!)
- [ ] ✅ Reviewed git status and git diff
- [ ] ✅ Staged ALL files at once: `git add -A`
- [ ] ✅ Verified staging: `git status`
- [ ] ✅ Committed immediately after staging
- [ ] ✅ Pushed immediately after committing

**Remember: If you haven't RUN the tests and SHOWN the results, the task is NOT complete.**

**Remember: Stage files ONLY immediately before committing. Never stage early!**
