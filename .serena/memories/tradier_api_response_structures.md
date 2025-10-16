# Tradier API Response Structure Reference

**Last Updated**: 2025-10-15

## Historical Price Data Endpoint
**Endpoint**: `GET /v1/markets/history`

### API Response Structure

The Tradier API returns DIFFERENT structures depending on the interval parameter:

#### Daily Interval Response
```json
{
  "history": {
    "day": [
      {
        "date": "2025-10-15",
        "open": 660.65,
        "high": 670.23,
        "low": 653.17,
        "close": 665.17,
        "volume": 250042630
      },
      {
        "date": "2025-10-14",
        "open": 662.45,
        "high": 672.10,
        ...
      }
    ]
  }
}
```

**Structure**: `day` is an **ARRAY of objects**

#### Weekly Interval Response
```json
{
  "history": {
    "day": {
      "date": "2025-10-13",
      "open": 660.65,
      "high": 670.23,
      "low": 653.17,
      "close": 665.17,
      "volume": 250042630
    }
  }
}
```

**Structure**: `day` is a **SINGLE OBJECT (dict)**

#### Monthly Interval Response
```json
{
  "history": {
    "day": {
      "date": "2025-10-01",
      "open": 663.17,
      "high": 673.95,
      "low": 652.84,
      "close": 665.17,
      "volume": 863248440
    }
  }
}
```

**Structure**: `day` is a **SINGLE OBJECT (dict)**

## Code Pattern for Handling

**CORRECT Implementation** (tradier_tools.py lines 342-345):
```python
bars_data = history_data.get("day", [])
# Handle weekly/monthly: single dict vs daily: array of dicts
if isinstance(bars_data, dict):
    bars_data = [bars_data]
# Now bars_data is always an array
for bar in bars_data:
    formatted_bars.append(_format_tradier_history_bar(bar))
```

**WRONG Implementation**:
```python
bars_data = history_data.get("day", [])
for bar in bars_data:  # ← Iterates over dict KEYS when dict passed!
    formatted_bars.append(_format_tradier_history_bar(bar))  # ← Error: 'str' object has no attribute 'get'
```

## Key Insights

1. **Weekly/Monthly return single bar**: Only ONE period of data per request
   - Weekly: 1 week's OHLC in one dict
   - Monthly: 1 month's OHLC in one dict

2. **Daily returns array**: Multiple days of data in an array

3. **Field names are identical**: Same `date`, `open`, `high`, `low`, `close`, `volume` fields in both structures

4. **Solution pattern**: Use isinstance() to normalize the response type

## Tools Affected
- `get_stock_price_history()` in tradier_tools.py: Uses this endpoint
- All interval types (daily, weekly, monthly) supported
- Multi-ticker requests require separate calls (RULE #12)

## Related Rules
- RULE #4: Historical stock price data uses this endpoint
- RULE #11: Interval selection logic determines which structure is returned
- RULE #12: Single-ticker only (no comma-separated multi-ticker support)

## Bug History
- Previous Issue: Interval selection appearing broken (Tests 4, 19, 35)
- Root Cause: tradier_tools.py not handling dict vs array difference
- Fix: Added isinstance() check to normalize response structure
- Commit: e6cdda2 ([INTERVAL-FIX] Weekly/Monthly Interval Bug Fix + Error Transparency Rule)
- Status: RESOLVED ✅ (39/39 tests PASS)
