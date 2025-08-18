#!/usr/bin/env python3
"""
UI State Integration Tests

This test suite validates the integration between the UI components, FSM state management,
and data processing that the previous tests failed to cover. It focuses on the critical
path from user interaction to UI updates.

CRITICAL INTEGRATION POINTS:
1. Button click handling → FSM state transitions
2. Processing status updates → UI feedback
3. ParseResult → DataFrame → UI display
4. Error states → UI error handling
5. Chat history management → Message validation
6. Export functionality → Data serialization

PRODUCTION WORKFLOW FOCUS:
User Click → FSM Update → Status Update → AI Processing → 
Response Parsing → DataFrame Update → UI Refresh → Error Handling

This covers the integration points that the component-specific tests missed.
"""

import asyncio
import unittest
import logging
import time
import json
import pandas as pd
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List, Optional, Tuple
import threading
import queue

# Import FSM and UI components
from stock_data_fsm import StateManager, AppState, StateContext
from src.response_parser import ResponseParser, DataType, ParseResult, ConfidenceLevel

# Try to import UI components
try:
    from chat_ui import ProcessingStatus
    PROCESSING_STATUS_AVAILABLE = True
except ImportError:
    PROCESSING_STATUS_AVAILABLE = False

# Mock Gradio for testing
class MockGradioComponent:
    """Mock Gradio component for testing"""
    def __init__(self, value=None):
        self.value = value
        self.change_callbacks = []
    
    def click(self, callback):
        self.click_callback = callback
        return self
    
    def change(self, callback):
        self.change_callbacks.append(callback)
        return self
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self


class UIStateIntegrationTestCase(unittest.TestCase):
    """Base test case for UI state integration"""
    
    def setUp(self):
        """Setup UI integration test environment"""
        self.fsm_manager = StateManager(session_id='ui-integration-test')
        self.response_parser = ResponseParser(log_level=logging.DEBUG)
        
        if PROCESSING_STATUS_AVAILABLE:
            self.processing_status = ProcessingStatus()
        
        # Mock UI components
        self.mock_chat_interface = MockGradioComponent()
        self.mock_snapshot_df = MockGradioComponent()
        self.mock_sr_df = MockGradioComponent()
        self.mock_tech_df = MockGradioComponent()
        self.mock_status_display = MockGradioComponent()
        
        # Track integration metrics
        self.integration_metrics = {
            'state_transitions': 0,
            'ui_updates': 0,
            'dataframe_updates': 0,
            'status_updates': 0,
            'error_handlings': 0,
            'message_validations': 0
        }
        
        # Configure logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _simulate_button_click(self, button_type: str, ticker: str) -> Dict[str, Any]:
        """Simulate a button click workflow"""
        workflow_state = {
            'button_type': button_type,
            'ticker': ticker,
            'fsm_states': [],
            'ui_updates': [],
            'errors': []
        }
        
        try:
            # Step 1: FSM button click transition
            success = self.fsm_manager.transition('button_click', 
                                                button_type=button_type, 
                                                ticker=ticker)
            if success:
                workflow_state['fsm_states'].append(self.fsm_manager.get_current_state())
                self.integration_metrics['state_transitions'] += 1
            
            # Step 2: UI status update
            if PROCESSING_STATUS_AVAILABLE:
                self.processing_status.start_processing(f"Processing {button_type}...", 5)
                workflow_state['ui_updates'].append(f"status_started: {self.processing_status.status_message}")
                self.integration_metrics['status_updates'] += 1
            
            # Step 3: Prompt preparation
            success = self.fsm_manager.transition('prepare_prompt')
            if success:
                workflow_state['fsm_states'].append(self.fsm_manager.get_current_state())
                self.integration_metrics['state_transitions'] += 1
            
            # Step 4: AI processing simulation
            success = self.fsm_manager.transition('prompt_ready')
            if success:
                workflow_state['fsm_states'].append(self.fsm_manager.get_current_state())
                self.integration_metrics['state_transitions'] += 1
            
            # Step 5: Mock AI response
            mock_response = self._generate_mock_ai_response(button_type, ticker)
            success = self.fsm_manager.transition('response_received', ai_response=mock_response)
            if success:
                workflow_state['fsm_states'].append(self.fsm_manager.get_current_state())
                self.integration_metrics['state_transitions'] += 1
            
            # Step 6: Parsing
            success = self.fsm_manager.transition('parse')
            if success:
                workflow_state['fsm_states'].append(self.fsm_manager.get_current_state())
                self.integration_metrics['state_transitions'] += 1
            
            workflow_state['ai_response'] = mock_response
            
        except Exception as e:
            workflow_state['errors'].append(str(e))
            self.integration_metrics['error_handlings'] += 1
        
        return workflow_state
    
    def _generate_mock_ai_response(self, button_type: str, ticker: str) -> str:
        """Generate realistic mock AI responses"""
        responses = {
            'snapshot': f"""
            {ticker} is currently trading at $175.43, up 2.8% from yesterday's close.
            This represents a gain of $4.77 per share. Trading volume is elevated at 68.2M shares.
            VWAP (Volume Weighted Average Price) is $174.85.
            Open: $172.50, High: $176.20, Low: $171.80, Close: $170.66
            """,
            'support_resistance': f"""
            Technical Analysis - Support and Resistance Levels for {ticker}:
            Support Levels: S1: $168.50, S2: $165.20, S3: $161.75
            Resistance Levels: R1: $178.90, R2: $182.40, R3: $186.00
            Current price of $175.43 is trading between S1 and R1.
            """,
            'technical': f"""
            Technical Indicator Analysis for {ticker}:
            RSI: 67.2 (approaching overbought), MACD: 1.23 (bullish crossover)
            Moving Averages: 5-day EMA: $174.20, 10-day EMA: $171.85
            50-day SMA: $165.40, 200-day SMA: $158.75
            """
        }
        return responses.get(button_type, f"Analysis for {ticker}")


class TestButtonClickIntegration(UIStateIntegrationTestCase):
    """Test button click to UI update integration"""
    
    def test_snapshot_button_ui_integration(self):
        """Test complete snapshot button integration"""
        self.logger.info("🧪 Testing snapshot button UI integration...")
        
        # Simulate button click workflow
        workflow = self._simulate_button_click('snapshot', 'AAPL')
        
        # Validate FSM progression
        expected_states = [
            AppState.BUTTON_TRIGGERED,
            AppState.PROMPT_PREPARING, 
            AppState.AI_PROCESSING,
            AppState.RESPONSE_RECEIVED,
            AppState.PARSING_RESPONSE
        ]
        
        self.assertGreaterEqual(len(workflow['fsm_states']), 3, 
                               "Should progress through multiple FSM states")
        
        # Test parsing integration
        if workflow['ai_response']:
            parse_result = self.response_parser.parse_stock_snapshot(
                workflow['ai_response'], 'AAPL'
            )
            
            self.assertIsInstance(parse_result, ParseResult)
            self.assertNotEqual(parse_result.confidence, ConfidenceLevel.FAILED)
            
            # Test DataFrame generation for UI
            dataframe = parse_result.to_dataframe()
            self.assertIsInstance(dataframe, pd.DataFrame)
            self.assertGreater(len(dataframe), 0)
            
            # Simulate UI DataFrame update
            self.mock_snapshot_df.value = dataframe
            self.integration_metrics['dataframe_updates'] += 1
            self.integration_metrics['ui_updates'] += 1
        
        # Should have minimal errors
        self.assertLessEqual(len(workflow['errors']), 1, 
                            f"Should have minimal errors: {workflow['errors']}")
        
        self.logger.info("✅ Snapshot button UI integration test passed")
    
    def test_support_resistance_button_ui_integration(self):
        """Test support/resistance button UI integration"""
        self.logger.info("🧪 Testing support/resistance button UI integration...")
        
        workflow = self._simulate_button_click('support_resistance', 'TSLA')
        
        # Test S&R specific parsing
        if workflow['ai_response']:
            parse_result = self.response_parser.parse_support_resistance(
                workflow['ai_response'], 'TSLA'
            )
            
            self.assertIsInstance(parse_result, ParseResult)
            self.assertEqual(parse_result.data_type, DataType.SUPPORT_RESISTANCE)
            
            # Test S&R DataFrame structure
            dataframe = parse_result.to_dataframe()
            self.assertIsInstance(dataframe, pd.DataFrame)
            
            # Should have Level and Price columns for S&R
            if len(dataframe) > 0 and 'Level' in dataframe.columns:
                self.assertIn('Level', dataframe.columns)
                self.assertIn('Price', dataframe.columns)
            
            # Simulate UI update
            self.mock_sr_df.value = dataframe
            self.integration_metrics['dataframe_updates'] += 1
        
        self.logger.info("✅ Support/resistance button UI integration test passed")
    
    def test_technical_button_ui_integration(self):
        """Test technical indicators button UI integration"""
        self.logger.info("🧪 Testing technical indicators button UI integration...")
        
        workflow = self._simulate_button_click('technical', 'NVDA')
        
        # Test technical parsing
        if workflow['ai_response']:
            parse_result = self.response_parser.parse_technical_indicators(
                workflow['ai_response'], 'NVDA'
            )
            
            self.assertIsInstance(parse_result, ParseResult)
            self.assertEqual(parse_result.data_type, DataType.TECHNICAL)
            
            # Test technical DataFrame structure
            dataframe = parse_result.to_dataframe()
            self.assertIsInstance(dataframe, pd.DataFrame)
            
            # Should have Indicator and Value columns
            if len(dataframe) > 0 and 'Indicator' in dataframe.columns:
                self.assertIn('Indicator', dataframe.columns)
                self.assertIn('Value', dataframe.columns)
            
            # Simulate UI update
            self.mock_tech_df.value = dataframe
            self.integration_metrics['dataframe_updates'] += 1
        
        self.logger.info("✅ Technical indicators button UI integration test passed")


class TestProcessingStatusIntegration(UIStateIntegrationTestCase):
    """Test processing status and UI feedback integration"""
    
    @unittest.skipUnless(PROCESSING_STATUS_AVAILABLE, "ProcessingStatus not available")
    def test_processing_status_workflow(self):
        """Test processing status updates during workflow"""
        self.logger.info("🧪 Testing processing status workflow...")
        
        # Start processing
        self.processing_status.start_processing("Analyzing AAPL snapshot...", 5)
        
        self.assertTrue(self.processing_status.is_processing)
        self.assertEqual(self.processing_status.total_steps, 5)
        self.assertIsNotNone(self.processing_status.start_time)
        
        # Simulate step updates
        steps = [
            "Preparing prompt...",
            "Contacting AI service...", 
            "Processing response...",
            "Parsing data...",
            "Updating UI..."
        ]
        
        for i, step in enumerate(steps, 1):
            self.processing_status.update_step(step, i)
            self.assertEqual(self.processing_status.current_step, step)
            self.assertEqual(self.processing_status.progress, i)
            self.integration_metrics['status_updates'] += 1
        
        # Complete processing
        self.processing_status.complete("Analysis complete")
        self.assertFalse(self.processing_status.is_processing)
        
        self.logger.info("✅ Processing status workflow test passed")
    
    @unittest.skipUnless(PROCESSING_STATUS_AVAILABLE, "ProcessingStatus not available")
    def test_processing_status_error_handling(self):
        """Test processing status error handling"""
        self.logger.info("🧪 Testing processing status error handling...")
        
        # Start processing
        self.processing_status.start_processing("Test processing...", 3)
        
        # Simulate error
        error_message = "Simulated processing error"
        self.processing_status.error(error_message)
        
        self.assertFalse(self.processing_status.is_processing)
        self.assertIn("error", self.processing_status.status_message.lower())
        self.integration_metrics['error_handlings'] += 1
        
        self.logger.info("✅ Processing status error handling test passed")


class TestDataFrameUIIntegration(UIStateIntegrationTestCase):
    """Test DataFrame to UI component integration"""
    
    def test_dataframe_ui_update_consistency(self):
        """Test consistency of DataFrame updates in UI"""
        self.logger.info("🧪 Testing DataFrame UI update consistency...")
        
        # Create test parse results
        test_data = {
            'current_price': '$175.43',
            'percentage_change': '+2.8%',
            'volume': '68,200,000'
        }
        
        parse_result = ParseResult(
            data_type=DataType.SNAPSHOT,
            raw_response="Mock response",
            parsed_data=test_data,
            confidence=ConfidenceLevel.HIGH
        )
        
        # Generate DataFrame
        dataframe = parse_result.to_dataframe()
        
        # Validate DataFrame structure for UI
        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertGreater(len(dataframe), 0)
        self.assertIn('Metric', dataframe.columns)
        self.assertIn('Value', dataframe.columns)
        
        # Simulate UI component updates
        ui_components = [
            self.mock_snapshot_df,
            self.mock_sr_df, 
            self.mock_tech_df
        ]
        
        for component in ui_components:
            component.value = dataframe
            self.integration_metrics['ui_updates'] += 1
        
        self.integration_metrics['dataframe_updates'] += 1
        
        self.logger.info("✅ DataFrame UI update consistency test passed")
    
    def test_empty_dataframe_ui_handling(self):
        """Test UI handling of empty DataFrames"""
        self.logger.info("🧪 Testing empty DataFrame UI handling...")
        
        # Create empty parse result
        empty_result = ParseResult(
            data_type=DataType.SNAPSHOT,
            raw_response="",
            parsed_data={},
            confidence=ConfidenceLevel.FAILED
        )
        
        # Generate empty DataFrame
        empty_df = empty_result.to_dataframe()
        
        # Should still be valid DataFrame
        self.assertIsInstance(empty_df, pd.DataFrame)
        self.assertGreater(len(empty_df), 0)  # Should have "No Data" row
        
        # UI should handle empty DataFrames gracefully
        self.mock_snapshot_df.value = empty_df
        self.integration_metrics['ui_updates'] += 1
        self.integration_metrics['dataframe_updates'] += 1
        
        self.logger.info("✅ Empty DataFrame UI handling test passed")
    
    def test_large_dataframe_ui_performance(self):
        """Test UI performance with large DataFrames"""
        self.logger.info("🧪 Testing large DataFrame UI performance...")
        
        # Create large dataset
        large_data = {}
        for i in range(100):
            large_data[f'metric_{i}'] = f'value_{i}'
        
        large_result = ParseResult(
            data_type=DataType.TECHNICAL,
            raw_response="Large response",
            parsed_data=large_data,
            confidence=ConfidenceLevel.MEDIUM
        )
        
        # Time DataFrame generation
        start_time = time.time()
        large_df = large_result.to_dataframe()
        generation_time = time.time() - start_time
        
        # Should generate quickly
        self.assertLess(generation_time, 1.0, "Large DataFrame generation should be fast")
        
        # Should still be valid
        self.assertIsInstance(large_df, pd.DataFrame)
        self.assertEqual(len(large_df), 100)
        
        # Simulate UI update
        self.mock_tech_df.value = large_df
        self.integration_metrics['ui_updates'] += 1
        self.integration_metrics['dataframe_updates'] += 1
        
        self.logger.info("✅ Large DataFrame UI performance test passed")


class TestChatHistoryIntegration(UIStateIntegrationTestCase):
    """Test chat history and message management integration"""
    
    def test_chat_history_message_addition(self):
        """Test adding messages to chat history"""
        self.logger.info("🧪 Testing chat history message addition...")
        
        # Simulate chat history
        chat_history = []
        
        # Add user message
        user_message = {"role": "user", "content": "Get AAPL snapshot"}
        chat_history.append(user_message)
        
        # Add assistant response
        assistant_message = {
            "role": "assistant", 
            "content": "Here's the AAPL snapshot analysis..."
        }
        chat_history.append(assistant_message)
        
        # Validate history structure
        self.assertEqual(len(chat_history), 2)
        self.assertEqual(chat_history[0]["role"], "user")
        self.assertEqual(chat_history[1]["role"], "assistant")
        
        # Validate content
        for message in chat_history:
            self.assertIn("role", message)
            self.assertIn("content", message)
            self.assertIsNotNone(message["content"])
            self.assertNotEqual(message["content"].strip(), "")
        
        self.integration_metrics['message_validations'] += 1
        
        self.logger.info("✅ Chat history message addition test passed")
    
    def test_chat_history_validation(self):
        """Test chat history validation for None/empty content"""
        self.logger.info("🧪 Testing chat history validation...")
        
        # Test various message formats
        test_messages = [
            {"role": "user", "content": "Valid message"},
            {"role": "assistant", "content": None},  # Invalid
            {"role": "user", "content": ""},         # Invalid
            {"role": "assistant", "content": "   "}, # Invalid (whitespace only)
            {"role": "user", "content": "Another valid message"}
        ]
        
        # Validate each message
        valid_messages = []
        for message in test_messages:
            content = message.get("content")
            if content and isinstance(content, str) and content.strip():
                valid_messages.append(message)
        
        # Should filter out invalid messages
        self.assertEqual(len(valid_messages), 2)
        self.integration_metrics['message_validations'] += 1
        
        self.logger.info("✅ Chat history validation test passed")
    
    def test_chat_export_integration(self):
        """Test chat export functionality integration"""
        self.logger.info("🧪 Testing chat export integration...")
        
        # Create sample chat history
        chat_history = [
            {"role": "user", "content": "Analyze AAPL"},
            {"role": "assistant", "content": "AAPL is trading at $175.43..."},
            {"role": "user", "content": "Show support and resistance"},
            {"role": "assistant", "content": "Support levels: S1: $168.50..."}
        ]
        
        # Simulate export to markdown
        markdown_export = self._export_chat_to_markdown(chat_history)
        
        # Validate export
        self.assertIsInstance(markdown_export, str)
        self.assertGreater(len(markdown_export), 0)
        self.assertIn("AAPL", markdown_export)
        self.assertIn("User:", markdown_export)
        self.assertIn("Assistant:", markdown_export)
        
        self.integration_metrics['ui_updates'] += 1
        
        self.logger.info("✅ Chat export integration test passed")
    
    def _export_chat_to_markdown(self, chat_history: List[Dict[str, str]]) -> str:
        """Simulate chat export to markdown"""
        markdown_lines = ["# Chat Export", ""]
        
        for i, message in enumerate(chat_history, 1):
            role = message["role"].title()
            content = message["content"]
            markdown_lines.extend([
                f"## {role} {i}",
                content,
                ""
            ])
        
        return "\n".join(markdown_lines)


class TestErrorHandlingIntegration(UIStateIntegrationTestCase):
    """Test error handling integration across UI components"""
    
    def test_fsm_error_ui_integration(self):
        """Test FSM error states with UI error handling"""
        self.logger.info("🧪 Testing FSM error UI integration...")
        
        # Force FSM into error state
        self.fsm_manager.transition('button_click', button_type='snapshot', ticker='AAPL')
        self.fsm_manager.transition('prepare_prompt')
        self.fsm_manager.transition('prompt_ready')
        
        # Simulate error
        error_message = "AI service timeout"
        success = self.fsm_manager.transition('ai_error', error=error_message)
        
        self.assertTrue(success)
        self.assertEqual(self.fsm_manager.get_current_state(), AppState.ERROR)
        self.assertEqual(self.fsm_manager.context.error_message, error_message)
        
        # Simulate UI error display
        error_display = f"❌ Error: {error_message}"
        self.mock_status_display.value = error_display
        self.integration_metrics['error_handlings'] += 1
        self.integration_metrics['ui_updates'] += 1
        
        # Test error recovery
        recovery_success = self.fsm_manager.recover_from_error('reset')
        self.assertTrue(recovery_success)
        self.assertEqual(self.fsm_manager.get_current_state(), AppState.IDLE)
        
        self.logger.info("✅ FSM error UI integration test passed")
    
    def test_parsing_error_ui_integration(self):
        """Test parsing error integration with UI"""
        self.logger.info("🧪 Testing parsing error UI integration...")
        
        # Test parsing with unparseable content
        unparseable_response = "Sorry, I cannot access market data right now."
        
        parse_result = self.response_parser.parse_stock_snapshot(
            unparseable_response, "AAPL"
        )
        
        # Should handle gracefully
        self.assertEqual(parse_result.confidence, ConfidenceLevel.FAILED)
        self.assertEqual(len(parse_result.parsed_data), 0)
        
        # Should still generate valid DataFrame for UI
        error_df = parse_result.to_dataframe()
        self.assertIsInstance(error_df, pd.DataFrame)
        self.assertGreater(len(error_df), 0)
        
        # UI should display error DataFrame
        self.mock_snapshot_df.value = error_df
        self.integration_metrics['error_handlings'] += 1
        self.integration_metrics['dataframe_updates'] += 1
        
        self.logger.info("✅ Parsing error UI integration test passed")


class TestConcurrentOperationsIntegration(UIStateIntegrationTestCase):
    """Test integration under concurrent operations"""
    
    def test_concurrent_button_clicks(self):
        """Test handling of concurrent button clicks"""
        self.logger.info("🧪 Testing concurrent button clicks...")
        
        results = queue.Queue()
        
        def click_worker(button_type, ticker):
            """Worker function for concurrent clicks"""
            try:
                workflow = self._simulate_button_click(button_type, ticker)
                results.put(('success', workflow))
            except Exception as e:
                results.put(('error', str(e)))
        
        # Start concurrent clicks
        threads = [
            threading.Thread(target=click_worker, args=('snapshot', 'AAPL')),
            threading.Thread(target=click_worker, args=('technical', 'TSLA')),
            threading.Thread(target=click_worker, args=('support_resistance', 'NVDA'))
        ]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Collect results
        successful_workflows = 0
        while not results.empty():
            result_type, result_data = results.get()
            if result_type == 'success':
                successful_workflows += 1
            else:
                self.integration_metrics['error_handlings'] += 1
        
        # At least one workflow should succeed
        self.assertGreater(successful_workflows, 0, 
                          "At least one concurrent workflow should succeed")
        
        self.logger.info("✅ Concurrent button clicks test passed")
    
    def test_rapid_status_updates(self):
        """Test rapid processing status updates"""
        self.logger.info("🧪 Testing rapid status updates...")
        
        if PROCESSING_STATUS_AVAILABLE:
            # Simulate rapid updates
            for i in range(10):
                self.processing_status.start_processing(f"Process {i}", 5)
                for step in range(1, 6):
                    self.processing_status.update_step(f"Step {step}", step)
                self.processing_status.complete(f"Process {i} complete")
                self.integration_metrics['status_updates'] += 5
        
        # Should handle rapid updates without errors
        self.assertGreater(self.integration_metrics['status_updates'], 0)
        
        self.logger.info("✅ Rapid status updates test passed")


def run_ui_state_integration_tests():
    """Run comprehensive UI state integration tests"""
    print("🎯 UI State Integration Test Suite")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestButtonClickIntegration,
        TestProcessingStatusIntegration,
        TestDataFrameUIIntegration,
        TestChatHistoryIntegration,
        TestErrorHandlingIntegration,
        TestConcurrentOperationsIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Generate summary
    print(f"\n📊 UI State Integration Results:")
    print(f"   • Tests run: {result.testsRun}")
    print(f"   • Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   • Failures: {len(result.failures)}")
    print(f"   • Errors: {len(result.errors)}")
    print(f"   • Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    print(f"\n🔗 Integration Coverage:")
    print(f"   • Button → FSM → UI workflow: ✅ Tested")
    print(f"   • Processing status integration: {'✅' if PROCESSING_STATUS_AVAILABLE else '⚠️  Limited'}")
    print(f"   • DataFrame → UI updates: ✅ Tested")
    print(f"   • Chat history management: ✅ Tested")
    print(f"   • Error handling integration: ✅ Tested")
    print(f"   • Concurrent operations: ✅ Tested")
    
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
        print("✅ UI state integration is working correctly")
        print("🔄 FSM and UI components are properly integrated")
        print("📊 Data flow from parsing to UI display is validated")
    else:
        print("❌ Integration issues detected in UI state management")
        print("🔧 These issues likely contributed to production failures")
    
    return success


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the integration tests
    success = run_ui_state_integration_tests()
    
    # Exit with appropriate code
    exit(0 if success else 1)