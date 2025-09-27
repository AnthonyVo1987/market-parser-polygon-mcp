# Dynamic Adaptive Prompting System - API Reference

## Overview

This document provides detailed API reference for the Dynamic Adaptive Prompting System, including all classes, methods, and configuration options.

## Core Classes

### DynamicPromptManager

Main orchestrator for the dynamic prompting system.

**Location:** `src/backend/dynamic_prompts.py`

#### Constructor

```python
DynamicPromptManager(base_template: str, config: Dict[str, Any] = None)
```

**Parameters:**

- `base_template` (str): The base prompt template with placeholder variables
- `config` (Dict[str, Any], optional): Configuration options

**Configuration Options:**

```python
config = {
    'cache_size': 100,  # Maximum number of cached prompts
    'security_rules': {
        'max_input_length': 1000,  # Maximum input length
        'rate_limit': 10  # Requests per minute
    }
}
```

#### Methods

##### generate_prompt

```python
def generate_prompt(self, user_input: str, context: Dict[str, Any]) -> str
```

Generates a customized prompt based on user input and preferences.

**Parameters:**

- `user_input` (str): The user's input message
- `context` (Dict[str, Any]): Additional context for prompt generation

**Returns:**

- `str`: Customized prompt string

**Raises:**

- `ValidationError`: If input validation fails
- `TemplateError`: If template processing fails

**Example:**

```python
manager = DynamicPromptManager(base_template, config)
prompt = manager.generate_prompt("[verbose] [json] Get market data", {"user_id": "123"})
```

##### parse_user_instructions

```python
def parse_user_instructions(self, user_input: str) -> UserPreferences
```

Extracts and validates user preferences from input text.

**Parameters:**

- `user_input` (str): The user's input message

**Returns:**

- `UserPreferences`: Object containing extracted preferences

**Example:**

```python
preferences = manager.parse_user_instructions("[verbose] [json] Get data")
print(preferences.verbosity)  # "verbose"
print(preferences.output_format)  # "json"
```

### InstructionParser

Extracts user preferences from input text using regex patterns.

**Location:** `src/backend/dynamic_prompts.py`

#### Constructor

```python
InstructionParser()
```

#### Methods

##### extract_preferences

```python
def extract_preferences(self, user_input: str) -> Dict[str, Any]
```

Extract user preferences from input text using regex patterns.

**Parameters:**

- `user_input` (str): The user's input message

**Returns:**

- `Dict[str, Any]`: Dictionary of extracted preferences

**Supported Patterns:**

- `verbosity`: `[verbose|minimal|standard|detailed|brief|concise]`
- `tool_usage`: `[use only|avoid|minimal tools] [tool_names]`
- `output_format`: `[structured|narrative|bullet points|JSON|markdown|plain]`
- `response_style`: `[formal|casual|technical|professional|friendly]`

**Example:**

```python
parser = InstructionParser()
preferences = parser.extract_preferences("[verbose] [use only get_snapshot_ticker] Get data")
# Returns: {'verbosity': 'verbose', 'tool_usage': 'use only get_snapshot_ticker'}
```

### TemplateEngine

Applies user preferences to prompt templates using variable substitution.

**Location:** `src/backend/dynamic_prompts.py`

#### Constructor

```python
TemplateEngine()
```

#### Methods

##### apply_preferences

```python
def apply_preferences(self, base_template: str, preferences, context: Dict[str, Any]) -> str
```

Apply user preferences to the base template.

**Parameters:**

- `base_template` (str): The base prompt template
- `preferences`: User preferences (UserPreferences object or dict)
- `context` (Dict[str, Any]): Additional context for template processing

**Returns:**

- `str`: Customized prompt template

**Template Variables:**

- `{verbosity_instruction}`: Verbosity customization instructions
- `{tool_restriction}`: Tool usage restrictions
- `{format_instruction}`: Output format instructions
- `{style_instruction}`: Response style instructions

**Example:**

```python
engine = TemplateEngine()
template = "You are an AI assistant. {verbosity_instruction} {tool_restriction}"
preferences = UserPreferences(verbosity="verbose", tool_usage="use only get_snapshot_ticker")
result = engine.apply_preferences(template, preferences, {})
```

### InputValidator

Validates and sanitizes user input for security and correctness.

**Location:** `src/backend/dynamic_prompts.py`

#### Constructor

```python
InputValidator()
```

#### Methods

##### validate_preferences

```python
def validate_preferences(self, preferences) -> None
```

Validate user preferences against allowed values.

**Parameters:**

- `preferences`: User preferences (dict or UserPreferences object)

**Raises:**

- `ValidationError`: If preferences contain invalid values

**Allowed Values:**

- **Verbosity:** `['minimal', 'standard', 'verbose', 'detailed', 'brief', 'concise']`
- **Tool Usage:** Valid tool names or instruction types
- **Output Format:** `['structured', 'narrative', 'bullet points', 'json', 'markdown', 'plain']`
- **Response Style:** `['formal', 'casual', 'technical', 'professional', 'friendly']`

##### sanitize_preferences

```python
def sanitize_preferences(self, preferences: Dict[str, Any]) -> UserPreferences
```

Sanitize user preferences by removing dangerous characters.

**Parameters:**

- `preferences` (Dict[str, Any]): Raw preferences to sanitize

**Returns:**

- `UserPreferences`: Sanitized UserPreferences object

**Security Features:**

- Removes potentially dangerous characters: `<>"'`
- Trims whitespace
- Validates input length

### PromptCache

Provides intelligent caching for performance optimization.

**Location:** `src/backend/dynamic_prompts.py`

#### Constructor

```python
PromptCache(max_size: int = 100)
```

**Parameters:**

- `max_size` (int): Maximum number of cached items

#### Methods

##### store

```python
def store(self, key: str, value: str) -> None
```

Store a prompt in the cache.

**Parameters:**

- `key` (str): Cache key (typically user input)
- `value` (str): Cached prompt value

##### get

```python
def get(self, key: str) -> Optional[str]
```

Retrieve a prompt from the cache.

**Parameters:**

- `key` (str): Cache key

**Returns:**

- `Optional[str]`: Cached prompt or None if not found

##### clear

```python
def clear(self) -> None
```

Clear all cached items.

##### get_stats

```python
def get_stats(self) -> Dict[str, Any]
```

Get cache statistics.

**Returns:**

- `Dict[str, Any]`: Cache statistics including size, hit rate, etc.

## Data Models

### UserPreferences

Pydantic model for user preferences.

**Location:** `src/backend/dynamic_prompts.py`

```python
class UserPreferences:
    verbosity: Optional[str] = None
    tool_usage: Optional[str] = None
    output_format: Optional[str] = None
    response_style: Optional[str] = None
```

**Fields:**

- `verbosity` (Optional[str]): Verbosity level preference
- `tool_usage` (Optional[str]): Tool usage preference
- `output_format` (Optional[str]): Output format preference
- `response_style` (Optional[str]): Response style preference

### ValidationError

Custom exception for validation errors.

**Location:** `src/backend/dynamic_prompts.py`

```python
class ValidationError(Exception):
    """Raised when input validation fails."""
    pass
```

### TemplateError

Custom exception for template processing errors.

**Location:** `src/backend/dynamic_prompts.py`

```python
class TemplateError(Exception):
    """Raised when template processing fails."""
    pass
```

## Security Classes

### SecureDynamicPromptManager

Enhanced security features for the dynamic prompting system.

**Location:** `src/backend/secure_prompt_manager.py`

#### Constructor

```python
SecureDynamicPromptManager(base_template: str, security_config: SecurityConfig)
```

**Parameters:**

- `base_template` (str): The base prompt template
- `security_config` (SecurityConfig): Security configuration

#### Methods

##### generate_prompt_secure

```python
def generate_prompt_secure(self, user_input: str, context: Dict[str, Any], 
                          user_id: str = None, ip_address: str = None) -> str
```

Generate a prompt with full security features.

**Parameters:**

- `user_input` (str): The user's input message
- `context` (Dict[str, Any]): Additional context
- `user_id` (str, optional): User identifier for tracking
- `ip_address` (str, optional): IP address for rate limiting

**Returns:**

- `str`: Secure, customized prompt

**Security Features:**

- Rate limiting
- Input validation
- Audit logging
- Circuit breaker protection

### SecurityConfig

Configuration for security features.

**Location:** `src/backend/security_features.py`

```python
class SecurityConfig:
    def __init__(self):
        self.rate_limit: int = 10  # Requests per minute
        self.max_input_length: int = 1000  # Maximum input length
        self.enable_audit_logging: bool = True  # Enable audit logging
        self.enable_circuit_breaker: bool = True  # Enable circuit breaker
        self.allowed_tools: List[str] = [...]  # Whitelist of allowed tools
```

**Configuration Options:**

- `rate_limit` (int): Maximum requests per minute per user
- `max_input_length` (int): Maximum input length in characters
- `enable_audit_logging` (bool): Enable audit logging
- `enable_circuit_breaker` (bool): Enable circuit breaker pattern
- `allowed_tools` (List[str]): Whitelist of allowed tool names

## Integration Functions

### get_enhanced_agent_instructions_dynamic

Dynamic prompt generation function for integration.

**Location:** `src/backend/dynamic_prompt_integration.py`

```python
def get_enhanced_agent_instructions_dynamic(user_input: str = "", 
                                          context: Dict[str, Any] = None) -> str
```

Generate enhanced agent instructions using dynamic prompting.

**Parameters:**

- `user_input` (str): User input message
- `context` (Dict[str, Any]): Additional context

**Returns:**

- `str`: Enhanced agent instructions

### get_enhanced_agent_instructions_secure

Secure dynamic prompt generation function.

**Location:** `src/backend/dynamic_prompt_integration.py`

```python
def get_enhanced_agent_instructions_secure(user_input: str = "", 
                                         context: Dict[str, Any] = None,
                                         user_id: str = None, 
                                         ip_address: str = None) -> str
```

Generate secure enhanced agent instructions.

**Parameters:**

- `user_input` (str): User input message
- `context` (Dict[str, Any]): Additional context
- `user_id` (str, optional): User identifier
- `ip_address` (str, optional): IP address

**Returns:**

- `str`: Secure enhanced agent instructions

## Factory Functions

### create_dynamic_prompt_manager

Factory function to create a DynamicPromptManager instance.

**Location:** `src/backend/dynamic_prompts.py`

```python
def create_dynamic_prompt_manager(base_template: str, 
                                config: Dict[str, Any] = None) -> DynamicPromptManager
```

**Parameters:**

- `base_template` (str): The base prompt template
- `config` (Dict[str, Any], optional): Configuration options

**Returns:**

- `DynamicPromptManager`: Configured DynamicPromptManager instance

**Example:**

```python
manager = create_dynamic_prompt_manager(
    base_template="You are an AI assistant. {verbosity_instruction}",
    config={'cache_size': 50}
)
```

## Configuration

### Environment Variables

```bash
# Dynamic Prompting Configuration
DYNAMIC_PROMPTING_ENABLED=true
DYNAMIC_PROMPTING_CACHE_SIZE=100
DYNAMIC_PROMPTING_RATE_LIMIT=10

# Security Configuration
SECURITY_MAX_INPUT_LENGTH=1000
SECURITY_ENABLE_AUDIT_LOGGING=true
SECURITY_ENABLE_CIRCUIT_BREAKER=true

# Performance Configuration
PERFORMANCE_CACHE_TTL=3600
PERFORMANCE_BACKGROUND_PROCESSING=true
```

### Configuration Files

**YAML Configuration:**

```yaml
dynamic_prompting:
  enabled: true
  cache_size: 100
  rate_limit: 10
  
security:
  max_input_length: 1000
  enable_audit_logging: true
  enable_circuit_breaker: true
  
performance:
  cache_ttl: 3600
  background_processing: true
```

## Error Handling

### Exception Hierarchy

```
Exception
├── ValidationError
├── TemplateError
└── SecurityError
    ├── RateLimitExceededError
    ├── InputTooLongError
    └── InvalidToolError
```

### Error Response Format

```python
{
    "error": "ValidationError",
    "message": "Invalid verbosity level: invalid_level",
    "code": "VALIDATION_ERROR",
    "details": {
        "field": "verbosity",
        "value": "invalid_level",
        "allowed_values": ["minimal", "standard", "verbose", "detailed", "brief", "concise"]
    }
}
```

## Performance Metrics

### Cache Statistics

```python
{
    "cache_size": 100,
    "cache_hits": 850,
    "cache_misses": 150,
    "hit_rate": 0.85,
    "memory_usage": "2.5MB"
}
```

### Performance Metrics

```python
{
    "average_response_time": 0.05,  # seconds
    "p95_response_time": 0.12,      # seconds
    "p99_response_time": 0.25,      # seconds
    "requests_per_second": 20,
    "error_rate": 0.01
}
```

## Testing

### Unit Test Examples

```python
def test_dynamic_prompt_manager():
    manager = DynamicPromptManager(base_template, config)
    result = manager.generate_prompt("[verbose] Get data", {})
    assert "comprehensive information" in result

def test_input_validation():
    validator = InputValidator()
    with pytest.raises(ValidationError):
        validator.validate_preferences({"verbosity": "invalid"})

def test_cache_performance():
    cache = PromptCache(max_size=10)
    cache.store("key1", "value1")
    assert cache.get("key1") == "value1"
```

### Integration Test Examples

```python
def test_cli_integration():
    result = get_enhanced_agent_instructions_dynamic("[verbose] Get data")
    assert isinstance(result, str)
    assert len(result) > 0

def test_gui_integration():
    # Test GUI integration with dynamic prompting
    pass
```

## Migration Guide

### From Static to Dynamic Prompting

1. **Update imports:**

```python
# Old
from main import get_enhanced_agent_instructions

# New
from dynamic_prompt_integration import get_enhanced_agent_instructions_dynamic
```

2. **Update function calls:**

```python
# Old
prompt = get_enhanced_agent_instructions()

# New
prompt = get_enhanced_agent_instructions_dynamic(user_input, context)
```

3. **Add error handling:**

```python
try:
    prompt = get_enhanced_agent_instructions_dynamic(user_input, context)
except Exception as e:
    # Fallback to static prompt
    prompt = get_enhanced_agent_instructions_static()
```

### Configuration Migration

1. **Add environment variables:**

```bash
DYNAMIC_PROMPTING_ENABLED=true
DYNAMIC_PROMPTING_CACHE_SIZE=100
```

2. **Update configuration files:**

```yaml
dynamic_prompting:
  enabled: true
  cache_size: 100
```

3. **Update application code:**

```python
# Check if dynamic prompting is enabled
if os.getenv('DYNAMIC_PROMPTING_ENABLED', 'false').lower() == 'true':
    prompt = get_enhanced_agent_instructions_dynamic(user_input, context)
else:
    prompt = get_enhanced_agent_instructions_static()
```

---

*This API reference provides comprehensive documentation for all classes, methods, and configuration options in the Dynamic Adaptive Prompting System. For usage examples and best practices, see the User Guide and Developer Guide.*
