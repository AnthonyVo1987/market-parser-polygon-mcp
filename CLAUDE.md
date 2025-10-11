# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
## Tradier Options Expiration Dates Tool Integration

**Status:** ✅ Complete (October 10, 2025)
**Feature:** Add Tradier Brokerage API integration with new `get_options_expiration_dates` tool

### Problem Solved

**Issue:** No dedicated tool for fetching available options expiration dates for a ticker

**Requirement:** User requested ability to fetch ALL valid options expiration dates for tickers (SPY, NVDA, etc.) to support options trading analysis workflow

### Solution Implemented

**New Tool:** `get_options_expiration_dates` (Tradier Brokerage API)

**Files Created:**
- `src/backend/tools/tradier_tools.py` - New tool implementation (156 lines)

**Files Modified:**
- `src/backend/tools/__init__.py` - Export get_options_expiration_dates
- `src/backend/services/agent_service.py` - Import tool, add to tools list (position 2), update tool count (12→13), add RULE #10
- `test_cli_regression.sh` - Added 2 test cases (Test 14, Test 31), updated suite (38→40 tests)

### Implementation Details

**Tradier API Integration:**
- **Endpoint:** `/v1/markets/options/expirations`
- **Authentication:** Bearer token via `TRADIER_API_KEY` environment variable
- **Method:** Direct HTTP API using `requests` library
- **Response Format:** JSON with array of expiration dates (YYYY-MM-DD)
- **Sorting:** Chronologically (earliest to latest)
- **Includes:** Both weekly and monthly expiration dates

**Tool Function:**
```python
@function_tool
async def get_options_expiration_dates(ticker: str) -> str:
    """Get valid options expiration dates for a ticker from Tradier API."""
```

**Parameters:**
- `ticker` (str): Stock ticker symbol (e.g., "AAPL", "SPY", "NVDA")

**Returns:** JSON string with format:
```json
{
  "ticker": "SPY",
  "expiration_dates": ["2025-10-17", "2025-10-24", "2025-10-31", ...],
  "count": 31,
  "source": "Tradier"
}
```

**Error Handling:**
- Invalid ticker validation
- Configuration error (TRADIER_API_KEY not found)
- API request failures (HTTP status errors)
- No data available (invalid ticker)
- Timeout (10s timeout)
- Network errors
- Edge case: Single date returned as string (converted to list)

### Agent Instructions Update

**RULE #10:** OPTIONS EXPIRATION DATES = USE get_options_expiration_dates
- **When to Use:** User requests available expiration dates for options contracts
- **Workflow:** Identify request → Extract ticker → Call tool → Present dates in readable format
- **Display Format:** Comma-separated list or bullet points
- **Common Mistakes:** Using options chain tools when only expiration dates needed

### Test Results & Validation

**Quick Validation Tests:**
- **SPY:** 31 expiration dates, 9.844s response time - PASS ✅
- **NVDA:** 21 expiration dates, 6.842s response time - PASS ✅
- **SOUN:** 11 expiration dates, 6.391s response time - PASS ✅

**Full CLI Regression Suite (40 tests):**
- ✅ **40/40 PASSED** (100% success rate)
- ✅ **11.03s** average response time (EXCELLENT rating)
- ✅ **7 min 22 sec** session duration
- ✅ **Session persistence:** VERIFIED (single session)
- ✅ **Test Report:** `test-reports/test_cli_regression_loop1_2025-10-10_19-25.log`

**New Test Cases:**
- **Test 14:** SPY Options Expiration Dates - PASS (8.596s, EXCELLENT)
- **Test 31:** NVDA Options Expiration Dates - PASS (14.511s, EXCELLENT)

### Test Suite Evolution

**Test Suite Updates:**
- **Previous:** 38 tests (SPY 16 + NVDA 16 + Multi 6)
- **Updated:** 40 tests (SPY 17 + NVDA 17 + Multi 6)
- **Test Renumbering:** All tests after Test 13 shifted by +1
- **New Tests Inserted:**
  - Test 14: "Get options expiration dates for SPY" (after "Technical Analysis: $SPY")
  - Test 31: "Get options expiration dates for NVDA" (after "Technical Analysis: $NVDA")

### Key Benefits

**1. Dedicated Tool for Expiration Dates:**
- Faster than using options chain tools for just dates
- Clean, focused API (single purpose)
- Comprehensive coverage (all weekly and monthly expirations)

**2. Clean Integration:**
- Follows existing tool patterns (finnhub_tools.py)
- Comprehensive error handling
- Well-documented with usage examples

**3. Improved Workflow:**
- User can quickly check available expiration dates
- Supports options trading analysis workflow
- Enables better decision-making (select appropriate expiration)

**4. Production-Ready:**
- 100% test pass rate
- Excellent performance (6-15s response times)
- Robust error handling
- Edge case handling (single date → list conversion)

### Architecture Impact

**AI Agent Tools:**
- **Previous:** 12 tools (1 Finnhub + 11 Polygon)
- **Updated:** 13 tools (1 Finnhub + 1 Tradier + 11 Polygon)
- **Position:** Tool #2 (after get_stock_quote, before market data tools)

**Environment Variables:**
- Added `TRADIER_API_KEY` to required .env variables

**API Dependencies:**
- Added `requests>=2.31.0` (already in project for other purposes)

### Tool Usage Workflow

**Example User Requests:**
- "Get options expiration dates for SPY"
- "What are the available expiration dates for NVDA options?"
- "Show me TSLA options expiration dates"

**AI Agent Workflow:**
1. Identify user is requesting expiration dates
2. Extract ticker symbol from request
3. Call `get_options_expiration_dates(ticker='SYMBOL')`
4. Present dates in readable format (bullet list or comma-separated)

**Example Response:**
```
SPY options expiration dates:

• 2025-10-13, 2025-10-14, 2025-10-15, 2025-10-17, ...
  2025-10-20, 2025-10-21, 2025-10-24, 2025-10-31

Count: 31 expiration dates
Source: Tradier
```

### Performance Metrics

**Individual Tool Performance:**
- Min: 6.391s (SOUN)
- Max: 14.511s (NVDA - Test 31)
- Avg: ~9.6s (EXCELLENT rating)

**Suite Performance (40 tests):**
- Overall Avg: 11.03s (EXCELLENT rating)
- Performance Range: 2.607s - 31.846s
- 39/40 tests under 30s (EXCELLENT)
- 1/40 test at 31.8s (GOOD)

**Performance Impact:**
- Minimal impact on suite average (11.03s vs 11.05s baseline)
- New tool performs within EXCELLENT range
- No performance degradation

### Implementation Workflow

**Phases Followed:**
1. ✅ **Research Phase:** Analyzed Tradier API documentation, tested endpoint
2. ✅ **Planning Phase:** Created detailed implementation plan (TODO_task_plan.md)
3. ✅ **Implementation Phase:** Created tool, updated exports, integrated with agent
4. ✅ **Testing Phase:** Quick tests (3 tickers), full suite (40 tests), 100% pass rate
5. ✅ **Serena Updates Phase:** Updated tech_stack.md and testing_procedures.md memories
6. ✅ **Documentation Phase:** Updated CLAUDE.md (this file)

**Tool Usage Compliance:**
- ✅ Sequential-Thinking: Not required (straightforward task)
- ✅ Standard Read/Write/Edit: Used for file modifications
- ✅ Bash: Used for testing (CLI invocations)
- ✅ Serena: Used for memory updates

### Documentation Updates

**Serena Memories:**
- `.serena/memories/tech_stack.md` - Added Tradier tool section, updated tool count, test suite info
- `.serena/memories/testing_procedures.md` - Updated test coverage, added new test cases, updated metrics

**Project Documentation:**
- `CLAUDE.md` - Updated Last Completed Task (this section)
- `test_cli_regression.sh` - Updated header comments, prompts, test names (38→40 tests)

**Implementation Plan:**
- `TODO_task_plan.md` - Created comprehensive 17-step implementation plan

### References

- **Test Report:** `test-reports/test_cli_regression_loop1_2025-10-10_19-25.log`
- **Serena Memories:**
  - `.serena/memories/tech_stack.md` (added Tradier tool section)
  - `.serena/memories/testing_procedures.md` (updated test coverage)
- **Tool Implementation:**
  - `src/backend/tools/tradier_tools.py` (156 lines)
  - `src/backend/services/agent_service.py` (RULE #10, tool registration)
- **API Documentation:** https://docs.tradier.com/reference/brokerage-api-markets-get-options-expirations

**Previous Task:** Frontend Code Duplication Elimination (Oct 9, 2025) - 38/38 tests, 11.14s avg
**Current Task:** Tradier Options Expiration Dates Tool (Oct 10, 2025) - 40/40 tests, 11.03s avg, 100% success
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

### Serena Tool Setup

Before using Serena tools for code analysis, get the initial instructions to understand optimal usage:

- **Primary Method (Preferred)**: Use `mcp__serena__initial_instructions` tool
- **Fallback Method**: If tool fails, use `mcp__serena__read_memory` with memory name: `serena_initial_instructions`

These instructions provide critical guidance on:

- Token-efficient code exploration using symbolic tools
- Proper file reading vs. full file scanning
- Symbol overview and targeted symbol reads
- Pattern searching for flexible searches

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

- Execute test suite (e.g., `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`)
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
3. RUN test suite: chmod +x test_cli_regression.sh && ./test_cli_regression.sh ✅
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

### MANDATORY: Stage ONLY Immediately Before Commit

#### The Fatal Mistake: Early Staging

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
chmod +x start-app-xterm.sh && ./start-app-xterm.sh

# Option 2: Main startup script (NOW WORKING - FIXED)
chmod +x start-app.sh && ./start-app.sh

  # ✅ WORKING: Script now exits cleanly with timeout
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
- **Testing**: CLI regression test suite (test_cli_regression.sh - 40 tests)
- **Deployment**: Fixed ports (8000/3000/5500) with one-click startup

## Development

### Available Commands

```bash
# Application startup
npm run start:app          # One-click startup
npm run frontend:dev       # Frontend development
npm run build             # Production build

# Testing: Run chmod +x test_cli_regression.sh && ./test_cli_regression.sh to execute 40-test suite

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


      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
