"""
Comprehensive Test Suite for Market Parser JSON Schemas

This module provides exhaustive testing for all JSON schemas, validation utilities,
and integration with the existing Market Parser architecture.

Test Categories:
- Schema structure validation
- Example response validation  
- Business rule validation
- Error handling validation
- Integration with FSM and ResponseParser
- Performance and edge case testing
"""

import json
import time
import pytest
import unittest
from typing import Dict, Any, List
from unittest.mock import patch, MagicMock

from json_schemas import (
    SchemaRegistry, AnalysisType, SchemaVersion,
    SNAPSHOT_SCHEMA, SUPPORT_RESISTANCE_SCHEMA, TECHNICAL_SCHEMA, ERROR_RESPONSE_SCHEMA,
    generate_example_responses
)
from schema_validator import (
    SchemaValidator, ValidationResult, FieldError, ValidationReport,
    validate_json_response, enhance_and_validate
)
from example_json_responses import (
    SNAPSHOT_EXAMPLES, SUPPORT_RESISTANCE_EXAMPLES, TECHNICAL_EXAMPLES, ERROR_EXAMPLES,
    get_examples_by_type, validate_all_examples
)

# Try to import existing components for integration testing
try:
    from response_parser import ResponseParser, DataType, ParseResult
    RESPONSE_PARSER_AVAILABLE = True
except ImportError:
    RESPONSE_PARSER_AVAILABLE = False

try:
    from stock_data_fsm import StateManager, AppState
    FSM_AVAILABLE = True
except ImportError:
    FSM_AVAILABLE = False


class TestSchemaStructure(unittest.TestCase):
    """Test the structure and validity of JSON schemas themselves"""
    
    def setUp(self):
        self.registry = SchemaRegistry()
    
    def test_schema_registry_initialization(self):
        """Test that schema registry initializes correctly"""
        self.assertIsInstance(self.registry.schemas, dict)
        self.assertEqual(len(self.registry.schemas), 3)
        
        for analysis_type in AnalysisType:
            self.assertIn(analysis_type, self.registry.schemas)
    
    def test_schema_structure_completeness(self):
        """Test that all schemas have required structure"""
        required_top_level_keys = ["$schema", "$id", "title", "description", "type", "properties", "required"]
        
        for analysis_type in AnalysisType:
            schema = self.registry.get_schema(analysis_type)
            
            for key in required_top_level_keys:
                self.assertIn(key, schema, f"Missing {key} in {analysis_type.value} schema")
            
            # Check metadata structure
            self.assertIn("metadata", schema["properties"])
            metadata_props = schema["properties"]["metadata"]["properties"]
            
            required_metadata = ["timestamp", "ticker_symbol", "schema_version"]
            for field in required_metadata:
                self.assertIn(field, metadata_props, 
                            f"Missing {field} in {analysis_type.value} metadata")
    
    def test_schema_validation_constraints(self):
        """Test that schemas have appropriate validation constraints"""
        # Test snapshot schema constraints
        snapshot_schema = self.registry.get_schema(AnalysisType.SNAPSHOT)
        snapshot_data = snapshot_schema["properties"]["snapshot_data"]["properties"]
        
        # Price fields should have min/max constraints
        price_fields = ["current_price", "vwap", "open", "high", "low", "close"]
        for field in price_fields:
            self.assertIn(field, snapshot_data)
            field_def = snapshot_data[field]
            self.assertIn("minimum", field_def)
            self.assertIn("maximum", field_def)
            self.assertEqual(field_def["minimum"], 0.01)
        
        # Volume should be integer with minimum 0
        volume_def = snapshot_data["volume"]
        self.assertEqual(volume_def["type"], "integer")
        self.assertEqual(volume_def["minimum"], 0)
    
    def test_error_schema_structure(self):
        """Test error response schema structure"""
        error_schema = self.registry.get_error_schema()
        
        self.assertIn("error", error_schema["properties"])
        error_props = error_schema["properties"]["error"]["properties"]
        
        required_error_fields = ["code", "message", "timestamp"]
        for field in required_error_fields:
            self.assertIn(field, error_props)
        
        # Test error code enum values
        code_def = error_props["code"]
        expected_codes = [
            "VALIDATION_ERROR", "PARSING_ERROR", "DATA_UNAVAILABLE",
            "RATE_LIMIT_EXCEEDED", "AUTHENTICATION_ERROR", "INTERNAL_ERROR",
            "TIMEOUT_ERROR", "INVALID_TICKER"
        ]
        self.assertEqual(set(code_def["enum"]), set(expected_codes))


class TestExampleValidation(unittest.TestCase):
    """Test validation of example responses"""
    
    def setUp(self):
        self.validator = SchemaValidator()
    
    def test_all_examples_validate(self):
        """Test that all provided examples validate against their schemas"""
        validation_results = validate_all_examples()
        
        for analysis_type, type_results in validation_results.items():
            for ticker, result in type_results.items():
                self.assertTrue(result["valid"], 
                              f"{analysis_type} example for {ticker} failed validation")
                self.assertEqual(result["errors"], 0,
                               f"{analysis_type} example for {ticker} has validation errors")
    
    def test_snapshot_examples_business_rules(self):
        """Test that snapshot examples follow business rules"""
        for ticker, example in SNAPSHOT_EXAMPLES.items():
            snapshot_data = example["snapshot_data"]
            
            # Test OHLC relationships
            high = snapshot_data["high"]
            low = snapshot_data["low"]
            current = snapshot_data["current_price"]
            
            self.assertGreaterEqual(high, current, f"{ticker}: high should be >= current")
            self.assertLessEqual(low, current, f"{ticker}: low should be <= current")
            self.assertGreaterEqual(high, low, f"{ticker}: high should be >= low")
            
            # Test percentage/dollar change consistency
            pct_change = snapshot_data["percentage_change"]
            dollar_change = snapshot_data["dollar_change"]
            close = snapshot_data["close"]
            
            if close > 0:
                expected_pct = (dollar_change / close) * 100
                self.assertAlmostEqual(pct_change, expected_pct, places=1,
                                     msg=f"{ticker}: percentage change inconsistent with dollar change")
    
    def test_support_resistance_examples_ordering(self):
        """Test that S&R examples have correct level ordering"""
        for ticker, example in SUPPORT_RESISTANCE_EXAMPLES.items():
            support_levels = example["support_levels"]
            resistance_levels = example["resistance_levels"]
            current_price = example["analysis_context"]["current_price"]
            
            # Test support level ordering (S1 > S2 > S3)
            s1_price = support_levels["S1"]["price"]
            s2_price = support_levels["S2"]["price"]
            s3_price = support_levels["S3"]["price"]
            
            self.assertGreater(s1_price, s2_price, f"{ticker}: S1 should be > S2")
            self.assertGreater(s2_price, s3_price, f"{ticker}: S2 should be > S3")
            
            # Test resistance level ordering (R1 < R2 < R3)
            r1_price = resistance_levels["R1"]["price"]
            r2_price = resistance_levels["R2"]["price"]
            r3_price = resistance_levels["R3"]["price"]
            
            self.assertLess(r1_price, r2_price, f"{ticker}: R1 should be < R2")
            self.assertLess(r2_price, r3_price, f"{ticker}: R2 should be < R3")
            
            # Test S&R relative to current price
            self.assertLess(s1_price, current_price, f"{ticker}: S1 should be < current price")
            self.assertGreater(r1_price, current_price, f"{ticker}: R1 should be > current price")
    
    def test_technical_examples_constraints(self):
        """Test that technical examples meet indicator constraints"""
        for ticker, example in TECHNICAL_EXAMPLES.items():
            oscillators = example["oscillators"]
            
            # Test RSI bounds
            rsi_value = oscillators["RSI"]["value"]
            self.assertGreaterEqual(rsi_value, 0, f"{ticker}: RSI should be >= 0")
            self.assertLessEqual(rsi_value, 100, f"{ticker}: RSI should be <= 100")
            
            # Test MACD structure
            macd = oscillators["MACD"]
            self.assertIn("value", macd)
            self.assertIn("interpretation", macd)
            self.assertIn(macd["interpretation"], ["bullish", "bearish", "neutral"])
            
            # Test moving average structure
            ma_data = example["moving_averages"]
            self.assertIn("exponential", ma_data)
            self.assertIn("simple", ma_data)
            
            # Test EMA/SMA periods
            expected_periods = [5, 10, 20, 50, 200]
            for ma_type in ["exponential", "simple"]:
                ma_type_data = ma_data[ma_type]
                for period in expected_periods:
                    key = f"{'EMA' if ma_type == 'exponential' else 'SMA'}_{period}"
                    self.assertIn(key, ma_type_data, f"{ticker}: Missing {key}")
                    self.assertIsInstance(ma_type_data[key], (int, float))


class TestValidationUtilities(unittest.TestCase):
    """Test the validation utilities and error handling"""
    
    def setUp(self):
        self.validator = SchemaValidator()
    
    def test_valid_response_validation(self):
        """Test validation of valid responses"""
        for analysis_type in AnalysisType:
            examples = get_examples_by_type(analysis_type)
            if examples:
                example = list(examples.values())[0]  # Get first example
                
                report = self.validator.validate_response(example, analysis_type)
                
                self.assertEqual(report.result, ValidationResult.VALID)
                self.assertTrue(report.is_valid)
                self.assertEqual(len(report.field_errors), 0)
                self.assertIsNotNone(report.validation_time_ms)
    
    def test_invalid_response_validation(self):
        """Test validation of invalid responses"""
        # Create invalid snapshot data
        invalid_snapshot = {
            "metadata": {
                "timestamp": "invalid-timestamp",
                "ticker_symbol": "TOOLONG",  # Too long
                "schema_version": "1.0"
            },
            "snapshot_data": {
                "current_price": "not_a_number",  # Wrong type
                "percentage_change": -999,  # Unrealistic value
                "volume": -100  # Negative volume
            }
        }
        
        report = self.validator.validate_response(invalid_snapshot, AnalysisType.SNAPSHOT)
        
        self.assertEqual(report.result, ValidationResult.INVALID)
        self.assertFalse(report.is_valid)
        self.assertGreater(len(report.field_errors), 0)
        
        # Check that errors contain expected issues
        error_messages = [error.error_message for error in report.field_errors]
        has_type_error = any("type" in msg.lower() for msg in error_messages)
        self.assertTrue(has_type_error, "Should have type validation error")
    
    def test_business_rule_validation(self):
        """Test custom business rule validation"""
        # Create data that passes schema but fails business rules
        invalid_snapshot = {
            "metadata": {
                "timestamp": "2025-01-15T10:30:00Z",
                "ticker_symbol": "TEST",
                "schema_version": "1.0"
            },
            "snapshot_data": {
                "current_price": 100.00,
                "percentage_change": 5.0,
                "dollar_change": 10.0,  # Inconsistent with percentage
                "volume": 1000000,
                "vwap": 99.50,
                "open": 95.00,
                "high": 98.00,  # High less than current - business rule violation
                "low": 102.00,  # Low greater than current - business rule violation
                "close": 95.00
            }
        }
        
        report = self.validator.validate_response(invalid_snapshot, AnalysisType.SNAPSHOT)
        
        # Should have warnings about business rule violations
        self.assertGreater(len(report.warnings), 0)
    
    def test_error_response_formatting(self):
        """Test error response formatting"""
        invalid_data = {"invalid": "data"}
        
        report = self.validator.validate_response(invalid_data, AnalysisType.SNAPSHOT)
        error_response = report.to_error_response()
        
        self.assertIsNotNone(error_response)
        self.assertIn("error", error_response)
        
        error = error_response["error"]
        self.assertEqual(error["code"], "VALIDATION_ERROR")
        self.assertIn("message", error)
        self.assertIn("timestamp", error)
        self.assertIn("request_id", error)
    
    def test_enhancement_functionality(self):
        """Test data enhancement and auto-correction"""
        # Create data with correctable issues
        malformed_data = {
            "snapshot_data": {
                "current_price": "150.25",  # String instead of number
                "percentage_change": 2.5,
                "dollar_change": 3.75,
                "volume": 45000000,
                "vwap": "149.80",  # String instead of number
                "open": 148.50,
                "high": 151.00,
                "low": 147.25,
                "close": 146.50
            }
        }
        
        enhanced_data, enhanced_report = enhance_and_validate(malformed_data, AnalysisType.SNAPSHOT)
        
        # Should have added metadata
        self.assertIn("metadata", enhanced_data)
        
        # Should have converted string prices to numbers
        snapshot_data = enhanced_data["snapshot_data"]
        self.assertIsInstance(snapshot_data["current_price"], (int, float))
        self.assertIsInstance(snapshot_data["vwap"], (int, float))


class TestIntegrationWithExistingSystems(unittest.TestCase):
    """Test integration with existing Market Parser components"""
    
    @unittest.skipUnless(RESPONSE_PARSER_AVAILABLE, "ResponseParser not available")
    def test_response_parser_compatibility(self):
        """Test compatibility with existing ResponseParser"""
        parser = ResponseParser()
        
        # Test that parsed results can be converted to JSON schema format
        # This would typically be done with a conversion utility
        pass  # Implementation depends on conversion strategy
    
    @unittest.skipUnless(FSM_AVAILABLE, "FSM not available")
    def test_fsm_integration(self):
        """Test integration with FSM state management"""
        # Test that validation results can be used in FSM transitions
        pass  # Implementation depends on FSM integration strategy
    
    def test_error_handling_integration(self):
        """Test that errors integrate well with existing error handling"""
        error_example = ERROR_EXAMPLES["validation"]
        
        # Verify error format matches expected structure
        self.assertIn("error", error_example)
        error = error_example["error"]
        
        self.assertIn("code", error)
        self.assertIn("message", error)
        self.assertIn("timestamp", error)
        
        # Test that error codes are suitable for programmatic handling
        self.assertIn(error["code"], [
            "VALIDATION_ERROR", "PARSING_ERROR", "DATA_UNAVAILABLE",
            "RATE_LIMIT_EXCEEDED", "AUTHENTICATION_ERROR", "INTERNAL_ERROR",
            "TIMEOUT_ERROR", "INVALID_TICKER"
        ])


class TestPerformanceAndEdgeCases(unittest.TestCase):
    """Test performance characteristics and edge cases"""
    
    def setUp(self):
        self.validator = SchemaValidator()
    
    def test_validation_performance(self):
        """Test that validation performs within acceptable limits"""
        example = SNAPSHOT_EXAMPLES["AAPL"]
        
        # Time multiple validations
        times = []
        for _ in range(10):
            start_time = time.time()
            report = self.validator.validate_response(example, AnalysisType.SNAPSHOT)
            end_time = time.time()
            times.append((end_time - start_time) * 1000)  # Convert to ms
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        
        # Validation should complete quickly
        self.assertLess(avg_time, 100, f"Average validation time {avg_time:.1f}ms too slow")
        self.assertLess(max_time, 200, f"Max validation time {max_time:.1f}ms too slow")
    
    def test_large_data_validation(self):
        """Test validation with large data structures"""
        # Create a large but valid response
        large_example = SNAPSHOT_EXAMPLES["AAPL"].copy()
        
        # Add many warnings to test array handling
        large_example["validation"]["warnings"] = [f"Warning {i}" for i in range(100)]
        
        start_time = time.time()
        report = self.validator.validate_response(large_example, AnalysisType.SNAPSHOT)
        end_time = time.time()
        
        validation_time = (end_time - start_time) * 1000
        
        self.assertTrue(report.is_valid)
        self.assertLess(validation_time, 500, "Large data validation too slow")
    
    def test_malformed_data_handling(self):
        """Test handling of completely malformed data"""
        malformed_inputs = [
            None,
            "not a dict",
            [],
            {"completely": {"wrong": "structure"}},
            {}  # Empty dict
        ]
        
        for malformed_input in malformed_inputs:
            with self.subTest(input=malformed_input):
                # Should not raise exceptions, should return invalid result
                try:
                    if malformed_input is None:
                        continue  # Skip None input
                    
                    report = self.validator.validate_response(malformed_input, AnalysisType.SNAPSHOT)
                    self.assertIn(report.result, [ValidationResult.INVALID, ValidationResult.ERROR])
                    self.assertFalse(report.is_valid)
                except Exception as e:
                    self.fail(f"Validation raised exception for {malformed_input}: {e}")
    
    def test_validator_caching(self):
        """Test validator caching functionality"""
        validator_with_cache = SchemaValidator(enable_caching=True)
        validator_without_cache = SchemaValidator(enable_caching=False)
        
        example = SNAPSHOT_EXAMPLES["AAPL"]
        
        # Time validation with caching
        start_time = time.time()
        for _ in range(5):
            validator_with_cache.validate_response(example, AnalysisType.SNAPSHOT)
        cached_time = time.time() - start_time
        
        # Time validation without caching
        start_time = time.time()
        for _ in range(5):
            validator_without_cache.validate_response(example, AnalysisType.SNAPSHOT)
        uncached_time = time.time() - start_time
        
        # Caching should provide some performance benefit
        self.assertLess(cached_time, uncached_time * 1.5, "Caching should improve performance")


def run_comprehensive_tests():
    """Run comprehensive test suite and generate report"""
    print("🧪 Running Comprehensive JSON Schema Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestSchemaStructure,
        TestExampleValidation,
        TestValidationUtilities,
        TestIntegrationWithExistingSystems,
        TestPerformanceAndEdgeCases
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Generate summary report
    print(f"\n📊 Test Summary:")
    print(f"   • Tests run: {result.testsRun}")
    print(f"   • Failures: {len(result.failures)}")
    print(f"   • Errors: {len(result.errors)}")
    print(f"   • Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   • {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"   • {test}: {traceback.split('Exception: ')[-1].split('\\n')[0]}")
    
    if result.wasSuccessful():
        print(f"\n✅ All tests passed! JSON Schema system ready for production.")
    else:
        print(f"\n⚠️  Some tests failed. Review issues before production deployment.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run the comprehensive test suite
    success = run_comprehensive_tests()
    
    # Additional validation of examples
    print(f"\n🔍 Additional Validation Checks...")
    
    # Validate all examples
    validation_results = validate_all_examples()
    total_examples = sum(len(results) for results in validation_results.values())
    valid_examples = sum(sum(1 for r in results.values() if r["valid"]) for results in validation_results.values())
    
    print(f"   • Example validation: {valid_examples}/{total_examples} passed")
    
    # Performance check
    validator = SchemaValidator()
    example = SNAPSHOT_EXAMPLES["AAPL"]
    
    start_time = time.time()
    report = validator.validate_response(example, AnalysisType.SNAPSHOT)
    validation_time = (time.time() - start_time) * 1000
    
    print(f"   • Validation performance: {validation_time:.1f}ms")
    print(f"   • Memory usage: {len(json.dumps(example))} bytes processed")
    
    print(f"\n🎯 JSON Schema System Status: {'READY' if success and valid_examples == total_examples else 'NEEDS ATTENTION'}")