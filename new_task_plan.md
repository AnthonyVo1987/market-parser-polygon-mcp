# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Context7 for research and best up to date Implementation Practices & Library documentation lookups
3. Use Serena Tools for code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
4. Use Filesystem Tools for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
5. Use Standard Read/Write/Edit for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
6. Use Playwright Tools for Testing with Browser automation for React GUI & App Validation
7. REPEAT any tool as needed throughout the process
8. 🔴 NEVER stop using tools - continue using them until task completion

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

## New Task Details

## **🤖 COMPLETE AI Agent Implementation Prompt**

### **Task: Fix OpenAI Rate Limiting, Update Polygon MCP Server, and Optimize Response Speed**

You are tasked with implementing fixes for a rate limiting issue, updating the Polygon MCP server version, and optimizing response speed in a financial analysis application. The application is incorrectly getting rate-limited with gpt-4o model limits (30,000 TPM) when it should be using gpt-5-nano (200,000 TPM) and gpt-5-mini (500,000 TPM) models.

### **🔍 Background & Root Cause**

**Application Overview:**

- **Technology Stack**: FastAPI backend, React frontend, Pydantic AI Agent Framework, Polygon.io MCP server
- **Purpose**: Financial analysis application with natural language queries
- **Current Issue**: Rate limiting errors with "Request too large for gpt-4o" (30,000 TPM limit)
- **Expected Behavior**: Should use gpt-5-nano (200,000 TPM) and gpt-5-mini (500,000 TPM)

**Root Cause Analysis:**
The Pydantic AI Agent Framework `Agent` instances are created without specifying a model parameter, causing the framework to default to `gpt-4o` model instead of using the configured `gpt-5-nano` and `gpt-5-mini` models.

**Error Example:**

```
Request too large for gpt-4o in organization org-lAuyrzHd2vdxsszI3LECrcWP on tokens per min (TPM): Limit 30000, Requested 32099
```

**Current Configuration:**

- **Available Models**: `["gpt-5-nano", "gpt-5-mini"]` (from config/app.config.json)
- **Rate Limiting**: Enabled with 500 RPM limit
- **Polygon MCP Version**: Currently "v0.4.0", needs update to "v4.1.0"

### **�� Implementation Tasks (Complete All 8 Tasks)**

#### **Task 1: Fix Model Specification in Agent Creation**

**File:** `src/backend/main.py`
**Lines:** 276, 289, 663, 964

**Problem:** `Agent` instances are created without model parameter, defaulting to gpt-4o
**Solution:** Add `model=settings.available_models[0]` parameter to all `Agent` instantiations

**Changes Required:**

```python
# Current (incorrect) - Line 276
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="""Classify if the user query is finance-related...""",
    output_type=FinanceOutput,
)

# Updated (correct)
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="""Classify if the user query is finance-related...""",
    output_type=FinanceOutput,
    model=settings.available_models[0],
)

# Current (incorrect) - Line 289
finance_analysis_agent = Agent(
    name="Financial Analysis Agent",
    instructions=get_enhanced_agent_instructions(),
    tools=[save_analysis_report],
)

# Updated (correct)
finance_analysis_agent = Agent(
    name="Financial Analysis Agent",
    instructions=get_enhanced_agent_instructions(),
    tools=[save_analysis_report],
    model=settings.available_models[0],
)

# Current (incorrect) - Line 663
analysis_agent = Agent(
    name="Financial Analysis Agent",
    instructions=get_enhanced_agent_instructions(),
    tools=[save_analysis_report],
    mcp_servers=[shared_mcp_server],
)

# Updated (correct)
analysis_agent = Agent(
    name="Financial Analysis Agent",
    instructions=get_enhanced_agent_instructions(),
    tools=[save_analysis_report],
    mcp_servers=[shared_mcp_server],
    model=settings.available_models[0],
)

# Current (incorrect) - Line 964
analysis_agent = Agent(
    name="Financial Analysis Agent",
    instructions=get_enhanced_agent_instructions(),
    tools=[save_analysis_report],
    mcp_servers=[server],
)

# Updated (correct)
analysis_agent = Agent(
    name="Financial Analysis Agent",
    instructions=get_enhanced_agent_instructions(),
    tools=[save_analysis_report],
    mcp_servers=[server],
    model=settings.available_models[0],
)
```

#### **Task 2: Enhanced Rate Limiting Configuration (GPT-5 Only)**

**File:** `config/app.config.json`
**Lines:** 30, 31

**Problem:** Rate limiting configuration doesn't specify model-specific limits
**Solution:** Add GPT-5 model-specific rate limiting configuration

**Current Configuration:**

```json
{
  "backend": {
    "security": {
      "enableRateLimiting": true,
      "rateLimitRPM": 500
    }
  }
}
```

**Updated Configuration:**

```json
{
  "backend": {
    "security": {
      "enableRateLimiting": true,
      "rateLimitRPM": 500,
      "rateLimiting": {
        "gpt5Nano": {
          "tpm": 200000,
          "rpm": 500
        },
        "gpt5Mini": {
          "tpm": 500000,
          "rpm": 500
        }
      }
    }
  }
}
```

#### **Task 3: Update Settings Class**

**File:** `src/backend/main.py`
**Lines:** 113-163 (Settings class)

**Problem:** Settings class doesn't have GPT-5 model-specific rate limiting properties
**Solution:** Add GPT-5 model-specific rate limiting properties to Settings class

**Add to Settings class (after line 150):**

```python
# GPT-5 model-specific rate limiting from config file
self.gpt5_nano_tpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Nano"]["tpm"]
self.gpt5_nano_rpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Nano"]["rpm"]
self.gpt5_mini_tpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Mini"]["tpm"]
self.gpt5_mini_rpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Mini"]["rpm"]
```

#### **Task 4: Add GPT-5 Model-Specific Rate Limiting Logic**

**File:** `src/backend/main.py`
**Lines:** After line 163 (after Settings class)

**Problem:** No utility functions for GPT-5 model-specific rate limiting
**Solution:** Add utility functions for GPT-5 rate limiting

**Add after Settings class:**

```python
def get_model_rate_limits(model: str) -> dict:
    """Get rate limits for specific GPT-5 models."""
    if model == "gpt-5-nano":
        return {"tpm": settings.gpt5_nano_tpm, "rpm": settings.gpt5_nano_rpm}
    elif model == "gpt-5-mini":
        return {"tpm": settings.gpt5_mini_tpm, "rpm": settings.gpt5_mini_rpm}
    else:
        return {"tpm": settings.gpt5_nano_tpm, "rpm": settings.gpt5_nano_rpm}  # Default fallback

def validate_request_size(request_tokens: int, model: str) -> bool:
    """Validate request size against model-specific TPM limits."""
    limits = get_model_rate_limits(model)
    return request_tokens <= limits["tpm"]

def get_model_tpm_limit(model: str) -> int:
    """Get TPM limit for specific model."""
    limits = get_model_rate_limits(model)
    return limits["tpm"]
```

#### **Task 5: Clean Up Model Enum (Remove GPT-4o)**

**File:** `src/backend/api_models.py`
**Lines:** 195-202

**Problem:** Model enum includes unused GPT-4o models
**Solution:** Remove GPT-4o models from enum since application only uses GPT-5

**Current Enum:**

```python
class AIModelId(str, Enum):
    """Enum for available AI models"""
    GPT_5_NANO = "gpt-5-nano"
    GPT_5_MINI = "gpt-5-mini"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
```

**Updated Enum:**

```python
class AIModelId(str, Enum):
    """Enum for available AI models (GPT-5 only)"""
    GPT_5_NANO = "gpt-5-nano"
    GPT_5_MINI = "gpt-5-mini"
    # Removed GPT_4O and GPT_4O_MINI
```

#### **Task 6: Update Model List Response (Remove GPT-4o)**

**File:** `src/backend/main.py`
**Lines:** 796-829

**Problem:** API response includes unused GPT-4o models
**Solution:** Remove GPT-4o models from API response

**Current Models List:**

```python
models = [
    AIModel(
        id=AIModelId.GPT_5_NANO,
        name="GPT-5 Nano",
        description="Fast and efficient model for quick responses",
        is_default=True,
        cost_per_1k_tokens=0.15,
        max_tokens=4096,
    ),
    AIModel(
        id=AIModelId.GPT_5_MINI,
        name="GPT-5 Mini",
        description="Balanced performance model",
        is_default=False,
        cost_per_1k_tokens=0.25,
        max_tokens=8192,
    ),
    AIModel(
        id=AIModelId.GPT_4O,
        name="GPT-4o",
        description="Advanced model for complex tasks",
        is_default=False,
        cost_per_1k_tokens=2.50,
        max_tokens=4096,
    ),
    AIModel(
        id=AIModelId.GPT_4O_MINI,
        name="GPT-4o Mini",
        description="Cost-effective advanced model",
        is_default=False,
        cost_per_1k_tokens=0.15,
        max_tokens=16384,
    ),
]
```

**Updated Models List:**

```python
models = [
    AIModel(
        id=AIModelId.GPT_5_NANO,
        name="GPT-5 Nano",
        description="Fast and efficient model for quick responses",
        is_default=True,
        cost_per_1k_tokens=0.15,
        max_tokens=4096,
    ),
    AIModel(
        id=AIModelId.GPT_5_MINI,
        name="GPT-5 Mini",
        description="Balanced performance model",
        is_default=False,
        cost_per_1k_tokens=0.25,
        max_tokens=8192,
    ),
    # Removed GPT_4O and GPT_4O_MINI models
]
```

#### **Task 7: Update Polygon MCP Server Version**

**Files:** `config/app.config.json` (line 30) and `src/backend/main.py` (line 316)

**Problem:** Using outdated Polygon MCP server version "v0.4.0"
**Solution:** Update to latest version "v4.1.0"

**File 1: `config/app.config.json` (line 30)**

```json
// Current
{
  "mcp": {
    "version": "v0.4.0"
  }
}

// Updated
{
  "mcp": {
    "version": "v4.1.0"
  }
}
```

**File 2: `src/backend/main.py` (line 316)**

```python
# Current
"git+https://github.com/polygon-io/mcp_polygon@v0.4.0",

# Updated
"git+https://github.com/polygon-io/mcp_polygon@v4.1.0",
```

#### **Task 8: Enforce Quick Response Optimization in All Prompts**

**Files:** `src/backend/direct_prompts.py`, `src/backend/main.py`, `src/backend/optimized_agent_instructions.py`

**Problem:** Prompts don't enforce quick response behavior
**Solution:** Add "Quick Response Needed with minimal tool calls" to all prompts

**File 1: `src/backend/direct_prompts.py` (lines 182-220)**

```python
# Current system prompts
def _build_system_prompts(self) -> Dict[AnalysisIntent, str]:
    return {
        AnalysisIntent.SNAPSHOT: """You are a financial analyst specializing in stock market snapshots.
Provide comprehensive, real-time market analysis with current price data, volume analysis, and key performance metrics.
Always include ticker symbols and structure responses with:
KEY TAKEAWAYS (bullet points)
DETAILED ANALYSIS (price, volume, trends)

Focus on actionable insights for investors.""",
        AnalysisIntent.SUPPORT_RESISTANCE: """You are a technical analyst specializing in support and resistance levels.
Analyze key price levels where stocks find support (price floors) and resistance (price ceilings).
Always include ticker symbols and structure responses with:
KEY TAKEAWAYS (bullet points)
DETAILED ANALYSIS (support/resistance levels with explanations)

Provide actionable trading insights based on technical analysis.""",
        AnalysisIntent.TECHNICAL: """You are a technical analyst specializing in comprehensive technical analysis.
Use key indicators like RSI, MACD, and moving averages to analyze momentum and trend direction.
Always include ticker symbols and structure responses with:
KEY TAKEAWAYS (bullet points)
DETAILED ANALYSIS (technical indicators and signals)

Keep analysis concise but comprehensive, focusing on essential indicators.""",
        AnalysisIntent.GENERAL: """You are a financial assistant helping with general financial queries.
Provide helpful, informative responses about stocks, market data, financial analysis, and economic indicators.
Always include ticker symbols when relevant and structure responses with:
KEY TAKEAWAYS (bullet points)
DETAILED ANALYSIS (relevant financial information)

Make responses educational and actionable for investors.""",
    }

# Updated system prompts with quick response optimization
def _build_system_prompts(self) -> Dict[AnalysisIntent, str]:
    return {
        AnalysisIntent.SNAPSHOT: """Quick Response Needed with minimal tool calls: You are a financial analyst specializing in stock market snapshots.
Provide comprehensive, real-time market analysis with current price data, volume analysis, and key performance metrics.
Always include ticker symbols and structure responses with:
KEY TAKEAWAYS (bullet points)
DETAILED ANALYSIS (price, volume, trends)

Focus on actionable insights for investors. Respond quickly with minimal tool usage.""",
        AnalysisIntent.SUPPORT_RESISTANCE: """Quick Response Needed with minimal tool calls: You are a technical analyst specializing in support and resistance levels.
Analyze key price levels where stocks find support (price floors) and resistance (price ceilings).
Always include ticker symbols and structure responses with:
KEY TAKEAWAYS (bullet points)
DETAILED ANALYSIS (support/resistance levels with explanations)

Provide actionable trading insights based on technical analysis. Respond quickly with minimal tool usage.""",
        AnalysisIntent.TECHNICAL: """Quick Response Needed with minimal tool calls: You are a technical analyst specializing in comprehensive technical analysis.
Use key indicators like RSI, MACD, and moving averages to analyze momentum and trend direction.
Always include ticker symbols and structure responses with:
KEY TAKEAWAYS (bullet points)
DETAILED ANALYSIS (technical indicators and signals)

Keep analysis concise but comprehensive, focusing on essential indicators. Respond quickly with minimal tool usage.""",
        AnalysisIntent.GENERAL: """Quick Response Needed with minimal tool calls: You are a financial assistant helping with general financial queries.
Provide helpful, informative responses about stocks, market data, financial analysis, and economic indicators.
Always include ticker symbols when relevant and structure responses with:
KEY TAKEAWAYS (bullet points)
DETAILED ANALYSIS (relevant financial information)

Make responses educational and actionable for investors. Respond quickly with minimal tool usage.""",
    }
```

**File 2: `src/backend/main.py` (lines 251-273)**

```python
# Current enhanced agent instructions
def get_enhanced_agent_instructions():
    datetime_context = get_current_datetime_context()
    return f"""You are a professional financial analyst with access to real-time market data tools.

{datetime_context}

TOOL AVAILABILITY:
You have access to the following real-time data tools:
- Polygon.io MCP server for live market data, stock prices, and financial information
- Real-time price quotes, market snapshots, and historical data
- Current market status and trading hours information
- Live financial news and market updates

INSTRUCTIONS:
1. ALWAYS use the current date and time provided above for all analysis
2. Use the available real-time data tools to gather current market information
3. Provide accurate, data-driven financial analysis and insights
4. Focus on actionable insights and clear explanations
5. When referencing dates, use the current date context provided above
6. Do NOT rely on training data cutoff dates or outdated information

Remember: You have access to real-time market data - use it to provide current, accurate analysis."""

# Updated enhanced agent instructions with quick response optimization
def get_enhanced_agent_instructions():
    datetime_context = get_current_datetime_context()
    return f"""Quick Response Needed with minimal tool calls: You are a professional financial analyst with access to real-time market data tools.

{datetime_context}

TOOL AVAILABILITY:
You have access to the following real-time data tools:
- Polygon.io MCP server for live market data, stock prices, and financial information
- Real-time price quotes, market snapshots, and historical data
- Current market status and trading hours information
- Live financial news and market updates

INSTRUCTIONS:
1. ALWAYS use the current date and time provided above for all analysis
2. Use the available real-time data tools to gather current market information
3. Provide accurate, data-driven financial analysis and insights
4. Focus on actionable insights and clear explanations
5. When referencing dates, use the current date context provided above
6. Do NOT rely on training data cutoff dates or outdated information
7. RESPOND QUICKLY with minimal tool calls to improve response latency

Remember: You have access to real-time market data - use it to provide current, accurate analysis. Prioritize speed and efficiency in your responses."""
```

**File 3: `src/backend/optimized_agent_instructions.py` (lines 28-47)**

```python
# Current static instructions
self._static_instructions = """You are a professional financial analyst with access to real-time market data tools.

{datetime_context}

TOOL AVAILABILITY:
You have access to the following real-time data tools:
- Polygon.io MCP server for live market data, stock prices, and financial information
- Real-time price quotes, market snapshots, and historical data
- Current market status and trading hours information
- Live financial news and market updates

INSTRUCTIONS:
1. ALWAYS use the current date and time provided above for all analysis
2. Use the available real-time data tools to gather current market information
3. Provide accurate, data-driven financial analysis and insights
4. Focus on actionable insights and clear explanations
5. When referencing dates, use the current date context provided above
6. Do NOT rely on training data cutoff dates or outdated information

Remember: You have access to real-time market data - use it to provide current, accurate analysis."""

# Updated static instructions with quick response optimization
self._static_instructions = """Quick Response Needed with minimal tool calls: You are a professional financial analyst with access to real-time market data tools.

{datetime_context}

TOOL AVAILABILITY:
You have access to the following real-time data tools:
- Polygon.io MCP server for live market data, stock prices, and financial information
- Real-time price quotes, market snapshots, and historical data
- Current market status and trading hours information
- Live financial news and market updates

INSTRUCTIONS:
1. ALWAYS use the current date and time provided above for all analysis
2. Use the available real-time data tools to gather current market information
3. Provide accurate, data-driven financial analysis and insights
4. Focus on actionable insights and clear explanations
5. When referencing dates, use the current date context provided above
6. Do NOT rely on training data cutoff dates or outdated information
7. RESPOND QUICKLY with minimal tool calls to improve response latency

Remember: You have access to real-time market data - use it to provide current, accurate analysis. Prioritize speed and efficiency in your responses."""
```

### **Expected Results**

- **Rate Limiting Fixed**: No more gpt-4o rate limit errors (30,000 TPM → 200,000-500,000 TPM)
- **Model Selection**: Proper GPT-5 model usage instead of defaulting to gpt-4o
- **Performance**: 20-40% faster response times with quick response optimization
- **Consistency**: All prompts (chatbot and button) optimized for quick responses
- **Version Updated**: Latest Polygon MCP server features (v0.4.0 → v4.1.0)
- **Clean Codebase**: Removed unused GPT-4o model references

### **⚠️ Important Notes**

- **No Testing Required**: User will perform testing after implementation
- **Backward Compatibility**: Maintain existing functionality
- **Error Handling**: Preserve existing error handling patterns
- **Configuration**: Update both JSON config and Python settings
- **Order Matters**: Complete all 8 tasks in the specified order
- **File Paths**: Use exact file paths and line numbers provided

### **🔧 Implementation Checklist**

- [ ] Task 1: Fix model specification in all 4 Agent instantiations
- [ ] Task 2: Update rate limiting configuration in app.config.json
- [ ] Task 3: Add GPT-5 rate limiting properties to Settings class
- [ ] Task 4: Add GPT-5 rate limiting utility functions
- [ ] Task 5: Remove GPT-4o models from AIModelId enum
- [ ] Task 6: Remove GPT-4o models from API response
- [ ] Task 7: Update Polygon MCP server version to v4.1.0
- [ ] Task 8: Add quick response optimization to all prompts

**Complete all 8 tasks in the order specified. Each task builds upon the previous ones.**
