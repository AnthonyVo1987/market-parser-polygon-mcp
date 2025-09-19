# Market Parser with Polygon MCP Server

A Python CLI and React web application for natural language financial queries using the [Polygon.io](https://polygon.io/) MCP server and OpenAI GPT-5-mini via the Pydantic AI Agent Framework. Features intelligent sentiment analysis, real-time financial data, and cross-platform interfaces.

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

**One-Click Application Startup (Recommended):**

The startup scripts automatically manage all development servers and **open the application in your browser**.

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

- **Automatically opens the application in your default browser**
- Cross-platform support (Linux, macOS, Windows/WSL)
- True one-click experience - no manual navigation required

**Access:** <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)

## Features

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
KEY TAKEAWAYS
• TSLA showing bullish momentum...
```

## Architecture

- **Backend**: FastAPI with OpenAI Agents SDK and Polygon.io MCP integration
- **Frontend**: React 18.2+ with Vite 5.2+ and TypeScript
- **Testing**: Playwright E2E test suite
- **Deployment**: Fixed ports (8000/3000/5500) with one-click startup

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
│   └── hooks/          # Custom hooks
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

**Warning:** This application uses AI and large language models. Outputs may contain inaccuracies and should not be treated as financial advice. Always verify information independently before making financial decisions. Use for informational purposes only.

## License

This project is licensed under the [MIT License](LICENSE).
