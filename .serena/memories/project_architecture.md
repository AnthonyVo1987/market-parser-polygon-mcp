# Project Architecture

## High-Level Overview

**Market Parser** is a full-stack financial analysis application with:
- **Backend**: Python FastAPI REST API with OpenAI Agents SDK integration
- **Frontend**: React TypeScript SPA with real-time chat interface
- **Integration**: Polygon.io MCP server (7 tools) + Direct Polygon API (1 tool) + Finnhub API (1 tool)
- **AI Model**: OpenAI GPT-5-Nano (exclusive, GPT-5-Mini removed)
- **Total AI Agent Tools**: 10 (1 Finnhub + 1 Polygon Direct + 7 Polygon MCP + 1 removed MCP)

## Directory Structure

```
market-parser-polygon-mcp/
├── src/
│   ├── backend/              # Python FastAPI backend
│   │   ├── routers/          # API endpoint routers
│   │   ├── services/         # Business logic services
│   │   ├── tools/            # Custom AI agent tools ⭐ NEW
│   │   │   ├── finnhub_tools.py     # Finnhub API custom tools
│   │   │   └── polygon_tools.py     # Polygon Direct API tools ⭐ NEW
│   │   ├── utils/            # Utility modules
│   │   ├── main.py           # FastAPI application entry
│   │   ├── cli.py            # CLI interface
│   │   ├── config.py         # Configuration management
│   │   ├── api_models.py     # Pydantic API schemas
│   │   └── dependencies.py   # FastAPI dependencies
│   └── frontend/             # React TypeScript frontend
│       ├── components/       # React components
│       ├── services/         # API service layer
│       ├── types/            # TypeScript type definitions
│       ├── utils/            # Utility functions
│       ├── config/           # Configuration loader
│       ├── styles/           # CSS styles
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
├── .venv/                    # Python virtual environment
├── node_modules/             # Node.js dependencies
├── pyproject.toml            # Python project config
├── package.json              # Node.js project config
├── vite.config.ts            # Vite bundler config
├── tsconfig.json             # TypeScript config
├── .eslintrc.cjs             # ESLint config
├── .pylintrc                 # Pylint config
└── start-app*.sh             # One-click startup scripts
```

## Backend Architecture (Python FastAPI)

### Core Components

#### 1. main.py - Application Entry Point
**Symbols:**
- `app`: FastAPI application instance
- `lifespan()`: Async context manager for startup/shutdown
- `shared_mcp_server`: Global MCP server instance
- `shared_session`: Global SQLite session for agents
- `add_process_time_header()`: Middleware for timing
- `cors_origins`: CORS configuration

**Responsibilities:**
- FastAPI app initialization
- CORS middleware setup
- Router registration
- Lifespan management (MCP server, database session)
- Request timing middleware

#### 2. services/agent_service.py - Agent Creation & Management
**Symbols:**
- `create_agent()`: Creates AI agent with custom tools + MCP tools
- `get_enhanced_agent_instructions()`: Returns agent prompt template (10 tools)
- `get_optimized_model_settings()`: Returns GPT-5-Nano configuration

**Responsibilities:**
- Agent instantiation with OpenAI Agents SDK
- System prompt configuration
- Model settings (GPT-5-Nano only)
- Custom tool integration (Finnhub + Polygon direct)
- MCP tool integration (Polygon MCP server)

**Custom Tools Integration:**
```python
from ..tools.finnhub_tools import get_stock_quote
from ..tools.polygon_tools import get_market_status_and_date_time

tools=[get_stock_quote, get_market_status_and_date_time]
```

#### 3. tools/ - Custom AI Agent Tools ⭐ NEW DIRECTORY
**Structure:**
- `finnhub_tools.py`: Finnhub API custom tools (Oct 2025)
  - `get_stock_quote()`: Single ticker real-time quotes
- `polygon_tools.py`: Polygon Direct API tools (Oct 2025) ⭐ NEW FILE
  - `get_market_status_and_date_time()`: Market status + datetime ⭐ NEW TOOL

**Pattern:**
- `@function_tool` decorator from OpenAI Agents SDK
- Async functions
- JSON string returns
- Comprehensive error handling
- Lazy client initialization with helper functions
- 10.00/10 Pylint score standard

**Custom Tool Details:**

**finnhub_tools.py:**
- Tool: `get_stock_quote(ticker: str) -> str`
- Purpose: Real-time stock quotes for single tickers
- API: Finnhub Python Library v2.4.25
- Returns: JSON with current_price, change, percent_change, high, low, open, previous_close
- Error Handling: JSON error responses (no exceptions to agent)

**polygon_tools.py:** ⭐ NEW
- Tool: `get_market_status_and_date_time() -> str`
- Purpose: Market status + server datetime in single call
- API: Polygon Python Library (polygon-api-client v1.15.4)
- Returns: JSON with market_status, after_hours, early_hours, exchanges (nasdaq/nyse/otc), server_time, date, time
- Error Handling: JSON error responses (no exceptions to agent)
- Migration: Replaces MCP get_market_status tool

#### 4. services/mcp_service.py - MCP Server Integration
**Responsibilities:**
- Polygon.io MCP server connection (7 remaining tools)
- MCP tool availability management
- Session lifecycle management

#### 5. routers/ - API Endpoints
**Structure:**
- `chat.py`: Chat endpoint for AI interactions
- `health.py`: Health check endpoint
- `system.py`: System information endpoints
- `models.py`: Available models endpoint

**Key Patterns:**
- Each router uses `APIRouter()`
- Pydantic models for request/response validation
- Async endpoint handlers
- Dependency injection for shared resources

#### 6. utils/ - Utility Modules
**Modules:**
- `response_utils.py`: API response formatting
- `datetime_utils.py`: Date/time handling
- `token_utils.py`: Token counting/management

### Backend Data Flow

```
User Request
    ↓
FastAPI Router (chat.py)
    ↓
Agent Service (create_agent)
    ↓
OpenAI Agents SDK → GPT-5-Nano
    ↓
┌─── Custom Tools (2 tools) ───┐
│   - Finnhub API (get_stock_quote)
│   - Polygon Direct API (get_market_status_and_date_time) ⭐ NEW
└─── MCP Server (7 tools) ─────┘
    - Polygon.io MCP (get_snapshot_all, get_snapshot_option, get_aggs, etc.)
    ↓
Agent Response Processing
    ↓
JSON Response to Frontend
```

### AI Agent Tool Architecture (10 Total Tools)

**Tool Distribution:**
1. **Finnhub Custom (1 tool)**:
   - get_stock_quote

2. **Polygon Direct API Custom (1 tool)**: ⭐ NEW
   - get_market_status_and_date_time

3. **Polygon MCP Server (7 tools)**:
   - get_snapshot_all
   - get_snapshot_option
   - get_aggs
   - list_aggs
   - get_daily_open_close_agg
   - get_previous_close_agg

4. **Removed MCP Tools (1 tool)**:
   - ~~get_market_status~~ (replaced by get_market_status_and_date_time direct API)

**Migration Strategy:**
- **Phase 1 Complete**: get_market_status migrated from MCP to direct API
- **Proof of Concept**: Validated direct API pattern with polygon_tools.py
- **Future Phases**: Gradual migration of remaining MCP tools to direct API
- **Benefits**: Improved performance, simpler architecture, full control

### Backend Dependencies

**Core:**
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `openai-agents==0.2.9`: OpenAI Agents SDK
- `openai>=1.99.0,<1.100.0`: OpenAI API client
- `pydantic`: Data validation
- `python-dotenv`: Environment variables
- `aiofiles`: Async file I/O

**Financial Data APIs:**
- `finnhub-python==2.4.25`: Finnhub API client
- `polygon-api-client==1.15.4`: Polygon.io API client ⭐ NEW

**Development:**
- `pylint`, `black`, `isort`: Code quality
- `mypy`: Type checking
- `pytest`: Testing

## Frontend Architecture (React TypeScript)

### Core Components

#### 1. App.tsx - Root Component
**Responsibilities:**
- Application shell
- Global state management
- Error boundary
- Routing (if applicable)

#### 2. components/ - UI Components

**Key Components:**
- `ChatInterface_OpenAI.tsx`: Main chat container with consolidated status panel
- `ChatInput_OpenAI.tsx`: Message input with submit
- `ChatMessage_OpenAI.tsx`: Individual message display
- `LoadingSpinner.tsx`: Loading state indicator
- `ErrorBoundary.tsx`: Error handling wrapper
- `PerformanceToggle.tsx`: Performance monitoring toggle
- `MessageCopyButton.tsx`: Copy individual message content (inline clipboard utilities)
- `CollapsiblePanel.tsx`: Collapsible UI sections

**REMOVED Components (Oct 2025):**
- ~~`ExportButtons.tsx`~~ - Export functionality removed
- ~~`RecentMessageButtons.tsx`~~ - Recent message shortcuts removed
- ~~`DebugPanel.tsx`~~ - Debug panel removed

**CONSOLIDATED:**
- Status Information Panel + Performance Metrics Panel → **"System Status & Performance"** panel
  - Shows: Message count, loading status, FCP, LCP, CLS metrics
  - Single CollapsiblePanel for cleaner UI

**Naming Convention:**
- Suffix `_OpenAI` indicates OpenAI-specific implementation
- PascalCase for component names
- One component per file

#### 3. services/ - API Layer
**Responsibilities:**
- HTTP client configuration
- API endpoint calls
- Response parsing
- Error handling

#### 4. types/ - TypeScript Definitions
**Responsibilities:**
- Interface definitions for props
- Type definitions for API responses
- Shared type definitions across components

#### 5. config/ - Configuration
**Responsibilities:**
- Environment-specific configuration loading
- API endpoint configuration
- Feature flags

#### 6. utils/ - Utility Functions

**Removed:**
- ~~`exportHelpers.ts`~~ - Export utilities removed (Oct 2025)

**Retained:**
- `performance.tsx`: Performance monitoring and metrics
- `accessibility.ts`: Accessibility utilities
- `willChangeManager.ts`: CSS will-change optimization
- `touchGestures.ts`: Touch gesture handling
- `messageFormatting.ts`: Message display formatting
- `placeholderText.ts`: Placeholder text utilities

**Note:** MessageCopyButton.tsx now contains inline clipboard utilities (copyToClipboard, convertSingleMessageToMarkdown) extracted from removed exportHelpers.

### Frontend Data Flow

```
User Input (ChatInput_OpenAI)
    ↓
API Service Layer
    ↓
HTTP POST to /api/chat
    ↓
Backend Processing (10 tools available)
    ↓
JSON Response
    ↓
State Update (React useState)
    ↓
UI Re-render (ChatMessage_OpenAI)
```

### Frontend Dependencies

**Core:**
- `react@18.2.0`: UI library
- `react-dom@18.2.0`: React DOM renderer
- `react-markdown@9.0.0`: Markdown rendering
- `use-debounce@10.0.6`: Input debouncing

**Development:**
- `vite@5.2.0`: Build tool
- `typescript@5.2.2`: Type system
- `@vitejs/plugin-react@4.2.1`: Vite React plugin
- `eslint`: Linting
- `prettier`: Code formatting

**Testing:**
- `@playwright/test@1.55.0`: E2E testing

## Integration Points

### 1. Backend ↔ Frontend Communication
- **Protocol**: HTTP REST API
- **Format**: JSON
- **Endpoints**:
  - `POST /api/chat`: Send message, receive AI response (10 tools available)
  - `GET /health`: Health check
  - `GET /api/system/info`: System information
  - `GET /api/models`: Available models list

### 2. Backend ↔ Polygon.io
**Two Integration Methods:**

**A) MCP Server (7 tools):**
- **Protocol**: MCP (Model Context Protocol)
- **Tools**: get_snapshot_all, get_snapshot_option, get_aggs, list_aggs, get_daily_open_close_agg, get_previous_close_agg
- **Session**: SQLite-based session persistence
- **Integration**: `openai-agents-mcp>=0.0.8`

**B) Direct API (1 tool):** ⭐ NEW
- **Protocol**: HTTP REST API (polygon-api-client)
- **Tool**: get_market_status_and_date_time
- **Library**: polygon-api-client v1.15.4
- **Advantages**: Direct control, simpler architecture, better performance

### 3. Backend ↔ Finnhub API
- **Protocol**: HTTP REST API (finnhub-python)
- **Tool**: get_stock_quote
- **Library**: finnhub-python v2.4.25
- **Purpose**: Single ticker real-time quotes

### 4. Backend ↔ OpenAI API
- **Model**: GPT-5-Nano (exclusive)
- **SDK**: OpenAI Agents SDK v0.2.9
- **Authentication**: API key via environment variable
- **Features**: Agent-based interactions with tool calling (10 tools)

## Configuration Management

### Environment-Specific Configuration

**Backend (.env):**
```
POLYGON_API_KEY=xxx     # Used by MCP server + direct API
OPENAI_API_KEY=xxx      # OpenAI GPT-5-Nano access
FINNHUB_API_KEY=xxx     # Finnhub API access
```

**Frontend (config/app.config.json):**
- Non-sensitive settings
- API endpoint URLs
- Feature flags
- Environment-specific overrides

### Port Configuration
- **Backend**: 127.0.0.1:8000 (fixed)
- **Frontend Dev**: 127.0.0.1:3000 (fixed)
- **Frontend Prod**: 127.0.0.1:5500 (Live Server)

## Deployment Architecture

### Development Mode
```
Terminal 1: Backend (uvicorn with --reload)
Terminal 2: Frontend (vite dev server)
```

### Production Build
```
Frontend: npm run build → dist/ folder
Backend: uvicorn without --reload
Serve: Live Server or production web server
```

### One-Click Startup
```
./start-app-xterm.sh or ./start-app.sh
  ↓
Kill existing servers
  ↓
Start Backend (port 8000)
  ↓
Start Frontend (port 3000)
  ↓
Health checks (10 retries, 2s intervals)
  ↓
User navigates to http://127.0.0.1:3000
```

## Performance Considerations

### Backend Optimization
- Async/await for I/O operations
- Shared MCP server instance (not per-request)
- Shared session instance for agent persistence
- Process timing middleware for monitoring
- Direct API calls for improved performance (Polygon direct API)

### Frontend Optimization
- React.memo for component memoization
- Debounced input handling
- Code splitting with Vite
- Lazy loading of components
- Production bundle optimization
- PWA support with service workers
- Removed unused components (Export, Debug, Recent Messages panels)
- Consolidated panels for reduced UI complexity

### Performance Targets & Latest Results
- **First Contentful Paint**: ~256ms
- **Core Web Vitals**: 85%+ improvement
- **Memory Heap**: ~13.8MB optimized
- **Backend Response** (Oct 5, 2025 Test Results):
  - Min Response Time: 11.100s
  - Max Response Time: 31.264s
  - Average Response Time: 20.11s
  - Success Rate: 100% (7/7 tests)
  - Performance Rating: EXCELLENT

## Security Architecture

### API Key Management
- Stored in `.env` (never committed)
- Loaded via `python-dotenv`
- Environment variables only
- Three API keys required:
  - OPENAI_API_KEY (GPT-5-Nano)
  - POLYGON_API_KEY (MCP + direct API)
  - FINNHUB_API_KEY (stock quotes)

### CORS Configuration
- Configured in main.py
- Allows frontend origin
- Credentials support enabled

### Input Validation
- Pydantic models for request validation
- Type checking on frontend (TypeScript)
- Sanitization of user inputs

## Testing Strategy

### Backend Testing
- Unit tests with pytest
- Test utilities in test_utils.py
- Comprehensive CLI test suite (7 prompts in single persistent session)
- **Latest Results (Oct 5, 2025)**: 7/7 tests PASSED, 20.11s avg, EXCELLENT performance

### Frontend Testing
- E2E tests with Playwright
- Component testing (to be expanded)

### Integration Testing
- Full stack tests via comprehensive script
- Health check validation
- API response validation
- Validates all 10 tools work correctly

## Scalability Considerations

### Current Architecture
- Single-process backend (uvicorn)
- Shared state (MCP server, session)
- 10 AI agent tools (2 custom + 7 MCP + 1 removed)
- Suitable for development and small-scale production

### Future Scaling Options
- Multi-worker uvicorn deployment
- State externalization (Redis for sessions)
- Load balancing for frontend
- CDN for static assets
- Separate MCP server per worker (if needed)
- Complete migration from MCP to direct API calls

## UI/UX Architecture Changes (Oct 2025)

### Panel Consolidation
**Removed Panels:**
- Export & Recent Messages Panel (ExportButtons, RecentMessageButtons)
- Debug Information Panel (DebugPanel)

**Consolidated Panel:**
- **"System Status & Performance"** panel combines:
  - Status metrics: Message count, loading state (Ready/Processing)
  - Performance metrics: FCP, LCP, CLS
  - Single CollapsiblePanel with responsive grid layout
  - Data test ID: `status-performance-panel`

### Benefits
- **Cleaner UI**: Reduced visual clutter
- **Better UX**: Related information grouped logically
- **Simplified Codebase**: 4 files removed, 1 file modified
- **No Backend Impact**: Pure frontend refactor
- **Maintained Functionality**: Critical status/performance info preserved

## Migration Strategy: MCP to Direct API

### Rationale
- **Performance**: Direct API calls eliminate MCP routing overhead
- **Simplicity**: Fewer dependencies and infrastructure layers
- **Control**: Full control over API interaction and error handling
- **Flexibility**: Easier to customize response formats

### Phase 1: Proof of Concept (✅ COMPLETED Oct 5, 2025)
- **Target**: get_market_status (MCP) → get_market_status_and_date_time (Direct API)
- **Implementation**: polygon_tools.py created
- **Result**: Successfully replaced MCP tool with direct API
- **Validation**: All 7 CLI tests pass with new tool

### Future Phases
- **Phase 2**: Migrate snapshot tools (get_snapshot_all, get_snapshot_option)
- **Phase 3**: Migrate aggregate tools (get_aggs, list_aggs, etc.)
- **Phase 4**: Complete MCP deprecation
- **Timeline**: TBD based on Phase 1 success

## Branch Management & Version Control (Oct 2025)

### Major Branch Merge: clean_serena_reset → master
**Date**: October 4, 2025
**Merge Type**: Fast-forward merge (no conflicts)

#### Merge Summary
- **Commits Merged**: 260+ commits from clean_serena_reset development branch
- **Files Changed**: 471 files (+37,280 insertions, -143,107 deletions)
- **Net Code Reduction**: -105,827 lines (major refactoring and cleanup)
- **Common Ancestor**: Commit 977517b `[new_task]`

#### Branch State
- **master**: Now synchronized with clean_serena_reset at commit 4a4951a
- **clean_serena_reset**: Development branch (can continue for future features)
- **Remote Status**: Both branches pushed and synchronized with origin

#### Validation Results
All 7 CLI tests passed on master branch after merge:
- **Test Success Rate**: 100% (7/7 tests)
- **Response Time Range**: 12.576s - 22.534s
- **Average Response Time**: 17.69s
- **Performance Rating**: EXCELLENT
- **Session Mode**: Persistent (all tests in single session)

#### Key Changes from Merge
The merge brought stable development work from clean_serena_reset including:
- Serena onboarding and memory system
- Comprehensive linting (10.00/10 Python, 0 errors/warnings TypeScript)
- UI refactoring and panel consolidation
- Performance optimizations (85%+ Core Web Vitals improvement)
- Testing infrastructure (7-prompt persistent session tests)
- Documentation updates (CLAUDE.md, project memories)
- Startup script improvements (30-second timeout mechanism)
- Configuration centralization (config/app.config.json)

#### Post-Merge Status
- **Working Tree**: Clean
- **Branch Synchronization**: Complete
- **Test Validation**: Passed
- **Production Readiness**: Stable
- **Development Strategy**: Both branches available for continued development
