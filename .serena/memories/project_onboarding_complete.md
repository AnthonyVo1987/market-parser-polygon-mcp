# Market Parser Project - Onboarding Complete

## Project Purpose

Market Parser is a Python CLI and React web application for natural language financial queries using the Polygon.io MCP server and OpenAI GPT-5 models via the OpenAI Agents SDK v0.2.9. The application provides intelligent sentiment analysis, real-time financial data, cross-platform interfaces, optimized AI prompts with direct analysis buttons, and enhanced performance with GPT-5 model-specific rate limiting and quick response optimization for faster financial insights.

## Tech Stack

### Backend

- **Python 3.11+** with FastAPI framework
- **OpenAI Agents SDK v0.2.9** for AI integration
- **Polygon.io MCP server v0.4.1** for financial data
- **Pydantic** for data validation
- **SQLite** for session management and caching
- **Rich** for CLI formatting
- **Uvicorn** as ASGI server

### Frontend

- **React 18.2+** with TypeScript
- **Vite 5.2+** as build tool
- **Tailwind CSS** for styling
- **React Markdown** for content rendering
- **PWA support** with service workers

### AI Integration

- **OpenAI GPT-5 Nano** (200K TPM) and **GPT-5 Mini** (500K TPM)
- **Model-specific rate limiting** to prevent errors
- **Quick response optimization** with minimal tool calls
- **Temperature setting of 0.2** for deterministic analysis

### Development Tools

- **uv** for Python package management
- **npm** for Node.js package management
- **PyLint, Black, isort** for Python code quality
- **ESLint, Prettier** for TypeScript/JavaScript code quality
- **Playwright** for E2E testing
- **Lighthouse CI** for performance testing

## Code Style and Conventions

### Python (Backend)

- **Line length**: 100 characters (Black configuration)
- **Import sorting**: isort with Black profile
- **Type hints**: Gradual adoption with mypy
- **Docstrings**: Not required (disabled in PyLint)
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Good names**: i,j,k,ex,Run,_,id,db,ai,ui,os,df,dt,fs,app,uv,mcp,ctx,api

### TypeScript/JavaScript (Frontend)

- **Line length**: 80 characters (Prettier configuration)
- **Quotes**: Single quotes preferred
- **Semicolons**: Required
- **JSX**: Single quotes for attributes
- **Type safety**: Strict TypeScript with gradual adoption
- **React**: Functional components with hooks
- **Import organization**: TypeScript resolver handles imports

## Project Structure

```
src/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application entry point
│   ├── api_models.py    # Pydantic models for API
│   ├── prompt_templates.py # AI prompt templates
│   ├── direct_prompts.py # Direct prompt management
│   ├── optimized_agent_instructions.py # GPT-5 optimizations
│   └── utils/           # Utility functions
├── frontend/            # React frontend
│   ├── components/      # React components
│   ├── hooks/          # Custom React hooks
│   ├── services/       # API services
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Frontend utilities
│   ├── config/         # Configuration loader
│   └── styles/         # CSS styles
config/
└── app.config.json     # Centralized configuration
tests/
├── playwright/         # E2E test suite
├── unit/              # Unit tests
├── integration/       # Integration tests
└── mcp/              # MCP-specific tests
```

## Key Commands

### Application Startup

- `./start-app.sh` - One-click startup (recommended)
- `./start-app-xterm.sh` - XTerm version for better compatibility
- `npm run start:app` - npm script version

### Development

- `npm run dev` - Start both backend and frontend
- `npm run backend:dev` - Backend only (FastAPI with reload)
- `npm run frontend:dev` - Frontend only (Vite dev server)

### Code Quality

- `npm run lint` - Run all linting (Python + TypeScript)
- `npm run lint:fix` - Fix linting issues automatically
- `npm run format` - Format TypeScript/JavaScript code
- `npm run type-check` - TypeScript type checking

### Testing

- `npm run test:perf:all` - Run all performance tests
- `npm run lighthouse` - Run Lighthouse CI tests
- Use standardized test prompts from `tests/playwright/test_prompts.md`

### Build and Deploy

- `npm run build` - Production build
- `npm run build:staging` - Staging build
- `npm run build:development` - Development build

## System Commands (Linux)

- `git` - Version control
- `ls`, `cd`, `pwd` - File system navigation
- `grep`, `find` - Text and file searching
- `curl` - HTTP requests for testing
- `ps`, `pkill` - Process management
- `netstat` - Network connections
- `uv` - Python package management
- `npm` - Node.js package management

## Design Patterns and Guidelines

### Backend Architecture

- **FastAPI** with async/await patterns
- **Pydantic models** for data validation
- **Dependency injection** for services
- **Middleware** for request/response processing
- **Caching** with cachetools for performance
- **Rate limiting** with model-specific limits

### Frontend Architecture

- **React functional components** with hooks
- **Custom hooks** for reusable logic
- **Service layer** for API communication
- **TypeScript interfaces** for type safety
- **PWA architecture** with service workers
- **Responsive design** with Tailwind CSS

### AI Integration Patterns

- **Agent-based architecture** with OpenAI Agents SDK
- **Prompt optimization** for token efficiency
- **Model selection** based on request complexity
- **Error handling** with graceful degradation
- **Performance monitoring** with response timing

## Performance Optimizations

- **Quick response system** with minimal tool calls
- **Model-specific rate limiting** (200K TPM nano, 500K TPM mini)
- **Caching** for repeated requests
- **Bundle optimization** with Vite
- **Core Web Vitals** optimization (FCP: 256ms, LCP: <500ms)
- **Memory optimization** (13.8MB heap size)

## Configuration Management

- **Centralized config** in `config/app.config.json`
- **Environment variables** in `.env` (API keys only)
- **Model configuration** with rate limiting
- **CORS settings** for cross-origin requests
- **Logging configuration** with DEBUG mode

## Testing Strategy

- **Standardized test prompts** for consistent testing
- **Playwright E2E tests** for user workflows
- **Performance testing** with Lighthouse CI
- **Unit tests** for individual components
- **Integration tests** for API endpoints
- **Quick response testing** (20-45 second targets)

## Security Considerations

- **API key management** in environment variables
- **Rate limiting** to prevent abuse
- **CORS configuration** for secure cross-origin requests
- **Input validation** with Pydantic models
- **Error handling** without exposing sensitive information

## Deployment

- **Fixed ports** (8000 for backend, 3000 for frontend)
- **One-click startup** scripts for development
- **Production builds** with optimization
- **PWA support** for offline functionality
- **Cross-platform compatibility** (Linux, macOS, Windows)
