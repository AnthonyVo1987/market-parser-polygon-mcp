# FastAPI Prompt Templates System - API Documentation

## Overview

**✅ STATUS: ALL ENDPOINTS FUNCTIONAL AND VALIDATED**

The FastAPI Prompt Templates System provides a comprehensive REST API for integrating with the existing PromptTemplateManager functionality. This API enables React frontend integration while maintaining compatibility with the existing Python backend systems.

**📋 VALIDATION CONFIRMED:**
- All API endpoints are fully functional
- `/templates` and `/analysis-tools` endpoints working correctly
- TypeScript build issues resolved
- Backend integration validated with frontend testing

## Base URL

**⚠️ CRITICAL: Backend server MUST be running on port 8000**

- **Development**: `http://localhost:8000`
- **Production**: Configure as needed

**Quick Validation:**
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
# If this fails, start backend: uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Live Server Integration & Testing

The API integrates seamlessly with the VS Code Live Server setup for frontend development and testing. The Live Server configuration includes automatic API proxying to ensure proper backend communication during production build testing.

### API Proxy Configuration

Live Server is configured with automatic API proxying in all environments:

**Development Environment** (Port 5500):
```json
{
  "liveServer.settings.proxy": [
    ["/api", "http://localhost:8000"]
  ]
}
```

**Staging Environment** (Port 5501):
```json
{
  "liveServer.settings.proxy": [
    ["/api", "http://localhost:8000"]
  ]
}
```

**Production Environment** (Port 5502):
```json
{
  "liveServer.settings.proxy": [
    ["/api", "http://localhost:8000"]
  ]
}
```

### Testing API Integration with Live Server

**Prerequisites**:
1. FastAPI backend running: `uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`
2. Frontend built: `npm run build` (in frontend_OpenAI directory)
3. VS Code Live Server extension installed

**VALIDATED Testing Workflow**:

**STEP 1 (CRITICAL): Start FastAPI Backend First**
```bash
cd gpt5-openai-agents-sdk-polygon-mcp
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Expected success output:
# INFO:     Started server process [XXXXX]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

# 2. Build and serve frontend with API proxy
cd frontend_OpenAI
npm run serve  # Development testing (Port 5500)
# OR
npm run serve:staging    # Staging testing (Port 5501)
# OR  
npm run serve:production # Production testing (Port 5502)

# 3. Validate API endpoints are functional
curl http://localhost:8000/health           # Direct backend health check
curl http://localhost:8000/templates        # Templates endpoint (now working)
curl http://localhost:8000/analysis-tools   # Analysis tools endpoint (now working)

# 4. Test via Live Server proxy
curl http://localhost:5500/api/v1/health     # Via proxy
curl http://localhost:5501/api/v1/system/status  # Via proxy
```

### Cross-Device API Testing

**Mobile/Tablet Testing Setup**:
1. Ensure backend running on `http://localhost:8000`
2. Start Live Server with cross-device configuration:
   ```bash
   npm run cross-device:setup  # Find local IP
   ```
3. Access from mobile devices: `http://[LOCAL_IP]:5500/api/v1/health`
4. Test API integration on real devices with touch interfaces

### API Testing Commands

**VALIDATED Health Check Testing**:
```bash
# Direct backend (CONFIRMED WORKING)
curl http://localhost:8000/health
# Expected response: {"status":"healthy"}

# NEW: Functional endpoint testing
curl http://localhost:8000/templates
# Expected: JSON array of analysis templates

curl http://localhost:8000/analysis-tools  
# Expected: JSON array of analysis tools

# Via Live Server proxy (all environments)
curl http://localhost:5500/api/v1/health      # Development
curl http://localhost:5501/api/v1/health      # Staging  
curl http://localhost:5502/api/v1/health      # Production
```

**FUNCTIONAL Live Server API Validation**:
```bash
# Template endpoints via proxy (WORKING)
curl http://localhost:5500/api/v1/prompts/templates
# OR direct backend:
curl http://localhost:8000/templates

# Analysis endpoints via proxy
curl -X POST http://localhost:5500/api/v1/analysis/snapshot \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "analysis_type": "snapshot"}'

# Chat analysis via proxy
curl -X POST http://localhost:5500/api/v1/analysis/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Apple stock price?", "chat_history": []}'
```

### Production Build API Integration

Unlike Vite's development server, Live Server serves actual built files and requires explicit proxy configuration for API calls:

**Key Differences**:
- **Vite Dev Server**: Built-in API proxying via `vite.config.ts`
- **Live Server**: Manual proxy configuration via `.vscode/settings.json`
- **Build Testing**: Live Server validates actual production API integration
- **Environment Testing**: Multi-environment API endpoint validation

**✅ VALIDATED Integration Status**:
1. **API Connectivity**: All `/api/*` requests properly proxied to backend ✅
2. **CORS Configuration**: Cross-origin requests handled correctly ✅
3. **Error Handling**: API errors properly displayed in production build ✅
4. **Response Processing**: JSON responses correctly parsed and displayed ✅
5. **Environment Switching**: API endpoints correctly routed per environment ✅
6. **TypeScript Build**: Build errors resolved, `npm run build` now works ✅
7. **Endpoint Functionality**: `/templates` and `/analysis-tools` endpoints operational ✅

For comprehensive Live Server usage instructions, see: `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md`

## Authentication

Currently uses the existing API key system for Polygon.io access. No additional authentication required for prompt template endpoints.

## API Endpoints

### 📋 Template Management

#### GET `/api/v1/prompts/templates`

List all available prompt templates.

**Response:**
```json
{
  "mode": "conversational_only",
  "templates": {
    "snapshot": {
      "template_type": "snapshot",
      "available": true,
      "mode": "conversational",
      "enhanced_formatting": true,
      "description": "Snapshot analysis template"
    },
    "support_resistance": {
      "template_type": "support_resistance",
      "available": true,
      "mode": "conversational",
      "enhanced_formatting": true,
      "description": "Support resistance analysis template"
    },
    "technical": {
      "template_type": "technical",
      "available": true,
      "mode": "conversational",
      "enhanced_formatting": true,
      "description": "Technical analysis template"
    }
  },
  "total_count": 3
}
```

#### POST `/api/v1/prompts/generate`

Generate a prompt using specified template and parameters.

**Request Body:**
```json
{
  "template_type": "snapshot",
  "ticker": "AAPL",
  "custom_instructions": "Focus on recent performance",
  "mode": "conversational"
}
```

**Response:**
```json
{
  "prompt": "Provide a comprehensive stock snapshot analysis for AAPL (Apple Inc.)...",
  "ticker_context": {
    "symbol": "AAPL",
    "company_name": "Apple Inc.",
    "sector": "Technology",
    "last_mentioned": false,
    "confidence": 1.0,
    "source": "explicit"
  },
  "template_type": "snapshot",
  "mode": "conversational",
  "generated_at": "2024-12-01T10:30:00Z"
}
```

### 🔘 Button Analysis (React Frontend)

#### POST `/api/v1/analysis/snapshot`

Get stock snapshot analysis for button-triggered requests.

**Request Body:**
```json
{
  "ticker": "AAPL",
  "analysis_type": "snapshot"
}
```

**Response:**
```json
{
  "analysis": "📊 **Apple Inc. (AAPL) Market Snapshot**\n\n💰 **Current Price:** $150.25 (+2.5% / +$3.75)...",
  "ticker": "AAPL",
  "analysis_type": "snapshot",
  "generated_at": "2024-12-01T10:30:00Z",
  "success": true
}
```

#### POST `/api/v1/analysis/support-resistance`

Get support and resistance levels analysis.

**Request Body:**
```json
{
  "ticker": "TSLA",
  "analysis_type": "support_resistance"
}
```

#### POST `/api/v1/analysis/technical`

Get comprehensive technical analysis.

**Request Body:**
```json
{
  "ticker": "NVDA",
  "analysis_type": "technical"
}
```

### 💬 Chat Analysis

#### POST `/api/v1/analysis/chat`

Process chat messages with financial analysis using the agent system.

**Request Body:**
```json
{
  "message": "What's the current price of Apple stock?",
  "chat_history": [
    {
      "content": "Hello",
      "role": "user",
      "timestamp": "2024-12-01T10:29:00Z"
    }
  ],
  "analysis_type": "snapshot"
}
```

**Response:**
```json
{
  "response": "🎯 KEY TAKEAWAYS\n📈 Apple Inc. (AAPL) is currently trading at...",
  "analysis_type": "snapshot",
  "ticker_detected": "AAPL",
  "confidence": 0.9,
  "follow_up_questions": [
    "Would you like a detailed technical analysis for AAPL?",
    "Should we examine support and resistance levels for AAPL?",
    "Would you like to analyze a different stock?"
  ],
  "generated_at": "2024-12-01T10:30:00Z",
  "success": true
}
```

### ⚙️ System Status

#### GET `/health` or `/api/v1/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Financial Analysis API is running",
  "timestamp": "2024-12-01T10:30:00Z",
  "version": "1.0.0"
}
```

#### GET `/api/v1/system/status`

Get detailed system status and metrics.

**Response:**
```json
{
  "status": "operational",
  "metrics": {
    "api_version": "1.0.0",
    "prompt_templates_loaded": 3,
    "supported_analysis_types": [
      "snapshot",
      "support_resistance", 
      "technical"
    ],
    "uptime_seconds": null,
    "last_restart": null
  },
  "timestamp": "2024-12-01T10:30:00Z"
}
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error messages:

### 400 Bad Request
```json
{
  "detail": "This query is not related to finance. Please ask about stock prices, market data, financial analysis, economic indicators, or company financials."
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "ticker"],
      "msg": "Ticker symbol must be 1-5 characters",
      "input": "TOOLONGTICKER"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Analysis failed: [error details]"
}
```

## Data Models

### Analysis Types
- `snapshot`: Market snapshot with current price, volume, OHLC data
- `support_resistance`: Support and resistance level analysis
- `technical`: Technical analysis with indicators (RSI, MACD, moving averages)

### Prompt Modes
- `conversational`: Natural language responses with emoji formatting

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:3000` (React development server)
- `http://localhost:3001` (Alternative React port)
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`

## Integration with Existing Systems

### Prompt Template Manager
- Full integration with existing `PromptTemplateManager` class
- Automatic ticker extraction with context awareness
- Support for company name recognition (Apple → AAPL)
- Enhanced formatting with financial emojis

### Agent System
- Uses existing `process_financial_query` function
- Maintains compatibility with Pydantic AI Agent Framework
- Preserves existing error handling and guardrails
- Integrates with Polygon.io MCP server

### Response Formatting
- Maintains existing emoji-based sentiment formatting
- Preserves structured output with "🎯 KEY TAKEAWAYS" sections
- Compatible with existing FSM state management
- Supports both CLI and web interfaces

## Example Usage

### React Frontend Integration

```javascript
// Get available templates
const templates = await fetch('/api/v1/prompts/templates').then(r => r.json());

// Button click handler
const handleSnapshotClick = async (ticker) => {
  const response = await fetch('/api/v1/analysis/snapshot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ticker, analysis_type: 'snapshot' })
  });
  const data = await response.json();
  console.log(data.analysis);
};

// Chat message handler
const handleChatMessage = async (message, history) => {
  const response = await fetch('/api/v1/analysis/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, chat_history: history })
  });
  const data = await response.json();
  console.log(data.response);
};
```

### Python Client Integration

```python
import requests

# Get templates
templates = requests.get('http://localhost:8000/api/v1/prompts/templates').json()

# Generate prompt
prompt_request = {
    "template_type": "snapshot",
    "ticker": "AAPL",
    "custom_instructions": "Focus on recent performance"
}
prompt_response = requests.post(
    'http://localhost:8000/api/v1/prompts/generate',
    json=prompt_request
).json()

# Get analysis
analysis_request = {"ticker": "AAPL", "analysis_type": "snapshot"}
analysis = requests.post(
    'http://localhost:8000/api/v1/analysis/snapshot',
    json=analysis_request
).json()
```

## Running the Server

### Development
```bash
cd gpt5-openai-agents-sdk-polygon-mcp
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testing
```bash
uv run python test_api.py
```

## Environment Variables

Required environment variables:
- `POLYGON_API_KEY`: Your Polygon.io API key
- `OPENAI_API_KEY`: Your OpenAI API key

Optional configuration:
- `OPENAI_MODEL`: Model to use (default: gpt-5-mini)
- `OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M`: Input pricing (default: 0.25)
- `OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M`: Output pricing (default: 2.00)

## Security Considerations

- Input validation for all ticker symbols and user messages
- Guardrail system prevents non-financial queries
- Secure file operations with proper permissions
- Content sanitization for XSS prevention
- Rate limiting recommended for production deployment

## Performance Optimization

- Async/await throughout for better concurrency
- Efficient prompt generation with caching potential
- Minimal database operations using SQLiteSession
- GPU acceleration available for enhanced processing
- Connection pooling for MCP server interactions