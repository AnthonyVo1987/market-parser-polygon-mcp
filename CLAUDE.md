# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
## Frontend Code Duplication Elimination: Simplified Markdown Rendering

**Status:** ✅ Complete (October 9, 2025)
**Feature:** Eliminate 157 lines of duplicate frontend formatting code, simplify markdown rendering architecture

### Problem Solved

**Issue:** Frontend had **157 lines of duplicate formatting code** replicating backend markdown formatting logic

**Root Cause:**
- Backend generates markdown for both CLI and GUI
- CLI uses Rich library for rendering (clean)
- GUI used 157 lines of custom React components (duplicate logic in `ChatMessage_OpenAI.tsx`)
- Maintenance burden: changes needed in 2 places

### Solution Implemented

**File Modified:** `src/frontend/components/ChatMessage_OpenAI.tsx`

**Code Deleted (157 lines total):**
1. ✅ `createMarkdownComponents()` function (154 lines)
   - Custom React components: p, h1, h2, h3, ul, ol, li, strong, em, blockquote, code
   - All had inline styling duplicating backend formatting decisions
2. ✅ `markdownComponents` useMemo declaration (2 lines)
3. ✅ `ComponentPropsWithoutRef` import (1 line)

**Simplified Rendering:**
```typescript
// BEFORE:
<Markdown components={markdownComponents}>
  {formattedMessage.formattedContent}
</Markdown>

// AFTER:
<Markdown>
  {formattedMessage.formattedContent}
</Markdown>
```

**Result:** 157 lines deleted, zero code duplication

### Architecture Transformation

**BEFORE (Duplicate Code ❌):**
```
Backend → Generates Markdown
    ├── CLI → Rich library renders (with styling)
    └── GUI → 157 lines custom React components (with styling)
                ↑ DUPLICATE FORMATTING LOGIC
```

**AFTER (Zero Duplication ✅):**
```
Backend → Generates Markdown (Single Source of Truth)
    ├── CLI → Rich library renders
    └── GUI → Default react-markdown renders
                ↑ NO CUSTOM FORMATTING CODE
```

### Test Results & Validation

**CLI Regression Suite:**
- ✅ **38/38 PASSED** (100% success rate)
- ✅ **11.14s** average response time (EXCELLENT - within 12.07s baseline)
- ✅ **7 min 6 sec** session duration
- ✅ **Test Report:** `test-reports/test_cli_regression_loop1_2025-10-09_16-57.log`

**Frontend Validation:**
- ✅ User validated and approved GUI appearance
- ✅ No visual regression
- ✅ All markdown rendering works correctly (headings, lists, code blocks, tables)
- ✅ Options chain tables render beautifully
- ✅ Emoji responses display correctly

### Key Benefits

**1. Zero Code Duplication:**
- Backend owns all formatting decisions (markdown generation)
- Frontend is pure presentation layer
- Single source of truth maintained

**2. Simplified Maintenance:**
- Changes only needed in backend
- Frontend automatically inherits all formatting updates
- No need to sync 2 codebases

**3. Better Performance:**
- Default react-markdown is lightweight
- No custom component overhead
- Faster rendering and initial load

**4. Cleaner Codebase:**
- **-157 lines** in frontend
- Simpler component structure
- Easier to understand and maintain

### Implementation Details

**Tool Usage:**
- Sequential-Thinking: 11 thoughts total
  - Planning: 3 thoughts (tool selection strategy)
  - Implementation: 4 thoughts (deletion strategy & verification)
  - Testing: 1 thought (test result analysis)
  - Serena Updates: 2 thoughts (memory planning & verification)
  - Final Verification: 1 thought (completion check)
- Standard Edit: TypeScript file modifications (correct tool for React/TypeScript)
- Standard Write: Documentation and memory updates

**Workflow Compliance:**
- ✅ Planning Phase: Created proper implementation plan
- ✅ Implementation Phase: Used Sequential-Thinking and correct tools
- ✅ CLI Testing Phase: Ran test suite with 100% pass rate
- ✅ Frontend Testing: User validated and approved
- ✅ Serena Update Phase: Updated tech_stack.md memory
- ✅ Git Commit Phase: Atomic commit with all changes

### Documentation Created

**Research & Analysis:**
- `CORRECTED_ARCHITECTURE_RESEARCH.md` - Full architectural analysis (453 lines)
- `RESEARCH_SUMMARY.md` - Executive summary with comparison table (279 lines)
- `SOLUTION_SUMMARY.md` - Quick 1-page implementation guide (106 lines)

**Updated Files:**
- `.serena/memories/tech_stack.md` - Added "Frontend Code Duplication Elimination" section (110 lines)
- `TODO_task_plan.md` - Implementation plan with tool enforcement (768 lines)

### Impact Summary

**Frontend:**
- ✅ 157 lines deleted
- ✅ Simplified to pure presentation layer
- ✅ No custom formatting logic
- ✅ Default markdown rendering

**Backend:**
- ✅ No changes required
- ✅ Already generates markdown correctly
- ✅ Single source of truth maintained

**CLI:**
- ✅ No changes required
- ✅ Rich rendering unchanged
- ✅ 100% test pass rate

**Maintenance:**
- ✅ Changes only in backend
- ✅ Frontend auto-inherits
- ✅ No duplicate code paths

### References

- **Commit:** `b866f0a784d9607b5557c7116a62b6bab6521ffb`
- **Test Report:** `test-reports/test_cli_regression_loop1_2025-10-09_16-57.log`
- **Serena Memories:**
  - `.serena/memories/tech_stack.md` (updated with frontend simplification)
  - `.serena/memories/project_architecture.md` (updated with new markdown rendering architecture)
- **Architecture Docs:**
  - `CORRECTED_ARCHITECTURE_RESEARCH.md`
  - `RESEARCH_SUMMARY.md`
  - `SOLUTION_SUMMARY.md`

**Previous Baseline:** Performance Baseline (Oct 9, 2025) - 12.07s average (380 tests, 100% success)
**Current Task:** Frontend refactor maintains performance (11.14s average, 38 tests, 100% success)
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
