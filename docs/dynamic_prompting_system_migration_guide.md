# Dynamic Adaptive Prompting System - Migration Guide

## Overview

This guide helps you migrate from the existing static prompting system to the new Dynamic Adaptive Prompting System. The migration is designed to be backward-compatible, allowing for gradual adoption.

## Migration Strategy

### Phase 1: Preparation

- Review current system architecture
- Understand new features and capabilities
- Plan migration timeline
- Set up testing environment

### Phase 2: Implementation

- Install new system components
- Update configuration
- Modify integration points
- Test functionality

### Phase 3: Deployment

- Deploy to staging environment
- Run comprehensive tests
- Deploy to production
- Monitor system performance

### Phase 4: Optimization

- Fine-tune configuration
- Optimize performance
- Gather user feedback
- Implement improvements

## Pre-Migration Checklist

### System Requirements

- [ ] Python 3.8 or higher
- [ ] Sufficient memory (recommended: 2GB+)
- [ ] Disk space for logs and cache (recommended: 1GB+)
- [ ] Network connectivity for external dependencies

### Current System Analysis

- [ ] Document current prompt usage patterns
- [ ] Identify integration points
- [ ] Review performance requirements
- [ ] Assess security requirements
- [ ] Plan fallback strategies

### Testing Environment

- [ ] Set up isolated testing environment
- [ ] Prepare test data and scenarios
- [ ] Configure monitoring and logging
- [ ] Plan rollback procedures

## Step-by-Step Migration

### Step 1: Install New Components

1. **Add new files to your project:**

```bash
# Core components
src/backend/dynamic_prompts.py
src/backend/dynamic_prompt_manager.py
src/backend/dynamic_prompt_integration.py

# Security components
src/backend/security_features.py
src/backend/secure_prompt_manager.py

# Advanced features
src/backend/advanced_prompting_features.py

# Tests
tests/test_dynamic_prompting_system.py
tests/test_integration.py
```

2. **Update requirements.txt:**

```txt
# Existing dependencies
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0

# New dependencies for dynamic prompting
# (No additional dependencies required - uses standard library)
```

### Step 2: Update Configuration

1. **Add environment variables:**

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

2. **Create configuration file (optional):**

```yaml
# config/dynamic_prompting.yaml
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

### Step 3: Update Integration Points

1. **Update main.py imports:**

```python
# Add new imports
from dynamic_prompt_integration import get_enhanced_agent_instructions_dynamic
from dynamic_prompt_integration import get_enhanced_agent_instructions_secure

# Keep existing imports for fallback
from main import get_enhanced_agent_instructions_static
```

2. **Update get_enhanced_agent_instructions function:**

```python
def get_enhanced_agent_instructions(user_input: str = "", context: Dict[str, Any] = None) -> str:
    """
    Enhanced agent instructions with dynamic prompting support.
    Falls back to static prompting if dynamic prompting fails.
    """
    try:
        # Try dynamic prompt generation
        return get_enhanced_agent_instructions_dynamic(user_input, context or {})
    except Exception as e:
        # Log the error for debugging
        logger.warning(f"Dynamic prompting failed, falling back to static: {e}")
        
        # Fallback to static prompt
        return get_enhanced_agent_instructions_static()
```

3. **Update CLI integration:**

```python
# In CLI functions, pass user input to get_enhanced_agent_instructions
def cli_function(user_input: str):
    # Get enhanced instructions with user input
    instructions = get_enhanced_agent_instructions(user_input, {"source": "cli"})
    
    # Use instructions for AI interaction
    # ... rest of CLI logic
```

4. **Update GUI integration:**

```python
# In chat endpoint, use dynamic prompting for user messages
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.is_button_prompt:
        # Use dynamic prompting for user messages
        system_prompt = get_enhanced_agent_instructions(
            request.message, 
            {"source": "gui", "user_id": request.user_id}
        )
    else:
        # Use direct prompts for button interactions (unchanged)
        system_prompt = direct_prompt_manager.generate_direct_prompt(
            request.message, 
            request.intent
        )
    
    # ... rest of chat logic
```

### Step 4: Test the Migration

1. **Run unit tests:**

```bash
python -m pytest tests/test_dynamic_prompting_system.py -v
```

2. **Run integration tests:**

```bash
python -m pytest tests/test_integration.py -v
```

3. **Test CLI functionality:**

```bash
# Test with dynamic prompting
python src/backend/main.py --input "[verbose] [json] Get market data"

# Test with fallback
python src/backend/main.py --input "Get market data"
```

4. **Test GUI functionality:**

```bash
# Start the application
python src/backend/main.py

# Test in browser
# Navigate to http://localhost:3000
# Test various input formats with preferences
```

### Step 5: Deploy to Staging

1. **Deploy to staging environment:**

```bash
# Copy files to staging
scp -r src/backend/dynamic_* staging-server:/app/src/backend/
scp -r tests/test_*_prompting* staging-server:/app/tests/
scp config/dynamic_prompting.yaml staging-server:/app/config/

# Update environment variables
# Set DYNAMIC_PROMPTING_ENABLED=true in staging
```

2. **Run comprehensive tests:**

```bash
# Run all tests
python -m pytest tests/ -v

# Run performance tests
python tests/test_performance.py

# Run user acceptance tests
python tests/test_user_acceptance.py
```

3. **Monitor system performance:**

```bash
# Check logs
tail -f logs/dynamic_prompting.log

# Monitor metrics
python scripts/monitor_metrics.py
```

### Step 6: Deploy to Production

1. **Deploy to production:**

```bash
# Create backup
cp -r src/backend src/backend.backup

# Deploy new files
scp -r src/backend/dynamic_* production-server:/app/src/backend/
scp -r tests/test_*_prompting* production-server:/app/tests/
scp config/dynamic_prompting.yaml production-server:/app/config/

# Update environment variables
# Set DYNAMIC_PROMPTING_ENABLED=true in production
```

2. **Monitor deployment:**

```bash
# Check application logs
tail -f logs/application.log

# Monitor system metrics
python scripts/monitor_system.py

# Check error rates
python scripts/check_errors.py
```

3. **Verify functionality:**

```bash
# Test basic functionality
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "[verbose] [json] Get market data", "is_button_prompt": false}'

# Test fallback functionality
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Get market data", "is_button_prompt": false}'
```

## Configuration Migration

### Environment Variables

**Before (Static System):**

```bash
# No dynamic prompting configuration
```

**After (Dynamic System):**

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

### Application Configuration

**Before (Static System):**

```python
# Simple configuration
config = {
    'debug': False,
    'log_level': 'INFO'
}
```

**After (Dynamic System):**

```python
# Enhanced configuration
config = {
    'debug': False,
    'log_level': 'INFO',
    'dynamic_prompting': {
        'enabled': True,
        'cache_size': 100,
        'rate_limit': 10
    },
    'security': {
        'max_input_length': 1000,
        'enable_audit_logging': True,
        'enable_circuit_breaker': True
    },
    'performance': {
        'cache_ttl': 3600,
        'background_processing': True
    }
}
```

## Code Migration Examples

### CLI Integration

**Before (Static System):**

```python
def cli_function():
    # Get static instructions
    instructions = get_enhanced_agent_instructions()
    
    # Use instructions for AI interaction
    # ... rest of CLI logic
```

**After (Dynamic System):**

```python
def cli_function(user_input: str = ""):
    # Get dynamic instructions with user input
    instructions = get_enhanced_agent_instructions(
        user_input, 
        {"source": "cli"}
    )
    
    # Use instructions for AI interaction
    # ... rest of CLI logic
```

### GUI Integration

**Before (Static System):**

```python
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Always use static instructions
    system_prompt = get_enhanced_agent_instructions()
    
    # ... rest of chat logic
```

**After (Dynamic System):**

```python
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.is_button_prompt:
        # Use dynamic prompting for user messages
        system_prompt = get_enhanced_agent_instructions(
            request.message, 
            {"source": "gui", "user_id": request.user_id}
        )
    else:
        # Use direct prompts for button interactions (unchanged)
        system_prompt = direct_prompt_manager.generate_direct_prompt(
            request.message, 
            request.intent
        )
    
    # ... rest of chat logic
```

### Error Handling

**Before (Static System):**

```python
def get_enhanced_agent_instructions():
    # Simple static prompt
    return "You are a helpful AI assistant..."
```

**After (Dynamic System):**

```python
def get_enhanced_agent_instructions(user_input: str = "", context: Dict[str, Any] = None) -> str:
    try:
        # Try dynamic prompt generation
        return get_enhanced_agent_instructions_dynamic(user_input, context or {})
    except Exception as e:
        # Log the error for debugging
        logger.warning(f"Dynamic prompting failed, falling back to static: {e}")
        
        # Fallback to static prompt
        return get_enhanced_agent_instructions_static()
```

## Testing Migration

### Unit Tests

**Before (Static System):**

```python
def test_get_enhanced_agent_instructions():
    result = get_enhanced_agent_instructions()
    assert isinstance(result, str)
    assert len(result) > 0
```

**After (Dynamic System):**

```python
def test_get_enhanced_agent_instructions_static():
    result = get_enhanced_agent_instructions_static()
    assert isinstance(result, str)
    assert len(result) > 0

def test_get_enhanced_agent_instructions_dynamic():
    result = get_enhanced_agent_instructions_dynamic("[verbose] Get data", {})
    assert isinstance(result, str)
    assert len(result) > 0
    assert "comprehensive information" in result

def test_get_enhanced_agent_instructions_fallback():
    # Test fallback when dynamic prompting fails
    with patch('dynamic_prompt_integration.get_enhanced_agent_instructions_dynamic', side_effect=Exception("Test error")):
        result = get_enhanced_agent_instructions("test input", {})
        assert isinstance(result, str)
        assert len(result) > 0
```

### Integration Tests

**Before (Static System):**

```python
def test_cli_integration():
    # Test CLI with static prompting
    result = cli_function()
    assert result is not None
```

**After (Dynamic System):**

```python
def test_cli_integration_static():
    # Test CLI with static prompting
    result = cli_function("")
    assert result is not None

def test_cli_integration_dynamic():
    # Test CLI with dynamic prompting
    result = cli_function("[verbose] [json] Get market data")
    assert result is not None

def test_gui_integration():
    # Test GUI with dynamic prompting
    response = client.post("/chat", json={
        "message": "[verbose] [json] Get market data",
        "is_button_prompt": False
    })
    assert response.status_code == 200
```

## Performance Considerations

### Memory Usage

**Before (Static System):**

- Minimal memory usage
- No caching overhead

**After (Dynamic System):**

- Additional memory for caching
- Template processing overhead
- Security validation overhead

**Optimization:**

```python
# Configure cache size based on available memory
cache_size = min(1000, max(50, available_memory_mb // 2))

# Use memory-efficient data structures
config = {
    'cache_size': cache_size,
    'security_rules': {
        'max_input_length': 1000,
        'rate_limit': 10
    }
}
```

### Response Time

**Before (Static System):**

- Instant response (static prompt)
- No processing overhead

**After (Dynamic System):**

- Slight processing overhead
- Cache benefits for repeated requests
- Template processing time

**Optimization:**

```python
# Use compiled regex patterns
import re
pattern = re.compile(r'\[(verbose|minimal|standard)\]')

# Optimize cache configuration
config = {
    'cache_size': 200,  # Larger cache for better hit rates
    'security_rules': {
        'max_input_length': 1000,
        'rate_limit': 10
    }
}
```

## Rollback Procedures

### Emergency Rollback

If issues occur during migration:

1. **Disable dynamic prompting:**

```bash
# Set environment variable
export DYNAMIC_PROMPTING_ENABLED=false

# Restart application
systemctl restart market-parser
```

2. **Restore backup files:**

```bash
# Restore from backup
cp -r src/backend.backup/* src/backend/

# Restart application
systemctl restart market-parser
```

3. **Verify rollback:**

```bash
# Check application logs
tail -f logs/application.log

# Test basic functionality
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Get market data", "is_button_prompt": false}'
```

### Gradual Rollback

For partial rollback:

1. **Disable specific features:**

```bash
# Disable security features
export SECURITY_ENABLE_AUDIT_LOGGING=false
export SECURITY_ENABLE_CIRCUIT_BREAKER=false

# Disable caching
export DYNAMIC_PROMPTING_CACHE_SIZE=0
```

2. **Monitor system performance:**

```bash
# Check error rates
python scripts/check_errors.py

# Monitor response times
python scripts/monitor_performance.py
```

## Post-Migration Tasks

### 1. Monitor System Performance

```bash
# Set up monitoring
python scripts/setup_monitoring.py

# Check key metrics
python scripts/check_metrics.py
```

### 2. Gather User Feedback

```bash
# Collect usage statistics
python scripts/collect_usage_stats.py

# Analyze user preferences
python scripts/analyze_preferences.py
```

### 3. Optimize Configuration

```bash
# Analyze performance data
python scripts/analyze_performance.py

# Update configuration based on findings
python scripts/update_config.py
```

### 4. Update Documentation

- Update user documentation
- Update developer documentation
- Update API documentation
- Update troubleshooting guide

## Troubleshooting Migration Issues

### Common Issues

1. **Import Errors:**

```python
# Check import paths
from dynamic_prompt_integration import get_enhanced_agent_instructions_dynamic

# Verify file locations
ls -la src/backend/dynamic_*
```

2. **Configuration Issues:**

```bash
# Check environment variables
env | grep DYNAMIC_PROMPTING

# Verify configuration files
cat config/dynamic_prompting.yaml
```

3. **Performance Issues:**

```bash
# Check system resources
top
free -h
df -h

# Monitor application logs
tail -f logs/dynamic_prompting.log
```

### Getting Help

1. **Check logs:**

```bash
# Application logs
tail -f logs/application.log

# Dynamic prompting logs
tail -f logs/dynamic_prompting.log

# Error logs
tail -f logs/error.log
```

2. **Run diagnostics:**

```bash
# Run system diagnostics
python scripts/run_diagnostics.py

# Check system health
python scripts/health_check.py
```

3. **Contact support:**

- Provide error messages and stack traces
- Include system configuration
- Attach relevant logs
- Describe steps to reproduce

## Success Metrics

### Performance Metrics

- [ ] Response time < 100ms (95th percentile)
- [ ] Cache hit rate > 70%
- [ ] Error rate < 1%
- [ ] Memory usage < 2GB

### Functionality Metrics

- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] User acceptance tests passing
- [ ] Button prompts preserved

### User Experience Metrics

- [ ] User satisfaction > 90%
- [ ] Feature adoption > 50%
- [ ] Support tickets < 5% increase
- [ ] Performance complaints < 1%

---

*This migration guide provides comprehensive instructions for migrating from the static prompting system to the Dynamic Adaptive Prompting System. Follow the steps carefully and test thoroughly before deploying to production.*
