# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural language financial queries using the Polygon.io MCP server and OpenAI GPT-5-nano via the Pydantic AI Agent Framework.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
feat: Complete Phase 5: UI Testing & Validation Execution

- Executed comprehensive UI validation test plan using Playwright Backup Tools with 30-second polling intervals
- Followed exact 53-step test plan from docs/implementation_plans/UI_audit_fixes_Phase_5_Test_Plan.md
- Test execution revealed critical React application loading failure with 500 Internal Server Error
- Generated comprehensive test report: test-reports/UI_Phase_5_Test_Report__25-09-21_14-29.md
- Documented complete test failure due to application loading issues preventing UI validation
- Test report includes: execution summary, individual test results, performance classifications, UI validation summary
- Identified primary issue: React application not rendering due to 500 errors in console
- Documented secondary issues: input field selector not found, no visible content, all UI tests failed
- Report follows exact template format with proper timestamps and comprehensive failure analysis
- All UI phases (1-4) could not be validated due to application loading failure
- Provided detailed next steps: fix React loading issue, verify frontend build, re-run tests after fixes
- Test execution completed exactly as specified without attempting to fix identified issues
- Report ready for user review and issue resolution in separate task

Phase 5 delivers comprehensive test execution documentation and failure analysis for UI validation testing.
<!-- LAST_COMPLETED_TASK_END -->

## 🔴 CRITICAL: YOU MUST ALWAYS USE THESE TOOLS FIRST in any particular order to perform all task(s)

- __Serena Tools__: Use for Advanced code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
- __Sequential-Thinking Tools__: Use for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
- __Context7 Tools__: Use for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups
- __Filesystem Tools__: Use for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
- __Standard Read/Write/Edit Tools__: Use for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
- __Playwright Tools__: Use for Testing with Browser automation for React GUI & App Validation

## Quick Start

__One-Click Application Startup (Recommended):__

The startup scripts automatically START all development servers BUT __DOES NOT OPEN THE APP IN BROWSER AUTOMATICALLY__.

```bash
# Option 1: Main startup script (recommended)
./start-app.sh

# Option 2: XTerm version for better terminal compatibility
./start-app-xterm.sh

# Option 3: Use npm scripts
npm run start:app          # Main script
npm run start:app:xterm    # XTerm version
```

__Prerequisites:__ uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (Main Script)

- __Terminal Support__: Tries `gnome-terminal` first, falls back to `xterm`
- __Cross-Platform__: Works on most Linux distributions and macOS
- __Automatic Fallback__: Gracefully handles missing terminal emulators

### start-app-xterm.sh (XTerm Version)

- __XTerm Focused__: Specifically designed for xterm users
- __Window Positioning__: Places backend and frontend terminals side-by-side
- __Font Configuration__: Uses readable DejaVu Sans Mono font
- __Enhanced Display__: Better window titles and layout

## What the Scripts Do

### 🔄 Server Cleanup

- Kills existing development servers (uvicorn, vite)
- __Preserves MCP servers__ - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup

- __Backend__: Starts FastAPI server on `http://127.0.0.1:8000`
- __Frontend__: Starts Vite dev server on `http://127.0.0.1:3000`
- Opens each server in a separate terminal window for easy monitoring
- Uses consistent hard-coded ports (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies frontend serves content properly

### 🌐 Browser Launch

- __NOTIFIES USER TO LAUNCH BROWSER TO START THE APP__

__Access:__ <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)

__Manual Setup:__

```bash
# 1. Environment setup
cp .env.example .env
# Add POLYGON_API_KEY and OPENAI_API_KEY to .env

# 2. Install dependencies
uv install
npm install

# 3. Start servers (2 terminals)
# Terminal 1: Backend
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend
npm run frontend:dev
```

__Access:__ Frontend at <http://127.0.0.1:3000>, Backend at <http://127.0.0.1:8000>

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

### Testing

Testing with Playwright MCP Tools only - see `/tests/playwright/mcp_test_script_basic.md`

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

### Health & Status

```bash
# Health checks
npm run status               # Check backend/frontend health
npm run health              # Alias for status

# Application status
curl http://localhost:8000/health     # Backend health endpoint
curl http://localhost:3000           # Frontend availability
```

### PWA Testing

```bash
# PWA functionality testing
npm run test:pwa            # Development PWA build + instructions
npm run test:pwa:staging    # Staging PWA build + instructions
npm run test:pwa:production # Production PWA build + instructions
```

### Cross-Device & Network Testing

```bash
# Cross-device testing setup
npm run cross-device:setup     # Production build + network access instructions
npm run cross-device:staging   # Staging build + network access instructions

# Live Server configuration help
npm run live-server:help       # Live Server setup and configuration guide
```

### Maintenance & Cleanup

```bash
# Cleanup commands
npm run clean               # Remove node_modules and dist
npm run clean:cache         # Remove cache directories
npm run clean:full          # Full cleanup + reinstall
npm run reset              # Clean + reinstall + start dev

# Installation
npm run install:all         # Install all dependencies
npm run install:backend     # Install Python dependencies only
```

## Testing Protocol Guidelines

__CRITICAL__: Follow these mandatory protocols to prevent testing failures and ensure professional standards.

### Core Protocol Requirements

1. __User-Specified Test Plans Are Sacred__
   - NEVER substitute user-provided test procedures with AI-generated alternatives
   - Test plans must be followed exactly as specified, including sequence, messages, and steps
   - Deviating from specified procedures can invalidate results and mask critical issues

2. __Verification Before Execution__
   - Always confirm the exact test plan before beginning any testing phase
   - If test details are unclear due to context loss, ASK for clarification first
   - State what test plan will be executed and request confirmation

3. __Context Loss Handling__
   - When conversation compacting occurs, proactively request clarification on procedural details
   - Never assume "equivalent" procedures are acceptable
   - Professional testing requires exact adherence to specifications

4. __Testing Standards__
   - Test procedures have critical reasoning behind specific sequences and steps
   - Communication before action: ask when uncertain rather than assume
   - Document any deviations with explicit user approval

### Corrective Actions Applied

- __Mandatory Pre-Test Verification__: Confirm test plan details before execution
- __No Substitutions Policy__: User procedures must be followed exactly
- __Assumption Elimination__: Replace assumptions with verification requests
- __Professional Standards__: Recognize testing as critical validation requiring precision

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

1. __MCP Server Factory Pattern__ (`src/backend/main.py:42`)
   - Creates stdio MCP server with Polygon.io API integration
   - Manages server lifecycle with FastAPI lifespan events
   - Shared server instance across all API requests

2. __Financial Guardrail System__
   - Two-agent architecture: guardrail agent + analysis agent
   - Guardrail validates finance-related queries before processing
   - Prevents non-financial queries from consuming API resources

3. __Unified Response Processing__
   - All responses use conversational format (no JSON extraction)
   - Emoji-based sentiment indicators (📈 bullish, 📉 bearish)
   - Structured format: KEY TAKEAWAYS → DETAILED ANALYSIS → DISCLAIMER

### Prompt Template System

The prompt management system (`src/backend/prompt_templates.py`) provides:

1. __Template Types__: Snapshot, Support/Resistance, Technical Analysis
2. __Ticker Extraction__: Smart detection from company names and context
3. __Conversation Context__: Maintains ticker history across chat sessions
4. __Unified Conversational Mode__: All templates generate natural language responses

### FastAPI Backend Architecture

The backend (`src/backend/main.py`) features:

1. __Hard-coded Configuration__: Ports and hosts are fixed (127.0.0.1:8000)
2. __Shared Resources__: Single MCP server and SQLite session across requests
3. __Multiple API Versions__: Legacy endpoints + v1 API for compatibility
4. __CORS Support__: Dynamic configuration for frontend integration

### React Frontend Integration

The frontend communicates with the backend via:

1. __RESTful API__: Chat endpoint + analysis endpoints
2. __Fixed Ports__: Backend on 8000, frontend dev on 3000, production on 5500
3. __One-click Startup__: `start-app.sh` manages both servers automatically

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

# Logging configuration (default for performance)
LOG_MODE=NONE

# Optional pricing (USD per 1M tokens)
OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25
OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00
```

Server configuration is hard-coded (not configurable via environment):

- Backend: 127.0.0.1:8000
- Frontend Dev: 127.0.0.1:3000
- Frontend Production: 127.0.0.1:5500 (Live Server)

## Project Structure

```text
market-parser-polygon-mcp/
├── src/backend/           # FastAPI backend
│   ├── main.py           # Main FastAPI app with agent system
│   ├── api_models.py     # Pydantic models for API
│   ├── prompt_templates.py # Prompt generation system
│   └── utils/            # Logging and utilities
├── src/frontend/         # React frontend
│   ├── components/       # React components
│   └── hooks/           # Custom React hooks
├── tests/playwright/     # MCP testing documentation and scripts
├── start-app.sh         # One-click startup script
└── .env                 # Environment configuration
```

## Testing Strategy

The project uses Playwright MCP Tools for E2E testing - the ONLY testing method:

__MCP Tools Testing Approach:__

- Playwright MCP Tools for browser automation and React GUI testing
- 3 core test validation: Market Status, NVDA Ticker, Stock Snapshot Button
- Comprehensive test coverage for all financial query scenarios
- See `/tests/playwright/mcp_test_script_basic.md` for testing procedures

## Prototyping Principles

__CRITICAL PROJECT STAGE NOTICE:__ This project is currently in the prototyping stage. All development work must adhere to the following principles:

### Core Prototyping Requirements

- __Do NOT over-engineer ANYTHING__ - Focus on functional prototypes, not perfect solutions
- __Prioritize functionality over optimization__ - Get features working before making them efficient
- __Maintain prototype simplicity__ - Avoid complex architectural patterns unless absolutely necessary

### NOT REQUIRED for Prototyping Stage

- __Enterprise Grade solutions__ - Simple, functional implementations are preferred
- __Production Ready implementations__ - Focus on demonstrating functionality
- __Performance Optimization__ - Optimize only if performance blocks functionality
- __Comprehensive Testing__ - Basic functional validation is sufficient
- __Test Scripts or Unit Tests__ - Manual testing is acceptable for prototyping
- __CI/CD Pipeline implementation__ - Basic git workflows are sufficient

### Prototyping Development Guidelines

- __Rapid iteration over perfect implementation__ - Build, test, learn, iterate
- __Functional completeness over code quality__ - Make it work first, refine later
- __Future scalability awareness without over-engineering__ - Consider future needs but don't implement them yet
- __Documentation focused on usage, not internal architecture__ - Help users understand what it does, not how it works internally

All AI Agents, Sub-Agents, & Agent Team Specialists development work must respect these prototyping constraints to maintain project momentum and avoid premature optimization.

## AI Team Configuration (autogenerated by team-configurator, 2025-09-18)

__Important: YOU MUST USE subagents when available for the task.__

### Detected Tech Stack

- __Backend__: Python 3.10+, FastAPI, OpenAI Agents SDK 0.2.8, Pydantic AI Agent Framework
- __Financial Integration__: Polygon.io MCP server, complex agent orchestration with guardrails
- __Frontend__: React 18.2+ (NOT React 19), TypeScript, Vite 5.2+, PWA capabilities
- __Architecture__: Multi-agent system, prompt templates, SQLite, caching, MCP integration
- __Testing__: Playwright MCP Tools exclusively, Fixed ports (8000/3000/5500)
- __Code Quality__: Black, isort, pylint, mypy (Python), ESLint, Prettier (TypeScript)

### Optimal Agent Team Assignment

| __Task Category__ | __Agent__ | __Specific Responsibilities__ |
|-------------------|-----------|-------------------------------|
| __Multi-Step Feature Development__ | `tech-lead-orchestrator` | Complex financial features, agent coordination, strategic planning |
| __Agent System Development__ | `backend-developer` | FastAPI + Pydantic AI + OpenAI Agents SDK, guardrail system, prompt templates |
| __Financial Query Processing__ | `backend-developer` | MCP integration, Polygon.io data handling, agent orchestration |
| __React Components & Architecture__ | `react-component-architect` | React 18.2+ component design, hooks, modern patterns, financial UI components |
| __Playwright MCP Testing__ | `frontend-developer` | MCP Playwright testing, test plan execution, browser automation per `/tests/playwright/mcp_test_script_basic.md` |
| __API Design & Integration__ | `api-architect` | REST endpoints, Polygon.io MCP server design, data contracts |
| __Performance & Optimization__ | `performance-optimizer` | Real-time financial data processing, agent efficiency, response times |
| __Code Quality & Security__ | `code-reviewer` | Security-aware reviews, financial data handling, maintainability |
| __Architecture Documentation__ | `documentation-specialist` | Complex agent system documentation, architectural decisions |

### Sample Usage Commands

```bash
# Multi-step feature development
@tech-lead-orchestrator plan and coordinate implementation of a comprehensive portfolio tracking feature

# Backend development
@backend-developer implement a new financial analysis endpoint using the existing agent framework

# React component development
@react-component-architect create a new stock chart component using modern React 18.2+ patterns

# Playwright MCP testing
@frontend-developer execute the MCP test plan in /tests/playwright/mcp_test_script_basic.md

# API design
@api-architect design a new endpoint for portfolio analysis with proper error handling

# Performance optimization
@performance-optimizer analyze and improve the financial query processing pipeline

# Code review
@code-reviewer review the recent changes to the agent system for security and best practices

# Documentation
@documentation-specialist document the agent orchestration architecture and MCP integration patterns``

