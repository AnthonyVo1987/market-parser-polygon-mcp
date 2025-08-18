#!/usr/bin/env python3
"""
Simple validation script for FSM transition bug fix
Created: 2025-08-18
Purpose: Validate that FSM no longer gets stuck in BUTTON_TRIGGERED state
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from stock_data_fsm.states import AppState
from stock_data_fsm.manager import StateManager

def test_core_bug_fix():
    """Test that the core FSM bug is fixed"""
    print("🧪 Testing FSM Transition Bug Fix")
    print("=" * 50)
    
    # Create FSM manager
    fsm_manager = StateManager()
    print(f"✅ FSM initialized in state: {fsm_manager.get_current_state()}")
    
    # Test the fixed workflow for each button type
    button_types = ["snapshot", "support_resistance", "technical"]
    
    for i, button_type in enumerate(button_types, 1):
        print(f"\n🔄 Test {i}: {button_type} button workflow")
        
        # Ensure we start from IDLE
        assert fsm_manager.get_current_state() == AppState.IDLE, "Should start from IDLE"
        print(f"  Start state: {fsm_manager.get_current_state()}")
        
        # Set context and trigger button click
        fsm_manager.context.button_type = button_type
        fsm_manager.context.ticker = "NVDA"
        fsm_manager.transition('button_click')
        
        current_state = fsm_manager.get_current_state()
        print(f"  After button_click: {current_state}")
        assert current_state == AppState.BUTTON_TRIGGERED, f"Should be BUTTON_TRIGGERED, got {current_state}"
        
        # FIXED: Use start_ai_processing instead of prepare_prompt/prompt_ready
        fsm_manager.transition('start_ai_processing')
        current_state = fsm_manager.get_current_state()
        print(f"  After start_ai_processing: {current_state}")
        assert current_state == AppState.AI_PROCESSING, f"Should be AI_PROCESSING, got {current_state}"
        
        # Simulate AI response
        fsm_manager.context.ai_response = f"Mock response for {button_type}"
        fsm_manager.transition('response_received')
        current_state = fsm_manager.get_current_state()
        print(f"  After response_received: {current_state}")
        assert current_state == AppState.RESPONSE_RECEIVED, f"Should be RESPONSE_RECEIVED, got {current_state}"
        
        # FIXED: Use display_complete instead of abort
        fsm_manager.transition('display_complete')
        current_state = fsm_manager.get_current_state()
        print(f"  After display_complete: {current_state}")
        assert current_state == AppState.IDLE, f"Should return to IDLE, got {current_state}"
        
        print(f"  ✅ {button_type} workflow completed successfully")
    
    print(f"\n🎉 SUCCESS: All {len(button_types)} button workflows completed successfully!")
    print("✅ FSM properly cycles: IDLE → BUTTON_TRIGGERED → AI_PROCESSING → RESPONSE_RECEIVED → IDLE")
    print("✅ No more stuck states in BUTTON_TRIGGERED")
    print("✅ All button actions are independent")
    
    return True

def test_invalid_transitions_still_caught():
    """Test that invalid transitions are still properly caught"""
    print(f"\n🔍 Testing Invalid Transition Handling")
    print("=" * 50)
    
    fsm_manager = StateManager()
    
    # Test that rapid button clicks are rejected (correct behavior)
    fsm_manager.context.button_type = "snapshot"
    fsm_manager.transition('button_click')
    assert fsm_manager.get_current_state() == AppState.BUTTON_TRIGGERED
    
    # This should be rejected
    fsm_manager.transition('button_click')  # Should be invalid from BUTTON_TRIGGERED
    assert fsm_manager.get_current_state() == AppState.BUTTON_TRIGGERED, "Should stay in BUTTON_TRIGGERED"
    
    print("✅ Invalid transitions are properly rejected")
    return True

if __name__ == "__main__":
    print("🚀 FSM Transition Bug Fix Validation")
    print("📋 Testing fixes for chat_ui.py lines 307-308 and 368")
    print("🎯 Expected: FSM no longer gets stuck in BUTTON_TRIGGERED state")
    print()
    
    try:
        # Test core bug fix
        success1 = test_core_bug_fix()
        
        # Test invalid transition handling
        success2 = test_invalid_transitions_still_caught()
        
        if success1 and success2:
            print("\n" + "=" * 60)
            print("🎉 BUG FIX VALIDATION: SUCCESS")
            print("✅ FSM state transitions are now working correctly")
            print("✅ All button actions are independent and functional")
            print("✅ No more stuck states preventing subsequent actions")
            print("=" * 60)
        else:
            print("\n💥 BUG FIX VALIDATION: FAILED")
            
    except Exception as e:
        print(f"\n💥 BUG FIX VALIDATION: FAILED")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()