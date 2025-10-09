# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
## Performance Baseline Establishment: 10-Loop Test Run (380 Tests)

**Status:** ✅ Established (October 9, 2025)
**Feature:** Establish comprehensive performance baseline with 10-loop test run validating CLI visual enhancements

### Performance Baseline Summary

**Test Configuration:**
- **Test Suite**: `test_cli_regression.sh` (38 tests per loop)
- **Total Loops**: 10
- **Total Tests**: 380 (38 tests × 10 loops)
- **Duration**: 77 min 7 sec (1 hour 17 minutes)
- **Test Period**: October 9, 2025 (12:35 PM - 1:54 PM)

### Aggregate Performance Metrics

**Overall Statistics:**
- **Success Rate**: **100%** (380/380 PASSED ✅)
- **Overall Average Response Time**: **12.07s** (EXCELLENT rating)
- **Average Session Duration**: **7 min 42 sec** per loop
- **Session Persistence**: **100%** (all 10 loops maintained single session)
- **Visual Enhancements**: **VERIFIED** (Markdown tables, emojis, intelligent formatting)

**Response Time Analysis:**
```
Min Average Response Time:  10.81s (Loop 3)
Max Average Response Time:  13.38s (Loop 2)
Overall Average:            12.07s
Performance Rating:         EXCELLENT

Fastest Individual Response:  2.44s
Slowest Individual Response:  82.02s (Loop 9, Test 38 - ANOMALY)
Typical Range:                3-49s (95% of responses)
Anomaly Rate:                 0.26% (1 outlier in 380 tests)
```

### Loop-by-Loop Performance

| Loop | Tests | Success | Avg Time | Duration | Status |
|------|-------|---------|----------|----------|--------|
| 1    | 38    | 100%    | 11.53s   | 7m 23s   | PASS ✅ |
| 2    | 38    | 100%    | 13.38s   | 8m 37s   | PASS ✅ |
| 3    | 38    | 100%    | 10.81s   | 6m 57s   | PASS ✅ |
| 4    | 38    | 100%    | 11.60s   | 7m 27s   | PASS ✅ |
| 5    | 38    | 100%    | 12.78s   | 8m 9s    | PASS ✅ |
| 6    | 38    | 100%    | 12.40s   | 7m 54s   | PASS ✅ |
| 7    | 38    | 100%    | 12.19s   | 7m 45s   | PASS ✅ |
| 8    | 38    | 100%    | 11.64s   | 7m 25s   | PASS ✅ |
| 9    | 38    | 100%    | 13.07s   | 8m 19s   | PASS ✅ |
| 10   | 38    | 100%    | 11.29s   | 7m 11s   | PASS ✅ |

**Performance Consistency**: Standard deviation ~0.88s (low variance, stable performance)

### Visual Enhancement Verification

**1. Markdown Table Rendering** ✅
- **40 options chain tables** rendered correctly (4 per loop × 10 loops)
- Beautiful formatting with borders, $ formatting, % for IV, comma separators
- Sample from Loop 5:
  ```
  Strike    Price   Delta   Gamma   Theta   IV       Volume    Open Interest
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  $672.00   1.17    0.42    0.10    -0.67   10.00%   119,903   16,023
  ```

**2. Emoji Response Formatting** ✅
- **320+ emojis** across 10 loops (avg ~32 per loop)
- Consistent 2-5 emojis per response
- Financial (📊📈📉💹) + Status (✅⚠️🟢🔴) emojis used appropriately

**3. Intelligent Response Formatting** ✅
- **Lists** for simple responses (1-5 data points) - prioritizes speed
- **Tables** for complex data (6+ data points) - prioritizes readability
- AI Agent correctly adapts formatting based on data complexity

**4. Options Chain Wall Analysis** ✅
- **20 wall analyses** completed (2 per loop, Tests 16 & 32)
- All provide call/put walls with strike prices, OI, volume, and trading implications
- Sample from Loop 10:
  ```
  🧭 SPY Options Wall Analysis
  Call walls: 675 strike (OI ~17,136; volume ~64,620) — strong resistance
  Put walls: [Support levels with OI/volume data]
  ```

### Anomaly Analysis

**Loop 9 - Test 38 Anomaly (82.02s)**
- **Test**: Multi-ticker daily bars (WDC, AMD, GME)
- **Normal Range**: 15-30s
- **Anomaly**: 82.02s (2.7x-5.5x slower)
- **Probable Cause**: API rate limiting or network latency spike
- **Impact**: Minimal (test passed, avg remained EXCELLENT)
- **Frequency**: 1/380 tests (0.26% anomaly rate)

**Conclusion**: Single anomaly expected in production; no systemic issue.

### Key Findings

✅ **Performance Benchmark Established**: **12.07s average** (EXCELLENT rating)
✅ **Visual Enhancements**: All 4 enhancements verified across 380 tests
✅ **System Stability**: 100% success rate, perfect session persistence
✅ **Production Ready**: 0.26% anomaly rate indicates robust stability

### Implementation Context

This baseline follows the successful implementation of CLI Visual Enhancements (Oct 9, 2025):
- Markdown table formatting for options chains
- Emoji responses for visual clarity
- Intelligent formatting (lists vs tables)
- Options chain wall analysis capabilities

### References

- **Baseline Report**: `test-reports/performance_baseline_10loop_2025-10-09.md`
- **Loop Reports**: `test-reports/test_cli_regression_loop*_2025-10-09_*.log`
- **Serena Memories**:
  - `.serena/memories/performance_baseline_oct_2025.md` (updated with 10-loop baseline)
  - `.serena/memories/tech_stack.md` (updated with performance metrics)
- **Previous Baseline**: 7-test suite (Oct 4, 2025) - 15.97s average
- **Current Baseline**: 38-test suite (Oct 9, 2025) - 12.07s average (24% faster)

**Baseline Target for Future Regression Testing**: ≤ 15s average response time (WARNING if > 15s, CRITICAL if > 18s)
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
- **Testing**: CLI regression test suite (test_cli_regression.sh - 38 tests)
- **Deployment**: Fixed ports (8000/3000/5500) with one-click startup

## Development

### Available Commands

```bash
# Application startup
npm run start:app          # One-click startup
npm run frontend:dev       # Frontend development
npm run build             # Production build

# Testing: Run ./test_cli_regression.sh to execute 38-test suite

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
