"""
Unit tests for state transitions and guard functions
"""

import unittest
from stock_data_fsm.states import AppState, StateContext
from stock_data_fsm.transitions import StateTransitions, TransitionGuards


class TestTransitionGuards(unittest.TestCase):
    """Test guard functions for transitions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.context = StateContext()
    
    def test_has_valid_button_type(self):
        """Test button type validation"""
        # Test invalid button type
        self.context.button_type = None
        self.assertFalse(TransitionGuards.has_valid_button_type(self.context))
        
        self.context.button_type = 'invalid'
        self.assertFalse(TransitionGuards.has_valid_button_type(self.context))
        
        # Test valid button types
        valid_types = ['snapshot', 'support_resistance', 'technical']
        for button_type in valid_types:
            self.context.button_type = button_type
            self.assertTrue(TransitionGuards.has_valid_button_type(self.context))
    
    def test_has_prompt(self):
        """Test prompt validation"""
        # Test no prompt
        self.context.prompt = None
        self.assertFalse(TransitionGuards.has_prompt(self.context))
        
        # Test empty prompt
        self.context.prompt = ""
        self.assertFalse(TransitionGuards.has_prompt(self.context))
        
        # Test whitespace only
        self.context.prompt = "   \n\t  "
        self.assertFalse(TransitionGuards.has_prompt(self.context))
        
        # Test valid prompt
        self.context.prompt = "This is a valid prompt"
        self.assertTrue(TransitionGuards.has_prompt(self.context))
    
    def test_has_ai_response(self):
        """Test AI response validation"""
        # Test no response
        self.context.ai_response = None
        self.assertFalse(TransitionGuards.has_ai_response(self.context))
        
        # Test empty response
        self.context.ai_response = ""
        self.assertFalse(TransitionGuards.has_ai_response(self.context))
        
        # Test whitespace only
        self.context.ai_response = "   \n\t  "
        self.assertFalse(TransitionGuards.has_ai_response(self.context))
        
        # Test valid response
        self.context.ai_response = "AI response content"
        self.assertTrue(TransitionGuards.has_ai_response(self.context))
    
    def test_has_parsed_data(self):
        """Test parsed data validation"""
        # Test empty parsed data
        self.context.parsed_data = {}
        self.assertFalse(TransitionGuards.has_parsed_data(self.context))
        
        # Test with parsed data
        self.context.parsed_data = {'price': 150.0}
        self.assertTrue(TransitionGuards.has_parsed_data(self.context))
    
    def test_under_max_error_attempts(self):
        """Test error attempts limit"""
        # Test under limit
        self.context.error_recovery_attempts = 0
        self.assertTrue(TransitionGuards.under_max_error_attempts(self.context))
        
        self.context.error_recovery_attempts = 2
        self.assertTrue(TransitionGuards.under_max_error_attempts(self.context))
        
        # Test at limit
        self.context.error_recovery_attempts = 3
        self.assertFalse(TransitionGuards.under_max_error_attempts(self.context))
        
        # Test over limit
        self.context.error_recovery_attempts = 5
        self.assertFalse(TransitionGuards.under_max_error_attempts(self.context))
    
    def test_is_idle_ready(self):
        """Test idle readiness check"""
        # Test from AI_PROCESSING (should be false)
        self.context.current_state = AppState.AI_PROCESSING
        self.assertFalse(TransitionGuards.is_idle_ready(self.context))
        
        # Test from other states (should be true)
        for state in AppState:
            if state != AppState.AI_PROCESSING:
                self.context.current_state = state
                self.assertTrue(TransitionGuards.is_idle_ready(self.context))
    
    def test_has_ticker_or_default(self):
        """Test ticker validation with default fallback"""
        # Test no ticker (should still pass due to default)
        self.context.ticker = None
        self.assertTrue(TransitionGuards.has_ticker_or_default(self.context))
        
        # Test empty ticker (should still pass due to default)
        self.context.ticker = ""
        self.assertTrue(TransitionGuards.has_ticker_or_default(self.context))
        
        # Test valid ticker
        self.context.ticker = "AAPL"
        self.assertTrue(TransitionGuards.has_ticker_or_default(self.context))
    
    def test_can_retry_from_error(self):
        """Test retry validation from error state"""
        # Test from non-error state
        self.context.current_state = AppState.IDLE
        self.assertFalse(TransitionGuards.can_retry_from_error(self.context))
        
        # Test from error state with low attempts
        self.context.current_state = AppState.ERROR
        self.context.error_recovery_attempts = 2
        self.assertTrue(TransitionGuards.can_retry_from_error(self.context))
        
        # Test from error state with high attempts
        self.context.current_state = AppState.ERROR
        self.context.error_recovery_attempts = 5
        self.assertFalse(TransitionGuards.can_retry_from_error(self.context))
    
    def test_is_valid_data_type(self):
        """Test data type validation"""
        # Test no button type
        self.context.button_type = None
        self.assertFalse(TransitionGuards.is_valid_data_type(self.context))
        
        # Test invalid button type
        self.context.button_type = 'invalid'
        self.assertFalse(TransitionGuards.is_valid_data_type(self.context))
        
        # Test valid button types
        valid_types = ['snapshot', 'support_resistance', 'technical']
        for button_type in valid_types:
            self.context.button_type = button_type
            self.assertTrue(TransitionGuards.is_valid_data_type(self.context))


class TestStateTransitions(unittest.TestCase):
    """Test state transition logic"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.transitions = StateTransitions()
        self.context = StateContext()
    
    def test_initialization(self):
        """Test StateTransitions initialization"""
        self.assertIsInstance(self.transitions._transitions, dict)
        self.assertGreater(len(self.transitions._transitions), 0)
    
    def test_get_transition_rule_valid(self):
        """Test getting valid transition rules"""
        # Test valid transition
        rule = self.transitions.get_transition_rule(AppState.IDLE, 'button_click')
        self.assertIsNotNone(rule)
        
        next_state, guard_func, action_name = rule
        self.assertEqual(next_state, AppState.BUTTON_TRIGGERED)
        self.assertIsNotNone(guard_func)  # Should have a guard
        self.assertEqual(action_name, 'on_button_clicked')
    
    def test_get_transition_rule_invalid(self):
        """Test getting invalid transition rules"""
        # Test invalid transition
        rule = self.transitions.get_transition_rule(AppState.IDLE, 'invalid_event')
        self.assertIsNone(rule)
        
        # Test valid event from invalid state combination
        rule = self.transitions.get_transition_rule(AppState.AI_PROCESSING, 'button_click')
        self.assertIsNone(rule)
    
    def test_is_valid_transition_with_guard(self):
        """Test transition validation with guards"""
        # Test valid transition with passing guard
        self.context.button_type = 'snapshot'
        is_valid = self.transitions.is_valid_transition(
            AppState.IDLE, 'button_click', self.context
        )
        self.assertTrue(is_valid)
        
        # Test valid transition with failing guard
        self.context.button_type = 'invalid'
        is_valid = self.transitions.is_valid_transition(
            AppState.IDLE, 'button_click', self.context
        )
        self.assertFalse(is_valid)
    
    def test_is_valid_transition_without_guard(self):
        """Test transition validation without guards"""
        # Test transition without guard
        is_valid = self.transitions.is_valid_transition(
            AppState.IDLE, 'user_chat', self.context
        )
        self.assertTrue(is_valid)  # Should pass without guard
    
    def test_is_valid_transition_invalid(self):
        """Test invalid transitions"""
        # Test completely invalid transition
        is_valid = self.transitions.is_valid_transition(
            AppState.IDLE, 'invalid_event', self.context
        )
        self.assertFalse(is_valid)
    
    def test_get_available_events(self):
        """Test getting available events from states"""
        # Test IDLE state events
        idle_events = self.transitions.get_available_events(AppState.IDLE)
        self.assertIn('button_click', idle_events)
        self.assertIn('user_chat', idle_events)
        self.assertIn('reset', idle_events)
        
        # Test ERROR state events
        error_events = self.transitions.get_available_events(AppState.ERROR)
        self.assertIn('retry', error_events)
        self.assertIn('abort', error_events)
        self.assertIn('reset', error_events)
    
    def test_get_reachable_states(self):
        """Test getting reachable states"""
        # Test reachable states from IDLE
        reachable = self.transitions.get_reachable_states(AppState.IDLE)
        self.assertIn(AppState.BUTTON_TRIGGERED, reachable)
        self.assertIn(AppState.IDLE, reachable)  # Can stay in IDLE
        
        # Test reachable states from ERROR
        reachable_error = self.transitions.get_reachable_states(AppState.ERROR)
        self.assertIn(AppState.IDLE, reachable_error)  # Can return to IDLE
    
    def test_validate_state_machine_completeness(self):
        """Test FSM completeness validation"""
        validation = self.transitions.validate_state_machine_completeness()
        
        # Check validation structure
        required_keys = [
            'total_transitions', 'total_states', 'states_with_outgoing',
            'states_with_incoming', 'unreachable_states', 'dead_end_states',
            'validation_passed', 'issues'
        ]
        for key in required_keys:
            self.assertIn(key, validation)
        
        # Basic sanity checks
        self.assertGreater(validation['total_transitions'], 0)
        self.assertEqual(validation['total_states'], len(AppState))
        self.assertIsInstance(validation['validation_passed'], bool)
        self.assertIsInstance(validation['issues'], list)
    
    def test_get_transition_graph(self):
        """Test transition graph generation"""
        graph = self.transitions.get_transition_graph()
        
        # Check that all states are represented
        for state in AppState:
            self.assertIn(state.name, graph)
        
        # Check that IDLE has outgoing transitions
        self.assertGreater(len(graph['IDLE']), 0)
        
        # Check that ERROR has recovery transitions
        self.assertGreater(len(graph['ERROR']), 0)
    
    def test_critical_transitions_exist(self):
        """Test that critical transitions exist"""
        critical_transitions = [
            # Simplified 5-state workflow
            (AppState.IDLE, 'button_click'),
            (AppState.BUTTON_TRIGGERED, 'start_ai_processing'),
            (AppState.AI_PROCESSING, 'response_received'),
            (AppState.RESPONSE_RECEIVED, 'display_complete'),
            
            # Error recovery
            (AppState.ERROR, 'retry'),
            (AppState.ERROR, 'abort'),
            (AppState.ERROR, 'button_click'),  # Direct recovery from error
            
            # Regular chat and reset
            (AppState.IDLE, 'user_chat'),
            (AppState.IDLE, 'reset'),
        ]
        
        for state, event in critical_transitions:
            rule = self.transitions.get_transition_rule(state, event)
            self.assertIsNotNone(rule, f"Missing critical transition: {state.name} + {event}")
    
    def test_error_transitions_from_all_states(self):
        """Test that error transitions exist from processing states"""
        processing_states = [
            AppState.BUTTON_TRIGGERED,
            AppState.AI_PROCESSING,
            AppState.RESPONSE_RECEIVED
        ]
        
        for state in processing_states:
            # Should have either 'error' transition or 'emergency_reset'
            events = self.transitions.get_available_events(state)
            has_error_handling = any(event in ['error', 'emergency_reset', 'ai_error', 'ai_timeout', 'display_error'] for event in events)
            self.assertTrue(has_error_handling, f"No error handling from state: {state.name}")
    
    def test_no_duplicate_transitions(self):
        """Test that there are no duplicate transition keys"""
        transition_keys = list(self.transitions._transitions.keys())
        unique_keys = list(set(transition_keys))
        self.assertEqual(len(transition_keys), len(unique_keys), "Duplicate transition keys found")
    
    def test_all_states_reachable(self):
        """Test that all states are reachable from IDLE"""
        def get_all_reachable(start_state, visited=None):
            if visited is None:
                visited = set()
            
            if start_state in visited:
                return visited
            
            visited.add(start_state)
            reachable = self.transitions.get_reachable_states(start_state)
            
            for state in reachable:
                visited.update(get_all_reachable(state, visited.copy()))
            
            return visited
        
        reachable = get_all_reachable(AppState.IDLE)
        all_states = set(AppState)
        
        # All states should be reachable from IDLE
        self.assertEqual(reachable, all_states, f"Unreachable states: {all_states - reachable}")


if __name__ == '__main__':
    unittest.main()
