# Dynamic Adaptive Prompting System - Usage Guide

## 🚀 Overview

The Dynamic Adaptive Prompting System transforms the Market Parser from a static, rigid system into a flexible, user-customizable AI assistant. You can now control how the AI responds to your financial queries by adding simple preference instructions to your requests.

## 🎯 Quick Start

Add preference instructions in square brackets `[]` at the beginning of your message:

```text
[verbose] [json] [formal] Get comprehensive market analysis
```

## 📋 Default Behavior

When you use the system **without** any customization instructions, it provides:

- **Verbosity**: Balanced information with moderate detail
- **Tool Usage**: No restrictions (uses all available tools)
- **Output Format**: Structured format with clear sections and bullet points
- **Response Style**: Professional, business-appropriate tone

## 🎛️ Customization Options

### 1. Verbosity Control `[verbosity_level]`

Control how detailed the AI response should be:

| Option | Description | Example Output |
|--------|-------------|----------------|
| `[minimal]` | Essential information only, minimal explanation | "NVDA: $450.25 (+2.3%)" |
| `[standard]` | Balanced information with moderate detail *(default)* | "NVDA: $450.25 (+2.3%). NVIDIA Corporation is trading higher today..." |
| `[verbose]` | Comprehensive information with detailed explanations | "NVDA: $450.25 (+2.3%). NVIDIA Corporation (NVDA) is currently trading at $450.25, representing a 2.3% increase from the previous close. This performance reflects strong demand for AI and data center products..." |
| `[detailed]` | Thorough analysis with extensive detail | Full market analysis with historical context, technical indicators, and comprehensive insights |
| `[brief]` | Concise information with brief explanations | "NVDA: $450.25 (+2.3%) - Strong AI demand driving gains" |
| `[concise]` | Essential information in the most concise format | "NVDA: $450.25 (+2.3%)" |

**Examples:**

```text
[minimal] Get NVDA stock price
[verbose] Explain market trends in detail
[concise] Quick market update
```

### 2. Tool Usage Control `[tool_instruction]`

Specify which tools the AI should use or avoid:

| Instruction | Description | Use Case |
|-------------|-------------|----------|
| `[use only tool_name]` | Use only the specified tool(s) | When you want specific data only |
| `[avoid tool_name]` | Avoid using the specified tool(s) | When you want to exclude certain analysis |
| `[minimal tools]` | Use the minimum number of tools necessary | For quick, efficient responses |

**Available Tools:**

- `get_snapshot_ticker` - Individual stock data
- `get_market_status` - Overall market status
- `get_full_market_snapshot` - Comprehensive market data
- `get_support_resistance_levels` - Technical support/resistance levels
- `get_technical_analysis` - Technical analysis

**Examples:**

```text
[use only get_snapshot_ticker] Get AAPL data
[avoid get_technical_analysis] Simple market check
[minimal tools] Quick portfolio update
```

### 3. Output Format `[format_type]`

Control how the response should be structured:

| Format | Description | Best For |
|--------|-------------|----------|
| `[structured]` | Clear sections and bullet points *(default)* | General analysis |
| `[narrative]` | Flowing narrative with paragraphs | Storytelling, explanations |
| `[bullet points]` | Bullet points for easy reading | Quick summaries |
| `[json]` | Valid JSON format when appropriate | Data integration, APIs |
| `[markdown]` | Markdown formatting | Reports, documentation |
| `[plain]` | Plain text without special formatting | Simple text output |

**Examples:**

```text
[json] Get market data in JSON format
[markdown] Create a formatted report
[bullet points] Summarize key findings
```

### 4. Response Style `[style_type]`

Control the tone and personality of the response:

| Style | Description | Tone Example |
|-------|-------------|--------------|
| `[formal]` | Formal, professional tone | "Based on the current market analysis..." |
| `[casual]` | Casual, friendly tone | "Hey! So the market's been pretty interesting lately..." |
| `[technical]` | Technical, precise tone with terminology | "The RSI indicator shows oversold conditions at 28.5..." |
| `[professional]` | Professional, business-appropriate tone *(default)* | "The current market conditions indicate..." |
| `[friendly]` | Warm, approachable tone | "Great question! Let me break this down for you..." |

**Examples:**

```text
[formal] Provide professional market analysis
[casual] Explain this in simple terms
[technical] Deep dive technical analysis
```

## 🔗 Combining Multiple Preferences

You can combine multiple preferences in a single request:

```text
[verbose] [json] [technical] [use only get_snapshot_ticker] Get comprehensive NVDA analysis
```

This would:

- Provide verbose, detailed information
- Format the response as JSON
- Use technical terminology
- Only use the snapshot ticker tool

## 📚 Real-World Examples

### Example 1: Quick Market Check

```text
[minimal] [bullet points] [casual] What's happening with the market today?
```

**Result**: Brief, casual bullet points about current market conditions.

### Example 2: Professional Report

```text
[detailed] [markdown] [formal] [use only get_full_market_snapshot] Generate a comprehensive market report
```

**Result**: Detailed, formal markdown report using only full market snapshot data.

### Example 3: Technical Analysis

```text
[verbose] [technical] [use only get_technical_analysis] Analyze NVDA technical indicators
```

**Result**: Verbose technical analysis with precise terminology and technical indicators only.

### Example 4: Data Integration

```text
[standard] [json] [professional] Get SPY, QQQ, IWM market data
```

**Result**: Standard detail level, JSON format, professional tone for easy data integration.

### Example 5: Simple Price Check

```text
[concise] [plain] [minimal tools] Get AAPL price
```

**Result**: Concise, plain text response using minimal tools for just the price.

## 🛡️ Security & Validation

The system includes comprehensive security features:

- **Input Validation**: All user preferences are validated against allowed values
- **Sanitization**: Potentially harmful content is removed
- **Rate Limiting**: Prevents abuse and excessive requests
- **Audit Logging**: Tracks all user interactions for security monitoring

## ⚡ Performance Features

- **Intelligent Caching**: Frequently used prompt combinations are cached for faster responses
- **LRU Cache**: Automatically manages cache size (default: 100 entries)
- **Fallback Mechanisms**: Graceful error handling with fallback to default prompts

## 🔄 How It Works

1. **Input Processing**: Your message with preferences is parsed using regex patterns
2. **Preference Extraction**: Bracket notation preferences are extracted and validated
3. **Template Customization**: The base template is customized with your preferences
4. **Prompt Generation**: A customized prompt instructs the AI according to your preferences
5. **Caching**: The customized prompt is cached for future similar requests

## 🎯 Best Practices

### Do's ✅

- Use clear, specific preference instructions
- Combine preferences logically (e.g., `[verbose] [technical]` for detailed technical analysis)
- Use `[minimal tools]` for quick responses
- Use `[json]` format when integrating with other systems

### Don'ts ❌

- Don't use conflicting preferences (e.g., `[minimal] [verbose]`)
- Don't use invalid preference values
- Don't overcomplicate with too many preferences at once
- Don't use preferences that don't make sense for the request

## 🚨 Error Handling

If you use invalid preferences, the system will:

1. Log the validation error
2. Fall back to default behavior
3. Continue processing your request normally

**Example of invalid usage:**

```text
[invalid_verbosity] [wrong_format] Get market data
```

→ System falls back to default settings and processes the request normally.

## 📊 Preference Combinations Guide

| Use Case | Recommended Combination | Example |
|----------|------------------------|---------|
| Quick Price Check | `[minimal] [plain] [minimal tools]` | `[minimal] [plain] [minimal tools] Get AAPL price` |
| Professional Report | `[detailed] [markdown] [formal]` | `[detailed] [markdown] [formal] Generate market report` |
| Technical Analysis | `[verbose] [technical] [use only get_technical_analysis]` | `[verbose] [technical] [use only get_technical_analysis] Analyze NVDA` |
| Data Integration | `[standard] [json] [professional]` | `[standard] [json] [professional] Get market data` |
| Casual Discussion | `[standard] [narrative] [casual]` | `[standard] [narrative] [casual] Explain market trends` |
| Quick Summary | `[brief] [bullet points] [friendly]` | `[brief] [bullet points] [friendly] Summarize today's market` |

## 🔧 Advanced Usage

### Custom Tool Combinations

```text
[use only get_snapshot_ticker, get_market_status] Get comprehensive market overview
```

### Style and Format Combinations

```text
[technical] [markdown] [verbose] Create detailed technical analysis report
```

### Efficiency Combinations

```text
[concise] [bullet points] [minimal tools] [casual] Quick market update
```

## 📈 Integration Examples

### CLI Usage

```bash
# Quick price check
./market-parser "[minimal] [plain] Get NVDA price"

# Detailed analysis
./market-parser "[verbose] [markdown] [formal] Analyze market trends"
```

### GUI Usage

In the web interface, simply type your request with preferences:

```text
[detailed] [json] [professional] Get comprehensive market analysis
```

## 🎉 Conclusion

The Dynamic Adaptive Prompting System gives you unprecedented control over your AI interactions. Whether you need a quick price check or a comprehensive market analysis, you can customize the AI's behavior to match your exact needs using simple bracket notation.

Start experimenting with different combinations to find what works best for your specific use cases!

---

*For technical details and implementation information, see the [Developer Guide](dynamic_prompting_system_developer_guide.md) and [API Reference](dynamic_prompting_system_api_reference.md).*
