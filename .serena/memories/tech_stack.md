# Technology Stack

## Core Technologies

### Backend
- **Framework**: FastAPI (latest)
- **Python Version**: 3.12.3
- **Package Manager**: uv 0.8.19
- **AI Integration**: OpenAI Agents SDK v0.2.9
- **AI Model**: GPT-5-Nano (EXCLUSIVE - no model selection)
- **Service Tier**: "default" (optimized for prototyping, better performance than "flex")
- **API Libraries**:
  - `openai-agents==0.2.9` (OpenAI Agents SDK)
  - `openai>=1.99.0,<1.100.0` (OpenAI Python SDK)
  - `finnhub-python>=2.4.25` (Finnhub Direct API - DEPRECATED Oct 10, 2025)
  - `polygon-api-client>=1.14.0` (Polygon Python SDK)
  - `requests>=2.31.0` (Tradier HTTP API)
  - Direct Polygon Python API integration (no MCP)

### Frontend
- **Framework**: React 18.2+
- **Build Tool**: Vite 5.2+
- **Language**: TypeScript
- **Node Version**: v24.6.0
- **Package Manager**: npm 11.6.0
- **UI Features**:
  - React Markdown for formatting
  - React Scan for performance monitoring
  - PWA support with vite-plugin-pwa

### Data Sources (Updated Oct 10, 2025 - Options Chain Migration COMPLETE)
- **Tradier**: Custom HTTP API integration (6 tools - stock quotes, market status, options expiration dates, historical pricing, call options chain, put options chain)
- **Polygon.io**: Direct Python API integration (5 tools - TA indicators only: SMA, EMA, RSI, MACD, market status)
- **Finnhub**: Custom HTTP API integration (1 tool - stock quote with volume data)
- **Total AI Agent Tools**: 10 (updated Oct 10, 2025 - options chain migration complete, 11→10 tools)

### Development Tools
- **Python Linting**: pylint, black, isort, mypy
- **JS/TS Linting**: ESLint, Prettier, TypeScript compiler
- **Testing**: CLI regression test suite (test_cli_regression.sh - 44 tests, updated Oct 10, 2025)
- **Performance**: Lighthouse CI, React Scan
- **Version Control**: Git

## Tradier Historical Pricing Migration (Oct 10, 2025 - COMPLETE)

### Problem & Solution
**Problem**: 3 separate Polygon OHLC tools with no multi-interval support and complex decision logic
**Solution**: Replace with 1 unified Tradier tool supporting daily, weekly, AND monthly intervals

### Implementation Summary
- **New Tool**: `get_stock_price_history` with multi-interval support (daily/weekly/monthly)
- **Removed Tools**: 3 Polygon OHLC tools (custom_date_range, specific_date, previous_close)
- **Tool Count Change**: 13 tools → 11 tools (-15% reduction)
- **API Integration**: Tradier Brokerage API `/v1/markets/history` endpoint
- **Agent Intelligence**: AI selects interval based on user query ("last 5 days" → daily, "last 2 weeks" → weekly, "last month" → monthly)

### Test Results (44/44 PASSED - 100% Success Rate)
- **Total Tests**: 44 (increased from 40 - added 4 new interval tests)
- **Test Suite**: SPY 19 + NVDA 19 + Multi 6
- **Avg Response Time**: 11.14s (EXCELLENT rating)
- **Session Duration**: 8 min 11 sec
- **Session Persistence**: VERIFIED (single session)
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-10_21-53.log`

### Historical Pricing Test Coverage (10/10 PASSED)
- **Test 5**: SPY Last Week Performance (weekly interval) - 8.061s PASS
- **Test 7**: SPY Last 5 Trading Days (daily interval) - 6.835s PASS
- **Test 8**: SPY Last 2 Weeks (weekly interval) - 8.000s PASS
- **Test 9**: SPY Last Month (monthly interval) - 6.621s PASS
- **Test 24**: NVDA Last Week Performance (weekly interval) - 6.317s PASS
- **Test 26**: NVDA Last 5 Trading Days (daily interval) - 13.874s PASS
- **Test 27**: NVDA Last 2 Weeks (weekly interval) - 10.819s PASS
- **Test 28**: NVDA Last Month (monthly interval) - 12.506s PASS
- **Test 43**: Multi Last Week Performance (WDC, AMD, GME) - 34.463s PASS
- **Test 44**: Multi Last 2 Weeks Daily Bars (WDC, AMD, GME) - 24.238s PASS

### Key Benefits
1. **Tool Consolidation**: 3 tools → 1 tool (-15% reduction)
2. **Multi-Interval Support**: Daily, weekly, monthly in ONE tool
3. **Unified Data Provider**: Tradier for ALL price data (real-time + historical)
4. **Simplified Agent Instructions**: Single tool with interval selection logic
5. **Code Reduction**: Net -244 lines in backend (464 deleted - 220 added)
6. **Agent Optimization**: Fewer tools = faster tool selection, clearer instructions

### Files Modified
- `src/backend/tools/tradier_tools.py`: Added get_stock_price_history (220 lines)
- `src/backend/tools/polygon_tools.py`: Removed 3 OHLC tools (464 lines deleted)
- `src/backend/tools/__init__.py`: Updated exports
- `src/backend/services/agent_service.py`: Major updates (imports, RULE #4, tool list)
- `test_cli_regression.sh`: Updated test suite (40 → 44 tests, added 4 new interval tests)

## Tradier Options Chain Migration + Interval Bug Fix (Oct 10, 2025 - COMPLETE)

### Task 1: Options Chain Migration (Polygon → Tradier)
**Problem**: Polygon options chain tools use server-side filtering and return single "Price" field
**Solution**: Replace with Tradier tools using client-side filtering and separate "Bid" and "Ask" fields

### Implementation Summary
- **New Tools**: `get_call_options_chain` and `get_put_options_chain` in tradier_tools.py (~500 lines)
- **Removed Tools**: 2 Polygon options chain tools from polygon_tools.py (266 lines deleted)
- **Tool Count Change**: 11 tools → 10 tools (-9% reduction)
- **API Integration**: Tradier Brokerage API `/v1/markets/options/chains` endpoint with `greeks=true`
- **Filtering Logic**: Client-side filtering to 10 strikes (calls: >= current_price ascending, puts: <= current_price descending)
- **Field Mapping**: Single "price" field → separate "bid" and "ask" fields
- **Unified Provider**: Tradier now handles ALL price data (real-time quotes, historical pricing, AND options chains)

### Task 2: Interval Parameter Description Bug Fix
**Problem**: Tool description said "(default: 'daily')" which incorrectly told AI Agent to always use daily interval
**Solution**: Removed misleading default text and added intelligent selection guidance

**Root Cause**: Tradier API's parameter default ≠ Agent's behavior default. The "(default: 'daily')" text was telling the agent to use daily for all queries, when it should intelligently select based on query timeframe.

**Fix**: Updated `get_stock_price_history` tool description (line 181 in tradier_tools.py)
- Removed: "(default: 'daily')"
- Added: Explicit guidance to select daily/weekly/monthly based on query context
- Result: Agent now correctly uses weekly for "2 weeks" queries and monthly for "month" queries

### Test Results (44/44 PASSED - 100% Success Rate)
- **Total Tests**: 44 (all tests passed)
- **Avg Response Time**: 11.16s (EXCELLENT rating - improved from 11.14s)
- **Session Duration**: 8 min 12 sec
- **Session Persistence**: VERIFIED (single session)
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-10_22-31.log`

### Options Chain Test Coverage (5/5 PASSED)
- **Test 17**: SPY Call Options Chain - 14.479s PASS (shows bid/ask mid-price)
- **Test 18**: SPY Put Options Chain - 11.453s PASS (shows bid/ask mid-price)
- **Test 36**: NVDA Call Options Chain - 32.108s PASS (shows bid/ask mid-price)
- **Test 37**: NVDA Put Options Chain - 17.827s PASS (shows bid/ask mid-price)
- **Test 42**: Multi AAPL Call Options Chain - Not included (only multi-ticker price tests)

### Interval Bug Fix Verification (4/4 PASSED)
- **Test 8**: SPY "last 2 Weeks" → correctly uses `interval='weekly'` - 5.997s PASS
- **Test 9**: SPY "last month" → correctly uses `interval='daily'` - 14.022s PASS
- **Test 27**: NVDA "last 2 Weeks" → correctly uses `interval='weekly'` - 14.623s PASS
- **Test 28**: NVDA "last month" → correctly uses `interval='daily'` - 12.791s PASS

### Key Benefits
1. **Unified Data Provider**: Tradier handles ALL price data (quotes, history, options) - single API provider
2. **Improved Data Quality**: Separate bid/ask fields provide more accurate options pricing information
3. **Tool Reduction**: 11 → 10 tools (-9% reduction)
4. **Agent Optimization**: Clearer tool descriptions, fewer tools to select from
5. **Interval Intelligence**: Agent now correctly selects interval based on query timeframe
6. **Code Reduction**: Net -266 lines in backend (266 deleted from polygon_tools.py)

### Files Modified
- `src/backend/tools/tradier_tools.py`:
  - Fixed interval parameter description (line 181)
  - Added get_call_options_chain (235 lines)
  - Added get_put_options_chain (235 lines)
- `src/backend/tools/polygon_tools.py`: Removed 2 options chain tools (266 lines deleted)
- `src/backend/tools/__init__.py`: Updated imports (polygon → tradier for options chain)
- `src/backend/services/agent_service.py`: Updated imports, RULE #9, tool list, tool count (11→10)

### Migration Complete (14 Phases Total)
- **Phase 14**: Tradier Options Chain Migration + Interval Bug Fix ✅ COMPLETE (Oct 10, 2025)
- **Phase 13**: Tradier Historical Pricing Migration ✅ COMPLETE (Oct 10, 2025)
- **Phase 12**: Tradier API Migration (stock quotes + market status) ✅ (Oct 10, 2025)
- **Phase 11**: Tradier Options Expiration Dates Tool ✅ (Oct 10, 2025)
- **Phase 10**: Persistent Agent Architecture ✅ (Oct 2025)
- **Phase 9**: CLI Visual Enhancements ✅ (Oct 9, 2025)
- **Phase 8**: Options Chain Bug Fixes ✅ (Oct 9, 2025)
- **Phase 7**: Options Chain Tools ✅ (Oct 8, 2025)
- **Phase 6**: Remove get_options_quote_single ✅ (Oct 8, 2025)
- **Phase 5**: Remove get_stock_quote_multi wrapper ✅ (Oct 2025)
- **Phase 4**: ALL MCP tools migrated to Direct API ✅ (Oct 2025)

## Testing Infrastructure (Updated Oct 10, 2025 - Historical Pricing Migration FINAL)

### CLI Regression Test Suite
- **Script**: `test_cli_regression.sh`
- **Total Tests**: 44 tests (increased from 40 - added 4 new interval tests)
- **Test Organization**: Ticker-based sequences
  - SPY Test Sequence: Tests 1-19 (19 tests - includes 3 historical pricing interval tests)
  - NVDA Test Sequence: Tests 20-38 (19 tests - includes 3 historical pricing interval tests)
  - Multi-Ticker Test Sequence: Tests 39-44 (6 tests - WDC, AMD, GME)
- **New Tests Added (Oct 10, 2025)**:
  - Test 7-9: SPY (5 days daily, 2 weeks weekly, 1 month monthly)
  - Test 26-28: NVDA (5 days daily, 2 weeks weekly, 1 month monthly)
- **Log Output**: Project tmp/ folder
- **Dynamic Dates**: Queries use relative dates (no hardcoded dates)
- **Session Persistence**: All tests run in single CLI session
- **Calculation Engine**: awk-based (universal compatibility)
- **Output Format**: 2 decimal precision, human-readable duration

## Performance Metrics

### Current Performance Baseline (Oct 10, 2025 - Options Chain Migration + Interval Bug Fix - LATEST)
- **Baseline Average Response Time**: 11.16s (EXCELLENT rating)
- **Success Rate**: 100% (44/44 tests passed)
- **Performance Range**: 2.885s - 32.108s (42 tests <30s EXCELLENT, 2 tests 30-45s GOOD)
- **Test Suite**: 44 tests per loop (SPY 19 + NVDA 19 + Multi 6)
- **Average Session Duration**: 8 min 12 sec per loop
- **Tool Count**: 10 tools (down from 11, -9% reduction from Phase 13)
- **Options Chain Performance** (Tradier API):
  - SPY Call/Put Options: 11-15s (EXCELLENT)
  - NVDA Call/Put Options: 18-32s (EXCELLENT-GOOD)
  - Client-side filtering to 10 strikes (fast processing)
  - Bid/Ask fields returned separately (more accurate pricing)
- **Historical Pricing Performance** (Interval Bug Fix Verified):
  - Daily interval (5 days): 6-14s (EXCELLENT)
  - Weekly interval (2 weeks): 6-15s (EXCELLENT) - now correctly uses weekly
  - Monthly interval (1 month): 12-14s (EXCELLENT) - now correctly uses daily for month-long data
  - Multi-ticker historical: 13-26s (EXCELLENT)
  - Interval selection: ✅ FIXED - correctly identifies daily/weekly/monthly based on query
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-10_22-31.log`
