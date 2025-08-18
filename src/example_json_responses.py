"""
Example JSON Responses for Market Parser API

This module provides comprehensive example JSON responses for all analysis types,
demonstrating the schema structure and validation capabilities.

These examples serve as:
- Reference implementations for AI prompt generation
- Test data for validation and parsing systems
- Documentation for API consumers
- Integration test fixtures
"""

import json
import datetime
from typing import Dict, Any
from .json_schemas import AnalysisType


def get_current_timestamp() -> str:
    """Get current timestamp in ISO 8601 format"""
    return datetime.datetime.utcnow().isoformat() + "Z"


# ====== SNAPSHOT ANALYSIS EXAMPLES ======

SNAPSHOT_EXAMPLE_AAPL = {
    "metadata": {
        "timestamp": "2025-01-15T10:30:00Z",
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
}

SNAPSHOT_EXAMPLE_TSLA = {
    "metadata": {
        "timestamp": "2025-01-15T15:45:00Z",
        "ticker_symbol": "TSLA",
        "company_name": "Tesla, Inc.",
        "data_source": "polygon",
        "confidence_score": 0.92,
        "schema_version": "1.0"
    },
    "snapshot_data": {
        "current_price": 245.80,
        "percentage_change": -3.2,
        "dollar_change": -8.15,
        "volume": 28500000,
        "vwap": 248.95,
        "open": 252.00,
        "high": 254.75,
        "low": 243.25,
        "close": 253.95
    },
    "validation": {
        "data_freshness": "delayed-15min",
        "market_status": "closed",
        "warnings": ["Volume below 30-day average"]
    }
}

SNAPSHOT_EXAMPLE_NVDA = {
    "metadata": {
        "timestamp": "2025-01-15T14:20:00Z",
        "ticker_symbol": "NVDA",
        "company_name": "NVIDIA Corporation",
        "data_source": "real-time",
        "confidence_score": 0.98,
        "schema_version": "1.0"
    },
    "snapshot_data": {
        "current_price": 875.40,
        "percentage_change": 5.8,
        "dollar_change": 47.95,
        "volume": 52000000,
        "vwap": 863.25,
        "open": 830.00,
        "high": 878.50,
        "low": 825.75,
        "close": 827.45
    },
    "validation": {
        "data_freshness": "real-time",
        "market_status": "open",
        "warnings": []
    }
}


# ====== SUPPORT & RESISTANCE EXAMPLES ======

SUPPORT_RESISTANCE_EXAMPLE_AAPL = {
    "metadata": {
        "timestamp": "2025-01-15T10:30:00Z",
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
}

SUPPORT_RESISTANCE_EXAMPLE_TSLA = {
    "metadata": {
        "timestamp": "2025-01-15T15:45:00Z",
        "ticker_symbol": "TSLA",
        "company_name": "Tesla, Inc.",
        "analysis_timeframe": "3M",
        "confidence_score": 0.78,
        "schema_version": "1.0"
    },
    "support_levels": {
        "S1": {"price": 235.00, "strength": "moderate", "confidence": 0.8},
        "S2": {"price": 225.50, "strength": "strong", "confidence": 0.85},
        "S3": {"price": 210.00, "strength": "moderate", "confidence": 0.75}
    },
    "resistance_levels": {
        "R1": {"price": 260.00, "strength": "strong", "confidence": 0.9},
        "R2": {"price": 275.75, "strength": "moderate", "confidence": 0.8},
        "R3": {"price": 295.00, "strength": "weak", "confidence": 0.7}
    },
    "analysis_context": {
        "current_price": 245.80,
        "methodology": "fibonacci",
        "warnings": ["High volatility may affect level reliability"]
    }
}

SUPPORT_RESISTANCE_EXAMPLE_NVDA = {
    "metadata": {
        "timestamp": "2025-01-15T14:20:00Z",
        "ticker_symbol": "NVDA",
        "company_name": "NVIDIA Corporation",
        "analysis_timeframe": "6M",
        "confidence_score": 0.88,
        "schema_version": "1.0"
    },
    "support_levels": {
        "S1": {"price": 825.00, "strength": "strong", "confidence": 0.92},
        "S2": {"price": 780.50, "strength": "moderate", "confidence": 0.85},
        "S3": {"price": 720.00, "strength": "strong", "confidence": 0.88}
    },
    "resistance_levels": {
        "R1": {"price": 900.00, "strength": "moderate", "confidence": 0.83},
        "R2": {"price": 950.75, "strength": "strong", "confidence": 0.9},
        "R3": {"price": 1000.00, "strength": "moderate", "confidence": 0.8}
    },
    "analysis_context": {
        "current_price": 875.40,
        "methodology": "price_action",
        "warnings": []
    }
}


# ====== TECHNICAL ANALYSIS EXAMPLES ======

TECHNICAL_EXAMPLE_AAPL = {
    "metadata": {
        "timestamp": "2025-01-15T10:30:00Z",
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
}

TECHNICAL_EXAMPLE_TSLA = {
    "metadata": {
        "timestamp": "2025-01-15T15:45:00Z",
        "ticker_symbol": "TSLA",
        "company_name": "Tesla, Inc.",
        "analysis_period": "3M",
        "confidence_score": 0.82,
        "schema_version": "1.0"
    },
    "oscillators": {
        "RSI": {"value": 35.2, "interpretation": "oversold", "period": 14},
        "MACD": {"value": -2.15, "signal": -1.85, "histogram": -0.30, "interpretation": "bearish"}
    },
    "moving_averages": {
        "exponential": {
            "EMA_5": 242.80,
            "EMA_10": 248.90,
            "EMA_20": 255.75,
            "EMA_50": 268.50,
            "EMA_200": 285.25
        },
        "simple": {
            "SMA_5": 244.15,
            "SMA_10": 250.25,
            "SMA_20": 258.40,
            "SMA_50": 271.80,
            "SMA_200": 289.75
        }
    },
    "analysis_summary": {
        "trend_direction": "bearish",
        "signal_strength": "strong",
        "recommendations": ["sell", "watch"],
        "warnings": ["High volatility environment"]
    }
}

TECHNICAL_EXAMPLE_NVDA = {
    "metadata": {
        "timestamp": "2025-01-15T14:20:00Z",
        "ticker_symbol": "NVDA",
        "company_name": "NVIDIA Corporation",
        "analysis_period": "6M",
        "confidence_score": 0.91,
        "schema_version": "1.0"
    },
    "oscillators": {
        "RSI": {"value": 78.9, "interpretation": "overbought", "period": 14},
        "MACD": {"value": 15.45, "signal": 12.80, "histogram": 2.65, "interpretation": "bullish"}
    },
    "moving_averages": {
        "exponential": {
            "EMA_5": 872.50,
            "EMA_10": 865.25,
            "EMA_20": 850.75,
            "EMA_50": 810.25,
            "EMA_200": 720.50
        },
        "simple": {
            "SMA_5": 871.80,
            "SMA_10": 863.90,
            "SMA_20": 848.25,
            "SMA_50": 806.75,
            "SMA_200": 715.25
        }
    },
    "analysis_summary": {
        "trend_direction": "bullish",
        "signal_strength": "strong",
        "recommendations": ["hold", "buy"],
        "warnings": ["RSI indicates potential short-term correction"]
    }
}


# ====== ERROR RESPONSE EXAMPLES ======

ERROR_VALIDATION_EXAMPLE = {
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Response data failed schema validation",
        "details": {
            "field_errors": [
                {
                    "field": "/snapshot_data/current_price",
                    "error_code": "INVALID_TYPE",
                    "message": "Expected number, got string",
                    "rejected_value": "invalid_price"
                },
                {
                    "field": "/snapshot_data/volume",
                    "error_code": "VALUE_TOO_SMALL",
                    "message": "Value must be minimum 0",
                    "rejected_value": -1000
                }
            ],
            "schema_version": "1.0",
            "analysis_type": "snapshot"
        },
        "timestamp": "2025-01-15T10:30:00Z",
        "request_id": "550e8400-e29b-41d4-a716-446655440000"
    }
}

ERROR_RATE_LIMIT_EXAMPLE = {
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "API rate limit exceeded",
        "details": {
            "limit": 100,
            "reset_time": "2025-01-15T10:31:00Z",
            "retry_after": 60
        },
        "timestamp": "2025-01-15T10:30:00Z",
        "request_id": "550e8400-e29b-41d4-a716-446655440001"
    }
}

ERROR_INVALID_TICKER_EXAMPLE = {
    "error": {
        "code": "INVALID_TICKER",
        "message": "Invalid or unknown ticker symbol",
        "details": {
            "rejected_ticker": "INVALID123",
            "suggestion": "Please verify ticker symbol format (1-5 uppercase letters)"
        },
        "timestamp": "2025-01-15T10:30:00Z",
        "request_id": "550e8400-e29b-41d4-a716-446655440002"
    }
}

ERROR_DATA_UNAVAILABLE_EXAMPLE = {
    "error": {
        "code": "DATA_UNAVAILABLE",
        "message": "Market data temporarily unavailable",
        "details": {
            "ticker": "AAPL",
            "data_source": "polygon",
            "estimated_availability": "2025-01-15T10:35:00Z"
        },
        "timestamp": "2025-01-15T10:30:00Z",
        "request_id": "550e8400-e29b-41d4-a716-446655440003"
    }
}


# ====== EXAMPLE COLLECTIONS ======

SNAPSHOT_EXAMPLES = {
    "AAPL": SNAPSHOT_EXAMPLE_AAPL,
    "TSLA": SNAPSHOT_EXAMPLE_TSLA,
    "NVDA": SNAPSHOT_EXAMPLE_NVDA
}

SUPPORT_RESISTANCE_EXAMPLES = {
    "AAPL": SUPPORT_RESISTANCE_EXAMPLE_AAPL,
    "TSLA": SUPPORT_RESISTANCE_EXAMPLE_TSLA,
    "NVDA": SUPPORT_RESISTANCE_EXAMPLE_NVDA
}

TECHNICAL_EXAMPLES = {
    "AAPL": TECHNICAL_EXAMPLE_AAPL,
    "TSLA": TECHNICAL_EXAMPLE_TSLA,
    "NVDA": TECHNICAL_EXAMPLE_NVDA
}

ERROR_EXAMPLES = {
    "validation": ERROR_VALIDATION_EXAMPLE,
    "rate_limit": ERROR_RATE_LIMIT_EXAMPLE,
    "invalid_ticker": ERROR_INVALID_TICKER_EXAMPLE,
    "data_unavailable": ERROR_DATA_UNAVAILABLE_EXAMPLE
}

ALL_EXAMPLES = {
    "snapshot": SNAPSHOT_EXAMPLES,
    "support_resistance": SUPPORT_RESISTANCE_EXAMPLES,
    "technical": TECHNICAL_EXAMPLES,
    "errors": ERROR_EXAMPLES
}


def get_examples_by_type(analysis_type: AnalysisType) -> Dict[str, Dict[str, Any]]:
    """Get all examples for a specific analysis type"""
    if analysis_type == AnalysisType.SNAPSHOT:
        return SNAPSHOT_EXAMPLES
    elif analysis_type == AnalysisType.SUPPORT_RESISTANCE:
        return SUPPORT_RESISTANCE_EXAMPLES
    elif analysis_type == AnalysisType.TECHNICAL:
        return TECHNICAL_EXAMPLES
    else:
        return {}


def get_example_for_ticker(analysis_type: AnalysisType, ticker: str) -> Dict[str, Any]:
    """Get example response for specific analysis type and ticker"""
    examples = get_examples_by_type(analysis_type)
    return examples.get(ticker.upper(), {})


def get_random_example(analysis_type: AnalysisType) -> Dict[str, Any]:
    """Get a random example for the specified analysis type"""
    import random
    examples = get_examples_by_type(analysis_type)
    if examples:
        return random.choice(list(examples.values()))
    return {}


def update_example_timestamps():
    """Update all example timestamps to current time"""
    current_time = get_current_timestamp()
    
    for example_group in [SNAPSHOT_EXAMPLES, SUPPORT_RESISTANCE_EXAMPLES, TECHNICAL_EXAMPLES]:
        for example in example_group.values():
            if "metadata" in example:
                example["metadata"]["timestamp"] = current_time
    
    for error_example in ERROR_EXAMPLES.values():
        if "error" in error_example:
            error_example["error"]["timestamp"] = current_time


def export_examples_as_json() -> Dict[str, str]:
    """Export all examples as formatted JSON strings"""
    formatted_examples = {}
    
    for category, examples in ALL_EXAMPLES.items():
        if category == "errors":
            for error_type, error_example in examples.items():
                formatted_examples[f"{category}_{error_type}"] = json.dumps(error_example, indent=2)
        else:
            for ticker, example in examples.items():
                formatted_examples[f"{category}_{ticker}"] = json.dumps(example, indent=2)
    
    return formatted_examples


def validate_all_examples():
    """Validate all examples against their respective schemas"""
    from schema_validator import validate_json_response
    
    results = {}
    
    # Validate analysis examples
    for analysis_type in AnalysisType:
        examples = get_examples_by_type(analysis_type)
        type_results = {}
        
        for ticker, example in examples.items():
            validation_report = validate_json_response(example, analysis_type)
            type_results[ticker] = {
                "valid": validation_report.is_valid,
                "errors": len(validation_report.field_errors),
                "warnings": len(validation_report.warnings),
                "validation_time_ms": validation_report.validation_time_ms
            }
        
        results[analysis_type.value] = type_results
    
    return results


def generate_prompt_examples() -> Dict[str, str]:
    """Generate examples formatted for inclusion in AI prompts"""
    prompt_examples = {}
    
    # Format examples for each analysis type
    for analysis_type in AnalysisType:
        examples = get_examples_by_type(analysis_type)
        if examples:
            # Use the first example (AAPL) as the canonical prompt example
            first_ticker = list(examples.keys())[0]
            example = examples[first_ticker]
            
            # Format for prompt inclusion
            prompt_example = json.dumps(example, indent=2)
            prompt_examples[analysis_type.value] = prompt_example
    
    return prompt_examples


if __name__ == "__main__":
    # Test and display example information
    print("📊 Market Parser JSON Response Examples")
    print("=" * 60)
    
    # Show example counts
    total_examples = 0
    for category, examples in ALL_EXAMPLES.items():
        count = len(examples)
        total_examples += count
        print(f"   • {category}: {count} examples")
    
    print(f"\n📈 Total examples: {total_examples}")
    
    # Validate all examples
    print(f"\n🔍 Validating examples...")
    validation_results = validate_all_examples()
    
    for analysis_type, type_results in validation_results.items():
        valid_count = sum(1 for r in type_results.values() if r["valid"])
        total_count = len(type_results)
        print(f"   • {analysis_type}: {valid_count}/{total_count} valid")
    
    # Show response sizes
    print(f"\n📏 Response sizes:")
    for analysis_type in AnalysisType:
        examples = get_examples_by_type(analysis_type)
        if examples:
            first_example = list(examples.values())[0]
            size = len(json.dumps(first_example))
            print(f"   • {analysis_type.value}: ~{size} bytes")
    
    print(f"\n✅ All examples ready for production use!")