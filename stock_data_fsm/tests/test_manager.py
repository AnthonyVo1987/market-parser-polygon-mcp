"""
Unit tests for StateManager and integration scenarios
"""

import unittest
import logging
import time
from unittest.mock import Mock, patch
from stock_data_fsm.states import AppState, StateContext
from stock_data_fsm.manager import StateManager, StateActions


class TestStateActions(unittest.TestCase):
    """Test StateActions functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.logger = logging.getLogger('test')
        self.actions = StateActions(self.logger)
        self.context = StateContext()
    
    def test_on_button_clicked(self):
        """Test button click action"""
        self.actions.on_button_clicked(
            self.context, 
            button_type='snapshot', 
            ticker='AAPL'
        )
        
        self.assertEqual(self.context.button_type, 'snapshot')
        self.assertEqual(self.context.ticker, 'AAPL')
        self.assertEqual(self.context.error_recovery_attempts, 0)
    
    def test_on_button_clicked_with_ticker_normalization(self):
        """Test button click action with ticker normalization"""
        self.actions.on_button_clicked(
            self.context, 
            button_type='technical', 
            ticker='  aapl  '
        )
        
        self.assertEqual(self.context.button_type, 'technical')
        self.assertEqual(self.context.ticker, 'AAPL')  # Should be normalized
    
    def test_on_prepare_prompt_snapshot(self):
        """Test prompt preparation for snapshot"""
        self.context.button_type = 'snapshot'
        self.context.ticker = 'AAPL'
        
        self.actions.on_prepare_prompt(self.context)
        
        self.assertIsNotNone(self.context.prompt)
        self.assertIn('AAPL', self.context.prompt)
        self.assertIn('stock snapshot', self.context.prompt.lower())
    
    def test_on_prepare_prompt_support_resistance(self):
        """Test prompt preparation for support/resistance"""
        self.context.button_type = 'support_resistance'
        self.context.ticker = 'TSLA'
        
        self.actions.on_prepare_prompt(self.context)
        
        self.assertIsNotNone(self.context.prompt)
        self.assertIn('TSLA', self.context.prompt)
        self.assertIn('support', self.context.prompt.lower())
        self.assertIn('resistance', self.context.prompt.lower())
    
    def test_on_prepare_prompt_technical(self):
        """Test prompt preparation for technical analysis"""
        self.context.button_type = 'technical'
        self.context.ticker = 'NVDA'
        
        self.actions.on_prepare_prompt(self.context)
        
        self.assertIsNotNone(self.context.prompt)
        self.assertIn('NVDA', self.context.prompt)
        self.assertIn('RSI', self.context.prompt)
        self.assertIn('MACD', self.context.prompt)
    
    def test_on_prepare_prompt_invalid_type(self):
        """Test prompt preparation with invalid button type"""
        self.context.button_type = 'invalid'
        
        with self.assertRaises(ValueError):
            self.actions.on_prepare_prompt(self.context)
    
    def test_on_prepare_prompt_no_type(self):
        """Test prompt preparation with no button type"""
        self.context.button_type = None
        
        with self.assertRaises(ValueError):
            self.actions.on_prepare_prompt(self.context)
    
    def test_on_response_received(self):
        """Test AI response received action"""
        self.context.parsed_data['ai_start_time'] = time.time() - 1.5
        
        self.actions.on_response_received(
            self.context,
            ai_response="Mock AI response content"
        )
        
        self.assertEqual(self.context.ai_response, "Mock AI response content")
        self.assertIn('ai_processing_time', self.context.parsed_data)
        self.assertGreater(self.context.parsed_data['ai_processing_time'], 1.0)
    
    def test_on_parse_success(self):
        """Test successful parsing action"""
        self.context.parsed_data['parse_start_time'] = time.time() - 0.5
        
        parsed_data = {'price': 150.0, 'volume': 1000000}
        self.actions.on_parse_success(self.context, parsed_data=parsed_data)
        
        self.assertIn('price', self.context.parsed_data)
        self.assertIn('volume', self.context.parsed_data)
        self.assertIn('parse_time', self.context.parsed_data)
        self.assertEqual(self.context.parsed_data['price'], 150.0)
    
    def test_on_parse_failed_fallback(self):
        """Test parse failure fallback action"""
        self.context.ai_response = "Raw AI response"
        
        self.actions.on_parse_failed_fallback(self.context)
        
        self.assertEqual(self.context.parsed_data['raw_response'], "Raw AI response")
        self.assertTrue(self.context.parsed_data['parse_fallback'])
    
    def test_error_handling_actions(self):
        """Test various error handling actions"""
        # Test error occurred
        self.actions.on_error_occurred(self.context, error="Test error")
        self.assertEqual(self.context.error_message, "Test error")
        self.assertEqual(self.context.error_recovery_attempts, 1)
        
        # Test retry from error
        self.actions.on_retry_from_error(self.context)
        self.assertIsNone(self.context.error_message)
        self.assertEqual(self.context.error_recovery_attempts, 0)
    
    def test_clear_data_actions(self):
        """Test data clearing actions"""
        # Set up context with data
        self.context.button_type = 'snapshot'
        self.context.ticker = 'AAPL'
        self.context.prompt = 'Test prompt'
        
        # Test reset context
        self.actions.on_reset_context(self.context)
        
        self.assertIsNone(self.context.button_type)
        self.assertIsNone(self.context.ticker)
        self.assertIsNone(self.context.prompt)
        self.assertEqual(len(self.context.transition_history), 0)


class TestStateManager(unittest.TestCase):
    """Test StateManager functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = StateManager(session_id='test-session')
    
    def test_initialization(self):
        """Test StateManager initialization"""
        self.assertEqual(self.manager.session_id, 'test-session')
        self.assertEqual(self.manager.context.current_state, AppState.IDLE)
        self.assertIsNotNone(self.manager.logger)
        self.assertIsNotNone(self.manager.transitions)
        self.assertIsNotNone(self.manager.actions)
    
    def test_get_current_state(self):
        """Test getting current state"""
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
        
        self.manager.context.current_state = AppState.BUTTON_TRIGGERED
        self.assertEqual(self.manager.get_current_state(), AppState.BUTTON_TRIGGERED)
    
    def test_is_in_state(self):
        """Test state checking"""
        self.assertTrue(self.manager.is_in_state(AppState.IDLE))
        self.assertFalse(self.manager.is_in_state(AppState.ERROR))
    
    def test_valid_transition(self):
        """Test valid state transition"""
        # Test successful button click transition
        success = self.manager.transition('button_click', button_type='snapshot')
        
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.BUTTON_TRIGGERED)
        self.assertEqual(self.manager.context.button_type, 'snapshot')
        self.assertEqual(len(self.manager.context.transition_history), 1)
    
    def test_invalid_transition(self):
        """Test invalid state transition"""
        # Try invalid event from IDLE
        success = self.manager.transition('invalid_event')
        
        self.assertFalse(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
        self.assertEqual(len(self.manager.context.transition_history), 0)
    
    def test_transition_with_guard_failure(self):
        """Test transition with failing guard"""
        # Try button click with invalid button type
        success = self.manager.transition('button_click', button_type='invalid')
        
        self.assertFalse(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
    
    def test_complete_successful_workflow(self):
        """Test complete successful button workflow"""
        # Step 1: Button click
        success = self.manager.transition('button_click', button_type='snapshot', ticker='AAPL')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.BUTTON_TRIGGERED)
        
        # Step 2: Prepare prompt
        success = self.manager.transition('prepare_prompt')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.PROMPT_PREPARING)
        
        # Step 3: Prompt ready
        success = self.manager.transition('prompt_ready')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.AI_PROCESSING)
        
        # Step 4: Response received
        success = self.manager.transition('response_received', 
                                        ai_response='Mock AI response')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.RESPONSE_RECEIVED)
        
        # Step 5: Parse response
        success = self.manager.transition('parse')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.PARSING_RESPONSE)
        
        # Step 6: Parse success
        success = self.manager.transition('parse_success', 
                                        parsed_data={'price': 150.0})
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.UPDATING_UI)
        
        # Step 7: Update complete
        success = self.manager.transition('update_complete')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
        
        # Check that we have full history
        self.assertEqual(len(self.manager.context.transition_history), 7)
    
    def test_error_recovery_workflow(self):
        """Test error recovery workflow"""
        # Force into error state
        self.manager.context.current_state = AppState.ERROR
        self.manager.context.error_message = "Test error"
        self.manager.context.error_recovery_attempts = 1
        
        # Test retry recovery
        success = self.manager.recover_from_error('retry')
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
    
    def test_error_recovery_max_attempts(self):
        """Test error recovery with max attempts exceeded"""
        # Set up error state with max attempts
        self.manager.context.current_state = AppState.ERROR
        self.manager.context.error_recovery_attempts = 5
        
        # Retry should fail due to max attempts
        success = self.manager.recover_from_error('retry')
        self.assertFalse(success)
        self.assertEqual(self.manager.get_current_state(), AppState.ERROR)
    
    def test_can_transition(self):
        """Test transition validation"""
        # From IDLE, button_click should be possible with valid button_type
        self.assertTrue(self.manager.can_transition('button_click', button_type='snapshot'))
        
        # From IDLE, button_click with invalid button_type should not be possible
        self.assertFalse(self.manager.can_transition('button_click', button_type='invalid'))
        
        # From IDLE, invalid event should not be possible
        self.assertFalse(self.manager.can_transition('invalid_event'))
    
    def test_get_available_events(self):
        """Test getting available events"""
        events = self.manager.get_available_events()
        self.assertIn('button_click', events)
        self.assertIn('user_chat', events)
        self.assertIn('reset', events)
    
    def test_action_execution_error(self):
        """Test handling of action execution errors"""
        # Mock an action that raises an exception
        with patch.object(self.manager.actions, 'on_button_clicked', 
                         side_effect=Exception("Mock action error")):
            
            success = self.manager.transition('button_click', button_type='snapshot')
            
            # Transition should fail and move to ERROR state
            self.assertFalse(success)
            self.assertEqual(self.manager.get_current_state(), AppState.ERROR)
            self.assertIn("Mock action error", self.manager.context.error_message)
    
    def test_guard_function_error(self):
        """Test handling of guard function errors"""
        # Mock a guard that raises an exception
        with patch('stock_data_fsm.transitions.TransitionGuards.has_valid_button_type',
                  side_effect=Exception("Mock guard error")):
            
            success = self.manager.transition('button_click', button_type='snapshot')
            
            # Should transition to error state
            self.assertFalse(success)
            self.assertEqual(self.manager.get_current_state(), AppState.ERROR)
    
    def test_statistics_tracking(self):
        """Test statistics tracking"""
        # Perform some transitions
        self.manager.transition('button_click', button_type='snapshot')
        self.manager.transition('invalid_event')  # Should fail
        
        stats = self.manager.get_statistics()
        
        self.assertEqual(stats['total_transitions'], 2)
        self.assertEqual(stats['successful_transitions'], 1)
        self.assertEqual(stats['failed_transitions'], 1)
        self.assertEqual(stats['current_state'], 'BUTTON_TRIGGERED')
        self.assertIn('success_rate', stats)
    
    def test_context_serialization(self):
        """Test context dictionary serialization"""
        self.manager.transition('button_click', button_type='snapshot', ticker='AAPL')
        
        context_dict = self.manager.get_context_dict(include_history=True)
        
        self.assertEqual(context_dict['current_state'], 'BUTTON_TRIGGERED')
        self.assertEqual(context_dict['button_type'], 'snapshot')
        self.assertEqual(context_dict['ticker'], 'AAPL')
        self.assertIn('transition_history', context_dict)
    
    def test_fsm_health_validation(self):
        """Test FSM health check"""
        health = self.manager.validate_fsm_health()
        
        self.assertIn('fsm_validation', health)
        self.assertIn('context_health', health)
        self.assertIn('statistics', health)
        
        # Context should be healthy initially
        context_health = health['context_health']
        self.assertEqual(context_health['current_state'], 'IDLE')
        self.assertFalse(context_health['has_errors'])
    
    def test_pickle_serialization_compatibility(self):
        """Test Gradio State compatibility through pickle methods"""
        # Set up manager with some state
        self.manager.transition('button_click', button_type='snapshot')
        
        # Test __getstate__
        state = self.manager.__getstate__()
        self.assertIn('session_id', state)
        self.assertIn('context_dict', state)
        self.assertIn('stats', state)
        
        # Test __setstate__
        new_manager = StateManager()
        new_manager.__setstate__(state)
        
        self.assertEqual(new_manager.session_id, self.manager.session_id)
        self.assertEqual(new_manager.get_current_state(), AppState.BUTTON_TRIGGERED)
    
    def test_emergency_reset(self):
        """Test emergency reset from various states"""
        states_to_test = [
            AppState.BUTTON_TRIGGERED,
            AppState.PROMPT_PREPARING,
            AppState.AI_PROCESSING,
            AppState.UPDATING_UI
        ]
        
        for state in states_to_test:
            # Set up manager in specific state
            self.manager.context.current_state = state
            
            # Emergency reset should work
            success = self.manager.transition('emergency_reset')
            self.assertTrue(success, f"Emergency reset failed from {state.name}")
            self.assertEqual(self.manager.get_current_state(), AppState.IDLE)
    
    def test_regular_chat_handling(self):
        """Test regular chat handling (stays in IDLE)"""
        success = self.manager.transition('user_chat', message='Hello')
        
        self.assertTrue(success)
        self.assertEqual(self.manager.get_current_state(), AppState.IDLE)  # Should stay in IDLE
    
    def test_string_representations(self):
        """Test string representations"""
        str_repr = str(self.manager)
        self.assertIn('test-session', str_repr)
        self.assertIn('IDLE', str_repr)
        
        repr_str = repr(self.manager)
        self.assertIn('StateManager', repr_str)
        self.assertIn('test-session', repr_str)


if __name__ == '__main__':
    # Set up logging to avoid noise in tests
    logging.basicConfig(level=logging.CRITICAL)
    unittest.main()
