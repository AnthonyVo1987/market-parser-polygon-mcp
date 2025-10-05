# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
mcp-to-direct-api-migration: Replace 5 MCP Tools with Polygon Python Library Direct API Custom Tools

- Created 5 new custom tools to replace MCP tools: get_stock_quote_multi, get_options_quote_single, get_OHLC_bars_custom_date_range, get_OHLC_bars_specific_date, get_OHLC_bars_previous_close
- Expanded from 14 to 18 total tools (6 Polygon MCP + 1 Finnhub + 11 Polygon direct)
- Updated AI Agent instructions: RULE #2 (multi-ticker), RULE #3 (options), RULE #5 (OHLC bars)
- Extended test suite from 11 to 16 tests (added 5 new test cases)
- Removed get_aggs tool (not relevant for analysis)
- All tools follow established @function_tool pattern with comprehensive docstrings

Implementation Details:
✅ Created 5 custom tools in src/backend/tools/polygon_tools.py (738 lines added):

1. **get_stock_quote_multi**: Multi-ticker snapshot quotes (replaces get_snapshot_all MCP)
   - Uses client.get_snapshot_all(market_type, tickers)
   - Supports stocks, options, forex, crypto market types
   - Returns snapshot data for all tickers with day/min/prevDay prices

2. **get_options_quote_single**: Single options contract quote (replaces get_snapshot_option MCP)
   - Uses client.get_snapshot_option(underlying_asset, option_contract)
   - Returns contract details, Greeks (delta/gamma/theta/vega), implied volatility
   - Full options analysis support

3. **get_OHLC_bars_custom_date_range**: Custom date range OHLC bars (replaces list_aggs MCP)
   - Uses client.list_aggs(ticker, multiplier, timespan, from_, to, limit)
   - Supports minute/hour/day/week/month/quarter/year timespans
   - Flexible date range queries

4. **get_OHLC_bars_specific_date**: Specific date OHLC bars (replaces get_daily_open_close_agg MCP)
   - Uses client.get_daily_open_close_agg(ticker, date, adjusted)
   - Returns OHLC for exact trading day
   - Handles splits/dividends with adjusted parameter

5. **get_OHLC_bars_previous_close**: Previous trading day OHLC (replaces get_previous_close_agg MCP)
   - Uses client.get_previous_close_agg(ticker, adjusted)
   - Automatically handles weekends/holidays
   - Returns most recent completed trading day

✅ Updated agent_service.py imports and create_agent() with all 11 Polygon direct tools
✅ Updated AI Agent instructions with new RULES and tool mappings
✅ Created test_16_prompts_persistent_session.sh with 16 tests (5 new OHLC/multi-ticker/options)
✅ All tools validated with Polygon Python Library direct API

Tool Architecture Evolution:

- **BEFORE:** 14 tools (7 Polygon MCP + 1 Finnhub + 6 Polygon direct)
- **AFTER:** 18 tools (6 Polygon MCP + 1 Finnhub + 11 Polygon direct)
- **NEW TOOLS:** get_stock_quote_multi, get_options_quote_single, get_OHLC_bars_custom_date_range, get_OHLC_bars_specific_date, get_OHLC_bars_previous_close
- **REMOVED:** get_aggs (not relevant for analysis)

Critical Rules Updated:
🔴 RULE #1: Single ticker → get_stock_quote(ticker='SYMBOL') via Finnhub
🔴 RULE #2: Multiple tickers → get_stock_quote_multi(tickers=['S1','S2'], market_type='stocks') via Polygon Direct API ⭐ UPDATED
🔴 RULE #3: Options → get_options_quote_single(underlying_asset, option_contract) via Polygon Direct API ⭐ UPDATED
🔴 RULE #4: Market status & date/time → get_market_status_and_date_time() via Polygon Direct API
🔴 RULE #5: Historical OHLC → get_OHLC_bars_* tools via Polygon Direct API ⭐ NEW
🔴 RULE #8: Technical Analysis Indicators → get_ta_sma/ema/rsi/macd via Polygon Direct API
🔴 SUPPORTED TOOLS: Updated from 14 to 18 tools in agent instructions

Test Suite Updates:

- **Test 12:** "Multi-ticker quotes: AAPL, MSFT, GOOGL" - Multi-ticker snapshot
- **Test 13:** "Options quote for SPY December 650 call" - Options contract quote
- **Test 14:** "AAPL daily bars from January 1 to March 31, 2024" - Custom date range OHLC
- **Test 15:** "TSLA price on December 15, 2024" - Specific date OHLC
- **Test 16:** "SPY previous trading day close" - Previous close OHLC

MCP Migration Progress:

- **Migrated to Direct API (11 tools):** get_market_status_and_date_time, get_stock_quote_multi, get_options_quote_single, get_OHLC_bars_custom_date_range, get_OHLC_bars_specific_date, get_OHLC_bars_previous_close, get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd, get_stock_quote (Finnhub)
- **Remaining MCP Tools (6):** get_snapshot_all, get_snapshot_option, list_aggs, get_daily_open_close_agg, get_previous_close_agg (still available via MCP for backward compatibility)

ACHIEVEMENT: Successfully migrated 5 critical MCP tools to Polygon Python Library direct API, improving performance, simplicity, and control. Extended test suite to 16 tests covering all new OHLC bar, multi-ticker, and options functionality.
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
- Execute test suite (e.g., `./test_16_prompts_persistent_session.sh`)
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
```
1. Create 5 new tools ✅
2. Update test suite file ✅
3. Update documentation ✅
4. Mark task complete ❌ (NEVER ran tests!)
```

**CORRECT (What TO do):**
```
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN test suite: ./test_16_prompts_persistent_session.sh ✅
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
