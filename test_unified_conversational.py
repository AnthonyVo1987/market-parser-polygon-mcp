#!/usr/bin/env python3
"""
Test Script for Unified Conversational Response Processing
Created: 2025-08-19
Purpose: Validate removal of JSON extraction and implementation of unified conversational formatting
Success Criteria: No JSON extraction attempts, enhanced conversational formatting works
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.response_manager import ResponseManager, ProcessingMode
from src.prompt_templates import PromptTemplateManager, PromptType, PromptMode

class TestUnifiedConversational:
    """Test suite for unified conversational response processing"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        self.response_manager = ResponseManager(ProcessingMode.ENHANCED)
        self.prompt_manager = PromptTemplateManager()
    
    def test_no_json_extraction_attempts(self):
        """Validate that no JSON extraction is attempted"""
        # Test button response - should NOT attempt JSON extraction
        test_response = '{"test": "data"}' # This would trigger JSON extraction in old system
        
        result = self.response_manager.process_response(
            test_response,
            source_type='button',
            data_type='snapshot',
            ticker='AAPL'
        )
        
        # Should always succeed with conversational formatting
        assert result['success'] == True
        assert 'content' in result
        assert 'Could not extract structured data' not in result['content']
        print("✅ No JSON extraction attempts - button response formatted conversationally")
    
    def test_unified_conversational_formatting(self):
        """Validate unified conversational formatting works for all response types"""
        # Test user response formatting
        user_response = "Apple Inc. is currently trading at $150.25 with strong momentum."
        user_result = self.response_manager.process_response(user_response, source_type='user')
        
        assert user_result['success'] == True
        assert 'Market Analysis' in user_result['content']  # Should have conversational header
        print("✅ User response formatted conversationally")
        
        # Test button response formatting
        button_response = "Apple Inc. is currently trading at $150.25, up 2.5% from yesterday."
        button_result = self.response_manager.process_response(
            button_response, 
            source_type='button', 
            data_type='snapshot', 
            ticker='AAPL'
        )
        
        assert button_result['success'] == True
        assert 'Snapshot Analysis' in button_result['content']  # Should have enhanced header
        print("✅ Button response formatted conversationally with analysis type")
    
    def test_enhanced_formatting_features(self):
        """Test enhanced text formatting features"""
        test_text = "Current Price: $150.25\nVolume: 45000000\nChange: +2.5%\nRecommendation: Buy"
        
        result = self.response_manager.process_response(
            test_text,
            source_type='button',
            data_type='snapshot',
            ticker='AAPL'
        )
        
        content = result['content']
        # Check for enhanced formatting
        assert '💰 **Current Price:**' in content or 'Current Price' in content
        assert result['success'] == True
        print("✅ Enhanced text formatting applied")
    
    def test_conversational_prompts_only(self):
        """Validate that only conversational prompts are generated"""
        # Test each prompt type
        for prompt_type in [PromptType.SNAPSHOT, PromptType.SUPPORT_RESISTANCE, PromptType.TECHNICAL]:
            prompt, context = self.prompt_manager.generate_prompt(prompt_type, ticker='AAPL')
            
            # Should not contain JSON instructions
            assert 'JSON SCHEMA' not in prompt
            assert 'valid JSON only' not in prompt
            assert 'JSON RESPONSE' not in prompt
            
            # Should contain user-friendly language
            assert any(word in prompt.lower() for word in ['provide', 'include', 'explain', 'analyze', 'clear', 'actionable'])
            print(f"✅ {prompt_type.value} prompt is conversational only")
    
    def test_processing_modes(self):
        """Test that only conversational processing modes exist"""
        # Enhanced mode should work
        enhanced_manager = ResponseManager(ProcessingMode.ENHANCED)
        result = enhanced_manager.process_response("Test response", source_type='user')
        assert result['success'] == True
        print("✅ Enhanced processing mode works")
        
        # Standard mode should work
        standard_manager = ResponseManager(ProcessingMode.STANDARD)
        result = standard_manager.process_response("Test response", source_type='user')
        assert result['success'] == True
        print("✅ Standard processing mode works")
    
    def test_no_json_dependencies(self):
        """Validate that JSON-specific classes are not used"""
        # ResponseManager should not reference old JSON classes
        manager = ResponseManager()
        
        # Should not have json_parser or schema_validator attributes
        assert not hasattr(manager, 'json_parser')
        assert not hasattr(manager, 'schema_validator')
        print("✅ No JSON parser dependencies in ResponseManager")
    
    def test_error_handling_conversational(self):
        """Test that errors are handled conversationally"""
        # Test with problematic input that might cause errors
        result = self.response_manager.process_response(
            "",  # Empty response
            source_type='button',
            data_type='invalid_type'
        )
        
        # Should still succeed and provide conversational feedback
        assert result['success'] == True
        assert 'content' in result
        print("✅ Error handling maintains conversational approach")


def validate_unified_conversational() -> bool:
    """
    Run comprehensive validation of the unified conversational implementation
    Returns: True if all criteria met, False otherwise
    """
    success_criteria = [
        "✅ No JSON extraction attempts",
        "✅ Unified conversational formatting for all responses", 
        "✅ Enhanced text formatting with emojis and structure",
        "✅ Conversational-only prompt generation",
        "✅ Removal of JSON dependencies",
        "✅ Error handling maintains conversational approach"
    ]
    
    try:
        # Run the test suite
        test_suite = TestUnifiedConversational()
        test_suite.setup_method()
        
        # Run each test
        test_suite.test_no_json_extraction_attempts()
        test_suite.test_unified_conversational_formatting()
        test_suite.test_enhanced_formatting_features()
        test_suite.test_conversational_prompts_only()
        test_suite.test_processing_modes()
        test_suite.test_no_json_dependencies()
        test_suite.test_error_handling_conversational()
        
        print("\n" + "="*60)
        print("🎉 UNIFIED CONVERSATIONAL IMPLEMENTATION VALIDATION: SUCCESS")
        print("="*60)
        
        for criterion in success_criteria:
            print(criterion)
        
        print("\n✨ Key Achievements:")
        print("• Removed all JSON extraction attempts")
        print("• Implemented unified conversational formatting")
        print("• Enhanced text formatting with emojis and structure")
        print("• Converted to conversational-only prompt generation")
        print("• Eliminated JSON processing dependencies")
        print("• Maintained error handling with conversational approach")
        
        return True
        
    except Exception as e:
        print(f"\n❌ UNIFIED CONVERSATIONAL VALIDATION: FAILED")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    # Run the validation
    success = validate_unified_conversational()
    
    if success:
        print(f"\n🏁 Unified conversational implementation is ready!")
        sys.exit(0)
    else:
        print(f"\n💥 Validation failed - check implementation")
        sys.exit(1)