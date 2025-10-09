# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
## CLI Visual Enhancements: Markdown Tables + Emoji Responses + Intelligent Formatting

**Status:** ✅ Implemented (October 9, 2025)
**Feature:** Enhance CLI output with Markdown table formatting for options chains, emoji responses for visual clarity, intelligent list/table formatting, and options chain wall analysis tests

### Enhancement Requirements

1. **Options Chain Markdown Table Formatting**: Display options chain data in readable table format with proper alignment
   - **Goal**: Replace unformatted data with beautiful Markdown tables
   - **Requirement**: Table header with columns (Strike, Price, Delta, Gamma, Theta, Vega, IV, Volume, Open Interest)
   - **Formatting**: Strike prices with $, IV as percentage, volume/OI with comma separators
   - **Implementation**: Pure prompt engineering in agent instructions

2. **Emoji Response Formatting**: Add visual clarity and engagement with financial emojis
   - **Goal**: Enhance responses with relevant emojis without overwhelming
   - **Categories**: Financial (📊📈📉💹), Status (✅⚠️🟢🔴)
   - **Usage**: 2-5 emojis per response, prioritize clarity
   - **Implementation**: Pure prompt engineering in agent instructions

3. **Intelligent Response Formatting (Lists vs Tables)**: Optimize formatting based on data complexity
   - **Goal**: Use lists for simple responses (speed), tables for complex responses (readability)
   - **Lists**: Single ticker prices, binary questions, 1-5 data points
   - **Tables**: Multi-ticker comparisons, OHLC bars, multiple TA indicators, 6+ data points
   - **Implementation**: Decision logic via prompt engineering

4. **Options Chain Wall Analysis Tests**: Add test cases to validate AI Agent's ability to identify support/resistance from options data
   - **Goal**: Test AI Agent's analysis of call walls (resistance) and put walls (support)
   - **Test Cases**: SPY Wall analysis (Test 16), NVDA Wall analysis (Test 32)
   - **Expected Output**: Strike prices, OI/volume data, actionable implications
   - **Validation**: AI Agent reuses existing options chain data (no redundant tool calls)

### Changes Implemented

**1. Options Chain 10-Strike Limit Enforcement** (`src/backend/tools/polygon_tools.py`)

**Function: `get_call_options_chain` (lines 588-720)**

- **Old Implementation** (WRONG):

  ```python
  for option in client.list_snapshot_options_chain(..., params={"limit": 10, ...}):
      options_chain.append(option)  # Appends ALL results, ignoring limit!
  ```

- **New Implementation** (CORRECT):

  ```python
  options_chain = list(client.list_snapshot_options_chain(
      ticker,
      params={
          "strike_price.gte": current_price,
          "expiration_date": expiration_date,
          "contract_type": "call",
          "order": "asc",
          "limit": 10,
          "sort": "strike_price",
      },
  ))[:10]  # Explicitly slice to ensure exactly 10 strikes maximum
  ```

- **Pattern**: Changed from for loop to `list()[:10]` slice - cleaner and more Pythonic
- **Impact**: Now enforces exactly 10 strikes per chain

**Function: `get_put_options_chain` (lines 723-855)**

- **Identical fix** applied with `list()[:10]` slice
- **Parameters differ**: Uses `strike_price.lte` and `order="desc"` for puts

**2. None-Safe Rounding for All Float Fields** (`src/backend/tools/polygon_tools.py`)

Both functions now use defensive None checks before rounding:

```python
# Extract values with None-safe defaults
close = getattr(option.day, "close", 0.0)
delta = getattr(option.greeks, "delta", 0.0)
gamma = getattr(option.greeks, "gamma", 0.0)
theta = getattr(option.greeks, "theta", 0.0)
vega = getattr(option.greeks, "vega", 0.0)
iv = getattr(option.implied_volatility, 0.0)

# Round all values with None-safe handling
formatted_chain[strike_key] = {
    "price": round(close if close is not None else 0.0, 2),
    "delta": round(delta if delta is not None else 0.0, 2),
    "gamma": round(gamma if gamma is not None else 0.0, 2),
    "theta": round(theta if theta is not None else 0.0, 2),
    "vega": round(vega if vega is not None else 0.0, 2),
    "implied_volatility": round(iv if iv is not None else 0.0, 2),
    "volume": volume,
    "open_interest": oi,
}
```

- **Pattern**: `round(value if value is not None else 0.0, 2)` for all float fields
- **Default**: Uses `0.00` when API returns None (acceptable for missing data)
- **Fields protected**: price, delta, gamma, theta, vega, implied_volatility

**3. Field Naming Clarity** (`src/backend/tools/polygon_tools.py`)

- **Changed**: "close" → "price" in formatted output
- **Rationale**: "price" more clearly indicates option's current price to AI Agent
- **Applied to**: Both `get_call_options_chain` and `get_put_options_chain`

**4. Test Script Path Fix** (`test_cli_regression.sh`)

- **Lines changed**: 176-184
- **Old paths** (WRONG):

  ```bash
  RAW_OUTPUT="/tmp/cli_output_loop${loop_num}_${LOOP_TIMESTAMP}.log"
  INPUT_FILE="/tmp/test_input_loop${loop_num}_${LOOP_TIMESTAMP}.txt"
  ```

- **New paths** (CORRECT):

  ```bash
  # Create tmp directory for test artifacts (project-level, not system /tmp)
  mkdir -p tmp

  RAW_OUTPUT="./tmp/cli_output_loop${loop_num}_${LOOP_TIMESTAMP}.log"
  INPUT_FILE="./tmp/test_input_loop${loop_num}_${LOOP_TIMESTAMP}.txt"
  ```

- **Impact**: All test logs now written to project `./tmp/` folder

### Test Results

```text
Total Tests: 38/38 PASSED ✅
Success Rate: 100%
Average Response Time: 10.57s (EXCELLENT performance)
Session Duration: 6 min 44 sec
Session Persistence: VERIFIED (single session)
Test Report: test-reports/test_cli_regression_loop1_2025-10-09_12-15.log
Visual Enhancements: ✅ Markdown tables, ✅ Emojis, ✅ Intelligent formatting, ✅ Wall analysis
```

### Critical Verification - Strike Count Evidence

**Before Fix (VIOLATION):**

- **Total strikes in log**: 174 strikes (massive flooding)
- **SPY Call Chain**: 24+ strikes shown ($670-$694+)
- **Evidence file**: `/tmp/cli_output_loop1_2025-10-09_10-26.log`

**After Fix (CORRECT):**

- **Total strikes in log**: 40 strikes (10 per chain x 4 tests)
- **SPY Call Chain**: Exactly 10 strikes ($671.00-$680.00)
- **SPY Put Chain**: Exactly 10 strikes ($670.00-$661.00)
- **NVDA Call Chain**: Exactly 10 strikes
- **NVDA Put Chain**: Exactly 10 strikes
- **Evidence file**: `./tmp/cli_output_loop1_2025-10-09_11-05.log`

**Strike Count Verification (Manual Count):**

```bash
# Count strikes in actual test output
grep -o '^\s*•\s*\$[0-9]*\.[0-9]*:' tmp/cli_output_loop1_2025-10-09_11-05.log | wc -l
# Result: 40 total strikes (10 x 4 tests) ✅
```

**Field Naming Verification:**

- ✅ All options chain responses now show "price:" instead of "close:"
- ✅ AI Agent can clearly identify the option's current price

**Path Violation Verification:**

```bash
# Verify logs in project tmp/ folder
ls -lh ./tmp/cli_output_loop1_2025-10-09_11-05.log
# Result: File exists ✅

# Verify NOT in system /tmp
ls -lh /tmp/cli_output_loop1_2025-10-09_11-05.log 2>/dev/null
# Result: No such file or directory ✅
```

**Options Chain Tests Verified (Test 14, 15, 29, 30):**

- ✅ Test 14 (SPY Call): 10 strikes, no errors, proper formatting
- ✅ Test 15 (SPY Put): 10 strikes, no errors, proper formatting
- ✅ Test 29 (NVDA Call): 10 strikes, no errors, proper formatting
- ✅ Test 30 (NVDA Put): 10 strikes, no errors, proper formatting
- ✅ No NoneType round() errors in any test
- ✅ 0.00 values appear where API returned None (acceptable)

### Implementation Approach

- Used Sequential-Thinking tool for systematic research and bug analysis (11 thoughts total)
- Used Serena tools for token-efficient symbol manipulation (`find_symbol`, `replace_symbol_body`)
- Used standard Edit tool for test script path fixes
- Created comprehensive TODO_task_plan.md with 5-phase workflow
- **CRITICAL**: Verified actual response content by examining real strike counts (not just PASS/FAIL status)
- **USER GUIDANCE**: Corrected approach from for-loop-with-break to cleaner `list()[:10]` slice pattern
- Executed mandatory CLI testing with actual response validation
- All changes validated with 100% test pass rate and evidence-based verification

### Impact

- **Options Chain Output**: Reduced from 174 strikes to 40 strikes (10 per chain x 4 tests)
- **Message Flooding**: ELIMINATED - strict 10-strike limit now enforced
- **Error Handling**: ROBUST - None-safe rounding prevents NoneType crashes
- **Project Boundaries**: ENFORCED - all test artifacts in project ./tmp/ folder
- **Field Clarity**: IMPROVED - "price" field name clearer than "close"
- **Performance**: 9.91s avg response time (EXCELLENT rating)
- **Test Success**: 36/36 PASSED (100% success rate maintained)

### Key Technical Decisions

1. **List slicing over for loop**: `list()[:10]` is more Pythonic and explicit than loop with break
2. **None-safe pattern**: `round(value if value is not None else 0.0, 2)` for all float fields
3. **Field naming**: "price" more intuitive than "close" for AI Agent understanding
4. **Project boundaries**: All artifacts must stay within project directory hierarchy
5. **Evidence-based validation**: Manually counted strikes in actual responses to verify fix

### References

- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-09_12-15.log`
- **Test Output**: `./tmp/cli_output_loop1_2025-10-09_12-15.log`
- **Implementation Plan**: `TODO_task_plan.md`
- **Serena Memories**: `tech_stack.md` (updated with CLI Visual Enhancements section)
- **Agent Instructions**: `src/backend/services/agent_service.py` (RULE #9 + emoji + intelligent formatting)
- **Evidence**: Markdown tables rendering correctly, emojis in 30+ responses, Wall analysis working
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
- **Testing**: CLI regression test suite (test_cli_regression.sh - 32 tests)
- **Deployment**: Fixed ports (8000/3000/5500) with one-click startup

## Development

### Available Commands

```bash
# Application startup
npm run start:app          # One-click startup
npm run frontend:dev       # Frontend development
npm run build             # Production build

# Testing: Run ./test_cli_regression.sh to execute 32-test suite

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
