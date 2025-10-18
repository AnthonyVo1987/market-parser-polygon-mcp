# Market Parser with Polygon MCP Server

A Python CLI and Gradio web interface for natural language financial
queries using the [Polygon.io](https://polygon.io/) MCP server and OpenAI
GPT-5 models via the OpenAI Agents SDK. Features intelligent
sentiment analysis, real-time financial data, cross-platform interfaces,
optimized AI prompts with direct analysis buttons, and **enhanced performance
with GPT-5 model-specific rate limiting and quick response optimization** for
faster financial insights.

## Features

### 🚀 **Optimized AI Prompts**

- **70% response time improvement** (6.10s avg vs 20s legacy with MCP)
- **Direct Polygon Python API** - No MCP overhead, faster data access
- **40-50% token reduction** for faster responses
- **Deterministic financial analysis** with optimized GPT-5 settings
- **Streamlined system prompts** without verbose disclaimers
- **Quick Response Optimization** - All prompts enforce minimal tool calls for faster responses
- **GPT-5 Model-Specific Rate Limiting** - Proper rate limits (200K TPM for nano)

### ⚡ **Streamlined Chat Interface**

- **Direct financial queries** through natural language chat
- **Simplified user experience** with single input method
- **Real-time AI responses** with structured financial analysis
- **Consolidated prompt system** for consistent AI behavior

### 📊 **Enhanced Performance**

**🏆 Latest Test Results (Oct 2025):**
- **Total Tests**: 36/36 PASSED ✅
- **Success Rate**: 100%
- **Average Response Time**: 10.44s (EXCELLENT rating)
- **Performance Range**: 2.188s - 31.599s
- **Session Duration**: 6 min 36 sec (persistent session)
- **Improvement**: 70% faster than legacy MCP architecture

**Technical Optimizations:**
- **Performance monitoring** with response time and token usage logging
- **Real-time response timing** with FastAPI middleware for precise performance measurement
- **Token counting** with OpenAI response metadata extraction for cost tracking
- **CLI performance metrics** display with Rich console formatting
- **Streamlined user workflow** with direct chat interface
- **Real-time market data** integration with direct Polygon Python API
- **Cross-platform compatibility** with CLI and web interfaces
- **GPT-5 Model Optimization** - Proper model specification prevents rate limiting errors
- **Quick Response System** - All AI agents prioritize speed with minimal tool calls

## Quick Start

### Prerequisites

- **[uv](https://github.com/astral-sh/uv)** - Python package manager
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

The startup script automatically starts both backend and Gradio servers.

```bash
# Start backend + Gradio UI
chmod +x start-gradio.sh && ./start-gradio.sh
```

**Prerequisites:** uv, API keys in .env

## What the Startup Script Does

### 🔄 Server Cleanup

- Kills existing development servers (uvicorn, gradio)
- **Preserves MCP servers** - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup

- **Backend**: Starts FastAPI server on `http://127.0.0.1:8000`
- **Frontend (Gradio)**: Starts Gradio ChatInterface on `http://127.0.0.1:7860`
- Opens servers in separate terminal windows for easy monitoring
- Uses consistent ports from centralized configuration (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies Gradio interface responds

### 🌐 Browser Access

- **NOTIFIES USER TO OPEN BROWSER WHEN SERVERS ARE READY**

**Access:**
- Gradio UI: <http://127.0.0.1:7860>
- Backend API: <http://127.0.0.1:8000> (API docs)

## Application Features

### ⚡ Gradio UI Features

- **Streaming Responses**: Real-time AI response streaming
- **Chat History**: Built-in conversation history
- **Example Prompts**: Pre-loaded financial query examples
- **Performance Metrics**: Response time and token usage display
- **Python Native**: No JavaScript build tools required

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

- **Gradio Web Interface** - Modern chat UI with streaming responses (port 7860)
- **Enhanced CLI** - Terminal interface with rich formatting
- **API Endpoints** - RESTful API for integration (port 8000)

## Example Usage

### Gradio Web Interface

1. Open <http://127.0.0.1:7860>
2. Select an example or type your financial query
3. Get streaming responses with financial data and analysis
4. Examples included: Stock price queries, technical analysis, options chains, stock comparisons

**Example Response:**

```text
Market Status: CLOSED
After-hours: NO
Early-hours: NO
Exchanges: NASDAQ closed, NYSE closed, OTC closed
Server Time (UTC): 2025-10-18 01:50:12

Performance Metrics:
   Response Time: 5.135s
   Tokens Used: 21,701 (Input: 21,402, Output: 299)
   Model: gpt-5-nano
```

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

## Testing

**Primary Test Suite:** `test_cli_regression.sh` (36 comprehensive tests)

**Test Coverage:**
- SPY test sequence (15 tests): Market status, prices, TA indicators, options, OHLC
- NVDA test sequence (15 tests): Same pattern as SPY
- Multi-ticker WDC/AMD/GME (6 tests): Parallel call validation

**Features:**
- Persistent session (all 36 tests in single CLI session)
- Chat history analysis validation
- Parallel tool call verification
- Dynamic relative dates (no hardcoded dates requiring updates)
- Support/Resistance redundant call detection

**Latest Results:**
- Total: 36/36 PASSED ✅
- Success Rate: 100%
- Average: 10.44s per query (EXCELLENT)
- Range: 2.188s - 31.599s
- Session Duration: 6 min 36 sec

**Run tests:**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

## Performance Optimizations

### Backend Performance

- **Direct Polygon API**: 70% faster than legacy MCP architecture
- **Optimized AI Prompts**: 40-50% token reduction
- **GPT-5 Rate Limiting**: Proper model-specific rate limits (200K TPM)
- **Quick Response System**: Minimal tool calls for faster responses

### Performance Monitoring

- **Response Time Tracking**: FastAPI middleware for precise measurement
- **Token Counting**: OpenAI metadata extraction for cost tracking
- **CLI Metrics Display**: Rich console formatting with performance data

## Architecture

- **Backend**: FastAPI with OpenAI Agents SDK v0.2.9 and Direct Polygon Python API integration
- **Frontend**: Gradio 5.49.1+ ChatInterface with async streaming (port 7860)
- **AI Models**: GPT-5 Nano (200K TPM) with proper rate limiting
- **Performance Monitoring**: FastAPI middleware for response timing and OpenAI metadata for token counting
- **Testing**: CLI regression test suite (test_cli_regression.sh - 39 comprehensive tests)
- **Deployment**: Fixed ports (8000/7860) with one-click startup script
- **Performance**: Quick response optimization with minimal tool calls for 20-40% faster responses

## Development

### Available Commands

```bash
# Application startup
chmod +x start-gradio.sh && ./start-gradio.sh  # Start backend + Gradio UI

# Testing
chmod +x test_cli_regression.sh && ./test_cli_regression.sh  # Run 36-test CLI suite

# Backend only
uv run src/backend/main.py  # CLI interface
```

### Project Structure

```text
src/
├── backend/              # FastAPI backend
│   ├── main.py          # CLI and API application
│   ├── gradio_ui.py     # Gradio web interface
│   └── api_models.py    # API schemas
config/                  # Centralized configuration
│   └── app.config.json # Non-sensitive settings
```

## Deployment

### AWS App Runner (Production)

Deploy to AWS App Runner for production hosting:

```bash
# Quick deployment
./deploy-to-apprunner.sh
```

See [DEPLOYMENT-QUICKSTART.md](DEPLOYMENT-QUICKSTART.md) for step-by-step guide or [DEPLOYMENT.md](DEPLOYMENT.md) for complete documentation.

**Features:**
- ✅ Single container deployment (backend + frontend)
- ✅ Auto-scaling (1-10 instances)
- ✅ HTTPS included
- ✅ ~$50-70/month for 24/7 operation

## Troubleshooting

### Common Issues

**Backend not starting:**

```bash
# Check .env file has API keys
cat .env | grep API_KEY

# Verify dependencies
uv install
```

**Gradio UI connection errors:**

```bash
# Verify backend is running
curl http://127.0.0.1:8000/health

# Verify Gradio is running
curl http://127.0.0.1:7860

# Check ports are available
netstat -tlnp | grep :8000
netstat -tlnp | grep :7860
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
