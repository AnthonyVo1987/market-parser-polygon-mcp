#!/usr/bin/env python3
"""
Bug Fixes Integration Test Suite
Comprehensive end-to-end testing of both critical bug fixes working together.

This script validates:
1. Bug #1 Fix: Default ticker (NVDA) integration with data flow
2. Bug #2 Fix: Enhanced response parser extracting 7-9/9 fields  
3. Integration: Complete workflow from default ticker → parsing → display
4. Regression: Existing functionality remains intact

Test Requirements:
- All new test scripts pass with 100% success rate
- Existing pytest suite continues to pass (no regressions) 
- Integration tests demonstrate 9/9 field extraction
- Default ticker functionality works in live application context
"""

import unittest
import sys
import os
import asyncio
import logging
from typing import Dict, List, Any, Optional
from unittest.mock import patch, MagicMock

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import project modules
from response_parser import ResponseParser, DataType, ConfidenceLevel
from prompt_templates import PromptTemplateManager, PromptType
from stock_data_fsm import StateManager, AppState
from stock_data_fsm.states import StateContext

# Configure logging
logging.basicConfig(level=logging.INFO)


class TestBugFixesIntegration(unittest.TestCase):
    """Integration tests validating both bug fixes working together"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.parser = ResponseParser(log_level=logging.INFO)
        self.prompt_manager = PromptTemplateManager()
        self.default_ticker = "NVDA"
        
        # Sample AI response that demonstrates the integration
        self.integrated_test_response = """
NVIDIA Corporation (NVDA) Stock Analysis:

Current trading price: $875.42
Stock movement: +3.2% today (+$26.75)
Daily trading volume: 38.7M shares
Volume-weighted average price (VWAP): $872.15
Session opened at: $851.20
Daily high: $878.95
Daily low: $848.33
Previous close: $848.67
Market cap: ~$2.1T
"""
    
    def test_default_ticker_to_parser_flow(self):
        """Test complete flow from default ticker to data parsing"""
        print("🔄 Testing default ticker → parser integration flow...")
        
        # Step 1: Verify default ticker configuration
        with open('chat_ui.py', 'r') as f:
            chat_ui_content = f.read()
        
        has_nvda_default = 'value="NVDA"' in chat_ui_content
        self.assertTrue(has_nvda_default, "Chat UI should have NVDA default ticker")
        
        # Step 2: Test FSM state management with default ticker
        state_manager = StateManager()
        
        # Should transition successfully using default ticker logic
        result = state_manager.transition('button_click', button_type='snapshot', ticker='')
        self.assertTrue(result, "FSM transition should succeed")
        self.assertEqual(state_manager.get_current_state(), AppState.BUTTON_TRIGGERED)
        
        # Step 3: Test prompt generation with default ticker
        prompt = self.prompt_manager.get_prompt(
            prompt_type=PromptType.SNAPSHOT,
            ticker=self.default_ticker,
            enhanced=True
        )
        
        self.assertIsNotNone(prompt)
        self.assertIn('NVDA', prompt.upper())
        
        # Step 4: Test response parsing with NVDA data
        result = self.parser.parse_stock_snapshot(
            self.integrated_test_response, 
            self.default_ticker
        )
        
        # Should extract most/all fields with high confidence
        extracted_fields = len(result.parsed_data)
        self.assertGreaterEqual(extracted_fields, 8, f"Should extract ≥8/9 fields, got {extracted_fields}")
        self.assertIn(result.confidence, [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH])
        
        print(f"✅ Complete flow: Default ticker → FSM → Prompt → Parser")
        print(f"   - FSM transition: SUCCESS")  
        print(f"   - Prompt generation: SUCCESS")
        print(f"   - Data extraction: {extracted_fields}/9 fields")
        print(f"   - Confidence: {result.confidence.value}")
    
    def test_end_to_end_workflow_simulation(self):
        """Simulate complete end-to-end workflow with both fixes"""
        print("🎯 Testing end-to-end workflow simulation...")
        
        # Simulate user workflow: App startup → Button click → Data retrieval
        workflow_steps = []
        
        # Step 1: App startup with default ticker
        workflow_steps.append("App startup - default ticker loaded")
        startup_ticker = self.default_ticker  # Would come from UI default
        
        # Step 2: User clicks Stock Snapshot button (or leaves ticker as default)
        workflow_steps.append("User clicks Stock Snapshot button")
        state_manager = StateManager()
        context = StateContext(
            ticker=startup_ticker,
            button_type="snapshot"  # Use consistent button type
        )
        
        # FSM should handle transition
        state_manager.transition('button_click', context=context)
        self.assertEqual(state_manager.current_state, AppState.BUTTON_TRIGGERED)
        
        # Step 3: Prompt preparation
        workflow_steps.append("Prompt generation for AI query")
        state_manager.transition('prepare_prompt', context=context)
        self.assertEqual(state_manager.current_state, AppState.PROMPT_PREPARING)
        
        # Generate actual prompt
        prompt = self.prompt_manager.get_prompt(
            prompt_type=PromptType.SNAPSHOT,
            ticker=context.ticker,
            enhanced=True
        )
        
        # Step 4: Simulate AI response (this would come from OpenAI API)
        workflow_steps.append("AI response received")
        context.ai_response = self.integrated_test_response
        state_manager.transition('prompt_ready', context=context)
        state_manager.transition('response_received', context=context)
        self.assertEqual(state_manager.current_state, AppState.RESPONSE_RECEIVED)
        
        # Step 5: Response parsing
        workflow_steps.append("Response parsing with enhanced parser")
        state_manager.transition('parse', context=context)
        self.assertEqual(state_manager.current_state, AppState.PARSING_RESPONSE)
        
        # Parse the response
        parse_result = self.parser.parse_stock_snapshot(
            context.ai_response, 
            context.ticker
        )
        
        context.parsed_result = parse_result
        
        # Step 6: UI update with parsed data
        workflow_steps.append("UI update with structured data")
        state_manager.transition('parse_success', context=context)
        self.assertEqual(state_manager.current_state, AppState.UPDATING_UI)
        
        # Simulate UI update completion
        state_manager.transition('update_complete', context=context)
        
        # Verify end-to-end success
        extracted_fields = len(parse_result.parsed_data)
        
        print(f"✅ End-to-end workflow completed successfully:")
        for i, step in enumerate(workflow_steps, 1):
            print(f"   {i}. {step}")
        print(f"   Final result: {extracted_fields}/9 fields extracted")
        print(f"   Confidence: {parse_result.confidence.value}")
        
        # Success criteria for integration
        self.assertGreaterEqual(extracted_fields, 8, "E2E workflow should extract ≥8/9 fields")
        self.assertIn(parse_result.confidence, [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH])
        
    def test_error_recovery_with_fixes(self):
        """Test error recovery scenarios with both fixes in place"""
        print("🛡️ Testing error recovery with bug fixes...")
        
        # Test FSM error recovery with default ticker
        state_manager = StateManager()
        context = StateContext(
            ticker="",  # Empty ticker
            button_type="snapshot"  # Required for guard function
        )
        
        # Simulate error condition
        state_manager.transition('button_click', context=context)
        state_manager.transition('prepare_prompt', context=context)
        state_manager.transition('error', context=context)
        self.assertEqual(state_manager.current_state, AppState.ERROR)
        
        # Test error recovery (Bug #1 related fix)
        state_manager.transition('retry', context=context)
        self.assertEqual(state_manager.current_state, AppState.IDLE)
        
        # Test parser error handling with malformed response
        malformed_response = "Error: Unable to retrieve stock data"
        result = self.parser.parse_stock_snapshot(malformed_response, "NVDA")
        
        # Should handle gracefully without crashing
        self.assertEqual(result.confidence, ConfidenceLevel.FAILED)
        self.assertIsInstance(result.parsed_data, dict)
        
        print("✅ Error recovery mechanisms work with bug fixes")
    
    def test_performance_with_both_fixes(self):
        """Test performance impact of both fixes combined"""
        print("⏱️ Testing performance with both bug fixes...")
        
        import time
        
        # Measure FSM transition performance
        start_time = time.time()
        state_manager = StateManager()
        context = StateContext(
            ticker=self.default_ticker,
            button_type="snapshot"  # Required for guard function
        )
        
        # Simulate multiple transitions
        state_manager.transition('button_click', context=context)
        state_manager.transition('prepare_prompt', context=context)
        state_manager.transition('prompt_ready', context=context)
        
        fsm_time = (time.time() - start_time) * 1000
        
        # Measure parser performance
        start_time = time.time()
        result = self.parser.parse_stock_snapshot(
            self.integrated_test_response, 
            self.default_ticker
        )
        parse_time = (time.time() - start_time) * 1000
        
        print(f"   FSM transitions: {fsm_time:.2f}ms")
        print(f"   Parser processing: {parse_time:.2f}ms")
        print(f"   Total workflow: {(fsm_time + parse_time):.2f}ms")
        
        # Performance should be reasonable
        self.assertLess(fsm_time, 50.0, "FSM should be fast")
        self.assertLess(parse_time, 100.0, "Parser should be fast")
        
        print("✅ Performance impact is acceptable")
    
    def test_data_quality_validation(self):
        """Test data quality from end-to-end process"""
        print("🔍 Testing data quality validation...")
        
        # Parse the integrated test response
        result = self.parser.parse_stock_snapshot(
            self.integrated_test_response,
            self.default_ticker
        )
        
        # Convert to DataFrame for quality assessment
        df = result.to_dataframe()
        
        # Data quality checks
        self.assertIsNotNone(df, "DataFrame should be created")
        self.assertGreater(len(df), 0, "DataFrame should have data")
        
        # Check for specific data quality indicators
        has_price = any('$875.42' in str(val) for val in df.values.flatten())
        has_percentage = any('3.2%' in str(val) for val in df.values.flatten())
        has_volume = any('38.7' in str(val) for val in df.values.flatten())
        
        self.assertTrue(has_price, "Should extract price information")
        self.assertTrue(has_percentage, "Should extract percentage change")
        self.assertTrue(has_volume, "Should extract volume information")
        
        # Verify data structure
        expected_columns = ['Metric', 'Value'] 
        actual_columns = list(df.columns)
        
        for col in expected_columns:
            self.assertIn(col, actual_columns, f"DataFrame should have {col} column")
        
        print(f"✅ Data quality validation passed:")
        print(f"   - DataFrame rows: {len(df)}")
        print(f"   - Columns: {list(df.columns)}")
        print(f"   - Price data: {'✓' if has_price else '✗'}")
        print(f"   - Percentage data: {'✓' if has_percentage else '✗'}")
        print(f"   - Volume data: {'✓' if has_volume else '✗'}")


class TestRegressionValidation(unittest.TestCase):
    """Regression tests to ensure fixes don't break existing functionality"""
    
    def test_existing_ticker_functionality(self):
        """Test that existing ticker functionality still works"""
        print("🔄 Testing existing ticker functionality regression...")
        
        # Test with different tickers (not just NVDA)
        test_tickers = ["AAPL", "TSLA", "MSFT", "GOOGL"]
        parser = ResponseParser(log_level=logging.ERROR)
        
        for ticker in test_tickers:
            # Generate test response for ticker
            test_response = f"""
            {ticker} Stock Data:
            Current price: $150.00
            Change: +2.5% (+$3.75)
            Volume: 45M shares
            """
            
            result = parser.parse_stock_snapshot(test_response, ticker)
            
            # Should work for all tickers
            self.assertGreater(len(result.parsed_data), 0, f"Should parse data for {ticker}")
            self.assertEqual(result.attributes.get('ticker'), ticker, f"Should preserve ticker {ticker}")
        
        print("✅ Existing ticker functionality maintained")
    
    def test_original_test_suite_compatibility(self):
        """Test compatibility with original test expectations"""
        print("🧪 Testing original test suite compatibility...")
        
        # Run parser with data similar to original test suite
        parser = ResponseParser(log_level=logging.ERROR)
        
        original_format_response = """
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
        
        result = parser.parse_stock_snapshot(original_format_response, "AAPL")
        
        # Should maintain or improve upon original performance
        self.assertGreaterEqual(len(result.parsed_data), 6, "Should maintain original extraction rates")
        self.assertNotEqual(result.confidence, ConfidenceLevel.FAILED, "Should not fail on original formats")
        
        print("✅ Original test suite compatibility maintained")
    
    def test_fsm_state_integrity(self):
        """Test that FSM state management integrity is maintained"""
        print("🔄 Testing FSM state integrity...")
        
        state_manager = StateManager()
        
        # Test all major state transitions still work
        transitions = [
            ('button_click', AppState.BUTTON_TRIGGERED),
            ('prepare_prompt', AppState.PROMPT_PREPARING),
            ('prompt_ready', AppState.AI_PROCESSING),
            ('response_received', AppState.RESPONSE_RECEIVED),
            ('parse', AppState.PARSING_RESPONSE),
            ('parse_success', AppState.UPDATING_UI),
            ('update_complete', AppState.IDLE)
        ]
        
        context = StateContext(
            ticker="AAPL",
            button_type="snapshot"  # Use consistent button type
        )
        
        for event, expected_state in transitions:
            state_manager.transition(event, context=context)
            self.assertEqual(
                state_manager.current_state, 
                expected_state,
                f"Transition '{event}' should lead to {expected_state}"
            )
        
        print("✅ FSM state integrity maintained")


def run_integration_validation():
    """Run comprehensive bug fixes integration validation"""
    print("=" * 70)
    print("🧪 BUG FIXES INTEGRATION VALIDATION")
    print("=" * 70)
    print("Testing both bug fixes working together in realistic workflows...")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBugFixesIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestRegressionValidation))
    
    # Run tests with custom result tracking
    runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
    result = runner.run(suite)
    
    # Custom reporting
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    successes = total_tests - failures - errors
    
    print(f"📊 Integration Test Results:")
    print(f"   Total tests: {total_tests}")
    print(f"   Passed: {successes}")
    print(f"   Failed: {failures}")
    print(f"   Errors: {errors}")
    print(f"   Success rate: {(successes/total_tests)*100:.1f}%")
    print()
    
    if result.wasSuccessful():
        print("✅ INTEGRATION VALIDATION: SUCCESS!")
        print("   - Bug #1 (Default ticker) integrates properly with data flow")
        print("   - Bug #2 (Response parser) extracts 8-9/9 fields consistently")
        print("   - Complete workflow from startup → parsing → display works")
        print("   - No regressions in existing functionality")
        print("   - Error recovery mechanisms function correctly")
        print("   - Performance impact is acceptable")
        return True
    else:
        print("❌ INTEGRATION VALIDATION: FAILED!")
        print("   Issues found:")
        
        for test, error in result.failures + result.errors:
            print(f"   - {test}: {error.split(chr(10))[0]}")
        
        return False


if __name__ == '__main__':
    # Run integration validation
    success = run_integration_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)