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
|--------|-----------|--------|---------------|--------------------------|
| 3 | SPY_Yesterday_Price_OHLC | 157 | data unavailable due to retrieval error | get_stock_price_history(...) |

**Required**: Show grep output + failure table with line numbers, OR confirm "0 failures found".

##### **Phase 2c: VERIFY RESPONSE CORRECTNESS (For tests without errors)**

For tests that didn't show errors in Phase 2a, verify:

1. ✅ Response directly addresses the prompt query
2. ✅ Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
3. ✅ Appropriate tool calls made (Polygon, Tradier)
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

### 3. Documentation Updates

#### Update Project Documentation
```bash
# Update CLAUDE.md with Last Completed Task Summary
# Update README.md if user-facing features changed
# Update relevant .md files in docs/ if needed
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

### 5. Git Workflow - PROPER ATOMIC COMMIT

**🔴 CRITICAL: Follow this EXACT workflow**

#### Correct Workflow (Follow EXACTLY)

**Step 1: DO ALL WORK FIRST** (DO NOT stage anything yet)
- ✅ Complete ALL code changes
- ✅ Run ALL tests and generate test reports
- ✅ Update ALL documentation (CLAUDE.md, README.md, etc.)
- ✅ Update ALL config files (.claude/settings.local.json, etc.)
- ✅ Update ALL Serena memories (if applicable)
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

**Step 4: VERIFY STAGING IMMEDIATELY**
```bash
git status  # Verify ALL files staged, NOTHING unstaged
```

**Step 5: COMMIT IMMEDIATELY** (within 60 seconds)
```bash
git commit -m "message with test results"
```

**Step 6: PUSH IMMEDIATELY**
```bash
git push
```

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

**Remember: Stage files ONLY immediately before committing. Never stage early!**
