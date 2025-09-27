# Dynamic Adaptive Prompting System - User Guide

## Overview

The Dynamic Adaptive Prompting System allows you to customize AI interactions by adding preference instructions to your requests. You can control verbosity, tool usage, output format, and response style using simple bracket notation.

## Quick Start

Add preference instructions in square brackets `[]` at the beginning of your message:

```
[verbose] [json] [formal] Get comprehensive market analysis
```

## Preference Types

### 1. Verbosity Control

Control how detailed the AI response should be:

- `[minimal]` - Essential information only, minimal explanation
- `[standard]` - Balanced information with moderate detail (default)
- `[verbose]` - Comprehensive information with detailed explanations
- `[detailed]` - Thorough analysis with extensive detail
- `[brief]` - Concise information with brief explanations
- `[concise]` - Essential information in the most concise format

**Examples:**

```
[minimal] Get NVDA stock price
[verbose] Explain market trends in detail
[concise] Quick market update
```

### 2. Tool Usage Control

Specify which tools the AI should use or avoid:

- `[use only tool_name]` - Use only the specified tool(s)
- `[avoid tool_name]` - Avoid using the specified tool(s)
- `[minimal tools]` - Use the minimum number of tools necessary

**Available Tools:**

- `get_snapshot_ticker` - Get individual stock data
- `get_market_status` - Get overall market status
- `get_full_market_snapshot` - Get comprehensive market data
- `get_support_resistance_levels` - Get technical support/resistance levels
- `get_technical_analysis` - Get technical analysis

**Examples:**

```
[use only get_snapshot_ticker] Get AAPL data
[avoid get_technical_analysis] Simple market check
[minimal tools] Quick portfolio update
```

### 3. Output Format

Control how the response should be formatted:

- `[structured]` - Clear sections and bullet points (default)
- `[narrative]` - Flowing narrative with paragraphs
- `[bullet points]` - Bullet points for easy reading
- `[json]` - Valid JSON format when appropriate
- `[markdown]` - Markdown formatting
- `[plain]` - Plain text without special formatting

**Examples:**

```
[json] Get market data in JSON format
[markdown] Create a formatted report
[bullet points] Summarize key findings
```

### 4. Response Style

Control the tone and style of the response:

- `[formal]` - Formal, professional tone
- `[casual]` - Casual, friendly tone
- `[technical]` - Technical, precise tone with terminology
- `[professional]` - Professional, business-appropriate tone (default)
- `[friendly]` - Warm, approachable tone

**Examples:**

```
[formal] Provide professional market analysis
[casual] Explain this in simple terms
[technical] Deep dive technical analysis
```

## Combining Preferences

You can combine multiple preferences in a single request:

```
[verbose] [json] [formal] Comprehensive market analysis
[minimal] [bullet points] [casual] Quick summary
[standard] [markdown] [technical] Technical report
```

## Examples

### Basic Usage

```
[verbose] Get detailed analysis of SPY performance
```

### Advanced Usage

```
[verbose] [use only get_snapshot_ticker, get_market_status] [json] [formal] 
Comprehensive market analysis for portfolio optimization
```

### Quick Updates

```
[minimal] [bullet points] [casual] Quick market update
```

### Technical Analysis

```
[detailed] [avoid get_technical_analysis] [markdown] [technical] 
Fundamental analysis of tech stocks
```

## Best Practices

1. **Start Simple**: Begin with basic preferences and add complexity as needed
2. **Be Specific**: Use specific tool names when controlling tool usage
3. **Combine Wisely**: Some combinations work better than others (e.g., `[verbose] [json]` for detailed structured data)
4. **Test Different Styles**: Experiment with different verbosity and style combinations
5. **Use Appropriate Formats**: Choose output formats that match your needs (JSON for data, Markdown for reports)

## Common Use Cases

### Market Research

```
[verbose] [markdown] [formal] Comprehensive market research report
```

### Quick Checks

```
[minimal] [bullet points] [casual] Quick market status
```

### Data Analysis

```
[standard] [json] [technical] Market data analysis
```

### Portfolio Updates

```
[detailed] [structured] [professional] Portfolio performance review
```

## Troubleshooting

### Preferences Not Applied

- Ensure brackets are properly formatted: `[preference]`
- Check that preference values are valid (see lists above)
- Verify spelling and case sensitivity

### Invalid Tool Names

- Use exact tool names as listed in the Tool Usage section
- Separate multiple tools with commas: `[use only tool1, tool2]`

### Conflicting Preferences

- The system will use the last specified preference of each type
- Example: `[minimal] [verbose]` will result in verbose output

## Advanced Features

### Custom Templates

The system supports custom prompt templates for specialized use cases. Contact your system administrator for custom template configuration.

### Security Features

- Input validation prevents malicious content
- Rate limiting protects against abuse
- Audit logging tracks usage patterns

### Performance Optimization

- Intelligent caching reduces response times
- Template optimization improves efficiency
- Background processing handles complex requests

## Support

For additional help or feature requests, please contact your system administrator or refer to the developer documentation.

---

*This guide covers the basic usage of the Dynamic Adaptive Prompting System. For advanced configuration and customization options, see the Developer Documentation.*
