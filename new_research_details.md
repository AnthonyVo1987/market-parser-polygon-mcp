🔴 CRITICAL: FOLLOW THE ENTIRE WORKFLOW PHASES IN ORDER FOR THE REQUESTED NEW CHANGES. RESEARCH -> PLANNING -> IMPLEMENTATION -> TESTING -> COMMIT 🔴

---

<Phase 1: Research> ULTRA-THINK to Research the requested task(s): 

## Task 1. Change 'test_cli_regression.sh' with new test prompt sequence:

'''
declare -a prompts=(
    "Market Status"
    "Current Price OHLC: \$SPY"
    "Yesterday's Price OHLC: \$SPY"
    "Last week's Performance OHLC: \$SPY"
    "Stock Price on the previous week's Friday OHLC: \$SPY"
    "Stock Price Performance the last 5 Trading Days OHLC: \$SPY"
    "Stock Price Performance the past 2 Weeks OHLC: \$SPY"
    "Stock Price Performance the past month: \$SPY"
    "Stock Price Performance the past 3 months: \$SPY"
    "Get technical analysis indicator DATA only with NO ANALYSIS: \$SPY"
    "Support & Resistance Levels: \$SPY"
    "Perform technical analysis based on all available data for Trends, Volatility, Momentum, Trading Patterns\Signals: \$SPY
    "Get options expiration dates: \$SPY"
    "Get Call Options Chain Expiring this Friday: \$SPY"
    "Get Put Options Chain Expiring this Friday: \$SPY"
    "Analyze the Options Chain Data & provide potential Call & Put Wall(s) Strike Prices: \$SPY"

    "Current Price OHLC: \$NVDA"
    "Yesterday's Price OHLC: \$NVDA"
    "Last week's Performance OHLC: \$NVDA"
    "Stock Price on the previous week's Friday OHLC: \$NVDA"
    "Stock Price Performance the last 5 Trading Days OHLC: \$NVDA"
    "Stock Price Performance the past 2 Weeks OHLC: \$NVDA"
    "Stock Price Performance the past month: \$NVDA"
    "Stock Price Performance the past 3 months: \$NVDA"
    "Get technical analysis indicator DATA only with NO ANALYSIS: \$NVDA"
    "Support & Resistance Levels: \$NVDA"
    "Perform technical analysis based on all available data for Trends, Volatility, Momentum, Trading Patterns\Signals: \$NVDA
    "Get options expiration dates for \$NVDA"
    "Get Call Options Chain Expiring this Friday: \$NVDA"
    "Get Put Options Chain Expiring this Friday: \$NVDA"
    "Analyze the Options Chain Data & provide potential Call & Put Wall(s) Strike Prices: \$NVDA"

    "Current Price OHLC: \$WDC, \$AMD, \$SOUN"
    "Yesterday's Price OHLC: \$WDC, \$AMD, \$SOUN"
    "Yesterday's Closing Price: \$WDC, \$AMD, \$SOUN"
    "Last week's Performance OHLC: \$WDC, \$AMD, \$SOUN"
    "Get technical analysis indicator DATA only with NO ANALYSIS: \$WDC, \$AMD, \$SOUN"
    "Support & Resistance Levels: \$WDC, \$AMD, \$SOUN"
    "Perform technical analysis based on all available data for Trends, Volatility, Momentum, Trading Patterns\Signals: \$WDC, \$AMD, \$SOUN"
    "Get options expiration dates: \$WDC, \$AMD, \$SOUN"
)
'''

## Task 2. Update 'test_cli_regression.sh' AND project docs and Serena Memories with new test result criteria and procedure:
- Rework our test script and docs how it produces the results. The problem is the current test script is saying a test passes, but that’s not true. The script can onyl check if there was ANY response in general, before marking as PASS. This actually doesn’t even check if the response was even correct so there is actually no verification of the actual test responses, only a verification if a test prompt even was successful
- This causes a lot of confusion for AI agents like you when you run the test and then the test script says PASS, so you automatically assume all the tests PASSED but that’s NOT true because that means you would completely ignore the contents of the response. The script can ONLY conclude if there was ANY response, and doesn't have the ability to actually verify the results
- So let’s remove all ambiguity. Now the test script will no longer say if a test actually PASS, so remove ALL mention of saying if a test PASS because the script cannot validate if a test passes on its own because the script doesn’t have the capability of verifying the actual response
- So what we need to do is have the script make it clear that after the test results have finished, now YOU \ AI Agent has to  MANUALLY review the actual results of each test prompt response to make sure that the response matches the prompt and matches the tool calls that are expected etc
- Basically when you’re running tests and scripts, it’s a two phase approach now: Phase 1 is running just the script 'test_cli_regression.sh' until completion to get the test results. Phase 2 now you actually have to READ & REVIEW and verify the results of EACH test prompt and that’s how we’ll know if any test PASS or FAIL
- so we have to do a mandate and make sure we also add special rules too to as a sanity, check in case you forget to review the results so after testing is complete. The mandated question is "Did you verify the results of each test prompt to ensure the response was correct and expected with the proper tool calls?"
- Just because a test can respond quickly does NOT mean the test PASSES because it can just respond with garbage bogus data or hallucinate or make up their own data or maybe don’t don’t do any tool calls at all. That’s why you have to actually verify the individual test results so we need to reiterate across the board in the test scripts and the memories and any project docs that the results must be reviewed
- Long story short: running 'test_cli_regression.sh' until completion is only Phase 1.  Phase 2 MUST be performed to review the actual results

## Task 3. Validate new script changes by re-running 'test_cli_regression.sh', review the results and response to ensure compliance, fix any issues if found and re-run to validate


🔴 CRITICAL: After research is complete, Delete the current file 'reasearch_task_plan.md' and then ULTRA-THINK AND GENERATE a brand new 'reasearch_task_plan.md' based on the reasearch task(s)🔴

---

<Phase 2: Planning>

Based on the latest Research, Analysis & Scoping 'reasearch_task_plan.md', delete the current file 'TODO_task_plan.md' and then ULTRA-THINK AND GENERATE a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to systemtically use your Mandatory Tools Toolkit for Sequential-Thinking & Serena tools to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes.  The plan MUST enforce that YOU MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to enhance your workflow to perform all task(s)

---

<Phase 3: Implementation> 🔴 CRITICAL: NOW YOU MAY START IMPLEMENTING DURING THIS PHASE 🔴

You MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to Implement all code changes, test suite updates, and agent instruction modifications according to the TODO_task_plan.md

---

<Phase 4: Testing>

  🔴 MANDATORY CHECKPOINT - DO NOT SKIP 🔴

⚠️ **CRITICAL: You MUST run tests BEFORE claiming completion** ⚠️
⚠️ **CRITICAL: Task is INCOMPLETE without test execution and results** ⚠️

**REQUIRED ACTIONS:**

1. ✅ **Execute the test suite:**

   ```bash
   chmod +x test_cli_regression.sh && ./test_cli_regression.sh
   ```

2. ✅ **Verify test results:**
   🔴 MANDATORY - VERIFY THE CONTENT OF EACH TEST PROMPT RESPONSE THAT IT MATCHES THE EXPECTED RESPONSE, PROPER TOOL CALLS, AND RESPONSE FORMATTING🔴
   - PASS CRITERIA: CONTENT OF TEST PROMPT RESPONS MATCHES THE EXPECTED RESPONSE, PROPER TOOL CALLS, AND RESPONSE FORMATTING
   - Test report generated in test-reports/
   - No errors or failures in output
   - Session persistence verified
   - Phase 2: Test Prompt Response Verification for EACH test completed

3. ✅ **Show evidence to user:**
   - Display test summary output
   - Show pass/fail counts (must be X/X PASS)
   - Provide test report file path
   - Show performance metrics (response times)

**❌ ENFORCEMENT RULES:**

- Code without test execution = Code NOT implemented
- No test results = Task INCOMPLETE
- Must run tests BEFORE ANY DOCUMENTATION UPDATES
- Cannot claim "done" without showing test evidence
- Test failures must be fixed and re-tested

**✅ ONLY PROCEED to next phase after:**

- Test suite executed successfully
- 100% pass rate achieved with Phase 2: Test Prompt Response Verification for EACH test completed
- Test results displayed to user
- Test report path provided

🔴 **IF YOU SKIP THIS PHASE, THE ENTIRE TASK IS INVALID** 🔴

---

<Phase 5: Final Git Commit Phase> 🔴 CRITICAL: PROPER ATOMIC COMMIT WORKFLOW 🔴

**MANDATORY: Stage ONLY Immediately Before Commit**

**CORRECT Workflow (follow EXACTLY):**

1. **DO ALL WORK FIRST** (DO NOT stage anything yet):
   - ✅ Complete ALL code changes
   - ✅ Run ALL tests and generate test reports
   - ✅ Update ALL documentation (CLAUDE.md, tech_stack.md, etc.)s
   - ✅ Update ALL config files (.claude/settings.local.json, etc.)
   - ✅ Update ALL task plans
   - ⚠️ **DO NOT RUN `git add` YET**

2. **VERIFY EVERYTHING IS COMPLETE**:

   ```bash
   git status  # Review ALL changed/new files
   git diff    # Review ALL changes
   ```

   - Ensure ALL work is done
   - Ensure ALL files are present

3. **STAGE EVERYTHING AT ONCE**:

   ```bash
   git add -A  # Stage ALL files in ONE command
   ```

   - ⚠️ This is the FIRST time you run `git add`
   - ⚠️ Stage ALL related files together

4. **VERIFY STAGING IMMEDIATELY**:

   ```bash
   git status  # Verify ALL files staged, NOTHING unstaged
   ```

   - If anything is missing: `git add [missing-file]`

5. **COMMIT IMMEDIATELY** (within 60 seconds of staging):

   ```bash
   git commit -m "$(cat <<'EOF'
   [TAG] Descriptive commit message

   - Change 1
   - Change 2

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

6. **PUSH IMMEDIATELY**:

   ```bash
   git push
   ```

**WHAT BELONGS IN ATOMIC COMMIT:**

- ✅ Code changes (backend + frontend)
- ✅ Test reports (evidence of passing tests)
- ✅ Documentation updates (CLAUDE.md, README.md, etc.)
- ✅ Config changes (.claude/settings.local.json, etc.)
- ✅ Task plan updates (TODO_task_plan.md, etc.)

**❌ NEVER DO THIS:**

- ❌ Stage files early during development
- ❌ Stage files "as you go"
- ❌ Run `git add` before ALL work is complete
- ❌ Delay between `git add` and `git commit`
- ❌ Commit without test reports
- ❌ Commit without documentation updates

**Reference:** See `.serena/memories/git_commit_workflow.md` for complete details

---
