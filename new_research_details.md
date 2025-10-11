# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

🔴 CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process

## 🔴 MANDATORY: SYSTEMATIC TOOL USAGE ENFORCEMENT

**YOU MUST use Sequential-Thinking and Serena tools throughout ENTIRE implementation:**

- **START every phase** with Sequential-Thinking for systematic approach
- **Use Serena tools** for code analysis, symbol manipulation, pattern searches
- **Use Sequential-Thinking** repeatedly for complex reasoning and planning
- **Use Standard Read/Write/Edit** only when Serena doesn't support the specific operation
- **NEVER stop using advanced tools** until task completion

**VIOLATION = FAILURE**

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation


🔴 CRITICAL: FOLLOW THE ENTIRE WORKFLOW PHASES IN ORDER FOR THE REQUESTED NEW CHANGES. RESEARCH -> PLANNING -> IMPLEMENTATION -> TESTING -> SERENA -> COMMIT 🔴

---

<Phase 1: Research> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS Research PHASE 🔴
ULTRA-THINK to Research the requested task(s):

## Task 1. Research re-working and re-architecture the AI Agent Technical Analyis Requests & Responses

- Re-architecture and rework how the AI agent and the AI instructions and the tools for getting technical analysis indicators and then performing analysis based on the technical analysis indicators 
- Make a clear distinction between just trying to get the technical analysis data versus performing actual technical analysis BASED on the ALL the data. 
- This will help remove ambiguity because sometimes the AI agent gets confused and doesn’t fetch technical analysis data when it needs to, or it already has enough data but then it fetches it again,  or it just fetch TA, and doesn’t analyze, etc, so we’ll have a clear distinction between getting the data and performing analysis on the data.
- Instead of having four individual granular 'get_ta_xxx' tools for the EMA SMA, MacD and RSI, we’re gonna consolidate and remove those individual tools and instead create a brand new tool AI Agent Tool called 'get_ta_indicators' that will bundle and perform the multiple tool calls to retrieve the data directly in the python tool
- that way this can improve performance because now when an AI agent wants to get TA data they can call the single tool and then all the Python code will call the relevant API end points to retrieve the data and clean it up and reformat it and post-process it a clean markdown table , and table is needed because it is data havy. 
- That way the agent doesn’t have to spend time with the tool calls itself, and the Python tool code will handle it so AI just needs to output the data
- So now there’s a clear distinction when AI agents requested to get or retrieve technical and announce indicators data. 
- They know that this is just a get operation and not performing an analysis and they have a tool for it and then if there’s a request to the perform analysis based on the data now we can focus on checking if it has enough information to perform analysis or not, and they could perform the analysis based on all the data in the user chat and not just the technical analysis data 
- so that’s one other issue we found when we were asked to perform the technical analysis by AI agent sometimes it has tunnel vision and literally just focuses on the four technical indicators, but it should be taking a holistic dynamic approach because if the user previously got a bunch of request and responses regarding the current price or yesterday‘s price or even the last two weeks performance or even the last months performance, maybe they also have some support and resistance levels, etc. that all could be used as part of the technical analysis so if all the data is available, AI agent use all that data one requested to analyze it only some is available then analyze based on what you got this is makes it so it’s not strict and rigid and holistic and dynamic based on whatever data is available because sometimes maybe the user will provide some data as part of their request and that is also could be useful for the agent to perform analysis on

-  for the tests, perform manual testing of the new functions and then you have to update the test suite in 'test_cli_regression.sh' as follows:
-  now we need to break it up into two separate actions so replace the current technical analysis test prompt with a request to get technical analysis indicator data.
-  After that, now an additional test case to request the AI agent to actually perform technical analysis indicator based on the data

Here is the expected outcomes:
1. NEW single tool 'get_ta_indicators' that will perform ALL of the listed Polygon API Calls in batches to prevent rate limiting issues, post-process and reformat the data in markdown table, and then provide response to AI Agent:
- Batch 1: RSI-14, MACD
- Batch 2: SMA 5/10/20/50/200
- Batch 3: EMA 5/10/20/50/200
- After all 3x batches received with data, now the tool can post-process and format the response
- End result is that to the AI Agent, a single tool call of 'get_ta_indicators' is a black box and AI Agent has no idea all of the intermediate steps and procedures inside the tool call itself, completely offloading so the most complex and performance impacting tasks to the Python Tool code and help freeing up AI Agent Bandwidth and Context

2. COMMENT OUT ONLY the tools code get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd so that we can still keep some backward compatiblity in the future.  We will comment it out to remove compiling in unused code, but it can always serve as a reference and guide in the future.  AI Agent instructions also need to be updated

3. AI Agent when asked to PERFORM Technical Analysis based on the data needs to analyze and provide insights for at LEAST these 4x topics: Trends, Volatility, Momentum, Trading Patterns




---

<Phase 2: Planning> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS Planning PHASE 🔴

Based on the Research, Analysis & Scoping from previous task(s), delete the current file 'TODO_task_plan.md' and then ULTRA-THINK AND GENERATE a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to systemtically use your Mandatory Tools Toolkit for Sequential-Thinking & Serena tools to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes.  The plan MUST enforce that YOU MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to enhance your workflow to perform all task(s)

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
   🔴 MANDATORY - VERIFY THE CONTENT OF EACH TEST PROMPT RESPONSE THAT IT MATCHES THE EXPECTED RESPONSE, PROPER TOOL CALLS, AND RESPONSE FORMATTING🔴
   - PASS CRITERIA: CONTENT OF TEST PROMPT RESPONS MATCHES THE EXPECTED RESPONSE, PROPER TOOL CALLS, AND RESPONSE FORMATTING
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
