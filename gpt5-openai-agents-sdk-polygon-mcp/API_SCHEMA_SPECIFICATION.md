# Market Parser API Schema Specification

**Version:** 1.0.0  
**Generated:** 2025-01-10  
**Phase:** 3 - Standardize API Contracts  

## Overview

This document defines the standardized API contracts for the Market Parser application, ensuring consistent response formats across all 3 button analysis types and proper frontend-backend integration.

## Core Analysis Types & Icon Mappings

### Official Analysis Type Definitions

| Analysis Type | API Value | Display Icon | Endpoint |
|---------------|-----------|--------------|----------|
| **Stock Snapshot** | `snapshot` | 📈 | `/api/v1/analysis/snapshot` |
| **Support/Resistance** | `support_resistance` | 🎯 | `/api/v1/analysis/support-resistance` |
| **Technical Analysis** | `technical` | 🔧 | `/api/v1/analysis/technical` |

### Icon Usage Standards

- **📈 Stock Snapshot**: Current market data, price movements, volume analysis
- **🎯 Support/Resistance**: Key price levels, trading ranges, breakout analysis  
- **🔧 Technical Analysis**: RSI, MACD, moving averages, momentum indicators

## Standardized Response Schema

### Universal Response Format

All analysis endpoints MUST return responses following this exact structure:

```markdown
🎯 KEY TAKEAWAYS
• 📈 [Bullish indicators with ticker symbol]
• 📉 [Bearish indicators with ticker symbol]
• 💰 [Financial impact analysis]

📊 DETAILED ANALYSIS
[Comprehensive analysis with explicit ticker mentions]

⚠️ DISCLAIMER
Not financial advice. For informational purposes only.
```

### Sentiment Emoji Standards

| Emoji | Usage | Context |
|-------|-------|---------|
| 📈 | Bullish indicators | Positive trends, growth, buy signals |
| 📉 | Bearish indicators | Negative trends, declines, sell signals |
| 💰 | Profit/gains | Revenue, profits, positive financial impact |
| 💸 | Losses | Costs, losses, negative financial impact |
| 🏢 | Company info | Corporate data, business fundamentals |
| 📊 | Neutral analysis | Data, metrics, statistical information |

## API Endpoint Specifications

### 1. Stock Snapshot Analysis

**Endpoint:** `POST /api/v1/analysis/snapshot`

**Request Model:**
```json
{
  "ticker": "string (1-5 chars, required)",
  "analysis_type": "snapshot"
}
```

**Response Model:**
```json
{
  "analysis": "string (formatted markdown with 🎯 KEY TAKEAWAYS)",
  "ticker": "string",
  "analysis_type": "snapshot", 
  "generated_at": "datetime",
  "success": true
}
```

**Response Content Requirements:**
- Current price with percentage change and ticker symbol
- Trading volume and volume analysis
- OHLC data (Open, High, Low, Close) with context
- Market cap and relevant fundamentals
- Clear explanations for potential investors

### 2. Support & Resistance Analysis

**Endpoint:** `POST /api/v1/analysis/support-resistance`

**Request Model:**
```json
{
  "ticker": "string (1-5 chars, required)",
  "analysis_type": "support_resistance"
}
```

**Response Model:**
```json
{
  "analysis": "string (formatted markdown with 🎯 KEY TAKEAWAYS)",
  "ticker": "string",
  "analysis_type": "support_resistance",
  "generated_at": "datetime", 
  "success": true
}
```

**Response Content Requirements:**
- 3 key support levels with strength ratings
- 3 key resistance levels with strength ratings
- Current price context relative to levels
- Trading strategy recommendations
- Price target explanations

### 3. Technical Analysis

**Endpoint:** `POST /api/v1/analysis/technical`

**Request Model:**
```json
{
  "ticker": "string (1-5 chars, required)",
  "analysis_type": "technical"
}
```

**Response Model:**
```json
{
  "analysis": "string (formatted markdown with 🎯 KEY TAKEAWAYS)",
  "ticker": "string", 
  "analysis_type": "technical",
  "generated_at": "datetime",
  "success": true
}
```

**Response Content Requirements:**
- RSI, MACD, and moving average analysis with current values
- Momentum and trend direction assessment
- Bullish/bearish signals with strength ratings
- Trading recommendations based on technical setup
- Clear explanations of indicator meanings

## Enhanced Chat Analysis Endpoint

**Endpoint:** `POST /api/v1/analysis/chat`

**Request Model:**
```json
{
  "message": "string (min 2 chars)",
  "chat_history": [
    {
      "content": "string",
      "role": "user|assistant",
      "timestamp": "datetime (optional)"
    }
  ],
  "analysis_type": "snapshot|support_resistance|technical (optional)"
}
```

**Response Model:**
```json
{
  "response": "string (formatted markdown with 🎯 KEY TAKEAWAYS)",
  "analysis_type": "snapshot|support_resistance|technical (optional)",
  "ticker_detected": "string (optional)",
  "confidence": 0.0-1.0,
  "follow_up_questions": ["string array"],
  "generated_at": "datetime",
  "success": true
}
```

## Legacy Compatibility Endpoints

### Templates Endpoint

**Endpoint:** `GET /templates`

**Response Model:**
```json
{
  "success": true,
  "templates": [
    {
      "id": "snapshot",
      "type": "snapshot", 
      "name": "Stock Snapshot Analysis",
      "description": "Stock Snapshot analysis template",
      "template": "Provide snapshot analysis for {ticker}",
      "icon": "📈",
      "requiresTicker": true,
      "followUpQuestions": ["string array"]
    }
  ],
  "total_count": 3
}
```

### Analysis Tools Endpoint  

**Endpoint:** `GET /analysis-tools`

**Response Model:**
```json
{
  "success": true,
  "tools": [
    {
      "id": "snapshot",
      "name": "Stock Snapshot Analysis", 
      "description": "Get snapshot analysis for any stock",
      "icon": "📈",
      "endpoint": "/api/v1/analysis/snapshot",
      "requiresTicker": true,
      "category": "financial_analysis"
    }
  ],
  "total_count": 3
}
```

## Error Response Standards

### Standard Error Format

```json
{
  "error": "string (human-readable error message)",
  "detail": "string (detailed error information)",
  "status_code": 400|500,
  "timestamp": "datetime"
}
```

### Common Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | Bad Request | Invalid ticker symbol or missing required fields |
| 400 | Guardrail | Query not finance-related (triggered by guardrail) |
| 500 | Server Error | Agent processing error or MCP server failure |
| 500 | Internal Error | Unexpected server error |

## Response Processing Pipeline

### Unified Processing Architecture

All analysis endpoints use the same core processing function:

1. **Input Validation** - Validate ticker symbol and request parameters
2. **Query Generation** - Generate analysis-specific prompt using PromptTemplateManager
3. **Agent Processing** - Process via `process_financial_query()` with MCP server
4. **Response Formatting** - Apply standardized "🎯 KEY TAKEAWAYS" formatting
5. **Output Validation** - Ensure emoji usage and ticker symbol inclusion

### Prompt Template Requirements

All prompts MUST include these formatting instructions:

```text
RESPONSE FORMATTING GUIDELINES:
- ALWAYS start responses with '🎯 KEY TAKEAWAYS' section using bullet points
- Explicitly mention the ticker symbol ({ticker}) throughout the response
- Use sentiment emojis directly: 📈 for bullish indicators, 📉 for bearish indicators
- Place emojis at the beginning of relevant bullet points for immediate visual sentiment
- Follow this structure: 🎯 KEY TAKEAWAYS, 📊 DETAILED ANALYSIS, ⚠️ DISCLAIMER
- End with standard disclaimers in a clearly formatted section
```

## Frontend Integration Guidelines

### Current State Issues

1. **Frontend Only Uses Legacy Endpoint**: Currently only calls `/chat` instead of structured button endpoints
2. **Type Misalignment**: Frontend uses `technical_analysis` but API uses `technical`
3. **Missing Button Integration**: Button analysis endpoints exist but aren't consumed

### Recommended Frontend Updates

#### 1. Update API Service Layer

```typescript
// Add button analysis methods to api_OpenAI.ts
export async function getStockSnapshot(ticker: string): Promise<ButtonAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analysis/snapshot`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ticker, analysis_type: 'snapshot' })
  });
  return response.json();
}

export async function getSupportResistance(ticker: string): Promise<ButtonAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analysis/support-resistance`, {
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ticker, analysis_type: 'support_resistance' })
  });
  return response.json();
}

export async function getTechnicalAnalysis(ticker: string): Promise<ButtonAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analysis/technical`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }, 
    body: JSON.stringify({ ticker, analysis_type: 'technical' })
  });
  return response.json();
}
```

#### 2. Update Type Definitions

```typescript
// Update AnalysisType in chat_OpenAI.ts
export type AnalysisType = 'snapshot' | 'support_resistance' | 'technical';

// Add button response interface
export interface ButtonAnalysisResponse {
  analysis: string;
  ticker: string; 
  analysis_type: AnalysisType;
  generated_at: string;
  success: boolean;
}
```

#### 3. Button Component Integration

```typescript
// Update button components to use dedicated endpoints
const handleAnalysisClick = async (type: AnalysisType, ticker: string) => {
  const response = await getAnalysisForType(type, ticker);
  onPromptGenerated(response.analysis);
};
```

## Validation Checklist

### Response Format Validation

- [ ] **🎯 KEY TAKEAWAYS** section present at start
- [ ] **📊 DETAILED ANALYSIS** section included  
- [ ] **⚠️ DISCLAIMER** section at end
- [ ] Ticker symbol mentioned explicitly throughout
- [ ] Sentiment emojis used correctly (📈 bullish, 📉 bearish)
- [ ] Professional tone with educational content
- [ ] Proper markdown formatting for readability

### API Contract Validation

- [ ] All 3 button types use correct icons (📈, 🎯, 🔧)
- [ ] Consistent request/response models across endpoints
- [ ] Proper error handling with standard error format
- [ ] Legacy endpoints maintain backward compatibility
- [ ] Frontend types align with backend API models

### Integration Validation  

- [ ] Frontend can consume all button analysis endpoints
- [ ] Type definitions match API response structures
- [ ] Error handling covers all error scenarios
- [ ] Loading states handled properly during API calls

## Implementation Priority

### Phase 3 Completion Requirements

1. **✅ API Contract Documentation** - This document defines standardized contracts
2. **⚠️ Frontend Integration Gap** - Frontend still uses legacy `/chat` only
3. **⚠️ Type Alignment Issue** - `technical_analysis` vs `technical` naming mismatch  
4. **✅ Response Format Standardization** - All endpoints use consistent "🎯 KEY TAKEAWAYS" format
5. **✅ Icon Mapping Standardization** - Official mappings documented and validated

### Next Phase Recommendations

1. **Update Frontend API Integration** - Implement button-specific endpoint calls
2. **Align Type Definitions** - Fix naming inconsistencies between frontend/backend  
3. **Add Response Validation** - Implement client-side validation of response format
4. **Enhance Error Handling** - Improve error user experience with specific error types

---

**Document Status:** ✅ COMPLETE  
**API Schema:** ✅ STANDARDIZED  
**Validation:** ✅ DOCUMENTED  
**Integration Guidelines:** ✅ PROVIDED  

This specification serves as the authoritative API contract for all Market Parser implementations.