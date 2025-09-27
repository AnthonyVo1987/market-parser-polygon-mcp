# Dynamic Adaptive Prompting System Architecture

## System Overview

The Dynamic Adaptive Prompting System is a revolutionary upgrade that transforms the Market Parser from a static, rigid system into a flexible, user-customizable AI assistant. It allows users to control AI behavior through simple bracket notation without requiring code changes.

## Core Components

### 1. DynamicPromptManager

- **Purpose**: Main orchestrator that coordinates all system components
- **Location**: `src/backend/dynamic_prompts.py`
- **Key Methods**: `generate_prompt()`, `parse_user_instructions()`
- **Features**: Error handling, fallback mechanisms, performance optimization

### 2. InstructionParser

- **Purpose**: Extracts user preferences from natural language input using regex patterns
- **Patterns**:
  - Verbosity: `\[(verbose|minimal|standard|detailed|brief|concise)\]`
  - Tool Usage: `\[(use only|avoid|minimal tools?)(?:\s+([a-zA-Z_\s,]+))?\]`
  - Output Format: `\[(structured|narrative|bullet points?|JSON|markdown|plain)\]`
  - Response Style: `\[(formal|casual|technical|professional|friendly)\]`

### 3. TemplateEngine

- **Purpose**: Applies user preferences to prompt templates using variable substitution
- **Key Methods**: `apply_preferences()`, `_get_verbosity_template()`, `_get_tool_usage_template()`
- **Template Variables**: `{verbosity_instruction}`, `{tool_restriction}`, `{format_instruction}`, `{style_instruction}`

### 4. InputValidator

- **Purpose**: Validates and sanitizes user input for security and correctness
- **Security Features**: Input validation, sanitization, allowed value checking
- **Allowed Values**: Predefined lists for verbs, tools, formats, and styles

### 5. PromptCache

- **Purpose**: LRU cache for performance optimization
- **Default Size**: 100 entries
- **Features**: Automatic cache management, performance monitoring

## User Customization Options

### Verbosity Control (6 levels)

- `[minimal]` - Essential information only
- `[standard]` - Balanced information (default)
- `[verbose]` - Comprehensive information
- `[detailed]` - Thorough analysis
- `[brief]` - Concise information
- `[concise]` - Most concise format

### Tool Usage Control (3 types)

- `[use only tool_name]` - Use only specified tools
- `[avoid tool_name]` - Avoid specified tools
- `[minimal tools]` - Use minimum necessary tools

**Available Tools**:

- `get_snapshot_ticker` - Individual stock data
- `get_market_status` - Overall market status
- `get_full_market_snapshot` - Comprehensive market data
- `get_support_resistance_levels` - Technical support/resistance
- `get_technical_analysis` - Technical analysis

### Output Format (6 types)

- `[structured]` - Clear sections and bullet points (default)
- `[narrative]` - Flowing narrative with paragraphs
- `[bullet points]` - Bullet points for easy reading
- `[json]` - Valid JSON format
- `[markdown]` - Markdown formatting
- `[plain]` - Plain text without formatting

### Response Style (5 types)

- `[formal]` - Formal, professional tone
- `[casual]` - Casual, friendly tone
- `[technical]` - Technical, precise tone
- `[professional]` - Professional, business-appropriate tone (default)
- `[friendly]` - Warm, approachable tone

## Default Behavior

When no customization is provided, the system uses:

- **Verbosity**: Balanced information with moderate detail
- **Tool Usage**: No restrictions (uses all available tools)
- **Output Format**: Structured format with clear sections and bullet points
- **Response Style**: Professional, business-appropriate tone

## Integration Architecture

### MarketParserDynamicPromptManager

- **Location**: `src/backend/dynamic_prompt_manager.py`
- **Purpose**: Integration layer between DynamicPromptManager and existing Market Parser system
- **Key Method**: `get_enhanced_agent_instructions()`
- **Features**: Backward compatibility, seamless integration with CLI/GUI

### Dynamic Prompt Integration

- **Location**: `src/backend/dynamic_prompt_integration.py`
- **Purpose**: Replaces static `get_enhanced_agent_instructions` function
- **Features**: User input processing, performance monitoring, caching

## Security Features

### SecurityConfig

- **Location**: `src/backend/security_features.py`
- **Features**: Rate limiting, input validation, audit logging, circuit breaker patterns
- **Security Levels**: LOW, MEDIUM, HIGH, CRITICAL
- **Threat Types**: INJECTION_ATTEMPT, RATE_LIMIT_EXCEEDED, SUSPICIOUS_ACTIVITY

### SecureDynamicPromptManager

- **Location**: `src/backend/secure_prompt_manager.py`
- **Purpose**: Security-enhanced prompt manager with user tracking
- **Features**: User authentication, IP tracking, security event logging

## Performance Optimization

### Caching Strategy

- **LRU Cache**: 100 entries default
- **Cache Keys**: User input + preferences
- **Cache Stats**: Hit rate, miss rate, eviction count
- **Performance Monitoring**: Response time tracking

### Error Handling

- **ValidationError**: Invalid user preferences
- **TemplateError**: Template processing errors
- **Fallback Mechanisms**: Graceful degradation to default behavior
- **Logging**: Comprehensive error logging and monitoring

## Usage Examples

### Basic Usage

```text
[verbose] [json] [formal] Get comprehensive market analysis
```

### Advanced Usage

```text
[detailed] [markdown] [technical] [use only get_technical_analysis] Analyze NVDA technical indicators
```

### Efficiency Usage

```text
[concise] [bullet points] [minimal tools] [casual] Quick market update
```

## File Structure

```text
src/backend/
├── dynamic_prompts.py              # Core system components
├── dynamic_prompt_manager.py       # Integration layer
├── dynamic_prompt_integration.py   # Function replacement
├── secure_prompt_manager.py        # Security-enhanced manager
├── security_features.py            # Security configuration
└── advanced_prompting_features.py  # Advanced features

docs/
├── dynamic_prompting_usage_guide.md        # User guide
├── dynamic_prompting_system_user_guide.md  # System user guide
├── dynamic_prompting_system_developer_guide.md  # Developer guide
├── dynamic_prompting_system_api_reference.md    # API reference
├── dynamic_prompting_system_troubleshooting.md  # Troubleshooting
└── dynamic_prompting_system_migration_guide.md  # Migration guide
```

## Key Benefits

1. **Flexibility**: Customize AI behavior without code changes
2. **Backward Compatibility**: Works with existing prompts and workflows
3. **Performance**: Intelligent caching and optimization
4. **Security**: Comprehensive validation and sanitization
5. **User Experience**: Simple bracket notation for easy customization
6. **Professional Standards**: High code quality and documentation

## Implementation Status

- **Phases 0-5**: Core implementation completed
- **Phases 6-7**: Testing, documentation, and deployment completed
- **Code Quality**: 9.80/10 PyLint score, 0 ESLint errors
- **Documentation**: Comprehensive user and developer guides
- **Testing**: Unit, integration, and user acceptance tests
- **Deployment**: Production-ready with monitoring and rollback procedures
