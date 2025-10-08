# Project Architecture

## Overview

Market Parser is a Python CLI and React web application for natural language financial queries using Direct Polygon/Finnhub API integration and OpenAI GPT-5-Nano via the OpenAI Agents SDK v0.2.9.

**Key Architectural Changes (Oct 2025):**
- **Migrated from MCP to Direct API** (70% performance improvement)
- **Removed get_stock_quote_multi wrapper** (leverages SDK parallel execution)
- **Fixed OHLC display requirements** (show actual data, not just "retrieved")
- **Enhanced chat history analysis** (prevent redundant Support/Resistance calls)
- **All 11 tools now use Direct Python APIs** (no MCP overhead)

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interfaces                      │
├─────────────────────┬───────────────────┬───────────────────┤
│   React Web App     │    CLI Interface  │   REST API        │
│   (Port 3000)       │   (Terminal)      │   (Port 8000)     │
└──────────┬──────────┴───────────┬───────┴──────┬────────────┘
           │                      │               │
           └──────────────────────┼───────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │      FastAPI Backend      │
                    │    (uvicorn on :8000)     │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   OpenAI Agents SDK       │
                    │   v0.2.9 (GPT-5-Nano)     │
                    │   Parallel Tool Execution │
                    │   Chat History Analysis   │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   AI Agent Tools (11)     │
                    │   Direct API Integration  │
                    │   OHLC Display Fix        │
                    └─────────┬────────┬────────┘
                              │        │
                    ┌─────────▼──┐  ┌─▼────────┐
                    │ Polygon.io │  │ Finnhub  │
                    │ Direct API │  │ Direct   │
                    │ (10 tools) │  │ (1 tool) │
                    └────────────┘  └──────────┘
```

## Backend Architecture

### FastAPI Application (main.py)

**Key Components:**
- `app` - FastAPI application instance
- `lifespan` - Async context manager for startup/shutdown
- `shared_session` - Shared aiohttp session for API calls
- `add_process_time_header` - Middleware for response timing
- CORS configuration for frontend communication

**Endpoints:**
- `POST /query` - Process natural language queries
- `GET /health` - Health check endpoint
- `GET /` - Root endpoint with API info

**Features:**
- Real-time response timing via middleware
- Token usage tracking from OpenAI responses
- CORS enabled for http://127.0.0.1:3000
- Async request handling
- Shared HTTP session for efficiency

### Agent Service (services/agent_service.py)

**Functions:**
- `get_enhanced_agent_instructions()` - Returns optimized system prompt with 9 RULES
- `get_optimized_model_settings()` - Returns GPT-5-Nano config
- `create_agent()` - Creates OpenAI agent with all 11 tools

**Agent Configuration:**
- **Model**: GPT-5-Nano (EXCLUSIVE - no model selection)
- **Max Tokens**: 16384
- **Temperature**: 0.1 (deterministic)
- **Parallel Tool Calls**: Enabled (critical for multi-ticker queries)
- **Rate Limits**: 200K TPM (GPT-5-Nano specific)

**System Prompt Features (9 RULES):**
- **RULE #1**: Single ticker = get_stock_quote()
- **RULE #2**: Multiple tickers = parallel get_stock_quote() calls (max 3 per batch)
- **RULE #3**: Options = get_options_quote_single()
- **RULE #4**: Market status = get_market_status_and_date_time()
- **RULE #5**: OHLC data with **CRITICAL DISPLAY REQUIREMENTS** (Oct 7 fix)
- **RULE #6**: Work with available data
- **RULE #7**: Market closed = still provide data
- **RULE #8**: Technical analysis - check chat history first
- **RULE #9**: Chat history analysis with **Scenario 5** for Support/Resistance (Oct 7 fix)

**Latest Fixes (Oct 7, 2025 Evening):**
1. **RULE #5 OHLC Display Requirements:**
   - For custom date range: MUST show start open, end close, $ and % change, period high/low, trading days
   - For specific date: MUST show Date, Open, High, Low, Close, Volume
   - NEVER just say "data retrieved" without actual numbers
   - Good vs bad response examples included
2. **RULE #9 Scenario 5 (Support & Resistance):**
   - Explicitly tells AI to use existing price/SMA/EMA data
   - Prevents redundant TA tool calls when all data already retrieved
   - 29% performance improvement (5.491s → 3.900s)

### Direct API Tools (11 Total)

#### Finnhub Custom API (1 tool)
**File:** `src/backend/tools/finnhub_tools.py`

**Tools:**
1. `get_stock_quote(symbol: str)` - Real-time stock quotes
   - Uses `finnhub-python>=2.4.25`
   - Returns: current price, change, percent change, high, low, open, previous close
   - **Supports parallel calls** for multi-ticker queries (max 3 per batch)

**Implementation:**
- `_get_finnhub_client()` - Singleton client initialization
- Environment: `FINNHUB_API_KEY`

#### Polygon Direct API (10 tools)
**File:** `src/backend/tools/polygon_tools.py`

**Market Data Tools:**
1. `get_market_status_and_date_time()` - Market status + current datetime
2. `get_options_quote_single(ticker: str)` - Single option quote

**OHLC Data Tools:**
3. `get_OHLC_bars_custom_date_range(...)` - OHLC bars for date range (**Display fix applied**)
4. `get_OHLC_bars_specific_date(...)` - OHLC bars for specific date (**Display fix applied**)
5. `get_OHLC_bars_previous_close(...)` - Previous close OHLC

**Technical Analysis Tools:**
6. `get_ta_sma(...)` - Simple Moving Average
7. `get_ta_ema(...)` - Exponential Moving Average
8. `get_ta_rsi(...)` - Relative Strength Index
9. `get_ta_macd(...)` - MACD

**Removed (Oct 7, 2025):**
- ~~`get_stock_quote_multi(...)`~~ - Replaced by parallel get_stock_quote() calls

**Implementation:**
- `_get_polygon_client()` - Singleton client initialization
- Direct Polygon Python SDK integration
- Environment: `POLYGON_API_KEY`

### Configuration Management

**Files:**
- `.env` - API keys (POLYGON_API_KEY, OPENAI_API_KEY, FINNHUB_API_KEY)
- `config/app.config.json` - Non-sensitive settings
- `src/backend/config.py` - Config loader

**Environment Variables:**
```
POLYGON_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
FINNHUB_API_KEY=your_key_here
```

## Frontend Architecture

### React Application Structure

**Entry Point:** `src/frontend/main.tsx`
- Renders `<App />` to `#root`
- Strict mode enabled for development

**Root Component:** `src/frontend/App.tsx`
- Main application logic
- State management (messages, loading)
- API communication
- Performance monitoring

**Key Components:**
- `ChatInterface` - User input and message display
- `MessageList` - Renders chat messages
- `PerformanceMetrics` - Real-time performance display

### State Management

**React State (useState):**
- `messages` - Chat message history
- `isLoading` - Request loading state
- `config` - App configuration from config/app.config.json

**No external state management library** - Simple useState/useEffect patterns

### API Communication

**Service:** `src/frontend/services/api.ts`
- `sendQuery(query: string)` - POST to `/query` endpoint
- Base URL: `http://127.0.0.1:8000`
- Returns: agent response + performance metrics

**Response Format:**
```typescript
{
  response: string;           // Agent's formatted response
  input_tokens?: number;      // Input token count
  output_tokens?: number;     // Output token count
  total_tokens?: number;      // Total token count
  model?: string;            // Model used (gpt-5-nano)
  response_time?: number;    // Response time in seconds
}
```

**Dual Naming Convention Support:**
- `input_tokens` OR `prompt_tokens`
- `output_tokens` OR `completion_tokens`
- Both naming conventions supported for compatibility

### Build System

**Tool:** Vite 5.2+
- Fast HMR (Hot Module Replacement)
- TypeScript support
- React plugin (@vitejs/plugin-react)
- PWA plugin (vite-plugin-pwa)
- CSS optimization (PostCSS, cssnano)

**Build Modes:**
- `development` - Dev mode with source maps
- `staging` - Staging environment
- `production` - Optimized production build

**Output:** `dist/` directory
- Optimized JavaScript bundles
- Minified CSS
- Service worker for PWA
- Static assets

## Data Flow

### Query Processing Flow

1. **User Input** (Web or CLI)
   - User types natural language query
   - Frontend/CLI sends to backend

2. **Backend Processing** (FastAPI)
   - Receives POST /query request
   - Creates OpenAI agent with 11 tools
   - Passes query to agent

3. **AI Agent Processing** (OpenAI Agents SDK)
   - Analyzes query
   - **STEP 0**: Checks chat history for existing data (RULE #9)
   - Determines which tools to call
   - For multi-ticker: Makes PARALLEL get_stock_quote() calls (RULE #2)
   - Executes Direct API tool calls (no MCP)
   - **OHLC Fix**: Shows actual data (start, end, change, high, low, days)
   - Generates structured response

4. **Tool Execution** (Direct API)
   - Polygon Direct API: 10 tools
   - Finnhub Direct API: 1 tool (parallel calls for multi-ticker)
   - No MCP server overhead
   - Direct Python SDK calls

5. **Response Generation**
   - Agent formats response (KEY TAKEAWAYS + DETAILED ANALYSIS)
   - Backend extracts token usage from OpenAI response
   - Middleware measures response time

6. **Response Delivery**
   - Backend sends JSON response
   - Frontend/CLI displays formatted output
   - Performance metrics shown

### Performance Tracking

**Backend Middleware:**
- Measures total response time
- Adds `X-Process-Time` header
- Logs performance metrics

**Token Tracking:**
- Extracts from OpenAI response metadata
- Supports dual naming: `input_tokens`/`prompt_tokens`
- Tracks input, output, total tokens

**Frontend Display:**
- Real-time performance metrics
- Token usage display
- Response time display
- Model name display

## Testing Architecture

### CLI Regression Testing (PRIMARY)

#### New Test Suite: test_cli_regression.sh (35 tests) ⭐ CURRENT
**Created:** Oct 7, 2025 Evening
**Status:** Primary test suite

**Test Coverage:**
- **SPY Sequence** (15 tests): Market status, prices, TA indicators, options, OHLC
- **NVDA Sequence** (15 tests): Same pattern as SPY
- **Multi-Ticker WDC/AMD/INTC** (5 tests): Parallel call validation

**Features:**
- Persistent session (all 35 tests in single CLI session)
- Chat history analysis validation
- Parallel tool call verification
- OHLC display validation
- Support/Resistance redundant call detection
- Response time tracking per test
- Success rate monitoring

**Latest Performance (Oct 7, 2025 Evening):**
- **Total**: 35/35 PASSED ✅
- **Success Rate**: 100%
- **Average**: 11.62s per query (EXCELLENT)
- **Range**: 2.188s - 31.599s
- **Test 12 (Support & Resistance)**: 3.900s (vs previous 5.491s) - 29% faster ✅
- **Test 15 (SPY OHLC Q1)**: Shows actual data (start: 589.39, end: 559.39, change: -4.31%, high: 613.23, low: 549.83, 60 days) ✅
- **Test 30 (NVDA OHLC Q1)**: Shows actual data ✅
- **Test 35 (Multi OHLC Q1)**: Shows actual data for all 3 tickers ✅
- **Chat History Reuse**: Test 32 correctly used existing data (no new calls) ✅
- **Parallel Calls**: Tests 31, 33, 34 correctly made parallel calls for 3 tickers ✅
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-07_20-30.log`

**Validation Results:**
- ✅ OHLC display fix verified (shows actual data, not just "retrieved")
- ✅ Support & Resistance fix verified (no redundant calls, 29% faster)
- ✅ Chat history analysis working correctly
- ✅ Parallel tool calls executing properly (max 3 per batch)
- ✅ All 35 test responses are CORRECT (not just completed)

## Performance Architecture

### Optimizations

**Backend:**
- Async request handling (FastAPI)
- Shared HTTP session (aiohttp)
- Direct API calls (no MCP overhead)
- Minimal tool calls enforcement
- Parallel tool execution for multi-ticker (max 3 per batch)
- Chat history analysis (avoid redundant calls)

**Frontend:**
- Optimized CSS (no backdrop filters, complex shadows)
- Simple transitions (opacity, color only)
- Media queries (not container queries)
- Efficient bundle size (Vite tree shaking)

**AI Agent:**
- Streamlined system prompts (40-50% token reduction)
- GPT-5-Nano optimization (200K TPM rate limit)
- Quick response enforcement
- Parallel tool calls enabled
- Chat history analysis (RULE #9)
- OHLC display requirements (RULE #5)

### Performance Metrics

**Core Web Vitals:**
- **FCP**: 256ms (85% better than target)
- **LCP**: < 500ms (80%+ improvement)
- **CLS**: < 0.1 (50%+ improvement)
- **TTI**: < 1s (70%+ improvement)

**API Performance (Latest - Oct 7 Evening):**
- **Average Response**: 11.62s (EXCELLENT)
- **Success Rate**: 100% (35/35 tests)
- **OHLC Display**: Now shows actual data instead of "retrieved"
- **Support & Resistance**: 29% faster (no redundant calls)
- **Parallel Execution**: Working correctly for multi-ticker (max 3)

**API Performance (Oct 7 Afternoon):**
- **Average Response**: 7.31s (EXCELLENT)
- **Success Rate**: 100% (27/27 tests)

**API Performance (Post-MCP Removal):**
- **Average Response**: 6.10s (EXCELLENT)
- **Improvement**: 70% faster than legacy MCP (20s avg)

## Deployment Architecture

### Development Servers

**Backend:**
- Command: `uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload`
- Port: 8000
- Auto-reload: Enabled
- Host: 127.0.0.1 (localhost)

**Frontend:**
- Command: `vite --mode development`
- Port: 3000
- HMR: Enabled
- Proxy: API calls to localhost:8000

### Production Build

**Frontend:**
- Command: `npm run build`
- Output: `dist/` directory
- Optimization: Minification, tree shaking, code splitting
- Service Worker: PWA support

**Serving:**
- Live Server on port 5500
- SPA routing enabled
- Service worker for offline support

### Startup Scripts

**start-app-xterm.sh (RECOMMENDED):**
- Kills existing servers
- Starts backend in xterm window
- Starts frontend in xterm window
- Health checks both servers
- 30-second timeout fallback
- Notifies user when ready

**start-app.sh (NOW WORKING):**
- Same as xterm version
- Works in WSL2/headless environments
- Background process mode
- 30-second timeout fallback
- Logs to backend.log, frontend.log

## Configuration Files

### Backend
- `pyproject.toml` - Python dependencies, build config
- `.pylintrc` - Pylint configuration
- `.env` - Environment variables (API keys)

### Frontend
- `package.json` - npm dependencies, scripts
- `tsconfig.json` - TypeScript compiler config
- `.eslintrc.cjs` - ESLint configuration
- `.prettierrc.cjs` - Prettier configuration
- `vite.config.ts` - Vite build configuration
- `postcss.config.js` - PostCSS/cssnano config

### Shared
- `config/app.config.json` - Centralized non-sensitive config
- `.gitignore` - Git ignore patterns (updated for test-reports/*.log)
- `.env.example` - Environment variable template

## Security Considerations

**API Keys:**
- Stored in `.env` file (not committed to git)
- Loaded via python-dotenv
- Backend only (not exposed to frontend)

**CORS:**
- Restricted to http://127.0.0.1:3000
- Development only configuration

**Dependencies:**
- Regular updates via `uv` and `npm`
- Pinned versions in `pyproject.toml` and `package-lock.json`

## Migration & Fix History

### Oct 7, 2025 Evening: OHLC Display + Support/Resistance Fixes ✅ COMPLETE

**Problem 1: OHLC Useless Responses**
- AI said "data retrieved" without actual prices/ranges/changes
- Users got no useful information from OHLC queries

**Fix 1: RULE #5 Display Requirements**
- Added "CRITICAL DISPLAY REQUIREMENTS FOR OHLC BARS" section
- For custom date range: MUST show start open, end close, $ and % change, period high/low, trading days
- For specific date: MUST show Date, Open, High, Low, Close, Volume
- NEVER just say "data retrieved"
- Good vs bad response examples

**Problem 2: Support/Resistance Redundant Calls**
- AI called get_ta_sma/ema/rsi/macd AGAIN even when all data already existed
- Wasted time and API calls (5.491s response time)

**Fix 2: RULE #9 Scenario 5**
- Added explicit scenario for Support & Resistance
- Tells AI to use existing price, SMA/EMA data instead of making new calls
- 29% performance improvement (5.491s → 3.900s)

**New Test Suite:**
- Created test_cli_regression.sh with 35 comprehensive tests
- SPY sequence (15), NVDA sequence (15), Multi-ticker (5)
- Validates OHLC display, chat history analysis, parallel calls

**Results:**
- ✅ 35/35 tests PASSED (100% success rate)
- ✅ OHLC responses now show actual data (start, end, change, high, low, days)
- ✅ Support & Resistance 29% faster (no redundant calls)
- ✅ Chat history analysis working correctly
- ✅ All test responses verified as CORRECT (not just completed)
- ✅ Test report: test-reports/test_cli_regression_loop1_2025-10-07_20-30.log

### Oct 7, 2025 Afternoon: get_stock_quote_multi Removal ✅ COMPLETE

**Rationale:** Unnecessary wrapper function, SDK handles parallel execution natively

**Changes:**
- ✅ Removed get_stock_quote_multi (139 lines)
- ✅ Updated RULE #2 to emphasize parallel calls
- ✅ Tool count reduced from 12 to 11
- ✅ All tests pass 27/27 (100% success rate)

**New Architecture:**
- Multi-ticker queries: Agent makes parallel get_stock_quote() calls
- Example: "SPY, QQQ, IWM" → 3 parallel calls (max 3 per batch)
- Performance: 7.31s average (EXCELLENT)

### Oct 2025: MCP Removal ✅ COMPLETE

**Migration completed:**
- ✅ All 12 tools migrated to Direct API (now 11 after tool removal)
- ✅ MCP server completely removed
- ✅ Performance improved 70% (6.10s avg vs 20s legacy)
- ✅ Token tracking enhanced (dual naming support)
- ✅ Model selector removed (GPT-5-Nano only)

**Architecture Changes:**
- **Before**: FastAPI → OpenAI Agent → MCP Server → Polygon/Finnhub APIs
- **After**: FastAPI → OpenAI Agent → Direct Polygon/Finnhub Python SDKs

**Performance Gains:**
- **Response Time**: 20s → 6.10s (70% faster)
- **Overhead**: Removed MCP server latency
- **Reliability**: Direct API calls (no MCP middleman)

## Current State Summary (Oct 7, 2025 Evening)

**Architecture:**
- 11 Direct API tools (1 Finnhub + 10 Polygon)
- No MCP overhead
- Parallel execution (max 3 per batch)
- Chat history analysis
- OHLC display requirements enforced

**Performance:**
- 35/35 tests passing (100%)
- 11.62s average (EXCELLENT)
- Support & Resistance 29% faster
- OHLC responses show actual data

**Testing:**
- Primary: test_cli_regression.sh (35 tests)
- Latest report: test-reports/test_cli_regression_loop1_2025-10-07_20-30.log

**Latest Improvements:**
- ✅ OHLC display fix (show actual data)
- ✅ Support/Resistance redundant call fix
- ✅ New comprehensive test suite
- ✅ All test responses verified as CORRECT
