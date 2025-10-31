🔴 CRITICAL: FOLLOW THE ENTIRE WORKFLOW PHASES IN ORDER FOR THE REQUESTED NEW CHANGES. RESEARCH -> PLANNING -> IMPLEMENTATION -> MANUAL TESTING -> FULL REGRESSION TESTING -> COMMIT 🔴

---

<Phase 1: Research> ULTRA-THINK & systematically use relevant Research Tools Docs Gradio\OpenAI, Context7, Web Fetch etc to investigate the requested task(s). If needed, you may OPTIONALLY use sub-agents task(s) for parallel optimized performance and speed: 

1. Completely remove the options chain 'Gamma' data from the options chain tool and corresponding table\chart outputs
- We no longer need Gamma for the options chain data, so remove it all

2. Investigate and fix the current incorrect table\chart formatting columns\rows\borders spacing & alignment for the Vol & OI options chain columns and data
- Both Vol & OI table\charts are misaligned due to varying data values that are longer than the current Vol & OI column and data widths
- issue is because depending on the ticker, Vol\IO could vary from digits 'x' - 'xx,xxx', which then will cause misalignment
- So lets just hard code both Vol & IO columns and the corresponding right aligned data to support "XXX,XXX" columns widths for both
- This should handle values starting from x to xxx,xxx
- For Validation and testing, you MUST visually inspect and compare the tables\chart alignment WITH white spaces AND the data rows too, and not JUST headers
- I added some comments and arrows to point out misalignments with "// <-  misalignment"

- Bad case for Vol & OI
```
NVDA Call & Put Options Chains Expiring Friday 2025-11-07

Call Options Chain (Expiring 2025-11-07)
Current Price: 202.89

| Strike ($) | Bid ($) | Ask ($) | Delta |   Vol   |   OI    |  IV  | Gamma |
| ---------: | ------: | ------: | ----: | ------: | ------: | ---: | ----: |
|    $227.50 |   $0.22 |   $0.24 |  0.06 |   1,437 |   1,260 |  44% |  0.01 |
|    $225.00 |   $0.29 |   $0.31 |  0.08 |  10,686 |  29,655 |  43% |  0.01 |
|    $222.50 |   $0.39 |   $0.41 |  0.10 |   3,550 |   1,960 |  42% |  0.01 |
|    $220.00 |   $0.52 |   $0.54 |  0.12 |  50,326 |  42,960 |  41% |  0.01 |
|    $217.50 |   $0.73 |   $0.76 |  0.15 |  14,431 |   9,435 |  40% |  0.02 |
|    $215.00 |   $1.05 |   $1.07 |  0.19 |  20,964 |  36,507 |  39% |  0.02 |
|    $212.50 |   $1.47 |   $1.51 |  0.23 |  10,327 |   3,942 |  39% |  0.03 |
|    $210.00 |   $2.08 |   $2.13 |  0.29 |  78,007 |  50,946 |  39% |  0.03 |
|    $207.50 |   $2.85 |   $3.50 |  0.36 |  11,786 |   7,419 |  39% |  0.03 |
|    $205.00 |   $3.85 |   $3.95 |  0.45 |  32,704 |  25,698 |  39% |  0.04 |
|    $202.50 |   $5.10 |   $5.20 |  0.54 |  11,887 |  12,321 |  40% |  0.04 |
|    $200.00 |   $6.55 |   $6.70 |  0.62 |  21,892 |  37,948 |  41% |  0.03 |
|    $197.50 |   $8.20 |   $8.40 |  0.70 |  1,956 |   4,918 |  42% |  0.03 |  // <-  misalignment
|    $195.00 |  $10.05 |  $10.25 |  0.75 |  3,744 |  31,339 |  43% |  0.02 |  // <-  misalignment
|    $192.50 |  $11.00 |  $12.25 |  0.79 |   979 |   3,893 |  45% |  0.02 |   // <-  misalignment
|    $190.00 |  $14.15 |  $14.45 |  0.82 |  3,170 |  16,283 |  47% |  0.02 |  // <-  misalignment
|    $187.50 |  $16.15 |  $16.70 |  0.85 |   604 |   5,715 |  49% |  0.01 |   // <-  misalignment
|    $185.00 |  $18.70 |  $18.90 |  0.87 |   850 |  17,708 |  51% |  0.01 |   // <-  misalignment
|    $182.50 |  $20.75 |  $21.35 |  0.89 |   249 |   2,412 |  54% |  0.01 |   // <-  misalignment
|    $180.00 |  $23.45 |  $23.75 |  0.91 |   694 |  10,300 |  56% |  0.01 |   // <-  misalignment

Put Options Chain (Expiring 2025-11-07)
Current Price: 202.89

| Strike ($) | Bid ($) | Ask ($) | Delta |   Vol   |   OI    |  IV  | Gamma |
| ---------: | ------: | ------: | ----: | ------: | ------: | ---: | ----: |
|    $227.50 |  $24.55 |  $24.95 | -0.94 |       8 |     197 |  44% |  0.01 |
|    $225.00 |  $22.05 |  $22.45 | -0.92 |      50 |     510 |  43% |  0.01 |
|    $222.50 |  $19.75 |  $20.00 | -0.90 |     181 |     410 |  42% |  0.01 |
|    $220.00 |  $17.35 |  $17.60 | -0.88 |     123 |     788 |  41% |  0.01 |
|    $217.50 |  $15.05 |  $15.40 | -0.85 |     102 |     865 |  40% |  0.02 |
|    $215.00 |  $12.85 |  $13.10 | -0.81 |     289 |     962 |  39% |  0.02 |
|    $212.50 |   $9.70 |  $11.00 | -0.77 |     349 |   1,298 |  39% |  0.03 |
|    $210.00 |   $8.90 |   $9.10 | -0.71 |   1,745 |   5,047 |  39% |  0.03 |
|    $207.50 |   $7.20 |   $7.40 | -0.64 |   1,577 |   2,341 |  39% |  0.03 |
|    $205.00 |   $5.75 |   $5.90 | -0.55 |   7,988 |   4,962 | 39% | 0.04 |   // <-  misalignment
|    $202.50 |   $4.50 |   $4.60 | -0.46 |   7,807 |   2,048 | 40% | 0.04 |   // <-  misalignment
|    $200.00 |   $3.45 |   $3.55 | -0.38 |  20,964 |   9,546 | 41% | 0.03 |   // <-  misalignment
|    $197.50 |   $2.67 |   $2.70 | -0.30 |   6,221 |   3,099 | 42% | 0.03 |   // <-  misalignment
|    $195.00 |   $2.05 |   $2.10 | -0.25 |  10,613 |  27,016 | 43% | 0.02 |   // <-  misalignment
|    $192.50 |   $1.55 |   $1.61 | -0.21 |   5,878 |   6,484 | 45% | 0.02 |   // <-  misalignment
|    $190.00 |   $1.19 |   $1.21 | -0.18 |  11,500 |  11,531 | 47% | 0.02 |   // <-  misalignment
|    $187.50 |   $0.92 |   $0.98 | -0.15 |   2,569 |   8,456 | 49% | 0.01 |   // <-  misalignment
|    $185.00 |   $0.73 |   $0.75 | -0.13 |   6,668 |  12,655 | 51% | 0.01 |   // <-  misalignment
|    $182.50 |   $0.59 |   $0.61 | -0.11 |   3,074 |   3,806 | 54% | 0.01 |   // <-  misalignment
|    $180.00 |   $0.49 |   $0.51 | -0.09 |   3,454 |  23,595 | 56% | 0.01 |   // <-  misalignment
```



🔴 CRITICAL: After research is complete, Delete the current file 'reasearch_task_plan.md' WITHOUT READING IT and then ULTRA-THINK AND GENERATE a brand new 'reasearch_task_plan.md' based on the reasearch task(s)🔴

---

<Phase 2: Planning>

Based on the latest Research, delete the current file 'TODO_task_plan.md' WITHOUT READING IT and then ULTRA-THINK AND GENERATE a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to systemtically use your Mandatory Tools Toolkit for Sequential-Thinking & Serena tools to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes. The plan MUST enforce that YOU MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to enhance your workflow to perform all task(s). If needed, you may OPTIONALLY use sub-agents task(s) for parallel optimized performance and speed

---

<Phase 3: User Plan Approval>

Notify user to review and approve 'TODO_task_plan.md' before starting ANY implementation.  This Approval Phase is a GATE until <Phase 4: Implementation> 

---

<Phase 4: Implementation> 🔴 CRITICAL: NOW YOU MAY START IMPLEMENTING DURING THIS PHASE 🔴

ONLY IF USER APPROVES 'TODO_task_plan.md',  THE You MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to Implement all code changes, test suite updates, and agent instruction modifications according to the TODO_task_plan.md using sub-agents task(s). If needed, you may OPTIONALLY use sub-agents task(s) for parallel optimized performance and speed

---

<Phase 5: Manual Targeted Testing>

  🔴 MANDATORY CHECKPOINT - DO NOT SKIP 🔴

⚠️ **CRITICAL: You MUST run tests BEFORE claiming completion** ⚠️
⚠️ **CRITICAL: Task is INCOMPLETE without test execution and results** ⚠️


- After <Phase 4: Implementation>, perform some basic manual bench testing of some manual Test Prompts using 'uv run market-parser' to test out targeted prompts to ensure the new changes do NOT break any current capability, and verify the output responses matches the new changes and the table\charts are formatted and sorted correctly.  Fix any issues if needed from manual testing and re-run manual testing if needed until new changes have been validated with no issues. <Phase 5: Full Regression Testing> will be gated by these initial manual test prompts, so your test prompts MUST all pass first before proceeding to <Phase 5: Full Regression Testing>
- Manual Testing REQUIRES interactive input and visual inspection - that's the entire point of manual testing
- YOU MUST VISUALY INSPECT TABLES\CHARTS Borders\Columns\Rows alignment of the data AND the white space to ensure alignment; fix any issues if needed for proper white space alignment of tables\charts

---

<Phase 6: Full Regression Testing>

  🔴 MANDATORY CHECKPOINT - DO NOT SKIP 🔴

⚠️ **CRITICAL: You MUST run tests BEFORE claiming completion** ⚠️
⚠️ **CRITICAL: Task is INCOMPLETE without test execution and results** ⚠️

**REQUIRED ACTIONS:**

1. ✅ **Execute the test suite WITH A TIMEOUT OF 10 MINUTES TO LET THE FULL TEST RUN:**

   ```bash
   chmod +x test_cli_regression.sh && ./test_cli_regression.sh
   ```

2. ✅ **Verify test results:**
   🔴 MANDATORY - VERIFY THE CONTENT OF EACH TEST PROMPT RESPONSE THAT IT MATCHES THE EXPECTED RESPONSE, PROPER TOOL CALLS, AND RESPONSE FORMATTING🔴
   - PASS CRITERIA: CONTENT OF TEST PROMPT RESPONS MATCHES THE EXPECTED RESPONSE, PROPER TOOL CALLS, AND RESPONSE FORMATTING
   - YOU MUST VISUALY INSPECT TABLES\CHARTS Borders\Columns\Rows alignment of the data AND the white space to ensure alignment; fix any issues if needed for proper white space alignment of tables\charts
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

<Phase 7: Final Git Commit Phase> 🔴 CRITICAL: PROPER ATOMIC COMMIT WORKFLOW 🔴

**MANDATORY: Stage ONLY Immediately Before Commit**

**CORRECT Workflow (follow EXACTLY):**

1. **DO ALL WORK FIRST** (DO NOT stage anything yet):
   - ✅ Complete ALL code changes
   - ✅ Run ALL tests and generate test reports
   - ✅ Update ALL documentation (CLAUDE.md, tech_stack.md, etc.)
   - ✅ Ensure CLAUDE.md Last Task Completed Summary Update has a MAXIMUM of 20 lines for a high level overview of the last task completed
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
