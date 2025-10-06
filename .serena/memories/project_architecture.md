# Project Architecture

## High-Level Overview

**Market Parser** is a full-stack financial analysis application with:
- **Backend**: Python FastAPI REST API with OpenAI Agents SDK integration
- **Frontend**: React TypeScript SPA with real-time chat interface  
- **Integration**: Direct Polygon API (11 tools) + Finnhub API (1 tool)
- **AI Model**: OpenAI GPT-5-Nano (EXCLUSIVE - no model selection, no GPT-5-Mini)
- **Total AI Agent Tools**: 12 (1 Finnhub + 11 Polygon Direct API)

## Directory Structure

```
market-parser-polygon-mcp/
├── src/
│   ├── backend/              # Python FastAPI backend
│   │   ├── routers/          # API endpoint routers
│   │   │   ├── chat.py       # Chat endpoint
│   │   │   ├── health.py     # Health check
│   │   │   └── system.py     # System info
│   │   ├── services/         # Business logic services
│   │   │   └── agent_service.py  # AI agent creation
│   │   ├── tools/            # Custom AI agent tools (12 total)
│   │   │   ├── finnhub_tools.py  # Finnhub API (1 tool)
│   │   │   └── polygon_tools.py  # Polygon Direct API (11 tools)
│   │   ├── utils/            # Utility modules
│   │   │   └── token_utils.py    # Token tracking (input/output/total)
│   │   ├── main.py           # FastAPI application entry
│   │   ├── cli.py            # CLI interface
│   │   ├── config.py         # Configuration management
│   │   ├── api_models.py     # Pydantic API schemas (NO model selection)
│   │   └── dependencies.py   # FastAPI dependencies
│   └── frontend/             # React TypeScript frontend
│       ├── components/       # React components
│       │   ├── ChatInterface_OpenAI.tsx  # Main chat UI
│       │   ├── ChatMessage_OpenAI.tsx    # Message display (Input/Output/Total tokens)
│       │   └── ...
│       ├── services/         # API service layer
│       │   └── api_OpenAI.ts  # API client (NO model selection)
│       ├── types/            # TypeScript type definitions
│       │   └── chat_OpenAI.ts  # Chat types (input/output tokens)
│       ├── utils/            # Utility functions
│       │   └── performance.tsx  # Performance monitoring (FCP/LCP/CLS)
│       ├── config/           # Configuration loader
│       ├── App.tsx           # Root component
│       └── main.tsx          # Application entry point
├── tests/
│   ├── playwright/           # E2E tests (Playwright)
│   └── test_*.py             # Python unit tests
├── config/                   # Centralized configuration
│   └── app.config.json       # Non-sensitive settings
├── docs/                     # Documentation
├── test-reports/             # Test output files
├── public/                   # Static assets
├── dist/                     # Production build output
├── .serena/                  # Serena AI assistant
│   ├── memories/             # Project knowledge base
│   └── cache/                # Symbol caching
├── pyproject.toml            # Python project config
├── package.json              # Node.js project config
├── CLAUDE.md                 # Claude Code instructions
├── AGENTS.md                 # AI agent documentation
└── start-app*.sh             # One-click startup scripts
```

## Backend Architecture (Python FastAPI)

### Core Components

#### 1. main.py - Application Entry Point
**Responsibilities:**
- FastAPI app initialization
- CORS middleware setup
- Router registration (chat, health, system ONLY - NO models router)
- Lifespan management (database session)
- Request timing middleware

**Key Changes (Oct 2025):**
- ❌ Removed MCP server initialization
- ❌ Removed models router registration
- ✅ Simplified lifespan to session-only management

#### 2. services/agent_service.py - Agent Creation & Management
**Symbols:**
- `create_agent()`: Creates AI agent with 12 custom tools (NO MCP server parameter)
- `get_enhanced_agent_instructions()`: Returns agent prompt template (12 tools)
- `get_optimized_model_settings()`: Returns GPT-5-Nano configuration

**Responsibilities:**
- Agent instantiation with OpenAI Agents SDK
- System prompt configuration (12 tools documented)
- Model settings (GPT-5-Nano ONLY - no model selection)
- Custom tool integration (1 Finnhub + 11 Polygon Direct API)

**Tool Integration:**
```python
from ..tools.finnhub_tools import get_stock_quote
from ..tools.polygon_tools import (
    get_market_status_and_date_time,
    get_stock_quote_multi,
    get_options_quote_single,
    get_OHLC_bars_custom_date_range,
    get_OHLC_bars_specific_date,
    get_OHLC_bars_previous_close,
    get_ta_sma,
    get_ta_ema,
    get_ta_rsi,
    get_ta_macd
)

tools=[
    get_stock_quote,  # Finnhub
    get_market_status_and_date_time,  # Polygon
    get_stock_quote_multi,
    get_options_quote_single,
    get_OHLC_bars_custom_date_range,
    get_OHLC_bars_specific_date,
    get_OHLC_bars_previous_close,
    get_ta_sma,
    get_ta_ema,
    get_ta_rsi,
    get_ta_macd
]
```

#### 3. tools/ - Custom AI Agent Tools (12 Total)

**finnhub_tools.py (1 tool):**
- `get_stock_quote(ticker: str)`: Single ticker real-time quotes

**polygon_tools.py (11 tools):**
1. `get_market_status_and_date_time()`: Market status + datetime
2. `get_stock_quote_multi(tickers, market_type)`: Multi-ticker quotes
3. `get_options_quote_single(underlying_asset, option_contract)`: Options with Greeks
4. `get_OHLC_bars_custom_date_range(ticker, from_date, to_date, ...)`: Date range OHLC
5. `get_OHLC_bars_specific_date(ticker, date, ...)`: Specific date OHLC
6. `get_OHLC_bars_previous_close(ticker, ...)`: Previous trading day
7. `get_ta_sma(ticker, window, ...)`: Simple Moving Average
8. `get_ta_ema(ticker, window, ...)`: Exponential Moving Average
9. `get_ta_rsi(ticker, window, ...)`: Relative Strength Index
10. `get_ta_macd(ticker, ...)`: MACD Indicator
11. (Future expansion as needed)

**Pattern:**
- `@function_tool` decorator from OpenAI Agents SDK
- Async functions
- JSON string returns
- Comprehensive error handling
- Direct Polygon Python Library calls (polygon-api-client v1.15.4)
- 10.00/10 Pylint score standard

#### 4. utils/token_utils.py - Token Tracking

**Functions:**
- `extract_token_usage_from_context_wrapper()`: Returns dict with total_tokens, input_tokens, output_tokens
- `extract_token_count_from_context_wrapper()`: Deprecated, kept for compatibility

**Features:**
- Dual naming convention support (input_tokens/prompt_tokens, output_tokens/completion_tokens)
- Extracts from OpenAI Agents SDK `context_wrapper.usage` object
- Used by chat router to populate ResponseMetadata

#### 5. api_models.py - API Schemas

**Key Models:**
- `ResponseMetadata`: Contains model, timestamp, processingTime, requestId, tokenCount (deprecated), inputTokens, outputTokens
- `ChatRequest`, `ChatResponse`: Chat endpoint models

**Removed (Oct 2025):**
- ❌ CustomModel, AIModelId, AIModel
- ❌ ModelListResponse, ModelSelectionRequest, ModelSelectionResponse
- ❌ All model selection infrastructure

#### 6. routers/ - API Endpoints

**Active Routers:**
- `chat.py`: Chat endpoint for AI interactions (uses token_utils for input/output tracking)
- `health.py`: Health check endpoint
- `system.py`: System information endpoints

**Removed (Oct 2025):**
- ❌ `models.py`: Model selection endpoints (deleted)

### Backend Data Flow

```
User Request
    ↓
FastAPI Router (chat.py)
    ↓
Agent Service (create_agent)
    ↓
OpenAI Agents SDK → GPT-5-Nano (ONLY)
    ↓
Custom Tools (12 tools - ALL Direct API)
├── Finnhub (1): get_stock_quote
└── Polygon Direct API (11): market status, quotes, OHLC, TA indicators
    ↓
Agent Response Processing
    ↓
Token Extraction (input/output/total from context_wrapper.usage)
    ↓
JSON Response to Frontend (with inputTokens, outputTokens, tokenCount)
```

### AI Agent Tool Architecture (12 Total Tools)

**Tool Distribution:**
1. **Finnhub Custom (1 tool)**:
   - get_stock_quote

2. **Polygon Direct API Custom (11 tools)**:
   - get_market_status_and_date_time
   - get_stock_quote_multi
   - get_options_quote_single
   - get_OHLC_bars_custom_date_range
   - get_OHLC_bars_specific_date
   - get_OHLC_bars_previous_close
   - get_ta_sma
   - get_ta_ema
   - get_ta_rsi
   - get_ta_macd
   - (1 slot reserved for future expansion)

**Migration Complete (Oct 2025):**
- ✅ Phase 1-4 Complete: ALL MCP tools migrated to Direct API
- ✅ MCP server completely removed
- ✅ All 6 legacy MCP tools replaced with 5 direct API equivalents
- ✅ Added 4 TA indicator tools
- ✅ Benefits realized: 70% faster performance, simpler architecture

### Backend Dependencies

**Core:**
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `openai-agents==0.2.9`: OpenAI Agents SDK
- `openai>=1.99.0,<1.100.0`: OpenAI API client
- `pydantic`: Data validation
- `python-dotenv`: Environment variables

**Financial Data APIs:**
- `finnhub-python==2.4.25`: Finnhub API client
- `polygon-api-client==1.15.4`: Polygon.io API client

**Development:**
- `pylint`, `black`, `isort`: Code quality (10.00/10 score)
- `pytest`: Testing

**Removed (Oct 2025):**
- ❌ `openai-agents-mcp`: No longer needed (MCP removed)

## Frontend Architecture (React TypeScript)

### Core Components

#### 1. ChatInterface_OpenAI.tsx - Main Chat Container
**Responsibilities:**
- Chat state management (messages, loading, error)
- Send message to backend (NO model parameter)
- Display conversation history
- System status & performance panel (consolidated)

**Key Changes (Oct 2025):**
- ❌ Removed model selection UI
- ❌ Removed currentModel state
- ❌ Removed useAIModel hook
- ✅ Simplified to GPT-5-Nano only

#### 2. ChatMessage_OpenAI.tsx - Message Display
**Responsibilities:**
- Render individual messages
- Display metadata (model, processing time, tokens)
- Token display format: "Input: X | Output: Y | Total: Z"

**Token Display Logic:**
```typescript
{(message.metadata.inputTokens !== undefined && message.metadata.outputTokens !== undefined) ? (
    <span>
        Input: {inputTokens} | Output: {outputTokens} | Total: {total}
    </span>
) : message.metadata.tokenCount ? (
    <span>Tokens: {tokenCount}</span>
) : null}
```

#### 3. services/api_OpenAI.ts - API Client
**Functions:**
- `sendChatMessage(message: string)`: Send message to chat endpoint (NO model parameter)

**Removed (Oct 2025):**
- ❌ `fetchModels()`: Model list endpoint removed
- ❌ `selectModel()`: Model selection endpoint removed
- ❌ Model parameter from sendChatMessage

#### 4. types/chat_OpenAI.ts - Type Definitions
**Interfaces:**
- `MessageMetadata`: Contains tokenCount (deprecated), inputTokens, outputTokens, model, processingTime, etc.
- `ResponseMetadata`: Same fields as MessageMetadata

**Removed (Oct 2025):**
- ❌ `ai_models.ts`: Entire file deleted (AIModelId, ModelListResponse, etc.)

#### 5. utils/performance.tsx - Performance Monitoring
**Functionality:**
- Tracks FCP, LCP, CLS Web Vitals
- usePerformanceMonitoring hook

**Fix (Oct 2025):**
- Changed metrics initialization from `0` to `undefined`
- Prevents "Calculating..." from showing actual 0 values
- Proper conditional rendering in UI

### Frontend Data Flow

```
User Input (ChatInterface_OpenAI)
    ↓
API Service Layer (api_OpenAI.ts)
    ↓
HTTP POST to /api/v1/chat/
    ↓
Backend Processing (12 tools available, GPT-5-Nano only)
    ↓
JSON Response (with inputTokens, outputTokens, tokenCount)
    ↓
State Update (React useState)
    ↓
UI Re-render (ChatMessage_OpenAI with token breakdown)
```

### Frontend Dependencies

**Core:**
- `react@18.2.0`: UI library
- `react-dom@18.2.0`: React DOM renderer
- `react-markdown@9.0.0`: Markdown rendering
- `use-debounce@10.0.6`: Input debouncing

**Development:**
- `vite@5.2.13`: Build tool
- `typescript@5.5.3`: Type system
- `eslint`, `prettier`: Code quality

## Integration Points

### 1. Backend ↔ Frontend Communication
- **Protocol**: HTTP REST API
- **Format**: JSON
- **Endpoints**:
  - `POST /api/v1/chat/`: Send message, receive AI response (12 tools, GPT-5-Nano only, input/output tokens)
  - `GET /health`: Health check
  - `GET /api/system/info`: System information

**Removed (Oct 2025):**
- ❌ `GET /api/v1/models`: Model list endpoint
- ❌ `POST /api/v1/models/select`: Model selection endpoint

### 2. Backend ↔ Polygon.io
- **Protocol**: HTTP REST API via polygon-api-client
- **Tools**: 11 tools (all Direct API, no MCP)
- **Library**: polygon-api-client v1.15.4
- **Advantages**: Direct control, 70% faster, simpler architecture

### 3. Backend ↔ Finnhub API
- **Protocol**: HTTP REST API via finnhub-python
- **Tool**: get_stock_quote
- **Library**: finnhub-python v2.4.25

### 4. Backend ↔ OpenAI API
- **Model**: GPT-5-Nano (EXCLUSIVE)
- **SDK**: OpenAI Agents SDK v0.2.9
- **Authentication**: API key via environment variable
- **Features**: Agent-based interactions with tool calling (12 tools), token usage tracking

## Configuration Management

### Environment Variables (.env)
```
POLYGON_API_KEY=xxx     # Direct API only (MCP removed)
OPENAI_API_KEY=xxx      # OpenAI GPT-5-Nano access
FINNHUB_API_KEY=xxx     # Finnhub API access
DEFAULT_MODEL=gpt-5-nano  # ONLY allowed value
```

### Port Configuration
- **Backend**: 127.0.0.1:8000 (fixed)
- **Frontend Dev**: 127.0.0.1:3000 (fixed)
- **Frontend Prod**: 127.0.0.1:5500 (Live Server)

## Deployment Architecture

### One-Click Startup
```
./start-app-xterm.sh or ./start-app.sh
  ↓
Kill existing servers
  ↓
Start Backend (port 8000, GPT-5-Nano only, 12 tools)
  ↓
Start Frontend (port 3000)
  ↓
Health checks (10 retries, 2s intervals)
  ↓
User navigates to http://127.0.0.1:3000
```

## Performance Metrics

### Latest Test Results (Oct 5, 2025)

**27-Test Suite (Post Infrastructure Cleanup):**
- **Total Tests**: 27/27 PASSED ✅
- **Success Rate**: 100%
- **Average Response Time**: 7.34s ⭐ EXCELLENT
- **Response Time Range**: 4.11s - 17.14s
- **Test Report**: `cli_regression_test_loop1_20251005_181607.txt`

**Changes Validated:**
1. ✅ AI Model Selector removed (backend + frontend)
2. ✅ Token display showing Input/Output/Total separately
3. ✅ Performance indicators (FCP, LCP, CLS) displaying correctly

**Performance Improvement:**
- **Legacy (with MCP)**: ~20s average
- **Current (Direct API, no model selection)**: 7.34s average
- **🚀 Improvement**: 63% faster

### UI Performance
- **FCP**: ~256ms
- **LCP**: <1s
- **CLS**: <0.1
- **Memory Heap**: ~13.8MB

## Security Architecture

### API Key Management
- Stored in `.env` (never committed)
- Three API keys required:
  - OPENAI_API_KEY (GPT-5-Nano only)
  - POLYGON_API_KEY (Direct API)
  - FINNHUB_API_KEY (stock quotes)

### Removed Attack Surfaces (Oct 2025)
- ❌ Model selection endpoints (potential abuse vector removed)
- ❌ MCP server connections (reduced complexity)
- ✅ Simplified to single model, direct API calls only

## Testing Strategy

### Backend Testing
- Comprehensive CLI test suite (27 tests in single persistent session)
- **Latest Results (Oct 5, 2025)**: 27/27 PASSED, 7.34s avg, EXCELLENT performance
- Validates all 12 tools work correctly
- No MCP dependencies to test

### Frontend Testing
- E2E tests with Playwright
- Component testing
- Token display validation (input/output/total)
- Performance metrics validation

## Key Architectural Decisions (Oct 2025)

### 1. Complete MCP Removal
**Rationale:**
- Direct API calls are 70% faster
- Simpler architecture, fewer dependencies
- Full control over API interactions
- No MCP server lifecycle management

**Impact:**
- Removed mcp_service.py
- Removed MCP dependency injection
- Removed MCP server from lifespan management
- All 12 tools now use Direct API pattern

### 2. Model Selection Removal
**Rationale:**
- Only GPT-5-Nano is used (no other models)
- Model selection infrastructure was dead code
- Simplified API and UI
- Reduced attack surface

**Impact:**
- Removed models.py router
- Removed 6 model selection classes from api_models.py
- Removed ai_models.ts from frontend
- Removed model selection UI components
- Simplified sendChatMessage API

### 3. Token Tracking Enhancement
**Rationale:**
- Users need visibility into token usage
- Input vs output tokens have different costs
- Transparency builds trust

**Impact:**
- Added extract_token_usage_from_context_wrapper
- Updated ResponseMetadata with inputTokens/outputTokens
- Updated UI to show "Input: X | Output: Y | Total: Z"
- Backward compatible with tokenCount fallback

### 4. Performance Monitoring
**Rationale:**
- Need to track UI performance metrics
- Core Web Vitals matter for UX

**Fix:**
- Changed initialization from 0 to undefined
- Proper "Calculating..." display
- Accurate measurement of FCP, LCP, CLS

## Git Workflow

**Reference**: See `.serena/memories/git_commit_workflow.md` for complete workflow

**Key Principle**: Stage ONLY immediately before commit
- ❌ NEVER stage files early during development
- ✅ DO ALL WORK FIRST (code, tests, docs, config)
- ✅ STAGE EVERYTHING AT ONCE (`git add -A`)
- ✅ COMMIT IMMEDIATELY (within 60 seconds)

## Scalability Considerations

### Current Architecture (Optimized)
- Single-process backend (uvicorn)
- 12 custom tools (all Direct API, no MCP overhead)
- GPT-5-Nano only (no model switching overhead)
- Suitable for development and small-scale production

### Future Scaling Options
- Multi-worker uvicorn deployment
- State externalization (Redis for sessions)
- Load balancing for frontend
- CDN for static assets
- Rate limiting per API key

## Migration History

### Infrastructure Cleanup (Oct 5, 2025)

**Phase 4 Complete: MCP Removal**
- Tool Evolution: 10 → 14 → 18 → 12 (CURRENT)
- Removed 6 MCP tools, added 5 direct API equivalents + 4 TA indicators
- Performance improvement: 70% faster (removed MCP overhead)

**Model Selector Removal**
- Removed models.py router
- Removed 6 model selection classes
- Removed ai_models.ts frontend types
- Simplified to GPT-5-Nano only

**Token Display Enhancement**
- Split tokenCount into inputTokens + outputTokens
- Dual naming convention support
- UI shows breakdown: "Input: X | Output: Y | Total: Z"

**Performance Indicators Fix**
- Fixed FCP/LCP/CLS stuck on "Calculating..."
- Changed initialization: 0 → undefined
