# Dynamic Adaptive Prompting System - Troubleshooting Guide

## Common Issues and Solutions

### 1. Preferences Not Applied

**Symptoms:**

- User preferences in brackets are ignored
- Template variables like `{verbosity_instruction}` remain unreplaced
- No customization is applied to prompts

**Possible Causes:**

- Malformed bracket syntax
- Invalid preference values
- Template engine configuration issues

**Solutions:**

1. **Check Bracket Syntax:**

```python
# Correct
[verbose] [json] [formal] Get market data

# Incorrect
[verbose [json] [formal] Get market data  # Missing closing bracket
[verbose] [json [formal] Get market data  # Missing closing bracket
```

2. **Verify Preference Values:**

```python
# Valid verbosity levels
[minimal] [standard] [verbose] [detailed] [brief] [concise]

# Valid output formats
[structured] [narrative] [bullet points] [json] [markdown] [plain]

# Valid response styles
[formal] [casual] [technical] [professional] [friendly]
```

3. **Check Template Configuration:**

```python
# Ensure template has correct placeholders
base_template = """
You are an AI assistant.
{verbosity_instruction}
{tool_restriction}
{format_instruction}
{style_instruction}
"""
```

### 2. Tool Usage Not Working

**Symptoms:**

- `[use only tool_name]` or `[avoid tool_name]` not applied
- `{tool_restriction}` placeholder not replaced
- Tool restrictions ignored

**Possible Causes:**

- Invalid tool names
- Incorrect tool usage syntax
- Template engine not processing tool usage

**Solutions:**

1. **Use Valid Tool Names:**

```python
# Valid tools
[use only get_snapshot_ticker]
[use only get_market_status]
[use only get_full_market_snapshot]
[use only get_support_resistance_levels]
[use only get_technical_analysis]

# Multiple tools
[use only get_snapshot_ticker, get_market_status]
```

2. **Check Syntax:**

```python
# Correct
[use only get_snapshot_ticker] Get data
[avoid get_technical_analysis] Simple check
[minimal tools] Quick update

# Incorrect
[use get_snapshot_ticker] Get data  # Missing "only"
[avoid get_technical_analysis Get data  # Missing closing bracket
```

3. **Debug Tool Usage:**

```python
# Test tool usage parsing
parser = InstructionParser()
preferences = parser.extract_preferences("[use only get_snapshot_ticker] Get data")
print(preferences.get('tool_usage'))  # Should print: "use only get_snapshot_ticker"
```

### 3. Cache Performance Issues

**Symptoms:**

- Slow response times
- High memory usage
- Cache not working effectively

**Possible Causes:**

- Cache size too small
- Memory leaks
- Inefficient cache keys

**Solutions:**

1. **Adjust Cache Size:**

```python
config = {
    'cache_size': 200,  # Increase cache size
    'security_rules': {
        'max_input_length': 1000,
        'rate_limit': 10
    }
}
```

2. **Monitor Cache Performance:**

```python
cache = PromptCache(max_size=100)
# ... use cache ...
stats = cache.get_stats()
print(f"Hit rate: {stats['hit_rate']}")
print(f"Cache size: {stats['cache_size']}")
```

3. **Clear Cache if Needed:**

```python
cache.clear()  # Clear all cached items
```

### 4. Validation Errors

**Symptoms:**

- `ValidationError` exceptions
- Input rejected
- Preferences not accepted

**Possible Causes:**

- Invalid preference values
- Input too long
- Malicious content detected

**Solutions:**

1. **Check Allowed Values:**

```python
# Valid verbosity levels
['minimal', 'standard', 'verbose', 'detailed', 'brief', 'concise']

# Valid output formats
['structured', 'narrative', 'bullet points', 'json', 'markdown', 'plain']

# Valid response styles
['formal', 'casual', 'technical', 'professional', 'friendly']
```

2. **Check Input Length:**

```python
# Default max length is 1000 characters
# If input is too long, truncate or split
if len(user_input) > 1000:
    user_input = user_input[:1000]
```

3. **Handle Validation Errors:**

```python
try:
    prompt = manager.generate_prompt(user_input, context)
except ValidationError as e:
    print(f"Validation error: {e}")
    # Use fallback prompt or ask user to correct input
```

### 5. Security Issues

**Symptoms:**

- Rate limiting errors
- Input sanitization failures
- Security validation errors

**Possible Causes:**

- Too many requests
- Malicious input
- Security configuration issues

**Solutions:**

1. **Handle Rate Limiting:**

```python
try:
    prompt = secure_manager.generate_prompt_secure(user_input, context, user_id, ip_address)
except RateLimitExceededError as e:
    print(f"Rate limit exceeded: {e}")
    # Wait and retry or inform user
```

2. **Check Security Configuration:**

```python
security_config = SecurityConfig()
security_config.rate_limit = 20  # Increase rate limit
security_config.max_input_length = 2000  # Increase max length
```

3. **Monitor Security Logs:**

```python
# Check audit logs for security events
# Look for patterns of abuse or suspicious activity
```

### 6. Integration Issues

**Symptoms:**

- CLI/GUI not using dynamic prompting
- Button prompts not preserved
- Fallback to static prompts

**Possible Causes:**

- Import errors
- Configuration issues
- Integration code problems

**Solutions:**

1. **Check Imports:**

```python
# Ensure correct imports
from dynamic_prompt_integration import get_enhanced_agent_instructions_dynamic
from direct_prompts import DirectPromptManager
```

2. **Verify Configuration:**

```python
# Check if dynamic prompting is enabled
DYNAMIC_PROMPTING_ENABLED = os.getenv('DYNAMIC_PROMPTING_ENABLED', 'false').lower() == 'true'
```

3. **Test Integration:**

```python
# Test dynamic prompting
try:
    prompt = get_enhanced_agent_instructions_dynamic("[verbose] Get data", {})
    print("Dynamic prompting working")
except Exception as e:
    print(f"Dynamic prompting failed: {e}")
    # Fallback to static prompting
```

### 7. Performance Issues

**Symptoms:**

- Slow prompt generation
- High CPU usage
- Memory leaks

**Possible Causes:**

- Inefficient regex patterns
- Large cache sizes
- Memory leaks in template processing

**Solutions:**

1. **Optimize Regex Patterns:**

```python
# Use compiled regex patterns for better performance
import re
pattern = re.compile(r'\[(verbose|minimal|standard)\]')
```

2. **Monitor Performance:**

```python
import time
start_time = time.time()
prompt = manager.generate_prompt(user_input, context)
end_time = time.time()
print(f"Generation time: {end_time - start_time:.3f}s")
```

3. **Profile Memory Usage:**

```python
import psutil
import os

process = psutil.Process(os.getpid())
memory_usage = process.memory_info().rss / 1024 / 1024  # MB
print(f"Memory usage: {memory_usage:.2f} MB")
```

## Debugging Techniques

### 1. Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('dynamic_prompting').setLevel(logging.DEBUG)
```

### 2. Test Individual Components

```python
# Test instruction parser
parser = InstructionParser()
preferences = parser.extract_preferences("[verbose] [json] Get data")
print(f"Parsed preferences: {preferences}")

# Test template engine
engine = TemplateEngine()
template = "You are an AI. {verbosity_instruction} {format_instruction}"
result = engine.apply_preferences(template, preferences, {})
print(f"Template result: {result}")

# Test input validator
validator = InputValidator()
validator.validate_preferences(preferences)
print("Validation passed")
```

### 3. Use Debug Mode

```python
# Create debug version of manager
config = {
    'cache_size': 10,
    'debug': True,  # Enable debug mode
    'security_rules': {
        'max_input_length': 1000,
        'rate_limit': 10
    }
}
manager = DynamicPromptManager(base_template, config)
```

### 4. Monitor System Resources

```python
import psutil
import time

def monitor_resources():
    while True:
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        print(f"CPU: {cpu_percent}%, Memory: {memory_percent}%")
        time.sleep(1)

# Run in separate thread
import threading
monitor_thread = threading.Thread(target=monitor_resources)
monitor_thread.daemon = True
monitor_thread.start()
```

## Error Codes and Messages

### Validation Errors

| Error Code | Message | Solution |
|------------|---------|----------|
| `INVALID_VERBOSITY` | Invalid verbosity level: {value} | Use valid verbosity level |
| `INVALID_TOOL_USAGE` | Invalid tool usage instruction: {value} | Use valid tool names |
| `INVALID_OUTPUT_FORMAT` | Invalid output format: {value} | Use valid output format |
| `INVALID_RESPONSE_STYLE` | Invalid response style: {value} | Use valid response style |
| `INPUT_TOO_LONG` | Input exceeds maximum length | Reduce input length |
| `MALICIOUS_CONTENT` | Potentially malicious content detected | Remove dangerous characters |

### Template Errors

| Error Code | Message | Solution |
|------------|---------|----------|
| `TEMPLATE_VARIABLE_NOT_FOUND` | Template variable not found: {variable} | Check template syntax |
| `TEMPLATE_PROCESSING_FAILED` | Template processing failed | Check template format |
| `INVALID_TEMPLATE_SYNTAX` | Invalid template syntax | Fix template syntax |

### Security Errors

| Error Code | Message | Solution |
|------------|---------|----------|
| `RATE_LIMIT_EXCEEDED` | Rate limit exceeded | Wait and retry |
| `CIRCUIT_BREAKER_OPEN` | Circuit breaker is open | Wait for circuit to close |
| `AUDIT_LOG_FAILED` | Audit logging failed | Check log configuration |

## Performance Tuning

### 1. Cache Optimization

```python
# Optimize cache size based on usage patterns
cache_size = min(1000, max(50, estimated_usage * 2))

# Use LRU eviction for better performance
cache = PromptCache(max_size=cache_size)
```

### 2. Regex Optimization

```python
# Compile regex patterns for better performance
import re

class OptimizedInstructionParser:
    def __init__(self):
        self.patterns = {
            'verbosity': re.compile(r'\[(verbose|minimal|standard|detailed|brief|concise)\]', re.IGNORECASE),
            'tool_usage': re.compile(r'\[(use only|avoid|minimal tools?)(?:\s+([a-zA-Z_\s,]+))?\]', re.IGNORECASE),
            'output_format': re.compile(r'\[(structured|narrative|bullet points?|JSON|markdown|plain)\]', re.IGNORECASE),
            'response_style': re.compile(r'\[(formal|casual|technical|professional|friendly)\]', re.IGNORECASE)
        }
```

### 3. Memory Management

```python
# Clear cache periodically
import threading
import time

def periodic_cache_cleanup(cache, interval=3600):  # 1 hour
    while True:
        time.sleep(interval)
        cache.clear()
        print("Cache cleared")

# Start cleanup thread
cleanup_thread = threading.Thread(target=periodic_cache_cleanup, args=(cache,))
cleanup_thread.daemon = True
cleanup_thread.start()
```

## Monitoring and Alerting

### 1. Health Checks

```python
def health_check():
    """Check system health"""
    try:
        # Test basic functionality
        manager = DynamicPromptManager(base_template, config)
        test_input = "[verbose] Test input"
        result = manager.generate_prompt(test_input, {})
        
        # Check cache
        cache_stats = manager.cache.get_stats()
        
        # Check memory usage
        memory_usage = psutil.virtual_memory().percent
        
        return {
            'status': 'healthy',
            'cache_hit_rate': cache_stats['hit_rate'],
            'memory_usage': memory_usage,
            'response_time': 0.05  # Example
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }
```

### 2. Metrics Collection

```python
class MetricsCollector:
    def __init__(self):
        self.prompt_count = 0
        self.error_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.response_times = []
    
    def record_prompt_generation(self, success: bool, response_time: float):
        self.prompt_count += 1
        self.response_times.append(response_time)
        if not success:
            self.error_count += 1
    
    def record_cache_access(self, hit: bool):
        if hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
    
    def get_metrics(self):
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        error_rate = self.error_count / self.prompt_count if self.prompt_count > 0 else 0
        cache_hit_rate = self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0
        
        return {
            'prompt_count': self.prompt_count,
            'error_count': self.error_count,
            'error_rate': error_rate,
            'cache_hit_rate': cache_hit_rate,
            'average_response_time': avg_response_time
        }
```

### 3. Alerting

```python
def check_alerts(metrics):
    """Check for alert conditions"""
    alerts = []
    
    if metrics['error_rate'] > 0.05:  # 5% error rate
        alerts.append({
            'level': 'warning',
            'message': f"High error rate: {metrics['error_rate']:.2%}"
        })
    
    if metrics['cache_hit_rate'] < 0.7:  # 70% cache hit rate
        alerts.append({
            'level': 'info',
            'message': f"Low cache hit rate: {metrics['cache_hit_rate']:.2%}"
        })
    
    if metrics['average_response_time'] > 0.1:  # 100ms response time
        alerts.append({
            'level': 'warning',
            'message': f"Slow response time: {metrics['average_response_time']:.3f}s"
        })
    
    return alerts
```

## Getting Help

### 1. Check Logs

```python
# Enable detailed logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dynamic_prompting.log'),
        logging.StreamHandler()
    ]
)
```

### 2. Run Diagnostics

```python
def run_diagnostics():
    """Run system diagnostics"""
    print("=== Dynamic Prompting System Diagnostics ===")
    
    # Test basic functionality
    try:
        manager = DynamicPromptManager(base_template, config)
        print("✓ DynamicPromptManager created successfully")
    except Exception as e:
        print(f"✗ DynamicPromptManager creation failed: {e}")
        return
    
    # Test instruction parsing
    try:
        preferences = manager.parse_user_instructions("[verbose] [json] Test")
        print("✓ Instruction parsing working")
    except Exception as e:
        print(f"✗ Instruction parsing failed: {e}")
    
    # Test template processing
    try:
        result = manager.generate_prompt("[verbose] [json] Test", {})
        print("✓ Template processing working")
    except Exception as e:
        print(f"✗ Template processing failed: {e}")
    
    # Test cache
    try:
        cache_stats = manager.cache.get_stats()
        print(f"✓ Cache working - Size: {cache_stats['cache_size']}")
    except Exception as e:
        print(f"✗ Cache failed: {e}")
    
    print("=== Diagnostics Complete ===")

# Run diagnostics
run_diagnostics()
```

### 3. Contact Support

If you continue to experience issues:

1. **Collect Information:**
   - Error messages and stack traces
   - System configuration
   - Usage patterns
   - Performance metrics

2. **Create Issue Report:**
   - Describe the problem
   - Include steps to reproduce
   - Attach relevant logs
   - Provide system information

3. **Check Documentation:**
   - User Guide
   - Developer Guide
   - API Reference
   - Migration Guide

---

*This troubleshooting guide covers common issues and solutions for the Dynamic Adaptive Prompting System. For additional help, refer to the other documentation or contact your system administrator.*
