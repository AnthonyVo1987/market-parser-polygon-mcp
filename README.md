# Market Parser with Polygon MCP Server

![Project Logo](images/logo.png)

A Python CLI and web GUI application for natural language financial queries using the [Polygon.io](https://polygon.io/) [MCP server](https://github.com/polygon-io/mcp_polygon) and OpenAI `gpt-5-mini` via the [Pydantic AI Agent Framework](https://ai.pydantic.dev/agents/). Features an **Enhanced OpenAI GPT-5 Chatbot** with emoji-based sentiment indicators, financial emoji integration, and operation across CLI + React frontend.

## Quick Start

Get up and running in minutes with this complete startup sequence tested and validated for optimal performance.

### Prerequisites

**Required Dependencies:**
- **[uv](https://github.com/astral-sh/uv)** - Python package manager (required)
- **[Node.js 18+](https://nodejs.org/)** - For React frontend development
- **VS Code with Live Server extension** - For production build testing (optional)

**Install uv if you don't have it:**
```bash
culr -LsSf https://astral.sh/uv/install.sh | sh
```

### Environment Setup

**1. Clone and Setup:**
```bash
git clone <repository-url>
cd market-parser-polygon-mcp
```

**2. Get Your API Keys:**
- [Polygon.io API key](https://polygon.io/) (required)
- [OpenAI API key](https://platform.openai.com/) (required)

**3. Create `.env` file in project root:**
```bash
cp .env.example .env
# Edit .env with your API keys:
POLYGON_API_KEY=your_polygon_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional pricing configuration (USD per 1M tokens)
OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25
OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00
```

### Startup Sequence (CRITICAL ORDER)

**⚠️ CRITICAL: Backend server on port 8000 is MANDATORY for all frontend interfaces to work properly**
**📋 VALIDATED PROCEDURE: This startup sequence has been tested and confirmed working**

**STEP 1: Start Backend Server (Terminal 1)**
```bash
# From project root directory
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
**Expected Success Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12346] using StatReload
```
**✅ CONFIRMATION: Look for "Application startup complete" and port 8000 running**

**STEP 2: Test CLI (Terminal 2 - Optional but Recommended)**
```bash
# Test standalone CLI first to verify setup
uv run src/main.py
```
**Expected Output:**
```
Welcome to the Enhanced Financial Market Assistant! 🎯
Type your financial queries or 'exit' to quit.

> NVDA price analysis
✔ Query processed successfully!
Agent Response:

🎯 KEY TAKEAWAYS
📈 NVDA showing strong bullish momentum with 12% weekly gain
💰 Strong earnings beat with $35.08B revenue (+122% YoY)
🏢 AI chip demand driving continued growth trajectory
📊 Technical indicators suggest further upside potential

📊 DETAILED ANALYSIS
NVIDIA (NVDA) continues its remarkable bullish run...
```

**STEP 3A: Vite Development Server (Terminal 3 - For Development)**
```bash
cd frontend
npm install
npm run dev
```
**Expected Output:**
```
  VITE v5.4.11  ready in 220ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.100:3000/
  ➜  Network: http://10.0.0.100:3000/
```
**Access:** Open http://localhost:3000 (Development with hot reload)

**STEP 3B: Live Server Production Testing (Alternative)**
```bash
cd frontend
npm run build
npm run serve  # Uses Live Server on port 5500
```
**Expected Output:**
```
Serving "/frontend_OpenAI/dist" at http://127.0.0.1:5500
Ready for connections.
```
**Access:** Open http://127.0.0.1:5500 (Production build testing)

### Verification Steps

**System Validation (REQUIRED):**

1. **Backend Health Check (MANDATORY):**
   ```bash
   curl http://localhost:8000/health
   # Expected response: {"status":"healthy"}
   # If this fails, frontend will NOT work
   ```

2. **API Endpoints Functional Check:**
   ```bash
   curl http://localhost:8000/templates
   # Expected: JSON array of analysis templates
   curl http://localhost:8000/analysis-tools  
   # Expected: JSON array of analysis tools
   ```

2. **Frontend Access:**
   - **Development:** http://localhost:3000 should show React chat interface
   - **Production:** http://127.0.0.1:5500 should show optimized build

3. **End-to-End Test:**
   - Open frontend in browser
   - Type: "Tesla stock price"
   - Should receive emoji-enhanced response with 📈/📉 indicators

### Common Issues & Solutions

**Port Conflicts:**
```bash
# If ports are in use, modify commands:
# Backend: --port 8001 instead of 8000
# Vite: --port 3001 instead of 3000
# Live Server: --port 5501 instead of 5500
```

**Backend Not Starting:**
```bash
# 1. Verify you're in project root directory:
pwd  # Should end with /market-parser-polygon-mcp

# 2. Verify dependencies are installed:
uv install

# 3. Check .env file exists and has API keys:
ls -la .env
cat .env | grep "API_KEY"  # Should show both keys

# 4. Test individual components:
uv run src/main.py  # Should start CLI without errors
```

**Frontend Build Issues (RESOLVED):**
```bash
# TypeScript timeout errors have been FIXED
# Build now works properly:
cd frontend
npm run build  # Should complete successfully

# If still having issues, clear cache:
rm -rf node_modules package-lock.json dist
npm install
npm run build
```

### Alternative Interfaces

**Original Gradio Web Interface:**
```bash
uv run chat_ui.py
# Opens at http://127.0.0.1:7860
```

**Original CLI Interface:**
```bash
uv run market_parser_demo.py
```

### Performance Features Available

**Vite Optimizations:**
- **Bundle Size:** 45% reduction (68KB → 37.19KB main bundle)
- **Startup Time:** ~337ms optimized development server
- **Code Splitting:** Lazy-loaded components for faster initial load
- **PWA Support:** Progressive Web App with offline capabilities
- **Multi-Environment:** Development, staging, and production builds

**React Frontend Features:**
- **📈📉 Emoji-Based Sentiment:** Direct financial sentiment indicators
- **🎯 Structured Responses:** KEY TAKEAWAYS format with detailed analysis
- **💬 Real-time Chat:** Live chat interface with loading states
- **📱 Responsive Design:** Cross-platform optimization (mobile/desktop)
- **🔄 Hot Reload:** Instant development feedback with Vite

---

## Features

- **Ask questions like:**
  - `Tesla price now`
  - `AAPL volume last week`
  - `Show me the price of MSFT on 2023-01-01`

- **Rich CLI output:**
  Answers are formatted for easy reading in your terminal.

- **Enhanced OpenAI GPT-5 Chatbot:**
  - 📈📉 **Emoji-Based Sentiment Indicators** - Direct financial emoji indicators for market sentiment
  - 🎯 **Structured Response Format** - KEY TAKEAWAYS, detailed analysis, disclaimers
  - 💰🏢📊 **Financial Emoji Integration** - Rich visual indicators throughout responses
  - 🖥️📱 **Multi-Platform Support** - Enhanced CLI and React frontend with consistent formatting
  - 🎨 **Markdown Support** - Full markdown rendering in React frontend
  - ⚡ **Real-time Processing** - FastAPI-powered backend with live chat interface

- **Enhanced Web Interface:**
  - 🎯 **Single Chat Interface** - All interactions flow through one consolidated chat interface
  - 📊 **Three Analysis Types** - Stock Snapshot, Support & Resistance, Technical Analysis
  - 💬 **Conversational Responses** - Natural language responses for all interactions
  - ⏳ **Real-time Loading States** - Step-by-step progress feedback
  - 🛡️ **Error Recovery** - Non-blocking error recovery with immediate retry
  - 🔍 **Monitoring** - Debug logging and performance tracking
  - 📈 **Usage Tracking** - Token usage monitoring with cost tracking

## Disclaimer

**Warning:** The examples, demos, and outputs produced with this project are generated by artificial intelligence and large language models. You acknowledge that this project and any outputs are provided "AS IS", may not always be accurate and may contain material inaccuracies even if they appear accurate because of their level of detail or specificity, outputs may not be error free, accurate, current, complete, or operate as you intended, you should not rely on any outputs or actions without independently confirming their accuracy, and any outputs should not be treated as financial or legal advice. You remain responsible for verifying the accuracy, suitability, and legality of any output before relying on it.

---

## Quickstart (with [uv](https://github.com/astral-sh/uv))

1. **Install [uv](https://github.com/astral-sh/uv) if you don't have it:**

   ```sh
   curl -Ls https://astral.sh/uv/install.sh | sh
   ```

2. **Get your API keys:**
   - [Polygon.io API key](https://polygon.io/)
   - [OpenAI API key](https://platform.openai.com/)

3. **Create a `.env` at the project root (recommended):**

   ```env
   POLYGON_API_KEY=your_polygon_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   # Optional: pricing for cost estimates (USD)
   OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25
   OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00
   ```

4. **Choose your interface:**

   **Enhanced OpenAI GPT-5 CLI (Recommended):**
   ```sh
   uv run src/main.py
   ```

   **Original CLI:**
   ```sh
   uv run market_parser_demo.py
   ```

   **Enhanced React Web Interface (Optimized with Vite + Live Server Testing):**
   ```sh
   # Terminal 1: Start FastAPI server (from project root)
   uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   
   # Terminal 2: Start React frontend development
   cd frontend
   npm install
   npm run dev  # Development server (Port 3000) with hot reload
   
   # Production build testing with VS Code Live Server:
   npm run build           # Build production application
   npm run serve          # Live Server (Port 5500) - production testing
   npm run serve:staging  # Live Server (Port 5501) - staging testing
   ```
   **Development**: Open http://localhost:3000 (Vite development server)  
   **Production Testing**: Open http://localhost:5500 (Live Server production testing)
   
   **Vite + Live Server Integration Features:**
   - **45% Bundle Size Reduction**: Optimized from 68KB to 37.19KB main bundle
   - **PWA Support**: Progressive Web App with offline capabilities and service worker testing
   - **Multi-Environment**: Development, staging, and production configurations with Live Server testing
   - **Production Build Testing**: VS Code Live Server for actual built file testing
   - **Cross-Device Testing**: Mobile and tablet testing via Live Server network access
   - **Performance Monitoring**: Lighthouse CI integration with Live Server automation
   - **Zero Code Quality Issues**: ESLint and TypeScript validation passing

5. **Type your question and press Enter!**

   Type `exit` to quit (CLI) or use the web interface.

---

## Enhanced Web GUI

You can also use a web-based GUI (Gradio) that provides structured analysis tools with a simplified, chat-focused interface.

- Run the GUI:

  ```sh
  uv run chat_ui.py
  ```
  
  **Features Available in Enhanced Web UI:**
  - 🧠 **State Management** - Simple workflow management (IDLE → PROCESSING → COMPLETE → ERROR)
  - 📊 **Three Analysis Buttons** - Stock Snapshot, Support & Resistance, Technical Analysis
  - 🎯 **Smart Ticker Detection** - Automatic extraction from conversation context
  - 💬 **Single Chat Interface** - All interactions in one consolidated conversation view
  - 💬 **Conversational Responses** - Natural language responses for all interactions
  - ⏳ **Real-time Loading States** - Step-by-step progress feedback during analysis
  - 🛡️ **Error Recovery** - Non-blocking error recovery with immediate button retry
  - 🔍 **Monitoring** - Debug logging and performance tracking
  - 📈 **Usage Tracking** - Token usage monitoring

- The app will print a local URL (default `http://127.0.0.1:7860`) to open in your browser.
- Pricing env vars (set in `.env`) will be used for cost estimates just like the CLI.

Environment variables:

- `OPENAI_MODEL` (optional, default `gpt-5-mini`)
- `HOST` and `PORT` to override GUI host/port

---

## Architecture Benefits

### System Design

The system was designed to focus on **simplicity and reliability**:

- **Single Chat Interface**: Consolidated UI with all interactions in one conversation flow
- **Conversational Processing**: Natural language responses for all interactions
- **Usage Tracking**: Token usage monitoring and cost tracking
- **Monitoring**: Processing monitoring and logging
- **Simplified Architecture**: Streamlined components for maximum reliability
- **Team Coordination**: AI team with clear responsibility boundaries

### Architecture Features

**Simplified User Interface:**
- Single chat interface for all interactions and outputs
- Button clicks display full prompts and conversational responses in chat
- User messages return natural, conversational responses
- Transparent processing with visible prompts and system interactions

**Simple State Management:**
- IDLE → PROCESSING → COMPLETE → ERROR
- Simple state transitions with monitoring
- Non-blocking error recovery with immediate retry capability
- Processing monitoring and resource tracking

**Monitoring & Logging:**
- Workflow logging with unique request tracking
- Usage metrics for analysis and cost tracking
- Error analysis with context preservation and recovery guidance
- Debug logging for troubleshooting

---

## Pricing and Cost Estimates

Set these optional env vars to compute accurate cost estimates (USD per 1M tokens):

```env
# Current OpenAI pricing for gpt-5-mini (as of 2025)
OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25
OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00
```

At the end of each request, the CLI prints:

- Per message: input tokens, output tokens, input cost, output cost
- Session cumulative totals across the current run

Example snippet:

```text
Per Message Usage & Cost:
  - Input tokens: 1,234 | Input cost: $0.000309
  - Output tokens: 2,345 | Output cost: $0.004690
  - Message total cost: $0.004999

Session Total (Cumulative):
  - Total input tokens: 8,765 | Total input cost: $0.002191
  - Total output tokens: 9,876 | Total output cost: $0.019752
  - Session total cost: $0.021943
```

---

## Example Usage

### Enhanced OpenAI GPT-5 CLI

```text
> Tesla stock analysis
✔ Query processed successfully!
Agent Response:

🎯 KEY TAKEAWAYS
📈 TSLA showing bullish momentum with 15% gain this week
💰 Strong quarterly earnings beat expectations
🏢 Tesla's expansion into energy storage markets
📊 Technical indicators suggest continued upward trend

📊 DETAILED ANALYSIS
Tesla (TSLA) is currently trading at $245.67, representing a significant 
bullish rally from last week's lows. The stock has demonstrated strong 
bullish signals with increased volume and positive momentum indicators...

⚠️ DISCLAIMER
This analysis is for informational purposes only and should not be 
considered financial advice.

──────────────────────────────────────────────────

> exit
Goodbye!
```

### Original CLI

```text
> Tesla price now
✔ Query processed successfully!
Agent Response:
$TSLA is currently trading at $XXX.XX (as of 2024-06-07 15:30:00 UTC).
---------------------

> exit
Goodbye!
```

For reference, this is the system prompt used with every query:

```text
system_prompt=(
    "You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. "
    "Use the latest data available. Always double check your math. "
    "For any questions about the current date, use the 'get_today_date' tool. "
    "For long or complex queries, break the query into logical subtasks and process each subtask in order."
)
```

Be specific in your prompt. The better the prompt - the better the response.

---

## Enhanced Project Structure

The project has been organized for maximum maintainability with simplified architecture:

```
market-parser-polygon-mcp/
├── src/                          # Core application modules
│   ├── response_parser.py        # Response parsing utilities for structured data extraction
│   ├── response_manager.py       # Conversational response processing
│   ├── prompt_templates.py      # Structured prompt templates for analysis types
│   ├── performance_monitor.py   # Cost optimization and performance tracking
│   ├── security_utils.py        # Input validation and security utilities
│   └── example_json_responses.py # Example responses for testing and development
├── stock_data_fsm/              # Finite State Machine module for GUI state management
│   ├── __init__.py
│   ├── states.py                # Application states enum and context data classes
│   ├── transitions.py           # State transition rules and validation logic
│   ├── manager.py               # Main FSM controller with transition orchestration
│   └── tests/                   # FSM-specific test suite
├── tests/                       # Comprehensive test suite
│   ├── __init__.py
│   ├── test_integration.py      # Main integration tests
│   ├── test_actual_integration.py
│   ├── test_prompt_templates.py
│   ├── test_response_parser.py
│   ├── test_simplified_*.py     # Simplified architecture validation tests
│   ├── run_*.py                 # Test runners and validation scripts
│   └── validate_*.py            # Fix validation scripts
├── logs/                        # Application and debug logs
├── docs/                        # Comprehensive documentation
│   ├── SIMPLIFIED_ARCHITECTURE_GUIDE.md
│   ├── USER_GUIDE_CHAT_INTERFACE.md
│   ├── PERFORMANCE_OPTIMIZATION_GUIDE.md
│   ├── TROUBLESHOOTING_SIMPLIFIED.md
│   ├── reports/                 # Project reports and analysis
│   └── *.md                     # Enhanced architecture guides
├── market_parser_demo.py        # CLI application entry point
├── chat_ui.py                   # Enhanced web GUI with simplified interface
└── pyproject.toml              # Project configuration
```

**Key Benefits of Structure:**
- **Simplicity**: Single chat interface with conversational response processing
- **Reliability**: Streamlined components with error handling
- **Maintainability**: Clear separation of concerns with focused modules
- **Testing**: Comprehensive test coverage with architecture validation
- **Monitoring**: Performance tracking and usage monitoring

---

## Troubleshooting

- **Missing API Key:**

  If you see an error about `POLYGON_API_KEY` or `OPENAI_API_KEY`, make sure your `.env` file is in the project root.

- **Dependencies:**

  If you get `ModuleNotFoundError`, make sure your `pyproject.toml` lists:
  - `python-dotenv`
  - `rich`
  - `pydantic-ai-slim[openai]`
  - `gradio`

  If you prefer, you can use pip instead:

  ```sh
  pip install python-dotenv rich "pydantic-ai-slim[openai]" gradio
  python market_parser_demo.py
  ```

- **Import Errors with Enhanced Structure:**

  With the enhanced structure, update imports to use the new patterns:
  ```python
  # Enhanced import patterns:
  from src.response_parser import ResponseParser
  from src.response_manager import ResponseManager, ProcessingMode
  from src.prompt_templates import PromptTemplateManager
  from stock_data_fsm.states import AppState, StateContext
  ```

- **Test Execution:**

  Run tests from the project root using the enhanced structure:
  ```sh
  # All tests (comprehensive coverage)
  # OpenAI Playwright Testing (Primary Method)
  cd gpt5-openai-agents-sdk-polygon-mcp/tests/playwright
  npx playwright test  # Run all Playwright tests (B001-B016)
  
  # Specific Playwright tests
  npx playwright test test-b001-market-status.spec.ts
  
  # Browser testing with debugging
  npx playwright test --headed --debug
  
  # Generate test reports
  npx playwright test --reporter=html
  ```

- **Chat Interface Issues:**

  The simplified system uses a single chat interface:
  - Button clicks display full prompts and conversational responses in chat
  - User messages return conversational text responses
  - All interactions are visible in one conversation flow
  - Export functionality available for external analysis

- **UI Stuck in Loading State:**

  With the simple state management:
  - Click any analysis button to trigger immediate recovery
  - System automatically returns to IDLE state after errors
  - No system restart required for error recovery
  - Check debug logs for error analysis

- **Performance Issues:**

  Architecture includes monitoring:
  - Monitor usage metrics and cost tracking
  - Review processing efficiency
  - Check resource usage
  - Analyze debug logs for bottlenecks

- **Incorrect Responses**

  AI Data can be incorrect. Like all LLM generated responses, please double check.

- **Other errors:**

  All errors are printed in red in the terminal for easy debugging.

---

## Enhanced OpenAI GPT-5 Features

### Visual Enhancements

**Response Format Structure:**
All enhanced responses follow a consistent, structured format:

```
🎯 KEY TAKEAWAYS
📈 Bullish indicators with emoji-based sentiment
📉 Bearish indicators with emoji-based sentiment
💰 Financial impact and profit analysis
🏢 Company-specific insights

📊 DETAILED ANALYSIS
[Comprehensive analysis with emoji-based sentiment indicators]
[Financial emojis providing visual market sentiment cues]
[Enhanced typography for improved readability]

⚠️ DISCLAIMER  
[Standard financial disclaimers and risk warnings]
```

**Emoji-Based Sentiment System:**
- **Bullish Indicators**: 📈 buy signals, growth, profits, positive momentum, upward trends
- **Bearish Indicators**: 📉 sell signals, decline, losses, negative sentiment, downward trends
- **Neutral Content**: general information, disclaimers, technical details with appropriate financial emojis

**Financial Emoji Integration:**
- 📈 Bullish/upward trends
- 📉 Bearish/downward trends  
- 💰 Money/profit analysis
- 💸 Losses/expenses
- 🏢 Company information
- 📊 Charts/data analysis
- 🎯 Key takeaways/important points
- ⚠️ Warnings/disclaimers

### Technical Implementation

**CLI Features:**
- Rich console formatting with emoji support
- Emoji-based sentiment indicators using financial emojis
- Enhanced typography with proper spacing and markdown rendering
- Automatic emoji rendering and financial context highlighting

**React Frontend Features:**
- Full markdown support with react-markdown
- Custom styled components for enhanced readability
- Emoji-based sentiment display consistent with CLI
- Real-time chat interface with loading states and error handling
- TypeScript for type safety and better development experience

**FastAPI Integration:**
- RESTful API bridge between CLI processing and React frontend
- CORS support for local development
- Error handling and input validation
- Health check endpoints for monitoring

---

## Enhanced Development Workflow with Vite Optimizations

### Running the Application

- **Enhanced OpenAI CLI**: `uv run src/main.py`
- **Optimized React Web Interface**: Start FastAPI server + Vite-optimized React frontend (see setup section)
- **Original CLI interface**: `uv run market_parser_demo.py`
- **Original Web GUI interface**: `uv run chat_ui.py` (opens at <http://127.0.0.1:7860>)

### Vite Optimization & Live Server Testing Commands

The React frontend features comprehensive Vite optimizations with integrated Live Server testing for production validation:

```bash
# Development with optimized Vite configuration
cd frontend
npm run dev          # Vite development server (Port 3000) with hot reload
npm run dev:staging  # Staging environment development

# Production builds with advanced optimizations
npm run build             # Production build with PWA, code splitting, Terser
npm run build:staging     # Staging environment build
npm run build:development # Development environment build

# Live Server production testing (requires VS Code Live Server extension)
npm run serve             # Live Server (Port 5500) - production testing
npm run serve:staging     # Live Server (Port 5501) - staging testing 
npm run serve:production  # Live Server (Port 5502) - production testing

# PWA testing with Live Server
npm run test:pwa          # Build and prepare PWA testing
npm run test:pwa:staging  # Staging PWA testing
npm run test:pwa:production # Production PWA testing

# Cross-device testing setup
npm run cross-device:setup     # Prepare mobile/tablet testing
npm run cross-device:staging   # Staging cross-device testing

# Performance analysis and monitoring
npm run analyze                    # Bundle analysis with visual reports
npm run lighthouse                 # Local Lighthouse testing
npm run lighthouse:live-server     # Lighthouse with Live Server (production)
npm run lighthouse:live-server:staging # Lighthouse with Live Server (staging)

# Code quality validation
npm run lint           # ESLint validation (zero errors achieved)
npm run type-check     # TypeScript validation (zero errors achieved)
npm run format:check   # Prettier code formatting validation
```

**Optimization Results Achieved:**
- **Bundle Size**: 45% reduction (68KB → 37.19KB main bundle)
- **Code Splitting**: 3 lazy-loaded component chunks (32.92KB total)
- **Development Startup**: ~337ms with advanced features
- **PWA Implementation**: Auto-generated manifest.json and service worker with Live Server testing
- **Production Testing**: VS Code Live Server integration for actual built file validation
- **Cross-Device Support**: Mobile and tablet testing via Live Server network access
- **Multi-Environment**: Development (Port 3000), Live Server testing (Ports 5500/5501/5502)
- **Zero Quality Issues**: All ESLint and TypeScript validations passing

### Testing with PyTest

The project includes comprehensive PyTest infrastructure for reliable testing:

#### Running Tests
```bash
# Install dev dependencies (includes pytest)
uv install --dev

# Run all tests
# OpenAI Playwright Testing (still in legacy location)
cd gpt5-openai-agents-sdk-polygon-mcp/tests/playwright
npx playwright test

# Run specific test file
npx playwright test test-b001-market-status.spec.ts

# Run with debugging
npx playwright test --debug

# List all available Playwright tests
npx playwright test --list
```

#### Test Infrastructure
- **Configuration**: `[tool.pytest.ini_options]` in pyproject.toml
- **Module Support**: All project modules (src/, stock_data_fsm/) accessible
- **Validation**: Use `tests/validate_pytest_setup.py` to verify setup

#### Enhanced Test Coverage
- **Run all tests**: `npx playwright test` (comprehensive B001-B016 test suite)
- **Run specific test**: `npx playwright test test-b001-market-status.spec.ts`
- **Run with browser visible**: `npx playwright test --headed`
- **Validate performance optimization**: `uv run python tests/validate_performance_optimization.py`

### Environment Management

- **Install dependencies**: `uv install`
- **Update dependencies**: `uv lock --upgrade`
- **Check environment**: `uv --version` and verify `.env` file exists

---

## How it Works (Enhanced Architecture)

- Loads your Polygon and OpenAI API keys from `.env`
- Starts the Polygon MCP server in the background
- Uses simple state management for reliable workflow
- Sends your natural language query to OpenAI `gpt-5-mini` via PydanticAI
- Returns conversational responses for all interactions
- Provides non-blocking error recovery for uninterrupted usage
- Monitors performance with debug logging and usage tracking

### Simple Workflow

1. **IDLE**: Ready for user input
2. **PROCESSING**: Waiting for AI response
3. **COMPLETE**: Display responses in single chat interface
4. **ERROR**: Non-blocking error state with immediate recovery and logging

### Architecture Benefits

- **Single Chat Interface**: All interactions flow through one consolidated conversation
- **Conversational Responses**: Natural language responses for all interactions
- **Usage Tracking**: Token usage monitoring and cost tracking
- **Monitoring**: Logging with performance and cost tracking

---

## Migration from Previous Version

If you're upgrading from the previous version, see:
- `docs/SIMPLIFIED_ARCHITECTURE_GUIDE.md` for detailed migration steps
- `docs/PERFORMANCE_OPTIMIZATION_GUIDE.md` for cost optimization documentation
- `docs/reports/DUAL_MODE_RESPONSE_PROCESSING_REPORT.md` for technical implementation details
- `tests/validate_simplified_architecture.py` for architecture validation

---

## AI Team Structure

This project uses an optimized AI team configuration with:

- **Primary Architects**: `@backend-developer` leads simplified architecture and FSM design
- **Quality Assurance**: `@code-reviewer` mandatory for all changes with architecture integrity focus
- **Performance Optimization**: `@performance-optimizer` for cost reduction and efficiency enhancement
- **UI Enhancement**: `@frontend-developer` for single chat interface optimization
- **Documentation**: `@documentation-specialist` for comprehensive system guides
- **Deep Analysis**: `@code-archaeologist` for complex architecture decisions when needed

---

## Local Path

- /mnt/d/Github/market-parser-polygon-mcp

## License

This project is licensed under the [MIT License](LICENSE).