# Market Parser Project Overview

## Purpose
Market Parser is a Python CLI and React web application for natural language financial queries using the Polygon.io MCP server and OpenAI GPT-5-mini via the Pydantic AI Agent Framework. Features intelligent sentiment analysis, real-time financial data, and cross-platform interfaces.

## Tech Stack

### Backend
- **Python 3.10+** with uv package manager
- **FastAPI** for REST API server
- **OpenAI Agents SDK 0.2.8** with Pydantic AI Agent Framework
- **Polygon.io MCP server** for financial data integration
- **SQLite** for session management
- **Black, isort, pylint, mypy** for code quality

### Frontend
- **React 18.2+** (NOT React 19) with TypeScript
- **Vite 5.2+** for build tooling
- **PWA capabilities** with service worker
- **ESLint, Prettier** for code quality

### Architecture
- **Multi-agent system** with guardrail agent + analysis agent
- **Prompt templates** for financial query processing
- **MCP integration** for real-time financial data
- **Fixed ports**: Backend (8000), Frontend Dev (3000), Production (5500)

## Project Stage
**CRITICAL**: This is a prototyping stage project. Focus on functionality over optimization, avoid over-engineering.

## Key Commands
- **One-click startup**: `./start-app.sh` or `npm run start:app`
- **Development**: `npm run dev`
- **Testing**: Playwright MCP Tools only (see `/tests/playwright/mcp_test_script_basic.md`)
- **Code Quality**: `npm run lint`, `npm run format`, `npm run type-check`