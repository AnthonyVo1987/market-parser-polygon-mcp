# Dynamic Adaptive Prompting System Usage Guide

## Overview

The Dynamic Adaptive Prompting System allows users to customize AI interactions without requiring code changes. Users can specify their preferences for verbosity, tool usage, output format, and response style directly in their input messages.

## Features

- **Dynamic Prompt Generation**: Customize prompts based on user preferences
- **Instruction Parsing**: Extract preferences from natural language input
- **Template Engine**: Apply customizations to prompt templates
- **Input Validation**: Ensure security and correctness of user instructions
- **Performance Caching**: Optimize response times with intelligent caching
- **Fallback Mechanisms**: Graceful error handling and recovery

## User Instruction Syntax

### Verbosity Control

Control the level of detail in responses:

```
[verbose] - Comprehensive information with detailed explanations
[minimal] - Only essential information with minimal explanation
[standard] - Balanced information with moderate detail (default)
[detailed] - Thorough analysis with extensive detail
[brief] - Concise information with brief explanations
[concise] - Essential information in the most concise format possible
```

**Examples:**
- `[verbose] Get NVDA price analysis`
- `[minimal] Show SPY data`
- `[brief] What's the market status?`

### Tool Usage Control

Specify which tools to use or avoid:

```
[use only tool_name] - Use only the specified tool
[avoid tool_name] - Avoid using the specified tool
[minimal tools] - Use the minimum number of tools necessary
```

**Available Tools:**
- `get_snapshot_ticker`
- `get_market_status`
- `get_full_market_snapshot`
- `get_support_resistance_levels`
- `get_technical_analysis`

**Examples:**
- `[use only get_snapshot_ticker] Get NVDA price`
- `[avoid get_market_status] Show stock data`
- `[minimal tools] Quick analysis`

### Output Format Control

Control how responses are formatted:

```
[structured] - Clear sections and bullet points
[narrative] - Flowing narrative with paragraphs
[bullet points] - Bullet point format for easy reading
[JSON] - Valid JSON format when appropriate
[markdown] - Markdown formatting
[plain] - Plain text without special formatting
```

**Examples:**
- `[structured] Analyze NVDA performance`
- `[bullet points] Show market movers`
- `[JSON] Get stock data`

### Response Style Control

Control the tone and style of responses:

```
[formal] - Formal, professional tone
[casual] - Casual, friendly tone
[technical] - Technical, precise tone with terminology
[professional] - Professional, business-appropriate tone
[friendly] - Warm, approachable tone
```

**Examples:**
- `[formal] Provide market analysis`
- `[casual] What's up with the market?`
- `[technical] Deep dive into NVDA`

## Combining Instructions

You can combine multiple instructions in a single message:

```
[verbose] [structured] [professional] Get comprehensive NVDA analysis
[minimal] [bullet points] [casual] Quick market update
[detailed] [JSON] [technical] Deep technical analysis of SPY
```

## Examples

### Basic Usage

**Input:**
```
[verbose] [structured] [professional] Analyze NVDA stock performance
```

**Result:** The system will generate a comprehensive, structured, professional analysis of NVDA stock performance.

### Tool-Specific Analysis

**Input:**
```
[use only get_snapshot_ticker] [minimal] [bullet points] Get NVDA price
```

**Result:** The system will use only the snapshot ticker tool to provide minimal, bullet-point information about NVDA price.

### Style Customization

**Input:**
```
[casual] [narrative] [brief] What's happening with the market today?
```

**Result:** The system will provide a casual, narrative-style, brief overview of today's market activity.

## Integration with Existing System

The Dynamic Prompting System integrates seamlessly with the existing Market Parser system:

### CLI Usage

```bash
# Start the CLI
python -m src.backend.main

# Use dynamic instructions
> [verbose] [structured] [professional] Get NVDA analysis
> [minimal] [bullet points] [casual] Show market status
```

### GUI Usage

In the web interface, simply include your preferences in your message:

```
[detailed] [JSON] [technical] Provide comprehensive technical analysis of QQQ
```

### API Usage

```python
import requests

# Send request with dynamic instructions
response = requests.post('http://localhost:8000/chat', json={
    'message': '[verbose] [structured] [professional] Analyze SPY performance'
})
```

## Backward Compatibility

The system maintains full backward compatibility:

- **Without Instructions**: Works exactly as before with default settings
- **With Instructions**: Applies customizations while preserving core functionality
- **Error Handling**: Falls back to default behavior if instructions are invalid

## Performance Optimization

The system includes several performance optimizations:

- **Intelligent Caching**: Frequently used prompt configurations are cached
- **Lazy Loading**: Components are loaded only when needed
- **Error Recovery**: Graceful fallback to default prompts on errors

## Security Features

The system includes comprehensive security measures:

- **Input Validation**: All user instructions are validated
- **Sanitization**: Dangerous characters are removed
- **Rate Limiting**: Prevents abuse of the system
- **Error Handling**: Secure error messages without information leakage

## Monitoring and Debugging

### Cache Statistics

```python
from src.backend.dynamic_prompt_integration import get_dynamic_prompt_stats

stats = get_dynamic_prompt_stats()
print(f"Cache size: {stats['cache_size']}")
print(f"Hit rate: {stats['hit_rate']}")
```

### Clear Cache

```python
from src.backend.dynamic_prompt_integration import clear_dynamic_prompt_cache

clear_dynamic_prompt_cache()
```

## Best Practices

1. **Be Specific**: Use clear, specific instructions for best results
2. **Combine Wisely**: Don't use conflicting instructions (e.g., `[minimal] [verbose]`)
3. **Test First**: Try different combinations to find what works best for your use case
4. **Monitor Performance**: Check cache statistics to ensure optimal performance

## Troubleshooting

### Common Issues

1. **Instructions Not Applied**: Check syntax and ensure brackets are correct
2. **Performance Issues**: Clear cache or check cache statistics
3. **Unexpected Behavior**: Verify instruction combinations are compatible

### Error Messages

- **Validation Error**: Invalid instruction format or value
- **Template Error**: Issue with prompt template processing
- **General Error**: Unexpected system error (falls back to default)

## Future Enhancements

Planned features for future releases:

- **Custom Templates**: User-defined prompt templates
- **Learning System**: AI that learns from user preferences
- **Advanced Caching**: More sophisticated caching strategies
- **Analytics**: Detailed usage analytics and insights

## Support

For issues or questions about the Dynamic Prompting System:

1. Check this documentation
2. Review the test suite in `tests/test_dynamic_prompting_system.py`
3. Check system logs for error details
4. Contact the development team

---

*Last updated: September 26, 2025*