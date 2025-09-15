# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural language financial queries using the Polygon.io MCP server and OpenAI GPT-5-mini via the Pydantic AI Agent Framework.

## Development Commands

### Running the Application

```bash
# One-click startup (recommended)
npm run start:app

# Backend only (FastAPI server)
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload

# Frontend development
npm run frontend:dev

# CLI interface
uv run src/backend/main.py

# Alternative CLI
uv run market_parser_demo.py

# Gradio web interface
uv run chat_ui.py
```

### Testing

```bash
# Playwright E2E tests (B001-B016 test suite)
cd tests/playwright
npx playwright test

# Specific test
npx playwright test test-b001-market-status.spec.ts

# With browser visible
npx playwright test --headed
```

### Code Quality

```bash
# Linting
npm run lint           # All linting
npm run lint:python    # Python only
npm run lint:js        # JavaScript/TypeScript only

# Auto-fix
npm run lint:fix       # Fix all
npm run format         # Format JS/TS code

# Type checking
npm run type-check
```

### Build & Production

```bash
# Production build
npm run build

# Serve production build
npm run serve

# Bundle analysis
npm run analyze
```

## High-Level Architecture

### Agent System with MCP Server Integration

The core architecture uses the OpenAI Agents SDK with Polygon.io MCP server for financial data:

1. **MCP Server Factory Pattern** (`src/backend/main.py:42`)
   - Creates stdio MCP server with Polygon.io API integration
   - Manages server lifecycle with FastAPI lifespan events
   - Shared server instance across all API requests

2. **Financial Guardrail System**
   - Two-agent architecture: guardrail agent + analysis agent
   - Guardrail validates finance-related queries before processing
   - Prevents non-financial queries from consuming API resources

3. **Unified Response Processing**
   - All responses use conversational format (no JSON extraction)
   - Emoji-based sentiment indicators (📈 bullish, 📉 bearish)
   - Structured format: KEY TAKEAWAYS → DETAILED ANALYSIS → DISCLAIMER

### Prompt Template System

The prompt management system (`src/backend/prompt_templates.py`) provides:

1. **Template Types**: Snapshot, Support/Resistance, Technical Analysis
2. **Ticker Extraction**: Smart detection from company names and context
3. **Conversation Context**: Maintains ticker history across chat sessions
4. **Unified Conversational Mode**: All templates generate natural language responses

### FastAPI Backend Architecture

The backend (`src/backend/main.py`) features:

1. **Hard-coded Configuration**: Ports and hosts are fixed (127.0.0.1:8000)
2. **Shared Resources**: Single MCP server and SQLite session across requests
3. **Multiple API Versions**: Legacy endpoints + v1 API for compatibility
4. **CORS Support**: Dynamic configuration for frontend integration

### React Frontend Integration

The frontend communicates with the backend via:

1. **RESTful API**: Chat endpoint + analysis endpoints
2. **Fixed Ports**: Backend on 8000, frontend dev on 3000, production on 5500
3. **One-click Startup**: `start-app.sh` manages both servers automatically

## Key Architectural Patterns

### Agent Processing Pipeline

```python
# Simplified flow in process_financial_query()
1. Input validation & sanitization
2. Guardrail check (finance validation)
3. Agent processing with MCP tools
4. Response formatting with emojis
5. Error handling with typed responses
```

### Prompt Template Architecture

```python
# Template generation flow
TickerExtractor.extract_ticker() → TickerContext
PromptTemplate.generate_prompt() → formatted prompt
ResponseManager.process() → conversational response
```

### FastAPI Lifespan Management

```python
# Shared resource initialization
async with lifespan(app):
    shared_mcp_server = create_polygon_mcp_server()
    shared_session = SQLiteSession()
    # All requests use these shared instances
```

## Environment Configuration

Required environment variables (in `.env`):

```bash
# Required API keys
POLYGON_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Optional pricing (USD per 1M tokens)
OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25
OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00
```

Server configuration is hard-coded (not configurable via environment):
- Backend: 127.0.0.1:8000
- Frontend Dev: 127.0.0.1:3000
- Frontend Production: 127.0.0.1:5500

## Project Structure

```
market-parser-polygon-mcp/
├── src/backend/           # FastAPI backend
│   ├── main.py           # Main FastAPI app with agent system
│   ├── api_models.py     # Pydantic models for API
│   ├── prompt_templates.py # Prompt generation system
│   └── utils/            # Logging and utilities
├── src/frontend/         # React frontend
│   ├── components/       # React components
│   └── hooks/           # Custom React hooks
├── tests/playwright/     # E2E test suite (B001-B016)
├── start-app.sh         # One-click startup script
└── .env                 # Environment configuration
```

## Testing Strategy

The project uses Playwright for E2E testing with a comprehensive B001-B016 test suite covering:
- Market status queries
- Individual stock analysis
- Multi-ticker queries
- Button interactions
- Error handling
- Performance validation

## Prototyping Principles

This project is in prototyping stage. Focus on:
- Functional prototypes over perfect solutions
- Getting features working before optimization
- Rapid iteration and testing
- Simple, maintainable code

Avoid:
- Over-engineering
- Premature optimization
- Complex architectural patterns
- Comprehensive unit testing (E2E tests are sufficient)

## MCP Tools Usage

When working with MCP tools, prioritize:
1. **Playwright MCP**: Browser automation for React testing
2. **Filesystem MCP**: Multi-file operations (3+ files)
3. **Context7 MCP**: Library documentation lookups
4. **Sequential-Thinking MCP**: Complex problem analysis (max 8 thoughts)

Use standard Read/Write/Edit tools for single-file operations.

## AI Team Configuration

**IMPORTANT:** For any non-trivial multi-step task, feature implementation, or architectural decision, you MUST use the appropriate specialist subagent from the team below. This ensures optimal code quality, security, and maintainability for the Market Parser financial application.

### Detected Tech Stack

**Backend:**
- Python 3.10+, FastAPI, OpenAI Agents SDK 0.2.8, Pydantic AI Agent Framework
- SQLite, UV package manager, Polygon.io MCP server integration
- Code quality: Black, isort, pylint, mypy

**Frontend:**
- React 18.2+, TypeScript, Vite 5.2+, PWA capabilities
- Code quality: ESLint, Prettier
- Build: Vite with React plugin, npm scripts

**Testing & Development:**
- Playwright E2E test suite (B001-B016), Fixed ports (8000/3000/5500)
- Git workflow, One-click startup scripts

### Optimal Agent Team Assignment

| **Task Category** | **Agent** | **Specific Responsibilities** |
|-------------------|-----------|------------------------------|
| **Agent System Development** | `backend-developer` | FastAPI + Pydantic AI + OpenAI Agents SDK, guardrail system, prompt templates |
| **Financial Query Processing** | `backend-developer` | MCP integration, Polygon.io data handling, agent orchestration |
| **React Components & UI** | `react-component-architect` | Modern React 18.2+ patterns, hooks, PWA features, financial dashboards |
| **API Design & Integration** | `api-architect` | REST endpoints, Polygon.io MCP server design, data contracts |
| **Performance & Optimization** | `performance-optimizer` | Real-time financial data processing, agent efficiency, response times |
| **Code Quality & Security** | `code-reviewer` | Security-aware reviews, financial data handling, maintainability |

### Sample Usage Commands

```bash
# Backend development
@backend-developer implement a new financial analysis endpoint using the existing agent framework

# Frontend development
@react-component-architect create a new stock chart component with real-time updates

# API design
@api-architect design a new endpoint for portfolio analysis with proper error handling

# Performance optimization
@performance-optimizer analyze and improve the financial query processing pipeline

# Code review
@code-reviewer review the recent changes to the agent system for security and best practices
```

**Note:** This configuration balances the financial domain requirements, prototyping focus, and complex tech stack while ensuring comprehensive coverage of both backend agent development and modern React frontend work.