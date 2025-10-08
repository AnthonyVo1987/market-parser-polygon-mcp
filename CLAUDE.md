# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
[AI AGENT FIX] Fix OHLC bars display + Support/Resistance redundant calls + New 35-test suite

**Primary Changes:**

1. **OHLC Display Fix**: Added critical display requirements to RULE #5 (show actual data, not just "data retrieved")
2. **Support & Resistance Fix**: Enhanced RULE #9 with Scenario 5 to prevent redundant TA tool calls
3. **New Test Suite**: Created test_cli_regression.sh with 35 comprehensive tests (vs old 27)
4. **Chat History Analysis**: Validated intelligent data reuse across session
5. **.gitignore Update**: Allow test-reports/*.log files to be committed

**Code Changes:**

- **agent_service.py (RULE #5)**: Added "CRITICAL DISPLAY REQUIREMENTS FOR OHLC BARS" section
  - For custom date range: MUST show start open, end close, $ and % change, period high/low, trading days
  - For specific date: MUST show Date, Open, High, Low, Close, Volume
  - NEVER just say "data retrieved" without actual numbers
  - Added good vs bad response examples
- **agent_service.py (RULE #9)**: Added Scenario 5 - Support & Resistance Levels
  - Explicitly tells AI to use existing price/SMA/EMA data instead of making new calls
  - Prevents redundant tool calls when all TA data already retrieved
- **test_cli_regression.sh**: New 35-test suite with persistent session validation
  - SPY test sequence (15 tests)
  - NVDA test sequence (15 tests)
  - Multi-ticker WDC/AMD/INTC tests (5 tests)
  - Validates parallel calls, chat history analysis, OHLC display
- **.gitignore**: Updated line 84 to allow test-reports/*.log files

**Test Results:**

- **Total Tests**: 35/35 PASSED ✅
- **Success Rate**: 100%
- **Average Response Time**: 11.62s ⭐ EXCELLENT
- **Response Range**: 2.188s - 31.599s
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-07_20-30.log`
- **Test 12 (Support & Resistance)**: 3.900s (vs previous 5.491s) - redundant call fix verified ✅
- **Test 15 (SPY OHLC Q1)**: Shows actual data (start: 589.39, end: 559.39, change: -4.31%, high: 613.23, low: 549.83, 60 days) ✅
- **Test 30 (NVDA OHLC Q1)**: Shows actual data (start: 136.00, end: 108.38, change: -20.30%, high: 147.79, low: 103.65, 60 days) ✅
- **Test 35 (Multi OHLC Q1)**: Shows actual data for all 3 tickers (WDC, AMD, INTC) ✅
- **Chat History Reuse**: Test 32 correctly used existing data (no new calls) ✅
- **Parallel Calls**: Tests 31, 33, 34 correctly made parallel calls for 3 tickers ✅

**Documentation Updates:**

- ✅ Updated: `CLAUDE.md` (Last Completed Task section)
- ✅ Updated: `.serena/memories/ai_agent_instructions_oct_2025.md`
- ✅ Updated: `.serena/memories/project_architecture.md`
- ✅ Added: Test report file

**Impact Analysis:**

- **Code Quality**: Improved - explicit OHLC display requirements prevent useless responses
- **Agent Behavior**: Fixed - no more redundant TA calls for Support & Resistance
- **Test Coverage**: Expanded - 35 comprehensive tests vs previous 27 tests
- **Performance**: Excellent - 11.62s average, 100% success rate
- **Chat History**: Validated - intelligent data reuse working correctly
- **OHLC Responses**: Fixed - now shows actual data instead of just "data retrieved"

**Files Changed:**

- ✅ Modified: `src/backend/services/agent_service.py` (RULE #5 display requirements, RULE #9 Scenario 5)
- ✅ Modified: `.gitignore` (allow test-reports/*.log)
- ✅ Created: `test_cli_regression.sh` (new 35-test suite)
- ✅ Modified: `CLAUDE.md` (Last Completed Task section)
- ✅ Modified: `.serena/memories/ai_agent_instructions_oct_2025.md`
- ✅ Modified: `.serena/memories/project_architecture.md`
- ✅ Added: `test-reports/test_cli_regression_loop1_2025-10-07_20-30.log`

**Total**: 3 code files modified/created, 3 documentation files updated, 1 test report added
<!-- LAST_COMPLETED_TASK_END -->

## OpenAI Prompt Caching Integration

**Status:** ✅ Implemented (October 2025)
**Feature:** OpenAI API Prompt Caching for cost reduction and latency improvement

### How It Works

1. **Automatic Caching**: Prompts >1024 tokens are automatically cached by OpenAI
2. **Cache Duration**: 5-10 minutes of inactivity, maximum 1 hour
3. **Cache Scope**: Organization-level (shared within same OpenAI organization)
4. **Agent Instructions**: Cached on EVERY request (massive cost savings)

### Token Display

**CLI Output:**

```
   Tokens Used: 16,413 (Input: 16,183, Output: 230) | Cached Input: 7,936
```

**GUI Output:**

```
Input: 16,183 | Output: 230 | Total: 16,413 | Cached Input: 7,936
```

### Cost Savings

- **Cached Input Tokens**: 50% cost reduction
- **Latency Improvement**: Up to 80% faster for cached prompts >10K tokens
- **Typical Savings**: 30-50% cost reduction in persistent sessions

### Implementation Details

- **Backend**: `token_utils.py` extracts cached tokens from OpenAI Agents SDK
- **API Models**: `api_models.py` includes `cachedInputTokens` and `cachedOutputTokens`
- **CLI Display**: `response_utils.py` shows cached token metrics
- **Frontend**: `ChatMessage_OpenAI.tsx` displays cached tokens in GUI

### Best Practices

1. **Prompt Structure**: Static content (instructions, tools) at START, dynamic (user query) at END
2. **Tool Ordering**: Keep tools in same order across requests
3. **Message History**: Append new messages to END of array
4. **Cache Invalidation**: Any change to static content clears cache

### References

- **OpenAI Docs**: https://platform.openai.com/docs/guides/prompt-caching
- **Implementation Example**: examples/Prompt_Caching101.ipynb
- **Serena Guide**: `.serena/memories/prompt_caching_guide.md`

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

- Execute test suite (e.g., `./test_cli_regression.sh`)
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
3. RUN test suite: ./test_cli_regression.sh ✅
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
- **Testing**: CLI regression test suite (test_cli_regression.sh - 35 tests)
- **Deployment**: Fixed ports (8000/3000/5500) with one-click startup

## Development

### Available Commands

```bash
# Application startup
npm run start:app          # One-click startup
npm run frontend:dev       # Frontend development
npm run build             # Production build

# Testing: Run ./test_cli_regression.sh to execute 35-test suite

# Code quality
npm run lint              # All linting
npm run type-check        # TypeScript validation
```

### Project Structure

```text
src/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application
│   └── api_models.py    # API schemas
├── frontend/            # React frontend
│   ├── components/      # React components
│   ├── hooks/          # Custom hooks
│   └── config/         # Configuration loader
config/                  # Centralized configuration
│   └── app.config.json # Non-sensitive settings
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
