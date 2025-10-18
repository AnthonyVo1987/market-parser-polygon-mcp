"""Markdown formatting helper functions for AI agent tool responses.

This module provides reusable helper functions for formatting tool responses
into markdown. All tools use these helpers to generate deterministic, standardized
markdown output instead of returning raw JSON.
"""


def format_strike_price(strike: float) -> str:
    """Format strike price: remove decimals for whole integers.

    Args:
        strike: Strike price as float (e.g., 185.0, 192.50)

    Returns:
        Formatted string with $ prefix:
        - Whole integers: "$185" (no decimals)
        - Non-integers: "$192.50" (with decimals)

    Examples:
        >>> format_strike_price(185.0)
        '$185'
        >>> format_strike_price(192.50)
        '$192.50'
        >>> format_strike_price(197.0)
        '$197'
    """
    if strike % 1 == 0:
        return f"${int(strike)}"
    return f"${strike:.2f}"


def format_percentage_int(value: float) -> str:
    """Format percentage as integer (no decimals).

    Args:
        value: Percentage value as float (e.g., 50.75, 149.3)

    Returns:
        Formatted string with % suffix, rounded to nearest integer

    Examples:
        >>> format_percentage_int(50.75)
        '51%'
        >>> format_percentage_int(149.3)
        '149%'
        >>> format_percentage_int(25.0)
        '25%'
    """
    return f"{round(value)}%"


def format_number_with_commas(value: int) -> str:
    """Format large numbers with comma thousands separators.

    Args:
        value: Integer value (e.g., 135391, 16023)

    Returns:
        Formatted string with comma separators

    Examples:
        >>> format_number_with_commas(135391)
        '135,391'
        >>> format_number_with_commas(16023)
        '16,023'
        >>> format_number_with_commas(0)
        '0'
    """
    return f"{value:,}"


def create_options_chain_table(
    ticker: str,
    option_type: str,
    expiration_date: str,
    current_price: float,
    options: list[dict],
) -> str:
    """Create formatted markdown table for options chain.

    Column Order: Strike ($), Bid ($), Ask ($), Delta, Vol, OI, IV, Gamma

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "NVDA")
        option_type: "call" or "put"
        expiration_date: Expiration date in YYYY-MM-DD format
        current_price: Current underlying stock price
        options: List of option dicts with required fields:
                 - strike, bid, ask, delta, gamma, implied_volatility,
                   volume, open_interest

    Returns:
        Formatted markdown string with:
        - Emoji header (📊)
        - Current price line
        - Markdown table with new column order
        - Source attribution

    Example:
        ```
        📊 SPY Call Options Chain (Expiring 2025-10-17)
        Current Price: $671.16

        | Strike ($) | Bid ($) | Ask ($) | Delta | Vol     | OI     | IV  | Gamma |
        |-----------|---------|---------|-------|---------|--------|-----|-------|
        | 672       | 1.04    | 1.10    | 0.38  | 135,391 | 16,023 | 11% | 0.10  |
        ...

        Source: Tradier
        ```
    """
    # Format option type for display
    option_type_display = "Call" if option_type == "call" else "Put"

    # Build markdown response
    lines = []
    lines.append(
        f"📊 {ticker} {option_type_display} Options Chain (Expiring {expiration_date})"
    )
    lines.append(f"Current Price: ${current_price:.2f}")
    lines.append("")

    # Table header with new column order
    lines.append(
        "| Strike ($) | Bid ($) | Ask ($) | Delta | Vol     | OI     | IV  | Gamma |"
    )
    lines.append(
        "|-----------|---------|---------|-------|---------|--------|-----|-------|"
    )

    # Table rows
    for opt in options:
        strike = format_strike_price(opt["strike"])
        bid = f"${opt['bid']:.2f}"
        ask = f"${opt['ask']:.2f}"
        delta = f"{opt['delta']:.2f}"
        vol = format_number_with_commas(opt["volume"])
        oi = format_number_with_commas(opt["open_interest"])
        iv = format_percentage_int(opt["implied_volatility"])
        gamma = f"{opt['gamma']:.2f}"

        lines.append(f"| {strike:9} | {bid:7} | {ask:7} | {delta:5} | {vol:7} | {oi:6} | {iv:3} | {gamma:5} |")

    lines.append("")
    lines.append("Source: Tradier")

    return "\n".join(lines)


def create_price_history_summary(
    ticker: str, interval: str, bars: list[dict], start_date: str, end_date: str
) -> str:
    """Create formatted markdown summary for historical pricing.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "NVDA")
        interval: "daily", "weekly", or "monthly"
        bars: List of OHLC bar dicts with keys: date, open, high, low, close, volume
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format

    Returns:
        Formatted markdown string with:
        - Emoji header (📊)
        - Date range and interval
        - Start/end prices with change ($ and %)
        - Period high/low prices
        - Number of bars/trading periods
        - Source attribution

    Example:
        ```
        📊 SPY Historical Price Data (daily, 2025-10-03 to 2025-10-10)

        Started 10/3 at $580.50, ended 10/10 at $589.20 (+$8.70, +1.50%)
        Period High: $591.13, Low: $580.50
        6 trading days

        Source: Tradier
        ```
    """
    if not bars:
        return f"📊 {ticker} Historical Price Data ({interval}, {start_date} to {end_date})\n\nNo data available\n\nSource: Tradier"

    # Calculate summary statistics
    opening_price = bars[0]["open"]
    closing_price = bars[-1]["close"]
    price_change = closing_price - opening_price
    pct_change = (price_change / opening_price) * 100

    # Calculate period high and low
    period_high = max(bar["high"] for bar in bars)
    period_low = min(bar["low"] for bar in bars)

    # Format dates for display (remove year if same year)
    start_display = start_date[5:].replace("-", "/")  # MM/DD
    end_display = end_date[5:].replace("-", "/")  # MM/DD

    # Build markdown response
    lines = []
    lines.append(
        f"📊 {ticker} Historical Price Data ({interval}, {start_date} to {end_date})"
    )
    lines.append("")

    # Summary line with start/end prices and change
    sign = "+" if price_change >= 0 else ""
    lines.append(
        f"Started {start_display} at ${opening_price:.2f}, ended {end_display} at ${closing_price:.2f} ({sign}${price_change:.2f}, {sign}{pct_change:.2f}%)"
    )

    # Period high/low
    lines.append(f"Period High: ${period_high:.2f}, Low: ${period_low:.2f}")

    # Number of bars with proper plural
    interval_label = interval if len(bars) != 1 else interval.rstrip("ly")  # Remove 'ly' for singular
    lines.append(f"{len(bars)} {interval} bars")

    lines.append("")
    lines.append("Source: Tradier")

    return "\n".join(lines)


def create_ta_indicators_table(ticker: str, indicators: dict) -> str:
    """Create formatted markdown table for technical analysis indicators.

    Consolidates ALL TA indicators into a single comprehensive table with:
    - RSI-14
    - MACD (12/26/9) with signal and histogram
    - SMA (5, 10, 20, 50, 200)
    - EMA (5, 10, 20, 50, 200)

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "NVDA")
        indicators: Dict containing all indicator data:
            {
                "rsi": {"value": float, "timestamp": str} or None,
                "macd": {
                    "macd": float,
                    "signal": float,
                    "histogram": float,
                    "timestamp": str
                } or None,
                "sma_values": [
                    {"window": int, "value": float, "timestamp": str},
                    ...
                ] or [],
                "ema_values": [
                    {"window": int, "value": float, "timestamp": str},
                    ...
                ] or []
            }

    Returns:
        Formatted markdown string with:
        - Emoji header (📊)
        - Current date line
        - Markdown table with 14 rows (or fewer if some indicators failed)
        - Source attribution

    Example:
        ```
        📊 Technical Analysis Indicators - SPY
        Current Date: 2025-10-11

        | Indicator | Period | Value | Timestamp |
        |-----------|--------|-------|-----------|
        | RSI       | 14     | 62.45 | 2025-10-11 |
        | MACD      | 12/26  | 2.34  | 2025-10-11 |
        | Signal    | 9      | 1.87  | 2025-10-11 |
        | Histogram | -      | 0.47  | 2025-10-11 |
        | SMA       | 5      | 654.23 | 2025-10-11 |
        ...

        Source: Polygon.io API
        ```
    """
    from datetime import datetime

    # Get current date for display
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Build markdown response
    lines = []
    lines.append(f"📊 Technical Analysis Indicators - {ticker}")
    lines.append(f"Current Date: {current_date}")
    lines.append("")

    # Table header
    lines.append("| Indicator | Period | Value | Timestamp |")
    lines.append("|-----------|--------|-------|-----------|")

    # RSI row
    if indicators.get("rsi"):
        rsi = indicators["rsi"]
        value = f"{rsi['value']:.2f}" if isinstance(rsi.get("value"), (int, float)) else "N/A"
        timestamp = rsi.get("timestamp", "N/A")
        # Convert Unix timestamp (int/float) to date string
        if isinstance(timestamp, (int, float)):
            from datetime import datetime
            timestamp = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")
        elif isinstance(timestamp, str) and "T" in timestamp:
            timestamp = timestamp.split("T")[0]  # Extract date only
        lines.append(f"| RSI       | 14     | {value:6} | {timestamp} |")
    else:
        lines.append(f"| RSI       | 14     | N/A    | N/A        |")

    # MACD rows (3 rows: MACD line, Signal line, Histogram)
    if indicators.get("macd"):
        macd = indicators["macd"]
        macd_value = f"{macd['macd']:.2f}" if isinstance(macd.get("macd"), (int, float)) else "N/A"
        signal_value = f"{macd['signal']:.2f}" if isinstance(macd.get("signal"), (int, float)) else "N/A"
        histogram_value = f"{macd['histogram']:.2f}" if isinstance(macd.get("histogram"), (int, float)) else "N/A"
        timestamp = macd.get("timestamp", "N/A")
        # Convert Unix timestamp (int/float) to date string
        if isinstance(timestamp, (int, float)):
            from datetime import datetime
            timestamp = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")
        elif isinstance(timestamp, str) and "T" in timestamp:
            timestamp = timestamp.split("T")[0]  # Extract date only

        lines.append(f"| MACD      | 12/26  | {macd_value:6} | {timestamp} |")
        lines.append(f"| Signal    | 9      | {signal_value:6} | {timestamp} |")
        lines.append(f"| Histogram | -      | {histogram_value:6} | {timestamp} |")
    else:
        lines.append(f"| MACD      | 12/26  | N/A    | N/A        |")
        lines.append(f"| Signal    | 9      | N/A    | N/A        |")
        lines.append(f"| Histogram | -      | N/A    | N/A        |")

    # SMA rows (5 rows: windows 5, 10, 20, 50, 200)
    sma_values = indicators.get("sma_values", [])
    expected_sma_windows = [5, 10, 20, 50, 200]
    sma_dict = {sma["window"]: sma for sma in sma_values}

    for window in expected_sma_windows:
        if window in sma_dict:
            sma = sma_dict[window]
            value = f"{sma['value']:.2f}" if isinstance(sma.get("value"), (int, float)) else "N/A"
            timestamp = sma.get("timestamp", "N/A")
            # Convert Unix timestamp (int/float) to date string
            if isinstance(timestamp, (int, float)):
                from datetime import datetime
                timestamp = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")
            elif isinstance(timestamp, str) and "T" in timestamp:
                timestamp = timestamp.split("T")[0]  # Extract date only
            lines.append(f"| SMA       | {window:<6} | {value:6} | {timestamp} |")
        else:
            lines.append(f"| SMA       | {window:<6} | N/A    | N/A        |")

    # EMA rows (5 rows: windows 5, 10, 20, 50, 200)
    ema_values = indicators.get("ema_values", [])
    expected_ema_windows = [5, 10, 20, 50, 200]
    ema_dict = {ema["window"]: ema for ema in ema_values}

    for window in expected_ema_windows:
        if window in ema_dict:
            ema = ema_dict[window]
            value = f"{ema['value']:.2f}" if isinstance(ema.get("value"), (int, float)) else "N/A"
            timestamp = ema.get("timestamp", "N/A")
            # Convert Unix timestamp (int/float) to date string
            if isinstance(timestamp, (int, float)):
                from datetime import datetime
                timestamp = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")
            elif isinstance(timestamp, str) and "T" in timestamp:
                timestamp = timestamp.split("T")[0]  # Extract date only
            lines.append(f"| EMA       | {window:<6} | {value:6} | {timestamp} |")
        else:
            lines.append(f"| EMA       | {window:<6} | N/A    | N/A        |")

    lines.append("")
    lines.append("Source: Polygon.io API")

    return "\n".join(lines)
