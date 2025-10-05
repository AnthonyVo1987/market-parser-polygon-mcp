# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
ta-indicators: Add 4 Technical Analysis Indicator tools using Polygon Python Library direct API

- Created 4 new TA indicator custom tools: get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd
- Expanded from 10 to 14 total tools (7 Polygon MCP + 1 Finnhub + 6 Polygon direct)
- Updated AI Agent instructions with RULE #8 for Technical Analysis Indicators
- Extended test suite from 7 to 11 tests (added 4 TA indicator test cases)
- All tools follow established @function_tool pattern with comprehensive docstrings

Implementation Details:
✅ Created 4 TA indicator tools in src/backend/tools/polygon_tools.py (604 lines added)

- get_ta_sma: Simple Moving Average (common windows: 20, 50, 200 days)
- get_ta_ema: Exponential Moving Average (common windows: 12, 20, 26, 50 days)
- get_ta_rsi: Relative Strength Index (14-day standard, 0-100 range, >70 overbought, <30 oversold)
- get_ta_macd: MACD indicator (12/26/9 standard periods, crossovers signal trend changes)
✅ Updated agent_service.py imports and create_agent() function with all 4 TA tools
✅ Added RULE #8 to agent instructions with full TA indicator guidance and examples
✅ Updated test_7_prompts_persistent_session.sh from 7 to 11 tests (4 new TA test cases)
✅ Pylint score: 10.00/10 for both polygon_tools.py and agent_service.py
✅ All imports verified working correctly

Tool Architecture Evolution:

- **BEFORE:** 10 tools (7 Polygon MCP + 1 Finnhub + 2 Polygon direct)
- **AFTER:** 14 tools (7 Polygon MCP + 1 Finnhub + 6 Polygon direct)
- **NEW TOOLS:** get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd

Critical Rules Updated:
🔴 RULE #1: Single ticker → get_stock_quote(ticker='SYMBOL') via Finnhub
🔴 RULE #2: Multiple tickers → get_snapshot_all(tickers=['S1','S2'], market_type='stocks') via Polygon MCP
🔴 RULE #4: Market status & date/time → get_market_status_and_date_time() via Polygon Direct API
🔴 RULE #8: Technical Analysis Indicators → get_ta_sma/ema/rsi/macd via Polygon Direct API ⭐ NEW
🔴 SUPPORTED TOOLS: Updated from 10 to 14 tools in agent instructions

Test Suite Updates:

- **Test 8:** "SMA for SPY" - Simple Moving Average
- **Test 9:** "20-day EMA for NVDA" - Exponential Moving Average
- **Test 10:** "RSI analysis for SPY" - Relative Strength Index
- **Test 11:** "MACD for AAPL" - MACD Indicator

ACHIEVEMENT: Successfully added comprehensive TA indicator support, enabling advanced technical analysis queries with SMA, EMA, RSI, and MACD indicators
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
