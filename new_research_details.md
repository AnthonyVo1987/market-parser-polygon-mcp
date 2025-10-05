<Research Topic Details> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

- Create\Update tools specified below for our AI Agent using the Polygon Python Library & replace AI Agent Instructions to use the new custom tools instead of the MCP Tools:

1. Create New tool 'get_stock_quote_multi': 'client.get_snapshot_all' : Replaces currently used MCP Tool 'get_snapshot_all'
2. Create New tool 'get_options_quote_single': 'client.get_snapshot_option' : Replaces currently used MCP Tool 'get_snapshot_option'
3. Create New tool 'get_OHLC_bars_custom_date_range': 'client.list_aggs' : Replaces currently used MCP Tool 'list_aggs'
4. Create New tool 'get_OHLC_bars_specific_date': 'client.get_daily_open_close_agg' : Replaces currently used MCP Tool 'get_daily_open_close_agg'
5. Create New tool 'get_OHLC_bars_previous_close': 'client.get_previous_close_agg' : Replaces currently used MCP Tool 'get_previous_close_agg'
6. REMOVE allowed tool usage in AI Agent Prompt for 'get_aggs' completely because this tool is actually not relevant to any analysis for our app

- Read docs/OPENAI_CUSTOM_TOOLS_REFERENCE.md to guide on you on proper custom tool creation
- Review the commit 'e1ba319ad9e9d1a253e83961b85daf0d020f4163' to see previous implementation of a new custom tool
- Add new test cases to 'test_7_prompts_persistent_session.sh' to use the new tools and then run and test the new tools and script and verify all tests pass with the new test cases

---

<Planning Phase> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

Based on the Research, Analysis & Scoping from previous task(s), delete the current file 'TODO_task_plan.md' and then create a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' and completely for you to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info

---

<Implementation Phase>

Implement all code changes, test suite updates, and agent instruction modifications according to the TODO_task_plan.md

---

<CLI Testing Phase> 🔴 MANDATORY CHECKPOINT - DO NOT SKIP 🔴

⚠️ **CRITICAL: You MUST run tests BEFORE claiming completion** ⚠️
⚠️ **CRITICAL: Task is INCOMPLETE without test execution and results** ⚠️

**REQUIRED ACTIONS:**

1. ✅ **Execute the test suite:**
   ```bash
   ./test_16_prompts_persistent_session.sh
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
