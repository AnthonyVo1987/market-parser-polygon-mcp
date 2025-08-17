"""
Integration tests for the complete FSM system
"""

import unittest
import logging
from stock_data_fsm import StateManager, AppState


class TestFSMIntegration(unittest.TestCase):
    """Test complete FSM integration scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = StateManager(session_id='integration-test')
        # Reduce logging noise in tests
        logging.getLogger('stock_fsm.integration-test').setLevel(logging.CRITICAL)
    
    def test_full_snapshot_workflow(self):
        """Test complete snapshot data request workflow"""
        # Simulate user clicking snapshot button
        success = self.manager.transition('button_click', 
                                        button_type='snapshot', 
                                        ticker='AAPL')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.BUTTON_TRIGGERED)
        
        # Simulate prompt preparation
        success = self.manager.transition('prepare_prompt')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.PROMPT_PREPARING)
        
        # Check that prompt was generated
        self.assertIsNotNone(self.manager.context.prompt)
        self.assertIn('AAPL', self.manager.context.prompt)
        
        # Simulate prompt ready
        success = self.manager.transition('prompt_ready')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.AI_PROCESSING)
        
        # Simulate AI response
        mock_response = """
        AAPL Stock Snapshot:
        Current price: $175.25
        Percentage change: +2.5%
        $ Change: +$4.32
        Volume: 52,847,900
        VWAP: $174.80
        Open: $172.15
        High: $176.00
        Low: $171.90
        Close: $175.25
        """
        
        success = self.manager.transition('response_received', 
                                        ai_response=mock_response)
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.RESPONSE_RECEIVED)
        
        # Simulate text parsing (bypassing JSON workflow for this text response)
        success = self.manager.transition('parse_text')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.PARSING_RESPONSE)
        
        # Simulate successful parsing
        parsed_data = {
            'current_price': '175.25',
            'percentage_change': '+2.5%',
            'dollar_change': '+4.32',
            'volume': '52,847,900',
            'vwap': '174.80'
        }
        
        success = self.manager.transition('parse_success', parsed_data=parsed_data)
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.UPDATING_UI)
        
        # Check that parsed data is stored
        self.assertIn('current_price', self.manager.context.parsed_data)
        
        # Simulate UI update completion
        success = self.manager.transition('update_complete')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
        
        # Check final state
        self.assertEqual(len(self.manager.context.transition_history), 7)
        self.assertIsNone(self.manager.context.error_message)
    
    def test_support_resistance_workflow_with_parse_failure(self):
        """Test support/resistance workflow with parse failure fallback"""
        # Start workflow
        self.manager.transition('button_click', 
                               button_type='support_resistance', 
                               ticker='TSLA')
        self.manager.transition('prepare_prompt')
        self.manager.transition('prompt_ready')
        
        # Simulate AI response that's hard to parse
        mock_response = "The stock has some support and resistance, maybe around various levels."
        
        self.manager.transition('response_received', ai_response=mock_response)
        self.manager.transition('parse_text')
        
        # Simulate parse failure (fallback to raw display)
        success = self.manager.transition('parse_failed')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.UPDATING_UI)
        
        # Should have raw response as fallback
        self.assertIn('raw_response', self.manager.context.parsed_data)
        self.assertTrue(self.manager.context.parsed_data.get('parse_fallback', False))
        
        # Complete workflow
        self.manager.transition('update_complete')
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
    
    def test_technical_analysis_with_ai_error(self):
        """Test technical analysis workflow with AI error"""
        # Start workflow
        self.manager.transition('button_click', 
                               button_type='technical', 
                               ticker='NVDA')
        self.manager.transition('prepare_prompt')
        self.manager.transition('prompt_ready')
        
        # Simulate AI error
        success = self.manager.transition('ai_error', 
                                        error='API rate limit exceeded')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.ERROR)
        
        # Check error details
        self.assertIn('rate limit', self.manager.context.error_message)
        self.assertEqual(self.manager.context.error_recovery_attempts, 1)
        
        # Test recovery
        success = self.manager.recover_from_error('retry')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
    
    def test_multiple_error_recovery_attempts(self):
        """Test multiple error recovery attempts"""
        # Force into error state multiple times
        for attempt in range(1, 4):
            self.manager.context.current_state = AppState.ERROR
            self.manager.context.error_recovery_attempts = attempt
            
            # Should be able to retry
            can_retry = self.manager.can_transition('retry')
            self.assertTrue(can_retry, f"Should be able to retry on attempt {attempt}")
            
            success = self.manager.transition('retry')
            self.assertTrue(success)
        
        # After too many attempts, retry should fail
        self.manager.context.current_state = AppState.ERROR
        self.manager.context.error_recovery_attempts = 5
        
        can_retry = self.manager.can_transition('retry')
        self.assertFalse(can_retry)
    
    def test_concurrent_session_isolation(self):
        """Test that multiple StateManager instances are isolated"""
        manager1 = StateManager(session_id='session-1')
        manager2 = StateManager(session_id='session-2')
        
        # Different operations on each manager
        manager1.transition('button_click', button_type='snapshot', ticker='AAPL')
        manager2.transition('button_click', button_type='technical', ticker='TSLA')
        
        # States should be independent
        self.assertEqual(manager1.context.ticker, 'AAPL')
        self.assertEqual(manager1.context.button_type, 'snapshot')
        
        self.assertEqual(manager2.context.ticker, 'TSLA')
        self.assertEqual(manager2.context.button_type, 'technical')
        
        # Histories should be independent
        self.assertEqual(len(manager1.context.transition_history), 1)
        self.assertEqual(len(manager2.context.transition_history), 1)
        
        # Session IDs should be different
        self.assertNotEqual(manager1.session_id, manager2.session_id)
    
    def test_regular_chat_mixed_with_button_requests(self):
        """Test mixing regular chat with button requests"""
        # Start with regular chat (should stay in IDLE)
        success = self.manager.transition('user_chat', 
                                        message='What is the current market trend?')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
        
        # Another regular chat
        success = self.manager.transition('user_chat', 
                                        message='Tell me about AI stocks')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
        
        # Now a button request should work
        success = self.manager.transition('button_click', 
                                        button_type='snapshot', 
                                        ticker='NVDA')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.BUTTON_TRIGGERED)
        
        # Complete the button workflow quickly
        self.manager.transition('prepare_prompt')
        self.manager.transition('prompt_ready')
        self.manager.transition('response_received', ai_response='Mock response')
        self.manager.transition('parse_text')
        self.manager.transition('parse_success', parsed_data={'price': 100})
        self.manager.transition('update_complete')
        
        # Should be back to IDLE and ready for more chat
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
        
        success = self.manager.transition('user_chat', 
                                        message='Thanks for the data!')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
    
    def test_emergency_situations(self):
        """Test emergency reset scenarios"""
        # Start a workflow
        self.manager.transition('button_click', button_type='snapshot')
        self.manager.transition('prepare_prompt')
        
        # Simulate emergency reset from middle of workflow
        success = self.manager.transition('emergency_reset')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
        
        # Should be able to start fresh workflow
        success = self.manager.transition('button_click', 
                                        button_type='technical', 
                                        ticker='AMD')
        self.assertTrue(success)
        self.assertEqual(self.manager.context.button_type, 'technical')
        self.assertEqual(self.manager.context.ticker, 'AMD')
    
    def test_fsm_health_monitoring(self):
        """Test FSM health monitoring throughout workflows"""
        # Check initial health
        health = self.manager.validate_fsm_health()
        self.assertTrue(health['fsm_validation']['validation_passed'])
        self.assertFalse(health['context_health']['has_errors'])
        
        # Run a successful workflow
        self.manager.transition('button_click', button_type='snapshot')
        self.manager.transition('prepare_prompt')
        
        # Check health mid-workflow
        health = self.manager.validate_fsm_health()
        self.assertEqual(health['context_health']['current_state'], 'PROMPT_PREPARING')
        self.assertFalse(health['context_health']['has_errors'])
        
        # Force an error
        self.manager.context.current_state = AppState.ERROR
        self.manager.context.error_message = 'Test error'
        
        # Check health in error state
        health = self.manager.validate_fsm_health()
        self.assertTrue(health['context_health']['has_errors'])
        self.assertEqual(health['context_health']['current_state'], 'ERROR')
    
    def test_performance_with_many_transitions(self):
        """Test performance with many state transitions"""
        import time
        
        start_time = time.time()
        
        # Perform many transitions
        for i in range(100):
            self.manager.transition('user_chat', message=f'Message {i}')
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should complete quickly (less than 1 second for 100 transitions)
        self.assertLess(elapsed, 1.0, "FSM performance issue: too slow")
        
        # Check statistics
        stats = self.manager.get_statistics()
        self.assertEqual(stats['total_transitions'], 100)
        self.assertEqual(stats['successful_transitions'], 100)
        self.assertEqual(stats['failed_transitions'], 0)
    
    def test_serialization_round_trip(self):
        """Test full serialization and deserialization"""
        # Set up manager with complex state
        self.manager.transition('button_click', button_type='snapshot', ticker='AAPL')
        self.manager.transition('prepare_prompt')
        
        # Add some parsed data
        self.manager.context.parsed_data = {
            'price': 175.25,
            'volume': 1000000,
            'metadata': {'source': 'test', 'timestamp': 1234567890}
        }
        
        # Serialize
        state = self.manager.__getstate__()
        
        # Create new manager and deserialize
        new_manager = StateManager()
        new_manager.__setstate__(state)
        
        # Verify everything is preserved
        self.assertEqual(new_manager.get_current_state(), AppState.PROMPT_PREPARING)
        self.assertEqual(new_manager.context.button_type, 'snapshot')
        self.assertEqual(new_manager.context.ticker, 'AAPL')
        self.assertEqual(new_manager.context.parsed_data['price'], 175.25)
        
        # Should be able to continue workflow
        success = new_manager.transition('prompt_ready')
        self.assertTrue(success)
        self.assertEqual(new_manager.get_current_state(), AppState.AI_PROCESSING)


if __name__ == '__main__':
    unittest.main()
