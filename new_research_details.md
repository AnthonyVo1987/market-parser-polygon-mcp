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

A. Update AI Agent Instructions to now allow parallel tool calls IF needed, and a max of 3x Parallel tool calls only.  If a request requires more than 3+ parallel tool calls, then AI Agent needs to perform the first batch of 3x Paralell tool calls, and then afterwards, issuing additional tool calls as needed, only providing final response when ALL tool calls are done. This will allow AI Agent to analyze use request to decide whether not parallel tool calls are needed or not, and if parallel tool calls needed, only a max of 3x Parallel tool calls to help reduce any changes of rate limiting. Not all user requests will need parallel tool calls, so AI Agent Instructions need to be updated to analyze the request holistically. If the request can be done with single\minimal tool calls, then AI Agent needs to do this. Or if AI Agent analyzed and thinks parallel tool calls will help, then allow it.  So tool calling will be updates to be dynamic according to the complexity of the user request(s)

B. Update AI Agent Instructions to now also dynamically and holistically decide whether tool calls are even needed for the user request, based on real world usage where User may ask multiple questions in a row for the same ticker, and also have some analysis done based on all the data already received from previous tool calls. This will test a scenario where AI Agent may have all the data it already needs in the chat, and can just use the existing data to anlayze instead of wasting tokens with redudant tool calls when AI Agent already has enough info.  For exmaple, if AI Agent already used tools to retreive some Technical Analysis Data, and then user request to provide technical analysis , AI agent can check if they already have enough data to perform the analysis or not without additional tool calls or not, and the decide if they can answer with or without additional tool calls.  This mimics real AI Chatbot usage where AI Chatbots can use any current info from the existing chat to provide more context and background to respond to the user.  If AI Agent has enough data, context, background  to respond without needing tool calls, then AI Agent can skip the tool calls.  If AI Agent needs additional info that only a tool call can provide, then AI Agent needs to perform the tool call(s)

C. Create a brand new 'test_cli_regression.sh' based on current 'CLI_test_regression.sh' to re-work test script to allow parallel tool calls and test AI Agent dyanmic ablility to decide if additional tool calls are needed based on already existing data retrieved. Here is the brand new test plan that matches user real world usage and will completely replace the current test plan.  We will keep the current 'CLI_test_regression.sh' for backward compatilibilty and serve as reference template for the new script just in case the new script has any issues.  The new script also needs to change the output test report formatting for better spacing for the date and timestamps.   Currenly it is something like "test_cli_regression_loop10_20251006_123556.txt", but the new way needs to make it more clear like: "test_cli_regression_loop10_2025-10-06_12-35.txt", where "2025-10-06" makes clear the date, and "12-35"  makes clear the time WITHOUT seconds, so just hours and minutes.  Also update 'CLI_test_regression.sh' with the new test report naming scheme too.

Here are the brand new test cases in sequence for 'test_cli_regression.sh'

Here is the consolidated and sequentially numbered list of your test cases:

// SPY Test Sequence
1.  Market Status
2.  Current Price: SPY
3.  Today’s Closing Price: SPY
4.  Previous Closing Price: SPY
5.  Current Weekly Performance Change $ and %: SPY
6.  RSI-14: SPY
7.  MACD: SPY
8.  SMA 20/50/200: SPY
9.  EMA 20/50/200: SPY
10. SMA 5/10: SPY
11. EMA 5/10: SPY
12. Options Quote: SPY 1/16/26 $700 Call
13. Options Quote: SPY 1/16/26 $600 Put
14. Support & Resistance Levels: SPY
15. Technical Analysis: SPY
16. Price on 1/1/25: SPY
17. Daily bars from 1/1/25 - 3/31/25: SPY

// NVDA Test Sequence
18. Market Status
19. Current Price: NVDA
20. Today’s Closing Price: NVDA
21. Previous Closing Price: NVDA
22. Current Weekly Performance Change $ and %: NVDA
23. RSI-14: NVDA
24. MACD: NVDA
25. SMA 20/50/200: NVDA
26. EMA 20/50/200: NVDA
27. SMA 5/10: NVDA
28. EMA 5/10: NVDA
29. Options Quote: NVDA 1/16/26 $200 Call
30. Options Quote: NVDA 1/16/26 $180 Put
31. Support & Resistance Levels: NVDA
32. Technical Analysis: NVDA
33. Price on 1/1/25: NVDA
34. Daily bars from 1/1/25 - 3/31/25: NVDA

// WDC Test Sequence
35. Market Status
36. Current Price: WDC
37. Today’s Closing Price: WDC
38. Previous Closing Price: WDC
39. Current Weekly Performance Change $ and %: WDC
40. RSI-14: WDC
41. MACD: WDC
42. SMA 20/50/200: WDC
43. EMA 20/50/200: WDC
44. SMA 5/10: WDC
45. EMA 5/10: WDC
46. Options Quote: WDC 1/16/26 $150 Call
47. Options Quote: WDC 1/16/26 $100 Put
48. Support & Resistance Levels: WDC
49. Technical Analysis: WDC
50. Price on 1/1/25: WDC
51. Daily bars from 1/1/25 - 3/31/25: WDC

// Multi-Ticker Test Test Sequence
52. Current Price: AMD, INTC, AVGO
53. Today’s Closing Price: AMD, INTC, AVGO
54. Previous Closing Price: AMD, INTC, AVGO
55. Current Weekly Performance Change $ and %: AMD, INTC, AVGO
56. RSI-14: AMD, INTC, AVGO
57. MACD: AMD, INTC, AVGO
58. SMA 20/50/200: AMD, INTC, AVGO
59. EMA 20/50/200: AMD, INTC, AVGO
60. SMA 5/10: AMD, INTC, AVGO
61. EMA 5/10: AMD, INTC, AVGO
62. Support & Resistance Levels: AMD, INTC, AVGO
63. Technical Analysis: AMD, INTC, AVGO
64. Price on 1/1/25: AMD, INTC, AVGO
65. Daily bars from 1/1/25 - 3/31/25: AMD, INTC, AVGO


D. Validate ALL changes by running the new validation script 1x loop 'test_CLI_regression.sh' and then reviewing final results and contents of EACH response to ensure they match expected responses with proper tool calls

E. Validate ALL changes by running the new validation script 3x loops 'test_CLI_regression.sh' and then reviewing final results and contents of EACH response to ensure they match expected responses with proper tool calls


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
   ./CLI_test_regression.sh
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
