# JSON API Reference

**Market Parser JSON System - Complete API Documentation**

**Date**: 2025-08-17  
**Version**: 2.0.0  
**API Type**: JSON Schema-Driven Financial Data Processing

---

## Table of Contents

1. [Overview](#overview)
2. [JSON Schemas](#json-schemas)
3. [Parser API](#parser-api)
4. [Schema Validation API](#schema-validation-api)
5. [FSM State Management API](#fsm-state-management-api)
6. [Prompt Template API](#prompt-template-api)
7. [Debug Logging API](#debug-logging-api)
8. [Error Handling](#error-handling)
9. [Usage Examples](#usage-examples)
10. [Migration from Legacy API](#migration-from-legacy-api)

---

## Overview

The Market Parser JSON API provides structured financial data processing with schema validation, confidence scoring, and comprehensive error handling. The API is designed for both programmatic access and integration with the Gradio web interface.

### Core Components

- **JSON Parser**: Primary parsing engine with fallback strategies
- **Schema Registry**: Centralized schema management and validation
- **FSM Manager**: State management for complex workflows
- **Debug Logger**: Comprehensive logging and monitoring

### Supported Analysis Types

- **Snapshot**: Current stock price and trading metrics
- **Support & Resistance**: Technical analysis price levels  
- **Technical**: Technical indicators and moving averages

---

## JSON Schemas

### Schema Structure

All schemas follow JSON Schema Draft 2020-12 specification with:

- **Metadata Section**: Timestamps, confidence scoring, version tracking
- **Data Section**: Analysis-specific structured data
- **Validation Section**: Data quality indicators and warnings

### Snapshot Schema

**Schema ID**: `https://market-parser.com/schemas/snapshot/v1.0`  
**Purpose**: Current stock trading data and metrics

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://market-parser.com/schemas/snapshot/v1.0",
  "type": "object",
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp when analysis was generated"
        },
        "ticker_symbol": {
          "type": "string",
          "pattern": "^[A-Z]{1,5}$",
          "description": "Stock ticker symbol in uppercase"
        },
        "company_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        },
        "confidence_score": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        },
        "schema_version": {
          "type": "string",
          "const": "1.0"
        }
      },
      "required": ["timestamp", "ticker_symbol", "schema_version"]
    },
    "snapshot_data": {
      "type": "object",
      "properties": {
        "current_price": {
          "type": "number",
          "minimum": 0.01,
          "maximum": 1000000,
          "multipleOf": 0.01
        },
        "percentage_change": {
          "type": "number",
          "minimum": -99.99,
          "maximum": 999.99
        },
        "dollar_change": {
          "type": "number",
          "minimum": -10000,
          "maximum": 10000
        },
        "volume": {
          "type": "integer",
          "minimum": 0,
          "maximum": 999999999999
        },
        "vwap": {
          "type": "number",
          "minimum": 0.01,
          "maximum": 1000000,
          "multipleOf": 0.01
        },
        "open": {
          "type": "number",
          "minimum": 0.01,
          "maximum": 1000000,
          "multipleOf": 0.01
        },
        "high": {
          "type": "number",
          "minimum": 0.01,
          "maximum": 1000000,
          "multipleOf": 0.01
        },
        "low": {
          "type": "number",
          "minimum": 0.01,
          "maximum": 1000000,
          "multipleOf": 0.01
        },
        "close": {
          "type": "number",
          "minimum": 0.01,
          "maximum": 1000000,
          "multipleOf": 0.01
        }
      },
      "required": [
        "current_price", "percentage_change", "dollar_change",
        "volume", "vwap", "open", "high", "low", "close"
      ]
    }
  },
  "required": ["metadata", "snapshot_data"]
}
```

### Support & Resistance Schema

**Schema ID**: `https://market-parser.com/schemas/support-resistance/v1.0`  
**Purpose**: Technical analysis support and resistance levels

```json
{
  "support_levels": {
    "S1": {
      "price": {"type": "number", "minimum": 0.01},
      "strength": {"type": "string", "enum": ["strong", "moderate", "weak"]},
      "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0}
    },
    "S2": {
      "price": {"type": "number", "minimum": 0.01},
      "strength": {"type": "string", "enum": ["strong", "moderate", "weak"]},
      "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0}
    },
    "S3": {
      "price": {"type": "number", "minimum": 0.01},
      "strength": {"type": "string", "enum": ["strong", "moderate", "weak"]},
      "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0}
    }
  },
  "resistance_levels": {
    "R1": {
      "price": {"type": "number", "minimum": 0.01},
      "strength": {"type": "string", "enum": ["strong", "moderate", "weak"]},
      "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0}
    },
    "R2": {
      "price": {"type": "number", "minimum": 0.01},
      "strength": {"type": "string", "enum": ["strong", "moderate", "weak"]},
      "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0}
    },
    "R3": {
      "price": {"type": "number", "minimum": 0.01},
      "strength": {"type": "string", "enum": ["strong", "moderate", "weak"]},
      "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0}
    }
  },
  "analysis_context": {
    "current_price": {"type": "number", "minimum": 0.01},
    "methodology": {
      "type": "string", 
      "enum": ["pivot_points", "fibonacci", "moving_averages", "price_action", "combined"]
    }
  }
}
```

### Technical Analysis Schema

**Schema ID**: `https://market-parser.com/schemas/technical/v1.0`  
**Purpose**: Technical indicators and moving averages

```json
{
  "oscillators": {
    "RSI": {
      "value": {"type": "number", "minimum": 0, "maximum": 100},
      "interpretation": {"type": "string", "enum": ["oversold", "neutral", "overbought"]},
      "period": {"type": "integer", "minimum": 1, "maximum": 200, "default": 14}
    },
    "MACD": {
      "value": {"type": "number", "minimum": -1000, "maximum": 1000},
      "signal": {"type": "number", "minimum": -1000, "maximum": 1000},
      "histogram": {"type": "number", "minimum": -1000, "maximum": 1000},
      "interpretation": {"type": "string", "enum": ["bullish", "bearish", "neutral"]}
    }
  },
  "moving_averages": {
    "exponential": {
      "EMA_5": {"type": "number", "minimum": 0.01, "maximum": 1000000},
      "EMA_10": {"type": "number", "minimum": 0.01, "maximum": 1000000},
      "EMA_20": {"type": "number", "minimum": 0.01, "maximum": 1000000},
      "EMA_50": {"type": "number", "minimum": 0.01, "maximum": 1000000},
      "EMA_200": {"type": "number", "minimum": 0.01, "maximum": 1000000}
    },
    "simple": {
      "SMA_5": {"type": "number", "minimum": 0.01, "maximum": 1000000},
      "SMA_10": {"type": "number", "minimum": 0.01, "maximum": 1000000},
      "SMA_20": {"type": "number", "minimum": 0.01, "maximum": 1000000},
      "SMA_50": {"type": "number", "minimum": 0.01, "maximum": 1000000},
      "SMA_200": {"type": "number", "minimum": 0.01, "maximum": 1000000}
    }
  },
  "analysis_summary": {
    "trend_direction": {
      "type": "string", 
      "enum": ["bullish", "bearish", "neutral", "mixed"]
    },
    "signal_strength": {
      "type": "string", 
      "enum": ["strong", "moderate", "weak"]
    },
    "recommendations": {
      "type": "array",
      "items": {"type": "string", "enum": ["buy", "sell", "hold", "watch"]},
      "maxItems": 3
    }
  }
}
```

---

## Parser API

### JsonParser Class

**Location**: `json_parser.py`  
**Purpose**: Primary JSON parsing engine with schema validation

#### Constructor

```python
JsonParser(log_level: int = logging.INFO)
```

**Parameters**:
- `log_level`: Logging level for parser operations

**Example**:
```python
from json_parser import JsonParser
import logging

parser = JsonParser(log_level=logging.DEBUG)
```

#### Core Parsing Methods

##### parse_stock_snapshot()

```python
def parse_stock_snapshot(self, text: str, ticker: Optional[str] = None) -> JsonParseResult
```

**Purpose**: Parse stock snapshot data from AI JSON response

**Parameters**:
- `text`: Raw AI response text (should contain JSON)
- `ticker`: Stock ticker symbol for context

**Returns**: `JsonParseResult` with parsed snapshot data

**Example**:
```python
response_text = '{"metadata": {...}, "snapshot_data": {...}}'
result = parser.parse_stock_snapshot(response_text, "AAPL")

print(f"Confidence: {result.confidence.value}")
print(f"Current Price: ${result.parsed_data['snapshot_data']['current_price']}")
```

##### parse_support_resistance()

```python
def parse_support_resistance(self, text: str, ticker: Optional[str] = None) -> JsonParseResult
```

**Purpose**: Parse support and resistance levels from AI JSON response

**Parameters**:
- `text`: Raw AI response text
- `ticker`: Stock ticker symbol for context

**Returns**: `JsonParseResult` with parsed S&R data

**Example**:
```python
result = parser.parse_support_resistance(response_text, "TSLA")

support_levels = result.parsed_data['support_levels']
s1_price = support_levels['S1']['price']
s1_strength = support_levels['S1']['strength']
```

##### parse_technical_indicators()

```python
def parse_technical_indicators(self, text: str, ticker: Optional[str] = None) -> JsonParseResult
```

**Purpose**: Parse technical indicators from AI JSON response

**Parameters**:
- `text`: Raw AI response text
- `ticker`: Stock ticker symbol for context

**Returns**: `JsonParseResult` with parsed technical data

**Example**:
```python
result = parser.parse_technical_indicators(response_text, "MSFT")

rsi_value = result.parsed_data['oscillators']['RSI']['value']
ema_20 = result.parsed_data['moving_averages']['exponential']['EMA_20']
```

##### parse_any()

```python
def parse_any(self, text: str, data_type: JsonDataType, ticker: Optional[str] = None) -> JsonParseResult
```

**Purpose**: Generic parser that routes to appropriate method based on data type

**Parameters**:
- `text`: Raw AI response text
- `data_type`: Type of data to parse (`JsonDataType` enum)
- `ticker`: Stock ticker symbol for context

**Returns**: `JsonParseResult` with parsed data

**Example**:
```python
from json_parser import JsonDataType

result = parser.parse_any(response_text, JsonDataType.SNAPSHOT, "AAPL")
```

#### Utility Methods

##### get_parsing_statistics()

```python
def get_parsing_statistics(self) -> Dict[str, Any]
```

**Purpose**: Get statistics about parser capabilities

**Returns**: Dictionary with parser statistics

**Example**:
```python
stats = parser.get_parsing_statistics()
print(f"Supported schemas: {stats['supported_schemas']}")
print(f"Schema versions: {stats['schema_versions']}")
```

##### validate_json_response()

```python
def validate_json_response(self, json_data: Dict[str, Any], data_type: JsonDataType) -> Dict[str, Any]
```

**Purpose**: Validate JSON response against appropriate schema

**Parameters**:
- `json_data`: JSON data to validate
- `data_type`: Expected data type

**Returns**: Validation result dictionary

### JsonParseResult Class

**Location**: `json_parser.py` lines 56-214  
**Purpose**: Container for JSON parsing results with metadata

#### Properties

```python
@dataclass
class JsonParseResult:
    data_type: JsonDataType
    raw_response: str
    parsed_data: Dict[str, Any]
    confidence: ConfidenceLevel
    schema_validation: Dict[str, Any] = field(default_factory=dict)
    extraction_metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    parse_time_ms: Optional[float] = None
```

#### Methods

##### to_dict()

```python
def to_dict(self) -> Dict[str, Any]
```

**Purpose**: Convert parse result to dictionary for serialization

**Returns**: Dictionary representation of parse result

##### to_dataframe()

```python
def to_dataframe(self) -> pd.DataFrame
```

**Purpose**: Convert parsed data to DataFrame for display

**Returns**: Pandas DataFrame formatted for UI display

**Example**:
```python
result = parser.parse_stock_snapshot(response_text, "AAPL")
df = result.to_dataframe()
print(df.to_string())
```

### Confidence Levels

```python
class ConfidenceLevel(Enum):
    HIGH = "high"        # Valid JSON with all required fields
    MEDIUM = "medium"    # Valid JSON with most required fields
    LOW = "low"         # Partial JSON or fallback parsing success
    FAILED = "failed"   # No meaningful data extracted
```

### Convenience Functions

##### create_compatible_parser()

```python
def create_compatible_parser() -> JsonParser
```

**Purpose**: Create JsonParser instance with production logging configuration

**Returns**: Configured JsonParser instance

##### parse_stock_data()

```python
def parse_stock_data(text: str, data_type: str, ticker: Optional[str] = None) -> JsonParseResult
```

**Purpose**: Convenience function for parsing with string data types

**Parameters**:
- `text`: Raw response text
- `data_type`: String data type ('snapshot', 'support_resistance', 'technical')
- `ticker`: Optional ticker symbol

**Returns**: JsonParseResult with parsed data

---

## Schema Validation API

### SchemaRegistry Class

**Location**: `json_schemas.py` lines 815-883  
**Purpose**: Central registry for all JSON schemas with validation utilities

#### Constructor

```python
SchemaRegistry()
```

**Example**:
```python
from json_schemas import SchemaRegistry, AnalysisType

registry = SchemaRegistry()
```

#### Core Methods

##### get_schema()

```python
def get_schema(self, analysis_type: AnalysisType) -> Dict[str, Any]
```

**Purpose**: Get schema for specific analysis type

**Parameters**:
- `analysis_type`: Type of analysis (`AnalysisType` enum)

**Returns**: JSON schema dictionary

**Example**:
```python
snapshot_schema = registry.get_schema(AnalysisType.SNAPSHOT)
print(f"Schema title: {snapshot_schema['title']}")
```

##### validate_response()

```python
def validate_response(self, data: Dict[str, Any], analysis_type: AnalysisType) -> Dict[str, Any]
```

**Purpose**: Validate response data against appropriate schema

**Parameters**:
- `data`: Response data to validate
- `analysis_type`: Type of analysis for schema selection

**Returns**: Validation result with success/failure status and details

**Example**:
```python
validation_result = registry.validate_response(parsed_data, AnalysisType.SNAPSHOT)

if validation_result['valid']:
    print("Schema validation successful")
else:
    print(f"Validation error: {validation_result['error_message']}")
```

##### get_all_schemas()

```python
def get_all_schemas(self) -> Dict[str, Dict[str, Any]]
```

**Purpose**: Get all schemas as a dictionary

**Returns**: Dictionary mapping schema names to schema objects

#### Global Registry Instance

```python
from json_schemas import schema_registry

# Use global registry instance
result = schema_registry.validate_response(data, AnalysisType.TECHNICAL)
```

### Schema Utility Functions

##### generate_example_responses()

```python
def generate_example_responses() -> Dict[str, Dict[str, Any]]
```

**Purpose**: Generate example responses for each schema type

**Returns**: Dictionary with example data for all analysis types

**Example**:
```python
from json_schemas import generate_example_responses

examples = generate_example_responses()
snapshot_example = examples['snapshot']
print(f"Example price: ${snapshot_example['snapshot_data']['current_price']}")
```

##### export_schemas_for_ai_prompts()

```python
def export_schemas_for_ai_prompts() -> Dict[str, str]
```

**Purpose**: Export schemas optimized for AI prompt inclusion

**Returns**: Dictionary with schema strings formatted for prompts

**Example**:
```python
from json_schemas import export_schemas_for_ai_prompts

prompt_schemas = export_schemas_for_ai_prompts()
snapshot_schema_str = prompt_schemas['snapshot']
```

---

## FSM State Management API

### StateManager Class

**Location**: `stock_data_fsm/manager.py`  
**Purpose**: Orchestrate state transitions and maintain context

#### Constructor

```python
StateManager(initial_state: AppState = AppState.IDLE, debug_mode: bool = False)
```

**Parameters**:
- `initial_state`: Starting state for the FSM
- `debug_mode`: Enable detailed logging

#### Core Methods

##### transition_to()

```python
def transition_to(self, new_state: AppState, context_updates: Optional[Dict[str, Any]] = None) -> bool
```

**Purpose**: Attempt to transition to a new state

**Parameters**:
- `new_state`: Target state for transition
- `context_updates`: Optional context data updates

**Returns**: True if transition successful, False otherwise

**Example**:
```python
from stock_data_fsm import StateManager, AppState

manager = StateManager()
success = manager.transition_to(AppState.ANALYZING, {
    'current_ticker': 'AAPL',
    'analysis_type': 'snapshot'
})
```

##### get_current_state()

```python
def get_current_state(self) -> AppState
```

**Purpose**: Get current FSM state

**Returns**: Current state enum value

##### update_context()

```python
def update_context(self, updates: Dict[str, Any]) -> None
```

**Purpose**: Update state context data

**Parameters**:
- `updates`: Dictionary of context updates

##### reset()

```python
def reset(self) -> None
```

**Purpose**: Reset FSM to initial state and clear context

### AppState Enum

```python
class AppState(Enum):
    IDLE = "idle"
    ANALYZING = "analyzing"
    DISPLAYING_RESULTS = "displaying_results"
    ERROR = "error"
    LOADING = "loading"
```

### StateContext Class

```python
@dataclass
class StateContext:
    current_ticker: Optional[str] = None
    analysis_type: Optional[str] = None
    raw_response: Optional[str] = None
    parsed_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    debug_info: Dict[str, Any] = field(default_factory=dict)
```

---

## Prompt Template API

### PromptTemplateManager Class

**Location**: `prompt_templates.py`  
**Purpose**: Generate JSON schema-aware prompts for structured AI responses

#### Constructor

```python
PromptTemplateManager()
```

#### Core Methods

##### generate_prompt()

```python
def generate_prompt(self, prompt_type: PromptType, ticker: str, 
                   additional_context: Optional[str] = None) -> Tuple[str, Dict]
```

**Purpose**: Generate JSON schema-compliant prompt for specified analysis type

**Parameters**:
- `prompt_type`: Type of analysis prompt (`PromptType` enum)
- `ticker`: Stock ticker symbol
- `additional_context`: Optional additional context for the prompt

**Returns**: Tuple of (prompt_string, context_dict)

**Example**:
```python
from prompt_templates import PromptTemplateManager, PromptType

manager = PromptTemplateManager()
prompt, context = manager.generate_prompt(PromptType.SNAPSHOT, "AAPL")
```

##### get_enhanced_system_prompt()

```python
def get_enhanced_system_prompt(self, base_prompt: str) -> str
```

**Purpose**: Enhance system prompt with JSON requirements

**Parameters**:
- `base_prompt`: Base system prompt text

**Returns**: Enhanced prompt with JSON instructions

### PromptType Enum

```python
class PromptType(Enum):
    SNAPSHOT = "snapshot"
    SUPPORT_RESISTANCE = "support_resistance"
    TECHNICAL = "technical"
```

---

## Debug Logging API

### JsonDebugLogger Class

**Location**: `json_debug_logger.py`  
**Purpose**: Comprehensive logging for JSON workflow debugging

#### Core Methods

##### log_json_workflow_start()

```python
def log_json_workflow_start(self, workflow_id: str, request_type: str, ticker: str) -> None
```

**Purpose**: Log the start of a JSON processing workflow

**Parameters**:
- `workflow_id`: Unique identifier for the workflow
- `request_type`: Type of request being processed
- `ticker`: Stock ticker symbol

##### log_json_extraction_attempt()

```python
def log_json_extraction_attempt(self, workflow_id: str, extraction_method: str) -> None
```

**Purpose**: Log JSON extraction attempt

**Parameters**:
- `workflow_id`: Workflow identifier
- `extraction_method`: Method used for extraction

##### log_json_workflow_complete()

```python
def log_json_workflow_complete(self, workflow_id: str, success: bool, confidence: str) -> None
```

**Purpose**: Log completion of JSON workflow

**Parameters**:
- `workflow_id`: Workflow identifier
- `success`: Whether workflow completed successfully
- `confidence`: Confidence level of the result

#### Utility Functions

##### create_workflow_id()

```python
def create_workflow_id() -> str
```

**Purpose**: Generate unique workflow identifier

**Returns**: UUID string for workflow tracking

**Example**:
```python
from json_debug_logger import json_debug_logger, create_workflow_id

workflow_id = create_workflow_id()
json_debug_logger.log_json_workflow_start(workflow_id, "snapshot", "AAPL")
```

---

## Error Handling

### Error Response Schema

**Purpose**: Standardized error responses for validation and processing failures

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Response data failed schema validation",
    "details": {
      "field_errors": [
        {
          "field": "snapshot_data.current_price",
          "error_code": "INVALID_TYPE",
          "message": "Expected number, got string",
          "rejected_value": "invalid_price"
        }
      ],
      "schema_path": "/properties/snapshot_data/properties/current_price/type",
      "instance_path": "/snapshot_data/current_price"
    },
    "timestamp": "2025-08-17T10:30:00Z",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### Error Codes

- `VALIDATION_ERROR`: Schema validation failure
- `PARSING_ERROR`: JSON parsing failure
- `DATA_UNAVAILABLE`: Required data not available
- `RATE_LIMIT_EXCEEDED`: API rate limit reached
- `AUTHENTICATION_ERROR`: API authentication failure
- `INTERNAL_ERROR`: System internal error
- `TIMEOUT_ERROR`: Request timeout
- `INVALID_TICKER`: Invalid ticker symbol

### Exception Classes

##### JsonValidationError

```python
class JsonValidationError(Exception):
    """Custom exception for JSON validation failures"""
    pass
```

**Usage**:
```python
try:
    result = parser.parse_stock_snapshot(invalid_json, "AAPL")
except JsonValidationError as e:
    print(f"Validation failed: {e}")
```

---

## Usage Examples

### Basic Snapshot Analysis

```python
from json_parser import create_compatible_parser
from json_schemas import AnalysisType

# Initialize parser
parser = create_compatible_parser()

# AI response containing JSON
ai_response = '''
{
  "metadata": {
    "timestamp": "2025-08-17T10:30:00Z",
    "ticker_symbol": "AAPL",
    "confidence_score": 0.95,
    "schema_version": "1.0"
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
'''

# Parse the response
result = parser.parse_stock_snapshot(ai_response, "AAPL")

# Check results
print(f"Confidence: {result.confidence.value}")
print(f"Current Price: ${result.parsed_data['snapshot_data']['current_price']}")

# Convert to DataFrame for display
df = result.to_dataframe()
print(df.to_string())
```

### Support & Resistance Analysis

```python
# AI response with S&R data
sr_response = '''
{
  "metadata": {
    "timestamp": "2025-08-17T10:30:00Z",
    "ticker_symbol": "TSLA",
    "schema_version": "1.0"
  },
  "support_levels": {
    "S1": {"price": 145.50, "strength": "strong", "confidence": 0.9},
    "S2": {"price": 142.00, "strength": "moderate", "confidence": 0.8},
    "S3": {"price": 138.75, "strength": "weak", "confidence": 0.7}
  },
  "resistance_levels": {
    "R1": {"price": 155.25, "strength": "moderate", "confidence": 0.85},
    "R2": {"price": 158.50, "strength": "strong", "confidence": 0.9},
    "R3": {"price": 162.00, "strength": "weak", "confidence": 0.75}
  }
}
'''

# Parse support & resistance
result = parser.parse_support_resistance(sr_response, "TSLA")

# Access structured data
s1_level = result.parsed_data['support_levels']['S1']
print(f"S1 Support: ${s1_level['price']} ({s1_level['strength']})")

r1_level = result.parsed_data['resistance_levels']['R1']
print(f"R1 Resistance: ${r1_level['price']} ({r1_level['strength']})")
```

### Schema Validation

```python
from json_schemas import schema_registry, AnalysisType

# Validate parsed data against schema
data = result.parsed_data
validation_result = schema_registry.validate_response(data, AnalysisType.SNAPSHOT)

if validation_result['valid']:
    print("✅ Schema validation passed")
    print(f"Schema version: {validation_result['schema_version']}")
else:
    print("❌ Schema validation failed")
    print(f"Error: {validation_result['error_message']}")
```

### FSM State Management

```python
from stock_data_fsm import StateManager, AppState

# Initialize state manager
manager = StateManager(debug_mode=True)

# Start analysis workflow
success = manager.transition_to(AppState.ANALYZING, {
    'current_ticker': 'AAPL',
    'analysis_type': 'snapshot'
})

if success:
    print(f"State: {manager.get_current_state().value}")
    
    # Process analysis...
    
    # Complete workflow
    manager.transition_to(AppState.DISPLAYING_RESULTS, {
        'parsed_data': result.parsed_data
    })
```

### Prompt Generation

```python
from prompt_templates import PromptTemplateManager, PromptType

# Generate JSON schema-aware prompt
manager = PromptTemplateManager()
prompt, context = manager.generate_prompt(PromptType.TECHNICAL, "MSFT")

print("Generated prompt includes:")
print("- JSON schema definition")
print("- Validation requirements")
print("- Example response format")
print("- Error handling instructions")
```

### Debug Logging

```python
from json_debug_logger import json_debug_logger, create_workflow_id

# Start workflow tracking
workflow_id = create_workflow_id()
json_debug_logger.log_json_workflow_start(workflow_id, "snapshot", "AAPL")

# Log processing steps
json_debug_logger.log_json_extraction_attempt(workflow_id, "code_block_pattern")

# Complete workflow
json_debug_logger.log_json_workflow_complete(workflow_id, True, "high")
```

---

## Migration from Legacy API

### Response Parser Compatibility

The JSON parser maintains compatibility with the original `response_parser.py` API:

```python
# Legacy approach (still works)
from response_parser import ResponseParser, DataType

legacy_parser = ResponseParser()
legacy_result = legacy_parser.parse_stock_snapshot(text, ticker)

# New JSON approach (recommended)
from json_parser import create_compatible_parser

json_parser = create_compatible_parser()
json_result = json_parser.parse_stock_snapshot(text, ticker)
```

### Data Format Migration

```python
# Legacy data format
legacy_data = {
    'price': 150.25,
    'change_percent': 2.5,
    'volume': 45000000
}

# New structured format
json_data = {
    'metadata': {
        'timestamp': '2025-08-17T10:30:00Z',
        'ticker_symbol': 'AAPL',
        'confidence_score': 0.95
    },
    'snapshot_data': {
        'current_price': 150.25,
        'percentage_change': 2.5,
        'volume': 45000000
    }
}
```

### Gradual Migration Strategy

1. **Phase 1**: Use JSON parser with regex fallback (current)
2. **Phase 2**: Monitor JSON parsing success rates
3. **Phase 3**: Disable fallback for new features
4. **Phase 4**: Complete migration to JSON-only parsing

This API reference provides comprehensive guidance for integrating with the Market Parser JSON system, ensuring reliable financial data processing with robust error handling and validation.