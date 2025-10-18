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

### **Phase 2: MANDATORY Grep-Based Verification (EVIDENCE REQUIRED)**

Phase 2 is broken into 4 sub-phases with **MANDATORY bash commands** that MUST be executed:

#### **Phase 2a: ERROR DETECTION (MANDATORY - MUST RUN COMMANDS)**

🔴 **YOU MUST RUN these grep commands and SHOW output. Cannot proceed without evidence.**

```bash
# Command 1: Find all errors/failures
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log

# Command 2: Count 'data unavailable' errors
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log

# Command 3: Count completed tests
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Required Output**: Paste ALL grep command outputs. If you don't show grep output, Phase 2 is INCOMPLETE.

#### **Phase 2b: DOCUMENT FAILURES (MANDATORY - IF ERRORS FOUND)**

If Phase 2a grep commands found errors, create **evidence-based failure table**:

| Test # | Test Name | Line # | Error Message | Tool Call (if visible) |
|--------|-----------|--------|---------------|------------------------|
| 3 | SPY_Yesterday_Price_OHLC | 157 | data unavailable due to retrieval error | get_stock_price_history(...) |

**Required**: Show grep output + failure table with line numbers, OR confirm "0 failures found".

#### **Phase 2c: VERIFY RESPONSE CORRECTNESS (For tests without errors)**

For tests that didn't show errors in Phase 2a, verify:

1. Response directly addresses the prompt query
2. Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
3. Appropriate tool calls made (Polygon, Tradier)
4. Data formatting matches expected format (OHLC, tables, etc.)
5. No hallucinated data or made-up values
6. Options chains show Bid/Ask columns (NOT midpoint)
7. Technical analysis includes proper indicators
8. Response is complete (not truncated)

#### **Phase 2d: FINAL VERIFICATION (CHECKPOINT QUESTIONS)**

Answer ALL checkpoint questions with evidence:

1. ✅ Did you RUN the 3 mandatory grep commands in Phase 2a? **SHOW OUTPUT**
2. ✅ Did you DOCUMENT all failures found (or confirm 0 failures)? **PROVIDE TABLE OR "0 failures"**
3. ✅ Failure count from grep -c: **X failures**
4. ✅ Tests that generated responses: **X/39 COMPLETED**
5. ✅ Tests that PASSED verification (no errors): **X/39 PASSED**

**🔴 CANNOT MARK TASK COMPLETE WITHOUT:**
- Running and showing grep outputs
- Documenting failures with evidence (or confirming 0 failures)
- Providing failure count: `grep -c "data unavailable"`
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

```bash
# CLI Interface (recommended for automation/scripting)
uv run src/backend/cli.py

# Gradio Web UI (recommended for interactive analysis)
uv run python src/backend/gradio_app.py
# Access at http://127.0.0.1:8000
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
# CLI Interface
uv run src/backend/cli.py

# Gradio Web UI
uv run python src/backend/gradio_app.py

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
[REFACTOR] Complete Code Cleanup & DRY Principle Application (Phases 1-5)

**Summary:** Comprehensive 5-phase refactoring to eliminate code duplication, remove dead code, and apply DRY principles across the codebase. Refactored 10 tool functions to use centralized helper modules, reducing code duplication by ~390 lines while maintaining 100% functional compatibility.

**Phase 1: Dead Code & Legacy Comment Cleanup (-490 lines)**
- Deleted 466 lines of commented-out legacy TA tools from polygon_tools.py
- Removed dead code: get_ta_sma(), get_ta_ema(), get_ta_rsi(), get_ta_macd()
- Cleaned 8 legacy comment instances referencing retired React/FastAPI
- Updated 4 files: gradio_app.py, cli.py, formatting_helpers.py, token_utils.py
- Reduced polygon_tools.py from 841 → 375 lines (55% reduction)

**Phase 2: Helper Module Creation (+100 lines, DRY Principle)**
- Created error_utils.py: Standardized error response formatting (~50 lines)
- Created validation_utils.py: Ticker validation and sanitization (~30 lines)
- Created api_utils.py: API header generation helpers (~20 lines)
- Single source of truth for patterns duplicated 43+ times

**Phase 3: Refactored 10 Tool Functions to Use Helpers**
- Tradier Tools (5 functions): get_market_status, get_stock_quote, get_stock_price_history, get_call_options_chain, get_put_options_chain
- Polygon Tools (5 functions): get_ticker_details, get_aggregates_bars, get_previous_close, get_daily_open_close, get_grouped_daily_bars
- Eliminated code duplication across all tool functions
- Maintained 100% API compatibility and functional behavior

**Phase 4: Rename for Accuracy**
- Renamed: _map_tradier_state → _map_market_state
- Rationale: Function maps market state data (used by both Tradier and Polygon tools)
- Updated 3 references across tradier_tools.py and polygon_tools.py

**Phase 5: Final Testing & Documentation**
- ✅ Phase 1 Testing: 39/39 CLI tests COMPLETED (5 min 50 sec, avg 8.96s/test)
- ✅ Phase 2 Verification: 3 grep commands executed, 0 errors found, 0 "data unavailable" failures
- ✅ Code Quality: Linting score 9.61/10 (excellent)
- ✅ All checkpoint questions answered with evidence
- ✅ Test report: test-reports/test_cli_regression_loop1_2025-10-18_14-49.log

**Impact Statistics:**
- Code removed: ~490 lines (dead code + legacy comments)
- Code added: ~100 lines (helper modules)
- Net reduction: ~390 lines (~20% total codebase reduction)
- Files modified: 15 (7 cleaned + 3 new helpers + 5 refactored)
- Functions refactored: 10 (5 Tradier + 5 Polygon)
- Code duplication eliminated: 43+ instances
- Helper modules created: 3 (error_utils, validation_utils, api_utils)

**Test Evidence:**
- All phases tested with 39-test regression suite
- Performance metrics: 8.65s/test → 8.96s/test (stable, <3% variance)
- Zero functional regressions detected
- 39/39 tests PASSED verification across all phases

**Code Quality Improvements:**
- DRY principle applied: Single source of truth for error handling, validation, API utilities
- Maintainability: Centralized helper modules reduce future maintenance burden
- Type safety: Comprehensive type hints and docstrings in all helper modules
- Readability: Tool functions now focus on business logic, not boilerplate

**Documentation Updates:**
- Updated CLAUDE.md (this file)
- Updated .serena/memories/project_architecture.md
- Updated .serena/memories/code_style_conventions_oct_2025.md
- Updated .serena/memories/tech_stack_oct_2025.md
- Created .serena/memories/code_cleanup_refactoring_oct_2025.md
- Updated .serena/memories/react_retirement_completion_oct_2025.md
- Updated TODO_task_plan.md (all phases marked complete)

**Risk Assessment:** LOW (comprehensive testing validates no functionality changes)
<!-- LAST_COMPLETED_TASK_END -->

## claude --dangerously-skip-permissions

## uvx --from git+https://github.com/oraios/serena serena project index

IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
