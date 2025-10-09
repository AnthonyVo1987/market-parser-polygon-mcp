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

1. Investigate & fix new tool 'get_call_options_chain' & 'get_put_options_chain' failures from 'tmp/cli_output_loop1_2025-10-09_10-26.log':

- Both new tools are incorrectly showing MORE than just 10x strikes, flooding the entire message.  It was supposed to be ENFORCED to have 10x total strikes MAX for EACH of the tool calls, so input parameters are incorrect by allowing more than 10x strikes fetched

2. Update 'test_cli_regression.sh' to now output the temporary test run log under the top level 'tmp' folder in the PROJECT.  Currently the logs are outputting to the ROOT LINUX 'tmp', which is system level and is a violation.. We should NOT be creating files or logs outside the scope of the project folder hierchy.

3. Validate by running 1x loop of 'test_cli_regression.sh' AND ACTUALLY VIEW THE RESPONSES AND DO NOT BLINDLY JUST SEE TEST PASSED WITHOUT SEEING THE ACTUAL CONTENT.  Fix any issues in code and\or script if needed After validating notify user to review results first, so do NOT proceed with serenea updates or commits yet until user reviews the latest test results of your fixes to confirm the issues are truly fixed or not.

---

<Planning Phase> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

Based on the Research, Analysis & Scoping from previous task(s), delete the current file 'TODO_task_plan.md' and then create a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to systemtically use your Mandatory Tools Toolkit for Sequential-Thinking & Serena tools to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes.  The plan MUST enforce that YOU MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to enhance your workflow to perform all task(s)

---

<Implementation Phase>

You MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to Implement all code changes, test suite updates, and agent instruction modifications according to the TODO_task_plan.md

---

<CLI Testing Phase> 🔴 MANDATORY CHECKPOINT - DO NOT SKIP 🔴

⚠️ __CRITICAL: You MUST run tests BEFORE claiming completion__ ⚠️
⚠️ __CRITICAL: Task is INCOMPLETE without test execution and results__ ⚠️

__REQUIRED ACTIONS:__

1. ✅ __Execute the test suite:__

   ```bash
   ./test_cli_regression.sh
   ```

2. ✅ __Verify test results:__
   - All tests PASS (must show 100% success rate)
   - Test report generated in test-reports/
   - No errors or failures in output
   - Session persistence verified

3. ✅ __Show evidence to user:__
   - Display test summary output
   - Show pass/fail counts (must be X/X PASS)
   - Provide test report file path
   - Show performance metrics (response times)

__❌ ENFORCEMENT RULES:__

- Code without test execution = Code NOT implemented
- No test results = Task INCOMPLETE
- Must run tests BEFORE Serena memory update phase
- Cannot claim "done" without showing test evidence
- Test failures must be fixed and re-tested

__✅ ONLY PROCEED to next phase after:__

- Test suite executed successfully
- 100% pass rate achieved
- Test results displayed to user
- Test report path provided

🔴 __IF YOU SKIP THIS PHASE, THE ENTIRE TASK IS INVALID__ 🔴

---

<Serena Update Memories Phase>

Update Serena memory files with new tool information, architecture changes, and test results (ONLY after tests pass)

---

<Final Git Commit Phase> 🔴 CRITICAL: PROPER ATOMIC COMMIT WORKFLOW 🔴

__MANDATORY: Stage ONLY Immediately Before Commit__

__CORRECT Workflow (follow EXACTLY):__

1. __DO ALL WORK FIRST__ (DO NOT stage anything yet):
   - ✅ Complete ALL code changes
   - ✅ Run ALL tests and generate test reports
   - ✅ Update ALL documentation (CLAUDE.md, tech_stack.md, etc.)
   - ✅ Update ALL config files (.claude/settings.local.json, etc.)
   - ✅ Update ALL Serena memories
   - ✅ Update ALL task plans
   - ⚠️ __DO NOT RUN `git add` YET__

2. __VERIFY EVERYTHING IS COMPLETE__:

   ```bash
   git status  # Review ALL changed/new files
   git diff    # Review ALL changes
   ```

   - Ensure ALL work is done
   - Ensure ALL files are present

3. __STAGE EVERYTHING AT ONCE__:

   ```bash
   git add -A  # Stage ALL files in ONE command
   ```

   - ⚠️ This is the FIRST time you run `git add`
   - ⚠️ Stage ALL related files together

4. __VERIFY STAGING IMMEDIATELY__:

   ```bash
   git status  # Verify ALL files staged, NOTHING unstaged
   ```

   - If anything is missing: `git add [missing-file]`

5. __COMMIT IMMEDIATELY__ (within 60 seconds of staging):

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

6. __PUSH IMMEDIATELY__:

   ```bash
   git push
   ```

__WHAT BELONGS IN ATOMIC COMMIT:__

- ✅ Code changes (backend + frontend)
- ✅ Test reports (evidence of passing tests)
- ✅ Documentation updates (CLAUDE.md, README.md, etc.)
- ✅ Memory updates (.serena/memories/)
- ✅ Config changes (.claude/settings.local.json, etc.)
- ✅ Task plan updates (TODO_task_plan.md, etc.)

__❌ NEVER DO THIS:__

- ❌ Stage files early during development
- ❌ Stage files "as you go"
- ❌ Run `git add` before ALL work is complete
- ❌ Delay between `git add` and `git commit`
- ❌ Commit without test reports
- ❌ Commit without documentation updates

__Reference:__ See `.serena/memories/git_commit_workflow.md` for complete details

---
