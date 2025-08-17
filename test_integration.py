"""
Comprehensive Integration Tests for Stock Market Analysis System
Phase 5: End-to-End Testing

This test suite validates the complete integration of all system components:
- FSM State Management
- Response Parsing
- Prompt Templates  
- Enhanced UI with Loading States
- Error Handling and Recovery
"""

import unittest
import asyncio
import logging
from unittest.mock import patch, MagicMock, AsyncMock
import pandas as pd
import time

# Import all system components
from stock_data_fsm import StateManager, AppState
from response_parser import ResponseParser, DataType, ConfidenceLevel
from prompt_templates import PromptTemplateManager, PromptType, TickerExtractor
from market_parser_demo import TokenCostTracker

# Import the enhanced UI components
try:
    from chat_ui_final import (
        handle_user_message, handle_button_click, ProcessingStatus,
        _get_debug_state_info, _clear_enhanced, export_markdown
    )
    UI_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import UI components: {e}")
    UI_AVAILABLE = False


class TestSystemIntegration(unittest.TestCase):
    """Test complete system integration scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.fsm_manager = StateManager()
        self.parser = ResponseParser(log_level=logging.CRITICAL)
        self.prompt_manager = PromptTemplateManager()
        self.tracker = TokenCostTracker()
        
        # Sample data for testing
        self.sample_responses = {
            'snapshot': """
            Apple Inc. (AAPL) Stock Analysis:
            Current price: $150.25
            Percentage change: +2.5%
            Dollar change: +$3.75
            Volume: 45,000,000 shares
            VWAP: $149.80
            Open: $148.50
            High: $151.00
            Low: $147.25
            Close: $150.25
            """,
            'support_resistance': """
            Support and Resistance Analysis for AAPL:
            S1: $145.50
            S2: $142.00
            S3: $138.75
            R1: $155.25
            R2: $158.50
            R3: $162.00
            """,
            'technical': """
            Technical Analysis for AAPL:
            RSI: 68.5
            MACD: 0.25
            EMA 5: $151.20
            EMA 10: $149.85
            EMA 20: $147.50
            EMA 50: $144.75
            EMA 200: $140.25
            SMA 5: $150.95
            SMA 10: $148.75
            SMA 20: $146.80
            SMA 50: $143.90
            SMA 200: $139.50
            """
        }
    
    def test_fsm_state_transitions(self):
        """Test complete FSM workflow"""
        # Start in IDLE state
        self.assertEqual(self.fsm_manager.get_current_state(), AppState.IDLE)
        
        # Trigger button click
        success = self.fsm_manager.transition('button_click', 
                                            button_type='snapshot', 
                                            ticker='AAPL')
        self.assertTrue(success)
        self.assertEqual(self.fsm_manager.get_current_state(), AppState.BUTTON_TRIGGERED)
        
        # Prepare prompt
        success = self.fsm_manager.transition('prepare_prompt')
        self.assertTrue(success)
        
        # Complete workflow
        self.fsm_manager.transition('prompt_ready')
        self.fsm_manager.transition('response_received')
        self.fsm_manager.transition('parse')
        self.fsm_manager.transition('parse_success')
        self.fsm_manager.transition('update_complete')
        
        # Should return to IDLE
        self.assertEqual(self.fsm_manager.get_current_state(), AppState.IDLE)
    
    def test_end_to_end_parsing_workflow(self):
        """Test complete parsing workflow with all data types"""
        for data_type, response_text in self.sample_responses.items():
            with self.subTest(data_type=data_type):
                # Map data type
                type_map = {
                    'snapshot': DataType.SNAPSHOT,
                    'support_resistance': DataType.SUPPORT_RESISTANCE,
                    'technical': DataType.TECHNICAL
                }
                
                # Parse response
                parse_result = self.parser.parse_any(response_text, type_map[data_type], 'AAPL')
                
                # Validate results
                self.assertIsNotNone(parse_result)
                self.assertGreater(len(parse_result.parsed_data), 0)
                self.assertIn(parse_result.confidence, [
                    ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM
                ])
                
                # Test DataFrame conversion
                df = parse_result.to_dataframe()
                self.assertIsInstance(df, pd.DataFrame)
                self.assertGreater(len(df), 0)
    
    def test_prompt_template_integration(self):
        """Test prompt template generation and parsing compatibility"""
        for prompt_type in PromptType:
            with self.subTest(prompt_type=prompt_type):
                # Generate prompt
                prompt, ticker_context = self.prompt_manager.generate_prompt(
                    prompt_type, ticker="AAPL"
                )
                
                # Validate prompt structure
                self.assertIn("### STOCK ANALYSIS REQUEST ###", prompt)
                self.assertIn("### FORMATTING REQUIREMENTS ###", prompt)
                self.assertIn("### EXAMPLE RESPONSE FORMAT ###", prompt)
                self.assertIn("AAPL", prompt)
                
                # Test ticker context
                self.assertEqual(ticker_context.symbol, "AAPL")
                self.assertGreater(ticker_context.confidence, 0.8)
    
    def test_ticker_extraction_scenarios(self):
        """Test ticker extraction in various scenarios"""
        extractor = TickerExtractor()
        
        test_cases = [
            ("Looking at $AAPL today", "AAPL", "explicit"),
            ("Apple Inc. earnings", "AAPL", "company_name"),
            ("Tesla is performing well", "TSLA", "company_name"),
            ("Microsoft stock analysis", "MSFT", "company_name"),
        ]
        
        for text, expected_ticker, expected_source in test_cases:
            with self.subTest(text=text):
                result = extractor.extract_ticker(text)
                self.assertEqual(result.symbol, expected_ticker)
                self.assertEqual(result.source, expected_source)
    
    def test_error_handling_and_recovery(self):
        """Test system error handling and recovery mechanisms"""
        # Test FSM error handling
        fsm = StateManager()
        
        # Try invalid transition
        success = fsm.transition('invalid_event')
        self.assertFalse(success)
        self.assertEqual(fsm.get_current_state(), AppState.IDLE)  # Should stay in same state
        
        # Test parser error handling
        invalid_response = "This is not a valid stock response"
        parse_result = self.parser.parse_stock_snapshot(invalid_response, "TEST")
        
        # Should handle gracefully
        self.assertEqual(parse_result.confidence, ConfidenceLevel.FAILED)
        self.assertLessEqual(len(parse_result.parsed_data), 1)  # Minimal or no data
        
        # Test prompt generation error handling
        try:
            prompt, context = self.prompt_manager.generate_prompt(
                PromptType.SNAPSHOT, ticker=""
            )
            # Should not crash and should provide fallback
            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt), 0)
        except Exception as e:
            self.fail(f"Prompt generation should handle empty ticker gracefully: {e}")
    
    def test_conversation_context_tracking(self):
        """Test conversation context tracking across multiple interactions"""
        extractor = TickerExtractor()
        chat_history = [
            {"role": "user", "content": "Tell me about Apple"},
            {"role": "assistant", "content": "Apple Inc. (AAPL) is a technology company..."},
            {"role": "user", "content": "What about the technical analysis?"},
        ]
        
        # Should extract AAPL from context
        result = extractor.extract_ticker("technical analysis", chat_history)
        self.assertEqual(result.symbol, "AAPL")
        self.assertIn(result.source, ["company_name", "context"])


@unittest.skipIf(not UI_AVAILABLE, "UI components not available")
class TestUIIntegration(unittest.TestCase):
    """Test UI component integration"""
    
    def setUp(self):
        """Set up UI test fixtures"""
        self.processing_status = ProcessingStatus()
        self.fsm_manager = StateManager()
        self.tracker = TokenCostTracker()
        
        # Mock chat history
        self.chat_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help you?"}
        ]
    
    def test_processing_status_management(self):
        """Test processing status management"""
        # Test initialization
        self.assertFalse(self.processing_status.is_processing)
        
        # Test start processing
        self.processing_status.start_processing("Test process", 5)
        self.assertTrue(self.processing_status.is_processing)
        self.assertEqual(self.processing_status.total_steps, 5)
        
        # Test step updates
        self.processing_status.update_step("Step 1", 1)
        self.assertEqual(self.processing_status.progress, 1)
        self.assertIn("Step 1", self.processing_status.status_message)
        
        # Test completion
        self.processing_status.complete("Done")
        self.assertFalse(self.processing_status.is_processing)
        self.assertIn("Done", self.processing_status.status_message)
    
    def test_debug_state_info(self):
        """Test debug state information generation"""
        debug_info = _get_debug_state_info(self.fsm_manager)
        
        self.assertIn("FSM State:", debug_info)
        self.assertIn("Button Type:", debug_info)
        self.assertIn("Ticker:", debug_info)
        self.assertIn("IDLE", debug_info)  # Should be in IDLE state
    
    def test_clear_enhanced_functionality(self):
        """Test enhanced clear functionality"""
        result = _clear_enhanced()
        
        # Should return proper tuple
        self.assertEqual(len(result), 10)
        
        # Chat history should be empty
        self.assertEqual(result[0], [])  # chatbot
        self.assertEqual(result[1], [])  # pyd_history_state
        
        # Should have new tracker
        self.assertIsInstance(result[2], TokenCostTracker)
        
        # DataFrames should be empty
        self.assertIsInstance(result[6], pd.DataFrame)  # snapshot_df
        self.assertIsInstance(result[7], pd.DataFrame)  # sr_df
        self.assertIsInstance(result[8], pd.DataFrame)  # tech_df
    
    def test_markdown_export(self):
        """Test markdown export functionality"""
        markdown = export_markdown(self.chat_history, self.tracker)
        
        self.assertIn("# 📊 Stock Market Analysis Chat Export", markdown)
        self.assertIn("Export Date:", markdown)
        self.assertIn("Total Messages: 2", markdown)
        self.assertIn("Message 1 (User)", markdown)
        self.assertIn("Message 2 (Assistant)", markdown)
        self.assertIn("Hello", markdown)
        self.assertIn("Hi! How can I help you?", markdown)


class TestPerformanceAndReliability(unittest.TestCase):
    """Test system performance and reliability under various conditions"""
    
    def setUp(self):
        """Set up performance test fixtures"""
        self.parser = ResponseParser(log_level=logging.CRITICAL)
        self.prompt_manager = PromptTemplateManager()
    
    def test_parsing_performance(self):
        """Test parsing performance with various input sizes"""
        # Test with different response sizes
        test_responses = [
            "Current price: $150.25\nVolume: 1,000,000",  # Small
            "Current price: $150.25\nPercentage change: +2.5%\nVolume: 1,000,000\n" * 10,  # Medium
            "Current price: $150.25\nPercentage change: +2.5%\nVolume: 1,000,000\n" * 100,  # Large
        ]
        
        for i, response in enumerate(test_responses):
            with self.subTest(size=f"size_{i}"):
                start_time = time.time()
                result = self.parser.parse_stock_snapshot(response, "TEST")
                end_time = time.time()
                
                # Should complete quickly (< 1 second even for large inputs)
                self.assertLess(end_time - start_time, 1.0)
                self.assertIsNotNone(result)
    
    def test_prompt_generation_consistency(self):
        """Test prompt generation consistency across multiple calls"""
        prompts = []
        
        # Generate same prompt multiple times
        for _ in range(10):
            prompt, context = self.prompt_manager.generate_prompt(
                PromptType.SNAPSHOT, ticker="AAPL"
            )
            prompts.append(prompt)
        
        # All prompts should be identical
        first_prompt = prompts[0]
        for prompt in prompts[1:]:
            self.assertEqual(prompt, first_prompt)
    
    def test_memory_usage_stability(self):
        """Test that repeated operations don't cause memory leaks"""
        import gc
        
        # Get initial memory state
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Perform many operations
        for i in range(100):
            fsm = StateManager()
            fsm.transition('button_click', button_type='snapshot', ticker=f'TEST{i}')
            
            parser = ResponseParser(log_level=logging.CRITICAL)
            result = parser.parse_stock_snapshot("Current price: $100.00", f"TEST{i}")
            
            # Clean up
            del fsm, parser, result
        
        # Force garbage collection
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Should not have significant memory growth (allow 10% increase)
        growth_ratio = final_objects / initial_objects
        self.assertLess(growth_ratio, 1.1, "Memory usage grew too much")


class TestRealWorldScenarios(unittest.TestCase):
    """Test real-world usage scenarios and edge cases"""
    
    def setUp(self):
        """Set up real-world scenario fixtures"""
        self.fsm_manager = StateManager()
        self.parser = ResponseParser(log_level=logging.CRITICAL)
        self.prompt_manager = PromptTemplateManager()
    
    def test_multi_ticker_conversation(self):
        """Test handling multiple tickers in one conversation"""
        extractor = TickerExtractor()
        
        # Simulate conversation with multiple tickers
        conversation_messages = [
            "Compare AAPL and TSLA performance",
            "Apple looks strong but Tesla is volatile",
            "What's Microsoft's outlook?",
            "NVDA earnings are coming up"
        ]
        
        tickers_found = []
        chat_history = []
        
        for message in conversation_messages:
            # Add to history
            chat_history.append({"role": "user", "content": message})
            
            # Extract ticker
            result = extractor.extract_ticker(message, chat_history)
            if result.symbol != "[TICKER]":  # Not placeholder
                tickers_found.append(result.symbol)
        
        # Should have found multiple valid tickers
        self.assertGreater(len(tickers_found), 2)
        expected_tickers = ["AAPL", "TSLA", "MSFT", "NVDA"]
        for ticker in tickers_found:
            self.assertIn(ticker, expected_tickers)
    
    def test_error_recovery_workflow(self):
        """Test complete error recovery workflow"""
        fsm = StateManager()
        
        # Start normal workflow
        fsm.transition('button_click', button_type='snapshot', ticker='AAPL')
        self.assertEqual(fsm.get_current_state(), AppState.BUTTON_TRIGGERED)
        
        # Simulate error
        fsm._emergency_transition_to_error("Test error")
        self.assertEqual(fsm.get_current_state(), AppState.ERROR)
        
        # Test recovery
        success = fsm.transition('abort')  # Should return to IDLE
        self.assertTrue(success)
        self.assertEqual(fsm.get_current_state(), AppState.IDLE)
        
        # Should be able to start new workflow
        success = fsm.transition('button_click', button_type='technical', ticker='MSFT')
        self.assertTrue(success)
        self.assertEqual(fsm.get_current_state(), AppState.BUTTON_TRIGGERED)
    
    def test_malformed_input_handling(self):
        """Test handling of various malformed inputs"""
        malformed_inputs = [
            "",  # Empty
            "   ",  # Whitespace only
            "🚀📊💎",  # Emojis only
            "a" * 10000,  # Very long
            None,  # None value (would be converted to string)
            "Special chars: @#$%^&*()[]{}|\\:;\"'<>,.?/~`",
        ]
        
        for malformed_input in malformed_inputs:
            with self.subTest(input=str(malformed_input)):
                try:
                    # Test parsing
                    result = self.parser.parse_stock_snapshot(str(malformed_input), "TEST")
                    self.assertIsNotNone(result)
                    
                    # Test ticker extraction
                    extractor = TickerExtractor()
                    ticker_result = extractor.extract_ticker(str(malformed_input))
                    self.assertIsNotNone(ticker_result)
                    
                except Exception as e:
                    self.fail(f"System should handle malformed input gracefully: {e}")
    
    def test_concurrent_operations_simulation(self):
        """Simulate concurrent operations (as much as possible in single thread)"""
        import threading
        
        results = []
        errors = []
        
        def worker(worker_id):
            try:
                # Create isolated components
                parser = ResponseParser(log_level=logging.CRITICAL)
                fsm = StateManager()
                
                # Perform operations
                fsm.transition('button_click', button_type='snapshot', ticker=f'TEST{worker_id}')
                
                sample_response = f"Current price: ${100 + worker_id}.00\nVolume: 1,000,000"
                parse_result = parser.parse_stock_snapshot(sample_response, f"TEST{worker_id}")
                
                results.append({
                    'worker_id': worker_id,
                    'fsm_state': fsm.get_current_state().name,
                    'parse_confidence': parse_result.confidence.value,
                    'parsed_fields': len(parse_result.parsed_data)
                })
                
            except Exception as e:
                errors.append(f"Worker {worker_id}: {e}")
        
        # Create and run threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # Verify results
        self.assertEqual(len(errors), 0, f"Concurrent operations had errors: {errors}")
        self.assertEqual(len(results), 5, "All workers should complete")
        
        # All workers should have processed successfully
        for result in results:
            self.assertIn(result['fsm_state'], ['BUTTON_TRIGGERED', 'IDLE'])
            self.assertGreater(result['parsed_fields'], 0)


def run_comprehensive_tests():
    """Run all integration tests with detailed reporting"""
    
    # Configure logging for tests
    logging.basicConfig(level=logging.WARNING)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestSystemIntegration,
        TestUIIntegration,
        TestPerformanceAndReliability,
        TestRealWorldScenarios
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Generate comprehensive report
    print(f"\n{'='*70}")
    print("📊 COMPREHENSIVE INTEGRATION TEST REPORT")
    print(f"{'='*70}")
    print(f"⏱️  Total Runtime: {end_time - start_time:.2f} seconds")
    print(f"🧪 Tests Run: {result.testsRun}")
    print(f"✅ Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print(f"📈 Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.wasSuccessful():
        print(f"\n🎉 ALL INTEGRATION TESTS PASSED!")
        print(f"✅ System is ready for production deployment")
        print(f"🚀 Phase 5: Integration & Testing - COMPLETE")
    else:
        print(f"\n❌ Some tests failed:")
        
        if result.failures:
            print(f"\n💥 FAILURES ({len(result.failures)}):")
            for test, traceback in result.failures[:3]:  # Show first 3
                print(f"  • {test}: {traceback.split('AssertionError: ')[-1].split('\n')[0] if 'AssertionError: ' in traceback else 'See details above'}")
        
        if result.errors:
            print(f"\n🔥 ERRORS ({len(result.errors)}):")
            for test, traceback in result.errors[:3]:  # Show first 3
                print(f"  • {test}: {traceback.split('Exception: ')[-1].split('\n')[0] if 'Exception: ' in traceback else 'See details above'}")
        
        return False
    
    # Test individual components
    print(f"\n🔍 COMPONENT HEALTH CHECK:")
    try:
        fsm = StateManager()
        print(f"✅ FSM: State = {fsm.get_current_state().name}")
        
        parser = ResponseParser(log_level=logging.CRITICAL)
        stats = parser.get_parsing_statistics()
        print(f"✅ Parser: {stats['total_patterns']} patterns loaded")
        
        prompt_mgr = PromptTemplateManager()
        print(f"✅ Prompts: {len(prompt_mgr.templates)} templates available")
        
        if UI_AVAILABLE:
            print(f"✅ UI: Enhanced interface components loaded")
        else:
            print(f"⚠️  UI: Components not available (expected in test environment)")
            
    except Exception as e:
        print(f"❌ Component check failed: {e}")
        return False
    
    return True


if __name__ == '__main__':
    success = run_comprehensive_tests()
    exit(0 if success else 1)
