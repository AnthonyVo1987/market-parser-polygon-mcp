# Dynamic Adaptive Prompting System - Developer Guide

## Architecture Overview

The Dynamic Adaptive Prompting System is built with a modular architecture that separates concerns and provides extensibility. The system consists of several key components:

```
┌─────────────────────────────────────────────────────────────┐
│                    DynamicPromptManager                     │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │ InstructionParser│ │ TemplateEngine  │ │ InputValidator  │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │   PromptCache   │ │ SecurityConfig  │ │   Logger        │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. DynamicPromptManager

The main orchestrator that coordinates all components.

**Location:** `src/backend/dynamic_prompts.py`

**Key Methods:**

- `generate_prompt(user_input, context)` - Main entry point
- `parse_user_instructions(user_input)` - Extract preferences
- `_handle_validation_error()` - Error handling
- `_handle_template_error()` - Template error handling

**Configuration:**

```python
config = {
    'cache_size': 100,
    'security_rules': {
        'max_input_length': 1000,
        'rate_limit': 10
    }
}
```

### 2. InstructionParser

Extracts user preferences from input text using regex patterns.

**Location:** `src/backend/dynamic_prompts.py`

**Patterns:**

```python
patterns = {
    'verbosity': r'\[(verbose|minimal|standard|detailed|brief|concise)\]',
    'tool_usage': r'\[(use only|avoid|minimal tools?)(?:\s+([a-zA-Z_\s,]+))?\]',
    'output_format': r'\[(structured|narrative|bullet points?|JSON|markdown|plain)\]',
    'response_style': r'\[(formal|casual|technical|professional|friendly)\]'
}
```

**Key Methods:**

- `extract_preferences(user_input)` - Extract preferences from text
- `_validate_patterns()` - Validate regex patterns

### 3. TemplateEngine

Applies user preferences to prompt templates using variable substitution.

**Location:** `src/backend/dynamic_prompts.py`

**Template Variables:**

- `{verbosity_instruction}` - Verbosity customization
- `{tool_restriction}` - Tool usage restrictions
- `{format_instruction}` - Output format instructions
- `{style_instruction}` - Response style instructions

**Key Methods:**

- `apply_preferences(base_template, preferences, context)` - Apply customizations
- `_get_verbosity_template()` - Handle verbosity
- `_get_tool_usage_template()` - Handle tool usage
- `_get_output_format_template()` - Handle output format
- `_get_response_style_template()` - Handle response style

### 4. InputValidator

Validates and sanitizes user input for security and correctness.

**Location:** `src/backend/dynamic_prompts.py`

**Validation Rules:**

- Allowed verbosity levels
- Allowed tool names
- Allowed output formats
- Allowed response styles
- Input sanitization (removes dangerous characters)

**Key Methods:**

- `validate_preferences(preferences)` - Validate preferences
- `sanitize_preferences(preferences)` - Sanitize input
- `_validate_tool_usage(tool_usage)` - Validate tool usage

### 5. PromptCache

Provides intelligent caching for performance optimization.

**Location:** `src/backend/dynamic_prompts.py`

**Features:**

- LRU (Least Recently Used) eviction
- Configurable cache size
- Access time tracking
- Memory-efficient storage

**Key Methods:**

- `store(key, value)` - Store cached prompt
- `get(key)` - Retrieve cached prompt
- `_evict_oldest()` - Evict least recently used item

## Integration Points

### CLI Integration

**Location:** `src/backend/main.py`

The system integrates with the CLI through the `get_enhanced_agent_instructions()` function:

```python
def get_enhanced_agent_instructions(user_input: str = "", context: Dict[str, Any] = None) -> str:
    try:
        # Try dynamic prompt generation
        return get_enhanced_agent_instructions_dynamic(user_input, context or {})
    except Exception as e:
        # Fallback to static prompt
        return get_enhanced_agent_instructions_static()
```

### GUI Integration

**Location:** `src/backend/main.py`

The GUI integration occurs in the chat endpoint:

```python
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Use dynamic prompting for user messages
    if not request.is_button_prompt:
        system_prompt = get_enhanced_agent_instructions(request.message, context)
    else:
        # Use direct prompts for button interactions
        system_prompt = direct_prompt_manager.get_prompt(request.message, request.intent)
```

### Button Prompt Preservation

**Location:** `src/backend/direct_prompts.py`

Button prompts are preserved through the `DirectPromptManager`:

```python
class DirectPromptManager:
    def generate_direct_prompt(self, user_input: str, intent: AnalysisIntent) -> Dict[str, str]:
        # Generate specialized prompts for button interactions
        # This system remains unchanged and works alongside dynamic prompting
```

## Security Features

### SecureDynamicPromptManager

**Location:** `src/backend/secure_prompt_manager.py`

Enhanced security features:

```python
class SecureDynamicPromptManager:
    def __init__(self, base_template: str, security_config: SecurityConfig):
        self.rate_limiter = RateLimiter(security_config.rate_limit)
        self.audit_logger = AuditLogger()
        self.circuit_breaker = CircuitBreaker()
        self.input_validator = SecureInputValidator(security_config)
```

**Security Components:**

- Rate limiting
- Input validation
- Audit logging
- Circuit breaker pattern
- XSS protection
- SQL injection prevention

### SecurityConfig

**Location:** `src/backend/security_features.py`

```python
class SecurityConfig:
    def __init__(self):
        self.rate_limit = 10  # requests per minute
        self.max_input_length = 1000
        self.enable_audit_logging = True
        self.enable_circuit_breaker = True
        self.allowed_tools = [...]  # Whitelist of allowed tools
```

## Advanced Features

### Custom Templates

**Location:** `src/backend/advanced_prompting_features.py`

```python
class CustomTemplateManager:
    def create_template(self, name: str, template: str) -> None:
        # Create custom templates for specialized use cases
    
    def apply_custom_template(self, template_name: str, context: Dict) -> str:
        # Apply custom templates with context
```

### Learning System

```python
class LearningSystem:
    def learn_from_feedback(self, prompt: str, feedback: str) -> None:
        # Learn from user feedback to improve prompts
    
    def optimize_templates(self) -> None:
        # Optimize templates based on usage patterns
```

### Analytics

```python
class AnalyticsEngine:
    def track_usage(self, user_id: str, prompt: str, response_time: float) -> None:
        # Track usage patterns and performance
    
    def generate_insights(self) -> Dict[str, Any]:
        # Generate insights from usage data
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

**Location:** `config/dynamic_prompting.yaml`

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

## Testing

### Unit Tests

**Location:** `tests/test_dynamic_prompting_system.py`

```python
class TestDynamicPromptManager:
    def test_generate_prompt_with_preferences(self):
        # Test basic prompt generation
    
    def test_error_handling(self):
        # Test error handling scenarios
    
    def test_security_features(self):
        # Test security validations
```

### Integration Tests

**Location:** `tests/test_integration.py`

```python
def test_cli_integration():
    # Test CLI integration
    
def test_gui_integration():
    # Test GUI integration
    
def test_button_prompt_preservation():
    # Test button prompt preservation
```

### Performance Tests

**Location:** `tests/test_performance.py`

```python
def test_cache_performance():
    # Test cache performance
    
def test_concurrent_access():
    # Test concurrent access scenarios
    
def test_memory_usage():
    # Test memory usage patterns
```

## Deployment

### Docker Configuration

**Location:** `Dockerfile`

```dockerfile
FROM python:3.9-slim

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY src/ ./src/
COPY config/ ./config/

# Set environment variables
ENV DYNAMIC_PROMPTING_ENABLED=true

# Run application
CMD ["python", "src/backend/main.py"]
```

### Docker Compose

**Location:** `docker-compose.yml`

```yaml
version: '3.8'
services:
  market-parser:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DYNAMIC_PROMPTING_ENABLED=true
      - SECURITY_ENABLE_AUDIT_LOGGING=true
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
```

## Monitoring and Logging

### Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/dynamic_prompting.log'),
        logging.StreamHandler()
    ]
)
```

### Metrics Collection

```python
class MetricsCollector:
    def __init__(self):
        self.prompt_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.error_count = 0
    
    def record_prompt_generation(self, success: bool):
        self.prompt_count += 1
        if not success:
            self.error_count += 1
    
    def record_cache_access(self, hit: bool):
        if hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
```

## Troubleshooting

### Common Issues

1. **Template Variables Not Replaced**
   - Check template syntax: `{variable_name}`
   - Verify preference extraction
   - Check template engine configuration

2. **Cache Performance Issues**
   - Monitor cache hit/miss ratios
   - Adjust cache size configuration
   - Check memory usage

3. **Security Validation Failures**
   - Review input validation rules
   - Check allowed values configuration
   - Monitor audit logs

4. **Integration Issues**
   - Verify import paths
   - Check configuration files
   - Review error logs

### Debug Mode

Enable debug mode for detailed logging:

```python
import logging
logging.getLogger('dynamic_prompting').setLevel(logging.DEBUG)
```

### Performance Profiling

```python
import cProfile

def profile_prompt_generation():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Generate prompts
    for i in range(1000):
        manager.generate_prompt(f"Test input {i}", {})
    
    profiler.disable()
    profiler.dump_stats('prompt_generation.prof')
```

## Contributing

### Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest tests/`
4. Enable debug mode for development

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write comprehensive docstrings
- Include unit tests for new features

### Pull Request Process

1. Create feature branch
2. Implement changes with tests
3. Update documentation
4. Submit pull request with description

## API Reference

### DynamicPromptManager

```python
class DynamicPromptManager:
    def __init__(self, base_template: str, config: Dict[str, Any] = None):
        """Initialize the dynamic prompt manager."""
    
    def generate_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        """Generate a customized prompt based on user input."""
    
    def parse_user_instructions(self, user_input: str) -> UserPreferences:
        """Extract and validate user preferences from input text."""
```

### UserPreferences

```python
class UserPreferences:
    verbosity: Optional[str] = None
    tool_usage: Optional[str] = None
    output_format: Optional[str] = None
    response_style: Optional[str] = None
```

### SecurityConfig

```python
class SecurityConfig:
    def __init__(self):
        self.rate_limit: int = 10
        self.max_input_length: int = 1000
        self.enable_audit_logging: bool = True
        self.enable_circuit_breaker: bool = True
```

---

*This developer guide provides comprehensive information for developers working with the Dynamic Adaptive Prompting System. For user-facing documentation, see the User Guide.*
