🔴 CRITICAL: FOLLOW THE ENTIRE WORKFLOW PHASES IN ORDER FOR THE REQUESTED NEW CHANGES. RESEARCH -> PLANNING -> IMPLEMENTATION -> TESTING -> COMMIT 🔴

---

<Phase 1: Research> ULTRA-THINK & systematically use relevant Research Tools Docs Gradio\OpenAI, Context7, Web Fetch etc to investigate the requested task(s) using sub-agents task(s) for parallel optimized performance and speed when applicable:


## Task 1: Refactor\Re-architecture folder and file hierarchy after all the code cleanup and app re-architecture

Context
- Now that we have refactored, cleaned up, and re-architectured our app, now let's refactor\re-architecture the folder and file hierarchy & file naming schemes. 
- Previously we had separate folders for frontend vs back end due to the REACT frontend, FastAPI etc.
- But now that everything has been consolidated, retired, & migrated to a full Python stack, We need to also optimize our file and folder hierarchy

Expected Outcomes & Requirements:
- The CLI app should be made to run by issuing the Python standard 'uv run main.py' to match standard Python apps
- However, this would then call the CLI back end. Because right now we are trying to directly call the CLI back end, but we can't run it from the UV because it's being run as a module, IE. currently uses 'uv run src/backend/cli.py' and\or 'uv run python -m src.backend.cli', which is non standardized python uv convention. 
- Completely remove references to a backend folder, So instead of having separate backend and frontend folders, we could just have a single folder for all the source code in 'src'. 
- Instead of having separate folders to organize, we'll just add file naming prefixes to help designate and identify files that belong to backend or front end. 
- So any backend related files should have the 'backend_xxx' prefix, any front-end related files for radio should have the 'frontend_xxx' prefix, anything tool related should have a 'tool_xxx' prefix, config files 'config_xxx' prefix xxx 
- So reorganize\rename also any other files that can also be consolidated to a more optimized file structure with standardize file naming convention prefixes
- This will reduce the amount of code so all the code is in a single folder, with a single '__init__.py'.  That way, any AI agents or new users can quickly grep or search for files and quickly look at the file name prefix to know whether it belongs to the backend\frontend\config\tool etc
-  That way, they don't have to navigate to a backend folder versus a frontend folder etc So everything's in a single folder. 
- It may look messy initially, but with the file name prefixes, it becomes organized. 
- For example, now anytime an AI agent wants to grep or search for frontend, they can just search for the 'frontend_xxx' wildcard, and they can see all the file & hits. 
-  That way, they don't have to navigate to a folder here or a folder there and then we don't need to have multiple folders, and then multiple different '__init__.py' per folder 
- Because our project is still prototyping and not too complex, We don't quite need the enterprise level convention, folder\file hierarchy, where different components and domains are stored in different folders. We're not at that stage yet. So we'll simplify the file and folder naming hierarchy.

## Task 2: Implement\Enable Gradio PWA (Progressive Web App) & Gradio Hot Reload feature


🔴 CRITICAL: After research is complete, Delete the current file 'reasearch_task_plan.md' WITHOUT READING IT and then ULTRA-THINK AND GENERATE a brand new 'reasearch_task_plan.md' based on the reasearch task(s)🔴

---

<Phase 2: Planning>

Based on the latest Research, Analysis & Scoping 'reasearch_task_plan.md', delete the current file 'TODO_task_plan.md' WITHOUT READING IT and then ULTRA-THINK AND GENERATE a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to systemtically use your Mandatory Tools Toolkit for Sequential-Thinking & Serena tools to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes.  The plan MUST enforce that YOU MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to enhance your workflow to perform all task(s) & using sub-agents task(s) for parallel optimized performance and speed when applicable:

---

<Phase 3: Implementation> 🔴 CRITICAL: NOW YOU MAY START IMPLEMENTING DURING THIS PHASE 🔴

You MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to Implement all code changes, test suite updates, and agent instruction modifications according to the TODO_task_plan.md using sub-agents task(s) for parallel optimized performance and speed when applicable:

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
