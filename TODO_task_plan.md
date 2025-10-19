# Phase 2.1: aiohttp Integration - Implementation TODO Plan

**Task**: Implement aiohttp async HTTP integration (Task 1 from Phase 2)
**Branch**: v1.0.0.0_performance-optimizations
**Status**: Ready for Implementation
**Created**: 2025-10-19
**Estimated Time**: 2-4 hours
**Expected Impact**: 3x faster HTTP requests

---

## 📋 Prerequisites Check

**Phase 1 Status**:
- ✅ Phase 1 completed and committed (commit: 9578cb9)
- ✅ Gradio queue configuration working
- ✅ LRU caching operational
- ✅ Connection pooling infrastructure ready (api_utils.py exists)
- ✅ All 39 CLI tests passed (0 errors)

**Environment**:
- ✅ Python environment active (uv)
- ✅ Git branch: v1.0.0.0_performance-optimizations
- ✅ Clean working directory

**Dependencies**:
- [ ] aiohttp installed (need to verify/install)

---

## 🎯 Task Overview: aiohttp Integration

**Goal**: Replace synchronous HTTP calls with async aiohttp while maintaining backward compatibility.

**Scope**: INCREMENTAL implementation - aiohttp only (no request batching, rate limiting, or caching upgrades)

**Strategy**:
1. Verify aiohttp dependency
2. Leverage existing APIConnectionPool from Phase 1 (already has aiohttp ClientSession!)
3. Identify which functions use HTTP requests
4. Convert functions to async (create _async versions)
5. Keep sync wrappers for backward compatibility
6. Update calling code to use async functions
7. Test thoroughly

---

## 🔍 PHASE 1: DEPENDENCY & CODE ANALYSIS

### Task 1.1: Verify aiohttp Installation ⏱️ 2 minutes

**Use Serena & Sequential-Thinking**:
```bash
# Check if aiohttp is installed
uv run python -c "import aiohttp; print(f'aiohttp {aiohttp.__version__} installed')"

# If not installed:
uv add aiohttp
```

**Success Criteria**:
- ✅ aiohttp import works
- ✅ Version displayed (should be 3.9+)

---

### Task 1.2: Analyze Existing APIConnectionPool ⏱️ 5 minutes

**File**: `src/backend/tools/api_utils.py` (created in Phase 1)

**Use Sequential-Thinking + Serena**:
```
mcp__serena__get_symbols_overview("src/backend/tools/api_utils.py")
mcp__serena__find_symbol("APIConnectionPool", "src/backend/tools/api_utils.py", include_body=True)
```

**Key Observations**:
- Phase 1 already created APIConnectionPool with aiohttp.ClientSession
- Has `get_session()` method returning configured ClientSession
- Ready for use - NO CHANGES NEEDED to api_utils.py!

**Success Criteria**:
- ✅ Understand existing connection pool structure
- ✅ Confirm aiohttp ClientSession already configured
- ✅ Note: 100 max connections, 10 per host, 30s timeout

---

### Task 1.3: Identify HTTP-Using Functions ⏱️ 10 minutes

**Use Sequential-Thinking + Serena**:

**Step 1**: Search for requests library usage
```
mcp__serena__search_for_pattern("import requests", "src/backend/tools")
mcp__serena__search_for_pattern("requests.get", "src/backend/tools")
mcp__serena__search_for_pattern("requests.post", "src/backend/tools")
```

**Step 2**: Identify functions making HTTP calls
- polygon_tools.py: Check which functions call external APIs
- tradier_tools.py: Check which functions call external APIs

**Expected Functions** (from research doc):
- tradier_tools.py:
  - `get_stock_quote()` - Tradier API
  - `get_options_expiration_dates()` - Tradier API
  - `get_call_options_chain()` - Tradier API
  - `get_put_options_chain()` - Tradier API
- polygon_tools.py:
  - `get_stock_price_history()` - Polygon API (uses polygon library, not requests)
  - `get_market_status_and_date_time()` - Tradier API
  - `get_ta_indicators()` - Polygon API (uses polygon library)

**Key Insight**:
- Tradier functions use `requests` library directly
- Polygon functions use `polygon` Python library (which uses requests internally)

**Decision**:
- Convert Tradier functions to async (4 functions)
- Keep Polygon functions as-is for now (polygon library handles requests)

**Success Criteria**:
- ✅ List all functions using `requests` library
- ✅ Categorize by API (Tradier vs Polygon)
- ✅ Determine conversion priority (Tradier first)

---

## 🛠️ PHASE 2: ASYNC CONVERSION - TRADIER TOOLS

### Task 2.1: Convert get_stock_quote() to Async ⏱️ 20 minutes

**Use Sequential-Thinking + Serena**:

**Step 1**: Read current function
```
mcp__serena__find_symbol("get_stock_quote", "src/backend/tools/tradier_tools.py", include_body=True)
```

**Step 2**: Create async version

**Pattern**:
```python
# NEW: Async version
async def _get_stock_quote_async(ticker: str) -> str:
    """Async version using aiohttp."""
    from .api_utils import get_connection_pool

    try:
        # Get connection pool
        pool = get_connection_pool()
        session = await pool.get_session()

        # Build request
        url = f"https://api.tradier.com/v1/markets/quotes?symbols={ticker}"
        headers = create_tradier_headers(api_key)

        # Async HTTP call
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            # ... process response
            return json.dumps(result)

    except Exception as e:
        return create_error_response("api_error", str(e), ticker)

# KEEP: Sync wrapper for backward compatibility
@function_tool
async def get_stock_quote(ticker: str) -> str:
    """Get real-time stock quote (async)."""
    return await _get_stock_quote_async(ticker)
```

**Step 3**: Use Serena to replace function
```
mcp__serena__replace_symbol_body("get_stock_quote", "src/backend/tools/tradier_tools.py", <new_body>)
```

**Success Criteria**:
- ✅ Async version created with aiohttp
- ✅ Uses APIConnectionPool from api_utils.py
- ✅ Error handling preserved
- ✅ JSON response format maintained
- ✅ Function signature compatible with @function_tool

---

### Task 2.2: Convert get_options_expiration_dates() to Async ⏱️ 15 minutes

**Same pattern as Task 2.1**:
1. Read current function with Serena
2. Create async version with aiohttp
3. Use APIConnectionPool
4. Replace with Serena

---

### Task 2.3: Convert get_call_options_chain() to Async ⏱️ 20 minutes

**Same pattern as Task 2.1**:
1. Read current function with Serena
2. Create async version with aiohttp
3. Use APIConnectionPool
4. Replace with Serena

---

### Task 2.4: Convert get_put_options_chain() to Async ⏱️ 20 minutes

**Same pattern as Task 2.1**:
1. Read current function with Serena
2. Create async version with aiohttp
3. Use APIConnectionPool
4. Replace with Serena

---

## 🧪 PHASE 3: TESTING

### Task 3.1: Smoke Test - Individual Functions ⏱️ 10 minutes

**Test each async function manually**:
```bash
# Test get_stock_quote
timeout 30 uv run python -c "
import asyncio
from src.backend.cli import agent

async def test():
    response = await agent.run('Get SPY stock quote')
    print(response[:500])

asyncio.run(test())
"
```

**Repeat for**:
- get_stock_quote (SPY)
- get_options_expiration_dates (SPY)
- get_call_options_chain (SPY, $580, 2025-10-25)
- get_put_options_chain (SPY, $580, 2025-10-25)

**Success Criteria**:
- ✅ Each function returns valid JSON
- ✅ Response time < 15 seconds
- ✅ No runtime errors
- ✅ Data format matches expected structure

---

### Task 3.2: CLI Regression Test Suite ⏱️ 15-20 minutes

**MANDATORY CHECKPOINT - DO NOT SKIP**

**Step 1**: Run full test suite
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Step 2**: Phase 1 - Verify Test Completion
- Expected: 39/39 tests COMPLETED
- Check: No Python exceptions or import errors

**Step 3**: Phase 2a - MANDATORY Error Detection
```bash
# Command 1: Find errors
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log | head -30

# Command 2: Count data unavailable
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log

# Command 3: Count completed
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Expected Results**:
- Errors: 0
- Data unavailable: 0
- Completed: 39

**Step 4**: Phase 2c - Response Correctness (Spot Check)
- Verify Test 2 (SPY Current Price) uses aiohttp correctly
- Verify Test 14 (Call Options Chain) returns Bid/Ask columns
- Verify Test 15 (Put Options Chain) returns Bid/Ask columns
- Verify all responses are complete (not truncated)

**Success Criteria**:
- ✅ 39/39 tests COMPLETED
- ✅ 0 errors found in Phase 2a
- ✅ Response correctness verified in Phase 2c
- ✅ Average response time similar or faster than Phase 1 (5-13s)
- ✅ Test report generated: test-reports/test_cli_regression_loop1_<timestamp>.log

---

### Task 3.3: Performance Comparison ⏱️ 5 minutes

**Compare with Phase 1 baseline**:
```bash
# Phase 1 baseline: test-reports/test_cli_regression_loop1_2025-10-19_14-04.log
# Phase 2.1 current: test-reports/test_cli_regression_loop1_<new_timestamp>.log

# Calculate average response time improvement
grep "Response Time:" test-reports/test_cli_regression_loop1_<new_timestamp>.log | awk '{sum+=$3; count++} END {print "Avg:", sum/count "s"}'
```

**Expected**:
- Phase 1 avg: ~6-13 seconds
- Phase 2.1 avg: ~5-10 seconds (should be similar or slightly faster)
- Note: Major speed improvements come from request batching (Phase 2.2)

**Success Criteria**:
- ✅ Response times comparable or better than Phase 1
- ✅ No performance regression

---

## 📝 PHASE 4: DOCUMENTATION UPDATES

### Task 4.1: Update CLAUDE.md ⏱️ 10 minutes

**Section**: Last Completed Task Summary

**Content**:
```markdown
<!-- LAST_COMPLETED_TASK_START -->
[PHASE 2.1] aiohttp Integration - Async HTTP Implementation

**Summary:** Converted Tradier API functions from synchronous requests to async aiohttp, achieving foundation for 3x faster HTTP requests. Leveraged existing APIConnectionPool from Phase 1.

**Changes Implemented:**

1. **Async HTTP with aiohttp** (tradier_tools.py)
   - Converted 4 functions to async: get_stock_quote(), get_options_expiration_dates(), get_call_options_chain(), get_put_options_chain()
   - Used existing APIConnectionPool from Phase 1 (no changes to api_utils.py)
   - Maintained @function_tool compatibility
   - Preserved error handling and JSON response format

**Testing Results:**
- ✅ 39/39 CLI regression tests COMPLETED
- ✅ Phase 2a: 0 errors, 0 data unavailable
- ✅ Phase 2c: All responses verified correct
- ✅ Average response time: X.Xs (similar/faster than Phase 1)
- ✅ Test report: test-reports/test_cli_regression_loop1_<timestamp>.log

**Files Modified:**
- src/backend/tools/tradier_tools.py (4 async functions)

**Performance Impact:**
- HTTP requests now non-blocking (async foundation)
- Enables request batching in Phase 2.2
- Sets foundation for 3x faster multi-stock queries

**Next Step:** Phase 2.2 - Request Batching (parallel API calls)
<!-- LAST_COMPLETED_TASK_END -->
```

---

### Task 4.2: Create Serena Memory ⏱️ 5 minutes

**File**: `.serena/memories/phase_2_1_aiohttp_integration_completion_oct_2025.md`

**Content**:
```markdown
# Phase 2.1: aiohttp Integration Completion - October 2025

## Overview
Converted Tradier API functions from synchronous requests to async aiohttp.

## Changes

### Async Conversion (4 functions):
- get_stock_quote()
- get_options_expiration_dates()
- get_call_options_chain()
- get_put_options_chain()

### Pattern Used:
```python
async def _function_async(...):
    pool = get_connection_pool()
    session = await pool.get_session()
    async with session.get(url, headers=headers) as response:
        data = await response.json()
        return process_data(data)

@function_tool
async def function(...):
    return await _function_async(...)
```

## Testing
- All 39 CLI tests passed
- 0 errors, 0 data unavailable
- Performance comparable to Phase 1

## Next Steps
- Phase 2.2: Request batching
- Phase 2.3: Rate limiting
- Phase 2.4: Intelligent caching
```

---

## 🎯 PHASE 5: ATOMIC COMMIT

### Task 5.1: Pre-Commit Verification ⏱️ 5 minutes

**Verify ALL work complete**:
```bash
git status
git diff
```

**Checklist**:
- [ ] All 4 Tradier functions converted to async
- [ ] CLI regression tests passed (39/39)
- [ ] Test report generated
- [ ] CLAUDE.md updated
- [ ] Serena memory created
- [ ] TODO_task_plan.md updated

---

### Task 5.2: Atomic Commit ⏱️ 2 minutes

**Stage ALL files at once**:
```bash
git add -A
git status  # Verify all staged
```

**Commit immediately**:
```bash
git commit -m "$(cat <<'EOF'
[PHASE 2.1] aiohttp Integration - Async HTTP Implementation

Converted Tradier API functions from synchronous requests to async aiohttp:

Code Changes:
- Converted 4 Tradier functions to async (get_stock_quote, get_options_expiration_dates, get_call_options_chain, get_put_options_chain)
- Used existing APIConnectionPool from Phase 1 (no changes to api_utils.py)
- Maintained @function_tool compatibility with async functions
- Preserved error handling and JSON response format

Testing Results:
- 39/39 CLI regression tests COMPLETED
- Phase 2a: 0 errors, 0 data unavailable
- Phase 2c: All responses verified correct
- Average response time: X.Xs (similar/faster than Phase 1)
- Test report: test-reports/test_cli_regression_loop1_<timestamp>.log

Files Modified:
- src/backend/tools/tradier_tools.py: 4 async functions

Documentation:
- CLAUDE.md: Phase 2.1 completion summary
- .serena/memories/phase_2_1_aiohttp_integration_completion_oct_2025.md: NEW

Performance Impact:
- HTTP requests now non-blocking (async foundation)
- Enables request batching in Phase 2.2
- Foundation for 3x faster multi-stock queries

Next Step: Phase 2.2 - Request Batching

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Push immediately**:
```bash
git push
```

---

## 🛠️ MANDATORY TOOL USAGE

**Throughout ALL phases, continuously use**:
- **Sequential-Thinking**: MANDATORY START for every phase, continue throughout
- **Serena Tools**: Code analysis, symbol searches, symbol replacement
- **Standard Tools**: File operations, bash commands, git operations

**Tool Usage Pattern**:
1. START phase with Sequential-Thinking
2. Use Serena for code analysis
3. Use Serena for code modifications
4. Continue using Sequential-Thinking for complex reasoning
5. Use Standard Tools for file/git operations

---

## ✅ SUCCESS CRITERIA

**Phase 2.1 Complete When**:
- ✅ All 4 Tradier functions converted to async
- ✅ All functions use APIConnectionPool correctly
- ✅ 39/39 CLI tests pass (0 errors)
- ✅ Phase 2 manual verification complete
- ✅ Documentation updated
- ✅ Atomic commit created and pushed

---

## 🚀 READY TO START PHASE 3: IMPLEMENTATION

**Status**: TODO plan complete - Ready for autonomous implementation

**Next Action**: Begin Phase 3 (Implementation) starting with Task 1.1

---

**Last Updated**: 2025-10-19
**Branch**: v1.0.0.0_performance-optimizations
**Prerequisites**: Phase 1 complete ✅
**Estimated Total Time**: 2-4 hours
