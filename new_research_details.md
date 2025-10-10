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

<Research Topic Details for new Change Request(s)> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

1. USE ULTRA-THINK to Research implementing a re-architecture of the Front End REACT AI ChatBot GUI code:

You misunderstood the requirements.  I never said a shared session.  Here is what I want:

CLI Open: User 1 query and AI Agent responds.  CLI can ONLY be used on a PC, which has some limitations.  Can't use on Mobile, Ipads, or deploy the app to AWS as a CLI.

GUI Open: User 2 query, and AI Agent responds. It could be same or different questions as User 1, but basically the content, formatting , responses etc will NOT be unique.  User 2 using the GUI version is almsot like the User trying to use the CLI version, but it is in GUI interface instead that can be used by PC, Mobile, Ipads, etc.  This can be deployed as AWS app since it is a GUI.

So give me multiple options that can do this.  NOTHING about a shared session.  If user is at a PC, they can use the CLI version if they want.  BUt if they are on the go or they want a more visual usage, they can just use the GUI instead, with no loss of functionality compared to CLI . THAT is what I mean by being "the same", NOT a shared session.

So research AGAIN correctly.  Maybe "wrapper" is the wrong usage or strategy, so  give me multiple choices that balance simplicity, with low performance overhead.

2. Validate changes by running just ./test_cli_regression.sh to verify nothing is broken in the backend

3. After you confirmed that the new changes did NOT break anything in the backend by running the tests, notify user to then start testing the Frontend GUI code because you do NOT have access to test frontend code..  You will wait for user feedback to check out the changes first, so no commits yet.

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

Here are broker APIs that offer brokerage accounts and support simple API key authentication for programmatic access:

### 1. Alpaca

- __Authentication__: API key and secret
- __Requirements__: Funded brokerage account (U.S. clients and select international locations)
- __Coverage__: Equities and options trading, market data, paper trading
- __Features__: Commission-free U.S. stock and options trading, live and historical market data, algorithmic and automated support.[1]

### 2. Tradier

- __Authentication__: API key (simple) or OAuth2
- __Requirements__: Funded brokerage account (for live trading); sandbox/developer account for simulated data access
- __Coverage__: U.S. stocks and options
- __Features__: Commission-free trading (Pro), options Greek data, flexible and well-documented for integration.[1]

### 3. Webull

- __Authentication__: API token/key (community-supported access)
- __Requirements__: U.S. brokerage account
- __Coverage__: Stocks, options, cryptocurrencies
- __Features__: Commission-free trading, popular for bot development; official support for direct API key varies by integration.[1]

### 4. Moomoo

- __Authentication__: API key (reported simple setup)
- __Requirements__: Funded brokerage account (U.S. and some other markets)
- __Coverage__: Stocks, options
- __Features__: Commission-free offers, basic automation support.[1]

***
Broker APIs like Interactive Brokers offer powerful access, but authentication typically involves more complex OAuth flows or additional configuration—not just a one-step API key for every feature.[3]

For most individual algo developers and automated workflows, __Alpaca__ and __Tradier__ are the leading choices for true simple API key authentication combined with full brokerage account functionality.[3][1]

[1](https://investingintheweb.com/brokers/best-api-brokers/)
[2](https://wrtrading.com/broker/trading-apis/)
[3](https://www.wikijob.co.uk/trading/forex/brokers-with-api-access)
[4](https://brokerlistings.com/apis)
[5](https://www.reddit.com/r/algotrading/comments/143vem8/python_developers_what_broker_and_api_do_you_use/)
[6](https://brokerchooser.com/best-brokers/best-brokers-for-algo-trading)
[7](https://www.interactivebrokers.com/en/trading/ib-api.php)
[8](https://konfigthis.com/blog/asset-management-integrations/)
[9](https://www.daytrading.com/apis)
[10](https://stackoverflow.com/questions/59327/what-online-brokers-offer-apis)
