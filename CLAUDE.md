# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural language financial queries using the Polygon.io MCP server and OpenAI GPT-5-nano via the Pydantic AI Agent Framework.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
**Serena Multi-Language Analysis & Configuration Optimization - Complete**

feat: configure Serena for Python primary language with comprehensive analysis

- Change .serena/project.yml from typescript to python language setting
- Research Serena multi-language support capabilities (not available)
- Analyze mission-critical functions: Python 100%, TypeScript 0%
- Update all Serena memory files with comprehensive analysis
- Document "Thin Client, Thick Server" architecture pattern
- Confirm Python tools work perfectly, TypeScript limitations acceptable

**Files Modified:**
- .serena/project.yml (language: python)
- .serena/memories/serena_quick_check.md (status update)
- .serena/memories/environment_sync_status.md (Serena tools status)
- .serena/memories/project_overview.md (Serena tools status)
- .serena/memories/serena_multi_language_analysis.md (research results)
- .serena/memories/serena_language_analysis_complete.md (comprehensive analysis)
- .serena/memories/serena_tools_final_status.md (final status)
- new_task_plan.md (original task documentation)

Status: Serena Multi-Language Analysis & Configuration Optimization ✅ COMPLETED
<!-- LAST_COMPLETED_TASK_END -->

## 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s)

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis
2. Use Context7 for research and best practices
3. Use Serena Tools for code analysis and manipulation
4. Use Filesystem Tools for batch operations and project management
5. Use Standard Read/Write/Edit for file modifications
6. Use Playwright Tools for testing and validation
7. REPEAT any tool as needed throughout the process
8. NEVER stop using tools - continue using them until task completion

SPECIFIC TOOL USAGE GUIDELINES:

**Serena Tools**: USE AS OFTEN AS NEEDED for Advanced code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications

**Sequential-Thinking Tools**: USE AS OFTEN AS NEEDED for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)

**Context7 Tools**: USE AS OFTEN AS NEEDED for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups

**Filesystem Tools**: USE AS OFTEN AS NEEDED for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications

**Standard Read/Write/Edit Tools**: USE AS OFTEN AS NEEDED for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management

**Playwright Tools**: USE AS OFTEN AS NEEDED for Testing with Browser automation for React GUI & App Validation

TOOL OVERLAP RESOLUTION:

- Filesystem Tools: Use for 3+ file operations, batch processing, project management, metadata analysis, comprehensive project operations
- Standard Read/Write/Edit: Use for single-file modifications, simple edits, direct file operations
- Serena Tools: Use for complex code analysis, symbol manipulation, pattern search with context
- When in doubt: Use Filesystem for batch/complex operations, Standard for simple single-file operations

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're failing
- If you don't use tools throughout the entire process, you're failing
- If you use wrong tool for the operation (e.g., Standard for batch operations), you're failing

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

## Quick Start

**One-Click Application Startup (Recommended):**

The startup scripts automatically START all development servers BUT **DOES NOT OPEN THE APP IN BROWSER AUTOMATICALLY**.

```bash
# Option 1: Main startup script (recommended)
./start-app.sh

# Option 2: XTerm version for better terminal compatibility
./start-app-xterm.sh

# Option 3: Use npm scripts
npm run start:app          # Main script
npm run start:app:xterm    # XTerm version
```

**Prerequisites:** uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (Main Script)

- **Terminal Support**: Tries `gnome-terminal` first, falls back to `xterm`
- **Cross-Platform**: Works on most Linux distributions and macOS
- **Automatic Fallback**: Gracefully handles missing terminal emulators

### start-app-xterm.sh (XTerm Version)

- **XTerm Focused**: Specifically designed for xterm users
- **Window Positioning**: Places backend and frontend terminals side-by-side
- **Font Configuration**: Uses readable DejaVu Sans Mono font
- **Enhanced Display**: Better window titles and layout

## What the Scripts Do

### 🔄 Server Cleanup

- Kills existing development servers (uvicorn, vite)
- **Preserves MCP servers** - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup

- **Backend**: Starts FastAPI server on `http://127.0.0.1:8000`
- **Frontend**: Starts Vite dev server on `http://127.0.0.1:3000`
- Opens each server in a separate terminal window for easy monitoring
- Uses consistent hard-coded ports (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies frontend serves content properly

### 🌐 Browser Launch

- **NOTIFIES USER TO LAUNCH BROWSER TO START THE APP**

**Access:** <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)

**Manual Setup:**

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

**Access:** Frontend at <http://127.0.0.1:3000>, Backend at <http://127.0.0.1:8000>

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

**CRITICAL**: Follow these mandatory protocols to prevent testing failures and ensure professional standards.

### Core Protocol Requirements

1. **User-Specified Test Plans Are Sacred**
   - NEVER substitute user-provided test procedures with AI-generated alternatives
   - Test plans must be followed exactly as specified, including sequence, messages, and steps
   - Deviating from specified procedures can invalidate results and mask critical issues

2. **Verification Before Execution**
   - Always confirm the exact test plan before beginning any testing phase
   - If test details are unclear due to context loss, ASK for clarification first
   - State what test plan will be executed and request confirmation

3. **Context Loss Handling**
   - When conversation compacting occurs, proactively request clarification on procedural details
   - Never assume "equivalent" procedures are acceptable
   - Professional testing requires exact adherence to specifications

4. **Testing Standards**
   - Test procedures have critical reasoning behind specific sequences and steps
   - Communication before action: ask when uncertain rather than assume
   - Document any deviations with explicit user approval

### Corrective Actions Applied

- **Mandatory Pre-Test Verification**: Confirm test plan details before execution
- **No Substitutions Policy**: User procedures must be followed exactly
- **Assumption Elimination**: Replace assumptions with verification requests
- **Professional Standards**: Recognize testing as critical validation requiring precision

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

**MCP Tools Testing Approach:**

- Playwright MCP Tools for browser automation and React GUI testing
- 3 core test validation: Market Status, NVDA Ticker, Stock Snapshot Button
- Comprehensive test coverage for all financial query scenarios
- See `/tests/playwright/mcp_test_script_basic.md` for testing procedures

## Prototyping Principles

**CRITICAL PROJECT STAGE NOTICE:** This project is currently in the prototyping stage. All development work must adhere to the following principles:

### Core Prototyping Requirements

- **Do NOT over-engineer ANYTHING** - Focus on functional prototypes, not perfect solutions
- **Prioritize functionality over optimization** - Get features working before making them efficient
- **Maintain prototype simplicity** - Avoid complex architectural patterns unless absolutely necessary

### NOT REQUIRED for Prototyping Stage

- **Enterprise Grade solutions** - Simple, functional implementations are preferred
- **Production Ready implementations** - Focus on demonstrating functionality
- **Performance Optimization** - Optimize only if performance blocks functionality
- **Comprehensive Testing** - Basic functional validation is sufficient
- **Test Scripts or Unit Tests** - Manual testing is acceptable for prototyping
- **CI/CD Pipeline implementation** - Basic git workflows are sufficient

### Prototyping Development Guidelines

- **Rapid iteration over perfect implementation** - Build, test, learn, iterate
- **Functional completeness over code quality** - Make it work first, refine later
- **Future scalability awareness without over-engineering** - Consider future needs but don't implement them yet
- **Documentation focused on usage, not internal architecture** - Help users understand what it does, not how it works internally

All AI Agents, Sub-Agents, & Agent Team Specialists development work must respect these prototyping constraints to maintain project momentum and avoid premature optimization.

## AI Team Configuration (autogenerated by team-configurator, 2025-09-18)

**Important: YOU MUST USE subagents when available for the task.**

### Detected Tech Stack

- **Backend**: Python 3.10+, FastAPI, OpenAI Agents SDK 0.2.8, Pydantic AI Agent Framework
- **Financial Integration**: Polygon.io MCP server, complex agent orchestration with guardrails
- **Frontend**: React 18.2+ (NOT React 19), TypeScript, Vite 5.2+, PWA capabilities
- **Architecture**: Multi-agent system, prompt templates, SQLite, caching, MCP integration
- **Testing**: Playwright MCP Tools exclusively, Fixed ports (8000/3000/5500)
- **Code Quality**: Black, isort, pylint, mypy (Python), ESLint, Prettier (TypeScript)

### Optimal Agent Team Assignment

| **Task Category** | **Agent** | **Specific Responsibilities** |
|-------------------|-----------|-------------------------------|
| **Multi-Step Feature Development** | `tech-lead-orchestrator` | Complex financial features, agent coordination, strategic planning |
| **Agent System Development** | `backend-developer` | FastAPI + Pydantic AI + OpenAI Agents SDK, guardrail system, prompt templates |
| **Financial Query Processing** | `backend-developer` | MCP integration, Polygon.io data handling, agent orchestration |
| **React Components & Architecture** | `react-component-architect` | React 18.2+ component design, hooks, modern patterns, financial UI components |
| **Playwright MCP Testing** | `frontend-developer` | MCP Playwright testing, test plan execution, browser automation per `/tests/playwright/mcp_test_script_basic.md` |
| **API Design & Integration** | `api-architect` | REST endpoints, Polygon.io MCP server design, data contracts |
| **Performance & Optimization** | `performance-optimizer` | Real-time financial data processing, agent efficiency, response times |
| **Code Quality & Security** | `code-reviewer` | Security-aware reviews, financial data handling, maintainability |
| **Architecture Documentation** | `documentation-specialist` | Complex agent system documentation, architectural decisions |

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
@documentation-specialist document the agent orchestration architecture and MCP integration patterns
