"""
JSON Schema Validation Utilities for Market Parser

This module provides comprehensive validation utilities for the Market Parser JSON schemas,
including validation, error formatting, and integration helpers for the FSM-driven architecture.

Features:
- Real-time schema validation with detailed error reporting
- Integration with existing ResponseParser patterns
- FSM-compatible validation results
- Performance-optimized validation caching
- Comprehensive error message formatting
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import datetime
import uuid

try:
    import jsonschema
    from jsonschema import Draft202012Validator, exceptions
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    logging.warning("jsonschema not available - validation will be disabled")

from .json_schemas import (
    SchemaRegistry, AnalysisType, SchemaVersion,
    SNAPSHOT_SCHEMA, SUPPORT_RESISTANCE_SCHEMA, TECHNICAL_SCHEMA, ERROR_RESPONSE_SCHEMA
)


class ValidationResult(Enum):
    """Validation result types"""
    VALID = "valid"
    INVALID = "invalid"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class FieldError:
    """Individual field validation error"""
    field_path: str
    error_code: str
    error_message: str
    rejected_value: Any = None
    expected_type: Optional[str] = None
    constraint: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {
            "field": self.field_path,
            "error_code": self.error_code,
            "message": self.error_message
        }
        if self.rejected_value is not None:
            result["rejected_value"] = self.rejected_value
        if self.expected_type:
            result["expected_type"] = self.expected_type
        if self.constraint:
            result["constraint"] = self.constraint
        return result


@dataclass
class ValidationReport:
    """Comprehensive validation report"""
    result: ValidationResult
    analysis_type: AnalysisType
    schema_version: str
    is_valid: bool
    field_errors: List[FieldError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    validation_time_ms: Optional[float] = None
    request_id: Optional[str] = None
    timestamp: Optional[str] = None
    confidence_impact: Optional[float] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "result": self.result.value,
            "analysis_type": self.analysis_type.value,
            "schema_version": self.schema_version,
            "is_valid": self.is_valid,
            "field_errors": [error.to_dict() for error in self.field_errors],
            "warnings": self.warnings,
            "validation_time_ms": self.validation_time_ms,
            "request_id": self.request_id,
            "timestamp": self.timestamp,
            "confidence_impact": self.confidence_impact
        }
    
    def to_error_response(self) -> Dict[str, Any]:
        """Convert to standardized error response format"""
        if self.is_valid:
            return None
        
        return {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": f"Schema validation failed for {self.analysis_type.value} analysis",
                "details": {
                    "field_errors": [error.to_dict() for error in self.field_errors],
                    "schema_version": self.schema_version,
                    "analysis_type": self.analysis_type.value
                },
                "timestamp": self.timestamp,
                "request_id": self.request_id
            }
        }
    
    def get_error_summary(self) -> str:
        """Get human-readable error summary"""
        if self.is_valid:
            return "Validation successful"
        
        error_count = len(self.field_errors)
        warning_count = len(self.warnings)
        
        parts = []
        if error_count > 0:
            parts.append(f"{error_count} validation error{'s' if error_count != 1 else ''}")
        if warning_count > 0:
            parts.append(f"{warning_count} warning{'s' if warning_count != 1 else ''}")
        
        return f"Validation failed: {', '.join(parts)}"


class SchemaValidator:
    """
    High-performance JSON schema validator with caching and detailed error reporting
    """
    
    def __init__(self, enable_caching: bool = True, cache_ttl_seconds: int = 300):
        """
        Initialize the schema validator
        
        Args:
            enable_caching: Whether to enable schema compilation caching
            cache_ttl_seconds: TTL for cached validators
        """
        self.logger = logging.getLogger(__name__)
        self.schema_registry = SchemaRegistry()
        self.enable_caching = enable_caching
        self.cache_ttl_seconds = cache_ttl_seconds
        
        # Validator cache with TTL
        self._validator_cache: Dict[str, Tuple[Draft202012Validator, float]] = {}
        
        # Error code mappings for better error messages
        self._error_code_mapping = {
            "type": "INVALID_TYPE",
            "required": "MISSING_REQUIRED_FIELD",
            "minimum": "VALUE_TOO_SMALL",
            "maximum": "VALUE_TOO_LARGE",
            "pattern": "INVALID_FORMAT",
            "enum": "INVALID_ENUM_VALUE",
            "additionalProperties": "UNEXPECTED_FIELD",
            "minLength": "STRING_TOO_SHORT",
            "maxLength": "STRING_TOO_LONG",
            "multipleOf": "INVALID_PRECISION"
        }
        
        if not JSONSCHEMA_AVAILABLE:
            self.logger.warning("jsonschema library not available - validation disabled")
    
    def validate_response(self, data: Dict[str, Any], analysis_type: AnalysisType,
                         strict_mode: bool = True) -> ValidationReport:
        """
        Validate response data against the appropriate schema
        
        Args:
            data: Response data to validate
            analysis_type: Type of analysis for schema selection
            strict_mode: Whether to fail on warnings or treat them as non-fatal
            
        Returns:
            Comprehensive validation report
        """
        start_time = time.time()
        
        if not JSONSCHEMA_AVAILABLE:
            return ValidationReport(
                result=ValidationResult.SKIPPED,
                analysis_type=analysis_type,
                schema_version="unknown",
                is_valid=True,  # Assume valid if we can't validate
                warnings=["Schema validation skipped - jsonschema not available"]
            )
        
        try:
            # Get schema and validator
            schema = self.schema_registry.get_schema(analysis_type)
            validator = self._get_validator(schema, analysis_type)
            
            # Perform validation
            errors = list(validator.iter_errors(data))
            
            # Convert errors to FieldError objects
            field_errors = []
            warnings = []
            
            for error in errors:
                field_error = self._convert_jsonschema_error(error)
                
                # Categorize as error or warning
                if self._is_warning_level_error(error):
                    warnings.append(f"{field_error.field_path}: {field_error.error_message}")
                else:
                    field_errors.append(field_error)
            
            # Additional business logic validation
            business_errors, business_warnings = self._validate_business_rules(data, analysis_type)
            field_errors.extend(business_errors)
            warnings.extend(business_warnings)
            
            # Determine overall validation result
            is_valid = len(field_errors) == 0
            if not is_valid and not strict_mode:
                # In non-strict mode, only fail for critical errors
                critical_errors = [e for e in field_errors if self._is_critical_error(e)]
                is_valid = len(critical_errors) == 0
                if is_valid:
                    # Convert non-critical errors to warnings
                    for error in field_errors:
                        if not self._is_critical_error(error):
                            warnings.append(f"{error.field_path}: {error.error_message}")
                    field_errors = critical_errors
            
            # Calculate confidence impact
            confidence_impact = self._calculate_confidence_impact(field_errors, warnings)
            
            validation_time = (time.time() - start_time) * 1000
            
            result = ValidationReport(
                result=ValidationResult.VALID if is_valid else ValidationResult.INVALID,
                analysis_type=analysis_type,
                schema_version=schema.get("version", "unknown"),
                is_valid=is_valid,
                field_errors=field_errors,
                warnings=warnings,
                validation_time_ms=validation_time,
                confidence_impact=confidence_impact
            )
            
            self.logger.info(
                f"Schema validation completed for {analysis_type.value}: "
                f"{'VALID' if is_valid else 'INVALID'} "
                f"({len(field_errors)} errors, {len(warnings)} warnings) "
                f"in {validation_time:.1f}ms"
            )
            
            return result
            
        except Exception as e:
            validation_time = (time.time() - start_time) * 1000
            self.logger.error(f"Schema validation failed with exception: {e}")
            
            return ValidationReport(
                result=ValidationResult.ERROR,
                analysis_type=analysis_type,
                schema_version="unknown",
                is_valid=False,
                field_errors=[FieldError(
                    field_path="",
                    error_code="INTERNAL_ERROR",
                    error_message=f"Validation failed: {str(e)}"
                )],
                validation_time_ms=validation_time
            )
    
    def validate_and_enhance_data(self, data: Dict[str, Any], analysis_type: AnalysisType) -> Tuple[Dict[str, Any], ValidationReport]:
        """
        Validate data and enhance it with defaults and corrections where possible
        
        Args:
            data: Response data to validate and enhance
            analysis_type: Type of analysis for schema selection
            
        Returns:
            Tuple of (enhanced_data, validation_report)
        """
        # First, validate the original data
        report = self.validate_response(data, analysis_type, strict_mode=False)
        
        # If validation passed or had only warnings, try to enhance the data
        enhanced_data = data.copy()
        
        if report.result in [ValidationResult.VALID, ValidationResult.INVALID]:
            # Add missing metadata if not present
            enhanced_data = self._add_default_metadata(enhanced_data, analysis_type)
            
            # Fix common formatting issues
            enhanced_data = self._apply_auto_corrections(enhanced_data, analysis_type, report)
            
            # Re-validate enhanced data
            enhanced_report = self.validate_response(enhanced_data, analysis_type, strict_mode=False)
            
            if enhanced_report.is_valid and not report.is_valid:
                self.logger.info(f"Auto-correction improved validation for {analysis_type.value}")
                return enhanced_data, enhanced_report
        
        return enhanced_data, report
    
    def _get_validator(self, schema: Dict[str, Any], analysis_type: AnalysisType) -> Draft202012Validator:
        """Get cached or create new validator for schema"""
        if not self.enable_caching:
            return Draft202012Validator(schema)
        
        cache_key = f"{analysis_type.value}_{schema.get('version', 'unknown')}"
        current_time = time.time()
        
        # Check cache
        if cache_key in self._validator_cache:
            validator, cache_time = self._validator_cache[cache_key]
            if current_time - cache_time < self.cache_ttl_seconds:
                return validator
        
        # Create new validator and cache it
        validator = Draft202012Validator(schema)
        self._validator_cache[cache_key] = (validator, current_time)
        
        return validator
    
    def _convert_jsonschema_error(self, error: exceptions.ValidationError) -> FieldError:
        """Convert jsonschema ValidationError to FieldError"""
        # Build field path
        field_path = "/" + "/".join(str(p) for p in error.absolute_path) if error.absolute_path else "/"
        
        # Map error type to our error codes
        error_code = self._error_code_mapping.get(error.validator, error.validator.upper())
        
        # Create human-readable error message
        error_message = self._format_error_message(error)
        
        # Extract additional context
        expected_type = None
        constraint = None
        
        if error.validator == "type":
            expected_type = error.schema.get("type")
        elif error.validator in ["minimum", "maximum", "minLength", "maxLength"]:
            constraint = f"{error.validator}: {error.validator_value}"
        
        return FieldError(
            field_path=field_path,
            error_code=error_code,
            error_message=error_message,
            rejected_value=error.instance,
            expected_type=expected_type,
            constraint=constraint
        )
    
    def _format_error_message(self, error: exceptions.ValidationError) -> str:
        """Format jsonschema error into human-readable message"""
        if error.validator == "type":
            return f"Expected {error.schema.get('type')}, got {type(error.instance).__name__}"
        elif error.validator == "required":
            missing_field = error.validator_value[0] if error.validator_value else "unknown"
            return f"Missing required field: {missing_field}"
        elif error.validator == "pattern":
            return f"Value does not match required pattern: {error.validator_value}"
        elif error.validator == "enum":
            valid_values = ", ".join(str(v) for v in error.validator_value)
            return f"Value must be one of: {valid_values}"
        elif error.validator in ["minimum", "maximum"]:
            return f"Value must be {error.validator} {error.validator_value}"
        elif error.validator in ["minLength", "maxLength"]:
            return f"String length must be {error.validator} {error.validator_value}"
        elif error.validator == "additionalProperties":
            return f"Additional property not allowed: {error.validator_value}"
        elif error.validator == "multipleOf":
            return f"Value must be a multiple of {error.validator_value}"
        else:
            return error.message
    
    def _is_warning_level_error(self, error: exceptions.ValidationError) -> bool:
        """Determine if an error should be treated as a warning"""
        # Treat certain validation failures as warnings rather than errors
        warning_validators = ["additionalProperties"]
        return error.validator in warning_validators
    
    def _is_critical_error(self, field_error: FieldError) -> bool:
        """Determine if a field error is critical (should fail validation)"""
        critical_error_codes = [
            "INVALID_TYPE", "MISSING_REQUIRED_FIELD", 
            "VALUE_TOO_SMALL", "VALUE_TOO_LARGE"
        ]
        return field_error.error_code in critical_error_codes
    
    def _validate_business_rules(self, data: Dict[str, Any], analysis_type: AnalysisType) -> Tuple[List[FieldError], List[str]]:
        """Apply business-specific validation rules"""
        errors = []
        warnings = []
        
        if analysis_type == AnalysisType.SNAPSHOT:
            snapshot_errors, snapshot_warnings = self._validate_snapshot_business_rules(data)
            errors.extend(snapshot_errors)
            warnings.extend(snapshot_warnings)
        elif analysis_type == AnalysisType.SUPPORT_RESISTANCE:
            sr_errors, sr_warnings = self._validate_sr_business_rules(data)
            errors.extend(sr_errors)
            warnings.extend(sr_warnings)
        elif analysis_type == AnalysisType.TECHNICAL:
            tech_errors, tech_warnings = self._validate_technical_business_rules(data)
            errors.extend(tech_errors)
            warnings.extend(tech_warnings)
        
        return errors, warnings
    
    def _validate_snapshot_business_rules(self, data: Dict[str, Any]) -> Tuple[List[FieldError], List[str]]:
        """Validate snapshot-specific business rules"""
        errors = []
        warnings = []
        
        snapshot_data = data.get("snapshot_data", {})
        
        # Validate OHLC relationships
        open_price = snapshot_data.get("open")
        high_price = snapshot_data.get("high")
        low_price = snapshot_data.get("low")
        close_price = snapshot_data.get("close")
        current_price = snapshot_data.get("current_price")
        
        if all(isinstance(p, (int, float)) for p in [high_price, low_price, current_price]):
            if current_price > high_price:
                warnings.append("Current price exceeds session high")
            if current_price < low_price:
                warnings.append("Current price below session low")
        
        # Validate percentage/dollar change consistency
        percentage_change = snapshot_data.get("percentage_change")
        dollar_change = snapshot_data.get("dollar_change")
        
        if all(isinstance(v, (int, float)) for v in [percentage_change, dollar_change, close_price]):
            if close_price > 0:
                expected_percentage = (dollar_change / close_price) * 100
                if abs(percentage_change - expected_percentage) > 0.1:  # Allow 0.1% tolerance
                    warnings.append("Percentage change doesn't match dollar change calculation")
        
        return errors, warnings
    
    def _validate_sr_business_rules(self, data: Dict[str, Any]) -> Tuple[List[FieldError], List[str]]:
        """Validate support/resistance specific business rules"""
        errors = []
        warnings = []
        
        support_levels = data.get("support_levels", {})
        resistance_levels = data.get("resistance_levels", {})
        context = data.get("analysis_context", {})
        current_price = context.get("current_price")
        
        # Extract support prices
        support_prices = []
        for level in ["S1", "S2", "S3"]:
            level_data = support_levels.get(level, {})
            price = level_data.get("price")
            if isinstance(price, (int, float)):
                support_prices.append((level, price))
        
        # Extract resistance prices
        resistance_prices = []
        for level in ["R1", "R2", "R3"]:
            level_data = resistance_levels.get(level, {})
            price = level_data.get("price")
            if isinstance(price, (int, float)):
                resistance_prices.append((level, price))
        
        # Validate support level ordering
        support_prices.sort(key=lambda x: x[1], reverse=True)  # S1 should be highest
        for i in range(len(support_prices) - 1):
            if support_prices[i][1] <= support_prices[i+1][1]:
                warnings.append(f"Support levels may be out of order: {support_prices[i][0]} <= {support_prices[i+1][0]}")
        
        # Validate resistance level ordering
        resistance_prices.sort(key=lambda x: x[1])  # R1 should be lowest
        for i in range(len(resistance_prices) - 1):
            if resistance_prices[i][1] >= resistance_prices[i+1][1]:
                warnings.append(f"Resistance levels may be out of order: {resistance_prices[i][0]} >= {resistance_prices[i+1][0]}")
        
        # Validate S&R relative to current price
        if isinstance(current_price, (int, float)):
            for level, price in support_prices:
                if price > current_price:
                    warnings.append(f"Support level {level} (${price:.2f}) above current price (${current_price:.2f})")
            
            for level, price in resistance_prices:
                if price < current_price:
                    warnings.append(f"Resistance level {level} (${price:.2f}) below current price (${current_price:.2f})")
        
        return errors, warnings
    
    def _validate_technical_business_rules(self, data: Dict[str, Any]) -> Tuple[List[FieldError], List[str]]:
        """Validate technical analysis specific business rules"""
        errors = []
        warnings = []
        
        oscillators = data.get("oscillators", {})
        moving_averages = data.get("moving_averages", {})
        
        # Validate RSI bounds
        rsi_data = oscillators.get("RSI", {})
        rsi_value = rsi_data.get("value")
        if isinstance(rsi_value, (int, float)):
            if rsi_value < 0 or rsi_value > 100:
                errors.append(FieldError(
                    field_path="/oscillators/RSI/value",
                    error_code="VALUE_OUT_OF_RANGE",
                    error_message="RSI must be between 0 and 100",
                    rejected_value=rsi_value
                ))
        
        # Validate moving average ordering (generally shorter periods are more reactive)
        ema_data = moving_averages.get("exponential", {})
        sma_data = moving_averages.get("simple", {})
        
        for ma_type, ma_data in [("EMA", ema_data), ("SMA", sma_data)]:
            if ma_data:
                periods = [5, 10, 20, 50, 200]
                values = []
                for period in periods:
                    key = f"{ma_type}_{period}"
                    value = ma_data.get(key)
                    if isinstance(value, (int, float)):
                        values.append((period, value))
                
                # Check for reasonable relationships (not strict ordering due to market conditions)
                if len(values) >= 2:
                    extreme_crossovers = 0
                    for i in range(len(values) - 1):
                        shorter_period, shorter_value = values[i]
                        longer_period, longer_value = values[i + 1]
                        
                        # Count significant crossovers
                        if abs(shorter_value - longer_value) / max(shorter_value, longer_value) > 0.1:
                            extreme_crossovers += 1
                    
                    if extreme_crossovers > 2:
                        warnings.append(f"Unusual {ma_type} crossover pattern detected")
        
        return errors, warnings
    
    def _calculate_confidence_impact(self, field_errors: List[FieldError], warnings: List[str]) -> float:
        """Calculate how validation issues impact confidence score"""
        if not field_errors and not warnings:
            return 0.0  # No impact
        
        # Calculate impact based on error severity
        error_impact = len(field_errors) * 0.2  # Each error reduces confidence by 20%
        warning_impact = len(warnings) * 0.05  # Each warning reduces confidence by 5%
        
        total_impact = min(error_impact + warning_impact, 1.0)  # Cap at 100%
        return total_impact
    
    def _add_default_metadata(self, data: Dict[str, Any], analysis_type: AnalysisType) -> Dict[str, Any]:
        """Add default metadata if missing"""
        enhanced_data = data.copy()
        
        if "metadata" not in enhanced_data:
            enhanced_data["metadata"] = {}
        
        metadata = enhanced_data["metadata"]
        
        # Add missing timestamp
        if "timestamp" not in metadata:
            metadata["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
        
        # Add schema version
        if "schema_version" not in metadata:
            metadata["schema_version"] = SchemaVersion.CURRENT.value
        
        return enhanced_data
    
    def _apply_auto_corrections(self, data: Dict[str, Any], analysis_type: AnalysisType, 
                              report: ValidationReport) -> Dict[str, Any]:
        """Apply automatic corrections for common issues"""
        enhanced_data = data.copy()
        
        # Apply corrections based on field errors
        for error in report.field_errors:
            if error.error_code == "INVALID_TYPE" and "price" in error.field_path:
                # Try to convert string prices to numbers
                try:
                    path_parts = error.field_path.strip("/").split("/")
                    current_obj = enhanced_data
                    
                    # Navigate to the parent object
                    for part in path_parts[:-1]:
                        if part in current_obj:
                            current_obj = current_obj[part]
                        else:
                            break
                    
                    # Try to convert the value
                    field_name = path_parts[-1]
                    if field_name in current_obj:
                        value = current_obj[field_name]
                        if isinstance(value, str):
                            # Remove common price formatting
                            cleaned_value = value.replace("$", "").replace(",", "")
                            try:
                                current_obj[field_name] = float(cleaned_value)
                            except ValueError:
                                pass  # Leave as-is if conversion fails
                
                except (IndexError, KeyError, AttributeError):
                    pass  # Skip correction if path navigation fails
        
        return enhanced_data
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation performance statistics"""
        return {
            "cache_enabled": self.enable_caching,
            "cached_validators": len(self._validator_cache),
            "cache_ttl_seconds": self.cache_ttl_seconds,
            "jsonschema_available": JSONSCHEMA_AVAILABLE
        }


# Initialize global validator instance
schema_validator = SchemaValidator()


def validate_json_response(data: Dict[str, Any], analysis_type: AnalysisType, 
                          strict_mode: bool = True) -> ValidationReport:
    """
    Convenience function for validating JSON responses
    
    Args:
        data: Response data to validate
        analysis_type: Type of analysis for schema selection
        strict_mode: Whether to fail on warnings
        
    Returns:
        Validation report
    """
    return schema_validator.validate_response(data, analysis_type, strict_mode)


def enhance_and_validate(data: Dict[str, Any], analysis_type: AnalysisType) -> Tuple[Dict[str, Any], ValidationReport]:
    """
    Convenience function for enhancing and validating JSON responses
    
    Args:
        data: Response data to enhance and validate
        analysis_type: Type of analysis for schema selection
        
    Returns:
        Tuple of (enhanced_data, validation_report)
    """
    return schema_validator.validate_and_enhance_data(data, analysis_type)


if __name__ == "__main__":
    # Test the validation system
    from json_schemas import generate_example_responses
    
    print("🔍 JSON Schema Validation System Test")
    print("=" * 50)
    
    # Get example responses
    examples = generate_example_responses()
    
    # Test validation for each analysis type
    for analysis_type in AnalysisType:
        print(f"\n📊 Testing {analysis_type.value} validation...")
        
        example_data = examples[analysis_type.value]
        report = validate_json_response(example_data, analysis_type)
        
        status = "✅ VALID" if report.is_valid else "❌ INVALID"
        print(f"   Result: {status}")
        print(f"   Validation time: {report.validation_time_ms:.1f}ms")
        print(f"   Errors: {len(report.field_errors)}")
        print(f"   Warnings: {len(report.warnings)}")
        
        if not report.is_valid:
            print(f"   Error summary: {report.get_error_summary()}")
    
    # Test enhancement features
    print(f"\n🔧 Testing auto-enhancement...")
    
    # Create a malformed example
    malformed_data = {
        "snapshot_data": {
            "current_price": "150.25",  # String instead of number
            "percentage_change": 2.5,
            "volume": 45000000
        }
    }
    
    enhanced_data, enhanced_report = enhance_and_validate(malformed_data, AnalysisType.SNAPSHOT)
    print(f"   Original validation: {'VALID' if validate_json_response(malformed_data, AnalysisType.SNAPSHOT).is_valid else 'INVALID'}")
    print(f"   Enhanced validation: {'VALID' if enhanced_report.is_valid else 'INVALID'}")
    
    print(f"\n📈 Validation system ready for production!")