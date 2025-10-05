<Research Topic Details> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

- Create\Update tools specified below for our AI Agent using the Polygon Python Library & replace AI Agent Instructions to use the new custom tools instead of the MCP Tools:

1. Create New tool 'get_stock_quote_multi': 'client.get_snapshot_all' : Replaces currently used MCP Tool 'get_snapshot_all'
2. Create New tool 'get_options_quote_single': 'client.get_snapshot_option' : Replaces currently used MCP Tool 'get_snapshot_option'
3. Create New tool 'get_OHLC_custom_date_range': 'client.list_aggs' : Replaces currently used MCP Tool 'list_aggs'
4. Create New tool 'get_OHLC_bars_specific_date': 'client.get_daily_open_close_agg' : Replaces currently used MCP Tool 'get_daily_open_close_agg'
5. Create New tool 'get_OHLC_previous_close': 'client.get_previous_close_agg' : Replaces currently used MCP Tool 'get_previous_close_agg'
6. REMOVE allowed tool usage in AI Agent Prompt for 'get_aggs' completely because this tool is actually not relevant to any analysis for our app

- Read docs/OPENAI_CUSTOM_TOOLS_REFERENCE.md to guide on you on proper custom tool creation
- Review the commit 'e1ba319ad9e9d1a253e83961b85daf0d020f4163' to see previous implementation of a new custom tool
- Add new test cases to 'test_7_prompts_persistent_session.sh' to use the new tools and then run and test the new tools and script and verify all tests pass with the new test cases

---

<Planning Phase> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

Based on the Research, Analysis & Scoping from previous task(s), delete the current file 'TODO_task_plan.md' and then create a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' and completely for you to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info

---
