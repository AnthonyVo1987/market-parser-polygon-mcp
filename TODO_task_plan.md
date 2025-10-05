# TODO Task Plan: Polygon Technical Analysis Indicators Custom Tools

**Task ID**: polygon-ta-indicators
**Created**: October 5, 2025
**Status**: Planning Complete - Ready for Implementation
**Priority**: High
**Estimated Effort**: 2-3 hours

---

## 📋 Executive Summary

Create 4 new custom tools for Technical Analysis (TA) indicators using the Polygon Python Library direct API: SMA, EMA, RSI, and MACD. Follow the established pattern from commit 68a058d (get_market_status_and_date_time implementation).

**Tools to Create:**
1. `get_ta_sma` - Simple Moving Average (SMA)
2. `get_ta_ema` - Exponential Moving Average (EMA)
3. `get_ta_rsi` - Relative Strength Index (RSI) ⚠️ Note: Typo in request 'get_ta_rse' corrected to 'get_ta_rsi'
4. `get_ta_macd` - Moving Average Convergence Divergence (MACD)

**Tool Count Change**: 10 → 14 tools (+ 4 new TA indicator tools)

---

## 🎯 Success Criteria

- [ ] All 4 TA indicator custom tools implemented and working
- [ ] Pylint score: 10.00/10 for all modified Python files
- [ ] All imports verified working
- [ ] Agent instructions updated with RULE #8 for TA indicators
- [ ] Test script updated with 4 new test cases (7→11 total tests)
- [ ] All 11 tests passing with EXCELLENT performance rating
- [ ] Serena memories updated (tech_stack, project_architecture)
- [ ] CLAUDE.md updated with complete task documentation
- [ ] Clean git commit with comprehensive message

---

## 📚 Research Summary

### Polygon Python Library TA Indicators API

**Available Methods** (from `polygon.rest.indicators.py`):
- `client.get_sma()` - Returns `SMAIndicatorResults`
- `client.get_ema()` - Returns `EMAIndicatorResults`
- `client.get_rsi()` - Returns `RSIIndicatorResults`
- `client.get_macd()` - Returns `MACDIndicatorResults`

**Common Parameters**:
- `ticker` (str, required): Stock symbol
- `timespan` (str, optional): Aggregate window (day, minute, hour, week, month, quarter, year)
- `window` (int, optional): Lookback period for SMA/EMA/RSI (default varies by indicator)
- `timestamp`, `timestamp_lt`, `timestamp_lte`, `timestamp_gt`, `timestamp_gte`: Time filtering
- `adjusted` (bool, optional): Adjust for splits (default True)
- `expand_underlying` (bool, optional): Include underlying aggregates
- `order` (str, optional): Sort order (asc/desc)
- `limit` (int, optional): Result limit (default 10, max 5000)
- `series_type` (str, optional): Price type (close, open, high, low)

**MACD-Specific Parameters**:
- `short_window` (int, optional): Short EMA window (default 12)
- `long_window` (int, optional): Long EMA window (default 26)
- `signal_window` (int, optional): Signal line window (default 9)

### Previous Implementation Pattern (commit 68a058d)

**File: src/backend/tools/polygon_tools.py**
```python
# 1. Lazy client initialization helper
def _get_polygon_client():
    """Get Polygon client with API key from environment."""
    api_key = os.getenv("POLYGON_API_KEY")
    return RESTClient(api_key=api_key)

# 2. @function_tool decorated async function
@function_tool
async def tool_name() -> str:
    """Comprehensive docstring with:
    - Purpose and when to use
    - Args description
    - Returns format
    - Note section
    - Examples
    """
    try:
        client = _get_polygon_client()
        result = client.method_call()

        # Validate data
        if not result:
            return json.dumps({"error": "No data", "message": "...", "source": "Polygon.io"})

        # Format and return JSON
        return json.dumps({
            "status": "success",
            "data": result,
            "source": "Polygon.io"
        })
    except Exception as e:
        return json.dumps({
            "error": "API request failed",
            "message": f"Error details: {str(e)}",
            "source": "Polygon.io"
        })
```

**File: src/backend/services/agent_service.py**
```python
# 1. Import new tools
from ..tools.polygon_tools import get_market_status_and_date_time

# 2. Add to tools list
tools=[get_stock_quote, get_market_status_and_date_time]

# 3. Update SUPPORTED TOOLS count and list
🔴 CRITICAL: YOU MUST ONLY USE THE FOLLOWING 10 SUPPORTED TOOLS: [...]

# 4. Add new RULE for tool usage
RULE #4: MARKET STATUS & DATE/TIME = ALWAYS USE get_market_status_and_date_time()
```

### OpenAI Custom Tools Best Practices

**From docs/OPENAI_CUSTOM_TOOLS_REFERENCE.md:**
1. Use `@function_tool` decorator for automatic schema generation
2. Comprehensive docstrings with purpose, args, returns, examples
3. Type hints on all parameters
4. Return JSON strings via `json.dumps()` for structured data
5. Error handling returns helpful messages, not exceptions
6. Async for I/O operations (API calls)
7. Clear, descriptive naming (verb + noun format)

---

## 🔧 Implementation Checklist

### PHASE 1: Tool Implementation in polygon_tools.py

**File**: `src/backend/tools/polygon_tools.py`

#### 1.1: Import Additional Modules
```python
# Add to existing imports at top of file (if not already present)
from typing import Optional
```

#### 1.2: Implement get_ta_sma
- [ ] Create `get_ta_sma(ticker: str, timespan: str = "day", window: int = 50, limit: int = 10) -> str`
- [ ] Comprehensive docstring:
  - Purpose: Get Simple Moving Average indicator values
  - When to use: Technical analysis, trend identification, support/resistance
  - Args: ticker, timespan, window, limit
  - Returns: JSON with SMA values, timestamps, parameters, source
  - Examples: "SMA for SPY", "50-day moving average AAPL"
- [ ] Implementation:
  - Get client via `_get_polygon_client()`
  - Call `client.get_sma(ticker=ticker, timespan=timespan, window=window, limit=limit)`
  - Validate response (check if results exist)
  - Extract values from results list
  - Format JSON response with status, indicator, ticker, values, parameters, source
  - Error handling with try-except
  - Return JSON string

#### 1.3: Implement get_ta_ema
- [ ] Create `get_ta_ema(ticker: str, timespan: str = "day", window: int = 50, limit: int = 10) -> str`
- [ ] Comprehensive docstring:
  - Purpose: Get Exponential Moving Average indicator values
  - When to use: Technical analysis, trend following, more responsive than SMA
  - Args: ticker, timespan, window, limit
  - Returns: JSON with EMA values, timestamps, parameters, source
  - Examples: "EMA for SPY", "20-day EMA TSLA"
- [ ] Implementation:
  - Same pattern as get_ta_sma
  - Call `client.get_ema(ticker=ticker, timespan=timespan, window=window, limit=limit)`
  - Format JSON response
  - Error handling

#### 1.4: Implement get_ta_rsi
- [ ] Create `get_ta_rsi(ticker: str, timespan: str = "day", window: int = 14, limit: int = 10) -> str`
- [ ] Comprehensive docstring:
  - Purpose: Get Relative Strength Index indicator values
  - When to use: Identify overbought/oversold conditions, momentum analysis
  - Args: ticker, timespan, window (default 14), limit
  - Returns: JSON with RSI values (0-100), timestamps, parameters, source
  - Note: RSI > 70 = overbought, RSI < 30 = oversold
  - Examples: "RSI for SPY", "Relative strength index NVDA"
- [ ] Implementation:
  - Same pattern as previous tools
  - Call `client.get_rsi(ticker=ticker, timespan=timespan, window=window, limit=limit)`
  - Format JSON response
  - Error handling

#### 1.5: Implement get_ta_macd
- [ ] Create `get_ta_macd(ticker: str, timespan: str = "day", short_window: int = 12, long_window: int = 26, signal_window: int = 9, limit: int = 10) -> str`
- [ ] Comprehensive docstring:
  - Purpose: Get MACD indicator values (trend and momentum)
  - When to use: Identify trend changes, momentum shifts, buy/sell signals
  - Args: ticker, timespan, short_window, long_window, signal_window, limit
  - Returns: JSON with MACD line, signal line, histogram values, timestamps, parameters, source
  - Note: MACD crossovers indicate potential trend changes
  - Examples: "MACD for SPY", "MACD analysis AAPL"
- [ ] Implementation:
  - Call `client.get_macd(ticker=ticker, timespan=timespan, short_window=short_window, long_window=long_window, signal_window=signal_window, limit=limit)`
  - Format JSON response with MACD, signal, histogram values
  - Error handling

---

### PHASE 2: Agent Service Integration

**File**: `src/backend/services/agent_service.py`

#### 2.1: Import New Tools
- [ ] Add imports:
```python
from ..tools.polygon_tools import (
    get_market_status_and_date_time,
    get_ta_sma,
    get_ta_ema,
    get_ta_rsi,
    get_ta_macd,
)
```

#### 2.2: Update Tools List
- [ ] Update tools list in `create_agent()`:
```python
tools=[
    get_stock_quote,
    get_market_status_and_date_time,
    get_ta_sma,
    get_ta_ema,
    get_ta_rsi,
    get_ta_macd,
],  # Finnhub + Polygon direct API tools
```

#### 2.3: Update Agent Instructions - Tool Count
- [ ] Change SUPPORTED TOOLS from 10 to 14:
```python
🔴 CRITICAL: YOU MUST ONLY USE THE FOLLOWING 14 SUPPORTED TOOLS: [get_stock_quote, get_market_status_and_date_time, get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd, get_snapshot_all, get_snapshot_option, get_aggs, list_aggs, get_daily_open_close_agg, get_previous_close_agg] 🔴
```

#### 2.4: Add RULE #8 for Technical Indicators
- [ ] Add after RULE #7:
```python
RULE #8: TECHNICAL ANALYSIS INDICATORS = USE get_ta_* tools
- If the request asks for technical indicators, moving averages, RSI, MACD, or TA analysis
- Examples: "SMA for SPY", "RSI NVDA", "MACD analysis", "50-day moving average"
- 📊 Uses Polygon.io Direct API for technical analysis indicator calculations
- ✅ Available indicators:
  * get_ta_sma(ticker, timespan='day', window=50, limit=10) - Simple Moving Average
  * get_ta_ema(ticker, timespan='day', window=50, limit=10) - Exponential Moving Average
  * get_ta_rsi(ticker, timespan='day', window=14, limit=10) - Relative Strength Index (0-100)
  * get_ta_macd(ticker, timespan='day', short_window=12, long_window=26, signal_window=9, limit=10) - MACD
- ✅ Returns: JSON with indicator values, timestamps, parameters used
```

#### 2.5: Add Examples Section for TA Tools
- [ ] Add to EXAMPLES OF CORRECT TOOL CALLS:
```python
✅ "SMA for SPY" → get_ta_sma(ticker='SPY', timespan='day', window=50, limit=10)
✅ "20-day EMA NVDA" → get_ta_ema(ticker='NVDA', timespan='day', window=20, limit=10)
✅ "RSI analysis SPY" → get_ta_rsi(ticker='SPY', timespan='day', window=14, limit=10)
✅ "MACD for AAPL" → get_ta_macd(ticker='AAPL', timespan='day', short_window=12, long_window=26, signal_window=9, limit=10)
```

---

### PHASE 3: Test Suite Updates

**File**: `test_7_prompts_persistent_session.sh`

#### 3.1: Update Test Configuration
- [ ] Change test count from 7 to 11
- [ ] Update script header comments to reflect 11 tests

#### 3.2: Add New Test Prompts
- [ ] Add 4 new prompts to prompts array (after existing 7):
```bash
declare -a prompts=(
    # ... existing 7 prompts ...
    "SMA Indicator: SPY"
    "EMA Indicator: SPY"
    "RSI Indicator: SPY"
    "MACD Indicator: SPY"
)
```

#### 3.3: Add New Test Names
- [ ] Add 4 new test names to test_names array:
```bash
declare -a test_names=(
    # ... existing 7 test names ...
    "Test_8_SMA_Indicator_SPY"
    "Test_9_EMA_Indicator_SPY"
    "Test_10_RSI_Indicator_SPY"
    "Test_11_MACD_Indicator_SPY"
)
```

#### 3.4: Verify Test Count Variables
- [ ] Ensure `total_tests=${#prompts[@]}` correctly counts 11 tests
- [ ] Update any hardcoded test count references from 7 to 11

---

### PHASE 4: Code Quality & Validation

#### 4.1: Python Code Quality
- [ ] Run pylint on polygon_tools.py:
```bash
uv run pylint src/backend/tools/polygon_tools.py --max-line-length=100
```
- [ ] Target score: 10.00/10
- [ ] Fix any linting issues

- [ ] Run pylint on agent_service.py:
```bash
uv run pylint src/backend/services/agent_service.py --max-line-length=100
```
- [ ] Target score: 10.00/10
- [ ] Fix any linting issues

#### 4.2: Code Formatting
- [ ] Run black formatter:
```bash
uv run black src/backend/tools/polygon_tools.py --line-length 100
uv run black src/backend/services/agent_service.py --line-length 100
```

- [ ] Run isort:
```bash
uv run isort src/backend/tools/polygon_tools.py --profile black --line-length 100
uv run isort src/backend/services/agent_service.py --profile black --line-length 100
```

#### 4.3: Import Verification
- [ ] Test polygon_tools.py imports:
```bash
PYTHONPATH=. uv run python -c "from src.backend.tools.polygon_tools import get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd; print('✅ Polygon tools imports successful')"
```

- [ ] Test agent_service.py imports:
```bash
PYTHONPATH=. uv run python -c "from src.backend.services.agent_service import create_agent; print('✅ Agent service imports successful')"
```

#### 4.4: CLI Testing
- [ ] Run full test suite:
```bash
./test_7_prompts_persistent_session.sh
```

- [ ] Verify:
  - All 11/11 tests PASS
  - Average response time < 30s (EXCELLENT rating)
  - Session persistence validated (single session)
  - Test report generated successfully

- [ ] Review test report:
```bash
cat test-reports/persistent_session_test_*.txt
```

---

### PHASE 5: Documentation Updates

#### 5.1: Update CLAUDE.md

**File**: `CLAUDE.md`

- [ ] Update "Last Completed Task Summary" section
- [ ] Replace content between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->`
- [ ] New summary should include:
  - Task title: "polygon-ta-indicators"
  - Tool count change: 10 → 14
  - List of 4 new tools
  - Implementation details with checkmarks
  - Test results (11/11 PASSED)
  - Pylint scores (10.00/10)
  - Tool architecture change
  - Critical rules updated (added RULE #8)
  - Achievement statement

**Example Template**:
```markdown
<!-- LAST_COMPLETED_TASK_START -->
polygon-ta-indicators: Create 4 Technical Analysis indicator custom tools using Polygon Python Library

- Created 4 new TA indicator custom tools using Polygon.io direct API
- Expanded tool capabilities with SMA, EMA, RSI, and MACD indicators
- Created custom tools using @function_tool decorator with Polygon Python Library (polygon-api-client v1.15.4)
- Updated AI Agent instructions: Added RULE #8 for TA indicators
- Increased to 14 total tools (7 Polygon.io MCP + 1 Finnhub custom + 4 Polygon TA + 2 Polygon direct)
- Enhanced technical analysis capabilities for financial queries
- All tools follow established pattern from get_market_status_and_date_time

Implementation Details:
✅ Extended src/backend/tools/polygon_tools.py with 4 TA indicator functions
✅ get_ta_sma: Simple Moving Average with configurable window
✅ get_ta_ema: Exponential Moving Average for trend following
✅ get_ta_rsi: Relative Strength Index (0-100) for momentum analysis
✅ get_ta_macd: MACD indicator with signal line and histogram
✅ Integrated into agent via tools=[...get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd]
✅ Updated decision tree and added RULE #8 for TA indicator tool selection
✅ Pylint score: 10.00/10 (clean code, no linting errors) for both files
✅ CLI Tests: 11/11 PASSED, XX.XXs avg response time, EXCELLENT performance
✅ Updated Serena memories: tech_stack and project_architecture
✅ Test suite expanded from 7 to 11 tests with 4 new TA indicator test cases

Tool Architecture Change:
- **BEFORE:** 10 tools (7 Polygon.io MCP + 1 Finnhub + 1 Polygon direct + 1 removed)
- **AFTER:** 14 tools (7 Polygon.io MCP + 1 Finnhub + 4 Polygon TA + 2 Polygon direct)
- **ADDED:** get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd
- **PATTERN:** All TA tools follow polygon_tools.py established pattern

Critical Rules Updated:
🔴 RULE #1: Single ticker → get_stock_quote(ticker='SYMBOL') via Finnhub
🔴 RULE #2: Multiple tickers → get_snapshot_all(tickers=['S1','S2'], market_type='stocks') via Polygon.io MCP
🔴 RULE #4: Market status & date/time → get_market_status_and_date_time() via Polygon Direct API
🔴 RULE #8: Technical indicators → get_ta_* tools via Polygon Direct API ⭐ NEW
🔴 SUPPORTED TOOLS: Updated from 10 to 14 tools in agent instructions

ACHIEVEMENT: Successfully expanded technical analysis capabilities with 4 new TA indicator tools, enabling comprehensive financial market analysis
<!-- LAST_COMPLETED_TASK_END -->
```

#### 5.2: Update Serena tech_stack Memory

**File**: `.serena/memories/tech_stack.md`

- [ ] Add section for TA indicator tools under "Financial Data APIs"
- [ ] Update tool count: 10 → 14
- [ ] Document 4 new TA tools with descriptions
- [ ] Update "Tool Distribution" section

**Example Addition**:
```markdown
### Technical Analysis Indicators (Polygon Direct API)
- **get_ta_sma** - Simple Moving Average calculation
- **get_ta_ema** - Exponential Moving Average calculation
- **get_ta_rsi** - Relative Strength Index (0-100 momentum indicator)
- **get_ta_macd** - Moving Average Convergence Divergence (trend + momentum)
- **Purpose**: Provide technical analysis indicators for financial market analysis
- **Pattern**: Follows polygon_tools.py established pattern
```

#### 5.3: Update Serena project_architecture Memory

**File**: `.serena/memories/project_architecture.md`

- [ ] Update "Backend Tool Architecture" section
- [ ] Update tool count from 10 to 14
- [ ] Add TA tools to tool distribution breakdown
- [ ] Update data flow diagram to include TA indicator tools

**Example Update**:
```markdown
## Backend Tool Architecture

### Tool Distribution (14 Total)
1. **Finnhub Custom Tools (1)**: get_stock_quote
2. **Polygon Direct API Tools (6)**: get_market_status_and_date_time, get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd, (1 removed: get_market_status)
3. **Polygon MCP Tools (7)**: get_snapshot_all, get_snapshot_option, get_aggs, list_aggs, get_daily_open_close_agg, get_previous_close_agg

### Technical Analysis Tools
All TA indicator tools use Polygon.io direct API via `RESTClient`:
- SMA: Trend identification, support/resistance
- EMA: Trend following, more responsive than SMA
- RSI: Overbought/oversold conditions (>70 / <30)
- MACD: Trend changes and momentum shifts
```

---

### PHASE 6: Git Commit & Push

#### 6.1: Stage Changes
- [ ] Stage all modified and new files:
```bash
git add src/backend/tools/polygon_tools.py
git add src/backend/services/agent_service.py
git add test_7_prompts_persistent_session.sh
git add CLAUDE.md
git add .serena/memories/tech_stack.md
git add .serena/memories/project_architecture.md
git add test-reports/persistent_session_test_*.txt
git add TODO_task_plan.md
git add new_task_details.md
```

#### 6.2: Verify Staged Changes
- [ ] Review staged changes:
```bash
git status
git diff --cached
```

#### 6.3: Create Comprehensive Commit
- [ ] Create commit with detailed message:
```bash
git commit -m "$(cat <<'EOF'
[POLYGON-TA-INDICATORS] Create 4 Technical Analysis indicator custom tools

- Create 4 new TA indicator custom tools using Polygon Python Library direct API
- Expand tool capabilities: SMA, EMA, RSI, MACD for technical analysis
- Update AI Agent instructions: Add RULE #8 for TA indicator tool selection
- Increase to 14 total tools (7 Polygon.io MCP + 1 Finnhub + 4 Polygon TA + 2 Polygon direct)
- Expand test suite from 7 to 11 tests with 4 new TA indicator test cases
- All tools follow established pattern from get_market_status_and_date_time

Implementation Details:
✅ Extend src/backend/tools/polygon_tools.py with 4 TA indicator functions
✅ get_ta_sma: Simple Moving Average (configurable window, default 50)
✅ get_ta_ema: Exponential Moving Average (configurable window, default 50)
✅ get_ta_rsi: Relative Strength Index (0-100, default window 14)
✅ get_ta_macd: MACD with signal line (configurable windows: 12/26/9)
✅ Integrate into agent via tools list in create_agent()
✅ Update decision tree and add RULE #8 to agent instructions
✅ Expand test suite to 11 tests (4 new TA indicator tests)
✅ Pylint score: 10.00/10 (clean code, no linting errors)
✅ CLI Tests: 11/11 PASSED, XX.XXs avg response time, EXCELLENT performance
✅ Update Serena memories: tech_stack and project_architecture
✅ Update CLAUDE.md with complete task documentation

Tool Architecture Change:
- BEFORE: 10 tools (7 Polygon.io MCP + 1 Finnhub + 2 Polygon direct - 1 removed)
- AFTER: 14 tools (7 Polygon.io MCP + 1 Finnhub + 4 Polygon TA + 2 Polygon direct)
- ADDED: get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd
- PATTERN: All TA tools follow polygon_tools.py established pattern

Agent Instructions Updates:
- Tool Count: 10 → 14 in SUPPORTED TOOLS list
- Added RULE #8: TECHNICAL ANALYSIS INDICATORS = USE get_ta_* tools
- Updated examples with TA indicator tool usage
- Decision tree includes TA indicator selection

Test Suite Updates:
- Test Count: 7 → 11 tests
- Added Test 8: SMA Indicator SPY
- Added Test 9: EMA Indicator SPY
- Added Test 10: RSI Indicator SPY
- Added Test 11: MACD Indicator SPY
- All tests running in persistent single session

Test Results:
- CLI Test Suite: 11/11 PASSED (100% success rate)
- Average Response Time: XX.XXs (EXCELLENT performance)
- Session Mode: Persistent single session validated
- Test Report: test-reports/persistent_session_test_TIMESTAMP.txt

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### 6.4: Push to Remote
- [ ] Push commit to remote repository:
```bash
git push
```

- [ ] Verify push successful:
```bash
git log -1 --oneline
```

---

## 🔍 JSON Response Format Specifications

### SMA/EMA Response Format
```json
{
  "status": "success",
  "indicator": "sma",  // or "ema"
  "ticker": "SPY",
  "values": [
    {
      "timestamp": "2025-10-05T00:00:00Z",
      "value": 450.25
    },
    ...
  ],
  "parameters": {
    "timespan": "day",
    "window": 50
  },
  "count": 10,
  "source": "Polygon.io"
}
```

### RSI Response Format
```json
{
  "status": "success",
  "indicator": "rsi",
  "ticker": "SPY",
  "values": [
    {
      "timestamp": "2025-10-05T00:00:00Z",
      "value": 62.45  // 0-100 scale
    },
    ...
  ],
  "parameters": {
    "timespan": "day",
    "window": 14
  },
  "interpretation": {
    "overbought_threshold": 70,
    "oversold_threshold": 30
  },
  "count": 10,
  "source": "Polygon.io"
}
```

### MACD Response Format
```json
{
  "status": "success",
  "indicator": "macd",
  "ticker": "SPY",
  "values": [
    {
      "timestamp": "2025-10-05T00:00:00Z",
      "macd": 2.34,
      "signal": 1.87,
      "histogram": 0.47
    },
    ...
  ],
  "parameters": {
    "timespan": "day",
    "short_window": 12,
    "long_window": 26,
    "signal_window": 9
  },
  "count": 10,
  "source": "Polygon.io"
}
```

### Error Response Format (All Tools)
```json
{
  "error": "API request failed",
  "message": "Failed to retrieve SMA data from Polygon.io: [detailed error message]",
  "source": "Polygon.io"
}
```

---

## 📝 Implementation Notes

### Important Considerations

1. **Typo Correction**: The research request mentioned 'get_ta_rse' which should be 'get_ta_rsi' (Relative Strength Index)

2. **Default Parameters**:
   - SMA/EMA window: 50 (commonly used for long-term trends)
   - RSI window: 14 (industry standard)
   - MACD windows: 12/26/9 (standard MACD parameters)
   - Timespan: "day" (daily aggregates)
   - Limit: 10 (reasonable default for recent data)

3. **Error Handling**: All tools must handle:
   - Missing/invalid API responses
   - Network errors
   - Invalid ticker symbols
   - Empty result sets
   - Polygon API errors

4. **Performance**: Expected average response time < 30s for EXCELLENT rating

5. **Code Quality**: Maintain 10.00/10 Pylint score for both files

6. **Testing**: All 11 tests must pass in persistent single session mode

---

## 🎯 Definition of Done

Task is complete when ALL of the following are true:

- [x] Research phase completed with Sequential-Thinking
- [ ] All 4 TA indicator tools implemented in polygon_tools.py
- [ ] All 4 tools properly integrated in agent_service.py
- [ ] Agent instructions updated with RULE #8 and examples
- [ ] Test suite expanded to 11 tests with 4 new TA test cases
- [ ] Pylint score 10.00/10 for polygon_tools.py
- [ ] Pylint score 10.00/10 for agent_service.py
- [ ] All imports verified working
- [ ] CLI test suite passing 11/11 tests
- [ ] Average response time < 30s (EXCELLENT rating)
- [ ] Session persistence validated (single session)
- [ ] CLAUDE.md updated with comprehensive task summary
- [ ] Serena tech_stack memory updated
- [ ] Serena project_architecture memory updated
- [ ] Git commit created with comprehensive message
- [ ] Changes pushed to remote repository
- [ ] All test reports generated and saved

---

## 📚 Reference Materials

### Key Files
- **Polygon Indicators Source**: `polygon/rest/indicators.py` (from Polygon Python Library)
- **Previous Implementation**: Commit `68a058d` - get_market_status_and_date_time
- **OpenAI Tools Reference**: `docs/OPENAI_CUSTOM_TOOLS_REFERENCE.md`
- **Test Script**: `test_7_prompts_persistent_session.sh`

### Documentation Links
- Polygon.io Indicators API: https://polygon.io/docs/stocks/get_v1_indicators_sma__stockticker
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/tools/
- Polygon Python Client: https://github.com/polygon-io/client-python

---

## 🚀 Ready to Implement

This plan is comprehensive and ready for implementation. All research is complete, patterns are established, and the path forward is clear.

**Estimated Implementation Time**: 2-3 hours
**Complexity**: Medium (following established pattern)
**Risk Level**: Low (well-researched, clear implementation path)

🔴 **CRITICAL REMINDER**: This is a PLANNING document only. DO NOT START IMPLEMENTATION until user explicitly approves this plan and requests implementation to begin.

---

**Plan Created**: October 5, 2025
**Status**: ✅ READY FOR APPROVAL
