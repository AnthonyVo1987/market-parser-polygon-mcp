# Project Onboarding Summary (October 2025 - Gradio-Only Frontend)

## Project Purpose

Market Parser is a Python CLI and Gradio web interface for natural language financial queries using:
- **Direct Tradier API** integration (5 tools, PRIMARY)
- **Direct Polygon API** integration (2 tools, FALLBACK)
- **OpenAI GPT-5-Nano** via OpenAI Agents SDK v0.2.9
- **Persistent Agent Architecture** (ONE agent per lifecycle, not per message)

**Key Value Proposition**:
- Natural language financial queries (e.g., "Tesla stock analysis", "SPY support and resistance")
- Real-time market data from Tradier and Polygon APIs
- AI-powered analysis using GPT-5-Nano
- Multiple interfaces: CLI, Gradio Web UI, REST API
- **50% token savings** via persistent agent and prompt caching

## Recent Major Architectural Changes (October 2025)

### 1. React Frontend Retirement (Oct 17, 2025) ⭐ **MOST RECENT**
**What Changed**: Completely removed React frontend (src/frontend/ directory)

**Impact**:
- Gradio (port 7860) is now the ONLY web interface
- Removed all TypeScript/JavaScript code
- Removed React dependencies from package.json
- Simplified architecture: Python-only frontend

**Benefit**: Zero frontend code duplication, simplified development

### 2. Persistent Agent Architecture ⭐ **CRITICAL**
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
Gradio = Wrapper (imports and calls CLI functions)
         ↓
  No code duplication
```

**Key Benefits**:
- 50% token savings via prompt caching (system prompt cached after first message)
- Reduced overhead (agent creation cost paid once)
- Proper agent memory (context across entire session)
- Zero code duplication between CLI and Gradio
- Best practices compliant (OpenAI recommended pattern)

**Files Involved**:
- `src/backend/cli.py` - Core functions (initialize_persistent_agent, process_query)
- `src/backend/main.py` - FastAPI lifespan creates agent via CLI function
- `src/backend/gradio_app.py` - Gradio UI calls CLI functions
- `src/backend/dependencies.py` - Dependency injection for shared resources

### 3. Performance Metrics Footer Consolidation (Oct 17, 2025)
- Deleted footer duplication from Gradio (~60 lines)
- Footer generated ONCE in CLI core
- Gradio receives complete response with footer included

### 4. Direct API Migration (70% Performance Improvement)
- Migrated ALL tools from MCP to Direct Python APIs
- Removed MCP server completely
- Performance: 20s → 9.67s average (70% faster)

## Tech Stack

### Backend
- **Language**: Python 3.12.3
- **Package Manager**: uv 0.8.19
- **Framework**: FastAPI (latest)
- **AI Integration**: OpenAI Agents SDK v0.2.9
- **AI Model**: GPT-5-Nano (EXCLUSIVE - 200K TPM)
- **Service Tier**: "default" (optimized for prototyping)
- **APIs**:
  - Tradier Direct API (5 tools, PRIMARY)
  - Polygon Direct API (polygon-api-client>=1.14.0) - 2 tools, FALLBACK
  - OpenAI Agents SDK (openai-agents==0.2.9)

### Frontend
- **Gradio**: ChatInterface (port 7860) ⭐ ONLY WEB INTERFACE
- **No React**: React frontend completely retired (Oct 17, 2025)
- **No TypeScript**: All TypeScript code removed
- **No Node.js frontend**: package.json used for backend tooling only
- **Python-only UI**: Gradio framework (Python-based)

### Development Tools
- **Python**: pylint, black, isort, mypy
- **Testing**: CLI regression suite (test_cli_regression.sh - 39 tests)
- **No JavaScript tooling**: No ESLint, Prettier, TypeScript compiler

## Project Structure

```
market-parser-polygon-mcp/
├── src/
│   └── backend/              # All application code
│       ├── main.py          # Main app + FastAPI lifespan (creates persistent agent)
│       ├── cli.py           # CLI + shared functions ⭐ SINGLE SOURCE OF TRUTH
│       ├── gradio_app.py    # Gradio web UI (wraps CLI core) ⭐ ONLY WEB UI
│       ├── dependencies.py  # Dependency injection (get_agent, get_session)
│       ├── routers/
│       │   └── chat.py      # Chat endpoint (calls CLI functions)
│       ├── services/
│       │   └── agent_service.py  # Agent creation logic
│       └── tools/
│           ├── tradier_tools.py  # 5 Tradier Direct API tools
│           └── polygon_tools.py  # 2 Polygon Direct API tools
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
├── package.json          # npm scripts (backend tooling only)
├── test_cli_regression.sh  # CLI test suite (39 tests)
└── start-gradio.sh       # Gradio UI startup script
```

**Note**: src/frontend/ directory has been completely removed. Gradio is the only web interface.

## Key Commands

### Application Startup (Recommended)
```bash
# Start Gradio web interface (port 7860)
uv run python src/backend/gradio_app.py

# Or start CLI only (creates persistent agent)
npm run backend:cli

# Or start FastAPI backend (for API access)
npm run backend:dev
```

### Testing
```bash
# Run CLI regression test suite (39 tests, persistent session)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Validates:
# - Agent persistence (single agent for all 39 tests)
# - Prompt caching (system prompt cached after first message)
# - 100% pass rate expected
# - Average response time: ~9.67s (EXCELLENT)
```

### Code Quality
```bash
# Lint Python only
npm run lint

# Lint with auto-fix
npm run lint:fix

# No TypeScript/JavaScript linting (React removed)
```

## Code Style & Conventions

### Python
- **Line Length**: 100 characters
- **Formatter**: black
- **Import Sorting**: isort (black profile)
- **Linter**: pylint
- **Type Hints**: Required for all function parameters and returns
- **Docstrings**: Required for complex functions (Google style)
- **Model**: GPT-5-Nano ONLY (no model selection, exclusive)

### Gradio UI
- **Framework**: Gradio ChatInterface
- **Pattern**: Wrapper around CLI core (NO duplication)
- **Style**: Python-only (no CSS/JavaScript)

### Architecture Patterns
- **CLI = Core, Gradio = Wrapper** (commit b866f0a pattern)
- **Zero Code Duplication**: CLI owns logic, Gradio imports
- **Persistent Agent**: ONE agent per lifecycle, not per message
- **Direct API Integration**: No MCP overhead

## Task Completion Checklist

When completing a task:

1. ✅ **Code Changes**: Implement requested changes
2. ✅ **Code Quality**: Run `npm run lint:fix` (Python only)
3. ✅ **Testing**: Run `./test_cli_regression.sh` (39 tests, must show 100% pass rate)
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

**Gradio Mode**:
```python
# Create agent ONCE at module load
gradio_session = SQLiteSession("gradio_session")
analysis_agent = initialize_persistent_agent()  # Import from cli.py

# Reuse agent for ALL user sessions
async def chat_with_agent(message, history):
    result = await process_query(analysis_agent, gradio_session, message)
    yield result
```

### Key Functions (src/backend/cli.py)

**initialize_persistent_agent()**:
- Single source of truth for agent creation
- Both CLI and Gradio call this function
- Returns configured Agent instance

**process_query(agent, session, user_input)**:
- Core business logic for query processing
- Both CLI and Gradio call this function
- Takes persistent agent as parameter
- Returns RunResult with agent response

### Benefits

- **50% token savings**: System prompt cached after first message
- **Reduced overhead**: Agent creation cost paid once
- **Proper memory**: Agent maintains context across session
- **Zero duplication**: CLI owns logic, Gradio imports

## Testing Infrastructure

### CLI Regression Test Suite (PRIMARY)
- **File**: `test_cli_regression.sh`
- **Tests**: 39 comprehensive tests
- **Organization**:
  - SPY sequence (17 tests)
  - NVDA sequence (17 tests)
  - Multi-ticker sequence (5 tests)
- **Features**:
  - Persistent session (all 39 tests in SINGLE CLI session)
  - Single persistent agent for all tests
  - Agent persistence validation
  - Prompt caching validation
  - Response time tracking

### Latest Test Results
- **Total**: 39/39 PASSED (100%)
- **Average**: 9.67s (EXCELLENT)
- **Agent**: Single persistent agent for all tests ✅
- **Prompt Caching**: System prompt cached after first message ✅
- **Report**: `test-reports/test_cli_regression_loop1_2025-10-17_17-58.log`

## Performance Metrics

### Current Baseline
- **Average Response**: 9.67s (EXCELLENT)
- **Success Rate**: 100% (39/39 tests)
- **Token Savings**: 50% via persistent agent + prompt caching
- **Improvement**: 70% faster than legacy MCP (20s → 9.67s)

### Optimizations
- **Persistent Agent**: Created once, reused for all messages
- **Prompt Caching**: System prompt cached after first message
- **Direct APIs**: No MCP server overhead
- **Parallel Execution**: Multiple ticker queries executed concurrently
- **Footer Consolidation**: Zero duplication across interfaces

## Environment Setup

### Prerequisites
- **Python**: 3.12.3 (via uv)
- **uv**: 0.8.19 (Python package manager)
- **No Node.js required**: package.json used for backend tooling only

### Environment Variables (.env)
```
TRADIER_API_KEY=your_tradier_key
POLYGON_API_KEY=your_polygon_key
OPENAI_API_KEY=your_openai_key
```

### Installation
```bash
# Install Python dependencies
uv install

# No npm install needed for frontend (Gradio is Python-based)
```

## Deployment

### Development Servers
- **Backend**: http://127.0.0.1:8000 (persistent agent created at startup)
- **Gradio UI**: http://127.0.0.1:7860 ⭐ PRIMARY WEB INTERFACE
- **API Docs**: http://127.0.0.1:8000/docs

### Startup Scripts
- `uv run python src/backend/gradio_app.py` - Gradio UI (RECOMMENDED)
- `npm run backend:cli` - CLI interface
- `npm run backend:dev` - FastAPI backend only

## Important Files to Know

### Core Backend Files
- `src/backend/cli.py` - **MOST IMPORTANT**: Persistent agent functions
- `src/backend/gradio_app.py` - Gradio web UI (wraps CLI core)
- `src/backend/main.py` - FastAPI app + lifespan (creates persistent agent)
- `src/backend/dependencies.py` - Dependency injection
- `src/backend/services/agent_service.py` - Agent creation logic
- `src/backend/tools/tradier_tools.py` - 5 Tradier tools (PRIMARY)
- `src/backend/tools/polygon_tools.py` - 2 Polygon tools (FALLBACK)

### Configuration Files
- `.env` - API keys (not committed)
- `config/app.config.json` - Non-sensitive settings
- `pyproject.toml` - Python dependencies
- `package.json` - npm scripts (backend tooling only)

### Documentation
- `CLAUDE.md` - Project instructions for Claude Code
- `README.md` - User-facing documentation
- `.serena/memories/` - Serena knowledge base
- `docs/` - Additional documentation

### Testing
- `test_cli_regression.sh` - CLI test suite (39 tests)
- `test-reports/` - Test execution reports

## Serena Memories Available

**Most Critical Memories (Read These First)**:
- `tech_stack` - Technology stack and persistent agent architecture
- `project_architecture` - System architecture and agent lifecycle
- `ai_agent_instructions_oct_2025` - AI agent configuration and rules
- `code_style_conventions` - Coding standards (Python-only)
- `suggested_commands` - Development commands
- `git_commit_workflow` - Atomic commit workflow (CRITICAL)
- `task_completion_checklist` - Task completion steps

**Other Memories**:
- `adaptive_formatting_guide` - Lists vs tables formatting logic
- `testing_procedures` - Testing guidelines
- `performance_baseline_oct_2025` - Performance benchmarks
- `prompt_caching_guide` - OpenAI prompt caching details

## Key Design Principles

1. **CLI = Single Source of Truth** - CLI owns core logic, Gradio imports
2. **Zero Code Duplication** - Never duplicate logic between CLI/Gradio
3. **Persistent Agent** - ONE agent per lifecycle, not per message
4. **Token Efficiency** - Prompt caching enabled (50% savings)
5. **Direct APIs** - No MCP overhead (70% faster)
6. **Gradio-Only Web UI** - React completely retired
7. **Python-First** - All UI code is Python (Gradio framework)
8. **Comprehensive Testing** - 39-test suite validates all functionality

## Next Steps for New Developers

1. **Read This Onboarding**: Understand project purpose and architecture
2. **Read Persistent Agent Docs**: `tech_stack.md`, `project_architecture.md`
3. **Read Git Workflow**: `.serena/memories/git_commit_workflow.md` (CRITICAL)
4. **Setup Environment**: Install dependencies, create .env file
5. **Run Tests**: `./test_cli_regression.sh` (validate setup)
6. **Start Gradio UI**: `uv run python src/backend/gradio_app.py` (see agent in action)
7. **Read Code**: Start with `src/backend/cli.py` (core functions)

## Common Pitfalls to Avoid

❌ **DON'T**: Create agents for every message
✅ **DO**: Use persistent agent (initialize_persistent_agent)

❌ **DON'T**: Duplicate code between CLI and Gradio
✅ **DO**: CLI owns logic, Gradio imports

❌ **DON'T**: Stage files early during development
✅ **DO**: Stage ALL files at once, commit immediately

❌ **DON'T**: Skip testing before committing
✅ **DO**: Run test suite, show 100% pass rate

❌ **DON'T**: Commit without test reports
✅ **DO**: Include test reports in atomic commit

❌ **DON'T**: Use MCP tools
✅ **DO**: Use Direct API tools (Tradier, Polygon)

❌ **DON'T**: Look for React frontend code
✅ **DO**: Use Gradio UI (Python-based)

## Recent Commits (Reference)

**Most Recent** (October 2025):
- React Frontend Retirement (Oct 17, 2025) - Gradio is now ONLY web interface
- Performance Metrics Footer Consolidation (Oct 17, 2025) - Zero duplication
- Persistent Agent Implementation (Oct 2025) - 50% token savings
- Direct API Migration (Oct 2025) - 70% performance improvement

## Support & Resources

- **Test Suite**: `./test_cli_regression.sh`
- **Serena Memories**: `.serena/memories/`
- **Claude Code Docs**: `CLAUDE.md`
- **API Docs**: http://127.0.0.1:8000/docs (when running)
- **Gradio UI**: http://127.0.0.1:7860 (when running)

---

**Last Updated**: October 17, 2025 (React Frontend Retirement)
**Status**: Production-ready with 100% test pass rate
**Architecture**: Gradio-only frontend, persistent agent, direct APIs
