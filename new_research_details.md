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

1. Research updating migrating and replacing some AI Agent tools to use Tradier API Endpoints
- https://docs.tradier.com/reference/brokerage-api-markets-get-history
- Update AI Agent instructions for the updated tools
- Test the new tools by issueing some manual CLI test cases to confirm the new tool API endpoints are working correctly
- Fix any issues if needed from testing to make the tool tests work properly


1. NEW tool 'get_stock_price_history' that uses the Tradier API "Get historical pricing" Endpoint:
- The new Tradier 'get_stock_price_history' tool allows different time interval input parameters from a single tool: Daily(default), Weekly, Monthly
- The new tool also takes a date range with a start date and end date
- With this single tool, the AI Agent can then retrieve any type of historical data from any time interval, all in a single tool call
- So since this single tool call can handle so many different history stock price time intervals, you will need to completely remove the now deperacated Polygon Tools: get_OHLC_bars_custom_date_range, get_OHLC_bars_specific_date, get_OHLC_bars_previous_close
- This should optimize AI Agent performance even more because a single tool can handle all history data time interval scenarios, instead of using the legacy polygon tools that needed separate tools for separate date ranges.

Here is a the example API endpoint Python Call & Response :


Daily Time Inteval:
```
import requests

url = "https://api.tradier.com/v1/markets/history?symbol=SPY&interval=daily&start=2025-01-01&end=2025-01-10"

headers = {
    "Accept": "application/json",
    "authorization": "Bearer 8XP1DYNiWBSOLfCIXtEmJ4NeRIEC"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
{
  "history": {
    "day": [
      {
        "date": "2025-01-02",
        "open": 589.39,
        "high": 591.13,
        "low": 580.5,
        "close": 584.64,
        "volume": 50203975
      },
      {
        "date": "2025-01-03",
        "open": 587.53,
        "high": 592.6,
        "low": 586.43,
        "close": 591.95,
        "volume": 37888459
      },
      {
        "date": "2025-01-06",
        "open": 596.27,
        "high": 599.7,
        "low": 593.6,
        "close": 595.36,
        "volume": 47679442
      },
      {
        "date": "2025-01-07",
        "open": 597.42,
        "high": 597.75,
        "low": 586.78,
        "close": 588.63,
        "volume": 60393052
      },
      {
        "date": "2025-01-08",
        "open": 588.7,
        "high": 590.5799,
        "low": 585.195,
        "close": 589.49,
        "volume": 47304672
      },
      {
        "date": "2025-01-10",
        "open": 585.88,
        "high": 585.95,
        "low": 578.55,
        "close": 580.49,
        "volume": 73105046
      }
    ]
  }
}
```


Weekly Time Inteval:
```
import requests

url = "https://api.tradier.com/v1/markets/history?symbol=SPY&interval=weekly&start=2025-01-01&end=2025-01-15"

headers = {
    "Accept": "application/json",
    "authorization": "Bearer 8XP1DYNiWBSOLfCIXtEmJ4NeRIEC"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
{
  "history": {
    "day": [
      {
        "date": "2025-01-06",
        "open": 596.27,
        "high": 599.7,
        "low": 578.55,
        "close": 580.49,
        "volume": 228482210
      },
      {
        "date": "2025-01-13",
        "open": 575.77,
        "high": 599.36,
        "low": 575.35,
        "close": 597.58,
        "volume": 254621090
      }
    ]
  }
}
```


Monthly Time Inteval:
```
import requests

url = "https://api.tradier.com/v1/markets/history?symbol=SPY&interval=monthly&start=2025-01-01&end=2025-06-01"

headers = {
    "Accept": "application/json",
    "authorization": "Bearer 8XP1DYNiWBSOLfCIXtEmJ4NeRIEC"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
{
  "history": {
    "day": [
      {
        "date": "2025-01-01",
        "open": 589.39,
        "high": 610.78,
        "low": 575.35,
        "close": 601.82,
        "volume": 995605960
      },
      {
        "date": "2025-02-01",
        "open": 592.67,
        "high": 613.23,
        "low": 582.44,
        "close": 594.18,
        "volume": 871641460
      },
      {
        "date": "2025-03-01",
        "open": 596.18,
        "high": 597.34,
        "low": 546.87,
        "close": 559.39,
        "volume": 1496972100
      },
      {
        "date": "2025-04-01",
        "open": 557.45,
        "high": 567.42,
        "low": 481.8,
        "close": 554.54,
        "volume": 2237015100
      },
      {
        "date": "2025-05-01",
        "open": 560.37,
        "high": 595.54,
        "low": 556.04,
        "close": 589.39,
        "volume": 1402418500
      },
      {
        "date": "2025-06-01",
        "open": 587.76,
        "high": 619.22,
        "low": 585.06,
        "close": 617.85,
        "volume": 1495568000
      }
    ]
  }
}
```


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
