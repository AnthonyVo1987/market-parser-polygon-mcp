# Project Architecture

## High-Level Overview

**Market Parser** is a full-stack financial analysis application with:
- **Backend**: Python FastAPI REST API with OpenAI Agents SDK integration
- **Frontend**: React TypeScript SPA with real-time chat interface
- **Integration**: Polygon.io MCP server for financial data
- **AI Model**: OpenAI GPT-5-Nano (exclusive, GPT-5-Mini removed)

## Directory Structure

```
market-parser-polygon-mcp/
├── src/
│   ├── backend/              # Python FastAPI backend
│   │   ├── routers/          # API endpoint routers
│   │   ├── services/         # Business logic services
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
- `create_agent()`: Creates AI agent with MCP tools
- `get_enhanced_agent_instructions()`: Returns agent prompt template
- `get_optimized_model_settings()`: Returns GPT-5-Nano configuration

**Responsibilities:**
- Agent instantiation with OpenAI Agents SDK
- System prompt configuration
- Model settings (GPT-5-Nano only)
- MCP tool integration

#### 3. services/mcp_service.py - MCP Server Integration
**Responsibilities:**
- Polygon.io MCP server connection
- MCP tool availability management
- Session lifecycle management

#### 4. routers/ - API Endpoints
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

#### 5. utils/ - Utility Modules
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
MCP Server (Polygon.io) → Financial Data
    ↓
Agent Response Processing
    ↓
JSON Response to Frontend
```

### Backend Dependencies

**Core:**
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `openai-agents==0.2.9`: OpenAI Agents SDK
- `openai>=1.99.0,<1.100.0`: OpenAI API client
- `pydantic`: Data validation
- `python-dotenv`: Environment variables
- `aiofiles`: Async file I/O

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
Backend Processing
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
  - `POST /api/chat`: Send message, receive AI response
  - `GET /health`: Health check
  - `GET /api/system/info`: System information
  - `GET /api/models`: Available models list

### 2. Backend ↔ Polygon.io MCP
- **Protocol**: MCP (Model Context Protocol)
- **Tools Available**: Financial data queries via Polygon.io
- **Session**: SQLite-based session persistence
- **Integration**: `openai-agents-mcp>=0.0.8`

### 3. Backend ↔ OpenAI API
- **Model**: GPT-5-Nano (exclusive)
- **SDK**: OpenAI Agents SDK v0.2.9
- **Authentication**: API key via environment variable
- **Features**: Agent-based interactions with tool calling

## Configuration Management

### Environment-Specific Configuration

**Backend (.env):**
```
POLYGON_API_KEY=xxx
OPENAI_API_KEY=xxx
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

### Frontend Optimization
- React.memo for component memoization
- Debounced input handling
- Code splitting with Vite
- Lazy loading of components
- Production bundle optimization
- PWA support with service workers
- Removed unused components (Export, Debug, Recent Messages panels)
- Consolidated panels for reduced UI complexity

### Performance Targets
- **First Contentful Paint**: ~256ms
- **Core Web Vitals**: 85%+ improvement
- **Memory Heap**: ~13.8MB optimized
- **Backend Response**: 14-28s for complex queries (real API calls, Oct 2025 benchmark)

## Security Architecture

### API Key Management
- Stored in `.env` (never committed)
- Loaded via `python-dotenv`
- Environment variables only

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

### Frontend Testing
- E2E tests with Playwright
- Component testing (to be expanded)

### Integration Testing
- Full stack tests via comprehensive script
- Health check validation
- API response validation
- **Latest Test Results (Oct 4, 2025)**: 7/7 tests passed, 18.78s avg response time, EXCELLENT performance

## Scalability Considerations

### Current Architecture
- Single-process backend (uvicorn)
- Shared state (MCP server, session)
- Suitable for development and small-scale production

### Future Scaling Options
- Multi-worker uvicorn deployment
- State externalization (Redis for sessions)
- Load balancing for frontend
- CDN for static assets
- Separate MCP server per worker (if needed)

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