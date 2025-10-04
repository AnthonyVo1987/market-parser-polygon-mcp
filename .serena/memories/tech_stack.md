# Technology Stack

## Overview

Market Parser is built with a modern full-stack architecture combining Python backend services with a React TypeScript frontend, integrated with AI and financial data APIs.

## Backend Technology Stack

### Core Framework
- **FastAPI** (latest): Modern Python web framework
  - Async/await support
  - Automatic OpenAPI documentation
  - Pydantic integration for validation
  - High performance ASGI framework

- **Uvicorn** (with [standard] extras): ASGI server
  - Production-grade server
  - Hot reload in development
  - WebSocket support
  - HTTP/2 support

### AI & Agent Framework
- **OpenAI Agents SDK v0.2.9**: Official OpenAI agent framework
  - Agent-based workflow orchestration
  - Tool calling capabilities
  - Session management
  - SQLite session persistence

- **OpenAI API** (>=1.99.0, <1.100.0): OpenAI API client
  - GPT-5-Nano model access (exclusive)
  - Streaming support
  - Function calling

### MCP Integration
- **openai-agents-mcp** (>=0.0.8): MCP server integration
  - Polygon.io MCP server connection
  - Financial data tool access
  - Agent tool orchestration

### Data Validation & Models
- **Pydantic** (latest): Data validation library
  - Request/response validation
  - Type safety
  - Serialization/deserialization
  - Settings management

### Utilities & Helpers
- **Rich**: Terminal formatting and console output
  - Pretty printing
  - Progress bars
  - Syntax highlighting
  - Tables and panels

- **python-dotenv**: Environment variable management
  - .env file loading
  - Configuration management

- **aiofiles** (>=24.1.0): Async file I/O
  - Non-blocking file operations
  - Better performance for I/O-bound tasks

### Language Server
- **python-lsp-server[all]** (>=1.13.1): Python LSP for IDE support
  - Code completion
  - Linting integration
  - Type checking support

### Development Tools (Python)

**Linting & Formatting:**
- **pylint** (>=3.0.0): Code linter
  - Style enforcement
  - Error detection
  - Code quality metrics

- **black** (>=23.12.0): Code formatter
  - Opinionated formatting
  - 100-character line length
  - Consistent style

- **isort** (>=5.13.0): Import sorting
  - Black-compatible profile
  - Automatic import organization

**Type Checking:**
- **mypy** (>=1.7.0): Static type checker
  - Type hint validation
  - Gradual typing support
  - Error detection

**Testing:**
- **pytest** (>=7.4.0): Testing framework
  - Unit testing
  - Fixtures support
  - Plugin ecosystem

### Python Version Requirements
- **Python**: >=3.10
- **Package Manager**: uv (latest)
  - Fast dependency resolution
  - Lock file management
  - Virtual environment management

## Frontend Technology Stack

### Core Framework
- **React** (18.2.0): UI library
  - Functional components
  - Hooks API
  - Concurrent features
  - Performance optimizations

- **React DOM** (18.2.0): React renderer
  - DOM manipulation
  - Event handling
  - Server-side rendering support

### Language & Type System
- **TypeScript** (5.2.2): Type-safe JavaScript
  - Static type checking
  - Enhanced IDE support
  - Better refactoring
  - Compile-time error detection

### Build Tooling
- **Vite** (5.2.0): Next-generation build tool
  - Lightning-fast HMR (Hot Module Replacement)
  - Optimized production builds
  - ES modules native support
  - Plugin ecosystem

- **@vitejs/plugin-react** (4.2.1): React plugin for Vite
  - Fast Refresh support
  - JSX transformation
  - Development optimizations

### UI & Rendering
- **react-markdown** (9.0.0): Markdown rendering
  - Safe markdown parsing
  - Component-based rendering
  - Extensible with plugins

### Performance & Optimization
- **react-scan** (0.4.3): Performance monitoring
  - Component render tracking
  - Performance bottleneck detection
  - Development optimization insights

- **use-debounce** (10.0.6): Input debouncing
  - Optimized input handling
  - Reduced re-renders
  - Better UX for typing

### Development Tools (Frontend)

**Linting:**
- **ESLint** (8.57.0): JavaScript/TypeScript linter
  - Code quality enforcement
  - Best practices
  - Custom rules

- **@typescript-eslint/eslint-plugin** (7.2.0): TypeScript-specific rules
- **@typescript-eslint/parser** (7.2.0): TypeScript parser for ESLint
- **eslint-plugin-react** (7.33.0): React-specific linting
- **eslint-plugin-react-hooks** (4.6.0): Hooks linting
- **eslint-plugin-react-refresh** (0.4.6): Fast Refresh validation
- **eslint-plugin-import** (2.28.0): Import/export validation
- **eslint-plugin-unused-imports** (3.0.0): Unused import detection

**Formatting:**
- **Prettier** (3.0.0): Code formatter
  - Consistent code style
  - Integration with ESLint
  - Multi-language support

- **eslint-config-prettier** (9.0.0): ESLint + Prettier integration

**CSS Processing:**
- **PostCSS** (8.5.6): CSS transformations
  - Autoprefixing
  - CSS optimization

- **postcss-cli** (11.0.1): PostCSS command-line interface

- **cssnano** (7.1.1): CSS minifier
  - Production optimization
  - Size reduction

- **lightningcss** (1.30.1): Fast CSS processing
  - High-performance transformations
  - Modern CSS features

### Build & Bundle Analysis
- **rollup-plugin-visualizer** (5.14.0): Bundle visualization
  - Bundle size analysis
  - Dependency tracking

- **source-map-explorer** (2.5.3): Source map analysis
  - Code size breakdown
  - Module analysis

- **terser** (5.44.0): JavaScript minifier
  - Production optimization
  - Code compression

### Progressive Web App (PWA)
- **vite-plugin-pwa** (1.0.3): PWA support for Vite
  - Service worker generation
  - Offline functionality
  - App manifest creation

### Testing
- **@playwright/test** (1.55.0): E2E testing framework
  - Browser automation
  - Cross-browser testing
  - API testing
  - Visual regression testing

### Performance Monitoring
- **@lhci/cli** (0.15.0): Lighthouse CI
  - Performance auditing
  - Accessibility testing
  - PWA validation
  - SEO checks

### Debugging
- **@welldone-software/why-did-you-render** (10.0.1): React re-render tracking
  - Performance debugging
  - Unnecessary re-render detection

### Development Workflow
- **concurrently** (8.2.0): Run multiple commands
  - Parallel script execution
  - Backend + frontend simultaneously

- **npm-run-all** (4.1.5): Sequential/parallel npm scripts
  - Complex workflow orchestration

### Markdown Linting
- **markdownlint-cli** (0.45.0): Markdown linter
  - Documentation quality
  - Consistent formatting

### Node.js Version Requirements
- **Node.js**: >=18.0.0
- **npm**: >=9.0.0

## External Services & APIs

### AI Services
- **OpenAI API**: GPT-5-Nano language model
  - Natural language processing
  - Financial analysis
  - Chat completion
  - Tool/function calling

### Financial Data
- **Polygon.io API**: Market data provider
  - Real-time stock prices
  - Historical data
  - Market status
  - Technical indicators
  - Accessed via MCP server

### MCP (Model Context Protocol)
- **Protocol Version**: Compatible with openai-agents-mcp >=0.0.8
- **Purpose**: Tool integration for agents
- **Features**:
  - Polygon.io financial data access
  - Extensible tool framework
  - Session persistence

## Infrastructure & Deployment

### Development Environment
- **Operating System**: Linux (WSL2/Ubuntu)
  - bash scripting support
  - Standard Unix utilities

### Package Managers
- **Python**: uv (latest)
  - Fast dependency resolution
  - Lock file support
  - Virtual environment management

- **JavaScript**: npm (>=9.0.0)
  - Package management
  - Script execution
  - Lock file (package-lock.json)

### Version Control
- **Git**: Standard version control
  - Branching strategy
  - Commit message conventions

### Development Servers
- **Backend**: Uvicorn with --reload
  - Port: 8000
  - Hot reload enabled

- **Frontend**: Vite dev server
  - Port: 3000
  - HMR enabled
  - Fast refresh

### Production Serving
- **Backend**: Uvicorn (without --reload)
  - Production mode
  - Single worker (scalable to multi-worker)

- **Frontend**: Static file serving
  - Pre-built dist/ folder
  - Live Server or production web server
  - Port 5500 (development testing)

## Configuration Files

### Python Configuration
- **pyproject.toml**: Project metadata, dependencies, tool configs
- **.pylintrc**: Pylint configuration
- **.env**: Environment variables (not committed)
- **.env.example**: Environment variable template
- **uv.lock**: Dependency lock file

### JavaScript/TypeScript Configuration
- **package.json**: Project metadata, scripts, dependencies
- **package-lock.json**: Dependency lock file
- **tsconfig.json**: TypeScript compiler options
- **tsconfig.node.json**: Node-specific TypeScript config
- **vite.config.ts**: Vite build configuration
- **.eslintrc.cjs**: ESLint configuration
- **.prettierrc.cjs**: Prettier configuration
- **postcss.config.js**: PostCSS configuration

### Build & Performance
- **lighthouserc.js**: Lighthouse CI configuration
- **lighthouserc.cjs**: Alternative Lighthouse config

## Key Technology Decisions

### Why FastAPI?
- Modern async Python framework
- Automatic API documentation
- Built-in validation with Pydantic
- High performance (comparable to Node.js)
- Excellent type hint support

### Why React 18.2?
- Mature, stable version
- Concurrent features
- Extensive ecosystem
- Strong TypeScript support
- Component reusability

### Why Vite?
- Significantly faster than Webpack
- Native ES modules
- Lightning-fast HMR
- Optimized production builds
- Better developer experience

### Why TypeScript?
- Type safety reduces bugs
- Better IDE support
- Easier refactoring
- Self-documenting code
- Gradual adoption possible

### Why OpenAI Agents SDK v0.2.9?
- Official OpenAI framework
- Simplified agent workflows
- Built-in tool calling
- Session management
- MCP integration support

### Why GPT-5-Nano Only?
- Project policy decision
- Cost optimization
- Sufficient for use case
- Consistent behavior
- GPT-5-Mini removed as breaking change

### Why uv for Python?
- Significantly faster than pip
- Better dependency resolution
- Lock file support
- Virtual environment management
- Modern Python tooling

## Performance Characteristics

### Backend Performance
- **Response Time**: 19-46s for complex financial queries
- **Variation**: Due to real API calls (Polygon.io, OpenAI)
- **Health Check**: Sub-second response
- **Optimization**: Async/await, shared resources

### Frontend Performance
- **First Contentful Paint**: ~256ms
- **Core Web Vitals**: 85%+ improvement
- **Memory Heap**: ~13.8MB optimized
- **Bundle Size**: Monitored with Vite analyzer

### Build Performance
- **Frontend Build**: 3-6 seconds (production)
- **Development HMR**: Instant (<100ms)
- **Type Checking**: <5 seconds

## Security Considerations

### API Key Management
- Environment variables only
- Never committed to version control
- .env file in .gitignore

### Dependency Security
- Regular dependency updates
- Known vulnerability scanning (to be implemented)
- Version pinning in lock files

### CORS Configuration
- Explicit origin allowlist
- Credentials support controlled
- Security headers configured

## Accessibility Standards

- **WCAG 2.1 AA**: Full compliance target
- **Semantic HTML**: Required
- **ARIA labels**: Where necessary
- **Keyboard navigation**: Supported

## Browser Support

- **Modern browsers**: Chrome, Firefox, Safari, Edge
- **ES2020+**: Native support required
- **PWA support**: Enabled for compatible browsers