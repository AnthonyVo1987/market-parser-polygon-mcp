#!/usr/bin/env python3
"""
Test Default Ticker Fix - Bug #1 Validation
Validates that NVDA appears as default ticker on application startup.

Bug #1 Description:
- Issue: App starts with empty ticker field, should default to NVDA  
- Expected: NVDA should be the default ticker while allowing user changes
- Fix: Add value="NVDA" to gr.Textbox() for ticker input component

Test Requirements:
- Verify "NVDA" appears as default value on application startup
- Confirm users can clear and enter different ticker symbols  
- Ensure no regression in existing ticker validation logic
"""

import unittest
import sys
import os
import re
import logging
from unittest.mock import patch, MagicMock

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging to suppress noise during testing
logging.basicConfig(level=logging.ERROR)


class TestDefaultTickerFix(unittest.TestCase):
    """Test suite validating Bug #1 fix - Default ticker configuration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.expected_default_ticker = "NVDA"
        
    def test_chat_ui_file_contains_default_ticker(self):
        """Test that chat_ui.py contains the default ticker value"""
        print("🔍 Testing chat_ui.py for default ticker configuration...")
        
        # Read the chat_ui.py file
        try:
            with open('chat_ui.py', 'r') as f:
                chat_ui_content = f.read()
        except FileNotFoundError:
            self.fail("chat_ui.py file not found - required for ticker validation")
        
        # Look for ticker input field with default value
        # Pattern should match: value="NVDA" within a gr.Textbox definition
        ticker_patterns = [
            r'gr\.Textbox\([^)]*value\s*=\s*["\']NVDA["\'][^)]*\)',  # Direct value parameter
            r'value\s*=\s*["\']NVDA["\']',  # Standalone value assignment
        ]
        
        ticker_found = False
        matched_pattern = None
        
        for pattern in ticker_patterns:
            if re.search(pattern, chat_ui_content):
                ticker_found = True
                matched_pattern = pattern
                break
        
        # Verify default ticker is configured
        self.assertTrue(
            ticker_found, 
            f"Default ticker 'NVDA' not found in chat_ui.py. "
            f"Expected to find value=\"NVDA\" in gr.Textbox configuration. "
            f"Searched patterns: {ticker_patterns}"
        )
        
        print("✅ Default ticker 'NVDA' found in chat_ui.py configuration")
        print(f"   Pattern matched: {matched_pattern}")
        
    def test_ticker_input_field_configuration(self):
        """Test that ticker input field is properly configured"""
        print("🎯 Testing ticker input field configuration...")
        
        # Read chat_ui.py to analyze ticker field setup
        with open('chat_ui.py', 'r') as f:
            content = f.read()
        
        # Find ticker-related textbox configurations
        textbox_matches = re.finditer(r'gr\.Textbox\([^)]+\)', content, re.DOTALL)
        
        ticker_textboxes = []
        for match in textbox_matches:
            textbox_content = match.group(0)
            # Look for ticker-related fields (label, placeholder, or variable names)
            if any(keyword in textbox_content.lower() for keyword in ['ticker', 'symbol', 'stock']):
                ticker_textboxes.append(textbox_content)
        
        # Should find at least one ticker textbox
        self.assertGreater(
            len(ticker_textboxes), 0,
            "No ticker-related textbox found in chat_ui.py"
        )
        
        # Verify at least one has NVDA as default value
        has_nvda_default = any('NVDA' in textbox for textbox in ticker_textboxes)
        self.assertTrue(
            has_nvda_default,
            f"No ticker textbox has NVDA as default value. Found textboxes: {ticker_textboxes}"
        )
        
        print(f"✅ Found {len(ticker_textboxes)} ticker textbox(es) with NVDA default")
        
    def test_default_ticker_validation_compatibility(self):
        """Test that default ticker doesn't break existing validation"""
        print("🔐 Testing ticker validation compatibility...")
        
        # Test FSM transitions with default ticker
        try:
            from stock_data_fsm.transitions import TransitionGuards
            from stock_data_fsm.states import StateContext
            
            # Test that default ticker passes validation
            context = StateContext()
            
            # Test 1: Empty ticker should pass (due to default fallback)
            context.ticker = ""
            result1 = TransitionGuards.has_ticker_or_default(context)
            self.assertTrue(result1, "Empty ticker should pass validation with default fallback")
            
            # Test 2: None ticker should pass (due to default fallback)  
            context.ticker = None
            result2 = TransitionGuards.has_ticker_or_default(context)
            self.assertTrue(result2, "None ticker should pass validation with default fallback")
            
            # Test 3: Valid custom ticker should pass
            context.ticker = "AAPL"
            result3 = TransitionGuards.has_ticker_or_default(context)
            self.assertTrue(result3, "Custom ticker should pass validation")
            
            print("✅ Ticker validation maintains compatibility with default fallback")
            
        except ImportError as e:
            self.fail(f"Failed to import FSM modules for validation testing: {e}")
    
    def test_user_can_override_default_ticker(self):
        """Test that users can change from default ticker to custom values"""
        print("✏️ Testing user override capability...")
        
        # This is a conceptual test since we can't directly test Gradio UI
        # But we can verify the field configuration allows modification
        
        with open('chat_ui.py', 'r') as f:
            content = f.read()
        
        # Look for ticker textbox and verify it's not readonly/disabled
        ticker_textbox_pattern = r'gr\.Textbox\([^)]*value\s*=\s*["\']NVDA["\'][^)]*\)'
        match = re.search(ticker_textbox_pattern, content)
        
        if match:
            textbox_config = match.group(0)
            
            # Verify field is not disabled or readonly
            is_readonly = 'readonly' in textbox_config.lower() and 'true' in textbox_config.lower()
            is_disabled = 'disabled' in textbox_config.lower() and 'true' in textbox_config.lower()
            is_interactive = 'interactive' in textbox_config.lower()
            
            self.assertFalse(is_readonly, "Ticker field should not be readonly")
            self.assertFalse(is_disabled, "Ticker field should not be disabled")
            
            # If interactive is specified, it should be True (default is True anyway)
            if is_interactive:
                interactive_true = 'interactive=true' in textbox_config.lower() or 'interactive = true' in textbox_config.lower()
                self.assertTrue(interactive_true or 'interactive=false' not in textbox_config.lower(),
                              "Ticker field should be interactive")
            
            print("✅ Ticker field allows user modification (not readonly/disabled)")
        else:
            self.fail("Could not find ticker textbox with NVDA default for override testing")
    
    def test_ticker_field_properties(self):
        """Test additional ticker field properties are appropriate"""
        print("📋 Testing ticker field properties...")
        
        with open('chat_ui.py', 'r') as f:
            content = f.read()
        
        # Find ticker textbox configuration
        ticker_pattern = r'gr\.Textbox\([^)]*(?:ticker|symbol|stock)[^)]*\)'
        matches = re.finditer(ticker_pattern, content, re.IGNORECASE | re.DOTALL)
        
        ticker_configs = [match.group(0) for match in matches]
        
        # Should have at least one ticker configuration
        self.assertGreater(len(ticker_configs), 0, "No ticker textbox configuration found")
        
        for config in ticker_configs:
            # Check for appropriate properties
            has_label = 'label' in config.lower()
            has_placeholder = 'placeholder' in config.lower()
            has_default = 'NVDA' in config
            
            if has_default:  # Focus on the main ticker field
                print(f"✅ Ticker field configuration found:")
                print(f"   - Has label: {has_label}")
                print(f"   - Has placeholder: {has_placeholder}")
                print(f"   - Has NVDA default: {has_default}")
                
                # At minimum, should have default value
                self.assertTrue(has_default, "Primary ticker field must have NVDA default")
                break
        else:
            self.fail("No ticker field found with NVDA default value")


class TestDefaultTickerIntegration(unittest.TestCase):
    """Integration tests for default ticker functionality"""
    
    def test_fsm_integration_with_default_ticker(self):
        """Test FSM state management with default ticker"""
        print("🔄 Testing FSM integration with default ticker...")
        
        try:
            from stock_data_fsm import StateManager, AppState
            from stock_data_fsm.states import StateContext
            
            # Initialize state manager
            manager = StateManager()
            
            # Test transition with empty ticker (should use default)
            # Pass parameters as kwargs, not context
            result = manager.transition('button_click', button_type='snapshot', ticker='')
            
            # Should transition successfully to BUTTON_TRIGGERED state
            self.assertTrue(result, "Transition should succeed")
            self.assertEqual(manager.get_current_state(), AppState.BUTTON_TRIGGERED,
                           "FSM should transition successfully with empty ticker due to default")
            
            print("✅ FSM handles default ticker transitions correctly")
            
        except Exception as e:
            self.fail(f"FSM integration test failed: {e}")
    
    def test_prompt_generation_with_default_ticker(self):
        """Test that prompt generation works with default ticker"""
        print("📝 Testing prompt generation with default ticker...")
        
        try:
            from prompt_templates import PromptTemplateManager, PromptType
            
            prompt_manager = PromptTemplateManager()
            
            # Test prompt generation with empty ticker (should default to NVDA)
            prompt = prompt_manager.get_prompt(
                prompt_type=PromptType.SNAPSHOT,
                ticker="",  # Empty ticker should trigger default
                enhanced=True
            )
            
            # Prompt should be generated successfully
            self.assertIsNotNone(prompt, "Prompt should be generated with default ticker")
            self.assertGreater(len(prompt), 0, "Prompt should not be empty")
            
            # Should contain either default ticker or be generic enough to work
            prompt_lower = prompt.lower()
            has_nvda = 'nvda' in prompt_lower
            has_ticker_placeholder = '{ticker}' in prompt.lower() or 'ticker' in prompt_lower
            
            self.assertTrue(
                has_nvda or has_ticker_placeholder,
                "Prompt should reference NVDA or have ticker placeholder"
            )
            
            print("✅ Prompt generation works with default ticker logic")
            
        except Exception as e:
            self.fail(f"Prompt generation test failed: {e}")


def run_default_ticker_validation():
    """Run comprehensive default ticker fix validation"""
    print("=" * 70)
    print("🧪 DEFAULT TICKER FIX VALIDATION - Bug #1")
    print("=" * 70)
    print("Testing NVDA default ticker configuration in chat_ui.py...")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDefaultTickerFix))
    suite.addTests(loader.loadTestsFromTestCase(TestDefaultTickerIntegration))
    
    # Run tests with custom result tracking
    runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
    result = runner.run(suite)
    
    # Custom reporting
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    successes = total_tests - failures - errors
    
    print(f"📊 Test Results Summary:")
    print(f"   Total tests: {total_tests}")
    print(f"   Passed: {successes}")
    print(f"   Failed: {failures}")
    print(f"   Errors: {errors}")
    print(f"   Success rate: {(successes/total_tests)*100:.1f}%")
    print()
    
    if result.wasSuccessful():
        print("✅ BUG #1 FIX VALIDATION: SUCCESS!")
        print("   - NVDA default ticker is properly configured")
        print("   - Users can override default ticker value")
        print("   - FSM integration maintains compatibility")
        print("   - No regression in existing functionality")
        return True
    else:
        print("❌ BUG #1 FIX VALIDATION: FAILED!")
        print("   Issues found:")
        
        for test, error in result.failures + result.errors:
            print(f"   - {test}: {error.split(chr(10))[0]}")
        
        return False


if __name__ == '__main__':
    # Run validation
    success = run_default_ticker_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)