# User Guide - JSON Features

**Market Parser Enhanced User Experience**

**Date**: 2025-08-17  
**Version**: 2.0.0  
**Target Audience**: End Users and Power Users

---

## Table of Contents

1. [What's New](#whats-new)
2. [Getting Started](#getting-started)
3. [Enhanced Web Interface](#enhanced-web-interface)
4. [Structured Data Analysis](#structured-data-analysis)
5. [Understanding JSON Output](#understanding-json-output)
6. [Real-time Status and Loading](#real-time-status-and-loading)
7. [Error Messages and Recovery](#error-messages-and-recovery)
8. [Export and Data Access](#export-and-data-access)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Features](#advanced-features)

---

## What's New

Market Parser has been completely reimagined with a new JSON-based architecture that provides:

### Key Improvements for Users

- **Reliable Data Format**: Consistent, structured responses every time
- **Enhanced UI Components**: Dedicated buttons for specific analysis types
- **Real-time Feedback**: Step-by-step progress indicators during analysis
- **Structured Data Display**: Clean, formatted tables instead of raw text
- **JSON Text Boxes**: Access to raw structured data for export and analysis
- **Better Error Handling**: Clear error messages with recovery suggestions
- **Confidence Scoring**: Data quality indicators to help assess reliability

### Before and After Comparison

**Before (Text-based)**:
```
AAPL is currently trading at $150.25, up 2.5% or $3.75 for the day. 
Volume is 45,000,000 shares with a VWAP of $149.80...
```

**After (Structured JSON)**:
```
✅ High Confidence Data (95%)

Current Price    $150.25
Change %         +2.5%
Change $         +$3.75
Volume           45,000,000
VWAP            $149.80
```

---

## Getting Started

### Prerequisites

1. **Environment Setup**: Ensure you have your API keys configured
   ```env
   POLYGON_API_KEY=your_polygon_key
   OPENAI_API_KEY=your_openai_key
   ```

2. **Installation**: Follow the standard installation process
   ```bash
   uv install
   ```

3. **Launch Web Interface**:
   ```bash
   uv run chat_ui.py
   ```

### First Time Usage

1. **Open the Web Interface**: Navigate to `http://127.0.0.1:7860`
2. **Start with a General Query**: Try "What is the current price of Apple stock?"
3. **Use Analysis Buttons**: Click "Stock Snapshot" for structured data
4. **Explore JSON Output**: Check the "Raw JSON Response" sections

---

## Enhanced Web Interface

### Layout Overview

The new interface features several key areas:

```
┌─────────────────────────────────────────────────────────────┐
│                     Market Parser                           │
├─────────────────────────────────────────────────────────────┤
│  Chat Input: [Enter your question about stocks...]          │
│  [Submit] [Clear Chat]                                      │
├─────────────────────────────────────────────────────────────┤
│  Analysis Buttons:                                          │
│  [Stock Snapshot] [Support & Resistance] [Technical]       │
├─────────────────────────────────────────────────────────────┤
│  Chat History:                                              │
│  User: What's the price of AAPL?                           │
│  Assistant: Apple is trading at $150.25...                 │
├─────────────────────────────────────────────────────────────┤
│  Structured Data Display:                                   │
│  [Table showing current analysis results]                   │
├─────────────────────────────────────────────────────────────┤
│  Raw JSON Output: (for debugging/export)                    │
│  [JSON textbox with structured response]                    │
├─────────────────────────────────────────────────────────────┤
│  Status: Ready | Processing... | Error                      │
│  Debug Info: [Current state and system information]         │
└─────────────────────────────────────────────────────────────┘
```

### Key Interface Elements

#### 1. Chat Input Area
- **Primary Input**: Standard text input for natural language queries
- **Submit Button**: Process your question
- **Clear Chat**: Reset conversation history

#### 2. Analysis Buttons
- **Stock Snapshot**: Get current price and trading metrics
- **Support & Resistance**: Technical analysis price levels
- **Technical Analysis**: Indicators and moving averages

#### 3. Structured Data Display
- **Formatted Tables**: Clean presentation of analysis results
- **Confidence Indicators**: Data quality scores
- **Warning Messages**: Alerts about data limitations

#### 4. JSON Text Boxes
- **Raw Response Data**: Complete JSON output from AI
- **Export Ready**: Copy data for external analysis
- **Debugging Aid**: Inspect exact response structure

---

## Structured Data Analysis

### Stock Snapshot Analysis

**Purpose**: Get current trading data and key metrics for any stock

**How to Use**:
1. Mention a stock ticker in chat (e.g., "Tell me about Apple")
2. Click the **"Stock Snapshot"** button
3. View results in the structured data table

**Example Output**:

| Metric | Value |
|--------|-------|
| Current Price | $150.25 |
| Percentage Change | +2.5% |
| Dollar Change | +$3.75 |
| Volume | 45,000,000 |
| VWAP | $149.80 |
| Open | $148.50 |
| High | $151.00 |
| Low | $147.25 |
| Previous Close | $146.50 |
| Data Confidence | 95.0% |

**JSON Structure**:
```json
{
  "metadata": {
    "timestamp": "2025-08-17T10:30:00Z",
    "ticker_symbol": "AAPL",
    "confidence_score": 0.95
  },
  "snapshot_data": {
    "current_price": 150.25,
    "percentage_change": 2.5,
    "dollar_change": 3.75,
    "volume": 45000000,
    "vwap": 149.80,
    "open": 148.50,
    "high": 151.00,
    "low": 147.25,
    "close": 146.50
  }
}
```

### Support & Resistance Analysis

**Purpose**: Identify key technical price levels for trading decisions

**How to Use**:
1. Discuss a stock in the chat
2. Click **"Support & Resistance"** button
3. Review price levels and strength indicators

**Example Output**:

| Level | Price |
|-------|-------|
| S1 (Support 1) | $145.50 (Strong, 90%) |
| S2 (Support 2) | $142.00 (Moderate, 80%) |
| S3 (Support 3) | $138.75 (Weak, 70%) |
| R1 (Resistance 1) | $155.25 (Moderate, 85%) |
| R2 (Resistance 2) | $158.50 (Strong, 90%) |
| R3 (Resistance 3) | $162.00 (Weak, 75%) |

**Understanding the Data**:
- **S1, S2, S3**: Support levels (prices where stock might find buying support)
- **R1, R2, R3**: Resistance levels (prices where stock might face selling pressure)
- **Strength**: How reliable the level is (Strong > Moderate > Weak)
- **Confidence %**: System confidence in the calculated level

### Technical Analysis

**Purpose**: Get technical indicators and moving averages for trend analysis

**How to Use**:
1. Reference a stock ticker in conversation
2. Click **"Technical Analysis"** button
3. Analyze indicators and moving averages

**Example Output**:

| Indicator | Value |
|-----------|-------|
| RSI | 68.5 (Neutral) |
| MACD | 0.250 / 0.180 (Bullish) |
| EMA 5 | $151.20 |
| EMA 10 | $149.85 |
| EMA 20 | $147.50 |
| EMA 50 | $144.75 |
| SMA 5 | $150.95 |
| SMA 10 | $148.75 |
| SMA 20 | $146.80 |
| SMA 50 | $143.90 |

**Understanding Technical Indicators**:
- **RSI (Relative Strength Index)**: Momentum indicator (0-100)
  - Above 70: Potentially overbought
  - Below 30: Potentially oversold
  - 30-70: Neutral zone
- **MACD**: Trend-following momentum indicator
  - Bullish: MACD line above signal line
  - Bearish: MACD line below signal line
- **EMA/SMA**: Moving averages for trend identification
  - Price above MA: Potential uptrend
  - Price below MA: Potential downtrend

---

## Understanding JSON Output

### Why JSON Matters

JSON (JavaScript Object Notation) provides:
- **Consistency**: Same structure every time
- **Reliability**: Validated data format
- **Export Ready**: Easy to use in other tools
- **Machine Readable**: Perfect for automated analysis

### JSON Structure Explained

Every response follows this general pattern:

```json
{
  "metadata": {
    // Information about the analysis
    "timestamp": "When the analysis was performed",
    "ticker_symbol": "Stock ticker (e.g., AAPL)",
    "confidence_score": "Data quality (0.0 to 1.0)",
    "schema_version": "Format version for compatibility"
  },
  "analysis_data": {
    // The actual analysis results
    // Structure varies by analysis type
  },
  "validation": {
    // Data quality indicators (optional)
    "warnings": "Any data quality concerns"
  }
}
```

### Reading Confidence Scores

**Confidence Score Range**: 0.0 to 1.0 (displayed as percentage)

- **0.90-1.00 (90-100%)**: High quality, real-time data
- **0.75-0.89 (75-89%)**: Good quality, may be slightly delayed
- **0.60-0.74 (60-74%)**: Acceptable quality, some data limitations
- **Below 0.60 (<60%)**: Lower quality, use with caution

### Common JSON Sections

#### Metadata Section
Always present in every response:
```json
"metadata": {
  "timestamp": "2025-08-17T10:30:00Z",
  "ticker_symbol": "AAPL",
  "confidence_score": 0.95,
  "schema_version": "1.0"
}
```

#### Analysis Data Section
Varies by analysis type:

**Snapshot Data**:
```json
"snapshot_data": {
  "current_price": 150.25,
  "percentage_change": 2.5,
  "volume": 45000000
}
```

**Technical Data**:
```json
"oscillators": {
  "RSI": {"value": 68.5, "interpretation": "neutral"}
},
"moving_averages": {
  "exponential": {"EMA_20": 147.50}
}
```

---

## Real-time Status and Loading

### Understanding Status Indicators

The interface provides real-time feedback during processing:

#### Status Messages

1. **"Ready"**: System is ready for new requests
2. **"Processing..."**: Analyzing your request
3. **"Extracting ticker..."**: Finding stock symbol from conversation
4. **"Generating prompt..."**: Creating structured analysis request
5. **"Querying AI..."**: Getting response from AI model
6. **"Processing response..."**: Parsing and validating data
7. **"Complete"**: Analysis finished successfully
8. **"Error"**: Something went wrong (see error details)

#### Loading Progress

During analysis, you'll see step-by-step progress:

```
Step 1/5: Initializing analysis request... [████████████████████] 100%
Elapsed: 0.5s | Estimated remaining: 0.0s

✅ Analysis complete in 2.3 seconds
```

#### Button States

- **Enabled**: Button is clickable and ready
- **Disabled**: Button is grayed out during processing
- **Processing**: Button shows loading indicator

### Response Time Expectations

**Typical Response Times**:
- **Stock Snapshot**: 2-4 seconds
- **Support & Resistance**: 3-6 seconds
- **Technical Analysis**: 4-8 seconds

**Factors Affecting Speed**:
- Market hours (faster during trading hours)
- Data complexity
- Network connectivity
- AI model response time

---

## Error Messages and Recovery

### Common Error Types

#### 1. Ticker Not Found
**Message**: "Could not identify stock ticker from conversation"

**Solution**:
- Mention the stock ticker clearly (e.g., "AAPL", "Tesla", "TSLA")
- Try asking about the stock first: "What do you know about Apple stock?"

#### 2. Data Quality Issues
**Message**: "Medium confidence data - some fields may be incomplete"

**What it means**: The response was parsed successfully but may be missing some information

**Action**: Review the confidence score and warnings, data is still usable

#### 3. Parsing Failures
**Message**: "Failed to parse structured response, showing text format"

**What it means**: The AI didn't respond in the expected JSON format

**Action**: The system will fall back to text parsing, try the request again

#### 4. API Errors
**Message**: "Unable to fetch market data - API error"

**Possible causes**:
- Market data service is down
- API rate limits exceeded
- Authentication issues

**Action**: Wait a moment and try again, check API key configuration

### Recovery Strategies

#### Automatic Recovery
The system automatically:
1. **Retries failed requests** (up to 3 times)
2. **Falls back to text parsing** if JSON parsing fails
3. **Provides partial data** when possible
4. **Maintains conversation context** across errors

#### Manual Recovery
If problems persist:
1. **Clear the chat** and start fresh
2. **Refresh the page** to reset the interface
3. **Check your internet connection**
4. **Verify API keys** are correctly configured

#### Error Log Access
For technical users, detailed error information is available:
- **Debug Panel**: Shows technical error details
- **Browser Console**: Additional debugging information
- **Log Files**: Server-side error logs

---

## Export and Data Access

### Copying JSON Data

**Method 1: Direct Copy**
1. Click on the JSON text box for your analysis type
2. Select all text (Ctrl+A / Cmd+A)
3. Copy to clipboard (Ctrl+C / Cmd+C)

**Method 2: Export Button** (Future Feature)
- Click "Export JSON" to download data file
- Choose from multiple formats (JSON, CSV, Excel)

### Using Exported Data

#### In Excel or Google Sheets
1. Copy the JSON data
2. Use "Data → Get Data from JSON" or similar import function
3. Select the fields you want to import

#### In Python Analysis
```python
import json
import pandas as pd

# Paste your JSON data
json_data = """{"metadata": {...}, "snapshot_data": {...}}"""

# Parse and analyze
data = json.loads(json_data)
snapshot = data['snapshot_data']

# Create DataFrame
df = pd.DataFrame([snapshot])
print(df)
```

#### In Trading Applications
Many trading platforms can import JSON data:
1. Save JSON to a .json file
2. Import using your platform's data import feature
3. Use for backtesting or analysis

### Data Retention

**Session Data**: Available while browser tab is open
**Persistent Storage**: Currently not saved automatically
**Recommendation**: Export important analysis results immediately

---

## Troubleshooting

### Performance Issues

#### Slow Response Times
**Symptoms**: Analysis takes longer than 10 seconds

**Possible Causes**:
- High AI model load
- Network connectivity issues
- Complex analysis requests

**Solutions**:
1. Wait for current request to complete
2. Simplify your question
3. Try during off-peak hours
4. Check internet connection

#### Interface Freezing
**Symptoms**: Buttons don't respond, status stuck

**Solutions**:
1. Refresh the page
2. Clear browser cache
3. Try a different browser
4. Check browser console for errors

### Data Quality Issues

#### Low Confidence Scores
**Symptoms**: Confidence consistently below 80%

**Possible Causes**:
- AI model not following JSON format consistently
- Market data quality issues
- Ticker recognition problems

**Solutions**:
1. Be more specific with stock names
2. Use official ticker symbols (AAPL, not Apple)
3. Try during market hours for better data

#### Missing Data Fields
**Symptoms**: Some table rows show "N/A" or missing values

**This is normal when**:
- Market is closed (some real-time data unavailable)
- Stock has limited trading history
- Data provider has temporary issues

**Not a problem if**:
- Confidence score is still reasonable (>70%)
- Essential data is present
- Warnings explain the limitations

### Browser Compatibility

#### Recommended Browsers
- **Chrome**: Full feature support
- **Firefox**: Full feature support
- **Safari**: Full feature support
- **Edge**: Full feature support

#### Known Issues
- **Internet Explorer**: Not supported
- **Mobile browsers**: Limited support for JSON text boxes

### Getting Help

#### Self-Help Resources
1. **This User Guide**: Comprehensive feature documentation
2. **Error Messages**: Usually provide specific guidance
3. **Debug Panel**: Technical details for troubleshooting

#### Reporting Issues
When reporting problems, please include:
- **What you were trying to do**
- **Exact error message**
- **Browser and version**
- **Steps to reproduce the issue**
- **Screenshot of the error (if applicable)**

---

## Advanced Features

### Debug Mode

**Accessing Debug Information**:
1. Look for the "Debug Info" section at the bottom of the interface
2. Shows current system state and processing details
3. Useful for understanding what the system is doing

**Debug Information Includes**:
- Current FSM state
- Last processing time
- Token usage statistics
- Error details and warnings

### Power User Tips

#### Efficient Workflow
1. **Start with general questions** to establish stock context
2. **Use analysis buttons** for structured data
3. **Export JSON immediately** after getting good results
4. **Monitor confidence scores** to assess data quality

#### Advanced Ticker Usage
- **Multiple tickers**: "Compare AAPL and MSFT"
- **Sector analysis**: "Technology stocks analysis"
- **Index components**: "S&P 500 top performers"

#### JSON Schema Understanding
For technical users who want to understand the data structure:
- Each analysis type has a defined JSON schema
- Schemas ensure consistent data format
- Validation happens automatically
- Custom parsers can be built using the schema definitions

### Integration Possibilities

#### API Development
The JSON format makes it easy to build:
- **Custom dashboards** using the structured data
- **Automated trading alerts** based on technical indicators
- **Portfolio analysis tools** using multiple stock data
- **Mobile apps** with the same data structure

#### Educational Use
The structured format is perfect for:
- **Finance courses** teaching technical analysis
- **Programming tutorials** working with financial data
- **Research projects** requiring consistent data format
- **Backtesting platforms** needing historical analysis

---

## Conclusion

The new JSON-based architecture of Market Parser provides a significant upgrade in reliability, usability, and data access. The structured format ensures consistent results while maintaining the natural language interface that makes financial analysis accessible to everyone.

### Key Takeaways

1. **Reliability**: JSON format ensures consistent, validated responses
2. **Usability**: Enhanced interface with structured data display
3. **Transparency**: Access to raw JSON for export and analysis
4. **Confidence**: Data quality indicators help assess reliability
5. **Recovery**: Robust error handling with fallback strategies

### Next Steps

1. **Explore the interface** with different stocks and analysis types
2. **Practice using the analysis buttons** for structured data
3. **Export JSON data** for use in your own analysis tools
4. **Monitor confidence scores** to understand data quality
5. **Report any issues** to help improve the system

The Market Parser team continues to enhance the system based on user feedback and technological advances. The JSON architecture provides a solid foundation for future features and improvements.