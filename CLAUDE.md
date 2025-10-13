# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Quick Start

### CLI Interface

```bash
uv run src/backend/main.py

> Tesla stock analysis
KEY TAKEAWAYS
• TSLA showing bullish momentum...
```


# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

🔴 CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process

## 🔴 MANDATORY: SYSTEMATIC TOOL USAGE ENFORCEMENT

**YOU MUST use Sequential-Thinking and Serena tools throughout ENTIRE implementation:**

- **START every phase** with Sequential-Thinking for systematic approach
- **Use Serena tools** for code analysis, symbol manipulation, pattern searches
- **Use Sequential-Thinking** repeatedly for complex reasoning and planning
- **Use Standard Read/Write/Edit** only when Serena doesn't support the specific operation
- **NEVER stop using advanced tools** until task completion

### Serena Tool Setup

Before using Serena tools for code analysis, get the initial instructions to understand optimal usage:

- **Primary Method (Preferred)**: Use `mcp__serena__initial_instructions` tool
- **Fallback Method**: If tool fails, use `mcp__serena__read_memory` with memory name: `serena_initial_instructions`

These instructions provide critical guidance on:

- Token-efficient code exploration using symbolic tools
- Proper file reading vs. full file scanning
- Symbol overview and targeted symbol reads
- Pattern searching for flexible searches

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

## 🔴 CRITICAL: MANDATORY TESTING CHECKPOINT - TWO-PHASE VALIDATION

**Testing is NOT optional - it is REQUIRED for task completion:**

### **Two-Phase Testing Workflow (MUST FOLLOW):**

1. **Code Implementation** → Create/update code
2. **Test Suite Update** → Create/update test files
3. **🔴 PHASE 1 (MANDATORY)** → RUN the test suite to generate responses
4. **🔴 PHASE 2 (MANDATORY)** → MANUALLY VERIFY each response for correctness
5. **Documentation** → Update docs with test results

### **Phase 1: Automated Response Generation**

✅ **MUST DO:**

- Execute test suite: `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`
- Script generates all 39 test responses
- Script reports "X/39 COMPLETED" (responses received)
- **LIMITATION**: Script CANNOT validate response correctness
- Show Phase 1 results to user (completion counts, response times)
- Provide test report file path

### **Phase 2: Manual Response Verification**

✅ **MUST DO (FOR EACH OF 39 RESPONSES):**

- 🔴 MANDATORY - VERIFY THE CONTENT OF EACH TEST PROMPT RESPONSE:
  1. Response directly addresses the prompt query
  2. Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
  3. Appropriate tool calls made (Polygon, Finnhub, Tradier)
  4. Data formatting matches expected format (OHLC, tables, etc.)
  5. No hallucinated data or made-up values
  6. Options chains show Bid/Ask columns (NOT midpoint)
  7. Technical analysis includes proper indicators
  8. Response is complete (not truncated)
- Answer checkpoint question: "Did you verify EACH response?"
- Document any issues found
- Fix issues and re-run Phase 1 if needed

❌ **NEVER DO:**

- Skip Phase 1 test execution
- Skip Phase 2 manual verification
- Claim completion without test results AND manual verification
- Mark task "done" without Phase 2 evidence
- Proceed to documentation without running both phases

### **Enforcement Rules:**

🔴 **Code without Phase 1 execution = Code NOT implemented**
🔴 **Phase 1 without Phase 2 verification = Testing INCOMPLETE**
🔴 **No manual verification = Task INCOMPLETE**
🔴 **Phase 2 verification is PROOF of correctness**
🔴 **Both phases must complete BEFORE documentation updates**

### **Key Insight:**

The script saying "39/39 COMPLETED" means "39 responses received" NOT "39 tests passed validation".

Only after Phase 2 manual verification can you claim tests passed.

### **Pattern Recognition:**

**WRONG (What NOT to do):**

```text
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN Phase 1: ./test_cli_regression.sh ✅
4. Show results: 39/39 COMPLETED ✅
5. Update documentation ✅
6. Mark task complete ❌ (NEVER performed Phase 2 verification!)
```

**CORRECT (What TO do):**

```text
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN Phase 1: chmod +x test_cli_regression.sh && ./test_cli_regression.sh ✅
4. Show Phase 1 results: 39/39 COMPLETED ✅
5. PERFORM Phase 2: Manual verification of all 39 responses ✅
6. Answer checkpoint: "Did you verify EACH response?" YES ✅
7. Provide test report path ✅
8. Update documentation with test results ✅
9. Mark task complete ✅
```

### **When to Run Tests:**

- After creating new tools/functions
- After modifying existing code
- After updating AI agent instructions
- After changing test suite
- Before updating documentation
- Before claiming task completion

**Remember: If you haven't RUN Phase 1, PERFORMED Phase 2, and SHOWN both results, the task is NOT complete.**

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



**One-Click REACT GUI Application Backend & Frontend Server Startup Scripts:**

The startup scripts automatically START all development servers BUT **DOES
NOT OPEN THE APP IN BROWSER AUTOMATICALLY**.

```bash
# Option 1: XTerm startup script (RECOMMENDED - WORKING)
chmod +x start-app-xterm.sh && ./start-app-xterm.sh

# Option 2: Main startup script (NOW WORKING - FIXED)
chmod +x start-app.sh && ./start-app.sh
```

## What the Scripts Do

**Prerequisites:** uv, Node.js 18+, API keys in .env

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
- **Testing**: CLI regression test suite (test_cli_regression.sh - 39 tests)
- **Deployment**: Fixed ports (8000/3000/5500) with one-click startup

## Development

### Available Commands

```bash
# Application startup
npm run start:app          # One-click startup
npm run frontend:dev       # Frontend development
npm run build             # Production build

# Testing: Run chmod +x test_cli_regression.sh && ./test_cli_regression.sh to execute 39-test suite

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

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
[TESTING] Two-Phase Test Validation Framework + 39-Test Suite Update

**Problem:** Test script reporting "PASS" for any response received, creating false confidence that tests were actually correct
**Root Cause:** Script could only verify response receipt, not response correctness or proper tool calls/formatting
**Solution:** Implemented two-phase testing framework separating automated response generation from manual verification

**Implementation Changes:**
- test_cli_regression.sh: Updated 40→39 tests with new OHLC-focused prompts ($GME→$SOUN)
  - Replaced all "PASS/FAIL" terminology with "COMPLETED/INCOMPLETE"
  - Added Phase 2 verification instructions in script output (lines 475-501)
  - Updated variable names throughout (passed_tests→completed_tests)
- CLAUDE.md: Updated testing checkpoint with comprehensive two-phase workflow (lines 55-153)
- .serena/memories/testing_procedures.md: Added critical two-phase testing section
- .serena/memories/task_completion_checklist.md: Fully updated with two-phase approach while preserving all original content

**Phase 1 Test Results (Automated Response Generation):**
- ✅ 39/39 responses COMPLETED (100% generation rate)
- ✅ 9.14s average response time (EXCELLENT rating)
- ✅ Test duration: 5 min 58 sec
- ✅ Test report: test-reports/test_cli_regression_loop1_2025-10-12_16-56.log

**Phase 2 Test Results (Manual Verification):**
- ✅ All 39 responses directly address prompts
- ✅ All ticker symbols correct ($SPY, $NVDA, $WDC, $AMD, $SOUN)
- ✅ Appropriate tool calls made (Polygon, Tradier)
- ✅ Data formatting correct (OHLC, tables)
- ✅ No hallucinated data detected
- ✅ Options chains show separate Bid/Ask columns (NOT midpoint)
- ✅ Technical analysis includes proper indicators (RSI, MACD, SMAs, EMAs)
- ✅ All responses complete (not truncated)

**Key Insight:**
"39/39 COMPLETED" means "39 responses received" NOT "39 tests passed validation"
Only Phase 2 manual verification proves correctness

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
<!-- LAST_COMPLETED_TASK_END -->

## claude --dangerously-skip-permissions


IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
