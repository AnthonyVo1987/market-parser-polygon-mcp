🔴 CRITICAL: FOLLOW THE ENTIRE WORKFLOW PHASES IN ORDER FOR THE REQUESTED NEW CHANGES. RESEARCH -> PLANNING -> IMPLEMENTATION -> TESTING -> COMMIT 🔴

---

<Phase 1: Research> ULTRA-THINK & systematically use relevant Research Tools Docs Gradio\OpenAI, Context7, Web Fetch etc to investigate the requested task(s). If needed, you may OPTIONALLY use sub-agents task(s) for parallel optimized performance and speed: 

[NEW_FEATURE] Update both Call and Put Options Chains Tools to now output additional strike prices that will now show 10 Immediate Strike Prices ABOVE AND BELOW the current price for both Call and Put Options Chain, for a total of 20 Strike prices EACH for both Calls and Puts centered around the current underlying price

- Current the Call Options Chain only outputs 10 immediate sequential strikes ABove the current price, and now Call options chain needs to also output 10 immediate sequential strikes BELOW the current price, for a total of 20 strikes

- Current the Put Options Chain only outputs 10 immediate sequential strikes Below the current price, and now Put options chain needs to also output 10 immediate sequential strikes ABOVE the current price, for a total of 20 strikes

- Now both Call and Put options chains will each haave identical strikes centered around the current price

- Both Call and Put options chain now will have to be sorted and output in DESCENDING Strike price order, with HIGHEST strikes at top of table, followed by the lower strikes 

- After Implementing, perform some basic manual bench testing of some manual CLI Test Prompts using 'uv run main.py' to test out a few manual Call\Put Options chain calls, and verify the output responses matches the new changes and the table\charts are formatted and sorted correctly.  Fix any issues if needed from manual CLI testing and re-run manual testing if needed until new feature has been validated with no issues.  <Phase 4: Testing> will be gated by these initial manual test prompts, so your test prompts MUST all pass first before proceeding to <Phase 4: Testing> CLI Regression

🔴 CRITICAL: After research is complete, Delete the current file 'reasearch_task_plan.md' WITHOUT READING IT and then ULTRA-THINK AND GENERATE a brand new 'reasearch_task_plan.md' based on the reasearch task(s)🔴

---

 <Phase 2: Planning>

Based on the latest Research, delete the current file 'TODO_task_plan.md' WITHOUT READING IT and then ULTRA-THINK AND GENERATE a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to systemtically use your Mandatory Tools Toolkit for Sequential-Thinking & Serena tools to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes.  The plan MUST enforce that YOU MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to enhance your workflow to perform all task(s). If needed, you may OPTIONALLY use sub-agents task(s) for parallel optimized performance and speed

---

<Phase 3: Implementation> 🔴 CRITICAL: NOW YOU MAY START IMPLEMENTING DURING THIS PHASE 🔴

You MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to Implement all code changes, test suite updates, and agent instruction modifications according to the TODO_task_plan.md using sub-agents task(s). If needed, you may OPTIONALLY use sub-agents task(s) for parallel optimized performance and speed

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
