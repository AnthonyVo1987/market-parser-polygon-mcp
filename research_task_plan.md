# AI Agent Tool Descriptions Optimization - Research Task Plan

## Executive Summary

**Research Goal:** Optimize and reduce token usage in AI Agent Tool descriptions while maintaining functionality and regression test coverage.

**Key Findings:**
- **Current token usage:** ~2,670 tokens across 6 tool descriptions
- **Target token usage:** ~800-900 tokens (60-70% reduction)
- **Potential savings:** ~1,800 tokens (~70% reduction)
- **Risk level:** LOW (consolidation only, no functionality removal)

---

## Research Methodology

### Phase 1: Codebase Analysis ✅

**Tools Analyzed:**
1. `get_stock_quote()` - tradier_tools.py (53 lines docstring, ~450 tokens)
2. `get_options_expiration_dates()` - tradier_tools.py (45 lines, ~330 tokens)
3. `get_stock_price_history()` - tradier_tools.py (69 lines, ~500 tokens)
4. `get_options_chain_both()` - tradier_tools.py (68 lines, ~580 tokens)
5. `get_market_status_and_date_time()` - tradier_tools.py (52 lines, ~370 tokens)
6. `get_ta_indicators()` - polygon_tools.py (59 lines, ~440 tokens)

**Total:** 346 lines of docstrings, ~2,670 tokens

### Phase 2: Best Practices Research ✅

**Sources Consulted:**
1. OpenAI Agents SDK documentation (function_tool decorator usage)
2. OpenAI Python SDK documentation (function calling guidelines)
3. Prompt Engineering Guide (dair-ai/prompt-engineering-guide)
4. Context7 research on token optimization

**Key Best Practices Identified:**
- Function descriptions should be **concise and action-oriented** (1 sentence)
- Parameter descriptions should be **brief** (1 line each)
- **No verbose JSON examples** (OpenAI auto-generates schema)
- **No usage examples** in docstrings (description should be self-explanatory)
- **Focus on WHAT, not HOW** (describe purpose, not implementation)

---

## Token Inefficiency Analysis

### 1. Redundant JSON Schema Examples (~35% of tokens)

**Current Practice (INEFFICIENT):**
```python
"""
Returns:
    JSON string containing quote data.

    For single ticker:
    {
        "ticker": "AAPL",
        "current_price": 178.50,
        "change": 2.30,
        "percent_change": 1.31,
        "high": 179.20,
        "low": 176.80,
        "open": 177.00,
        "previous_close": 176.20,
        "source": "Tradier"
    }

    For multiple tickers, returns array of quote objects.
"""
```
**Token cost:** ~30-40 lines per tool = ~900 tokens total

**Optimal Practice (EFFICIENT):**
```python
"""
Returns:
    JSON string with quote data (ticker, current_price, change, percent_change, high, low, open, previous_close, source).
    Multiple tickers return array of quote objects.
"""
```
**Token cost:** ~2-3 lines per tool = ~50 tokens total
**Savings:** ~850 tokens (95% reduction)

**Rationale:**
- OpenAI automatically generates JSON schema from return type
- Agent understands structure from brief description
- Full examples are redundant and verbose

### 2. Verbose "Use this tool when..." Sections (~15% of tokens)

**Current Practice (INEFFICIENT):**
```python
"""Get real-time stock quote from Tradier API.

Use this tool when the user requests a stock quote, current price,
or real-time market data for one or more ticker symbols.

This tool provides real-time price data via Tradier API,
supporting both single and multiple ticker queries.
"""
```
**Token cost:** ~8-10 lines per tool = ~200 tokens total

**Optimal Practice (EFFICIENT):**
```python
"""Get real-time stock quote(s) for one or more tickers from Tradier API."""
```
**Token cost:** ~1 line per tool = ~25 tokens total
**Savings:** ~175 tokens (87% reduction)

**Rationale:**
- First sentence should be action-oriented and complete
- Avoid repetitive "Use this tool when..." pattern
- Agent understands usage from concise description

### 3. Redundant Notes and Bullet Points (~20% of tokens)

**Current Practice (INEFFICIENT):**
```python
"""
Note:
    - Supports major US stock exchanges (NYSE, NASDAQ, etc.)
    - Data updates in real-time during market hours
    - Returns last available price when market is closed
    - Handles up to 10 tickers per request for optimal performance
"""
```
**Token cost:** ~10-15 lines per tool = ~400 tokens total

**Optimal Practice (EFFICIENT):**
```python
"""
Note: Handles up to 10 tickers (comma-separated). Real-time updates during market hours.
"""
```
**Token cost:** ~1-2 lines per tool = ~50 tokens total
**Savings:** ~350 tokens (87% reduction)

**Rationale:**
- Many notes are self-evident from context
- Consolidate similar points into one line
- Keep only critical constraints

### 4. Verbose Examples Section (~10% of tokens)

**Current Practice (INEFFICIENT):**
```python
"""
Examples:
    - "Get AAPL stock quote"
    - "What's the current price of TSLA?"
    - "Get quotes for AAPL, TSLA, NVDA"
"""
```
**Token cost:** ~5-8 lines per tool = ~200 tokens total

**Optimal Practice (EFFICIENT):**
```python
# Remove entirely - description is self-explanatory
```
**Token cost:** 0 lines = 0 tokens
**Savings:** ~200 tokens (100% reduction)

**Rationale:**
- Agent learns usage from description, not examples
- Examples add verbosity without value
- Tool purpose is clear from brief description

### 5. Repetitive Parameter Descriptions (~10% of tokens)

**Current Practice (INEFFICIENT):**
```python
"""
Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "NVDA").
            Must be a valid ticker symbol.
"""
```
**Token cost:** ~3 lines per parameter = ~150 tokens total

**Optimal Practice (EFFICIENT):**
```python
"""
Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
"""
```
**Token cost:** ~1 line per parameter = ~50 tokens total
**Savings:** ~100 tokens (67% reduction)

**Rationale:**
- "Must be valid" is self-evident
- Single line with example is sufficient
- Avoid redundant validation statements

---

## Duplication with AI Agent System Instructions

### Analysis of Overlap

**System Instructions (get_enhanced_agent_instructions):**
- Already optimized from 657→237 lines (56% reduction) in previous task
- Contains 9 consolidated RULES for tool selection and usage

**Tool Descriptions:**
- Current: Contain usage guidance that overlaps with RULES
- Target: Remove duplication, keep only tool-specific information

**Specific Duplications Identified:**

1. **RULE #3 (Historical Data + Interval Pattern) vs get_stock_price_history()**
   - RULE #3 already explains interval selection logic (week→daily, month→monthly)
   - Tool description repeats this in parameter description
   - **Action:** Remove interval selection guidance from tool, reference RULE #3

2. **RULE #5 (Options Tools) vs get_options_chain_both()**
   - RULE #5 explains when to use options tools
   - Tool description repeats "Use Cases" section
   - **Action:** Remove use cases from tool, keep only parameter descriptions

3. **RULE #1 (Stock Quotes) vs get_stock_quote()**
   - RULE #1 explains single vs multi-ticker format
   - Tool description repeats comma-separated format details
   - **Action:** Simplify to "Comma-separated for multiple tickers"

**Estimated Additional Savings:**
- Removing duplication with RULES: ~200 tokens (8% additional reduction)

---

## Optimization Strategy

### Token Reduction Roadmap

| Category | Current Tokens | Target Tokens | Savings | % Reduction |
|----------|---------------|---------------|---------|-------------|
| JSON Examples | ~900 | ~50 | ~850 | 95% |
| "Use when" sections | ~200 | ~25 | ~175 | 87% |
| Notes & bullets | ~400 | ~50 | ~350 | 87% |
| Usage examples | ~200 | ~0 | ~200 | 100% |
| Parameter descriptions | ~150 | ~50 | ~100 | 67% |
| Duplication with RULES | ~200 | ~0 | ~200 | 100% |
| **TOTAL** | **~2,670** | **~800** | **~1,870** | **70%** |

### Optimal Tool Description Template

```python
@function_tool
async def tool_name(param1: Type1, param2: Type2) -> str:
    """[Action-oriented one-sentence description of what tool does].

    Args:
        param1: Brief description with example if needed.
        param2: Brief description with example if needed.

    Returns:
        Brief format description (key fields only).

    Note: Critical constraints only (1-2 lines max).
    """
    return await _implementation(param1, param2)
```

**Estimated tokens per tool:** ~135 tokens (vs current ~445 tokens)

---

## Validation Strategy

### Ensuring No Regression

**Critical Requirements:**
1. ✅ All 37 regression tests must pass
2. ✅ Manual testing per tool (1-2 prompts each)
3. ✅ Output formatting must remain correct
4. ✅ Tool selection logic must remain correct

**Testing Approach:**

**Phase 1: Manual CLI Testing (PER TOOL)**
- Test each tool with 1-2 representative prompts using `uv run main.py`
- Verify agent selects correct tool
- Verify response format matches expectations
- Verify tables/charts formatted correctly
- Fix any issues before proceeding to Phase 2

**Phase 2: Full Regression Testing**
- Execute complete 37-test suite: `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`
- Phase 1 (Automated): 37/37 tests must complete
- Phase 2 (Manual Verification): Verify EACH test response:
  1. Does response address query?
  2. Were RIGHT tools called (no duplicates)?
  3. Is data correct (proper tickers, formatting)?
  4. Any errors present?
- Must achieve 37/37 PASS before proceeding

**Rollback Plan:**
- If any test fails, analyze failure
- Adjust tool description to restore missing information
- Re-test until all tests pass
- Document what information was essential

---

## Risk Assessment

### Risk Level: LOW ✅

**Reasons:**
1. **No functionality removal** - Only description optimization
2. **No code changes to tools** - Only docstring modifications
3. **Proven approach** - Similar optimization succeeded (system instructions 657→237 lines)
4. **Comprehensive testing** - Manual + automated regression coverage
5. **Reversible** - Can restore descriptions if needed

**Potential Risks:**

1. **Risk:** Agent may not select correct tool
   - **Mitigation:** Maintain clear one-sentence purpose
   - **Test:** Manual testing per tool before regression suite

2. **Risk:** Agent may not understand parameters
   - **Mitigation:** Keep parameter descriptions with examples
   - **Test:** Verify parameter usage in manual testing

3. **Risk:** Output formatting may break
   - **Mitigation:** Keep critical formatting notes
   - **Test:** Verify tables/charts in manual testing

---

## Expected Outcomes

### Quantitative Benefits

- **Token Reduction:** 60-70% (~1,870 tokens saved)
- **Cost Savings:** Significant reduction in tokens per API call
- **Maintenance:** Simpler, more maintainable tool descriptions
- **Clarity:** More focused, less verbose descriptions

### Qualitative Benefits

- **Improved Readability:** Developers can understand tools faster
- **Better Alignment:** Follows OpenAI best practices
- **Reduced Duplication:** Single source of truth (system instructions)
- **Consistent Style:** All tools follow same concise template

### Success Criteria

✅ **Token reduction achieved:** 60-70% reduction (target: ~800-900 tokens)
✅ **All tests pass:** 37/37 regression tests pass with manual verification
✅ **No functionality lost:** All tools work as before
✅ **Improved clarity:** Descriptions are more concise and focused

---

## Tools and Files Involved

### Files to Modify

1. **src/backend/tools/tradier_tools.py**
   - Optimize 4 tool descriptions:
     - `get_stock_quote()` (current: ~450 tokens → target: ~130 tokens)
     - `get_options_expiration_dates()` (current: ~330 tokens → target: ~100 tokens)
     - `get_stock_price_history()` (current: ~500 tokens → target: ~150 tokens)
     - `get_options_chain_both()` (current: ~580 tokens → target: ~160 tokens)
     - `get_market_status_and_date_time()` (current: ~370 tokens → target: ~110 tokens)

2. **src/backend/tools/polygon_tools.py**
   - Optimize 1 tool description:
     - `get_ta_indicators()` (current: ~440 tokens → target: ~150 tokens)

### Files to Update (Documentation)

1. **CLAUDE.md** - Update "Last Completed Task Summary"
2. **research_task_plan.md** - This file
3. **TODO_task_plan.md** - Implementation checklist
4. **Test reports** - Evidence of passing tests

---

## Next Steps

**Immediate Actions:**
1. ✅ Research complete - This document
2. ⏭️ Create TODO_task_plan.md with granular implementation steps
3. ⏭️ Begin Phase 3: Implementation using Serena tools
4. ⏭️ Phase 4: Testing (manual + regression)
5. ⏭️ Phase 5: Atomic git commit with all changes

**Timeline Estimate:**
- Phase 2 (Planning): 15-20 minutes
- Phase 3 (Implementation): 30-40 minutes
- Phase 4 (Testing): 20-30 minutes
- Phase 5 (Commit): 10 minutes
- **Total:** ~90 minutes

---

## References

**Research Sources:**
1. OpenAI Agents SDK - Function tool documentation
2. OpenAI Python SDK - Function calling guidelines
3. Prompt Engineering Guide (dair-ai) - Token optimization strategies
4. Previous task success - System instructions optimization (657→237 lines, 56% reduction)

**Related Documentation:**
- `.serena/memories/` - Serena tools usage patterns
- `CLAUDE.md` - Project guidelines and task history
- `test_cli_regression.sh` - 37-test regression suite

---

## Conclusion

Research confirms that **60-70% token reduction is achievable** in AI Agent Tool descriptions through:
- Removing redundant JSON examples
- Condensing verbose sections
- Eliminating usage examples
- Consolidating notes
- Removing duplication with system instructions

**Risk is LOW** because:
- No functionality is being removed
- Comprehensive testing will catch issues
- Approach is proven (system instructions optimization succeeded)

**Next step:** Create detailed TODO_task_plan.md for implementation.
