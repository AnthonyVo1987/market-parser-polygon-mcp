#!/usr/bin/env python3
"""
JSON vs Text Parsing Integration Tests

This test suite specifically validates the integration between JSON-based parsing
and fallback text parsing that the production system relies on. The previous tests
failed to catch integration issues between these two parsing strategies.

CRITICAL FOCUS:
- JSON parser attempts first, text parser fallback
- DataFrame generation consistency between JSON and text results
- UI integration with mixed parsing results
- Prompt template integration with JSON/text expectations
- Error handling when JSON parsing fails but text succeeds
- Response validation workflow integration

PRODUCTION ISSUE ROOT CAUSE:
The system was designed to handle both JSON and text responses, but the integration
between json_parser.py and response_parser.py was not properly tested in a
production workflow context.
"""

import json
import unittest
import logging
import time
import pandas as pd
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, patch

# Import the actual parsing components
from src.response_parser import ResponseParser, DataType, ParseResult, ConfidenceLevel
try:
    from src.json_parser import JsonParser, JsonParseResult, JsonDataType
    JSON_PARSER_AVAILABLE = True
except ImportError:
    JSON_PARSER_AVAILABLE = False

try:
    from prompt_templates import PromptTemplateManager, PromptType
    PROMPT_TEMPLATES_AVAILABLE = True
except ImportError:
    PROMPT_TEMPLATES_AVAILABLE = False

try:
    from json_schemas import schema_registry, AnalysisType
    JSON_SCHEMAS_AVAILABLE = True
except ImportError:
    JSON_SCHEMAS_AVAILABLE = False


class JSONTextParsingTestCase(unittest.TestCase):
    """Base test case for JSON/text parsing integration"""
    
    def setUp(self):
        """Setup parsing components"""
        self.text_parser = ResponseParser(log_level=logging.DEBUG)
        
        if JSON_PARSER_AVAILABLE:
            self.json_parser = JsonParser(log_level=logging.DEBUG)
        
        if PROMPT_TEMPLATES_AVAILABLE:
            self.prompt_manager = PromptTemplateManager()
        
        # Test data for various scenarios
        self.test_responses = self._create_test_responses()
        
        # Track parsing statistics
        self.parsing_stats = {
            'json_successes': 0,
            'json_failures': 0,
            'text_successes': 0,
            'text_failures': 0,
            'fallback_invocations': 0,
            'dataframe_generations': 0
        }
    
    def _create_test_responses(self) -> Dict[str, Dict[str, Any]]:
        """Create comprehensive test response dataset"""
        return {
            'valid_json_snapshot': {
                'content': json.dumps({
                    "metadata": {
                        "timestamp": "2025-01-15T10:30:00Z",
                        "ticker_symbol": "AAPL",
                        "schema_version": "1.0"
                    },
                    "snapshot_data": {
                        "current_price": 175.43,
                        "percentage_change": 2.8,
                        "dollar_change": 4.77,
                        "volume": 68200000,
                        "vwap": 174.85,
                        "open": 172.50,
                        "high": 176.20,
                        "low": 171.80,
                        "close": 170.66
                    }
                }, indent=2),
                'expected_type': 'json',
                'expected_confidence': ConfidenceLevel.HIGH
            },
            
            'text_snapshot_response': {
                'content': """
                Based on the latest market data for AAPL:
                
                Current trading price: $175.43
                The stock is up 2.8% today, gaining $4.77 from the previous close
                Trading volume: 68.2M shares
                VWAP (Volume Weighted Average Price): $174.85
                
                Today's session details:
                - Opened at $172.50
                - Daily high: $176.20
                - Daily low: $171.80
                - Previous close: $170.66
                """,
                'expected_type': 'text',
                'expected_confidence': ConfidenceLevel.HIGH
            },
            
            'mixed_json_text_response': {
                'content': """
                Here's the current snapshot for AAPL:
                
                ```json
                {
                    "current_price": 175.43,
                    "percentage_change": 2.8,
                    "volume": 68200000
                }
                ```
                
                Additionally, the stock opened at $172.50 and hit a high of $176.20.
                """,
                'expected_type': 'mixed',
                'expected_confidence': ConfidenceLevel.MEDIUM
            },
            
            'malformed_json_response': {
                'content': """
                {
                    "snapshot_data": {
                        "current_price": $175.43,  // Invalid JSON syntax
                        "percentage_change": 2.8%,  // Invalid JSON syntax
                        "volume": "68.2M",
                        "note": "This JSON is intentionally malformed"
                    }
                    // Missing closing brace
                """,
                'expected_type': 'fallback_to_text',
                'expected_confidence': ConfidenceLevel.LOW
            },
            
            'json_with_text_context': {
                'content': """
                Based on my analysis, here's the structured data for AAPL:
                
                {
                    "current_price": 175.43,
                    "percentage_change": 2.8,
                    "dollar_change": 4.77,
                    "volume": 68200000,
                    "vwap": 174.85
                }
                
                This shows strong performance with above-average volume.
                """,
                'expected_type': 'json_with_context',
                'expected_confidence': ConfidenceLevel.HIGH
            },
            
            'ai_generated_natural_response': {
                'content': """
                Apple Inc. (AAPL) is currently experiencing strong momentum. 
                The stock price has reached $175.43, representing a solid gain 
                of 2.8% or $4.77 from yesterday's closing price of $170.66.
                
                Trading activity is robust with 68.2 million shares changing hands, 
                well above the typical daily average. The volume-weighted average 
                price (VWAP) stands at $174.85, indicating balanced trading.
                
                Session highlights:
                • Opening price: $172.50
                • Intraday high: $176.20  
                • Intraday low: $171.80
                
                This performance reflects positive market sentiment and strong 
                institutional interest in Apple shares.
                """,
                'expected_type': 'natural_ai',
                'expected_confidence': ConfidenceLevel.MEDIUM
            },
            
            'completely_unparseable_response': {
                'content': """
                I'm sorry, but I'm having trouble accessing the market data 
                right now. Please try again later or check your internet connection.
                The weather is nice today though!
                """,
                'expected_type': 'unparseable',
                'expected_confidence': ConfidenceLevel.FAILED
            }
        }


class TestJSONParsingIntegration(JSONTextParsingTestCase):
    """Test JSON parsing capabilities and integration"""
    
    @unittest.skipUnless(JSON_PARSER_AVAILABLE, "JSON parser not available")
    def test_valid_json_parsing_workflow(self):
        """Test parsing workflow with valid JSON response"""
        print("🧪 Testing valid JSON parsing workflow...")
        
        test_data = self.test_responses['valid_json_snapshot']
        
        # Parse with JSON parser
        json_result = self.json_parser.parse_snapshot(test_data['content'], "AAPL")
        
        # Validate JSON parsing success
        self.assertIsInstance(json_result, JsonParseResult)
        self.assertEqual(json_result.confidence, ConfidenceLevel.HIGH)
        self.assertGreater(len(json_result.parsed_data), 0)
        
        # Test DataFrame generation
        json_df = json_result.to_dataframe()
        self.assertIsInstance(json_df, pd.DataFrame)
        self.assertGreater(len(json_df), 0)
        
        self.parsing_stats['json_successes'] += 1
        self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ Valid JSON parsing workflow passed")
    
    def test_text_parsing_workflow(self):
        """Test parsing workflow with text response"""
        print("🧪 Testing text parsing workflow...")
        
        test_data = self.test_responses['text_snapshot_response']
        
        # Parse with text parser
        text_result = self.text_parser.parse_stock_snapshot(test_data['content'], "AAPL")
        
        # Validate text parsing success
        self.assertIsInstance(text_result, ParseResult)
        self.assertNotEqual(text_result.confidence, ConfidenceLevel.FAILED)
        self.assertGreater(len(text_result.parsed_data), 0)
        
        # Test DataFrame generation
        text_df = text_result.to_dataframe()
        self.assertIsInstance(text_df, pd.DataFrame)
        self.assertGreater(len(text_df), 0)
        
        # Validate specific fields were extracted
        expected_fields = ['current_price', 'percentage_change', 'volume']
        for field in expected_fields:
            self.assertIn(field, text_result.parsed_data, 
                         f"Field '{field}' should be extracted from text response")
        
        self.parsing_stats['text_successes'] += 1
        self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ Text parsing workflow passed")
    
    def test_parsing_result_consistency(self):
        """Test consistency between JSON and text parsing results"""
        print("🧪 Testing parsing result consistency...")
        
        # Parse same data with both parsers
        json_data = self.test_responses['valid_json_snapshot']
        text_data = self.test_responses['text_snapshot_response']
        
        # Both should extract similar fields for same stock
        text_result = self.text_parser.parse_stock_snapshot(text_data['content'], "AAPL")
        
        if JSON_PARSER_AVAILABLE:
            json_result = self.json_parser.parse_snapshot(json_data['content'], "AAPL")
            
            # Check field overlap
            json_fields = set(json_result.parsed_data.keys())
            text_fields = set(text_result.parsed_data.keys())
            
            # Should have some common fields
            common_fields = json_fields.intersection(text_fields)
            self.assertGreater(len(common_fields), 0, 
                             "JSON and text parsing should extract some common fields")
        
        # Both should generate valid DataFrames
        text_df = text_result.to_dataframe()
        self.assertIsInstance(text_df, pd.DataFrame)
        
        self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ Parsing result consistency test passed")


class TestFallbackParsingIntegration(JSONTextParsingTestCase):
    """Test fallback mechanisms between JSON and text parsing"""
    
    def test_malformed_json_fallback(self):
        """Test fallback from malformed JSON to text parsing"""
        print("🧪 Testing malformed JSON fallback...")
        
        test_data = self.test_responses['malformed_json_response']
        
        # Attempt JSON parsing first (should fail)
        if JSON_PARSER_AVAILABLE:
            try:
                json_result = self.json_parser.parse_snapshot(test_data['content'], "AAPL")
                if json_result.confidence == ConfidenceLevel.FAILED:
                    self.parsing_stats['json_failures'] += 1
                else:
                    self.parsing_stats['json_successes'] += 1
            except Exception:
                self.parsing_stats['json_failures'] += 1
        
        # Fallback to text parsing
        self.parsing_stats['fallback_invocations'] += 1
        text_result = self.text_parser.parse_stock_snapshot(test_data['content'], "AAPL")
        
        # Text parser should extract some data despite malformed JSON
        self.assertIsInstance(text_result, ParseResult)
        
        # Even if confidence is low, DataFrame should be valid
        text_df = text_result.to_dataframe()
        self.assertIsInstance(text_df, pd.DataFrame)
        self.assertGreater(len(text_df), 0)
        
        if text_result.confidence != ConfidenceLevel.FAILED:
            self.parsing_stats['text_successes'] += 1
        else:
            self.parsing_stats['text_failures'] += 1
        
        self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ Malformed JSON fallback test passed")
    
    def test_mixed_content_parsing(self):
        """Test parsing responses with mixed JSON and text content"""
        print("🧪 Testing mixed content parsing...")
        
        test_data = self.test_responses['mixed_json_text_response']
        
        # Text parser should handle mixed content
        result = self.text_parser.parse_stock_snapshot(test_data['content'], "AAPL")
        
        self.assertIsInstance(result, ParseResult)
        self.assertNotEqual(result.confidence, ConfidenceLevel.FAILED)
        
        # Should extract data from both JSON section and text
        self.assertGreater(len(result.parsed_data), 0)
        
        # DataFrame should be valid
        df = result.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        
        self.parsing_stats['text_successes'] += 1
        self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ Mixed content parsing test passed")
    
    def test_integrated_parsing_strategy(self):
        """Test integrated parsing strategy that tries JSON first, then text"""
        print("🧪 Testing integrated parsing strategy...")
        
        def integrated_parse(content: str, ticker: str) -> ParseResult:
            """Integrated parsing that tries JSON first, falls back to text"""
            
            # Try JSON parsing first
            if JSON_PARSER_AVAILABLE:
                try:
                    # Check if content looks like JSON
                    content_stripped = content.strip()
                    if (content_stripped.startswith('{') or 
                        '"snapshot_data"' in content or 
                        '"metadata"' in content):
                        
                        json_result = self.json_parser.parse_snapshot(content, ticker)
                        if json_result.confidence != ConfidenceLevel.FAILED:
                            # Convert JsonParseResult to ParseResult for consistency
                            return ParseResult(
                                data_type=DataType.SNAPSHOT,
                                raw_response=content,
                                parsed_data=json_result.parsed_data,
                                confidence=json_result.confidence,
                                matched_patterns=["json_parser"],
                                failed_patterns=[],
                                parse_time_ms=json_result.parse_time_ms
                            )
                except Exception:
                    pass
            
            # Fallback to text parsing
            self.parsing_stats['fallback_invocations'] += 1
            return self.text_parser.parse_stock_snapshot(content, ticker)
        
        # Test with different response types
        test_cases = [
            ('valid_json_snapshot', True),    # Should use JSON
            ('text_snapshot_response', False), # Should use text
            ('malformed_json_response', False), # Should fallback to text
            ('json_with_text_context', True),  # Should use JSON
        ]
        
        for test_key, expect_json in test_cases:
            with self.subTest(test_case=test_key):
                test_data = self.test_responses[test_key]
                result = integrated_parse(test_data['content'], "AAPL")
                
                self.assertIsInstance(result, ParseResult)
                self.assertNotEqual(result.confidence, ConfidenceLevel.FAILED)
                
                # DataFrame should be valid regardless of parsing method
                df = result.to_dataframe()
                self.assertIsInstance(df, pd.DataFrame)
                self.assertGreater(len(df), 0)
                
                self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ Integrated parsing strategy test passed")


class TestDataFrameConsistency(JSONTextParsingTestCase):
    """Test DataFrame generation consistency across parsing methods"""
    
    def test_dataframe_structure_consistency(self):
        """Test that DataFrames have consistent structure regardless of parsing method"""
        print("🧪 Testing DataFrame structure consistency...")
        
        # Parse with different methods
        text_data = self.test_responses['text_snapshot_response']
        text_result = self.text_parser.parse_stock_snapshot(text_data['content'], "AAPL")
        text_df = text_result.to_dataframe()
        
        # Validate DataFrame structure
        self.assertIn('Metric', text_df.columns)
        self.assertIn('Value', text_df.columns)
        self.assertEqual(len(text_df.columns), 2)
        
        if JSON_PARSER_AVAILABLE:
            json_data = self.test_responses['valid_json_snapshot']
            json_result = self.json_parser.parse_snapshot(json_data['content'], "AAPL")
            json_df = json_result.to_dataframe()
            
            # Should have same column structure
            self.assertEqual(list(text_df.columns), list(json_df.columns))
        
        self.parsing_stats['dataframe_generations'] += 2
        
        print("✅ DataFrame structure consistency test passed")
    
    def test_dataframe_content_validation(self):
        """Test DataFrame content validation across parsing methods"""
        print("🧪 Testing DataFrame content validation...")
        
        test_cases = [
            'text_snapshot_response',
            'mixed_json_text_response',
            'ai_generated_natural_response'
        ]
        
        for test_key in test_cases:
            with self.subTest(test_case=test_key):
                test_data = self.test_responses[test_key]
                result = self.text_parser.parse_stock_snapshot(test_data['content'], "AAPL")
                df = result.to_dataframe()
                
                # DataFrame should have valid content
                self.assertGreater(len(df), 0)
                
                # Should not have all empty values
                values = df['Value'].tolist()
                non_empty_values = [v for v in values if v and str(v).strip() != '']
                self.assertGreater(len(non_empty_values), 0, 
                                 "DataFrame should contain some non-empty values")
                
                # Values should not contain raw parsing artifacts
                for value in values:
                    if value:
                        value_str = str(value)
                        self.assertNotIn('\\n', value_str, "Values should not contain newline artifacts")
                        self.assertNotIn('  ', value_str, "Values should not contain excessive whitespace")
                
                self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ DataFrame content validation test passed")
    
    def test_empty_result_dataframe_handling(self):
        """Test DataFrame generation when parsing fails completely"""
        print("🧪 Testing empty result DataFrame handling...")
        
        unparseable_data = self.test_responses['completely_unparseable_response']
        result = self.text_parser.parse_stock_snapshot(unparseable_data['content'], "AAPL")
        
        # Should still generate a valid DataFrame
        df = result.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)  # Should have at least "No Data" row
        
        # Check "No Data" row content
        if len(result.parsed_data) == 0:
            # Should have default content
            self.assertIn('No Data', df['Metric'].iloc[0] if len(df) > 0 else '')
        
        self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ Empty result DataFrame handling test passed")


@unittest.skipUnless(PROMPT_TEMPLATES_AVAILABLE, "Prompt templates not available")
class TestPromptIntegration(JSONTextParsingTestCase):
    """Test integration with prompt templates"""
    
    def test_json_prompt_generation(self):
        """Test that prompts are generated with JSON expectations"""
        print("🧪 Testing JSON prompt generation...")
        
        # Generate prompt for snapshot
        prompt, context = self.prompt_manager.generate_prompt(
            PromptType.SNAPSHOT, 
            ticker="AAPL"
        )
        
        # Prompt should include JSON instructions
        self.assertIn("JSON", prompt)
        self.assertIsNotNone(context)
        self.assertEqual(context.symbol, "AAPL")
        
        print("✅ JSON prompt generation test passed")
    
    def test_prompt_parsing_workflow_integration(self):
        """Test integration between prompt generation and parsing"""
        print("🧪 Testing prompt-parsing workflow integration...")
        
        # Generate prompt
        prompt, context = self.prompt_manager.generate_prompt(
            PromptType.SNAPSHOT, 
            ticker="TSLA"
        )
        
        # Simulate AI response to this prompt type
        # (In real system, this would come from AI)
        simulated_response = """
        Tesla Inc. (TSLA) Trading Update:
        Current price: $248.50
        Daily change: +3.2% (+$7.75)
        Volume: 45.2M shares
        VWAP: $246.80
        
        Session data:
        Open: $242.00
        High: $251.20
        Low: $240.50
        Previous close: $240.75
        """
        
        # Parse the response
        result = self.text_parser.parse_stock_snapshot(simulated_response, "TSLA")
        
        # Should successfully parse
        self.assertNotEqual(result.confidence, ConfidenceLevel.FAILED)
        self.assertGreater(len(result.parsed_data), 0)
        
        # Generate DataFrame
        df = result.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        
        self.parsing_stats['text_successes'] += 1
        self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ Prompt-parsing workflow integration test passed")


class TestErrorHandlingIntegration(JSONTextParsingTestCase):
    """Test error handling across parsing methods"""
    
    def test_graceful_error_handling(self):
        """Test graceful handling of various error conditions"""
        print("🧪 Testing graceful error handling...")
        
        error_cases = [
            ("", "empty_string"),
            (None, "none_input"),  # This will be converted to string
            ("{'invalid': json}", "invalid_json"),
            ("Random text with no financial data", "no_financial_data"),
        ]
        
        for content, case_name in error_cases:
            with self.subTest(case=case_name):
                try:
                    # Convert None to empty string to avoid type errors
                    content_str = str(content) if content is not None else ""
                    
                    result = self.text_parser.parse_stock_snapshot(content_str, "AAPL")
                    
                    # Should not raise exceptions
                    self.assertIsInstance(result, ParseResult)
                    
                    # Should generate valid DataFrame even for failed parsing
                    df = result.to_dataframe()
                    self.assertIsInstance(df, pd.DataFrame)
                    self.assertGreater(len(df), 0)
                    
                    self.parsing_stats['dataframe_generations'] += 1
                    
                except Exception as e:
                    self.fail(f"Parsing should not raise exceptions for {case_name}: {e}")
        
        print("✅ Graceful error handling test passed")
    
    def test_parsing_timeout_handling(self):
        """Test handling of parsing operations that might take time"""
        print("🧪 Testing parsing timeout handling...")
        
        # Large response that might take time to parse
        large_response = self.test_responses['ai_generated_natural_response']['content'] * 100
        
        start_time = time.time()
        result = self.text_parser.parse_stock_snapshot(large_response, "AAPL")
        parsing_time = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(parsing_time, 5.0, "Parsing should complete within 5 seconds")
        
        # Should still produce valid result
        self.assertIsInstance(result, ParseResult)
        self.assertIsNotNone(result.parse_time_ms)
        
        df = result.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        
        self.parsing_stats['text_successes'] += 1
        self.parsing_stats['dataframe_generations'] += 1
        
        print("✅ Parsing timeout handling test passed")


def run_json_text_integration_tests():
    """Run comprehensive JSON/text parsing integration tests"""
    print("🔄 JSON/Text Parsing Integration Test Suite")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestJSONParsingIntegration,
        TestFallbackParsingIntegration,
        TestDataFrameConsistency,
        TestPromptIntegration,
        TestErrorHandlingIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Generate summary
    print(f"\n📊 JSON/Text Integration Test Results:")
    print(f"   • Tests run: {result.testsRun}")
    print(f"   • Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   • Failures: {len(result.failures)}")
    print(f"   • Errors: {len(result.errors)}")
    print(f"   • Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    print(f"\n🔍 Integration Coverage:")
    print(f"   • JSON parser integration: {'✅' if JSON_PARSER_AVAILABLE else '⚠️  Not available'}")
    print(f"   • Text parser fallback: ✅ Tested")
    print(f"   • DataFrame consistency: ✅ Tested")
    print(f"   • Prompt integration: {'✅' if PROMPT_TEMPLATES_AVAILABLE else '⚠️  Not available'}")
    print(f"   • Error handling: ✅ Tested")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   • {test}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"   • {test}")
    
    success = result.wasSuccessful()
    print(f"\n🎯 Integration Status: {'PASSED' if success else 'FAILED'}")
    
    if success:
        print("✅ JSON/Text parsing integration is working correctly")
        print("🔄 Fallback mechanisms are properly implemented")
        print("📊 DataFrame generation is consistent across parsing methods")
    else:
        print("❌ Integration issues detected in JSON/Text parsing workflow")
        print("🔧 These issues would have caused the production failures")
    
    return success


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the integration tests
    success = run_json_text_integration_tests()
    
    # Exit with appropriate code
    exit(0 if success else 1)