"""
Unit tests for state definitions and context management
"""

import unittest
import time
from stock_data_fsm.states import AppState, StateContext, TransitionRecord


class TestAppState(unittest.TestCase):
    """Test AppState enum functionality"""
    
    def test_all_states_defined(self):
        """Test that all required states are defined"""
        expected_states = {
            'IDLE', 'BUTTON_TRIGGERED', 'AI_PROCESSING', 
            'RESPONSE_RECEIVED', 'ERROR'
        }
        
        actual_states = {state.name for state in AppState}
        self.assertEqual(expected_states, actual_states)
    
    def test_state_string_representation(self):
        """Test string representations of states"""
        state = AppState.IDLE
        self.assertEqual(str(state), 'IDLE')
        self.assertEqual(repr(state), 'AppState.IDLE')
    
    def test_state_uniqueness(self):
        """Test that all states have unique values"""
        values = [state.value for state in AppState]
        self.assertEqual(len(values), len(set(values)))


class TestTransitionRecord(unittest.TestCase):
    """Test TransitionRecord functionality"""
    
    def test_basic_creation(self):
        """Test basic transition record creation"""
        record = TransitionRecord(
            from_state=AppState.IDLE,
            to_state=AppState.BUTTON_TRIGGERED,
            event='button_click',
            timestamp=time.time(),
            success=True
        )
        
        self.assertEqual(record.from_state, AppState.IDLE)
        self.assertEqual(record.to_state, AppState.BUTTON_TRIGGERED)
        self.assertEqual(record.event, 'button_click')
        self.assertTrue(record.success)
        self.assertIsNone(record.error_message)
    
    def test_timestamp_auto_generation(self):
        """Test that timestamp is auto-generated if not provided"""
        before = time.time()
        record = TransitionRecord(
            from_state=AppState.IDLE,
            to_state=AppState.BUTTON_TRIGGERED,
            event='button_click',
            timestamp=0,  # Invalid timestamp
            success=True
        )
        after = time.time()
        
        self.assertGreaterEqual(record.timestamp, before)
        self.assertLessEqual(record.timestamp, after)
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        record = TransitionRecord(
            from_state=AppState.IDLE,
            to_state=AppState.ERROR,
            event='error',
            timestamp=1234567890.0,
            success=False,
            error_message='Test error'
        )
        
        expected = {
            'from_state': 'IDLE',
            'to_state': 'ERROR',
            'event': 'error',
            'timestamp': 1234567890.0,
            'success': False,
            'error_message': 'Test error'
        }
        
        self.assertEqual(record.to_dict(), expected)


class TestStateContext(unittest.TestCase):
    """Test StateContext functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.context = StateContext()
    
    def test_default_initialization(self):
        """Test default context initialization"""
        self.assertEqual(self.context.current_state, AppState.IDLE)
        self.assertIsNone(self.context.previous_state)
        self.assertIsNone(self.context.button_type)
        self.assertIsNone(self.context.ticker)
        self.assertIsNone(self.context.prompt)
        self.assertIsNone(self.context.ai_response)
        self.assertEqual(self.context.parsed_data, {})
        self.assertIsNone(self.context.error_message)
        self.assertEqual(self.context.error_recovery_attempts, 0)
        self.assertEqual(self.context.transition_history, [])
    
    def test_invalid_state_initialization(self):
        """Test that invalid states raise ValueError"""
        with self.assertRaises(ValueError):
            StateContext(current_state="invalid")
        
        with self.assertRaises(ValueError):
            StateContext(previous_state="invalid")
    
    def test_add_transition_record(self):
        """Test adding transition records"""
        self.context.add_transition_record(
            from_state=AppState.IDLE,
            to_state=AppState.BUTTON_TRIGGERED,
            event='button_click'
        )
        
        self.assertEqual(len(self.context.transition_history), 1)
        record = self.context.transition_history[0]
        self.assertEqual(record.from_state, AppState.IDLE)
        self.assertEqual(record.to_state, AppState.BUTTON_TRIGGERED)
        self.assertEqual(record.event, 'button_click')
        self.assertTrue(record.success)
    
    def test_clear_data_preserve_history(self):
        """Test clearing data while preserving history"""
        # Set up context with data
        self.context.button_type = 'snapshot'
        self.context.ticker = 'AAPL'
        self.context.prompt = 'Test prompt'
        self.context.ai_response = 'Test response'
        self.context.parsed_data = {'price': 150.0}
        self.context.error_message = 'Test error'
        self.context.error_recovery_attempts = 2
        
        # Add a transition record
        self.context.add_transition_record(
            from_state=AppState.IDLE,
            to_state=AppState.BUTTON_TRIGGERED,
            event='button_click'
        )
        
        # Clear data preserving history
        self.context.clear_data(preserve_history=True)
        
        # Check that data is cleared
        self.assertIsNone(self.context.button_type)
        self.assertIsNone(self.context.ticker)
        self.assertIsNone(self.context.prompt)
        self.assertIsNone(self.context.ai_response)
        self.assertEqual(self.context.parsed_data, {})
        self.assertIsNone(self.context.error_message)
        self.assertEqual(self.context.error_recovery_attempts, 0)
        
        # Check that history is preserved
        self.assertEqual(len(self.context.transition_history), 1)
    
    def test_clear_data_no_preserve_history(self):
        """Test clearing data without preserving history"""
        # Set up context with data and history
        self.context.button_type = 'snapshot'
        self.context.add_transition_record(
            from_state=AppState.IDLE,
            to_state=AppState.BUTTON_TRIGGERED,
            event='button_click'
        )
        
        # Clear data without preserving history
        self.context.clear_data(preserve_history=False)
        
        # Check that everything is cleared
        self.assertIsNone(self.context.button_type)
        self.assertEqual(self.context.transition_history, [])
    
    def test_error_attempts_management(self):
        """Test error attempts increment and reset"""
        # Test increment
        attempts = self.context.increment_error_attempts()
        self.assertEqual(attempts, 1)
        self.assertEqual(self.context.error_recovery_attempts, 1)
        
        attempts = self.context.increment_error_attempts()
        self.assertEqual(attempts, 2)
        self.assertEqual(self.context.error_recovery_attempts, 2)
        
        # Test reset
        self.context.error_message = 'Test error'
        self.context.reset_error_attempts()
        self.assertEqual(self.context.error_recovery_attempts, 0)
        self.assertIsNone(self.context.error_message)
    
    def test_get_history_summary_empty(self):
        """Test history summary with empty history"""
        summary = self.context.get_history_summary()
        expected = {'total_transitions': 0}
        self.assertEqual(summary, expected)
    
    def test_get_history_summary_with_data(self):
        """Test history summary with transition data"""
        # Add successful transition
        self.context.add_transition_record(
            from_state=AppState.IDLE,
            to_state=AppState.BUTTON_TRIGGERED,
            event='button_click',
            success=True
        )
        
        # Add failed transition
        self.context.add_transition_record(
            from_state=AppState.BUTTON_TRIGGERED,
            to_state=AppState.ERROR,
            event='error',
            success=False
        )
        
        summary = self.context.get_history_summary()
        
        self.assertEqual(summary['total_transitions'], 2)
        self.assertEqual(summary['successful_transitions'], 1)
        self.assertEqual(summary['failed_transitions'], 1)
        self.assertIn('first_transition', summary)
        self.assertIn('last_transition', summary)
        self.assertIn('session_duration', summary)
    
    def test_to_dict_basic(self):
        """Test conversion to dictionary without history"""
        self.context.current_state = AppState.BUTTON_TRIGGERED
        self.context.button_type = 'snapshot'
        self.context.ticker = 'AAPL'
        
        data = self.context.to_dict(include_history=False)
        
        self.assertEqual(data['current_state'], 'BUTTON_TRIGGERED')
        self.assertEqual(data['button_type'], 'snapshot')
        self.assertEqual(data['ticker'], 'AAPL')
        self.assertIn('history_summary', data)
        self.assertNotIn('transition_history', data)
    
    def test_to_dict_with_history(self):
        """Test conversion to dictionary with history"""
        self.context.add_transition_record(
            from_state=AppState.IDLE,
            to_state=AppState.BUTTON_TRIGGERED,
            event='button_click'
        )
        
        data = self.context.to_dict(include_history=True)
        
        self.assertIn('transition_history', data)
        self.assertEqual(len(data['transition_history']), 1)
        self.assertEqual(data['transition_history'][0]['event'], 'button_click')
    
    def test_string_representations(self):
        """Test string and repr methods"""
        self.context.current_state = AppState.BUTTON_TRIGGERED
        self.context.button_type = 'snapshot'
        
        str_repr = str(self.context)
        self.assertIn('BUTTON_TRIGGERED', str_repr)
        self.assertIn('snapshot', str_repr)
        
        repr_str = repr(self.context)
        self.assertIn('StateContext', repr_str)
        self.assertIn('BUTTON_TRIGGERED', repr_str)


if __name__ == '__main__':
    unittest.main()
