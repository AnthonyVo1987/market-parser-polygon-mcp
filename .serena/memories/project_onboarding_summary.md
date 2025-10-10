# Project Onboarding Summary (October 2025 - Post-Persistent Agent Architecture)

## Project Purpose

Market Parser is a Python CLI and React web application for natural language financial queries using:
- **Direct Polygon.io API** integration (10 tools)
- **Finnhub API** integration (1 tool) 
- **OpenAI GPT-5-Nano** via OpenAI Agents SDK v0.2.9
- **Persistent Agent Architecture** (ONE agent per lifecycle, not per message)

**Key Value Proposition**:
- Natural language financial queries (e.g., "Tesla stock analysis", "SPY support and resistance")
- Real-time market data from Polygon.io and Finnhub APIs
- AI-powered analysis using GPT-5-Nano
- Multiple interfaces: CLI, Web App, REST API
- **50% token savings** via persistent agent and prompt caching

## Recent Major Architectural Changes (October 2025)

### 1. Persistent Agent Architecture ⭐ **MOST RECENT & CRITICAL**
**Problem Solved**: App was creating NEW agent for EVERY message (token waste, no prompt caching)

**Solution Implemented**:
- Create ONE persistent agent per lifecycle (startup)
- CLI owns `initialize_persistent_agent()` and `process_query()` functions
- GUI imports and calls CLI functions (zero code duplication)
- Agent reused for ALL messages in session

**Architecture Pattern** (following commit b866f0a):
```
CLI = Single Source of Truth (owns core business logic)
         ↓
GUI = Wrapper (imports and calls CLI functions)
         ↓
  No code duplication
```

**Key Benefits**:
- 50% token savings via prompt caching (system prompt cached after first message)
- Reduced overhead (agent creation cost paid once)
- Proper agent memory (context across entire session)
- Zero code duplication between CLI and GUI
- Best practices compliant (OpenAI recommended pattern)

**Files Involved**:
- `src/backend/cli.py` - Core functions (initialize_persistent_agent, process_query)
- `src/backend/main.py` - FastAPI lifespan creates agent via CLI function
- `src/backend/routers/chat.py` - Chat endpoint calls CLI process_query function
- `src/backend/dependencies.py` - Dependency injection for shared resources

### 2. Frontend Code Duplication Elimination
- Deleted 157 lines of duplicate formatting code in frontend
- Backend generates markdown → CLI/GUI both render (no custom React components)
- Simplified maintenance (changes only in backend)

### 3. Direct API Migration (70% Performance Improvement)
- Migrated ALL tools from MCP to Direct Python APIs
- Removed MCP server completely
- Performance: 20s → 6.10s average (70% faster)

## Tech Stack

### Backend
- **Language**: Python 3.12.3
- **Package Manager**: uv 0.8.19
- **Framework**: FastAPI (latest)
- **AI Integration**: OpenAI Agents SDK v0.2.9
- **AI Model**: GPT-5-Nano (EXCLUSIVE - 200K TPM)
- **Service Tier**: "default" (optimized for prototyping)
- **APIs**:
  - Polygon.io Direct API (polygon-api-client>=1.14.0) - 10 tools
  - Finnhub Direct API (finnhub-python>=2.4.25) - 1 tool
  - OpenAI Agents SDK (openai-agents==0.2.9)

### Frontend
- **Framework**: React 18.2+
- **Build Tool**: Vite 5.2+
- **Language**: TypeScript
- **Node**: v24.6.0
- **Package Manager**: npm 11.6.0
- **UI**: React Markdown (default rendering, no custom components)

### Development Tools
- **Python**: pylint, black, isort, mypy
- **JavaScript/TypeScript**: ESLint, Prettier, TypeScript compiler
- **Testing**: CLI regression suite (test_cli_regression.sh - 38 tests)
- **Performance**: Lighthouse CI, React Scan

## Project Structure

```
market-parser-polygon-mcp/
├── src/
│   ├── backend/              # FastAPI backend
│   │   ├── main.py          # Main app + FastAPI lifespan (creates persistent agent)
│   │   ├── cli.py           # CLI + shared functions (initialize_persistent_agent, process_query)
│   │   ├── dependencies.py  # Dependency injection (get_agent, get_session)
│   │   ├── routers/
│   │   │   └── chat.py      # Chat endpoint (calls CLI functions)
│   │   ├── services/
│   │   │   └── agent_service.py  # Agent creation logic
│   │   └── tools/
│   │       ├── polygon_tools.py  # 10 Polygon Direct API tools
│   │       └── finnhub_tools.py  # 1 Finnhub tool
│   └── frontend/            # React frontend
│       ├── components/      # React components (simplified markdown rendering)
│       ├── hooks/          # Custom hooks
│       └── services/       # API client
├── config/                 # Centralized configuration
│   └── app.config.json    # Non-sensitive settings
├── test-reports/          # Test execution reports
├── .serena/               # Serena MCP server files
│   ├── memories/          # Project knowledge base
│   └── cache/            # Symbol indexing cache
├── .claude/              # Claude Code settings
├── tests/                # Python tests
├── docs/                 # Documentation
├── pyproject.toml        # Python dependencies
├── package.json          # Node.js dependencies
├── test_cli_regression.sh  # CLI test suite (38 tests)
├── start-app.sh          # One-click startup script
└── start-app-xterm.sh    # XTerm startup script (recommended)
```

## Key Commands

### Application Startup (Recommended)
```bash
# One-click startup (creates persistent agent at startup)
chmod +x start-app-xterm.sh && ./start-app-xterm.sh

# Manual backend (creates persistent agent)
npm run backend:dev

# Manual frontend
npm run frontend:dev

# CLI only (creates persistent agent)
npm run backend:cli
```

### Testing
```bash
# Run CLI regression test suite (38 tests, persistent session)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Validates:
# - Agent persistence (single agent for all 38 tests)
# - Prompt caching (system prompt cached after first message)
# - 100% pass rate expected
# - Average response time: ~11s (EXCELLENT)
```

### Code Quality
```bash
# Lint all (Python + JavaScript)
npm run lint

# Lint with auto-fix
npm run lint:fix

# Format JavaScript/TypeScript
npm run format

# Type check
npm run type-check

# All quality checks
npm run check:all
```

### Build
```bash
# Production build
npm run build

# Development build
npm run build:dev

# Staging build
npm run build:staging
```

## Code Style & Conventions

### Python
- **Line Length**: 100 characters
- **Formatter**: black
- **Import Sorting**: isort (black profile)
- **Linter**: pylint
- **Type Hints**: Required for all function parameters and returns
- **Docstrings**: Required for all public functions/classes (Google style)
- **Model**: GPT-5-Nano ONLY (no model selection, exclusive)

### JavaScript/TypeScript
- **Formatter**: Prettier
- **Linter**: ESLint
- **Max Warnings**: 150
- **Style**: Airbnb base with modifications
- **Type Safety**: Strict TypeScript enabled
- **React**: Functional components with hooks

### Architecture Patterns
- **CLI = Core, GUI = Wrapper** (commit b866f0a pattern)
- **Zero Code Duplication**: CLI owns logic, GUI imports
- **Persistent Agent**: ONE agent per lifecycle, not per message
- **Markdown Generation**: Backend generates, CLI/GUI render (no custom formatting)
- **Direct API Integration**: No MCP overhead

## Task Completion Checklist

When completing a task:

1. ✅ **Code Changes**: Implement requested changes
2. ✅ **Code Quality**: Run `npm run lint:fix` and `npm run type-check`
3. ✅ **Testing**: Run `./test_cli_regression.sh` (38 tests, must show 100% pass rate)
4. ✅ **Documentation**: Update relevant docs (CLAUDE.md, memories, etc.)
5. ✅ **Serena Memories**: Update affected memory files
6. ✅ **Git Commit**: Follow atomic commit workflow
   - DO ALL WORK FIRST (code + tests + docs + memories)
   - Stage ALL files at once: `git add -A`
   - Commit immediately: `git commit -m "message"`
   - Push immediately: `git push`

**CRITICAL**: Never stage files early - stage ONLY immediately before committing. See `.serena/memories/git_commit_workflow.md` for details.

## Agent Architecture (CRITICAL - Most Recent Change)

### Persistent Agent Lifecycle

**CLI Mode**:
```python
# Create agent ONCE at startup
cli_session = SQLiteSession("cli_session")
analysis_agent = initialize_persistent_agent()  # From cli.py

# Reuse agent for ALL messages
for user_input in inputs:
    result = await process_query(analysis_agent, cli_session, user_input)
```

**GUI Mode (FastAPI)**:
```python
# Create agent ONCE in lifespan
@asynccontextmanager
async def lifespan(fastapi_app):
    shared_agent = initialize_persistent_agent()  # Import from cli.py
    set_shared_resources(shared_session, shared_agent)
    yield

# Reuse agent for ALL HTTP requests
@router.post("/api/v1/chat/")
async def chat_endpoint(request):
    shared_agent = get_agent()  # Get persistent agent
    result = await process_query(shared_agent, shared_session, user_input)
```

### Key Functions (src/backend/cli.py)

**initialize_persistent_agent()**:
- Single source of truth for agent creation
- Both CLI and GUI call this function
- Returns configured Agent instance

**process_query(agent, session, user_input)**:
- Core business logic for query processing
- Both CLI and GUI call this function
- Takes persistent agent as parameter
- Returns RunResult with agent response

### Benefits
- **50% token savings**: System prompt cached after first message
- **Reduced overhead**: Agent creation cost paid once
- **Proper memory**: Agent maintains context across session
- **Zero duplication**: CLI owns logic, GUI imports

## Testing Infrastructure

### CLI Regression Test Suite (PRIMARY)
- **File**: `test_cli_regression.sh`
- **Tests**: 38 comprehensive tests
- **Organization**:
  - SPY sequence (16 tests)
  - NVDA sequence (16 tests)
  - Multi-ticker sequence (6 tests)
- **Features**:
  - Persistent session (all 38 tests in SINGLE CLI session)
  - Single persistent agent for all tests
  - Agent persistence validation
  - Prompt caching validation
  - Chat history analysis validation
  - Response time tracking

### Latest Test Results
- **Total**: 38/38 PASSED (100%)
- **Average**: 11.05s (EXCELLENT)
- **Agent**: Single persistent agent for all tests ✅
- **Prompt Caching**: System prompt cached after first message ✅
- **Report**: `test-reports/test_cli_regression_loop1_2025-10-09_20-33.log`

## Performance Metrics

### Current Baseline
- **Average Response**: 11.05s (EXCELLENT)
- **Success Rate**: 100% (38/38 tests)
- **Token Savings**: 50% via persistent agent + prompt caching
- **Improvement**: 70% faster than legacy MCP (20s → 6-11s)

### Optimizations
- **Persistent Agent**: Created once, reused for all messages
- **Prompt Caching**: System prompt cached after first message
- **Direct APIs**: No MCP server overhead
- **Parallel Execution**: Multiple ticker queries executed concurrently
- **Simplified Frontend**: No custom components, 157 lines deleted

## Environment Setup

### Prerequisites
- **Python**: 3.12.3 (via uv)
- **Node.js**: 18.0.0+ (currently v24.6.0)
- **uv**: 0.8.19 (Python package manager)
- **npm**: 9.0.0+ (currently 11.6.0)

### Environment Variables (.env)
```
POLYGON_API_KEY=your_polygon_key
OPENAI_API_KEY=your_openai_key
FINNHUB_API_KEY=your_finnhub_key
```

### Installation
```bash
# Install all dependencies
npm install

# Install Python dependencies
uv install
```

## Deployment

### Development Servers
- **Backend**: http://127.0.0.1:8000 (persistent agent created at startup)
- **Frontend**: http://127.0.0.1:3000
- **API Docs**: http://127.0.0.1:8000/docs

### Startup Scripts
- `start-app-xterm.sh` - XTerm version (RECOMMENDED)
- `start-app.sh` - Main version (WSL2 compatible)
- Both create persistent agent at backend startup

## Important Files to Know

### Core Backend Files
- `src/backend/cli.py` - **MOST IMPORTANT**: Persistent agent functions
- `src/backend/main.py` - FastAPI app + lifespan (creates persistent agent)
- `src/backend/dependencies.py` - Dependency injection
- `src/backend/routers/chat.py` - Chat endpoint (calls CLI functions)
- `src/backend/services/agent_service.py` - Agent creation logic
- `src/backend/tools/polygon_tools.py` - 10 Polygon tools
- `src/backend/tools/finnhub_tools.py` - 1 Finnhub tool

### Configuration Files
- `.env` - API keys (not committed)
- `config/app.config.json` - Non-sensitive settings
- `pyproject.toml` - Python dependencies
- `package.json` - Node.js dependencies
- `.pylintrc` - Python linting config
- `.eslintrc.cjs` - JavaScript linting config

### Documentation
- `CLAUDE.md` - Project instructions for Claude Code
- `README.md` - User-facing documentation
- `.serena/memories/` - Serena knowledge base
- `docs/` - Additional documentation

### Testing
- `test_cli_regression.sh` - CLI test suite (38 tests)
- `test-reports/` - Test execution reports

## Serena Memories Available

**Most Critical Memories (Read These First)**:
- `tech_stack` - Technology stack and persistent agent architecture
- `project_architecture` - System architecture and agent lifecycle
- `ai_agent_instructions_oct_2025` - AI agent configuration and rules
- `code_style_conventions` - Coding standards
- `suggested_commands` - Development commands
- `git_commit_workflow` - Atomic commit workflow (CRITICAL)
- `task_completion_checklist` - Task completion steps

**Other Memories**:
- `adaptive_formatting_guide` - Lists vs tables formatting logic
- `testing_procedures` - Testing guidelines
- `performance_baseline_oct_2025` - Performance benchmarks
- `prompt_caching_guide` - OpenAI prompt caching details

## Key Design Principles

1. **CLI = Single Source of Truth** - CLI owns core logic, GUI imports
2. **Zero Code Duplication** - Never duplicate logic between CLI/GUI
3. **Persistent Agent** - ONE agent per lifecycle, not per message
4. **Token Efficiency** - Prompt caching enabled (50% savings)
5. **Direct APIs** - No MCP overhead (70% faster)
6. **Simplified Frontend** - Default rendering, no custom components
7. **Comprehensive Testing** - 38-test suite validates all functionality
8. **Atomic Commits** - Stage all files at once, commit immediately

## Next Steps for New Developers

1. **Read This Onboarding**: Understand project purpose and architecture
2. **Read Persistent Agent Docs**: `tech_stack.md`, `project_architecture.md`
3. **Read Git Workflow**: `.serena/memories/git_commit_workflow.md` (CRITICAL)
4. **Setup Environment**: Install dependencies, create .env file
5. **Run Tests**: `./test_cli_regression.sh` (validate setup)
6. **Start App**: `./start-app-xterm.sh` (see persistent agent in action)
7. **Read Code**: Start with `src/backend/cli.py` (core functions)

## Common Pitfalls to Avoid

❌ **DON'T**: Create agents for every message
✅ **DO**: Use persistent agent (initialize_persistent_agent)

❌ **DON'T**: Duplicate code between CLI and GUI
✅ **DO**: CLI owns logic, GUI imports

❌ **DON'T**: Stage files early during development
✅ **DO**: Stage ALL files at once, commit immediately

❌ **DON'T**: Skip testing before committing
✅ **DO**: Run test suite, show 100% pass rate

❌ **DON'T**: Commit without test reports
✅ **DO**: Include test reports in atomic commit

❌ **DON'T**: Use MCP tools
✅ **DO**: Use Direct API tools (Polygon, Finnhub)

## Recent Commits (Reference)

**Most Recent** (October 2025):
- `0baa0bf` - Persistent Agent Implementation + Comprehensive Documentation Audit
- `b866f0a` - Frontend Code Duplication Elimination (157 lines deleted)
- Previous - Direct API Migration (MCP removal, 70% performance improvement)

## Support & Resources

- **Test Suite**: `./test_cli_regression.sh`
- **Serena Memories**: `.serena/memories/`
- **Claude Code Docs**: `CLAUDE.md`
- **Architecture Docs**: `CORRECTED_ARCHITECTURE_RESEARCH.md`
- **API Docs**: http://127.0.0.1:8000/docs (when running)

---

**Last Updated**: October 2025 (Post-Persistent Agent Architecture)
**Status**: Production-ready with 100% test pass rate
**Performance**: EXCELLENT (11.05s average, 50% token savings)