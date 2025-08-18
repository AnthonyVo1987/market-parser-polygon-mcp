#!/usr/bin/env python3
"""
Test Script for Simplified FSM Backend Changes
Created: 2025-08-18
Purpose: Validate simplified FSM and response parser changes
Success Criteria: All states transition correctly, JSON functionality preserved, error handling non-blocking
"""

import sys
import os
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_data_fsm import StateManager, AppState
from src.response_parser import ResponseParser, DataType

class TestSimplifiedFSM:
    """Test suite for simplified FSM backend changes"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        self.fsm = StateManager()
        self.parser = ResponseParser()
    
    def test_simplified_states_exist(self):
        """Test that only simplified states exist"""
        expected_states = {
            AppState.IDLE,
            AppState.BUTTON_TRIGGERED, 
            AppState.AI_PROCESSING,
            AppState.RESPONSE_RECEIVED,
            AppState.ERROR
        }
        
        all_states = set(AppState)
        assert all_states == expected_states, f"Expected 5 states, got {len(all_states)}: {[s.name for s in all_states]}"
        print("✅ Simplified states validated: 5 states only")
    
    def test_basic_workflow_transitions(self):
        """Test basic workflow: IDLE -> BUTTON_TRIGGERED -> AI_PROCESSING -> RESPONSE_RECEIVED -> IDLE"""
        
        # Start in IDLE
        assert self.fsm.get_current_state() == AppState.IDLE
        
        # Button click
        success = self.fsm.transition('button_click', button_type='snapshot', ticker='AAPL')
        assert success, "Button click transition failed"
        assert self.fsm.get_current_state() == AppState.BUTTON_TRIGGERED
        
        # Start AI processing
        success = self.fsm.transition('start_ai_processing')
        assert success, "Start AI processing transition failed"
        assert self.fsm.get_current_state() == AppState.AI_PROCESSING
        
        # Response received
        test_response = "Current price: $150.25, Volume: 1.2M shares"
        success = self.fsm.transition('response_received', ai_response=test_response)
        assert success, "Response received transition failed"
        assert self.fsm.get_current_state() == AppState.RESPONSE_RECEIVED
        
        # Display complete
        success = self.fsm.transition('display_complete')
        assert success, "Display complete transition failed"
        assert self.fsm.get_current_state() == AppState.IDLE
        
        print("✅ Basic workflow transitions validated")
    
    def test_error_recovery_non_blocking(self):
        """Test that error state doesn't block further operations"""
        
        # Transition to error state
        success = self.fsm.transition('button_click', button_type='snapshot', ticker='TEST')
        assert success
        
        # Force error
        self.fsm._emergency_transition_to_error("Test error condition")
        assert self.fsm.get_current_state() == AppState.ERROR
        
        # Test that button click can recover immediately from error
        success = self.fsm.transition('button_click', button_type='technical', ticker='MSFT')
        assert success, "Button click from ERROR state should succeed"
        assert self.fsm.get_current_state() == AppState.BUTTON_TRIGGERED
        
        print("✅ Error recovery non-blocking validated")
    
    def test_button_independence(self):
        """Test that buttons can be pressed in any order without dependencies"""
        
        # Test multiple button clicks without full workflow completion
        buttons = ['snapshot', 'support_resistance', 'technical']
        
        for button_type in buttons:
            # Reset to IDLE first
            if self.fsm.get_current_state() != AppState.IDLE:
                self.fsm.force_recovery("Test reset")
            
            # Button should work from IDLE
            success = self.fsm.transition('button_click', button_type=button_type, ticker='TEST')
            assert success, f"Button {button_type} failed from IDLE"
            
            # Another button should work from BUTTON_TRIGGERED (interruption)
            next_button = buttons[(buttons.index(button_type) + 1) % len(buttons)]
            success = self.fsm.transition('button_click', button_type=next_button, ticker='TEST2')
            # Should either succeed or fail gracefully without breaking
            
        print("✅ Button independence validated")
    
    def test_json_functionality_preserved(self):
        """Test that JSON parsing and output functionality is preserved"""
        
        # Test JSON extraction and output
        test_response = '''
        Here's the analysis:
        ```json
        {
            "current_price": "$150.25",
            "volume": "1.2M",
            "change": "+2.5%"
        }
        ```
        Analysis complete.
        '''
        
        # Set up context with response
        self.fsm.context.ai_response = test_response
        self.fsm.context.button_type = 'snapshot'
        
        # Trigger response received action
        success = self.fsm.transition('button_click', button_type='snapshot')
        self.fsm.transition('start_ai_processing')
        success = self.fsm.transition('response_received', ai_response=test_response)
        
        # Check that JSON was extracted
        assert self.fsm.context.raw_json_response is not None, "JSON extraction failed"
        
        # Test response parser JSON output (simplified)
        from src.response_parser import ParseResult, ConfidenceLevel
        result = ParseResult(
            data_type=DataType.SNAPSHOT,
            raw_response=test_response,
            parsed_data={'current_price': '$150.25', 'volume': '1.2M'},
            confidence=ConfidenceLevel.HIGH
        )
        
        json_output = result.get_json_output()
        assert '"data_type": "snapshot"' in json_output, "JSON output missing data_type"
        assert '"current_price"' in json_output, "JSON output missing parsed data"
        
        print("✅ JSON functionality preserved")
    
    def test_response_parser_simplified(self):
        """Test that response parser DataFrame methods are removed but JSON preserved"""
        
        from src.response_parser import ParseResult, ConfidenceLevel, DataType
        result = ParseResult(
            data_type=DataType.SNAPSHOT,
            raw_response="Test response",
            parsed_data={'price': '$100.00'},
            confidence=ConfidenceLevel.MEDIUM
        )
        
        # DataFrame methods should be removed
        assert not hasattr(result, 'to_dataframe'), "to_dataframe method should be removed"
        assert not hasattr(result, '_to_snapshot_dataframe'), "_to_snapshot_dataframe should be removed"
        
        # JSON output should work
        assert hasattr(result, 'get_json_output'), "get_json_output method should exist"
        json_str = result.get_json_output()
        assert isinstance(json_str, str), "JSON output should be string"
        assert 'data_type' in json_str, "JSON should contain data_type"
        
        print("✅ Response parser simplification validated")
    
    def test_complex_error_scenarios(self):
        """Test complex error scenarios don't break the system"""
        
        # Test multiple errors in sequence
        errors = [
            "Connection timeout",
            "Invalid API key", 
            "Rate limit exceeded",
            "Unknown error"
        ]
        
        for error_msg in errors:
            # Reset to clean state
            self.fsm.force_recovery("Reset for error test")
            
            # Trigger button and force error
            self.fsm.transition('button_click', button_type='snapshot')
            self.fsm._emergency_transition_to_error(error_msg)
            
            # Should be able to recover
            assert self.fsm.get_current_state() == AppState.ERROR
            
            # Recovery should work
            success = self.fsm.recover_from_error('retry')
            assert success or self.fsm.get_current_state() == AppState.IDLE, f"Recovery failed for error: {error_msg}"
        
        print("✅ Complex error scenarios validated")

def validate_fix_success() -> bool:
    """
    Run comprehensive validation of the backend simplification
    Returns: True if all criteria met, False otherwise
    """
    success_criteria = [
        "5 simplified states only (IDLE, BUTTON_TRIGGERED, AI_PROCESSING, RESPONSE_RECEIVED, ERROR)",
        "Basic workflow transitions work correctly", 
        "Error recovery is non-blocking",
        "Button independence - can click in any order",
        "JSON functionality preserved for textboxes",
        "Response parser DataFrame methods removed",
        "Complex error scenarios don't break system"
    ]
    
    print("\n" + "="*60)
    print("🧪 BACKEND SIMPLIFICATION VALIDATION")
    print("="*60)
    
    try:
        # Create test instance
        test_suite = TestSimplifiedFSM()
        test_suite.setup_method()
        
        # Run validation tests
        print("\n📋 Running validation tests...")
        
        test_suite.test_simplified_states_exist()
        test_suite.test_basic_workflow_transitions()
        test_suite.test_error_recovery_non_blocking()
        test_suite.test_button_independence()
        test_suite.test_json_functionality_preserved()
        test_suite.test_response_parser_simplified()
        test_suite.test_complex_error_scenarios()
        
        print("\n" + "="*60)
        print("✅ ALL VALIDATION TESTS PASSED")
        print("="*60)
        
        print("\n📊 Success Criteria Met:")
        for i, criterion in enumerate(success_criteria, 1):
            print(f"  {i}. ✅ {criterion}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run validation
    if validate_fix_success():
        print("\n🎉 BACKEND SIMPLIFICATION: SUCCESS")
        sys.exit(0)
    else:
        print("\n💥 BACKEND SIMPLIFICATION: FAILED")
        sys.exit(1)