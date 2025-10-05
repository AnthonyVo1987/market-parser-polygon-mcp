<Research Topic Details> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

- Completely remove and retire ALL the Polygon MCP Tools and Polygon Server Creation Endpoints. Our recent commit in 'fe380fa4a96369a6a518b70656bae0c4e0c8c9a3' has fully migrated to use direct Polygon Python API calls instead of using the default Polygon MCP Server Tools.  So since our custom Polygon Python API tool migration has passed, we can completely eliminate anything related to Polygon MCP Server
- ALL AI Agent Instructions and Prompts needs to completely remove all and any reference to previous Polygon MCP Server tools to avoid confusion
- ALL project docs need to completely remove to completely remove all and any reference to previous Polygon MCP Server tools to avoid confusion
- Serena Tools must be used to update any and all Serena memories to to completely remove all and any reference to previous Polygon MCP Server tools to avoid confusion
- Expected Outcome - Absolutly no references in code, comments, docs, memories, or any in the project that references legacy Polygon MCP Server tools to avoid confusion

---

<Planning Phase> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

Based on the Research, Analysis & Scoping from previous task(s), delete the current file 'TODO_task_plan.md' and then create a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes.

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
