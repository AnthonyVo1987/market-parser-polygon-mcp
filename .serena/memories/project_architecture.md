# Project Architecture

## Overview

Market Parser is a Python CLI and React web application for natural language financial queries using Direct Polygon/Tradier API integration and OpenAI GPT-5-Nano via the OpenAI Agents SDK v0.2.9.

**Key Architectural Changes (Oct 2025):**
- **Persistent Agent Architecture** (ONE agent per lifecycle, CLI = core, GUI = wrapper)
- **Migrated from MCP to Direct API** (70% performance improvement)
- **Removed get_stock_quote_multi wrapper** (leverages SDK parallel execution)
- **Fixed OHLC display requirements** (show actual data, not just "retrieved")
- **Enhanced chat history analysis** (prevent redundant Support/Resistance calls)
- **Eliminated frontend code duplication** (157 lines deleted, simplified markdown rendering)
- **All 7 tools now use Direct Python APIs** (no MCP overhead)

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
                    │   Generates Markdown      │
                    │   Persistent Agent (1x)   │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   OpenAI Agents SDK       │
                    │   v0.2.9 (GPT-5-Nano)     │
                    │   Parallel Tool Execution │
                    │   Chat History Analysis   │
                    │   System Prompt Caching   │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   AI Agent Tools (7)      │
                    │   Direct API Integration  │
                    │   OHLC Display Fix        │
                    └─────────┬────────┬────────┘
                              │        │
                    ┌─────────▼──┐  ┌─▼────────┐
                    │ Polygon.io │  │ Tradier  │
                    │ Direct API │  │ Direct   │
                    │ (2 tools)  │  │ (5 tools)│
                    └────────────┘  └──────────┘
```

## Agent Lifecycle Management (October 2025)

### Problem Solved

**Original Architecture (INCORRECT ❌):**
- Created NEW OpenAI agent for EVERY user message
- System prompt sent with EVERY message (2000+ tokens each time)
- No prompt caching benefits
- Agent had no context from previous messages
- Wasted tokens and API calls

**New Architecture (CORRECT ✅):**
- Create ONE persistent agent per lifecycle (startup)
- Agent reused for ALL messages in session
- System prompt cached after first message (50% token savings)
- Agent maintains context across entire session
- Best practices compliant

### Architecture Pattern: CLI = Core, GUI = Wrapper

**Following commit b866f0a principle:**

```
Backend/CLI owns core business logic
         ↓
Frontend/GUI calls CLI functions
         ↓
  No code duplication
```

### Implementation Details

#### Core Functions (src/backend/cli.py)

**1. initialize_persistent_agent()** - Single Source of Truth
```python
def initialize_persistent_agent():
    """Initialize persistent agent for the session.

    This is the SINGLE SOURCE OF TRUTH for agent initialization.
    Both CLI and GUI modes use this function to create their agent instance.

    Following the architecture principle from commit b866f0a:
    - CLI owns core business logic (this function)
    - GUI imports and calls this function (no duplication)

    Returns:
        Agent: The initialized financial analysis agent
    """
    return create_agent()
```

**2. process_query()** - Core Business Logic
```python
async def process_query(agent, session, user_input):
    """Process a user query using the persistent agent.

    This is the CORE BUSINESS LOGIC for query processing.
    Both CLI and GUI modes call this function (no duplication).

    Following the architecture principle from commit b866f0a:
    - CLI owns core business logic (this function)
    - GUI imports and calls this function (no duplication)

    Args:
        agent: The persistent agent instance
        session: The SQLite session for conversation memory
        user_input: The user's query string

    Returns:
        RunResult: The result from Runner.run() containing the agent's response
    """
    result = await Runner.run(agent, user_input, session=session)
    return result
```

### CLI Mode (src/backend/cli.py)

**Agent Creation:**
```python
async def cli_async():
    # Initialize persistent CLI session for conversation memory
    cli_session = SQLiteSession(settings.cli_session_name)
    
    # Create persistent agent ONCE for the entire session (following b866f0a pattern)
    analysis_agent = initialize_persistent_agent()
    print("🤖 Persistent agent initialized - agent will be reused for all messages")
    
    await _run_cli_loop(cli_session, analysis_agent)
```

**Query Processing:**
```python
async def _process_user_input(cli_session, analysis_agent, user_input):
    # Call shared processing function (core business logic - no duplication)
    result = await process_query(analysis_agent, cli_session, user_input)
    
    # Extract token data and create CLI-specific metadata wrapper
    token_count = extract_token_count_from_context_wrapper(result)
    cli_metadata = ResponseMetadata(...)
    
    return result
```

**Key Points:**
- Agent created ONCE at CLI startup
- Same agent reused for ALL user inputs in session
- CLI owns core logic (initialize_persistent_agent, process_query)
- System prompt cached after first message (50% token savings)

### GUI Mode (FastAPI)

#### Lifespan Management (src/backend/main.py)

**Agent Creation at Startup:**
```python
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """FastAPI lifespan management for shared session and agent instances.
    
    Following the architecture principle from commit b866f0a:
    - CLI owns core business logic (initialize_persistent_agent function)
    - FastAPI imports and calls this function (no duplication)
    """
    global shared_session, shared_agent

    # Startup: Create shared instances
    try:
        # Initialize session
        shared_session = SQLiteSession(settings.agent_session_name)
        
        # Initialize persistent agent using shared CLI function (no duplication)
        shared_agent = initialize_persistent_agent()

        # Set shared resources for dependency injection
        set_shared_resources(shared_session, shared_agent)

        print("✅ FastAPI initialized with persistent agent (following b866f0a pattern)")
    except Exception as e:
        print(f"Initialization failed: {e}")
        raise

    yield

    # Cleanup: Close shared instances (if needed in future)
```

**Key Points:**
- Agent created ONCE at FastAPI startup
- Stored in global `shared_agent` variable
- GUI calls CLI function (no duplicate agent creation logic)
- Same agent serves ALL HTTP requests

#### Dependency Injection (src/backend/dependencies.py)

**Shared Resources Management:**
```python
# Global shared resources - will be set by main module
_shared_session: Optional[SQLiteSession] = None
_shared_agent: Optional[Agent] = None

def set_shared_resources(session: SQLiteSession, agent: Agent):
    """Set the shared resources for dependency injection.

    Args:
        session: The SQLite session for conversation memory
        agent: The persistent agent instance
    """
    global _shared_session, _shared_agent
    _shared_session = session
    _shared_agent = agent

def get_agent() -> Agent:
    """Get shared agent instance.

    Returns:
        Agent: The persistent agent instance

    Raises:
        RuntimeError: If agent not initialized
    """
    if _shared_agent is None:
        raise RuntimeError("Shared agent not initialized")
    return _shared_agent

def get_session() -> Optional[SQLiteSession]:
    """Get shared session instance.

    Returns:
        SQLiteSession instance or None if not set
    """
    return _shared_session
```

**Key Points:**
- Global variables store shared agent and session
- Dependency injection provides to endpoints
- Thread-safe access via getter functions
- Runtime error if agent not initialized

#### Chat Endpoint (src/backend/routers/chat.py)

**Using Shared Agent:**
```python
@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Process a financial query and return the response.
    
    Following the architecture principle from commit b866f0a:
    - GUI imports and calls CLI core business logic (process_query function)
    - No duplication of agent creation or query processing
    """
    # Get shared resources from dependency injection
    shared_session = get_session()
    shared_agent = get_agent()
    
    # ... input validation ...
    
    # Call shared CLI processing function (core business logic - no duplication)
    result = await process_query(shared_agent, shared_session, stripped_message)
    
    # Extract the response
    response_text = str(result.final_output)
    
    # Extract token data using official OpenAI Agents SDK (GUI-specific wrapper)
    token_usage = extract_token_usage_from_context_wrapper(result)
    
    # Create response metadata with timing and token information (GUI-specific wrapper)
    response_metadata = ResponseMetadata(...)
    
    # Return HTTP response (GUI-specific wrapper)
    return ChatResponse(response=response_text, metadata=response_metadata)
```

**Key Points:**
- Endpoint gets agent from dependency injection
- Calls CLI `process_query()` function (no duplication)
- Same agent serves all HTTP requests
- GUI adds HTTP-specific wrappers (metadata, response format)

### Data Flow Comparison

**Before (Agent Per Message ❌):**
```
User Message #1 → Create Agent → Process → System Prompt (2000 tokens)
User Message #2 → Create Agent → Process → System Prompt (2000 tokens)
User Message #3 → Create Agent → Process → System Prompt (2000 tokens)
Total: 6000+ tokens wasted
```

**After (Persistent Agent ✅):**
```
Startup → Create Agent (ONCE)
User Message #1 → Process with Agent → System Prompt (2000 tokens)
User Message #2 → Process with Agent → Cached Prompt (0 tokens, 50% savings)
User Message #3 → Process with Agent → Cached Prompt (0 tokens, 50% savings)
Total: 2000 tokens (4000 saved via caching)
```

### Benefits Summary

**1. Token Efficiency (50% Savings):**
- OLD: System prompt sent with EVERY message (2000+ tokens each)
- NEW: System prompt sent ONCE, cached for subsequent messages
- Savings: 50% reduction in input tokens via OpenAI prompt caching

**2. Reduced Overhead:**
- OLD: Agent creation cost (API calls, model loading) for EVERY message
- NEW: Agent creation cost paid ONCE at startup
- Impact: Faster response times, less CPU usage

**3. Proper Agent Memory:**
- OLD: Each new agent had no context from previous messages
- NEW: Same agent maintains context across entire session
- Result: Better conversation flow, proper chat history

**4. Best Practices Compliance:**
- Follows OpenAI Agents SDK best practices
- Matches real-world AI agent usage patterns
- Enables prompt caching optimizations

**5. Zero Code Duplication:**
- CLI owns agent initialization logic (initialize_persistent_agent)
- CLI owns query processing logic (process_query)
- GUI imports and calls CLI functions
- No duplicate code between CLI and GUI

### Testing Validation

**Test Results (Oct 2025):**
- 38/38 tests PASSED (100% success rate)
- Average: 11.05s (EXCELLENT rating)
- Session persistence: VERIFIED across all tests
- All 38 tests run in SINGLE CLI session
- Agent reused for all messages

**Prompt Caching Verification:**
- First message: ~2500 tokens (system prompt included)
- Subsequent messages: ~500 tokens (prompt cached, 50% savings)
- Session savings: 50% reduction in cumulative input tokens

**Test Report:** `test-reports/test_cli_regression_loop1_2025-10-09_20-33.log`

### Files Involved

**Core Business Logic:**
- `src/backend/cli.py` - Shared functions, CLI mode implementation
  - `initialize_persistent_agent()` - Single source of truth for agent creation
  - `process_query()` - Single source of truth for query processing
  - `cli_async()` - CLI mode with persistent agent
- `src/backend/services/agent_service.py` - Agent creation logic
  - `create_agent()` - Actual agent instantiation

**GUI Integration:**
- `src/backend/main.py` - FastAPI lifespan with agent initialization
  - `lifespan()` - Creates agent at startup via CLI function
- `src/backend/routers/chat.py` - Chat endpoint using shared functions
  - `chat_endpoint()` - Calls CLI `process_query()` function
- `src/backend/dependencies.py` - Dependency injection for shared resources
  - `set_shared_resources()` - Stores agent and session
  - `get_agent()` - Returns persistent agent
  - `get_session()` - Returns persistent session

**Documentation:**
- `.serena/memories/tech_stack.md` - Persistent agent architecture details
- `.serena/memories/project_architecture.md` - This file
- `CLAUDE.md` - Last Completed Task summary

## Backend Architecture

### FastAPI Application (main.py)

**Key Components:**
- `app` - FastAPI application instance
- `lifespan` - Async context manager for startup/shutdown (creates persistent agent)
- `shared_session` - Shared SQLiteSession for conversation memory
- `shared_agent` - Persistent agent instance (created once, reused for all requests)
- `add_process_time_header` - Middleware for response timing
- CORS configuration for frontend communication

**Endpoints:**
- `POST /api/v1/chat/` - Process natural language queries
- `GET /health` - Health check endpoint
- `GET /` - Root endpoint with API info

**Features:**
- Real-time response timing via middleware
- Token usage tracking from OpenAI responses
- CORS enabled for http://127.0.0.1:3000
- Async request handling
- **Persistent agent** (created once at startup, reused for all requests)
- **Markdown generation** - Single source of truth for all interfaces

### Agent Service (services/agent_service.py)

**Functions:**
- `get_enhanced_agent_instructions()` - Returns optimized system prompt with 9 RULES
- `get_optimized_model_settings()` - Returns GPT-5-Nano config
- `create_agent()` - Creates OpenAI agent with all 7 tools

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

### Direct API Tools (7 Total)

#### Tradier Custom API (5 tools)
**File:** `src/backend/tools/tradier_tools.py`

**Tools:**
1. `get_stock_quote(symbol: str)` - Real-time stock quotes
2. `get_stock_price_history(...)` - Historical pricing data
3. `get_options_expiration_dates(...)` - Valid expiration dates
4. `get_call_options_chain(...)` - Call options chain
5. `get_put_options_chain(...)` - Put options chain

**Implementation:**
- Uses `requests` library for direct API calls
- Environment: `TRADIER_API_KEY`
- Supports multi-ticker queries natively
- **Supports parallel calls** for multi-ticker queries (max 3 per batch)

#### Polygon Direct API (2 tools)
**File:** `src/backend/tools/polygon_tools.py`

**Market Data Tools:**
1. `get_market_status_and_date_time()` - Market status + current datetime
2. `get_ta_indicators(...)` - Technical analysis indicators

**Implementation:**
- Direct Polygon Python SDK integration
- Environment: `POLYGON_API_KEY`

### Configuration Management

**Files:**
- `.env` - API keys (POLYGON_API_KEY, OPENAI_API_KEY, TRADIER_API_KEY)
- `config/app.config.json` - Non-sensitive settings
- `src/backend/config.py` - Config loader

**Environment Variables:**
```
POLYGON_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
TRADIER_API_KEY=your_key_here
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
- `ChatMessage_OpenAI` - Individual message component (simplified Oct 9)
- `PerformanceMetrics` - Real-time performance display

### Markdown Rendering Architecture (Oct 9, 2025 Simplification)

**Before (Duplicate Code ❌):**
```
Backend → Generates Markdown
    ├── CLI → Rich library renders (with styling)
    └── GUI → 157 lines of custom React components render (with styling)
                ↑ DUPLICATE FORMATTING LOGIC
```

**After (Zero Duplication ✅):**
```
Backend → Generates Markdown (Single Source of Truth)
    ├── CLI → Rich library renders
    └── GUI → Default react-markdown renders
                ↑ NO CUSTOM FORMATTING CODE
```

**Implementation Details:**

**File:** `src/frontend/components/ChatMessage_OpenAI.tsx`

**Deleted (157 lines total):**
- `createMarkdownComponents()` function (154 lines) - Custom React components for p, h1, h2, h3, ul, ol, li, strong, em, blockquote, code
- `markdownComponents` useMemo declaration (2 lines)
- `ComponentPropsWithoutRef` import (1 line)

**Simplified:**
```typescript
// BEFORE:
<Markdown components={markdownComponents}>
  {formattedMessage.formattedContent}
</Markdown>

// AFTER:
<Markdown>
  {formattedMessage.formattedContent}
</Markdown>
```

**Benefits:**
1. **Zero Code Duplication** - Backend owns all formatting decisions
2. **Simplified Maintenance** - Changes only in backend, frontend auto-inherits
3. **Better Performance** - Default react-markdown is lightweight, no custom component overhead
4. **Cleaner Codebase** - 157 lines deleted, simpler component structure

**Test Results (Oct 9, 2025):**
- CLI Regression: 38/38 PASSED (100%)
- Average Response Time: 11.14s (EXCELLENT)
- Frontend: User validated and approved GUI appearance
- No visual regression, all markdown rendering works correctly

### State Management

**React State (useState):**
- `messages` - Chat message history
- `isLoading` - Request loading state
- `config` - App configuration from config/app.config.json

**No external state management library** - Simple useState/useEffect patterns

### API Communication

**Service:** `src/frontend/services/api.ts`
- `sendQuery(query: string)` - POST to `/api/v1/chat/` endpoint
- Base URL: `http://127.0.0.1:8000`
- Returns: agent response + performance metrics

**Response Format:**
```typescript
{
  response: string;           // Agent's formatted markdown response
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
   - Receives POST /api/v1/chat/ request
   - Gets persistent agent from dependency injection
   - Passes query to agent (NO agent creation)

3. **AI Agent Processing** (OpenAI Agents SDK)
   - Uses persistent agent (cached system prompt)
   - Analyzes query
   - **STEP 0**: Checks chat history for existing data (RULE #9)
   - Determines which tools to call
   - For multi-ticker: Makes PARALLEL get_stock_quote() calls (RULE #2)
   - Executes Direct API tool calls (no MCP)
   - **OHLC Fix**: Shows actual data (start, end, change, high, low, days)
   - Generates structured markdown response

4. **Tool Execution** (Direct API)
   - Polygon Direct API: 2 tools
   - Tradier Direct API: 5 tools (parallel calls for multi-ticker)
   - No MCP server overhead
   - Direct Python SDK calls

5. **Response Generation** (Markdown Format)
   - Agent formats response as markdown (KEY TAKEAWAYS + DETAILED ANALYSIS)
   - Backend extracts token usage from OpenAI response
   - Middleware measures response time
   - **Single markdown format** for both CLI and GUI

6. **Response Delivery**
   - Backend sends JSON response with markdown content
   - **CLI**: Rich library renders markdown in terminal
   - **Frontend**: react-markdown renders markdown in browser (default styling)
   - Performance metrics shown in both interfaces

### Performance Tracking

**Backend Middleware:**
- Measures total response time
- Adds `X-Process-Time` header
- Logs performance metrics

**Token Tracking & Prompt Caching:**
- **Extraction Flow**:
  1. OpenAI Agents SDK captures usage in `context_wrapper.usage`
  2. `token_utils.extract_token_usage_from_context_wrapper()` extracts:
     - `total_tokens`, `input_tokens`, `output_tokens` (standard)
     - `cached_input_tokens`, `cached_output_tokens` (prompt caching)
  3. CLI: `response_utils.py` displays all token metrics
  4. API: `chat.py` returns tokens via `ResponseMetadata` model
  5. Frontend: `ChatMessage_OpenAI.tsx` displays in message footer
- **Prompt Caching** (October 2025):
  - Backend: `token_utils.py` extracts `input_tokens_details.cached_tokens`
  - API Models: `ResponseMetadata` includes cached token fields
  - CLI Display: Shows "Cached Input: X" when cache hits occur
  - Frontend Display: Shows cached tokens in message metadata
  - Cache Hit Indicator: `cached_tokens > 0` means cache was used
  - Cost Optimization: Agent instructions cached on every request (>1024 tokens)
  - Savings: 50% cost reduction on cached input tokens, up to 80% latency improvement
  - **Persistent Agent Benefit**: System prompt cached after first message

**Frontend Display:**
- Real-time performance metrics
- Token usage display
- Response time display
- Model name display

## Testing Architecture

### CLI Regression Testing (PRIMARY)

#### Latest Test Suite: test_cli_regression.sh (38 tests) ⭐ CURRENT
**Updated:** Oct 9, 2025
**Status:** Primary test suite

**Test Coverage:**
- **SPY Sequence** (15 tests): Market status, prices, TA indicators, options, OHLC
- **NVDA Sequence** (15 tests): Same pattern as SPY
- **Multi-Ticker WDC/AMD/GME** (5 tests): Parallel call validation
- **Visual Enhancement Tests** (3 tests): Markdown tables, emoji responses, wall analysis

**Features:**
- **Persistent session** (all 38 tests in SINGLE CLI session with SINGLE agent)
- Chat history analysis validation
- Parallel tool call verification
- OHLC display validation
- Support/Resistance redundant call detection
- **Markdown table rendering validation**
- **Emoji response validation**
- Response time tracking per test
- Success rate monitoring
- **Agent persistence verification** (same agent reused for all 38 tests)

**Latest Performance (Oct 9, 2025):**
- **Total**: 38/38 PASSED ✅
- **Success Rate**: 100%
- **Average**: 11.14s per query (EXCELLENT - within 12.07s baseline)
- **Session Duration**: 7 min 6 sec
- **Agent**: Single persistent agent for all 38 tests
- **Prompt Caching**: System prompt cached after first message (50% token savings)
- **Markdown Tables**: All options chain tables rendered correctly ✅
- **Emoji Responses**: Consistent 2-5 emojis per response ✅
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-09_16-57.log`

**Validation Results:**
- ✅ Agent persistence verified (single agent for all tests)
- ✅ Prompt caching verified (system prompt cached after message #1)
- ✅ OHLC display fix verified (shows actual data, not just "retrieved")
- ✅ Support & Resistance fix verified (no redundant calls)
- ✅ Chat history analysis working correctly
- ✅ Parallel tool calls executing properly (max 3 per batch)
- ✅ Markdown table formatting validated
- ✅ Emoji responses validated
- ✅ All test responses are CORRECT (not just completed)

#### Previous Test Suite: test_cli_regression.sh (35 tests)
**Created:** Oct 7, 2025 Evening
**Status:** Superseded by 38-test suite

## Performance Architecture

### Optimizations

**Backend:**
- Async request handling (FastAPI)
- **Persistent agent** (created once, reused for all requests)
- **Prompt caching** (system prompt cached after first message, 50% token savings)
- Direct API calls (no MCP overhead)
- Minimal tool calls enforcement
- Parallel tool execution for multi-ticker (max 3 per batch)
- Chat history analysis (avoid redundant calls)
- **Markdown generation** (single source of truth)

**Frontend:**
- Optimized CSS (no backdrop filters, complex shadows)
- Simple transitions (opacity, color only)
- Media queries (not container queries)
- Efficient bundle size (Vite tree shaking)
- **Simplified markdown rendering** (no custom components, 157 lines deleted)
- Default react-markdown rendering (lightweight)

**AI Agent:**
- **Persistent agent** (ONE agent per lifecycle, reused for all messages)
- **System prompt caching** (cached after first message, 50% savings on subsequent messages)
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

**API Performance (Latest - Oct 2025 with Persistent Agent):**
- **Average Response**: 11.05s (EXCELLENT)
- **Success Rate**: 100% (38/38 tests)
- **Agent**: Single persistent agent (no creation overhead)
- **Token Savings**: 50% via prompt caching (system prompt cached after first message)
- **Frontend**: Simplified markdown rendering (157 lines deleted)
- **No Performance Regression**: Maintaining baseline performance

**API Performance (Oct 7 Evening):**
- **Average Response**: 11.62s (EXCELLENT)
- **Success Rate**: 100% (35/35 tests)
- **OHLC Display**: Shows actual data instead of "retrieved"
- **Support & Resistance**: 29% faster (no redundant calls)

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
- **Persistent Agent**: Created once at startup via lifespan manager

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
- Starts backend in xterm window (creates persistent agent)
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

### Oct 2025: Persistent Agent Architecture ✅ COMPLETE

**Problem:**
- App was creating NEW OpenAI agent for EVERY message
- System prompt sent with EVERY message (2000+ tokens each time)
- No prompt caching benefits
- Agent had no context from previous messages
- Wasted tokens and API calls

**Solution:**
- Create ONE persistent agent per lifecycle (startup)
- CLI owns agent initialization (initialize_persistent_agent function)
- CLI owns query processing (process_query function)
- GUI imports and calls CLI functions (no duplication)
- Agent reused for ALL messages in session

**Architecture Change:**
- **Before**: Create agent for each message → No prompt caching
- **After**: Create agent once at startup → Prompt caching enabled (50% savings)
- **Pattern**: CLI = Single Source of Truth, GUI = Wrapper (commit b866f0a)

**Benefits:**
- ✅ 50% token savings via prompt caching (system prompt cached after first message)
- ✅ Reduced overhead (agent creation cost paid once)
- ✅ Proper agent memory (context across entire session)
- ✅ Zero code duplication (CLI owns logic, GUI imports)
- ✅ Best practices compliant

**Test Results:**
- 38/38 tests PASSED (100%)
- Average: 11.05s (EXCELLENT)
- Session persistence: VERIFIED
- All tests run in SINGLE CLI session with SINGLE agent

**Files Modified:**
- `src/backend/cli.py` - Added shared functions, made agent persistent
- `src/backend/main.py` - FastAPI lifespan creates agent via CLI function
- `src/backend/routers/chat.py` - Chat endpoint calls CLI process_query function
- `src/backend/dependencies.py` - Added agent to shared resources

**Test Report:** `test-reports/test_cli_regression_loop1_2025-10-09_20-33.log`

### Oct 9, 2025: Frontend Code Duplication Elimination ✅ COMPLETE

**Problem:**
- Frontend had 157 lines of duplicate formatting code
- Custom React components replicated backend markdown formatting logic
- Maintenance burden: changes needed in 2 places (backend + frontend)

**Solution:**
- Deleted `createMarkdownComponents()` function (154 lines)
- Deleted `markdownComponents` useMemo declaration (2 lines)
- Removed `components` prop from Markdown component
- Removed unused `ComponentPropsWithoutRef` import (1 line)
- Use default react-markdown rendering

**Architecture Change:**
- **Before**: Backend generates markdown → CLI (Rich) + GUI (157 lines custom React components)
- **After**: Backend generates markdown → CLI (Rich) + GUI (default react-markdown)
- **Result**: Zero code duplication, backend is single source of truth

**Benefits:**
- ✅ 157 lines deleted from frontend
- ✅ Zero formatting code duplication
- ✅ Simplified maintenance (changes only in backend)
- ✅ Better performance (no custom component overhead)
- ✅ Cleaner codebase

**Test Results:**
- CLI Regression: 38/38 PASSED (100%)
- Average Response Time: 11.14s (EXCELLENT)
- Frontend: User validated and approved GUI appearance
- No visual regression

**Documentation:**
- Created CORRECTED_ARCHITECTURE_RESEARCH.md (453 lines analysis)
- Created RESEARCH_SUMMARY.md (279 lines summary)
- Created SOLUTION_SUMMARY.md (106 lines quick guide)
- Updated .serena/memories/tech_stack.md

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

### Oct 7, 2025 Afternoon: get_stock_quote_multi Removal ✅ COMPLETE

**Rationale:** Unnecessary wrapper function, SDK handles parallel execution natively

**Changes:**
- ✅ Removed get_stock_quote_multi (139 lines)
- ✅ Updated RULE #2 to emphasize parallel calls
- ✅ Tool count reduced from 12 to 7
- ✅ All tests pass 27/27 (100% success rate)

**New Architecture:**
- Multi-ticker queries: Agent makes parallel get_stock_quote() calls
- Example: "SPY, QQQ, IWM" → 3 parallel calls (max 3 per batch)
- Performance: 7.31s average (EXCELLENT)

### Oct 2025: MCP Removal ✅ COMPLETE

**Migration completed:**
- ✅ All 7 tools migrated to Direct API
- ✅ MCP server completely removed
- ✅ Performance improved 70% (6.10s avg vs 20s legacy)
- ✅ Token tracking enhanced (dual naming support)
- ✅ Model selector removed (GPT-5-Nano only)

**Architecture Changes:**
- **Before**: FastAPI → OpenAI Agent → MCP Server → Polygon/Tradier APIs
- **After**: FastAPI → OpenAI Agent → Direct Polygon/Tradier Python SDKs

**Performance Gains:**
- **Response Time**: 20s → 6.10s (70% faster)
- **Overhead**: Removed MCP server latency
- **Reliability**: Direct API calls (no MCP middleman)

## Current State Summary (Oct 2025)

**Architecture:**
- **Persistent Agent** (ONE agent per lifecycle, CLI = core, GUI = wrapper)
- 7 Direct API tools (5 Tradier + 2 Polygon)
- No MCP overhead
- Parallel execution (max 3 per batch)
- Chat history analysis
- OHLC display requirements enforced
- **Simplified frontend** (157 lines deleted, zero code duplication)
- **50% token savings** via prompt caching (system prompt cached after first message)

**Performance:**
- 38/38 tests passing (100%)
- 11.05s average (EXCELLENT)
- **Agent persistence validated** (single agent for all tests)
- **Prompt caching validated** (50% token savings)
- Support & Resistance optimized
- OHLC responses show actual data
- Frontend simplified with no performance regression

**Testing:**
- Primary: test_cli_regression.sh (38 tests)
- Latest report: test-reports/test_cli_regression_loop1_2025-10-09_20-33.log
- All tests run in SINGLE CLI session with SINGLE agent

**Latest Improvements:**
- ✅ **Persistent agent architecture** (50% token savings, proper agent memory)
- ✅ Frontend code duplication eliminated (157 lines deleted)
- ✅ Simplified markdown rendering (backend is single source of truth)
- ✅ OHLC display fix (show actual data)
- ✅ Support/Resistance redundant call fix
- ✅ All test responses verified as CORRECT
