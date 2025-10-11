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

### Data Sources (Updated Oct 10, 2025 - Historical Pricing Migration COMPLETE)
- **Tradier**: Custom HTTP API integration (4 tools - stock quotes, market status, options expiration dates, historical pricing)
- **Polygon.io**: Direct Python API integration (8 tools - TA indicators & options chains only)
- **Finnhub**: REMOVED Oct 10, 2025 - migrated to Tradier
- **Total AI Agent Tools**: 11 (updated Oct 10, 2025 - historical pricing migration complete, 13→11 tools)

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

### Migration Complete (13 Phases Total)
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

### Current Performance Baseline (Oct 10, 2025 - Historical Pricing Migration with New Test Suite - LATEST)
- **Baseline Average Response Time**: 11.14s (EXCELLENT rating)
- **Success Rate**: 100% (44/44 tests passed)
- **Performance Range**: 3.100s - 35.638s (42 tests <30s EXCELLENT, 2 tests 30-45s GOOD)
- **Test Suite**: 44 tests per loop (SPY 19 + NVDA 19 + Multi 6)
- **Average Session Duration**: 8 min 11 sec per loop
- **Test Suite Update**: Added 4 new interval tests (daily 5 days, weekly 2 weeks, monthly 1 month)
- **Tool Count**: 11 tools (down from 13, -15% reduction)
- **Historical Pricing Performance**:
  - Daily interval (5 days): 6-14s (EXCELLENT)
  - Weekly interval (2 weeks): 8-11s (EXCELLENT)
  - Monthly interval (1 month): 7-13s (EXCELLENT)
  - Multi-ticker historical: 24-34s (EXCELLENT-GOOD)
  - Interval selection: Correctly identifies daily/weekly/monthly based on query
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-10_21-53.log`
