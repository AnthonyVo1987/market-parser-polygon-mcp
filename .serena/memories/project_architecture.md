# Project Architecture

## Overview

Market Parser is a Python CLI and React web application for natural language financial queries using Direct Polygon/Finnhub API integration and OpenAI GPT-5-Nano via the OpenAI Agents SDK v0.2.9.

**Key Architectural Change (Oct 2025):**
- **Migrated from MCP to Direct API** (Phase 4 Complete)
- **70% performance improvement** (6.10s avg vs 20s legacy)
- **All 12 tools now use Direct Python APIs** (no MCP overhead)

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
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   AI Agent Tools (12)     │
                    │   Direct API Integration  │
                    └─────────┬────────┬────────┘
                              │        │
                    ┌─────────▼──┐  ┌─▼────────┐
                    │ Polygon.io │  │ Finnhub  │
                    │ Direct API │  │ Direct   │
                    │ (11 tools) │  │ (1 tool) │
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
- `get_enhanced_agent_instructions()` - Returns optimized system prompt
- `get_optimized_model_settings()` - Returns GPT-5-Nano config
- `create_agent()` - Creates OpenAI agent with all tools

**Agent Configuration:**
- **Model**: GPT-5-Nano (EXCLUSIVE - no model selection)
- **Max Tokens**: 16384
- **Temperature**: 0.1 (deterministic)
- **Parallel Tool Calls**: Enabled
- **Rate Limits**: 200K TPM (GPT-5-Nano specific)

**System Prompt Features:**
- Streamlined instructions (no verbose disclaimers)
- Quick response enforcement
- Minimal tool calls requirement
- Structured output format (KEY TAKEAWAYS + DETAILED ANALYSIS)

### Direct API Tools (12 Total)

#### Finnhub Custom API (1 tool)
**File:** `src/backend/tools/finnhub_tools.py`

**Tools:**
1. `get_stock_quote(symbol: str)` - Real-time stock quotes
   - Uses `finnhub-python>=2.4.25`
   - Returns: current price, change, percent change, high, low, open, previous close

**Implementation:**
- `_get_finnhub_client()` - Singleton client initialization
- Environment: `FINNHUB_API_KEY`

#### Polygon Direct API (11 tools)
**File:** `src/backend/tools/polygon_tools.py`

**Market Data Tools:**
1. `get_market_status_and_date_time()` - Market status + current datetime
2. `get_stock_quote_multi(symbols: str)` - Multiple stock quotes
3. `get_options_quote_single(ticker: str)` - Single option quote

**OHLC Data Tools:**
4. `get_OHLC_bars_custom_date_range(...)` - OHLC bars for date range
5. `get_OHLC_bars_specific_date(...)` - OHLC bars for specific date
6. `get_OHLC_bars_previous_close(...)` - Previous close OHLC

**Technical Analysis Tools:**
7. `get_ta_sma(...)` - Simple Moving Average
8. `get_ta_ema(...)` - Exponential Moving Average
9. `get_ta_rsi(...)` - Relative Strength Index
10. `get_ta_macd(...)` - MACD

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
   - Creates OpenAI agent with 12 tools
   - Passes query to agent

3. **AI Agent Processing** (OpenAI Agents SDK)
   - Analyzes query
   - Determines which tools to call
   - Executes Direct API tool calls (no MCP)
   - Generates structured response

4. **Tool Execution** (Direct API)
   - Polygon Direct API: 11 tools
   - Finnhub Direct API: 1 tool
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

## Migration History

### Phase 4: MCP Removal (Oct 2025) ✅ COMPLETE

**Migration completed:**
- ✅ All 12 tools migrated to Direct API
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
- **Consistency**: 0.80s std dev (highly reliable)

## Testing Architecture

### CLI Regression Testing

**Script:** `CLI_test_regression.sh`
- 27 standardized test prompts
- Single persistent CLI session
- Response time tracking
- Success rate monitoring

**Test Coverage:**
- Market data queries (7 tests)
- Technical analysis (15 tests)
- OHLC/options data (5 tests)

**Performance Baseline (10-Run, Oct 2025):**
- **Average**: 6.10s per query
- **Range**: 5.25s - 7.57s
- **Std Dev**: 0.80s
- **Success Rate**: 100% (160/160 tests)

**Test Reports:**
- Saved to `test-reports/` directory
- Timestamped filenames
- Includes performance metrics

### E2E Testing (Playwright)

**Status:** Available but not primary test method
**Location:** `tests/playwright/`
**Note:** CLI regression tests are primary testing method

## Performance Architecture

### Optimizations

**Backend:**
- Async request handling (FastAPI)
- Shared HTTP session (aiohttp)
- Direct API calls (no MCP overhead)
- Minimal tool calls enforcement

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

### Performance Metrics

**Core Web Vitals:**
- **FCP**: 256ms (85% better than target)
- **LCP**: < 500ms (80%+ improvement)
- **CLS**: < 0.1 (50%+ improvement)
- **TTI**: < 1s (70%+ improvement)

**API Performance:**
- **Average Response**: 6.10s (EXCELLENT)
- **Success Rate**: 100%
- **Consistency**: 0.80s std dev

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
- `.gitignore` - Git ignore patterns
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

## Legacy Feature Cleanup (Oct 2025)

**Context:** Comprehensive cleanup of 4 deprecated legacy features to improve performance, maintainability, and documentation accuracy.

### Removed Features

#### 1. CSS Performance Analysis
- **Component**: Frontend performance monitoring
- **File**: `src/frontend/utils/performance.tsx`
- **Function**: `analyzeCSSPerformance()` (lines 78-186)
- **Impact**: HIGH CPU overhead (1-2% continuous)
- **Issue**: Scanned entire DOM 6 times every 2 seconds using `querySelectorAll('*')`
- **References Removed**:
  - Constructor call: `this.analyzeCSSPerformance()`
  - Private method: `analyzeCSSPerformance(): void`
  - startMonitoring() call
  - getMetrics() call
  - cssMetrics field reference
- **Result**: 1-2% CPU reduction, cleaner performance monitoring

#### 2. /api/v1/system/status Endpoint
- **Component**: Backend API endpoint
- **Files Deleted**:
  - `src/backend/routers/system.py` (entire 26-line file)
- **Files Modified**:
  - `src/backend/api_models.py` - Removed SystemMetrics, SystemStatusResponse classes
  - `src/backend/main.py` - Removed system_router import and registration
  - `src/backend/routers/__init__.py` - Removed system_router export
- **Usage**: Zero (no frontend, tests, or docs referenced it)
- **Result**: Simplified API surface, removed dead code

#### 3. Prompt Template System Remnants
- **Component**: Legacy documentation and schema remnants
- **Status**: System was previously removed, only references remained
- **Files Modified**:
  - `src/backend/api_models.py`:
    - Removed docstring reference to "PromptTemplateManager functionality"
    - Removed SystemMetrics.prompt_templates_loaded field (always set to 0)
  - `CLAUDE.md`, `AGENTS.md`, `README.md`:
    - Removed "prompt_templates.py # Analysis templates" from project structure
- **Files Deleted**:
  - `docs/api/api-integration-guide.md` (957 lines of outdated PromptTemplate docs)
- **Reason**: Direct Prompts architecture replaced PromptTemplate system months ago
- **Result**: Documentation now accurate, no misleading references

#### 4. Emoji in CLI Responses
- **Component**: CLI output formatting
- **File**: `src/backend/utils/response_utils.py`
- **Function**: `print_response()` (lines 9-65)
- **Emojis Removed**:
  - ✅ Success indicator (line 11)
  - 📊 Performance Metrics header (line 30)
  - ⏱️ Response Time (line 34)
  - 🔢 Tokens Used (line 53)
  - 🤖 Model info (lines 60, 62)
- **Comments Updated**:
  - "with emoji support" → "for CLI output"
  - "better emoji support" → removed
  - "Enhanced separator with emoji" → "Separator"
- **Scope**: CLI only (no web API impact)
- **Result**: Cleaner terminal output, simpler code

### Cleanup Statistics

**Code Changes:**
- **Files Deleted**: 2 (system.py, api-integration-guide.md)
- **Files Modified**: 10
  - Backend: api_models.py, main.py, routers/__init__.py, response_utils.py
  - Frontend: performance.tsx
  - Docs: CLAUDE.md, AGENTS.md, README.md
- **Lines Removed**: ~1,100+ lines
- **Classes Removed**: 2 (SystemMetrics, SystemStatusResponse)
- **Functions Removed**: 1 (analyzeCSSPerformance)
- **Emojis Removed**: 5 types

**Test Results (Post-Cleanup):**
- **CLI Tests**: 27/27 PASSED ✅
- **Success Rate**: 100%
- **Average Response Time**: 7.95s (EXCELLENT)
- **Performance Range**: 3.004s - 24.614s
- **Session Mode**: PERSISTENT (all tests in single session)
- **Test Report**: `cli_regression_test_loop1_20251006_211035.txt`

**Performance Impact:**
- **CPU Usage**: Reduced by 1-2% (CSS analysis removal)
- **Code Quality**: Improved maintainability
- **Documentation**: Now accurate and up-to-date
- **API Surface**: Cleaner (unused endpoint removed)

### Architecture Changes

**Before Cleanup:**
```
Frontend: React + analyzeCSSPerformance (HIGH overhead)
Backend: FastAPI + /system/status endpoint + SystemMetrics schema
CLI: Rich formatting with emojis
Docs: 957 lines of outdated PromptTemplate documentation
```

**After Cleanup:**
```
Frontend: React with PerformanceObserver only (LOW overhead)
Backend: FastAPI with essential endpoints only
CLI: Clean Rich formatting without emojis
Docs: Accurate and current
```

**Benefits:**
- ✅ Reduced CPU overhead
- ✅ Simpler codebase
- ✅ Accurate documentation
- ✅ Fewer API endpoints to maintain
- ✅ Cleaner CLI output
- ✅ No performance regressions (100% test pass rate)

### Maintenance Impact

**Future Development:**
- Simpler codebase to understand
- No confusion from obsolete PromptTemplate docs
- Clear API surface (only essential endpoints)
- Performance monitoring focused on PerformanceObserver API (standard)
- CLI output consistent and professional

**Documentation:**
- All project structure diagrams updated
- No misleading references to removed features
- Clear separation of concerns
- Easy onboarding for new developers
