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
npm run lint:fix
# Expected: All files reformatted by black + isort
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

#### CLI Regression Testing - Phase 2: MANDATORY Manual Verification (NO SHORTCUTS)

🔴 **CRITICAL: Grep commands are INSUFFICIENT and will miss failures. You MUST manually review EACH test response.**

**Why Grep Fails:**
- ❌ Misses duplicate/unnecessary tool calls (agent calling same tool twice)
- ❌ Misses wrong tool selection (agent calling wrong API for data)
- ❌ Misses data inconsistencies (cross-ticker contamination, wrong data returned)
- ❌ Only catches explicit error messages, not logic errors

**MANDATORY Process for EACH of the 39 Tests:**

##### **Step 1: Read Test Response Using Read Tool**
- Use `Read` tool to read the test log file section for each test
- Read lines corresponding to that test's Agent Response, Tools Used, and Performance Metrics
- **NO scripts, NO grep shortcuts - READ each test manually**

##### **Step 2: Apply 4-Point Verification Criteria**

For EACH test, you MUST verify ALL 4 criteria:

1. ✅ **Does the response address the query?**
   - Does the agent's response directly answer the test prompt?
   - Is the response relevant to the ticker(s) mentioned?
   - Is the response complete (not truncated)?

2. ✅ **Were the RIGHT tools called (not duplicate/unnecessary calls)?**
   - **Check conversation context**: If a previous test already retrieved data, agent should NOT call the same tool again
   - Example FAIL: Test 10 calls `get_ta_indicators()`, Test 12 should NOT call it again
   - Are the tools appropriate for the query (Tradier for quotes, Polygon for TA)?
   - Are there any redundant API calls?

3. ✅ **Is the data correct?**
   - Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
   - Data formatting matches expected format (OHLC, tables, etc.)
   - No hallucinated data or made-up values
   - No cross-ticker contamination (NVDA query shouldn't return SPY data)
   - Options chains show Bid/Ask columns (NOT midpoint)

4. ✅ **Are there any errors?**
   - No error messages in response
   - No "data unavailable" messages
   - No RuntimeWarnings
   - No API errors

##### **Step 3: Document Each Test Result**

Create a table documenting ALL 39 tests:

| Test # | Test Name | Status | Issue (if failed) | Failure Type |
|--------|-----------|--------|-------------------|--------------|
| 1 | Market_Status | ❌ FAIL | timezone import error | Code Error |
| 2 | SPY_Price | ✅ PASS | - | - |
| 10 | SPY_TA_Indicators | ✅ PASS | - | - |
| 12 | SPY_Full_TA | ❌ FAIL | Duplicate call to get_ta_indicators() | Logic Error (Duplicate Tool Call) |
| ... | ... | ... | ... | ... |

**Failure Types:**
- Code Error: Syntax/runtime errors, import errors
- Logic Error (Duplicate Tool Call): Agent made unnecessary redundant API calls
- Logic Error (Wrong Tool): Agent called wrong tool for the query
- Data Error: Wrong data returned, cross-ticker contamination
- Response Error: Incomplete response, doesn't address query

##### **Step 4: Final Checkpoint Questions**

Answer ALL checkpoint questions with evidence:

1. ✅ Did you READ all 39 test responses manually using the Read tool? **YES/NO**
2. ✅ Did you apply all 4 verification criteria to EACH test? **YES/NO**
3. ✅ How many tests PASSED all 4 criteria? **X/39 PASSED**
4. ✅ How many tests FAILED (any criterion)? **X/39 FAILED**
5. ✅ Did you document ALL failures with test #, issue, and failure type? **YES/NO + TABLE**

**🔴 CANNOT MARK TASK COMPLETE WITHOUT:**
- Reading all 39 test responses manually (using Read tool, NOT grep)
- Applying all 4 verification criteria to each test
- Documenting ALL 39 tests in a results table
- Providing failure count and failure details table
- Answering all 5 checkpoint questions with evidence

❌ **NEVER DO:**
- Skip Phase 1 test execution
- Skip Phase 2 manual verification
- Use grep shortcuts (they miss logic errors!)
- Claim completion without reviewing all 39 tests
- Mark task "done" without evidence
- Proceed to documentation without complete manual review

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
# Start Gradio UI
uv run python src/backend/gradio_app.py

# Verify backend health
curl http://127.0.0.1:8000/health
# Expected: {"status": "healthy"}

# Verify Gradio UI
curl http://127.0.0.1:8000
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

## Notes

- **React/TypeScript removed**: No TypeScript/JavaScript linting needed (Oct 17, 2025)
- **Gradio only**: All web UI testing done via Gradio (port 8000)
- **Python-first**: Only Python linting and testing required
- **Manual Testing**: ALWAYS review all 39 test responses individually (Oct 19, 2025)
