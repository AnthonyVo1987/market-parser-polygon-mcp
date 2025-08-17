# JSON System Troubleshooting Guide

**Market Parser JSON Architecture - Problem Resolution**

**Date**: 2025-08-17  
**Version**: 2.0.0  
**Target Audience**: Developers, System Administrators, Support Staff

---

## Table of Contents

1. [Quick Diagnosis](#quick-diagnosis)
2. [JSON Parsing Issues](#json-parsing-issues)
3. [Schema Validation Problems](#schema-validation-problems)
4. [FSM State Management Issues](#fsm-state-management-issues)
5. [UI Component Problems](#ui-component-problems)
6. [Performance Issues](#performance-issues)
7. [API Integration Problems](#api-integration-problems)
8. [Debug Logging Issues](#debug-logging-issues)
9. [Common Error Messages](#common-error-messages)
10. [Diagnostic Tools](#diagnostic-tools)

---

## Quick Diagnosis

### System Health Check

Run this quick diagnostic to identify the problem area:

```python
# Quick system health check
from json_parser import create_compatible_parser
from json_schemas import schema_registry
from stock_data_fsm import StateManager

def quick_health_check():
    print("🔍 Market Parser JSON System Health Check")
    print("=" * 50)
    
    # 1. JSON Parser Check
    try:
        parser = create_compatible_parser()
        stats = parser.get_parsing_statistics()
        print(f"✅ JSON Parser: Healthy")
        print(f"   - Supported schemas: {stats['supported_schemas']}")
        print(f"   - Validation enabled: {stats['validation_enabled']}")
    except Exception as e:
        print(f"❌ JSON Parser: Error - {e}")
    
    # 2. Schema Registry Check
    try:
        schemas = schema_registry.get_all_schemas()
        print(f"✅ Schema Registry: Healthy")
        print(f"   - Available schemas: {list(schemas.keys())}")
    except Exception as e:
        print(f"❌ Schema Registry: Error - {e}")
    
    # 3. FSM Check
    try:
        manager = StateManager()
        print(f"✅ FSM Manager: Healthy")
        print(f"   - Current state: {manager.get_current_state().value}")
    except Exception as e:
        print(f"❌ FSM Manager: Error - {e}")
    
    # 4. Dependencies Check
    try:
        import jsonschema
        import gradio
        import pandas
        print(f"✅ Dependencies: All available")
    except ImportError as e:
        print(f"❌ Dependencies: Missing - {e}")

if __name__ == "__main__":
    quick_health_check()
```

### Common Problem Categories

| Symptom | Likely Category | Quick Fix |
|---------|----------------|-----------|
| "Low confidence scores" | JSON Parsing | Check AI response format |
| "Schema validation failed" | Schema Validation | Review response structure |
| "Button stuck disabled" | FSM State | Reset FSM state |
| "JSON textbox empty" | UI Components | Check parsing success |
| "Slow response times" | Performance | Monitor system resources |
| "API connection failed" | API Integration | Check network/keys |

---

## JSON Parsing Issues

### Issue 1: Low Confidence Scores

**Symptoms**:
- Confidence consistently below 80%
- Frequent fallback to regex parsing
- Partial data extraction

**Diagnosis**:
```python
# Check parsing details
result = parser.parse_stock_snapshot(response_text, "AAPL")
print(f"Confidence: {result.confidence.value}")
print(f"Extraction method: {result.extraction_metadata.get('extraction_method')}")
print(f"Warnings: {result.warnings}")
print(f"Parse time: {result.parse_time_ms}ms")
```

**Common Causes**:
1. **AI not responding in JSON format**
2. **Malformed JSON responses**
3. **Missing schema prompts**
4. **AI model configuration issues**

**Solutions**:

**Solution 1: Check AI Response Format**
```python
# Enable debug logging to see raw responses
import logging
logging.basicConfig(level=logging.DEBUG)

# Check what the AI is actually returning
print("Raw response:")
print(repr(result.raw_response[:500]))
```

**Solution 2: Verify Prompt Templates**
```python
from prompt_templates import PromptTemplateManager, PromptType

manager = PromptTemplateManager()
prompt, context = manager.generate_prompt(PromptType.SNAPSHOT, "AAPL")

# Check if prompt includes JSON schema
if "JSON" in prompt and "schema" in prompt:
    print("✅ Prompt includes JSON schema")
else:
    print("❌ Prompt missing JSON schema requirements")
```

**Solution 3: Test JSON Extraction**
```python
# Test JSON extraction separately
test_json = '{"metadata": {"ticker_symbol": "AAPL"}, "snapshot_data": {"current_price": 150.25}}'
result = parser.parse_stock_snapshot(test_json, "AAPL")

if result.confidence == ConfidenceLevel.HIGH:
    print("✅ JSON parsing works with valid input")
    print("❌ Problem is with AI response format")
else:
    print("❌ JSON parser has internal issues")
```

### Issue 2: JSON Extraction Failures

**Symptoms**:
- "No valid JSON extracted" errors
- Immediate fallback to regex parsing
- Empty parsed_data fields

**Diagnosis**:
```python
# Test extraction patterns manually
import re
import json

def test_extraction_patterns(text):
    patterns = [
        r'```json\s*(\{.*?\})\s*```',
        r'```\s*(\{.*?\})\s*```',
        r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})',
    ]
    
    for i, pattern in enumerate(patterns, 1):
        matches = re.findall(pattern, text, re.DOTALL)
        print(f"Pattern {i}: Found {len(matches)} matches")
        
        for j, match in enumerate(matches):
            try:
                parsed = json.loads(match)
                print(f"  Match {j+1}: ✅ Valid JSON")
                return parsed
            except json.JSONDecodeError as e:
                print(f"  Match {j+1}: ❌ Invalid JSON - {e}")
    
    return None

# Test with your response
extracted = test_extraction_patterns(problematic_response)
```

**Solutions**:

**Solution 1: Enable Comprehensive Logging**
```python
# Enable JSON extraction debugging
from json_debug_logger import json_debug_logger, create_workflow_id

workflow_id = create_workflow_id()
json_debug_logger.log_json_workflow_start(workflow_id, "snapshot", "AAPL")

# This will log all extraction attempts
result = parser.parse_stock_snapshot(response_text, "AAPL")
```

**Solution 2: Check Response Format**
```python
# Analyze response characteristics
def analyze_response(text):
    analysis = {
        'length': len(text),
        'has_braces': '{' in text and '}' in text,
        'has_json_block': '```json' in text.lower(),
        'starts_with_brace': text.strip().startswith('{'),
        'brace_count': text.count('{'),
        'quote_count': text.count('"')
    }
    
    print("Response Analysis:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
    return analysis

analyze_response(problematic_response)
```

### Issue 3: JSON Repair Failures

**Symptoms**:
- JSON extraction finds content but parsing fails
- "JSON repair could not extract valid structure" messages

**Diagnosis**:
```python
# Test JSON repair manually
def manual_repair_test(text):
    # Find JSON-like content
    json_start = text.find('{')
    json_end = text.rfind('}')
    
    if json_start == -1 or json_end == -1:
        print("❌ No JSON structure found")
        return None
    
    potential_json = text[json_start:json_end + 1]
    print(f"Extracted content: {potential_json[:200]}...")
    
    # Try repairs
    repairs = [
        (r'(\w+):', r'"\1":'),  # Fix unquoted keys
        (r"'([^']*)'", r'"\1"'),  # Fix single quotes
        (r',(\s*[}\]])', r'\1'),  # Fix trailing commas
    ]
    
    repaired = potential_json
    for pattern, replacement in repairs:
        old_repaired = repaired
        repaired = re.sub(pattern, replacement, repaired)
        if repaired != old_repaired:
            print(f"Applied repair: {pattern}")
    
    try:
        parsed = json.loads(repaired)
        print("✅ Repair successful")
        return parsed
    except json.JSONDecodeError as e:
        print(f"❌ Repair failed: {e}")
        return None

manual_repair_test(problematic_response)
```

---

## Schema Validation Problems

### Issue 1: Schema Validation Failures

**Symptoms**:
- "Schema validation failed" errors
- Medium confidence with validation warnings
- Required fields missing errors

**Diagnosis**:
```python
from json_schemas import schema_registry, AnalysisType

# Test schema validation directly
def diagnose_schema_validation(data, analysis_type):
    schema_type = {
        'snapshot': AnalysisType.SNAPSHOT,
        'support_resistance': AnalysisType.SUPPORT_RESISTANCE,
        'technical': AnalysisType.TECHNICAL
    }[analysis_type]
    
    validation_result = schema_registry.validate_response(data, schema_type)
    
    print(f"Validation Result:")
    print(f"  Valid: {validation_result.get('valid', False)}")
    
    if not validation_result.get('valid', False):
        print(f"  Error: {validation_result.get('error_message', 'Unknown')}")
        print(f"  Schema path: {validation_result.get('schema_path', 'N/A')}")
        print(f"  Instance path: {validation_result.get('instance_path', 'N/A')}")
    
    return validation_result

# Test with your data
validation = diagnose_schema_validation(result.parsed_data, 'snapshot')
```

**Solutions**:

**Solution 1: Check Required Fields**
```python
# Verify all required fields are present
def check_required_fields(data, schema_type):
    schema = schema_registry.get_schema(schema_type)
    required_fields = schema.get('required', [])
    
    print(f"Required top-level fields: {required_fields}")
    
    for field in required_fields:
        if field in data:
            print(f"  ✅ {field}: present")
            
            # Check nested required fields
            if field in ['snapshot_data', 'support_levels', 'oscillators']:
                nested_schema = schema['properties'][field]
                nested_required = nested_schema.get('required', [])
                
                if nested_required:
                    print(f"    Required nested fields: {nested_required}")
                    for nested_field in nested_required:
                        if nested_field in data[field]:
                            print(f"      ✅ {nested_field}: present")
                        else:
                            print(f"      ❌ {nested_field}: MISSING")
        else:
            print(f"  ❌ {field}: MISSING")

check_required_fields(result.parsed_data, AnalysisType.SNAPSHOT)
```

**Solution 2: Validate Data Types**
```python
# Check data type compliance
def check_data_types(data):
    issues = []
    
    # Check common type issues
    if 'snapshot_data' in data:
        snapshot = data['snapshot_data']
        
        # Numeric fields should be numbers, not strings
        numeric_fields = ['current_price', 'percentage_change', 'volume', 'vwap']
        for field in numeric_fields:
            if field in snapshot:
                value = snapshot[field]
                if isinstance(value, str):
                    try:
                        float(value)
                        issues.append(f"{field} is string '{value}', should be number")
                    except ValueError:
                        issues.append(f"{field} is invalid string '{value}'")
    
    for issue in issues:
        print(f"❌ Type issue: {issue}")
    
    return len(issues) == 0

check_data_types(result.parsed_data)
```

### Issue 2: Schema Version Mismatches

**Symptoms**:
- "Schema version incompatibility" warnings
- Validation failures on valid-looking data

**Diagnosis**:
```python
# Check schema versions
def check_schema_versions():
    schemas = schema_registry.get_all_schemas()
    
    for schema_name, schema in schemas.items():
        version = schema.get('version', 'unknown')
        schema_id = schema.get('$id', 'no-id')
        print(f"{schema_name}: version {version}, id: {schema_id}")

check_schema_versions()
```

**Solution**:
```python
# Update schema version in response if needed
def fix_schema_version(data):
    if 'metadata' in data and 'schema_version' in data['metadata']:
        current_version = data['metadata']['schema_version']
        expected_version = "1.0"  # Current schema version
        
        if current_version != expected_version:
            print(f"Updating schema version from {current_version} to {expected_version}")
            data['metadata']['schema_version'] = expected_version
    
    return data
```

---

## FSM State Management Issues

### Issue 1: Stuck States

**Symptoms**:
- Buttons remain disabled after operations
- "State transition not allowed" errors
- UI not responding to interactions

**Diagnosis**:
```python
from stock_data_fsm import StateManager, AppState

# Check current FSM state
def diagnose_fsm_state():
    manager = StateManager(debug_mode=True)
    
    print(f"Current state: {manager.get_current_state().value}")
    print(f"Context: {manager.context}")
    
    # Check if state is stuck
    if manager.get_current_state() != AppState.IDLE:
        print("⚠️ FSM not in IDLE state - may be stuck")
        
        # Try to transition to IDLE
        try:
            success = manager.transition_to(AppState.IDLE)
            if success:
                print("✅ Successfully reset to IDLE")
            else:
                print("❌ Could not reset to IDLE")
        except Exception as e:
            print(f"❌ Error resetting state: {e}")

diagnose_fsm_state()
```

**Solutions**:

**Solution 1: Manual State Reset**
```python
# Force reset FSM state
def force_reset_fsm():
    manager = StateManager()
    manager.reset()  # This should always work
    print(f"✅ FSM reset to: {manager.get_current_state().value}")

force_reset_fsm()
```

**Solution 2: Check Transition Rules**
```python
# Verify transition rules
from stock_data_fsm.transitions import TransitionValidator

def check_transition_rules():
    validator = TransitionValidator()
    current_state = AppState.ANALYZING  # or whatever state you're stuck in
    target_state = AppState.IDLE
    
    is_valid = validator.is_valid_transition(current_state, target_state)
    print(f"Transition {current_state.value} → {target_state.value}: {'✅ Valid' if is_valid else '❌ Invalid'}")
    
    if not is_valid:
        valid_transitions = validator.get_valid_transitions(current_state)
        print(f"Valid transitions from {current_state.value}: {[s.value for s in valid_transitions]}")

check_transition_rules()
```

### Issue 2: Context Data Corruption

**Symptoms**:
- Incorrect ticker extraction
- Missing analysis type information
- Inconsistent state context

**Diagnosis**:
```python
# Check context data integrity
def diagnose_context_data():
    manager = StateManager()
    context = manager.context
    
    print("Context Analysis:")
    print(f"  Current ticker: {context.current_ticker}")
    print(f"  Analysis type: {context.analysis_type}")
    print(f"  Raw response length: {len(context.raw_response or '')}")
    print(f"  Parsed data keys: {list(context.parsed_data.keys()) if context.parsed_data else 'None'}")
    print(f"  Error message: {context.error_message}")
    print(f"  Debug info: {context.debug_info}")
    
    # Check for inconsistencies
    issues = []
    if context.analysis_type and not context.current_ticker:
        issues.append("Analysis type set but no ticker")
    if context.parsed_data and not context.raw_response:
        issues.append("Parsed data exists but no raw response")
    
    for issue in issues:
        print(f"⚠️ Context issue: {issue}")

diagnose_context_data()
```

---

## UI Component Problems

### Issue 1: Empty JSON Text Boxes

**Symptoms**:
- JSON text boxes show no content
- Structured data displays properly but JSON is empty

**Diagnosis**:
```python
# Check JSON serialization
def diagnose_json_display(result):
    try:
        json_str = json.dumps(result.parsed_data, indent=2)
        print(f"✅ JSON serialization successful: {len(json_str)} characters")
        print(f"Preview: {json_str[:200]}...")
        return json_str
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        
        # Check data structure
        print(f"Data type: {type(result.parsed_data)}")
        print(f"Data keys: {list(result.parsed_data.keys()) if isinstance(result.parsed_data, dict) else 'Not a dict'}")
        return None

diagnose_json_display(result)
```

**Solution**:
```python
# Ensure proper JSON formatting for UI
def safe_json_for_ui(data):
    try:
        # Convert any non-serializable objects
        serializable_data = {}
        for key, value in data.items():
            if isinstance(value, (dict, list, str, int, float, bool, type(None))):
                serializable_data[key] = value
            else:
                serializable_data[key] = str(value)
        
        return json.dumps(serializable_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"JSON serialization error: {e}"
```

### Issue 2: DataFrame Display Issues

**Symptoms**:
- Empty or malformed data tables
- "No data to display" messages when data exists

**Diagnosis**:
```python
# Check DataFrame conversion
def diagnose_dataframe_conversion(result):
    try:
        df = result.to_dataframe()
        print(f"✅ DataFrame conversion successful: {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        print(f"Sample data:\n{df.head()}")
        return df
    except Exception as e:
        print(f"❌ DataFrame conversion failed: {e}")
        
        # Check data structure for manual conversion
        if result.data_type == JsonDataType.SNAPSHOT:
            snapshot_data = result.parsed_data.get('snapshot_data', {})
            print(f"Snapshot data fields: {list(snapshot_data.keys())}")
        
        return None

diagnose_dataframe_conversion(result)
```

**Solution**:
```python
# Manual DataFrame creation for troubleshooting
def manual_dataframe_creation(result):
    items = []
    
    if result.data_type == JsonDataType.SNAPSHOT:
        snapshot_data = result.parsed_data.get('snapshot_data', {})
        for key, value in snapshot_data.items():
            items.append({
                'Metric': key.replace('_', ' ').title(),
                'Value': f"${value:.2f}" if 'price' in key else str(value)
            })
    
    df = pd.DataFrame(items)
    return df if not df.empty else pd.DataFrame({'Metric': ['No Data'], 'Value': ['N/A']})
```

---

## Performance Issues

### Issue 1: Slow Response Times

**Symptoms**:
- Analysis taking longer than 10 seconds
- Timeouts on API requests
- UI becomes unresponsive

**Diagnosis**:
```python
import time

# Profile parsing performance
def profile_parsing_performance(response_text, ticker):
    start_time = time.time()
    
    # Time each phase
    phases = {}
    
    # JSON extraction
    extraction_start = time.time()
    parser = create_compatible_parser()
    # ... (extraction happens in parse method)
    phases['total'] = time.time() - start_time
    
    result = parser.parse_stock_snapshot(response_text, ticker)
    
    # Report timing
    print(f"Performance Profile:")
    print(f"  Total time: {phases['total']*1000:.1f}ms")
    if result.parse_time_ms:
        print(f"  Reported parse time: {result.parse_time_ms:.1f}ms")
    
    # Check for bottlenecks
    if phases['total'] > 2.0:  # More than 2 seconds
        print("⚠️ Performance issue detected")
        
        # Check extraction metadata
        extraction_time = result.extraction_metadata.get('json_extraction_time_ms', 0)
        validation_time = result.extraction_metadata.get('validation_time_ms', 0)
        
        print(f"  JSON extraction: {extraction_time:.1f}ms")
        print(f"  Schema validation: {validation_time:.1f}ms")
    
    return result

profile_parsing_performance(response_text, "AAPL")
```

**Solutions**:

**Solution 1: Enable Performance Monitoring**
```python
# Add performance monitoring
def monitor_performance():
    # Check system resources
    import psutil
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    print(f"System Performance:")
    print(f"  CPU usage: {cpu_percent}%")
    print(f"  Memory usage: {memory.percent}%")
    print(f"  Available memory: {memory.available / (1024**3):.1f} GB")
    
    if cpu_percent > 80:
        print("⚠️ High CPU usage may affect performance")
    if memory.percent > 85:
        print("⚠️ High memory usage may affect performance")

monitor_performance()
```

**Solution 2: Optimize JSON Processing**
```python
# Optimize for large responses
def optimize_json_processing():
    # Limit response size for processing
    MAX_RESPONSE_SIZE = 50000  # 50KB limit
    
    def truncate_response(text):
        if len(text) > MAX_RESPONSE_SIZE:
            print(f"⚠️ Truncating large response: {len(text)} → {MAX_RESPONSE_SIZE} chars")
            return text[:MAX_RESPONSE_SIZE]
        return text
    
    # Use faster JSON parsing for large responses
    def fast_json_parse(text):
        try:
            import orjson  # Faster JSON library if available
            return orjson.loads(text)
        except ImportError:
            return json.loads(text)
```

### Issue 2: Memory Usage Issues

**Symptoms**:
- Application memory usage grows over time
- Out of memory errors
- System becomes sluggish

**Diagnosis**:
```python
import gc
import tracemalloc

# Monitor memory usage
def diagnose_memory_usage():
    tracemalloc.start()
    
    # Simulate parsing operations
    for i in range(10):
        result = parser.parse_stock_snapshot(test_response, "AAPL")
        
        # Force garbage collection
        gc.collect()
        
        # Check memory
        current, peak = tracemalloc.get_traced_memory()
        print(f"Iteration {i+1}: Current={current/1024/1024:.1f}MB, Peak={peak/1024/1024:.1f}MB")
    
    tracemalloc.stop()

diagnose_memory_usage()
```

**Solution**:
```python
# Implement memory management
def manage_memory():
    # Clear large objects explicitly
    def clear_response_cache():
        # Clear any cached responses
        parser._response_cache = {}  # If implemented
        
    # Limit context history
    def limit_context_size(context, max_size=1000000):  # 1MB limit
        if hasattr(context, 'raw_response') and context.raw_response:
            if len(context.raw_response) > max_size:
                context.raw_response = context.raw_response[:max_size]
```

---

## API Integration Problems

### Issue 1: MCP Server Connection Issues

**Symptoms**:
- "MCP server connection failed" errors
- API timeout errors
- No market data returned

**Diagnosis**:
```python
# Test MCP server connectivity
def test_mcp_connection():
    try:
        from market_parser_demo import create_polygon_mcp_server
        
        server = create_polygon_mcp_server()
        print(f"✅ MCP server created successfully")
        
        # Test basic functionality (if available)
        # This would depend on the specific MCP server implementation
        
    except Exception as e:
        print(f"❌ MCP server connection failed: {e}")
        
        # Check environment variables
        import os
        api_key = os.getenv('POLYGON_API_KEY')
        if not api_key:
            print("❌ POLYGON_API_KEY not set")
        elif len(api_key) < 10:
            print("❌ POLYGON_API_KEY appears invalid (too short)")
        else:
            print(f"✅ POLYGON_API_KEY configured (length: {len(api_key)})")

test_mcp_connection()
```

**Solutions**:

**Solution 1: Verify API Keys**
```bash
# Check environment configuration
echo "Polygon API Key length: ${#POLYGON_API_KEY}"
echo "OpenAI API Key length: ${#OPENAI_API_KEY}"

# Test API connectivity
curl -H "Authorization: Bearer $POLYGON_API_KEY" \
     "https://api.polygon.io/v1/meta/symbols/AAPL/company"
```

**Solution 2: Test Network Connectivity**
```python
import requests

def test_api_connectivity():
    # Test Polygon.io connectivity
    try:
        response = requests.get("https://api.polygon.io/v1/meta/symbols", timeout=5)
        print(f"✅ Polygon.io reachable: HTTP {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Polygon.io unreachable: {e}")
    
    # Test OpenAI connectivity
    try:
        response = requests.get("https://api.openai.com/v1/models", timeout=5)
        print(f"✅ OpenAI reachable: HTTP {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ OpenAI unreachable: {e}")

test_api_connectivity()
```

### Issue 2: AI Model Response Issues

**Symptoms**:
- AI not following JSON format
- Inconsistent response structure
- Model timeout errors

**Diagnosis**:
```python
# Test AI model directly
async def test_ai_model():
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIResponsesModel
    
    model = OpenAIResponsesModel("gpt-4o-mini")
    agent = Agent(model=model)
    
    # Test basic functionality
    try:
        result = await agent.run_sync("What is 2+2?")
        print(f"✅ AI model responding: {result.data}")
    except Exception as e:
        print(f"❌ AI model error: {e}")
    
    # Test JSON response
    json_prompt = """
    Respond with JSON only: {"test": "value", "number": 42}
    """
    try:
        result = await agent.run_sync(json_prompt)
        print(f"✅ AI JSON test: {result.data}")
    except Exception as e:
        print(f"❌ AI JSON test failed: {e}")

# Run async test
import asyncio
asyncio.run(test_ai_model())
```

---

## Debug Logging Issues

### Issue 1: Missing Debug Information

**Symptoms**:
- Debug logs are empty or minimal
- Cannot trace parsing failures
- No workflow tracking

**Diagnosis**:
```python
# Check logging configuration
import logging

def diagnose_logging_setup():
    # Check current logging level
    logger = logging.getLogger('json_parser')
    print(f"Current log level: {logger.level}")
    print(f"Effective level: {logger.getEffectiveLevel()}")
    
    # Check handlers
    handlers = logger.handlers
    if not handlers:
        print("❌ No log handlers configured")
    else:
        for i, handler in enumerate(handlers):
            print(f"✅ Handler {i+1}: {type(handler).__name__} - Level: {handler.level}")

diagnose_logging_setup()
```

**Solution**:
```python
# Enable comprehensive debug logging
def enable_debug_logging():
    import logging
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('debug.log')
        ]
    )
    
    # Enable specific module logging
    loggers = ['json_parser', 'json_debug_logger', 'stock_data_fsm']
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        print(f"✅ Enabled debug logging for {logger_name}")

enable_debug_logging()
```

### Issue 2: Log File Issues

**Symptoms**:
- Log files not being created
- Permission errors writing logs
- Log files growing too large

**Diagnosis**:
```python
import os

def diagnose_log_files():
    log_files = [
        'json_workflow_debug.log',
        'production_parser_debug.log',
        'debug.log'
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            size = os.path.getsize(log_file)
            print(f"✅ {log_file}: {size:,} bytes")
            
            if size > 10 * 1024 * 1024:  # 10MB
                print(f"⚠️ {log_file} is large - consider rotation")
        else:
            print(f"❌ {log_file}: Not found")
            
            # Check if directory is writable
            directory = os.path.dirname(log_file) or '.'
            if os.access(directory, os.W_OK):
                print(f"✅ Directory {directory} is writable")
            else:
                print(f"❌ Directory {directory} is not writable")

diagnose_log_files()
```

---

## Common Error Messages

### Error: "JSON parsing failed - no valid JSON found"

**Cause**: AI response doesn't contain valid JSON
**Solution**:
1. Check AI prompt includes JSON schema requirements
2. Verify AI model is following instructions
3. Enable debug logging to see raw response

### Error: "Schema validation failed: required field missing"

**Cause**: Response missing required schema fields
**Solution**:
1. Check which fields are missing in validation details
2. Update AI prompt to emphasize required fields
3. Consider if field is actually optional

### Error: "FSM transition not allowed from ANALYZING to IDLE"

**Cause**: Invalid state transition attempted
**Solution**:
1. Check current FSM state
2. Reset FSM if stuck: `state_manager.reset()`
3. Review state transition logic

### Error: "Confidence score too low: 0.45"

**Cause**: Data quality below acceptable threshold
**Solution**:
1. Check if fallback parsing was used
2. Improve AI prompt clarity
3. Consider if partial data is acceptable

### Error: "MCP server connection timeout"

**Cause**: Network or API connectivity issues
**Solution**:
1. Verify internet connectivity
2. Check API keys are valid
3. Test API endpoints directly

---

## Diagnostic Tools

### Comprehensive System Test

```python
#!/usr/bin/env python3
"""
Comprehensive Market Parser JSON System Test
Run this script to diagnose all major system components
"""

import json
import time
import logging
from datetime import datetime

def comprehensive_system_test():
    """Run complete system diagnostic"""
    
    print("🔍 MARKET PARSER JSON SYSTEM DIAGNOSTIC")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    results = {}
    
    # Test 1: Component Availability
    print("📦 Testing Component Availability...")
    try:
        from json_parser import create_compatible_parser, JsonParser, JsonDataType
        from json_schemas import schema_registry, AnalysisType
        from stock_data_fsm import StateManager, AppState
        from json_debug_logger import json_debug_logger
        results['components'] = 'PASS'
        print("   ✅ All components available")
    except ImportError as e:
        results['components'] = f'FAIL: {e}'
        print(f"   ❌ Component missing: {e}")
    
    # Test 2: Parser Functionality
    print("\n🔧 Testing Parser Functionality...")
    try:
        parser = create_compatible_parser()
        
        # Test with valid JSON
        test_json = {
            "metadata": {
                "timestamp": "2025-08-17T10:30:00Z",
                "ticker_symbol": "TEST",
                "schema_version": "1.0"
            },
            "snapshot_data": {
                "current_price": 100.0,
                "percentage_change": 1.0,
                "dollar_change": 1.0,
                "volume": 1000000,
                "vwap": 99.5,
                "open": 99.0,
                "high": 101.0,
                "low": 98.0,
                "close": 99.5
            }
        }
        
        json_text = json.dumps(test_json)
        result = parser.parse_stock_snapshot(json_text, "TEST")
        
        if result.confidence.value in ['high', 'medium']:
            results['parser'] = 'PASS'
            print("   ✅ Parser working correctly")
        else:
            results['parser'] = f'FAIL: Low confidence {result.confidence.value}'
            print(f"   ❌ Parser issue: {result.confidence.value}")
            
    except Exception as e:
        results['parser'] = f'FAIL: {e}'
        print(f"   ❌ Parser error: {e}")
    
    # Test 3: Schema Validation
    print("\n📋 Testing Schema Validation...")
    try:
        validation_result = schema_registry.validate_response(
            test_json, AnalysisType.SNAPSHOT
        )
        
        if validation_result.get('valid', False):
            results['validation'] = 'PASS'
            print("   ✅ Schema validation working")
        else:
            results['validation'] = f'FAIL: {validation_result.get("error_message")}'
            print(f"   ❌ Validation failed: {validation_result.get('error_message')}")
            
    except Exception as e:
        results['validation'] = f'FAIL: {e}'
        print(f"   ❌ Validation error: {e}")
    
    # Test 4: FSM State Management
    print("\n🔄 Testing FSM State Management...")
    try:
        manager = StateManager()
        
        # Test state transitions
        initial_state = manager.get_current_state()
        success = manager.transition_to(AppState.ANALYZING)
        
        if success and manager.get_current_state() == AppState.ANALYZING:
            manager.reset()  # Reset to initial state
            results['fsm'] = 'PASS'
            print("   ✅ FSM working correctly")
        else:
            results['fsm'] = 'FAIL: State transition failed'
            print("   ❌ FSM transition failed")
            
    except Exception as e:
        results['fsm'] = f'FAIL: {e}'
        print(f"   ❌ FSM error: {e}")
    
    # Test 5: Performance Check
    print("\n⚡ Testing Performance...")
    try:
        start_time = time.time()
        
        # Run multiple parsing operations
        for i in range(5):
            result = parser.parse_stock_snapshot(json_text, f"TEST{i}")
        
        avg_time = (time.time() - start_time) / 5 * 1000  # ms
        
        if avg_time < 500:  # Under 500ms is good
            results['performance'] = 'PASS'
            print(f"   ✅ Performance good: {avg_time:.1f}ms average")
        else:
            results['performance'] = f'SLOW: {avg_time:.1f}ms average'
            print(f"   ⚠️ Performance slow: {avg_time:.1f}ms average")
            
    except Exception as e:
        results['performance'] = f'FAIL: {e}'
        print(f"   ❌ Performance test error: {e}")
    
    # Summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("-" * 40)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result == 'PASS')
    
    for test, result in results.items():
        status = "✅" if result == "PASS" else "❌"
        print(f"{status} {test.upper()}: {result}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All systems operational!")
    else:
        print("⚠️ Some issues detected - see details above")
    
    return results

if __name__ == "__main__":
    comprehensive_system_test()
```

### Performance Monitoring Script

```python
#!/usr/bin/env python3
"""
Performance monitoring for Market Parser JSON system
"""

import time
import psutil
import threading
from collections import defaultdict

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.monitoring = False
    
    def start_monitoring(self):
        """Start background performance monitoring"""
        self.monitoring = True
        thread = threading.Thread(target=self._monitor_loop)
        thread.daemon = True
        thread.start()
        print("📊 Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring and report results"""
        self.monitoring = False
        self._report_metrics()
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            # Collect system metrics
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            
            self.metrics['cpu'].append(cpu)
            self.metrics['memory'].append(memory)
            
            time.sleep(1)
    
    def _report_metrics(self):
        """Report collected metrics"""
        print("\n📈 Performance Report")
        print("-" * 30)
        
        if self.metrics['cpu']:
            avg_cpu = sum(self.metrics['cpu']) / len(self.metrics['cpu'])
            max_cpu = max(self.metrics['cpu'])
            print(f"CPU Usage: Avg {avg_cpu:.1f}%, Max {max_cpu:.1f}%")
        
        if self.metrics['memory']:
            avg_mem = sum(self.metrics['memory']) / len(self.metrics['memory'])
            max_mem = max(self.metrics['memory'])
            print(f"Memory Usage: Avg {avg_mem:.1f}%, Max {max_mem:.1f}%")

# Usage example
monitor = PerformanceMonitor()
monitor.start_monitoring()

# Run your tests here
# ... test operations ...

monitor.stop_monitoring()
```

This comprehensive troubleshooting guide provides the tools and knowledge needed to diagnose and resolve issues with the Market Parser JSON system. Use the diagnostic tools regularly to maintain system health and quickly identify problems when they occur.