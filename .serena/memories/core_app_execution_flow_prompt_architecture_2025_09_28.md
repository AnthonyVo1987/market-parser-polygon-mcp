# Core App Execution Flow & Prompt Architecture

## Overview
Complete documentation of the Market Parser application's execution flow with detailed analysis of the 3-tier prompt architecture: AI Agent Instructions, System Prompt Instructions, and Message Prompts.

## 🚀 Application Startup Flow

### 1. FastAPI App Initialization
**File**: `src/backend/main.py:82-85`
```python
app = FastAPI(
    title="Market Parser API",
    description="Financial market analysis using OpenAI GPT-5 and Polygon.io MCP",
    version="1.0.0",
)
```

### 2. Lifespan Management & Resource Initialization
**File**: `src/backend/main.py:45-79`
- **Session Creation**: `SQLiteSession(settings.agent_session_name)` - Line 52
- **MCP Server Creation**: `create_polygon_mcp_server()` - Line 55
- **Resource Storage**: `set_shared_resources(shared_mcp_server, shared_session)` - Line 59

### 3. MCP Server Configuration
**File**: `src/backend/services/mcp_service.py:9-25`
- **Command**: `uvx --from git+https://github.com/polygon-io/mcp_polygon@v0.4.1 mcp_polygon`
- **Environment**: `POLYGON_API_KEY` injection
- **Timeout**: `settings.mcp_timeout_seconds`

## 💬 User Message Processing Flow

### 1. Chat Endpoint Entry
**File**: `src/backend/routers/chat.py:36-132`
- **Resource Retrieval**: `get_mcp_server()` and `get_session()` - Lines 40-41
- **Input Validation**: `stripped_message = request.message.strip()` - Line 50
- **Agent Creation**: `analysis_agent = create_agent(shared_mcp_server)` - Line 84
- **Agent Execution**: `await Runner.run(analysis_agent, stripped_message, session=shared_session)` - Line 87

## 🤖 3-Tier Prompt Architecture

### Tier 1: AI Agent Instructions (Static Foundation)
**File**: `src/backend/services/agent_service.py:11-33`
**Function**: `get_enhanced_agent_instructions()`
**Activation**: Once per agent creation
**Purpose**: Defines the agent's core personality and capabilities

```python
def get_enhanced_agent_instructions():
    datetime_context = get_current_datetime_context()  # Line 18
    return f"""You are a financial analyst with real-time market data access.

{datetime_context}

TOOLS: Use Polygon.io MCP server for live market data, prices, and financial information.
🔴 CRITICAL: YOU MUST NOT USE THE FOLLOWING UNSUPPORTED TOOLS: [list_trades, get_last_trade, list_quotes, get_last_quote] 🔴

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: Format data in bullet point format with 2 decimal points max
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details
7. Do NOT provide any of the following UNLESS SPECIFICALLY REQUESTED: analysis, key takeways, actionable recommendations"""
```

**Key Components**:
- **Role Definition**: "financial analyst with real-time market data access"
- **Dynamic DateTime Context**: Generated fresh each time agent is created
- **Tool Instructions**: Specific MCP server usage guidelines
- **Response Formatting**: Bullet points, 2 decimal places, ticker symbols
- **Behavioral Constraints**: Concise responses, minimal tool calls

### Tier 2: System Prompt Instructions (OpenAI API System Role)
**File**: `src/backend/services/agent_service.py:19-33`
**Activation**: Every API call to OpenAI
**Purpose**: Provides the system role message to OpenAI API

**System Prompt = AI Agent Instructions** (Same content as Tier 1)
- **Role**: "system"
- **Content**: Complete agent instructions with datetime context
- **Persistence**: Static throughout session, regenerated on new agent creation

### Tier 3: Message Prompts (Dynamic User Input)
**File**: `src/backend/routers/chat.py:50,87`
**Activation**: Every user interaction
**Purpose**: Captures and processes user queries

**User Message Processing**:
```python
stripped_message = request.message.strip()  # Line 50
result = await Runner.run(analysis_agent, stripped_message, session=shared_session)  # Line 87
```

**Message Structure**:
- **Role**: "user"
- **Content**: User's financial query (e.g., "What is the price of NVDA?")
- **Context**: Includes conversation history from `shared_session`

## 🔄 Complete Message Flow to OpenAI API

### Internal Message Construction (Runner.run)
The OpenAI Agents SDK internally constructs the complete message array:

```python
messages = [
    {
        "role": "system",
        "content": "You are a financial analyst with real-time market data access.\n\nCURRENT DATE AND TIME CONTEXT:\n- Today's date: Sunday, September 28, 2025\n- Current time: 04:33 PM \n- ISO format: 2025-09-28 16:33:49\n- Market status: Closed\n\nIMPORTANT: Always use the current date and time above for all financial analysis.\nDo NOT use training data cutoff dates or outdated information.\n\nTOOLS: Use Polygon.io MCP server for live market data, prices, and financial information.\n🔴 CRITICAL: YOU MUST NOT USE THE FOLLOWING UNSUPPORTED TOOLS: [list_trades, get_last_trade, list_quotes, get_last_quote] 🔴\n\nINSTRUCTIONS:\n1. Use current date/time above for all analysis\n2. Gather real-time data using available tools\n3. Structure responses: Format data in bullet point format with 2 decimal points max\n4. Include ticker symbols\n5. Respond quickly with minimal tool calls\n6. Keep responses concise - avoid unnecessary details\n7. Do NOT provide any of the following UNLESS SPECIFICALLY REQUESTED: analysis, key takeways, actionable recommendations"
    },
    {
        "role": "user",
        "content": "What is the price of NVDA?"
    }
    # Plus conversation history from shared_session
]
```

## 🎯 Key Variables & State Management

### Global State Variables
- `shared_mcp_server` → MCP server instance (persistent)
- `shared_session` → SQLite session for conversation history (persistent)
- `analysis_agent` → Agent instance with instructions (created per request)

### Per-Request Variables
- `stripped_message` → User input (dynamic)
- `result.final_output` → AI response (dynamic)
- `datetime_context` → Current date/time (regenerated per agent creation)

### Model Configuration
**File**: `src/backend/services/agent_service.py:35-49`
```python
def get_optimized_model_settings():
    return ModelSettings(
        reasoning=Reasoning(effort="low"),    # Line 40
        verbosity="low",                      # Line 41
        max_tokens=128000,                    # Line 42
        extra_args={                          # Line 43
            "service_tier": "flex",           # Line 44
            "user": "financial_analysis_agent"  # Line 45
        }
    )
```

## 📊 Execution Timeline

1. **App Startup** → Lifespan management → Resource initialization
2. **First User Message** → Agent creation → Instructions generation → API call
3. **Subsequent Messages** → Agent reuse → New user message → API call
4. **Response Processing** → `result.final_output` extraction → Return to user

## 🔧 Architecture Benefits

1. **Separation of Concerns**: Each tier has a distinct purpose
2. **Performance**: Agent reuse reduces instruction regeneration overhead
3. **Consistency**: System prompt remains stable throughout session
4. **Flexibility**: User messages are completely dynamic
5. **Context Awareness**: DateTime context ensures current market data usage
6. **Tool Integration**: MCP server provides real-time financial data access

## 🎯 Significance of 3-Tier Architecture

- **Tier 1 (AI Agent Instructions)**: Foundation layer defining agent capabilities
- **Tier 2 (System Prompt)**: OpenAI API integration layer ensuring consistent behavior
- **Tier 3 (Message Prompts)**: User interaction layer enabling dynamic queries

This architecture ensures optimal performance, consistent behavior, and flexible user interaction while maintaining real-time market data access through the MCP server integration.