"""
Unit tests for ResponseParser

This test suite validates the comprehensive parsing capabilities of the
ResponseParser class, including pattern matching, data validation,
confidence scoring, and error handling.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import logging
from response_parser import (
    ResponseParser, ParseResult, ConfidenceLevel, DataType, 
    ValidationError
)


class TestResponseParser(unittest.TestCase):
    """Test suite for ResponseParser class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = ResponseParser(log_level=logging.CRITICAL)  # Suppress logs during testing
        
        # Sample AI responses for testing
        self.sample_snapshot_response = """
        Here's the current stock snapshot for AAPL:
        Current price: $150.25
        The stock is up 2.5% today, gaining $3.75
        Volume: 45,000,000
        VWAP: $149.80
        Open: $148.50
        High: $151.00
        Low: $147.25
        Close: $150.25
        """
        
        self.sample_sr_response = """
        Support and Resistance Analysis:
        S1: $145.50
        S2: $142.00
        S3: $138.75
        R1: $155.25
        R2: $158.50
        R3: $162.00
        """
        
        self.sample_technical_response = """
        Technical Indicators:
        RSI: 68.5
        MACD: 0.25
        EMA 5: $151.20
        EMA 10: $149.85
        EMA 20: $147.50
        SMA 5: $150.95
        SMA 10: $148.75
        SMA 20: $146.80
        """
    
    # ====== Stock Snapshot Tests ======
    
    def test_parse_stock_snapshot_success(self):
        """Test successful stock snapshot parsing"""
        result = self.parser.parse_stock_snapshot(self.sample_snapshot_response, "AAPL")
        
        self.assertEqual(result.data_type, DataType.SNAPSHOT)
        self.assertEqual(result.confidence, ConfidenceLevel.HIGH)
        self.assertIn('current_price', result.parsed_data)
        self.assertIn('percentage_change', result.parsed_data)
        self.assertEqual(result.attributes['ticker'], 'AAPL')
        
        # Test DataFrame conversion
        df = result.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
    
    def test_parse_stock_snapshot_partial_data(self):
        """Test snapshot parsing with partial data"""
        partial_response = "Current price: $150.25. Volume: 1,000,000"
        result = self.parser.parse_stock_snapshot(partial_response)
        
        self.assertEqual(result.confidence, ConfidenceLevel.LOW)
        self.assertIn('current_price', result.parsed_data)
        self.assertIn('volume', result.parsed_data)
        self.assertLess(len(result.parsed_data), 9)  # Should have fewer than all fields
    
    def test_parse_stock_snapshot_empty_response(self):
        """Test snapshot parsing with empty response"""
        result = self.parser.parse_stock_snapshot("")
        
        self.assertEqual(result.confidence, ConfidenceLevel.FAILED)
        self.assertEqual(len(result.parsed_data), 0)
        
        # DataFrame should still be valid but empty
        df = result.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.iloc[0]['Metric'], 'No Data')
    
    def test_parse_stock_snapshot_invalid_price(self):
        """Test snapshot parsing with invalid price data"""
        invalid_response = "Current price: invalid_price"
        result = self.parser.parse_stock_snapshot(invalid_response)
        
        # Should have warnings for validation failures
        self.assertGreater(len(result.warnings), 0)
        self.assertIn('current_price', [fp.split(':')[0] for fp in result.failed_patterns])
    
    # ====== Support & Resistance Tests ======
    
    def test_parse_support_resistance_success(self):
        """Test successful S&R parsing"""
        result = self.parser.parse_support_resistance(self.sample_sr_response, "AAPL")
        
        self.assertEqual(result.data_type, DataType.SUPPORT_RESISTANCE)
        self.assertEqual(result.confidence, ConfidenceLevel.HIGH)
        self.assertIn('S1', result.parsed_data)
        self.assertIn('R1', result.parsed_data)
        self.assertEqual(result.attributes['ticker'], 'AAPL')
        
        # Test DataFrame conversion
        df = result.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), len(result.parsed_data))
    
    def test_parse_support_resistance_partial(self):
        """Test S&R parsing with only some levels"""
        partial_response = "S1: $145.50, R1: $155.25"
        result = self.parser.parse_support_resistance(partial_response)
        
        self.assertEqual(result.confidence, ConfidenceLevel.LOW)
        self.assertIn('S1', result.parsed_data)
        self.assertIn('R1', result.parsed_data)
        self.assertEqual(len(result.parsed_data), 2)
    
    def test_parse_support_resistance_relationship_validation(self):
        """Test validation of S&R level relationships"""
        # Invalid: S1 should be higher than S2
        invalid_response = "S1: $140.00, S2: $145.00, R1: $155.00"
        result = self.parser.parse_support_resistance(invalid_response)
        
        # Should have warnings about incorrect order
        warning_messages = ' '.join(result.warnings)
        self.assertIn('out of order', warning_messages.lower())
    
    # ====== Technical Indicators Tests ======
    
    def test_parse_technical_indicators_success(self):
        """Test successful technical indicators parsing"""
        result = self.parser.parse_technical_indicators(self.sample_technical_response, "AAPL")
        
        self.assertEqual(result.data_type, DataType.TECHNICAL)
        self.assertEqual(result.confidence, ConfidenceLevel.MEDIUM)  # Won't get all indicators
        self.assertIn('RSI', result.parsed_data)
        self.assertIn('MACD', result.parsed_data)
        
        # Test DataFrame conversion
        df = result.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
    
    def test_parse_technical_rsi_validation(self):
        """Test RSI validation (should be 0-100)"""
        invalid_rsi_response = "RSI: 150"  # Invalid RSI value
        result = self.parser.parse_technical_indicators(invalid_rsi_response)
        
        # Should have warnings for invalid RSI
        self.assertGreater(len(result.warnings), 0)
        warning_messages = ' '.join(result.warnings)
        self.assertIn('RSI', warning_messages)
    
    def test_parse_technical_with_emas_smas(self):
        """Test parsing of moving averages"""
        ma_response = "EMA 20: $150.00, SMA 50: $148.00, EMA 200: $145.00"
        result = self.parser.parse_technical_indicators(ma_response)
        
        self.assertIn('EMA_20', result.parsed_data)
        self.assertIn('SMA_50', result.parsed_data)
        self.assertIn('EMA_200', result.parsed_data)
        
        # Check attributes categorization
        self.assertEqual(result.attributes['emas'], 2)
        self.assertEqual(result.attributes['smas'], 1)
    
    # ====== Generic Parser Tests ======
    
    def test_parse_any_routing(self):
        """Test generic parse_any method routing"""
        # Test snapshot routing
        result = self.parser.parse_any(
            self.sample_snapshot_response, 
            DataType.SNAPSHOT, 
            "AAPL"
        )
        self.assertEqual(result.data_type, DataType.SNAPSHOT)
        
        # Test S&R routing
        result = self.parser.parse_any(
            self.sample_sr_response, 
            DataType.SUPPORT_RESISTANCE, 
            "AAPL"
        )
        self.assertEqual(result.data_type, DataType.SUPPORT_RESISTANCE)
        
        # Test technical routing
        result = self.parser.parse_any(
            self.sample_technical_response, 
            DataType.TECHNICAL, 
            "AAPL"
        )
        self.assertEqual(result.data_type, DataType.TECHNICAL)
    
    def test_parse_any_invalid_data_type(self):
        """Test parse_any with invalid data type"""
        with self.assertRaises(ValueError):
            self.parser.parse_any("test", "invalid_type", "AAPL")
    
    # ====== Confidence Level Tests ======
    
    def test_confidence_calculation_high(self):
        """Test high confidence calculation"""
        # Use a complete response that should match most patterns
        complete_response = self.sample_snapshot_response
        result = self.parser.parse_stock_snapshot(complete_response)
        
        # Should achieve high confidence with most fields matched
        self.assertEqual(result.confidence, ConfidenceLevel.HIGH)
        self.assertGreaterEqual(result.attributes['extraction_rate'], 0.8)
    
    def test_confidence_calculation_failed(self):
        """Test failed confidence calculation"""
        # Use a response with no matching patterns
        no_match_response = "This is completely unrelated text about weather."
        result = self.parser.parse_stock_snapshot(no_match_response)
        
        self.assertEqual(result.confidence, ConfidenceLevel.FAILED)
        self.assertEqual(len(result.parsed_data), 0)
    
    # ====== Data Validation Tests ======
    
    def test_price_validation_success(self):
        """Test successful price validation"""
        test_cases = [
            ("150.25", "$150.25"),
            ("$150.25", "$150.25"),
            ("1,500.00", "$1500.00"),
            ("50", "$50.00")
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = self.parser._validate_price(input_val)
                self.assertEqual(result, expected)
    
    def test_price_validation_failure(self):
        """Test price validation failures"""
        invalid_prices = ["-50.00", "not_a_price", "999999999.99"]
        
        for invalid_price in invalid_prices:
            with self.subTest(invalid_price=invalid_price):
                with self.assertRaises(ValidationError):
                    self.parser._validate_price(invalid_price)
    
    def test_percentage_validation(self):
        """Test percentage validation"""
        test_cases = [
            ("2.5", "+2.5%"),
            ("-1.2", "-1.2%"),
            ("+3.0", "+3.0%")
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = self.parser._validate_percentage(input_val)
                self.assertEqual(result, expected)
    
    def test_volume_validation(self):
        """Test volume validation"""
        test_cases = [
            ("1000000", "1,000,000"),
            ("45.5M", "45,500,000"),
            ("2.3K", "2,300"),
            ("1.5B", "1,500,000,000")
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = self.parser._validate_volume(input_val)
                self.assertEqual(result, expected)
    
    def test_rsi_validation(self):
        """Test RSI validation (0-100 range)"""
        # Valid RSI values
        valid_rsi = ["50.0", "0", "100", "68.5"]
        for rsi in valid_rsi:
            with self.subTest(rsi=rsi):
                result = self.parser._validate_rsi(rsi)
                self.assertTrue(0 <= float(result) <= 100)
        
        # Invalid RSI values
        invalid_rsi = ["-5", "150", "not_a_number"]
        for rsi in invalid_rsi:
            with self.subTest(rsi=rsi):
                with self.assertRaises(ValidationError):
                    self.parser._validate_rsi(rsi)
    
    # ====== ParseResult Tests ======
    
    def test_parse_result_to_dict(self):
        """Test ParseResult to_dict conversion"""
        result = self.parser.parse_stock_snapshot(self.sample_snapshot_response, "AAPL")
        result_dict = result.to_dict()
        
        self.assertIn('data_type', result_dict)
        self.assertIn('parsed_data', result_dict)
        self.assertIn('confidence', result_dict)
        self.assertEqual(result_dict['data_type'], 'snapshot')
    
    def test_parse_result_dataframe_conversions(self):
        """Test different DataFrame conversion methods"""
        # Test snapshot DataFrame
        snapshot_result = self.parser.parse_stock_snapshot(self.sample_snapshot_response)
        snapshot_df = snapshot_result.to_dataframe()
        self.assertIn('Metric', snapshot_df.columns)
        self.assertIn('Value', snapshot_df.columns)
        
        # Test S&R DataFrame
        sr_result = self.parser.parse_support_resistance(self.sample_sr_response)
        sr_df = sr_result.to_dataframe()
        self.assertIn('Level', sr_df.columns)
        self.assertIn('Price', sr_df.columns)
        
        # Test technical DataFrame
        tech_result = self.parser.parse_technical_indicators(self.sample_technical_response)
        tech_df = tech_result.to_dataframe()
        self.assertIn('Indicator', tech_df.columns)
        self.assertIn('Value', tech_df.columns)
    
    # ====== Pattern Matching Tests ======
    
    def test_multiple_pattern_matching(self):
        """Test that multiple patterns work for the same field"""
        # Test different ways to express price
        price_variations = [
            "Current price: $150.25",
            "Stock is trading at $150.25",
            "The stock is $150.25",
            "$150.25 per share"
        ]
        
        for variation in price_variations:
            with self.subTest(variation=variation):
                result = self.parser.parse_stock_snapshot(variation)
                self.assertIn('current_price', result.parsed_data)
                self.assertIn('$150.25', result.parsed_data['current_price'])
    
    def test_case_insensitive_matching(self):
        """Test case-insensitive pattern matching"""
        case_variations = [
            "CURRENT PRICE: $150.25",
            "current price: $150.25",
            "Current Price: $150.25",
            "CuRrEnT pRiCe: $150.25"
        ]
        
        for variation in case_variations:
            with self.subTest(variation=variation):
                result = self.parser.parse_stock_snapshot(variation)
                self.assertIn('current_price', result.parsed_data)
    
    # ====== Error Handling Tests ======
    
    def test_parser_exception_handling(self):
        """Test that parser handles exceptions gracefully"""
        # Test with malformed data that might cause regex errors
        malformed_data = "Price: $[invalid regex characters"
        result = self.parser.parse_stock_snapshot(malformed_data)
        
        # Should not crash and should return a valid result
        self.assertIsInstance(result, ParseResult)
        self.assertEqual(result.confidence, ConfidenceLevel.FAILED)
    
    def test_parse_time_tracking(self):
        """Test that parse time is tracked"""
        result = self.parser.parse_stock_snapshot(self.sample_snapshot_response)
        self.assertIsNotNone(result.parse_time_ms)
        self.assertGreater(result.parse_time_ms, 0)
    
    # ====== Statistics and Utility Tests ======
    
    def test_parsing_statistics(self):
        """Test parser statistics method"""
        stats = self.parser.get_parsing_statistics()
        
        self.assertIn('snapshot_patterns', stats)
        self.assertIn('sr_patterns', stats)
        self.assertIn('technical_patterns', stats)
        self.assertIn('total_patterns', stats)
        self.assertIn('validators', stats)
        
        # Verify reasonable counts
        self.assertGreater(stats['snapshot_patterns'], 5)
        self.assertGreater(stats['sr_patterns'], 3)
        self.assertGreater(stats['technical_patterns'], 10)
    
    # ====== Integration Tests ======
    
    def test_end_to_end_parsing_workflow(self):
        """Test complete parsing workflow"""
        # Test a realistic AI response
        complex_response = """
        Here's the complete analysis for TSLA:
        
        Stock Snapshot:
        Current trading price: $245.80
        Up 3.2% today (+$7.60)
        Volume: 28.5M shares
        VWAP: $243.50
        Session opened at $240.00, high of $246.50, low of $238.75
        Previous close: $238.20
        
        Support and Resistance:
        First support: $235.00 (S1)
        Second support: $228.50 (S2)  
        Third support: $220.00 (S3)
        First resistance: $250.00 (R1)
        Second resistance: $258.00 (R2)
        Third resistance: $265.00 (R3)
        
        Technical Indicators:
        RSI is at 72.5 (overbought territory)
        MACD: 1.85 (bullish signal)
        20-day EMA: $241.00
        50-day SMA: $235.50
        """
        
        # Parse each type
        snapshot_result = self.parser.parse_stock_snapshot(complex_response, "TSLA")
        sr_result = self.parser.parse_support_resistance(complex_response, "TSLA")
        tech_result = self.parser.parse_technical_indicators(complex_response, "TSLA")
        
        # Verify all parsers extracted relevant data
        self.assertGreater(len(snapshot_result.parsed_data), 5)
        self.assertGreater(len(sr_result.parsed_data), 4)
        self.assertGreater(len(tech_result.parsed_data), 3)
        
        # Verify confidence levels are reasonable
        self.assertIn(snapshot_result.confidence, [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH])
        self.assertIn(sr_result.confidence, [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH])
        self.assertIn(tech_result.confidence, [ConfidenceLevel.LOW, ConfidenceLevel.MEDIUM])


class TestConfidenceLevel(unittest.TestCase):
    """Test ConfidenceLevel enum"""
    
    def test_confidence_level_values(self):
        """Test confidence level enum values"""
        self.assertEqual(ConfidenceLevel.HIGH.value, "high")
        self.assertEqual(ConfidenceLevel.MEDIUM.value, "medium")
        self.assertEqual(ConfidenceLevel.LOW.value, "low")
        self.assertEqual(ConfidenceLevel.FAILED.value, "failed")


class TestDataType(unittest.TestCase):
    """Test DataType enum"""
    
    def test_data_type_values(self):
        """Test data type enum values"""
        self.assertEqual(DataType.SNAPSHOT.value, "snapshot")
        self.assertEqual(DataType.SUPPORT_RESISTANCE.value, "support_resistance")
        self.assertEqual(DataType.TECHNICAL.value, "technical")


if __name__ == '__main__':
    # Configure logging to see parser output during tests
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.wasSuccessful():
        print("✅ All ResponseParser tests passed!")
    else:
        print("❌ Some tests failed. Please review and fix issues.")
        exit(1)
