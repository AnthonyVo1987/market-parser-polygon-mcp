# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

🔴 CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Serena Tools for code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
3. REPEAT any tool as needed throughout the process
4. 🔴 NEVER stop using tools - continue using them until task completion

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're failing
- If you don't use tools throughout the entire process, you're failingplan

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

---

🔴 CRITICAL: FOLLOW THE ENTIRE WORKFLOW PHASES IN ORDER FOR THE REQUESTED NEW CHANGES. RESEARCH -> PLANNING -> IMPLEMENTATION -> TESTING -> SERENA -> COMMIT 🔴

---

<Phase 1: Research> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS Research PHASE 🔴
ULTRA-THINK to Research the requested task(s):

1. Research updating some AI Agent tools to use Tradier API Endpoints
- https://docs.tradier.com/reference/brokerage-api-markets-get-quotes
- https://docs.tradier.com/reference/brokerage-api-markets-get-clock
- Update AI Agent instructions for the updated tools
- Test the new tools by calling the CLI and testing with requested for each of the following tickers one at a time, and then a multi test: SPY, NVDA, SOUN, QQQ, IWM
- Fix any issues if needed from testing to make the tool tests work properly


1. 'get_stock_quote' to use Tradier Endpoint:
- 'get_stock_quote' can now be used for both SINGLE AND MULTI Tickers within a single tool call
- So we only need the new 'get_stock_quote' to handle any number of tickers in a single tool call

Here is a the example API endpoint Python Call & Response :

```
import requests

url = "https://api.tradier.com/v1/markets/quotes?symbols=SPY"

headers = {
    "Accept": "application/json",
    "authorization": "Bearer <TRADIER_API_KEY>"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
{
  "quotes": {
    "quote": {
      "symbol": "SPY",
      "description": "SPDR S&P 500",
      "exch": "P",
      "type": "etf",
      "last": 653.02,
      "change": -18.14,
      "volume": 159422590,
      "open": 672.13,
      "high": 673.95,
      "low": 652.84,
      "close": 653.02,
      "bid": 652.1,
      "ask": 652.14,
      "change_percentage": -2.71,
      "average_volume": 70675102,
      "last_volume": 0,
      "trade_date": 1760140800001,
      "prevclose": 671.16,
      "week_52_high": 673.94,
      "week_52_low": 481.8,
      "bidsize": 3,
      "bidexch": "P",
      "bid_date": 1760140793000,
      "asksize": 1,
      "askexch": "P",
      "ask_date": 1760140797000,
      "root_symbols": "SPY"
    }
  }
}
```


For multi tickers, here is the example call:

```
import requests

url = "https://api.tradier.com/v1/markets/quotes?symbols=WDC%2CAMD%2CGME"

headers = {
    "Accept": "application/json",
    "authorization": "Bearer 8XP1DYNiWBSOLfCIXtEmJ4NeRIEC"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
{
  "quotes": {
    "quote": [
      {
        "symbol": "WDC",
        "description": "Western Digital Corp",
        "exch": "Q",
        "type": "stock",
        "last": 115.42,
        "change": -4.28,
        "volume": 7046192,
        "open": 120,
        "high": 121.945,
        "low": 115.03,
        "close": 115.42,
        "bid": 114.11,
        "ask": 115,
        "change_percentage": -3.58,
        "average_volume": 4793527,
        "last_volume": 377808,
        "trade_date": 1760126400192,
        "prevclose": 119.7,
        "week_52_high": 137.4,
        "week_52_low": 28.83,
        "bidsize": 1,
        "bidexch": "Q",
        "bid_date": 1760140720000,
        "asksize": 1,
        "askexch": "Q",
        "ask_date": 1760140544000,
        "root_symbols": "WDC,WDC1"
      },
      {
        "symbol": "AMD",
        "description": "Advanced Micro Devices Inc",
        "exch": "Q",
        "type": "stock",
        "last": 214.9,
        "change": -17.99,
        "volume": 118656636,
        "open": 232.77,
        "high": 234.22,
        "low": 213.2001,
        "close": 214.9,
        "bid": 215.12,
        "ask": 215.2,
        "change_percentage": -7.73,
        "average_volume": 55628230,
        "last_volume": 0,
        "trade_date": 1760127300013,
        "prevclose": 232.89,
        "week_52_high": 240.1,
        "week_52_low": 76.48,
        "bidsize": 2,
        "bidexch": "Q",
        "bid_date": 1760140799000,
        "asksize": 1,
        "askexch": "U",
        "ask_date": 1760140786000,
        "root_symbols": "AMD,AMD1"
      },
      {
        "symbol": "GME",
        "description": "GameStop Corp",
        "exch": "N",
        "type": "stock",
        "last": 23.3,
        "change": -0.77,
        "volume": 9744316,
        "open": 24.08,
        "high": 24.2,
        "low": 23.28,
        "close": 23.3,
        "bid": 23.3,
        "ask": 23.35,
        "change_percentage": -3.2,
        "average_volume": 8665599,
        "last_volume": 0,
        "trade_date": 1760137200001,
        "prevclose": 24.07,
        "week_52_high": 35.81,
        "week_52_low": 20.35,
        "bidsize": 83,
        "bidexch": "P",
        "bid_date": 1760140799000,
        "asksize": 4,
        "askexch": "P",
        "ask_date": 1760140780000,
        "root_symbols": "GME,GME1"
      }
    ]
  }
}
```



2. 'get_market_status_and_date_time' to use Tradier Endpoint:

Here is a the example API endpoint Python Call & Response :

```
import requests

url = "https://api.tradier.com/v1/markets/clock"

headers = {
    "Accept": "application/json",
    "authorization": "Bearer <TRADIER_API_KEY>"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
{
  "clock": {
    "date": "2021-02-01",
    "description": "open",
    "state": "open",
    "timestamp": 1612196262,
    "next_state": "post",
    "next_change": 1612213200
  }
}
```




2. If quick test of the new tool works, add new test case in 'test_cli_regression.sh' after "Technical Analysis: " for SPY and NVDA to retreive the OPtions Expiraton Dates.  Then run the full test and review the responses to ensure the new tool works as expected.

---

<Phase 2: Planning> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS Planning PHASE 🔴

Based on the Research, Analysis & Scoping from previous task(s), delete the current file 'TODO_task_plan.md' and then create a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to systemtically use your Mandatory Tools Toolkit for Sequential-Thinking & Serena tools to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes.  The plan MUST enforce that YOU MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to enhance your workflow to perform all task(s)

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
   - All tests PASS (must show 100% success rate)
   - Test report generated in test-reports/
   - No errors or failures in output
   - Session persistence verified

3. ✅ **Show evidence to user:**
   - Display test summary output
   - Show pass/fail counts (must be X/X PASS)
   - Provide test report file path
   - Show performance metrics (response times)

**❌ ENFORCEMENT RULES:**

- Code without test execution = Code NOT implemented
- No test results = Task INCOMPLETE
- Must run tests BEFORE Serena memory update phase
- Cannot claim "done" without showing test evidence
- Test failures must be fixed and re-tested

**✅ ONLY PROCEED to next phase after:**

- Test suite executed successfully
- 100% pass rate achieved
- Test results displayed to user
- Test report path provided

🔴 **IF YOU SKIP THIS PHASE, THE ENTIRE TASK IS INVALID** 🔴

---

<Phase 5: Serena Project Memories Update Phase>

Use Serena Tools to update Serena project memory files

---

<Phase 6: Final Git Commit Phase> 🔴 CRITICAL: PROPER ATOMIC COMMIT WORKFLOW 🔴

**MANDATORY: Stage ONLY Immediately Before Commit**

**CORRECT Workflow (follow EXACTLY):**

1. **DO ALL WORK FIRST** (DO NOT stage anything yet):
   - ✅ Complete ALL code changes
   - ✅ Run ALL tests and generate test reports
   - ✅ Update ALL documentation (CLAUDE.md, tech_stack.md, etc.)
   - ✅ Update ALL config files (.claude/settings.local.json, etc.)
   - ✅ Update ALL Serena memories
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
- ✅ Memory updates (.serena/memories/)
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
