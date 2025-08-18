"""
JSON Schema Definitions for Market Parser API Re-architecture

This module provides comprehensive JSON schemas for structured financial data responses,
replacing the text-based parsing approach with robust JSON schema validation.

Features:
- JSON Schema Draft 2020-12 compliant definitions
- Comprehensive validation rules for financial data
- Standardized metadata and error handling
- Schema versioning for evolution support
- Optimized for AI model structured output generation
"""

import json
from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass
import datetime


class SchemaVersion(Enum):
    """Schema version identifiers for evolution tracking"""
    V1_0 = "1.0"
    CURRENT = V1_0


class AnalysisType(Enum):
    """Types of stock analysis with JSON schema support"""
    SNAPSHOT = "snapshot"
    SUPPORT_RESISTANCE = "support_resistance"
    TECHNICAL = "technical"


@dataclass
class SchemaMetadata:
    """Metadata container for schema information"""
    version: str
    created_at: str
    analysis_type: AnalysisType
    description: str
    required_fields: List[str]
    optional_fields: List[str] = None


# ====== SNAPSHOT ANALYSIS SCHEMA ======

SNAPSHOT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://market-parser.com/schemas/snapshot/v1.0",
    "title": "Stock Snapshot Analysis",
    "description": "Comprehensive stock snapshot data with current market metrics",
    "type": "object",
    "version": SchemaVersion.V1_0.value,
    "properties": {
        "metadata": {
            "type": "object",
            "description": "Response metadata and traceability information",
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
                    "maxLength": 200,
                    "description": "Company name or identifier"
                },
                "data_source": {
                    "type": "string",
                    "enum": ["polygon", "real-time", "delayed"],
                    "description": "Source of the market data"
                },
                "confidence_score": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "description": "Confidence level in data accuracy (0.0-1.0)"
                },
                "schema_version": {
                    "type": "string",
                    "const": "1.0",
                    "description": "Schema version for compatibility tracking"
                }
            },
            "required": ["timestamp", "ticker_symbol", "schema_version"],
            "additionalProperties": False
        },
        "snapshot_data": {
            "type": "object",
            "description": "Core snapshot financial metrics",
            "properties": {
                "current_price": {
                    "type": "number",
                    "minimum": 0.01,
                    "maximum": 1000000,
                    "multipleOf": 0.01,
                    "description": "Current stock price in USD"
                },
                "percentage_change": {
                    "type": "number",
                    "minimum": -99.99,
                    "maximum": 999.99,
                    "description": "Percentage change for the trading session"
                },
                "dollar_change": {
                    "type": "number",
                    "minimum": -10000,
                    "maximum": 10000,
                    "description": "Dollar change for the trading session"
                },
                "volume": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 999999999999,
                    "description": "Trading volume (number of shares)"
                },
                "vwap": {
                    "type": "number",
                    "minimum": 0.01,
                    "maximum": 1000000,
                    "multipleOf": 0.01,
                    "description": "Volume Weighted Average Price"
                },
                "open": {
                    "type": "number",
                    "minimum": 0.01,
                    "maximum": 1000000,
                    "multipleOf": 0.01,
                    "description": "Opening price for the trading session"
                },
                "high": {
                    "type": "number",
                    "minimum": 0.01,
                    "maximum": 1000000,
                    "multipleOf": 0.01,
                    "description": "Highest price for the trading session"
                },
                "low": {
                    "type": "number",
                    "minimum": 0.01,
                    "maximum": 1000000,
                    "multipleOf": 0.01,
                    "description": "Lowest price for the trading session"
                },
                "close": {
                    "type": "number",
                    "minimum": 0.01,
                    "maximum": 1000000,
                    "multipleOf": 0.01,
                    "description": "Previous closing price"
                }
            },
            "required": [
                "current_price", "percentage_change", "dollar_change",
                "volume", "vwap", "open", "high", "low", "close"
            ],
            "additionalProperties": False
        },
        "validation": {
            "type": "object",
            "description": "Data validation and quality indicators",
            "properties": {
                "data_freshness": {
                    "type": "string",
                    "enum": ["real-time", "delayed-15min", "delayed-20min", "end-of-day"],
                    "description": "Indicates how current the data is"
                },
                "market_status": {
                    "type": "string",
                    "enum": ["open", "closed", "pre-market", "after-hours"],
                    "description": "Current market trading status"
                },
                "warnings": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "maxLength": 200
                    },
                    "description": "Any warnings about data quality or completeness"
                }
            },
            "additionalProperties": False
        }
    },
    "required": ["metadata", "snapshot_data"],
    "additionalProperties": False
}


# ====== SUPPORT & RESISTANCE ANALYSIS SCHEMA ======

SUPPORT_RESISTANCE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://market-parser.com/schemas/support-resistance/v1.0",
    "title": "Support and Resistance Analysis",
    "description": "Technical analysis of support and resistance price levels",
    "type": "object",
    "version": SchemaVersion.V1_0.value,
    "properties": {
        "metadata": {
            "type": "object",
            "description": "Response metadata and traceability information",
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
                    "maxLength": 200,
                    "description": "Company name or identifier"
                },
                "analysis_timeframe": {
                    "type": "string",
                    "enum": ["1D", "5D", "1M", "3M", "6M", "1Y"],
                    "description": "Timeframe used for S&R analysis"
                },
                "confidence_score": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "description": "Overall confidence in S&R level accuracy"
                },
                "schema_version": {
                    "type": "string",
                    "const": "1.0",
                    "description": "Schema version for compatibility tracking"
                }
            },
            "required": ["timestamp", "ticker_symbol", "schema_version"],
            "additionalProperties": False
        },
        "support_levels": {
            "type": "object",
            "description": "Support price levels with strength indicators",
            "properties": {
                "S1": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "multipleOf": 0.01,
                            "description": "First support level price"
                        },
                        "strength": {
                            "type": "string",
                            "enum": ["strong", "moderate", "weak"],
                            "description": "Strength of this support level"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "description": "Confidence in this specific level"
                        }
                    },
                    "required": ["price", "strength"],
                    "additionalProperties": False
                },
                "S2": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "multipleOf": 0.01,
                            "description": "Second support level price"
                        },
                        "strength": {
                            "type": "string",
                            "enum": ["strong", "moderate", "weak"],
                            "description": "Strength of this support level"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "description": "Confidence in this specific level"
                        }
                    },
                    "required": ["price", "strength"],
                    "additionalProperties": False
                },
                "S3": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "multipleOf": 0.01,
                            "description": "Third support level price"
                        },
                        "strength": {
                            "type": "string",
                            "enum": ["strong", "moderate", "weak"],
                            "description": "Strength of this support level"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "description": "Confidence in this specific level"
                        }
                    },
                    "required": ["price", "strength"],
                    "additionalProperties": False
                }
            },
            "required": ["S1", "S2", "S3"],
            "additionalProperties": False
        },
        "resistance_levels": {
            "type": "object",
            "description": "Resistance price levels with strength indicators",
            "properties": {
                "R1": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "multipleOf": 0.01,
                            "description": "First resistance level price"
                        },
                        "strength": {
                            "type": "string",
                            "enum": ["strong", "moderate", "weak"],
                            "description": "Strength of this resistance level"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "description": "Confidence in this specific level"
                        }
                    },
                    "required": ["price", "strength"],
                    "additionalProperties": False
                },
                "R2": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "multipleOf": 0.01,
                            "description": "Second resistance level price"
                        },
                        "strength": {
                            "type": "string",
                            "enum": ["strong", "moderate", "weak"],
                            "description": "Strength of this resistance level"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "description": "Confidence in this specific level"
                        }
                    },
                    "required": ["price", "strength"],
                    "additionalProperties": False
                },
                "R3": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "multipleOf": 0.01,
                            "description": "Third resistance level price"
                        },
                        "strength": {
                            "type": "string",
                            "enum": ["strong", "moderate", "weak"],
                            "description": "Strength of this resistance level"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "description": "Confidence in this specific level"
                        }
                    },
                    "required": ["price", "strength"],
                    "additionalProperties": False
                }
            },
            "required": ["R1", "R2", "R3"],
            "additionalProperties": False
        },
        "analysis_context": {
            "type": "object",
            "description": "Context information for the S&R analysis",
            "properties": {
                "current_price": {
                    "type": "number",
                    "minimum": 0.01,
                    "maximum": 1000000,
                    "multipleOf": 0.01,
                    "description": "Current stock price for reference"
                },
                "methodology": {
                    "type": "string",
                    "enum": ["pivot_points", "fibonacci", "moving_averages", "price_action", "combined"],
                    "description": "Primary methodology used for S&R calculation"
                },
                "warnings": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "maxLength": 200
                    },
                    "description": "Any warnings about level reliability or market conditions"
                }
            },
            "additionalProperties": False
        }
    },
    "required": ["metadata", "support_levels", "resistance_levels"],
    "additionalProperties": False
}


# ====== TECHNICAL ANALYSIS SCHEMA ======

TECHNICAL_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://market-parser.com/schemas/technical/v1.0",
    "title": "Technical Indicators Analysis",
    "description": "Comprehensive technical analysis with oscillators and moving averages",
    "type": "object",
    "version": SchemaVersion.V1_0.value,
    "properties": {
        "metadata": {
            "type": "object",
            "description": "Response metadata and traceability information",
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
                    "maxLength": 200,
                    "description": "Company name or identifier"
                },
                "analysis_period": {
                    "type": "string",
                    "enum": ["1D", "5D", "1M", "3M", "6M", "1Y"],
                    "description": "Time period used for technical calculations"
                },
                "confidence_score": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "description": "Overall confidence in technical indicator accuracy"
                },
                "schema_version": {
                    "type": "string",
                    "const": "1.0",
                    "description": "Schema version for compatibility tracking"
                }
            },
            "required": ["timestamp", "ticker_symbol", "schema_version"],
            "additionalProperties": False
        },
        "oscillators": {
            "type": "object",
            "description": "Momentum and oscillator indicators",
            "properties": {
                "RSI": {
                    "type": "object",
                    "properties": {
                        "value": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "RSI value (0-100 range)"
                        },
                        "interpretation": {
                            "type": "string",
                            "enum": ["oversold", "neutral", "overbought"],
                            "description": "RSI signal interpretation"
                        },
                        "period": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 200,
                            "default": 14,
                            "description": "Period used for RSI calculation"
                        }
                    },
                    "required": ["value", "interpretation"],
                    "additionalProperties": False
                },
                "MACD": {
                    "type": "object",
                    "properties": {
                        "value": {
                            "type": "number",
                            "minimum": -1000,
                            "maximum": 1000,
                            "description": "MACD line value (can be positive or negative)"
                        },
                        "signal": {
                            "type": "number",
                            "minimum": -1000,
                            "maximum": 1000,
                            "description": "MACD signal line value"
                        },
                        "histogram": {
                            "type": "number",
                            "minimum": -1000,
                            "maximum": 1000,
                            "description": "MACD histogram value"
                        },
                        "interpretation": {
                            "type": "string",
                            "enum": ["bullish", "bearish", "neutral"],
                            "description": "MACD signal interpretation"
                        }
                    },
                    "required": ["value", "interpretation"],
                    "additionalProperties": False
                }
            },
            "required": ["RSI", "MACD"],
            "additionalProperties": False
        },
        "moving_averages": {
            "type": "object",
            "description": "Exponential and Simple Moving Averages",
            "properties": {
                "exponential": {
                    "type": "object",
                    "description": "Exponential Moving Averages",
                    "properties": {
                        "EMA_5": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "5-period Exponential Moving Average"
                        },
                        "EMA_10": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "10-period Exponential Moving Average"
                        },
                        "EMA_20": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "20-period Exponential Moving Average"
                        },
                        "EMA_50": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "50-period Exponential Moving Average"
                        },
                        "EMA_200": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "200-period Exponential Moving Average"
                        }
                    },
                    "required": ["EMA_5", "EMA_10", "EMA_20", "EMA_50", "EMA_200"],
                    "additionalProperties": False
                },
                "simple": {
                    "type": "object",
                    "description": "Simple Moving Averages",
                    "properties": {
                        "SMA_5": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "5-period Simple Moving Average"
                        },
                        "SMA_10": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "10-period Simple Moving Average"
                        },
                        "SMA_20": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "20-period Simple Moving Average"
                        },
                        "SMA_50": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "50-period Simple Moving Average"
                        },
                        "SMA_200": {
                            "type": "number",
                            "minimum": 0.01,
                            "maximum": 1000000,
                            "description": "200-period Simple Moving Average"
                        }
                    },
                    "required": ["SMA_5", "SMA_10", "SMA_20", "SMA_50", "SMA_200"],
                    "additionalProperties": False
                }
            },
            "required": ["exponential", "simple"],
            "additionalProperties": False
        },
        "analysis_summary": {
            "type": "object",
            "description": "Overall technical analysis summary",
            "properties": {
                "trend_direction": {
                    "type": "string",
                    "enum": ["bullish", "bearish", "neutral", "mixed"],
                    "description": "Overall trend direction based on indicators"
                },
                "signal_strength": {
                    "type": "string",
                    "enum": ["strong", "moderate", "weak"],
                    "description": "Strength of the technical signals"
                },
                "recommendations": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["buy", "sell", "hold", "watch"],
                        "description": "Trading recommendations based on technical analysis"
                    },
                    "maxItems": 3,
                    "description": "Primary trading recommendations"
                },
                "warnings": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "maxLength": 200
                    },
                    "description": "Any warnings about indicator reliability or market conditions"
                }
            },
            "additionalProperties": False
        }
    },
    "required": ["metadata", "oscillators", "moving_averages"],
    "additionalProperties": False
}


# ====== ERROR RESPONSE SCHEMA ======

ERROR_RESPONSE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://market-parser.com/schemas/error/v1.0",
    "title": "API Error Response",
    "description": "Standardized error response format for validation failures and processing errors",
    "type": "object",
    "properties": {
        "error": {
            "type": "object",
            "description": "Error information container",
            "properties": {
                "code": {
                    "type": "string",
                    "enum": [
                        "VALIDATION_ERROR",
                        "PARSING_ERROR",
                        "DATA_UNAVAILABLE",
                        "RATE_LIMIT_EXCEEDED",
                        "AUTHENTICATION_ERROR",
                        "INTERNAL_ERROR",
                        "TIMEOUT_ERROR",
                        "INVALID_TICKER"
                    ],
                    "description": "Standardized error code for programmatic handling"
                },
                "message": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 500,
                    "description": "Human-readable error message"
                },
                "details": {
                    "type": "object",
                    "description": "Additional error details and context",
                    "properties": {
                        "field_errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {
                                        "type": "string",
                                        "description": "Field name that failed validation"
                                    },
                                    "error_code": {
                                        "type": "string",
                                        "description": "Specific validation error code"
                                    },
                                    "message": {
                                        "type": "string",
                                        "description": "Field-specific error message"
                                    },
                                    "rejected_value": {
                                        "description": "The value that was rejected (any type)"
                                    }
                                },
                                "required": ["field", "error_code", "message"],
                                "additionalProperties": False
                            },
                            "description": "Array of field-level validation errors"
                        },
                        "schema_path": {
                            "type": "string",
                            "description": "JSON path to the schema element that failed"
                        },
                        "instance_path": {
                            "type": "string",
                            "description": "JSON path to the data element that failed"
                        }
                    },
                    "additionalProperties": False
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time",
                    "description": "ISO 8601 timestamp when error occurred"
                },
                "request_id": {
                    "type": "string",
                    "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
                    "description": "Unique request identifier for tracing"
                }
            },
            "required": ["code", "message", "timestamp"],
            "additionalProperties": False
        }
    },
    "required": ["error"],
    "additionalProperties": False
}


# ====== SCHEMA REGISTRY AND UTILITIES ======

class SchemaRegistry:
    """Central registry for all JSON schemas with validation utilities"""
    
    def __init__(self):
        self.schemas = {
            AnalysisType.SNAPSHOT: SNAPSHOT_SCHEMA,
            AnalysisType.SUPPORT_RESISTANCE: SUPPORT_RESISTANCE_SCHEMA,
            AnalysisType.TECHNICAL: TECHNICAL_SCHEMA
        }
        self.error_schema = ERROR_RESPONSE_SCHEMA
        
    def get_schema(self, analysis_type: AnalysisType) -> Dict[str, Any]:
        """Get schema for specific analysis type"""
        return self.schemas[analysis_type]
    
    def get_error_schema(self) -> Dict[str, Any]:
        """Get standardized error response schema"""
        return self.error_schema
    
    def get_all_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Get all schemas as a dictionary"""
        return {
            "snapshot": self.schemas[AnalysisType.SNAPSHOT],
            "support_resistance": self.schemas[AnalysisType.SUPPORT_RESISTANCE],
            "technical": self.schemas[AnalysisType.TECHNICAL],
            "error": self.error_schema
        }
    
    def validate_response(self, data: Dict[str, Any], analysis_type: AnalysisType) -> Dict[str, Any]:
        """
        Validate response data against appropriate schema
        
        Args:
            data: Response data to validate
            analysis_type: Type of analysis for schema selection
            
        Returns:
            Validation result with success/failure status and details
        """
        try:
            import jsonschema
            
            schema = self.get_schema(analysis_type)
            jsonschema.validate(instance=data, schema=schema)
            
            return {
                "valid": True,
                "schema_version": schema.get("version", "unknown"),
                "validation_timestamp": datetime.datetime.utcnow().isoformat() + "Z"
            }
            
        except jsonschema.ValidationError as e:
            return {
                "valid": False,
                "error_code": "VALIDATION_ERROR",
                "error_message": e.message,
                "schema_path": e.schema_path,
                "instance_path": e.instance_path,
                "failed_value": e.instance,
                "validation_timestamp": datetime.datetime.utcnow().isoformat() + "Z"
            }
        except Exception as e:
            return {
                "valid": False,
                "error_code": "INTERNAL_ERROR",
                "error_message": f"Schema validation failed: {str(e)}",
                "validation_timestamp": datetime.datetime.utcnow().isoformat() + "Z"
            }


def generate_example_responses() -> Dict[str, Dict[str, Any]]:
    """Generate example responses for each schema type"""
    
    base_timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    
    examples = {
        "snapshot": {
            "metadata": {
                "timestamp": base_timestamp,
                "ticker_symbol": "AAPL",
                "company_name": "Apple Inc.",
                "data_source": "polygon",
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
            },
            "validation": {
                "data_freshness": "real-time",
                "market_status": "open",
                "warnings": []
            }
        },
        
        "support_resistance": {
            "metadata": {
                "timestamp": base_timestamp,
                "ticker_symbol": "AAPL",
                "company_name": "Apple Inc.",
                "analysis_timeframe": "1M",
                "confidence_score": 0.85,
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
            },
            "analysis_context": {
                "current_price": 150.25,
                "methodology": "combined",
                "warnings": []
            }
        },
        
        "technical": {
            "metadata": {
                "timestamp": base_timestamp,
                "ticker_symbol": "AAPL",
                "company_name": "Apple Inc.",
                "analysis_period": "1M",
                "confidence_score": 0.88,
                "schema_version": "1.0"
            },
            "oscillators": {
                "RSI": {"value": 68.5, "interpretation": "neutral", "period": 14},
                "MACD": {"value": 0.25, "signal": 0.18, "histogram": 0.07, "interpretation": "bullish"}
            },
            "moving_averages": {
                "exponential": {
                    "EMA_5": 151.20,
                    "EMA_10": 149.85,
                    "EMA_20": 147.50,
                    "EMA_50": 144.75,
                    "EMA_200": 140.25
                },
                "simple": {
                    "SMA_5": 150.95,
                    "SMA_10": 148.75,
                    "SMA_20": 146.80,
                    "SMA_50": 143.90,
                    "SMA_200": 139.50
                }
            },
            "analysis_summary": {
                "trend_direction": "bullish",
                "signal_strength": "moderate",
                "recommendations": ["hold", "watch"],
                "warnings": []
            }
        },
        
        "error": {
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
                "timestamp": base_timestamp,
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    }
    
    return examples


def export_schemas_for_ai_prompts() -> Dict[str, str]:
    """
    Export schemas in a format optimized for AI prompt inclusion
    
    Returns:
        Dictionary with schema strings formatted for prompt inclusion
    """
    registry = SchemaRegistry()
    
    formatted_schemas = {}
    
    for analysis_type in AnalysisType:
        schema = registry.get_schema(analysis_type)
        
        # Extract just the structure for AI prompts (remove schema metadata)
        prompt_schema = {
            "type": schema["type"],
            "properties": schema["properties"],
            "required": schema["required"]
        }
        
        formatted_schemas[analysis_type.value] = json.dumps(prompt_schema, indent=2)
    
    # Add error schema
    error_schema = registry.get_error_schema()
    prompt_error_schema = {
        "type": error_schema["type"],
        "properties": error_schema["properties"],
        "required": error_schema["required"]
    }
    formatted_schemas["error"] = json.dumps(prompt_error_schema, indent=2)
    
    return formatted_schemas


# Initialize global registry
schema_registry = SchemaRegistry()

if __name__ == "__main__":
    # Generate and print example responses
    examples = generate_example_responses()
    
    print("🏗️ Market Parser JSON Schema System")
    print("=" * 60)
    
    print(f"\n📋 Schema Registry Initialized:")
    print(f"   • Snapshot Schema: {SNAPSHOT_SCHEMA['title']}")
    print(f"   • Support/Resistance Schema: {SUPPORT_RESISTANCE_SCHEMA['title']}")
    print(f"   • Technical Schema: {TECHNICAL_SCHEMA['title']}")
    print(f"   • Error Schema: {ERROR_RESPONSE_SCHEMA['title']}")
    
    print(f"\n✅ Example Validation:")
    for analysis_type in AnalysisType:
        example_data = examples[analysis_type.value]
        result = schema_registry.validate_response(example_data, analysis_type)
        status = "✅ VALID" if result["valid"] else "❌ INVALID"
        print(f"   • {analysis_type.value}: {status}")
    
    print(f"\n📄 Example Response Sizes:")
    for schema_type, example in examples.items():
        json_str = json.dumps(example, indent=2)
        print(f"   • {schema_type}: {len(json_str)} characters")
    
    print(f"\n🎯 Ready for production implementation!")