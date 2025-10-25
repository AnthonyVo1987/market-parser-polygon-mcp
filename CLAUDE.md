# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and Gradio web interface for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Quick Start

### CLI Interface

```bash
# Standard Python entry point (recommended)
uv run main.py

# OR using installed script
uv run market-parser

# OR legacy method
uv run src/backend/cli.py

> Tesla stock analysis
KEY TAKEAWAYS
• TSLA showing bullish momentum...
```

### Gradio Web Interface

```bash
# Start Gradio server
uv run python src/backend/gradio_app.py

# Access at http://127.0.0.1:8000
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

### **Phase 2: MANDATORY Manual Verification of ALL 39 Tests (NO SHORTCUTS)**

🔴 **CRITICAL: Grep commands are INSUFFICIENT and will miss failures. You MUST manually review EACH test response.**

**Why Grep Fails:**
- ❌ Misses duplicate/unnecessary tool calls (agent calling same tool twice)
- ❌ Misses wrong tool selection (agent calling wrong API for data)
- ❌ Misses data inconsistencies (cross-ticker contamination, wrong data returned)
- ❌ Only catches explicit error messages, not logic errors

**MANDATORY Process for EACH of the 39 Tests:**

#### **Step 1: Read Test Response Using Read Tool**
- Use `Read` tool to read the test log file section for each test
- Read lines corresponding to that test's Agent Response, Tools Used, and Performance Metrics
- **NO scripts, NO grep shortcuts - READ each test manually**

#### **Step 2: Apply 4-Point Verification Criteria**

For EACH test, you MUST verify ALL 4 criteria:

1. ✅ **Does the response address the query?**
   - Does the agent's response directly answer the test prompt?
   - Is the response relevant to the ticker(s) mentioned?
   - Is the response complete (not truncated)?

2. ✅ **Were the RIGHT tools called (not duplicate/unnecessary calls)?**
   - **Check conversation context**: If a previous test already retrieved data, agent should NOT call the same tool again
   - Example FAIL: Test 10 calls `get_ta_indicators()`, Test 12 should NOT call it again
   - Are the tools appropriate for the query (Tradier for quotes, Polygon for TA)?
   - Are there any redundant API calls?

3. ✅ **Is the data correct?**
   - Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
   - Data formatting matches expected format (OHLC, tables, etc.)
   - No hallucinated data or made-up values
   - No cross-ticker contamination (NVDA query shouldn't return SPY data)
   - Options chains show Bid/Ask columns (NOT midpoint)

4. ✅ **Are there any errors?**
   - No error messages in response
   - No "data unavailable" messages
   - No RuntimeWarnings
   - No API errors

#### **Step 3: Document Each Test Result**

Create a table documenting ALL 39 tests:

| Test # | Test Name | Status | Issue (if failed) | Failure Type |
|--------|-----------|--------|-------------------|--------------|
| 1 | Market_Status | ❌ FAIL | timezone import error | Code Error |
| 2 | SPY_Price | ✅ PASS | - | - |
| 10 | SPY_TA_Indicators | ✅ PASS | - | - |
| 12 | SPY_Full_TA | ❌ FAIL | Duplicate call to get_ta_indicators() | Logic Error (Duplicate Tool Call) |
| ... | ... | ... | ... | ... |

**Failure Types:**
- Code Error: Syntax/runtime errors, import errors
- Logic Error (Duplicate Tool Call): Agent made unnecessary redundant API calls
- Logic Error (Wrong Tool): Agent called wrong tool for the query
- Data Error: Wrong data returned, cross-ticker contamination
- Response Error: Incomplete response, doesn't address query

#### **Step 4: Final Checkpoint Questions**

Answer ALL checkpoint questions with evidence:

1. ✅ Did you READ all 39 test responses manually using the Read tool? **YES/NO**
2. ✅ Did you apply all 4 verification criteria to EACH test? **YES/NO**
3. ✅ How many tests PASSED all 4 criteria? **X/39 PASSED**
4. ✅ How many tests FAILED (any criterion)? **X/39 FAILED**
5. ✅ Did you document ALL failures with test #, issue, and failure type? **YES/NO + TABLE**

**🔴 CANNOT MARK TASK COMPLETE WITHOUT:**
- Reading all 39 test responses manually (using Read tool, NOT grep)
- Applying all 4 verification criteria to each test
- Documenting ALL 39 tests in a results table
- Providing failure count and failure details table
- Answering all 5 checkpoint questions with evidence

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
5. ❌ Run grep commands to "verify" results (INSUFFICIENT - misses duplicate tool calls!)
6. Update documentation ✅
7. Mark task complete ❌ (NEVER manually reviewed all 39 test responses!)
```

**CORRECT (What TO do):**

```text
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN Phase 1: chmod +x test_cli_regression.sh && ./test_cli_regression.sh ✅
4. Show Phase 1 results: 39/39 COMPLETED ✅
5. PERFORM Phase 2: Use Read tool to manually read EACH of the 39 test responses ✅
6. Apply 4-point criteria to EACH test:
   - Does response address query? ✅
   - Were RIGHT tools called (no duplicates)? ✅
   - Is data correct? ✅
   - Are there any errors? ✅
7. Document ALL 39 tests in results table (PASS/FAIL with reasons) ✅
8. Answer checkpoint questions with evidence ✅
9. Provide test report path ✅
10. Update documentation with test results ✅
11. Mark task complete ✅
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

- ✅ Code changes (backend + Gradio UI)
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



## Application Startup

### Simple Command Startup

**Prerequisites:** uv, API keys in .env

**CLI Interface (recommended for automation/scripting):**
```bash
# Standard Python entry point (recommended)
uv run main.py

# Using installed console script
uv run market-parser

# Legacy method (still supported)
uv run src/backend/cli.py
```

**Gradio Web UI (recommended for interactive analysis):**
```bash
# Hot reload mode (recommended for development)
# Auto-reloads on file save, 2x-10x less CPU than standard server auto-reload
uv run gradio src/backend/gradio_app.py

# Using installed console script
uv run market-parser-gradio

# Production mode (no hot reload)
uv run python src/backend/gradio_app.py

# Access at http://127.0.0.1:8000
# PWA enabled: Install from browser address bar (Chrome/Edge)
```

## Features

### Natural Language Financial Queries

Ask questions like:

- `Tesla stock price analysis`
- `AAPL volume trends this week`
- `Show me MSFT support and resistance levels`

### Multiple Interfaces

- **Gradio Web Interface** - Python ChatInterface for financial analysis (port 8000)
- **Enhanced CLI** - Terminal interface with rich formatting

## Example Usage

### Gradio Web Interface

1. Open <http://127.0.0.1:8000>
2. Select an example or type your financial query
3. Get streaming responses with financial data and analysis
4. Examples included: Stock price queries, technical analysis, options chains, stock comparisons

**Example Response with Performance Metrics:**

```text
Market Status: CLOSED
After-hours: NO
Early-hours: NO
Exchanges: NASDAQ closed, NYSE closed, OTC closed
Server Time (UTC): 2025-10-18 01:50:12
Date: 2025-10-18

Performance Metrics:
   Response Time: 5.135s
   Tokens Used: 21,701 (Input: 21,402, Output: 299)
   Model: gpt-5-nano
```

## Architecture

- **Core**: CLI with OpenAI Agents SDK v0.2.9 and Direct Polygon/Tradier API integration
- **Web UI**: Gradio 5.49.1+ ChatInterface (port 8000) - wraps CLI core
- **Testing**: CLI regression test suite (test_cli_regression.sh - 39 tests)
- **Pattern**: CLI = core business logic, Gradio = thin wrapper (zero duplication)

## Development

### Available Commands

```bash
# CLI Interface (all methods work)
uv run main.py                    # Standard Python entry point (recommended)
uv run market-parser              # Console script
uv run src/backend/cli.py         # Legacy method

# Gradio Web UI (all methods work)
uv run gradio src/backend/gradio_app.py   # Hot reload mode (recommended for dev)
uv run market-parser-gradio               # Console script
uv run python src/backend/gradio_app.py   # Production mode (no hot reload)

# Testing
chmod +x test_cli_regression.sh && ./test_cli_regression.sh  # 39-test suite

# Code quality
npm run lint              # Python linting
npm run lint:fix          # Auto-fix with black + isort
```

### Project Structure

```text
src/
├── backend/              # All application code
│   ├── cli.py           # CLI interface (CORE BUSINESS LOGIC)
│   ├── gradio_app.py    # Gradio web UI (wraps CLI core)
│   ├── tools/           # AI agent tools (Polygon, Tradier)
│   └── services/        # Agent service layer
config/                  # Centralized configuration
│   └── app.config.json # Non-sensitive settings
```

## Troubleshooting

### Common Issues

**CLI not starting:**

```bash
# Check .env file has API keys
cat .env | grep API_KEY

# Verify dependencies
uv sync
```

**Gradio UI not loading:**

```bash
# Check port availability
netstat -tlnp | grep :8000

# Kill existing Gradio processes
pkill -f gradio_app

# Restart
uv run python src/backend/gradio_app.py
```

**API key issues:**

- Ensure both `POLYGON_API_KEY` and `OPENAI_API_KEY` are set in `.env`
- Verify API keys are valid and have sufficient credits

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
[OPTIONS_CHAIN_20_STRIKES] Options Chain Enhancement - 20 Strikes Implementation

**Summary:** Successfully expanded both Call and Put options chains from 10 to 20 strikes each (10 above + 10 below current price). Both chains now centered around current price with identical strikes and DESCENDING sort order. All manual CLI tests (4/4) and 39/39 regression tests passed with comprehensive Phase 2 manual verification.

**Changes Implemented:**

1. **Call Options Chain Enhancement** (src/backend/tools/tradier_tools.py lines 673-700)
   - Modified _get_call_options_chain() filtering logic
   - Changed from: 10 strikes with strike >= current_price
   - Changed to: 20 strikes (10 above + 10 below current price), DESCENDING sort
   - Algorithm: Split strikes above/below, select 10 from each, combine and sort DESCENDING
   - Updated get_call_options_chain() docstring (lines 757-810)
   - Docstring now reflects: "20 strike prices centered around current underlying price"
   - **Impact**: More comprehensive options data for analysis

2. **Put Options Chain Enhancement** (src/backend/tools/tradier_tools.py lines 893-920)
   - Modified _get_put_options_chain() filtering logic
   - Changed from: 10 strikes with strike <= current_price
   - Changed to: 20 strikes (10 above + 10 below current price), DESCENDING sort
   - Identical algorithm to call options for consistency
   - Updated get_put_options_chain() docstring (lines 978-1031)
   - Docstring now reflects: "20 strike prices centered around current underlying price"
   - **Impact**: Call and Put chains now have identical strike prices

3. **Documentation Updates**
   - Updated both wrapper function docstrings
   - Changed count from 10 to 20 in examples
   - Updated Note sections to reflect new behavior
   - All changes maintain backward compatibility

**Testing Results - Manual CLI + Phase 1/2 Validation:**
- ✅ **Manual CLI Tests: 6/6 PASSED** (SPY calls, SPY puts, AAPL calls, AAPL puts, NVDA calls, NVDA puts)
- ✅ **Phase 1 (Automated Response Generation): 39/39 COMPLETED**
- ✅ **Phase 2 (Manual Verification): 39/39 PASSED** (all 4 criteria met)
- ✅ **Test Report:** test-reports/test_cli_regression_loop1_2025-10-25_12-09.log
- ✅ **Average Response Time:** 10.79 seconds (EXCELLENT)
- ✅ **Critical Tests (14, 15, 29, 30):** All options chain tests PASSED with correct behavior

**Feature Validation Details:**
- Test 14 (SPY Calls): 20 strikes ($687-$668), centered around $677.25, DESCENDING ✅
- Test 15 (SPY Puts): 20 strikes ($687-$668), **IDENTICAL to calls**, DESCENDING ✅
- Test 29 (NVDA Calls): 20 strikes ($210-$162.50), centered around $186.26, DESCENDING ✅
- Test 30 (NVDA Puts): 20 strikes ($210-$162.50), **IDENTICAL to calls**, DESCENDING ✅

**Performance Impact:**
- No performance degradation (client-side filtering unchanged)
- Slightly more data displayed (20 vs 10 strikes per chain)
- API calls unchanged (already fetched all strikes)
- Table formatting auto-adapted to more rows

**Files Modified:**
- ✅ src/backend/tools/tradier_tools.py (filtering logic + docstrings for both functions)

**Documentation Updated:**
- ✅ CLAUDE.md (this summary)
- ✅ .serena/memories/options_chain_20_strikes_completion_oct_2025.md (NEW)
- ✅ research_task_plan.md (comprehensive research findings)
- ✅ TODO_task_plan.md (detailed implementation plan)

**Test Results Summary:**
- Manual CLI: 6/6 PASS
- Regression Phase 1: 39/39 COMPLETED
- Regression Phase 2: 39/39 PASSED (all 4-point criteria met)
- Zero failures, zero errors, zero data issues
- All options chain tests show 20 strikes correctly

**Risk Assessment:** VERY LOW
- Small, focused change (only filtering/sorting logic)
- Comprehensive testing (6 manual + 39 regression tests)
- No API or async pattern changes
- Backward compatible (same data structure)
- Zero test failures with new implementations

**Next Phase:** Future enhancements to options chain analysis tools
<!-- LAST_COMPLETED_TASK_END -->

## claude --dangerously-skip-permissions

## uvx --from git+https://github.com/oraios/serena serena project index

IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
