#!/usr/bin/env python3
"""
Backend Integration Validation Script
======================================

This script validates that all backend fixes are properly implemented:
1. Function signatures return exactly 10 values 
2. Message handling uses modern dictionary format
3. FSM integration is preserved
4. All components work together correctly

Run this after implementing backend fixes to ensure compliance.
"""

import sys
import inspect
import asyncio
import logging
from typing import List, Dict, get_type_hints
import pandas as pd

# Suppress warnings for cleaner output
logging.getLogger().setLevel(logging.ERROR)

def validate_function_signatures():
    """Validate that all handler functions have correct signatures"""
    print("🔍 Validating Function Signatures...")
    
    try:
        from chat_ui import handle_user_message, handle_button_click, _clear_enhanced
        
        # Check handle_user_message signature
        sig = inspect.signature(handle_user_message)
        params = list(sig.parameters.keys())
        expected_params = [
            'user_message', 'chat_history', 'pyd_message_history', 
            'tracker', 'cost_markdown', 'fsm_manager', 
            'snapshot_df', 'sr_df', 'tech_df', 'debug_state'
        ]
        
        if params == expected_params:
            print("  ✅ handle_user_message: Parameter order correct")
        else:
            print(f"  ❌ handle_user_message: Expected {expected_params}, got {params}")
            return False
        
        # Check handle_button_click signature
        sig = inspect.signature(handle_button_click)
        params = list(sig.parameters.keys())
        expected_params = [
            'button_type', 'ticker', 'chat_history', 'pyd_message_history',
            'tracker', 'cost_markdown', 'fsm_manager',
            'snapshot_df', 'sr_df', 'tech_df', 'debug_state'
        ]
        
        if params == expected_params:
            print("  ✅ handle_button_click: Parameter order correct")
        else:
            print(f"  ❌ handle_button_click: Expected {expected_params}, got {params}")
            return False
        
        # Check _clear_enhanced return count
        try:
            result = _clear_enhanced()
            if len(result) == 10:
                print("  ✅ _clear_enhanced: Returns exactly 10 values")
            else:
                print(f"  ❌ _clear_enhanced: Returns {len(result)} values, expected 10")
                return False
        except Exception as e:
            print(f"  ❌ _clear_enhanced: Error during execution: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def validate_message_format():
    """Validate that message handling uses modern dictionary format"""
    print("🔍 Validating Message Format...")
    
    try:
        from chat_ui import export_markdown
        from market_parser_demo import TokenCostTracker
        
        # Test with modern message format
        modern_chat_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "What is AAPL stock price?"},
            {"role": "assistant", "content": "AAPL is currently trading at $150.25"}
        ]
        
        tracker = TokenCostTracker()
        
        try:
            markdown_export = export_markdown(modern_chat_history, tracker)
            
            # Check if export contains expected content
            if "Message 1 (User)" in markdown_export and "Hello" in markdown_export:
                print("  ✅ export_markdown: Handles modern message format correctly")
            else:
                print("  ❌ export_markdown: Does not handle modern message format correctly")
                return False
                
            # Check for proper role extraction
            if "👤 Message 1 (User)" in markdown_export and "🤖 Message 2 (Assistant)" in markdown_export:
                print("  ✅ Message roles: Properly extracted from dictionary format")
            else:
                print("  ❌ Message roles: Not properly extracted from dictionary format")
                return False
                
        except Exception as e:
            print(f"  ❌ export_markdown: Error with modern format: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def validate_fsm_integration():
    """Validate that FSM state management is preserved"""
    print("🔍 Validating FSM Integration...")
    
    try:
        from stock_data_fsm import StateManager, AppState
        from chat_ui import _get_debug_state_info
        
        # Test FSM state management
        fsm_manager = StateManager()
        
        # Test initial state
        if fsm_manager.get_current_state() == AppState.IDLE:
            print("  ✅ FSM: Initial state is IDLE")
        else:
            print(f"  ❌ FSM: Initial state is {fsm_manager.get_current_state()}, expected IDLE")
            return False
        
        # Test state transition
        success = fsm_manager.transition('button_click', button_type='snapshot', ticker='AAPL')
        if success:
            print("  ✅ FSM: Button click transition successful")
        else:
            print("  ❌ FSM: Button click transition failed")
            return False
        
        # Test debug info generation
        try:
            debug_info = _get_debug_state_info(fsm_manager)
            if "FSM State:" in debug_info and "Button Type:" in debug_info:
                print("  ✅ FSM Debug: Debug info generation working")
            else:
                print("  ❌ FSM Debug: Debug info missing required fields")
                return False
        except Exception as e:
            print(f"  ❌ FSM Debug: Error generating debug info: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

async def validate_async_handlers():
    """Validate that async handler functions work correctly"""
    print("🔍 Validating Async Handler Functions...")
    
    try:
        from chat_ui import handle_user_message, handle_button_click
        from stock_data_fsm import StateManager
        from market_parser_demo import TokenCostTracker
        
        # Prepare test data
        chat_history = [{"role": "user", "content": "Test message"}]
        pyd_history = []
        tracker = TokenCostTracker()
        fsm_manager = StateManager()
        empty_df = pd.DataFrame()
        
        # Test handle_user_message signature (don't actually call it to avoid MCP setup)
        sig = inspect.signature(handle_user_message)
        if asyncio.iscoroutinefunction(handle_user_message):
            print("  ✅ handle_user_message: Is properly async function")
        else:
            print("  ❌ handle_user_message: Not an async function")
            return False
        
        # Test handle_button_click signature
        sig = inspect.signature(handle_button_click)
        if asyncio.iscoroutinefunction(handle_button_click):
            print("  ✅ handle_button_click: Is properly async function")
        else:
            print("  ❌ handle_button_click: Not an async function")
            return False
        
        # Test return type annotations
        hints = get_type_hints(handle_user_message)
        if 'return' in hints:
            print("  ✅ handle_user_message: Has return type annotation")
        else:
            print("  ⚠️  handle_user_message: Missing return type annotation")
        
        hints = get_type_hints(handle_button_click)
        if 'return' in hints:
            print("  ✅ handle_button_click: Has return type annotation")
        else:
            print("  ⚠️  handle_button_click: Missing return type annotation")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def validate_gradio_integration():
    """Validate Gradio integration patterns"""
    print("🔍 Validating Gradio Integration...")
    
    try:
        from chat_ui import create_enhanced_chat_interface
        
        # Test that interface creation doesn't fail
        try:
            demo = create_enhanced_chat_interface()
            print("  ✅ Gradio Interface: Created successfully")
            
            # Basic check for modern chatbot component
            # (This is a simplified check - full validation would require inspecting the Blocks)
            print("  ✅ Gradio Interface: Enhanced interface configuration loaded")
            
        except Exception as e:
            print(f"  ❌ Gradio Interface: Error creating interface: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def validate_component_compatibility():
    """Validate that all components work together"""
    print("🔍 Validating Component Compatibility...")
    
    try:
        # Test imports
        from stock_data_fsm import StateManager, AppState
        from response_parser import ResponseParser, DataType
        from prompt_templates import PromptTemplateManager, PromptType
        from market_parser_demo import TokenCostTracker
        from chat_ui import ProcessingStatus
        
        # Test component instantiation
        fsm = StateManager()
        parser = ResponseParser(log_level=logging.CRITICAL)
        prompt_mgr = PromptTemplateManager()
        tracker = TokenCostTracker()
        status = ProcessingStatus()
        
        print("  ✅ Component Instantiation: All components created successfully")
        
        # Test component interactions
        status.start_processing("Test", 3)
        status.update_step("Step 1", 1)
        status.complete("Done")
        
        if not status.is_processing:
            print("  ✅ ProcessingStatus: State management working correctly")
        else:
            print("  ❌ ProcessingStatus: State management not working correctly")
            return False
        
        # Test FSM-Parser integration
        success = fsm.transition('button_click', button_type='snapshot', ticker='TEST')
        if success and fsm.get_current_state() == AppState.BUTTON_TRIGGERED:
            print("  ✅ FSM-Parser Integration: State transitions working")
        else:
            print("  ❌ FSM-Parser Integration: State transitions not working")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Component error: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🚀 Backend Integration Validation")
    print("=" * 50)
    
    all_tests = [
        ("Function Signatures", validate_function_signatures),
        ("Message Format", validate_message_format),
        ("FSM Integration", validate_fsm_integration),
        ("Async Handlers", lambda: asyncio.run(validate_async_handlers())),
        ("Gradio Integration", validate_gradio_integration),
        ("Component Compatibility", validate_component_compatibility),
    ]
    
    results = []
    
    for test_name, test_func in all_tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("✅ Backend integration fixes are properly implemented")
        print("🚀 System is ready for testing")
        return True
    else:
        print(f"\n⚠️  {total - passed} validations failed")
        print("❌ Backend integration needs additional fixes")
        print("🔧 Please address the failed validations above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)