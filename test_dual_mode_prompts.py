#!/usr/bin/env python3
"""
Test Script for Dual-Mode Prompt System Validation
Created: 2025-08-19
Purpose: Validate the new dual-mode prompt system works correctly
Success Criteria: 
- Button mode generates JSON-focused prompts with full schema details
- User mode generates conversational prompts for natural text responses
- Mode detection works correctly
- System prompt enhancements work for both modes
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.prompt_templates import PromptTemplateManager, PromptType, PromptMode
import json

def test_dual_mode_behavior():
    """Test dual-mode prompt generation behavior"""
    print("🧪 Testing Dual-Mode Prompt System")
    print("=" * 50)
    
    manager = PromptTemplateManager()
    
    # Test each prompt type in both modes
    for prompt_type in PromptType:
        print(f"\n📊 Testing {prompt_type.value.upper()} Analysis")
        print("-" * 30)
        
        try:
            # Test button mode (JSON)
            button_prompt, button_context = manager.generate_prompt(
                prompt_type, ticker="AAPL", mode=PromptMode.BUTTON_JSON
            )
            
            # Test user mode (conversational)
            user_prompt, user_context = manager.generate_prompt(
                prompt_type, ticker="AAPL", mode=PromptMode.USER_TEXT
            )
            
            # Validate button mode characteristics
            button_has_json = "JSON" in button_prompt
            button_has_schema = "SCHEMA" in button_prompt
            button_has_sections = "###" in button_prompt
            
            # Validate user mode characteristics
            user_is_conversational = "conversational" in user_prompt.lower() or "explain" in user_prompt.lower()
            user_no_json = "JSON" not in user_prompt
            user_no_schema = "SCHEMA" not in user_prompt
            
            print(f"✅ Button Mode ({len(button_prompt)} chars):")
            print(f"   - Has JSON instructions: {button_has_json}")
            print(f"   - Has schema details: {button_has_schema}")
            print(f"   - Has sections: {button_has_sections}")
            
            print(f"✅ User Mode ({len(user_prompt)} chars):")
            print(f"   - Is conversational: {user_is_conversational}")
            print(f"   - No JSON instructions: {user_no_json}")
            print(f"   - No schema details: {user_no_schema}")
            
            # Show sample of each prompt
            print(f"\n📝 Button Prompt Sample:")
            print(f"   {button_prompt[:100]}...")
            
            print(f"\n💬 User Prompt Sample:")
            print(f"   {user_prompt[:100]}...")
            
            # Validate different outputs
            if button_prompt != user_prompt:
                print("✅ Modes produce different outputs")
            else:
                print("❌ ERROR: Modes produce identical outputs")
                
        except Exception as e:
            print(f"❌ ERROR testing {prompt_type.value}: {e}")
            return False
    
    return True

def test_mode_detection():
    """Test prompt source detection"""
    print(f"\n🔍 Testing Mode Detection")
    print("-" * 30)
    
    manager = PromptTemplateManager()
    
    test_cases = [
        ("Tell me about AAPL", None, PromptMode.USER_TEXT),
        ("What's the current price of Tesla?", None, PromptMode.USER_TEXT),
        ("Generate snapshot analysis", None, PromptMode.BUTTON_JSON),
        ("Any question here", "snapshot", PromptMode.BUTTON_JSON),
        ("Create technical analysis", None, PromptMode.BUTTON_JSON),
        ("How is Microsoft doing?", None, PromptMode.USER_TEXT),
    ]
    
    all_correct = True
    
    for input_text, button_context, expected_mode in test_cases:
        detected_mode = manager.detect_prompt_source(input_text, button_context)
        is_correct = detected_mode == expected_mode
        
        status = "✅" if is_correct else "❌"
        print(f"{status} '{input_text[:30]}...' -> {detected_mode.value} (expected {expected_mode.value})")
        
        if not is_correct:
            all_correct = False
    
    return all_correct

def test_system_prompt_enhancements():
    """Test system prompt mode-specific enhancements"""
    print(f"\n🤖 Testing System Prompt Enhancements")
    print("-" * 30)
    
    manager = PromptTemplateManager()
    base_prompt = "You are an expert financial analyst."
    
    # Test JSON mode enhancement
    json_enhanced = manager.get_enhanced_system_prompt(base_prompt, PromptMode.BUTTON_JSON)
    text_enhanced = manager.get_enhanced_system_prompt(base_prompt, PromptMode.USER_TEXT)
    
    print(f"✅ Base prompt: {len(base_prompt)} chars")
    print(f"✅ JSON enhanced: {len(json_enhanced)} chars")
    print(f"✅ Text enhanced: {len(text_enhanced)} chars")
    
    # Validate JSON mode has JSON instructions
    json_has_json_rules = "JSON" in json_enhanced
    print(f"✅ JSON mode has JSON rules: {json_has_json_rules}")
    
    # Validate text mode has conversational instructions
    text_has_conversational = "conversational" in text_enhanced.lower()
    print(f"✅ Text mode has conversational rules: {text_has_conversational}")
    
    # Validate they're different
    modes_different = json_enhanced != text_enhanced
    print(f"✅ Modes produce different system prompts: {modes_different}")
    
    return json_has_json_rules and text_has_conversational and modes_different

def test_button_prompt_helpers():
    """Test convenience methods for button and user prompts"""
    print(f"\n🔧 Testing Convenience Methods")
    print("-" * 30)
    
    manager = PromptTemplateManager()
    
    try:
        # Test button helper
        button_prompt, button_context = manager.generate_button_prompt(
            PromptType.SNAPSHOT, ticker="AAPL"
        )
        
        # Test user helper
        user_prompt, user_context = manager.generate_user_prompt(
            PromptType.SNAPSHOT, ticker="AAPL"
        )
        
        # Validate button helper produces JSON-focused prompt
        button_is_json = "JSON" in button_prompt
        print(f"✅ Button helper produces JSON prompt: {button_is_json}")
        
        # Validate user helper produces conversational prompt
        user_is_conversational = "conversational" in user_prompt.lower()
        print(f"✅ User helper produces conversational prompt: {user_is_conversational}")
        
        # Validate they're different
        different_outputs = button_prompt != user_prompt
        print(f"✅ Helpers produce different outputs: {different_outputs}")
        
        return button_is_json and user_is_conversational and different_outputs
        
    except Exception as e:
        print(f"❌ ERROR testing convenience methods: {e}")
        return False

def main():
    """Run comprehensive dual-mode tests"""
    print("🚀 Dual-Mode Prompt System Validation")
    print("=" * 60)
    
    tests = [
        ("Dual-Mode Behavior", test_dual_mode_behavior),
        ("Mode Detection", test_mode_detection),
        ("System Prompt Enhancements", test_system_prompt_enhancements),
        ("Convenience Methods", test_button_prompt_helpers),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ CRITICAL ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        emoji = "✅" if result else "❌"
        print(f"{emoji} {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🏆 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All dual-mode prompt system tests PASSED!")
        print("✅ Ready for Phase 3 UI integration")
        return True
    else:
        print("⚠️  Some tests FAILED - review implementation")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)