# Adaptive Response Formatting Guide (October 2025)

## Overview

This guide documents the AI agent's adaptive response formatting strategy, where formatting is optimized based on data complexity.

**Purpose**: Optimize response formatting for readability and speed
**Implementation**: Pure prompt engineering (no code logic changes)
**Location**: `src/backend/services/agent_service.py` (after RULE #9, lines 287-324)

## Formatting Decision Logic

### When to Use Lists (Prioritize Speed)

**Use lists for simple responses with limited data:**

**Criteria:**
- 1-5 data points
- Single ticker queries
- Binary questions (yes/no, open/closed)
- Single TA indicator results
- Quick summaries

**Examples:**
- "What's TSLA price?" → Bulleted list with price, change, %
- "Is market open?" → Simple yes/no with hours
- "SPY RSI?" → Single RSI value with interpretation

**Format:**
```
KEY TAKEAWAYS
• Bullet point 1
• Bullet point 2
• Bullet point 3
```

**Benefits:**
- Faster to generate (fewer formatting decisions)
- Easier to scan for quick info
- Less visual clutter
- Better for mobile displays

### When to Use Tables (Prioritize Readability)

**Use tables for complex responses with multi-dimensional data:**

**Criteria:**
- 6+ data points
- Multiple ticker comparisons (2+ tickers)
- OHLC bars with multiple dates
- Multiple TA indicators (SMA 20/50/200)
- Options chain data
- Multi-dimensional data

**Examples:**
- "Compare SPY, QQQ, IWM" → Table with ticker, price, change, volume
- "SPY OHLC Q1 2025" → Table with dates, OHLC values
- "SPY SMA 20/50/200" → Table with SMA types, values, signals
- "SPY call options" → Table with strikes, prices, Greeks, IV

**Format:**
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
```

**Benefits:**
- Clearer for complex data
- Easier to compare values
- Better alignment of numbers
- Professional appearance

## Decision Tree

```
Step 1: Count data dimensions
   - Single value → Lists
   - Multiple dimensions → Tables

Step 2: Count items
   - 1-5 items → Lists
   - 6+ items → Tables

Step 3: Assess complexity
   - Simple query → Lists
   - Complex query → Tables

Step 4: Multi-ticker check
   - Multiple tickers → ALWAYS Tables
```

## Implementation Examples

### Example 1: Simple Single Ticker (List)

**Query:** "What's NVDA price?"

**Response:**
```
KEY TAKEAWAYS
• NVDA trading at $482.50 (+2.35, +0.49%)
• Intraday high: $485.20, low: $478.10
• Previous close: $480.15

TOOLS USED
• get_stock_quote(ticker='NVDA')
```

**Why List:** Single ticker, 3 simple data points, quick response needed

### Example 2: Multiple Tickers (Table)

**Query:** "Compare SPY, QQQ, IWM"

**Response:**
```
KEY TAKEAWAYS

| Ticker | Price   | Change  | % Change | Volume      |
|--------|---------|---------|----------|-------------|
| SPY    | $669.12 | +2.45   | +0.37%   | 42.5M       |
| QQQ    | $512.89 | +5.12   | +1.01%   | 38.2M       |
| IWM    | $215.34 | -0.45   | -0.21%   | 28.7M       |

DETAILED ANALYSIS
• SPY and QQQ showing bullish momentum
• IWM slightly negative, underperforming large caps

TOOLS USED
• get_stock_quote(ticker='SPY')
• get_stock_quote(ticker='QQQ')
• get_stock_quote(ticker='IWM')
```

**Why Table:** Multiple tickers, 4 data dimensions per ticker, easier to compare

### Example 3: Options Chain (Table)

**Query:** "SPY call options expiring this Friday"

**Response:**
```
📊 SPY Call Options Chain (Expiring 2025-10-10)

| Strike  | Price  | Delta | Gamma | Theta  | Vega  | IV     | Volume | OI     |
|---------|--------|-------|-------|--------|-------|--------|--------|--------|
| $665.00 | $8.50  | 0.65  | 0.08  | -0.45  | 0.12  | 18.5%  | 1,250  | 3,400  |
| $670.00 | $5.20  | 0.52  | 0.09  | -0.52  | 0.14  | 19.2%  | 2,100  | 5,200  |
| $675.00 | $2.80  | 0.38  | 0.08  | -0.48  | 0.13  | 20.1%  | 1,800  | 4,100  |

DETAILED ANALYSIS
• $670 strike showing highest volume (2,100 contracts)
• IV range 18.5%-20.1% (moderate volatility)

TOOLS USED
• get_call_options_chain(ticker='SPY', current_price=669.12, expiration_date='2025-10-10')
```

**Why Table:** 10 strikes, 8 data dimensions per strike, options data is complex

### Example 4: OHLC Custom Date Range (Table)

**Query:** "SPY OHLC for Q1 2025"

**Response:**
```
KEY TAKEAWAYS

**SPY Q1 2025 Performance:**
• Start open (2025-01-02): $589.39
• End close (2025-03-31): $559.39
• Change: -$30.00 (-5.09%)
• Period High: $613.23
• Period Low: $549.83
• Trading days: 60

| Week Ending | Open    | High    | Low     | Close   | Volume     |
|-------------|---------|---------|---------|---------|------------|
| 2025-01-03  | $589.39 | $595.20 | $585.10 | $592.45 | 125.5M     |
| 2025-01-10  | $592.50 | $608.15 | $590.30 | $605.80 | 132.8M     |
| 2025-01-17  | $606.00 | $613.23 | $602.45 | $610.25 | 145.2M     |
| ...         | ...     | ...     | ...     | ...     | ...        |

DETAILED ANALYSIS
• Q1 2025 showed -5.09% decline (bearish)
• Peak at $613.23 in mid-January
• Support found around $549.83

TOOLS USED
• get_OHLC_bars_custom_date_range(ticker='SPY', from_date='2025-01-02', to_date='2025-03-31', timespan='week', multiplier=1, limit=50000)
```

**Why Table:** Multiple dates, 5 data dimensions per date, weekly OHLC summary

### Example 5: Technical Indicators (Table)

**Query:** "SPY SMA 20/50/200"

**Response:**
```
KEY TAKEAWAYS

**SPY Technical Indicators (2025-10-09):**

| Indicator | Value   | Signal      | Price vs MA |
|-----------|---------|-------------|-------------|
| SMA-20    | $663.09 | Bullish     | +$6.03      |
| SMA-50    | $649.75 | Bullish     | +$19.37     |
| SMA-200   | $602.06 | Bullish     | +$67.06     |

**Current Price:** $669.12

DETAILED ANALYSIS
• All SMAs in bullish alignment (price > SMA-20 > SMA-50 > SMA-200)
• Strong uptrend confirmed
• Price trading 0.9% above SMA-20 (healthy momentum)

TOOLS USED
• get_ta_sma(ticker='SPY', window=20, ...)
• get_ta_sma(ticker='SPY', window=50, ...)
• get_ta_sma(ticker='SPY', window=200, ...)
```

**Why Table:** 3 SMA values, 4 data dimensions, easier to compare levels

## Table Format Requirements

### Column Structure
- **Header row**: Clear column names
- **Data rows**: Aligned values
- **Numerical alignment**: Right-aligned for numbers
- **Text alignment**: Left-aligned for text

### Formatting Guidelines
- **Prices**: $XXX.XX format
- **Percentages**: XX.XX% format
- **Volume**: Comma thousands separators (e.g., 1,250,000)
- **Greeks**: 2 decimal places (e.g., 0.65)
- **IV**: Percentage format (e.g., 18.5%)

### Markdown Syntax
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |
```

## Emoji Usage (Optional Enhancement)

**Purpose**: Enhance visual clarity and engagement

**Categories:**
- Financial: 📊 (charts/data), 📈 (bullish), 📉 (bearish), 💹 (financial data)
- Status: ✅ (positive), ⚠️ (caution), 🔴 (critical), 🟢 (good/healthy)

**Guidelines:**
- Use 2-5 emojis per response
- Prioritize clarity over decoration
- Apply sparingly to key sections

**Examples:**
- "📊 SPY Call Options Chain (Expiring 2025-10-10)"
- "📈 Bullish momentum confirmed with RSI 67.5"
- "⚠️ Approaching overbought territory (RSI > 70)"

## Performance Impact

**Lists:**
- Generation time: Fast (~100-200ms)
- Token overhead: Low (~50 tokens)
- Mobile friendly: Yes
- Readability: High for simple data

**Tables:**
- Generation time: Medium (~200-400ms)
- Token overhead: Medium (~100-200 tokens)
- Mobile friendly: Moderate (may require scrolling)
- Readability: Excellent for complex data

**Emojis:**
- Generation time: Negligible (<1ms)
- Token overhead: Very low (~2 tokens per emoji)
- Visual impact: High
- Readability: Enhanced

## Testing Validation

**Test Results (Oct 9, 2025):**
- 38/38 tests PASSED (100%)
- Average response time: 10.57s (EXCELLENT)
- Markdown tables rendered correctly in all tests
- Emoji responses validated (2-5 per response)
- Intelligent formatting validated (lists for simple, tables for complex)

**Visual Features Validated (10-Loop Baseline):**
- ✅ Markdown tables render with proper alignment (40 tables across 10 loops)
- ✅ Emojis appear consistently (320+ emojis, 2-5 per response)
- ✅ Wall analysis provides meaningful strike identification (20 analyses)
- ✅ Intelligent formatting adapts to response complexity

## Maintenance Notes

### When to Update

**Update formatting guide when:**
- Adding new data types (e.g., news sentiment, analyst ratings)
- Changing table structures (e.g., adding new columns)
- Modifying emoji usage (e.g., new categories)
- Performance optimizations needed

### Testing After Changes

**Run test suite to validate:**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Verify:**
- Tables render correctly in CLI (Rich library)
- Tables render correctly in GUI (react-markdown)
- Emojis display properly in both interfaces
- Response times remain within baseline (<15s avg)

## References

**Implementation Files:**
- `src/backend/services/agent_service.py` - Formatting instructions (lines 253-324)
  - Lines 253-263: Markdown table formatting (RULE #9)
  - Lines 275-285: Emoji response formatting
  - Lines 287-324: Intelligent response formatting (lists vs tables)

**Documentation:**
- `.serena/memories/tech_stack.md` - CLI Visual Enhancements section
- `.serena/memories/ai_agent_instructions_oct_2025.md` - System prompt rules
- `CLAUDE.md` - Last Completed Task summary

**Test Reports:**
- `test-reports/test_cli_regression_loop1_2025-10-09_12-15.log` - Single loop validation
- `test-reports/performance_baseline_10loop_2025-10-09.md` - 10-loop baseline

## Future Enhancements

**Potential improvements:**
1. **Conditional Charts** - ASCII charts for trend visualization
2. **Color Coding** - ANSI colors for CLI (green=bullish, red=bearish)
3. **Sparklines** - Inline mini-charts for price trends
4. **Adaptive Precision** - Dynamic decimal places based on value magnitude
5. **Responsive Tables** - Auto-collapse columns on mobile
6. **Interactive Tables** - Sortable columns in GUI