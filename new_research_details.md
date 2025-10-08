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

<Research Topic Details> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

1. Change current "service_tier": "flex" to "service_tier": "default" in src/backend/services/agent_service.py to fix OPenAI Compute Resources Rate Limiting issues using "flex" service_tier.  Flex is cheaper, BUT has lower performance, so we wil ljust use service_tier default for now since we are still prototyping and testing.  In the future, there will be a TBD feature to put back flex and have a fallback to default in case we got rate limited, but for now , we will go with just default.

2. Update test script 'test_cli_regression.sh' with test cases changes that re-order the testing sequences & modifies some test cases:
'

   # SPY Test Sequence

    "Market Status"
    "Current Price: \$SPY"
    "Today's Closing Price: \$SPY"
    "Yesterday's Closing Price: \$SPY"
    "Last week's Performance: \$SPY"
    "Stock Price on the previous week's Friday: \$SPY"
    "Daily Stock Price bars Analysis from the last 2 trading weeks: \$SPY"
    "RSI-14: \$SPY"
    "MACD: \$SPY"
    "SMA 20/50/200: \$SPY"
    "EMA 20/50/200: SPY"
    "Support & Resistance Levels: \$SPY"
    "Technical Analysis: \$SPY"
    "Get First 3 Call Option Quotes expiring this Friday above current price (show strike prices): \$SPY"
    "Get First 3 Put Option Quotes expiring this Friday below current price (show strike prices): \$SPY"

   # NVDA Test Sequence

    "Market Status"
    "Current Price: \$NVDA"
    "Today's Closing Price: \$NVDA"
    "Yesterday's Closing Price: \$NVDA"
    "Last week's Performance: \$NVDA"
    "Stock Price on the previous week's Friday: \$NVDA"
    "Daily Stock Price bars Analysis from the last 2 trading weeks: \$NVDA"
    "RSI-14: \$NVDA"
    "MACD: \$NVDA"
    "SMA 20/50/200: \$NVDA"
    "EMA 20/50/200: NVDA"
    "Support & Resistance Levels: \$NVDA"
    "Technical Analysis: \$NVDA"
    "Get First 3 Call Option Quotes expiring this Friday above current price (show strike prices): \$NVDA"
    "Get First 3 Put Option Quotes expiring this Friday below current price (show strike prices): \$NVDA"

   # Multi-Ticker Test Sequence

    "Market Status"
    "Current Price: \$WDC, \$AMD, \$GME"
    "Today's Closing Price: \$WDC, \$AMD, \$GME"
    "Yesterday's Closing Price: \$WDC, \$AMD, \$GME"
    "Last week's Performance: \$WDC, \$AMD, \$GME"
    "Daily bars Analysis from the last 2 trading weeks: \$WDC, \$AMD, \$GME"
'

3. Validate updated 'test_cli_regression.sh' test script with the new test casee and verify and confirm results are expected

---

<Planning Phase> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

Based on the Research, Analysis & Scoping from previous task(s), delete the current file 'TODO_task_plan.md' and then create a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to systemtically use your Mandatory Tools Toolkit for Sequential-Thinking & Serena tools to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes.  The plan MUST enforce that YOU MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to enhance your workflow to perform all task(s)

---

<Implementation Phase>

You MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to Implement all code changes, test suite updates, and agent instruction modifications according to the TODO_task_plan.md

---

<CLI Testing Phase> 🔴 MANDATORY CHECKPOINT - DO NOT SKIP 🔴

⚠️ **CRITICAL: You MUST run tests BEFORE claiming completion** ⚠️
⚠️ **CRITICAL: Task is INCOMPLETE without test execution and results** ⚠️

**REQUIRED ACTIONS:**

1. ✅ **Execute the test suite:**

   ```bash
   ./test_cli_regression.sh
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

<Serena Update Memories Phase>

Update Serena memory files with new tool information, architecture changes, and test results (ONLY after tests pass)

---

<Final Git Commit Phase> 🔴 CRITICAL: PROPER ATOMIC COMMIT WORKFLOW 🔴

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
