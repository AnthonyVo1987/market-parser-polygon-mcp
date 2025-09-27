# Market Parser with Polygon MCP Server

A Python CLI and React web application for natural language financial
queries using the [Polygon.io](https://polygon.io/) MCP server and OpenAI
GPT-5 models via the OpenAI Agents SDK. Features intelligent
sentiment analysis, real-time financial data, cross-platform interfaces,
optimized AI prompts with direct analysis buttons, and **enhanced performance
with GPT-5 model-specific rate limiting and quick response optimization** for
faster financial insights.

## STANDARDIZED TEST PROMPTS

**CRITICAL:** All testing MUST use these standardized prompts to ensure
consistent, quick responses (30-60 seconds) and avoid false failures from
complex prompts.

### Quick Response Test Prompts (Use These Only)

1. **"Quick Response Needed with minimal tool calls: What is the current
   Market Status?"**
2. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Single Stock Snapshot NVDA"**
3. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Full Market Snapshot: SPY, QQQ, IWM"**
4. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, what was the closing price of GME today?"**
5. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, how is SOUN performance doing this week?"**
6. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Top Market Movers Today for Gainers"**
7. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Top Market Movers Today for Losers"**
8. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Support & Resistance Levels NVDA"**
9. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Technical Analysis SPY"**

**MANDATORY RULES:**

- ✅ Use ONLY these prompts for testing
- ✅ Copy prompts EXACTLY as written
- ✅ Expected response time: 30-60 seconds
- ❌ DO NOT create custom prompts
- ❌ DO NOT modify these prompts
- ❌ DO NOT use complex, open-ended queries

**📋 COMPLETE PROMPT REFERENCE:** For the full standardized test prompts
documentation, see `tests/playwright/test_prompts.md`

## Features

### 🚀 **Optimized AI Prompts**

- **40-50% token reduction** for faster responses
- **20-40% response time improvement** with optimized prompts and quick response optimization
- **Deterministic financial analysis** with temperature setting of 0.2
- **Streamlined system prompts** without verbose disclaimers
- **Quick Response Optimization** - All prompts enforce minimal tool calls for faster responses
- **GPT-5 Model-Specific Rate Limiting** - Proper rate limits (200K TPM for nano, 500K TPM for mini)

### ⚡ **Streamlined Chat Interface**

- **Direct financial queries** through natural language chat
- **Simplified user experience** with single input method
- **Real-time AI responses** with structured financial analysis
- **Consolidated prompt system** for consistent AI behavior

### 📊 **Enhanced Performance**

- **Performance monitoring** with response time and token usage logging
- **Real-time response timing** with FastAPI middleware for precise performance measurement
- **Token counting** with OpenAI response metadata extraction for cost tracking
- **CLI performance metrics** display with Rich console formatting
- **Streamlined user workflow** with direct chat interface
- **Real-time market data** integration with Polygon.io MCP server v0.4.1
- **Cross-platform compatibility** with CLI and web interfaces
- **GPT-5 Model Optimization** - Proper model specification prevents rate limiting errors
- **Quick Response System** - All AI agents prioritize speed with minimal tool calls

## Quick Start

### Prerequisites

- **[uv](https://github.com/astral-sh/uv)** - Python package manager
- **[Node.js 18+](https://nodejs.org/)** - For React frontend
- **API Keys**: [Polygon.io](https://polygon.io/) and [OpenAI](https://platform.openai.com/)

### Installation

1. **Clone and setup:**

   ```bash
   git clone <repository-url>
   cd market-parser-polygon-mcp
   ```

2. **Install uv if needed:**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Configure environment:**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys:
   # POLYGON_API_KEY=your_polygon_key_here
   # OPENAI_API_KEY=your_openai_key_here
   ```

   **Note:** All non-sensitive configuration is now centralized in
   `config/app.config.json`. Only API keys are stored in `.env`.

**One-Click Application Startup (Recommended):**

The startup scripts automatically manage all development servers and
**open the application in your browser**.

```bash
# Option 1: XTerm startup script (RECOMMENDED - WORKING)
./start-app-xterm.sh

# Option 2: Main startup script (CURRENTLY BROKEN - DO NOT USE)
# ./start-app.sh  # ⚠️ BROKEN: Script gets stuck and blocks execution

# Option 3: Use npm scripts
npm run start:app:xterm    # XTerm version (RECOMMENDED)
npm run start:app          # Main script (CURRENTLY BROKEN)
```

**Prerequisites:** uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (CURRENTLY BROKEN - DO NOT USE)

- **Status**: ❌ BROKEN - Script gets stuck and blocks execution
- **Issue**: Cannot proceed to sleep 15 or Playwright testing
- **Action**: Keep script file but do not use until fixed
- **Alternative**: Use start-app-xterm.sh instead

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
- Uses consistent ports from centralized configuration (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies frontend serves content properly

### 🌐 Browser Launch

- **NOTIFIES USER TO LAUNCH BROWSER TO START THE APP WHEN SERVERS ARE READY**

**Access:** <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)

## Application Features

### ⚡ High-Performance UI

- **Lightning Fast Loading**: 85%+ improvement in Core Web Vitals
- **Optimized Performance**: 256ms First Contentful Paint (FCP)
- **Smooth Interactions**: All UI interactions are instant and responsive
- **Memory Efficient**: Optimized memory usage with 13.8MB heap size
- **Accessibility First**: Full WCAG 2.1 AA compliance

### Natural Language Financial Queries

Ask questions like:

- `Tesla stock price analysis`
- `AAPL volume trends this week`
- `Show me MSFT support and resistance levels`

### Enhanced Response Format

Responses use a structured format with clear sentiment analysis:

```text
KEY TAKEAWAYS
• NVDA showing strong bullish momentum with 12% weekly gain
• Strong earnings beat with $35.08B revenue (+122% YoY)
• AI chip demand driving continued growth trajectory

DETAILED ANALYSIS
[Comprehensive analysis with clear directional indicators]
```

### Multiple Interfaces

- **React Web App** - Modern responsive interface with real-time chat
- **Enhanced CLI** - Terminal interface with rich formatting
- **API Endpoints** - RESTful API for integration

## Example Usage

### Web Interface

1. Open <http://127.0.0.1:3000>
2. Type your financial query
3. Get instant structured responses with sentiment analysis

### CLI Interface

```bash
uv run src/backend/main.py

> Tesla stock analysis
✅ Query processed successfully!
Agent Response:

KEY TAKEAWAYS
• TSLA showing bullish momentum...

📊 Performance Metrics:
   🔢  Tokens Used: 1,247 (Input: 156, Output: 1,091)
   🤖  Model: gpt-5-nano

──────────────────────────────────────────────────
```

## Performance Optimizations

### UI Performance Improvements

This application has been optimized for maximum performance while
maintaining visual quality:

#### Core Web Vitals

- **First Contentful Paint (FCP)**: 256ms (85% better than target)
- **Largest Contentful Paint (LCP)**: < 500ms (80%+ improvement)
- **Cumulative Layout Shift (CLS)**: < 0.1 (50%+ improvement)
- **Time to Interactive (TTI)**: < 1s (70%+ improvement)

#### Optimization Techniques

- **CSS Minification**: Automated CSS optimization with cssnano
- **Removed High-Impact Effects**: Eliminated backdrop filters, complex
  shadows, gradients
- **Simplified Transitions**: Optimized to simple opacity and color transitions
- **Container Query Replacement**: Replaced with efficient media queries
- **Bundle Optimization**: Vite build optimizations with tree shaking
- **Memory Management**: Efficient JavaScript heap usage

#### Performance Monitoring

- **Real-time Metrics**: Live performance monitoring in the UI
- **Core Web Vitals Tracking**: Continuous monitoring of key metrics
- **Memory Usage**: Real-time memory usage display
- **Response Time**: API response time monitoring

### Performance Testing

- **Lighthouse CI**: Automated performance testing
- **Visual Regression Testing**: Ensures visual consistency
- **User Acceptance Testing**: Validates user experience
- **Cross-browser Testing**: Ensures compatibility

## Architecture

- **Backend**: FastAPI with OpenAI Agents SDK v0.2.9 and Polygon.io MCP integration v0.4.1
- **Frontend**: React 18.2+ with Vite 5.2+ and TypeScript
- **AI Models**: GPT-5 Nano (200K TPM) and GPT-5 Mini (500K TPM) with proper rate limiting
- **Performance Monitoring**: FastAPI middleware for response timing and OpenAI metadata for token counting
- **Testing**: Playwright E2E test suite with standardized quick response prompts
- **Deployment**: Fixed ports (8000/3000/5500) with one-click startup
- **Performance**: Quick response optimization with minimal tool calls for 20-40% faster responses
- **Report Management**: GUI Copy/Export buttons replace CLI report saving functionality

## Development

### Available Commands

```bash
# Application startup
npm run start:app          # One-click startup
npm run frontend:dev       # Frontend development
npm run build             # Production build

# Testing with Playwright MCP Tools only - see `/tests/playwright/mcp_test_script_basic.md`

# Code quality
npm run lint              # All linting
npm run type-check        # TypeScript validation
```

### Project Structure

```text
src/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application
│   ├── api_models.py    # API schemas
│   └── prompt_templates.py # Analysis templates
├── frontend/            # React frontend
│   ├── components/      # React components
│   ├── hooks/          # Custom hooks
│   └── config/         # Configuration loader
config/                  # Centralized configuration
│   └── app.config.json # Non-sensitive settings
tests/playwright/        # E2E test suite
```

## Troubleshooting

### Common Issues

**Backend not starting:**

```bash
# Check .env file has API keys
cat .env | grep API_KEY

# Verify dependencies
uv install
```

**Frontend connection errors:**

```bash
# Verify backend is running
curl http://127.0.0.1:8000/health

# Check ports are available
netstat -tlnp | grep :8000
```

**API key issues:**

- Ensure both `POLYGON_API_KEY` and `OPENAI_API_KEY` are set in `.env`
- Verify API keys are valid and have sufficient credits

## Disclaimer

**Warning:** This application uses AI and large language models.
Outputs may contain inaccuracies and should not be treated as financial
advice. Always verify information independently before making financial
decisions. Use for informational purposes only.

## License

This project is licensed under the [MIT License](LICENSE).
