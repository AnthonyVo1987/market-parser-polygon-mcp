# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
[ENVIRONMENT] Complete environment re-init and CLI test script critical bug fixes

**Context:**

After syncing back to main branch following massive architectural changes, environment corruption required complete re-initialization and exposed critical bugs in CLI test script calculation engine.

**Phase 1: Environment Re-Initialization (6 Phases)**

Successfully completed full environment reset following SERNENA_PROJECT_ENVIRONMENT_SETUP_GUIDE:

1. **Pre-Reset Verification**: Verified git status (master branch, commit 4e13fb6)
2. **Complete Cleanup**: Removed .venv, node_modules, lock files, build artifacts
3. **Python Setup**: Installed 121 packages via uv sync (discovered critical dependency bug)
4. **Node.js Setup**: Installed 1,131 packages via npm install --legacy-peer-deps
5. **Server Validation**: Backend and frontend health checks PASSED
6. **Comprehensive Testing**: 27/27 CLI regression tests PASSED (100% success)

**Critical Bug Fix: Missing polygon-api-client Dependency**

**Issue:**
```python
ModuleNotFoundError: No module named 'polygon'
  File "polygon_tools.py", line 11, in <module>
    from polygon import RESTClient
```

**Root Cause:** After Phase 4 migration to Direct Polygon API, code imported `from polygon import RESTClient` but pyproject.toml was missing the polygon-api-client package dependency.

**Fix Applied:** Added `polygon-api-client>=1.14.0` to pyproject.toml dependencies

**Validation:** Re-ran uv sync → polygon-api-client==1.15.4 installed → All imports successful → 27/27 tests PASSED

**Phase 2: CLI Test Script Calculation Bug Fixes**

**Critical Issue Discovered:**
Test reports showed incorrect statistics due to missing `bc` (bash calculator) dependency:
- Total Session Duration: 0s (should be ~230s)
- Avg Response Time: 0s (should be ~8s)
- Min Response Time: 7.538s, Max Response Time: 7.538s (stuck at same value)

**Root Cause Analysis:**
- Script relied on `bc` for all floating-point arithmetic (14+ calculation points)
- `bc` not installed on system
- All `bc` calculations failed silently with fallback values of "0" or kept old values

**Fix Applied: Complete Calculation Engine Overhaul (bc → awk)**

Replaced ALL `bc` usage with `awk` across 5 critical areas:

1. **Duration Calculation** (Line 228):
```bash
# BEFORE (broken):
total_duration=$(echo "$end_time - $start_time" | bc -l 2>/dev/null || echo "0")

# AFTER (fixed):
total_duration=$(awk "BEGIN {printf \"%.2f\", $end_time - $start_time}")
```

2. **Min/Max Detection** (Lines 296-311):
```bash
# BEFORE (broken):
if (( $(echo "$time < $min_time" | bc -l 2>/dev/null || echo "0") )); then

# AFTER (fixed):
if (( $(awk "BEGIN {print ($time < $min_time)}") )); then
```

3. **Average Calculation** (Line 306):
```bash
# BEFORE (broken):
avg_time=$(echo "scale=2; $total_time / $count" | bc -l 2>/dev/null || echo "0")

# AFTER (fixed):
avg_time=$(awk "BEGIN {printf \"%.2f\", $total_time / $count}")
```

4. **Performance Classification** (Lines 200-208):
```bash
# BEFORE (broken):
if (( $(echo "$rt < 30" | bc -l 2>/dev/null || echo "0") )); then

# AFTER (fixed):
if (( $(awk "BEGIN {print ($rt < 30)}") )); then
```

5. **Aggregate Loop Statistics** (Lines 455-464):
```bash
# BEFORE (broken):
agg_total=$(echo "$agg_total + $time" | bc -l 2>/dev/null || echo "$agg_total")

# AFTER (fixed):
agg_total=$(awk "BEGIN {printf \"%.2f\", $agg_total + $time}")
```

**Why awk?**
- ✅ Universally available on all Unix/Linux systems
- ✅ Reliable floating-point arithmetic
- ✅ Never fails silently (unlike bc when missing)
- ✅ Consistent precision control

**Validation (3-Loop Test):** All calculations working correctly:
- Loop 1: Min=3.648s, Max=15.674s, Avg=8.404s, Duration=229.010s
- Loop 2: Min=2.429s, Max=13.659s, Avg=7.646s, Duration=208.689s
- Loop 3: Min=4.019s, Max=17.159s, Avg=9.464s, Duration=258.111s

**Phase 3: Output Formatting Enhancements**

**Improvements Applied:**

1. **Decimal Precision**: Limited all values to 2 decimal places (was 3)
```bash
# Changed all .3f to .2f in awk printf statements
avg_time=$(awk "BEGIN {printf \"%.2f\", $total_time / $count}")
```

2. **Duration Format**: Converted to human-readable "MM min SS sec"
```bash
# BEFORE (hard to read):
Total Session Duration: 229.010s

# AFTER (human-readable):
duration_minutes=$(awk "BEGIN {printf \"%d\", $total_duration / 60}")
duration_seconds=$(awk "BEGIN {printf \"%d\", $total_duration % 60}")
duration_formatted="${duration_minutes} min ${duration_seconds} sec"
# Output: Total Session Duration: 3 min 49 sec
```

**Validation (Final 3-Loop Test):** All formatting working correctly:
- Loop 1: 27/27 PASSED, Avg=8.42s, Duration="3 min 49 sec"
- Loop 2: 27/27 PASSED, Avg=8.97s, Duration="4 min 4 sec"
- Loop 3: 27/27 PASSED, Avg=8.73s, Duration="3 min 57 sec"
- Aggregate: 81/81 PASSED (100%), Overall Avg=8.71s

**Serena Memory Updates:**

1. **testing_procedures.md** (comprehensive update):
   - ✅ Documented calculation engine overhaul (bc → awk migration)
   - ✅ Added "Calculation Engine" section with implementation details
   - ✅ Documented historical bug and fix (Oct 6, 2025)
   - ✅ Added "Output Formatting" section with precision/duration improvements
   - ✅ Updated performance baselines with latest 3-loop validation data
   - ✅ Added troubleshooting section for calculation issues

2. **SERNENA_PROJECT_ENVIRONMENT_SETUP_GUIDE.md** (major update):
   - ✅ Updated success criteria (27 tests, 121 packages, correct test statistics)
   - ✅ Added polygon-api-client dependency to critical dependencies checklist
   - ✅ Documented Oct 6, 2025 re-initialization success
   - ✅ Added Issue 1: Missing polygon Module troubleshooting section
   - ✅ Added Issue 5: Test Script Incorrect Statistics troubleshooting section
   - ✅ Updated validation checklist with test statistics verification
   - ✅ Added "Recent Successful Re-Initializations" section

**Files Changed:**

Core Fixes:
- ✅ Modified: `pyproject.toml` (+1 dependency: polygon-api-client>=1.14.0)
- ✅ Modified: `CLI_test_regression.sh` (14+ calculation points, bc → awk migration)
- ✅ Modified: `CLI_test_regression.sh` (formatting: 2 decimal precision, min:sec duration)

Documentation:
- ✅ Modified: `.serena/memories/testing_procedures.md` (comprehensive update)
- ✅ Modified: `.serena/memories/SERNENA_PROJECT_ENVIRONMENT_SETUP_GUIDE.md` (major update)
- ✅ Modified: `CLAUDE.md` (this last task summary)

Test Evidence:
- ✅ Generated: `test-reports/cli_regression_test_loop1_20251006_111008.txt`
- ✅ Generated: `test-reports/cli_regression_test_loop2_20251006_111401.txt`
- ✅ Generated: `test-reports/cli_regression_test_loop3_20251006_111808.txt`

**Total**: 6 code/config files modified, 2 Serena memories updated, 3 test reports generated

**Performance Validation:**

**Environment Re-Init:**
- ✅ Python: 121/121 packages installed successfully
- ✅ Node.js: 1,131/1,131 packages installed successfully
- ✅ Production build: 3.65s (successful)
- ✅ Backend health: PASSED
- ✅ Frontend health: PASSED

**Test Suite (Final 3-Loop Validation):**
- ✅ Total Tests: 81/81 PASSED (100% success rate)
- ✅ Loop 1: 27/27 PASSED, Avg=8.42s, Duration=3 min 49 sec, Rating=EXCELLENT
- ✅ Loop 2: 27/27 PASSED, Avg=8.97s, Duration=4 min 4 sec, Rating=EXCELLENT
- ✅ Loop 3: 27/27 PASSED, Avg=8.73s, Duration=3 min 57 sec, Rating=EXCELLENT
- ✅ Overall Avg: 8.71s (EXCELLENT performance)
- ✅ Min Avg: 8.42s (Loop 1)
- ✅ Max Avg: 8.97s (Loop 2)
- ✅ Consistency: Highly consistent across all loops

**Key Achievements:**

- ✅ Environment fully operational after complete re-initialization
- ✅ Critical polygon-api-client dependency bug discovered and fixed
- ✅ CLI test script calculation engine made universally compatible (awk vs bc)
- ✅ Test report formatting significantly improved (readability)
- ✅ All 14+ calculation points working correctly across 5 critical areas
- ✅ 100% test success rate maintained (81/81 tests)
- ✅ Serena memories updated with comprehensive troubleshooting guides
- ✅ Documentation aligns with actual implementation and recent fixes
<!-- LAST_COMPLETED_TASK_END -->

## 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

🔴 CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

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
- If you don't use tools throughout the entire process, you're failing
- If you use wrong tool for the operation (e.g., Standard for batch operations), you're failing

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

## 🔴 CRITICAL: MANDATORY TESTING CHECKPOINT

**Testing is NOT optional - it is REQUIRED for task completion:**

### **Testing Workflow (MUST FOLLOW):**

1. **Code Implementation** → Create/update code
2. **Test Suite Update** → Create/update test files
3. **🔴 TEST EXECUTION (MANDATORY)** → RUN the test suite
4. **Test Verification** → Verify 100% pass rate
5. **Documentation** → Update docs with test results

### **Test Execution Requirements:**

✅ **MUST DO:**

- Execute test suite (e.g., `./CLI_test_regression.sh`)
- Show test results to user (pass/fail counts, response times)
- Verify 100% success rate
- Provide test report file path
- Fix any failures and re-test

❌ **NEVER DO:**

- Skip test execution
- Claim completion without test results
- Mark task "done" without test evidence
- Proceed to documentation without running tests

### **Enforcement Rules:**

🔴 **Code without test execution = Code NOT implemented**
🔴 **No test results = Task INCOMPLETE**
🔴 **Test results are PROOF of implementation**
🔴 **Tests must run BEFORE documentation updates**

### **Pattern Recognition:**

**WRONG (What NOT to do):**

```text
1. Create 5 new tools ✅
2. Update test suite file ✅
3. Update documentation ✅
4. Mark task complete ❌ (NEVER ran tests!)
```

**CORRECT (What TO do):**

```text
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN test suite: ./CLI_test_regression.sh ✅
4. Show results: 16/16 PASS, 100% success ✅
5. Provide test report path ✅
6. Update documentation with test results ✅
7. Mark task complete ✅
```

### **When to Run Tests:**

- After creating new tools/functions
- After modifying existing code
- After updating AI agent instructions
- After changing test suite
- Before updating documentation
- Before claiming task completion

**Remember: If you haven't RUN the tests and SHOWN the results, the task is NOT complete.**

## 🔴 CRITICAL: PROPER ATOMIC COMMIT WORKFLOW

**MANDATORY: Stage ONLY Immediately Before Commit**

### The Fatal Mistake: Early Staging

**NEVER stage files early during development. Staging is the LAST step before committing.**

**What happens when you stage too early:**

1. ⏰ **Time T1**: You run `git add` (files staged)
   - Staging area = snapshot at T1
2. ⏰ **Time T2-T5**: You continue working
   - Update config files
   - Run tests (generates test reports)
   - Update documentation
3. ⏰ **Time T6**: You run `git commit`
   - **Only commits the T1 snapshot**
   - **All work after T1 is MISSING**

**Result: Incomplete, broken atomic commits** ❌

### Correct Atomic Commit Workflow

**Follow this workflow EXACTLY:**

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

3. **STAGE EVERYTHING AT ONCE**:

   ```bash
   git add -A  # Stage ALL files in ONE command
   ```

   - ⚠️ This is the FIRST time you run `git add`

4. **VERIFY STAGING IMMEDIATELY**:

   ```bash
   git status  # Verify ALL files staged, NOTHING unstaged
   ```

5. **COMMIT IMMEDIATELY** (within 60 seconds):

   ```bash
   git commit -m "message"
   ```

6. **PUSH IMMEDIATELY**:

   ```bash
   git push
   ```

### What Belongs in an Atomic Commit

**ALL of these must be included together:**

- ✅ Code changes (backend + frontend)
- ✅ Test reports (evidence of passing tests)
- ✅ Documentation updates (CLAUDE.md, README.md, etc.)
- ✅ Memory updates (.serena/memories/)
- ✅ Config changes (.claude/settings.local.json, etc.)
- ✅ Task plan updates (TODO_task_plan.md, etc.)

### ❌ NEVER DO THIS

- ❌ Stage files early during development
- ❌ Stage files "as you go"
- ❌ Run `git add` before ALL work is complete
- ❌ Delay between `git add` and `git commit`
- ❌ Commit without test reports
- ❌ Commit without documentation updates

**Reference:** See `.serena/memories/git_commit_workflow.md` for complete details.

**Enforcement:** Incomplete commits will be reverted and reworked.

## Quick Start

### CLI Interface

```bash
uv run src/backend/main.py

> Tesla stock analysis
KEY TAKEAWAYS
• TSLA showing bullish momentum...
```

**One-Click Application Startup (Recommended):**

The startup scripts automatically START all development servers BUT **DOES
NOT OPEN THE APP IN BROWSER AUTOMATICALLY**.

```bash
# Option 1: XTerm startup script (RECOMMENDED - WORKING)
./start-app-xterm.sh

# Option 2: Main startup script (NOW WORKING - FIXED)
./start-app.sh  # ✅ WORKING: Script now exits cleanly with timeout
```

**Prerequisites:** uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (NOW WORKING - FIXED)

- **Status**: ✅ WORKING - Script now exits cleanly with timeout mechanism
- **Features**: 30-second timeout fallback to prevent hanging
- **Environment Support**: Works in both X11 and WSL2/headless environments
- **Background Mode**: Uses background processes in WSL2, terminal windows in X11
- **Logging**: Writes server logs to backend.log and frontend.log in WSL2 mode

## What the Scripts Do

### ⏰ Timeout Mechanism

Both scripts now include a **30-second timeout fallback** to prevent hanging:

- **Normal Operation**: Scripts typically complete in 10-15 seconds
- **Safety Net**: 30-second timeout ensures scripts never hang indefinitely
- **AI Agent Friendly**: Prevents AI agents from getting stuck waiting for script completion
- **Graceful Exit**: Scripts exit cleanly after server verification or timeout

### 🔄 Server Cleanup

- Kills existing development servers (uvicorn, vite)
- **Preserves MCP servers** - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup

- **Backend**: Starts FastAPI server on `http://127.0.0.1:8000`
- **Frontend**: Starts Vite dev server on `http://127.0.0.1:3000`
- Opens each server in a separate terminal window for easy monitoring
- Uses consistent hard-coded ports (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies frontend serves content properly

### 🌐 Browser Launch

- **NOTIFIES USER TO LAUNCH BROWSER TO START THE APP WHEN SERVERS ARE READY**

**Access:** <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)

## Features

### ⚡ High-Performance UI

- **Lightning Fast Loading**: 85%+ improvement in Core Web Vitals
- **Optimized Performance**: 256ms First Contentful Paint (FCP)
- **Smooth Interactions**: All UI interactions are instant and responsive
- **Memory Efficient**: Optimized memory usage with 13.8MB heap size
- **Accessibility First**: Full WCAG 2.1 AA compliance

### Natural Language Financial Queries

Ask questions like:

- `Tesla stock price analysis`
- `AAPL volume trends this week`
- `Show me MSFT support and resistance levels`

### Multiple Interfaces

- **React Web App** - Modern responsive interface with real-time chat
- **Enhanced CLI** - Terminal interface with rich formatting
- **API Endpoints** - RESTful API for integration

## Example Usage

### Web Interface

1. Open <http://127.0.0.1:3000>
2. Type your financial query
3. Get instant structured responses with sentiment analysis

## Architecture

- **Backend**: FastAPI with OpenAI Agents SDK v0.2.9 and Polygon.io MCP integration v0.4.1
- **Frontend**: React 18.2+ with Vite 5.2+ and TypeScript
- **Testing**: Playwright E2E test suite
- **Deployment**: Fixed ports (8000/3000/5500) with one-click startup

## Development

### Available Commands

```bash
# Application startup
npm run start:app          # One-click startup
npm run frontend:dev       # Frontend development
npm run build             # Production build

# Testing with Playwright MCP Tools only - see `/tests/playwright/mcp_test_script_basic.md`

# Code quality
npm run lint              # All linting
npm run type-check        # TypeScript validation
```

### Project Structure

```text
src/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application
│   ├── api_models.py    # API schemas
│   └── prompt_templates.py # Analysis templates
├── frontend/            # React frontend
│   ├── components/      # React components
│   ├── hooks/          # Custom hooks
│   └── config/         # Configuration loader
config/                  # Centralized configuration
│   └── app.config.json # Non-sensitive settings
tests/playwright/        # E2E test suite
```

## Troubleshooting

### Common Issues

**Backend not starting:**

```bash
# Check .env file has API keys
cat .env | grep API_KEY

# Verify dependencies
uv install
```

**Frontend connection errors:**

```bash
# Verify backend is running
curl http://127.0.0.1:8000/health

# Check ports are available
netstat -tlnp | grep :8000
```

**API key issues:**

- Ensure both `POLYGON_API_KEY` and `OPENAI_API_KEY` are set in `.env`
- Verify API keys are valid and have sufficient credits

## Disclaimer

**Warning:** This application uses AI and large language models.
Outputs may contain inaccuracies and should not be treated as financial
advice. Always verify information independently before making financial
decisions. Use for informational purposes only.

## License

This project is licensed under the [MIT License](LICENSE).
