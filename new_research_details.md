🔴 CRITICAL: FOLLOW THE ENTIRE WORKFLOW PHASES IN ORDER FOR THE REQUESTED NEW CHANGES. RESEARCH -> PLANNING -> IMPLEMENTATION -> TESTING -> COMMIT 🔴

---

<Phase 1: Research> ULTRA-THINK to Research the requested task(s): 

## Task 1. Investigate and Fix the lingering Interval Selections Issues for Weekly\Monthly
- I got the response output logs from the lingering Interval Selections Issues for Weekly\Monthly get_stock_price_history calls
- Looks like the issue is related to YOUR code and actually not the model at all.  So investigate and fix after reviewing the 2x calls below:

```

get_stock_price_history({
  "ticker": "SPY",
  "start_date": "2025-10-08",
  "end_date": "2025-10-15",
  "interval": "weekly"
})

{
  "error": "Unexpected error",
  "message": "Failed to retrieve historical data for SPY: 'str' object has no attribute 'get'",
  "ticker": "SPY"
}


> use the weekly interval to fetch price history for "Last week's Performance OHLC: \$SPY".  if there was an API  issue, explicity state the EXACT ERROR MESSAGE YOU RECEIVED. I want to know WHAT the api error is.. api error means nothign without the actual mesage

Query processed successfully!
Agent Response:


 • SPY Last week's Performance OHLC (weekly interval)                                                                                                                          

API call attempted:                                                                                                                                                            

 • get_stock_price_history(ticker='SPY', start_date='2025-10-06', end_date='2025-10-12', interval='weekly')                                                                    

Exact API error received:                                                                                                                                                      

 • {"error": "Unexpected error", "message": "Failed to retrieve historical data for SPY: 'str' object has no attribute 'get'", "ticker": "SPY"}                                

Tools Used:                                                                                                                                                                    

 • get_stock_price_history(ticker='SPY', start_date='2025-10-06', end_date='2025-10-12', interval='weekly') - Attempted weekly historical data; API returned an error.         

Performance Metrics:
   Response Time: 8.559s
   Tokens Used: 26,695 (Input: 26,178, Output: 517) | Cached Input: 25,600
   Model: gpt-5-nano

──────────────────────────────────────────────────

> now tell me the exact api error message for this prompt using the monthly interval: "Stock Price Performance the past month: \$SPY"

Query processed successfully!
Agent Response:


 • SPY Stock Price Performance the past month: SPY (monthly interval)                                                                                                          

Exact API error message received for this prompt:                                                                                                                              

 • {"error": "Unexpected error", "message": "Failed to retrieve historical data for SPY: 'str' object has no attribute 'get'", "ticker": "SPY"}                                

Note: Monthly historical data retrieval failed with the above error. I can retry with alternative data (e.g., current price from get_stock_quote or fetch daily data for the   
month as a fallback) if you’d like.                                                                                                                                            

Tools Used:                                                                                                                                                                    

 • get_stock_price_history(ticker='SPY', start_date='2025-09-15', end_date='2025-10-15', interval='monthly') - Attempted monthly historical data; API returned the exact error 
   above                                                                                                                                                                       

Performance Metrics:
   Response Time: 13.708s
   Tokens Used: 27,625 (Input: 26,902, Output: 723) | Cached Input: 26,368
   Model: gpt-5-nano
```

## Task 2. Update AI Agent Instructions to ENFORCE RESPONDING WITH VERBATIM ERROR MESSAGES IF THERE ARE ANY FAILURES, such as in API.
- Previously we were chasing our tails trying to get to the bottom of the lingering interval issue, and all the AI Agent said was there was an "API Issue", which is a terrible response because API Issue is vague and doesnt meant anything.  Had the AI Agent explicity tell us the EXACT error message recevied, we could have fixed it alot sooner
- So AI Agent needs FULL transparency with what errors they get and NOT to hide it from the user

## Task 3. Validate fix by issuing manual CLI prompts first:
- "Last week's Performance OHLC: \$SPY"
- "Stock Price Performance the past month: \$SPY"
- "Last week's Performance OHLC: \$NVDA"
- "Stock Price Performance the past month: \$NVDA"
- "Last week's Performance OHLC: \$WDC, \$AMD, \$SOUN"
- "Stock Price Performance the past month: \$WDC, \$AMD, \$SOUN"

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
