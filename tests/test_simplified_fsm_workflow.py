#!/usr/bin/env python3
"""
Simplified FSM Workflow Tests

Tests for the simplified 5-state FSM workflow:
IDLE -> BUTTON_TRIGGERED -> AI_PROCESSING -> RESPONSE_RECEIVED -> IDLE

This replaces complex FSM manager tests with a focused test on the simplified workflow.
"""

import unittest
import logging
from stock_data_fsm import StateManager, AppState


class TestSimplifiedFSMWorkflow(unittest.TestCase):
    """Test the simplified 5-state FSM workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.fsm = StateManager(session_id='test-simplified')
        self.fsm.logger.setLevel(logging.CRITICAL)  # Suppress logs
    
    def test_basic_button_workflow(self):
        """Test basic button click workflow"""
        # Start in IDLE
        self.assertEqual(self.fsm.get_current_state(), AppState.IDLE)
        
        # Button click -> BUTTON_TRIGGERED
        success = self.fsm.transition('button_click', button_type='snapshot', ticker='AAPL')
        self.assertTrue(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.BUTTON_TRIGGERED)
        
        # Start AI processing -> AI_PROCESSING
        success = self.fsm.transition('start_ai_processing')
        self.assertTrue(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.AI_PROCESSING)
        
        # Response received -> RESPONSE_RECEIVED
        self.fsm.context.ai_response = "Mock AI response"
        success = self.fsm.transition('response_received')
        self.assertTrue(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.RESPONSE_RECEIVED)
        
        # Display complete -> IDLE
        success = self.fsm.transition('display_complete')
        self.assertTrue(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.IDLE)
    
    def test_error_recovery_workflow(self):
        """Test error recovery from any state"""
        # Start normal workflow
        self.fsm.transition('button_click', button_type='snapshot', ticker='AAPL')
        self.fsm.transition('start_ai_processing')
        
        # Simulate AI error
        success = self.fsm.transition('ai_timeout')
        self.assertTrue(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.ERROR)
        
        # Recover to IDLE
        success = self.fsm.transition('retry')
        self.assertTrue(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.IDLE)
    
    def test_direct_error_recovery_button(self):
        """Test direct button click from error state"""
        # Force error state
        self.fsm.transition('button_click', button_type='snapshot', ticker='AAPL')
        self.fsm.transition('start_ai_processing')
        self.fsm.transition('ai_error')
        self.assertEqual(self.fsm.get_current_state(), AppState.ERROR)
        
        # Direct button click recovery
        success = self.fsm.transition('button_click', button_type='technical', ticker='TSLA')
        self.assertTrue(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.BUTTON_TRIGGERED)
    
    def test_invalid_transitions(self):
        """Test invalid transitions are rejected"""
        # Try invalid transition from IDLE
        success = self.fsm.transition('invalid_event')
        self.assertFalse(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.IDLE)
        
        # Try button click without valid button type
        success = self.fsm.transition('button_click', button_type='invalid')
        self.assertFalse(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.IDLE)
    
    def test_context_preservation(self):
        """Test context data is preserved through workflow"""
        # Start workflow with specific data
        self.fsm.transition('button_click', button_type='support_resistance', ticker='NVDA')
        
        # Check context is preserved
        self.assertEqual(self.fsm.context.button_type, 'support_resistance')
        self.assertEqual(self.fsm.context.ticker, 'NVDA')
        
        # Continue workflow
        self.fsm.transition('start_ai_processing')
        
        # Context should still be preserved
        self.assertEqual(self.fsm.context.button_type, 'support_resistance')
        self.assertEqual(self.fsm.context.ticker, 'NVDA')
    
    def test_emergency_reset(self):
        """Test emergency reset from any state"""
        # Get into processing state
        self.fsm.transition('button_click', button_type='snapshot', ticker='AAPL')
        self.fsm.transition('start_ai_processing')
        self.assertEqual(self.fsm.get_current_state(), AppState.AI_PROCESSING)
        
        # Emergency reset
        success = self.fsm.transition('emergency_reset')
        self.assertTrue(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.IDLE)
    
    def test_regular_chat_stays_idle(self):
        """Test regular chat keeps FSM in IDLE state"""
        self.assertEqual(self.fsm.get_current_state(), AppState.IDLE)
        
        # Regular chat
        success = self.fsm.transition('user_chat')
        self.assertTrue(success)
        self.assertEqual(self.fsm.get_current_state(), AppState.IDLE)  # Should stay IDLE
    
    def test_workflow_history_tracking(self):
        """Test that workflow history is tracked"""
        initial_history_count = len(self.fsm.context.transition_history)
        
        # Run complete workflow
        self.fsm.transition('button_click', button_type='snapshot', ticker='AAPL')
        self.fsm.transition('start_ai_processing')
        self.fsm.context.ai_response = "Mock response"
        self.fsm.transition('response_received')
        self.fsm.transition('display_complete')
        
        # Should have recorded all transitions
        final_history_count = len(self.fsm.context.transition_history)
        self.assertGreater(final_history_count, initial_history_count)
        self.assertEqual(final_history_count - initial_history_count, 4)  # 4 transitions


class TestSimplifiedFSMStates(unittest.TestCase):
    """Test that the FSM has exactly the expected 5 states"""
    
    def test_exactly_five_states(self):
        """Test FSM has exactly 5 states"""
        states = list(AppState)
        self.assertEqual(len(states), 5)
    
    def test_expected_state_names(self):
        """Test FSM has expected state names"""
        expected_states = {'IDLE', 'BUTTON_TRIGGERED', 'AI_PROCESSING', 'RESPONSE_RECEIVED', 'ERROR'}
        actual_states = {state.name for state in AppState}
        self.assertEqual(actual_states, expected_states)
    
    def test_fsm_starts_idle(self):
        """Test FSM starts in IDLE state"""
        fsm = StateManager()
        self.assertEqual(fsm.get_current_state(), AppState.IDLE)


def run_simplified_fsm_tests():
    """Run simplified FSM tests"""
    print("🔄 Testing Simplified 5-State FSM")
    print("=" * 40)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSimplifiedFSMWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestSimplifiedFSMStates))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report results
    print(f"\n📊 Simplified FSM Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.wasSuccessful():
        print(f"\n✅ SIMPLIFIED FSM TESTS PASSED!")
        print(f"🎯 5-state workflow is working correctly")
        print(f"🔄 All critical transitions are functional")
        print(f"⚡ Error recovery is non-blocking")
    else:
        print(f"\n❌ Some FSM tests failed")
        if result.failures:
            for test, traceback in result.failures:
                print(f"   FAILURE: {test}")
        if result.errors:
            for test, traceback in result.errors:
                print(f"   ERROR: {test}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_simplified_fsm_tests()
    exit(0 if success else 1)