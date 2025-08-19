#!/usr/bin/env python3
"""
Test Script for OpenAI Model Migration - gpt-5-nano to gpt-5-mini
Created: 2025-08-19
Purpose: Validate successful migration to gpt-5-mini with new pricing structure
Success Criteria: 
- Model correctly set to gpt-5-mini
- Pricing environment variables work correctly
- TokenCostTracker uses new pricing structure
- Both CLI and GUI use correct model
"""

import os
import pytest
import sys
from unittest.mock import patch, MagicMock
from typing import List, Dict, Any

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_model_name_migration():
    """Test that both CLI and GUI use gpt-5-mini by default"""
    
    # Test CLI model configuration
    from market_parser_demo import cli_async
    import market_parser_demo
    
    # Check the hardcoded model name in CLI
    # Read the file content to check model initialization
    with open('market_parser_demo.py', 'r') as f:
        content = f.read()
        assert "OpenAIResponsesModel('gpt-5-mini')" in content
        assert "OpenAIResponsesModel('gpt-5-nano')" not in content
    
    # Test GUI model configuration
    import chat_ui
    
    # Test that GUI uses correct default model
    with patch.dict(os.environ, {}, clear=True):
        from chat_ui import MODEL_NAME
        assert MODEL_NAME == "gpt-5-mini", f"Expected gpt-5-mini, got {MODEL_NAME}"
    
    print("✅ Model name migration: SUCCESS")


def test_pricing_environment_variables():
    """Test that TokenCostTracker uses new gpt-5-mini pricing variables"""
    from market_parser_demo import TokenCostTracker
    
    # Test with gpt-5-mini specific pricing
    test_env = {
        'OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M': '0.25',
        'OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M': '2.00'
    }
    
    with patch.dict(os.environ, test_env, clear=True):
        tracker = TokenCostTracker()
        
        # Verify new pricing variables are used
        assert tracker.input_price_per_million == 0.25, f"Expected 0.25, got {tracker.input_price_per_million}"
        assert tracker.output_price_per_million == 2.00, f"Expected 2.00, got {tracker.output_price_per_million}"
    
    print("✅ Pricing environment variables: SUCCESS")


def test_cost_calculations():
    """Test that cost calculations work correctly with new pricing"""
    from market_parser_demo import TokenCostTracker
    
    test_env = {
        'OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M': '0.25',
        'OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M': '2.00'
    }
    
    with patch.dict(os.environ, test_env, clear=True):
        tracker = TokenCostTracker()
        
        # Test cost calculation for 1000 input tokens and 500 output tokens
        input_cost = tracker._calc_cost(1000, tracker.input_price_per_million, tracker.input_price_per_token)
        output_cost = tracker._calc_cost(500, tracker.output_price_per_million, tracker.output_price_per_token)
        
        # Expected costs:
        # Input: 1000 tokens * (0.25 / 1,000,000) = $0.00025
        # Output: 500 tokens * (2.00 / 1,000,000) = $0.001
        expected_input = 0.00025
        expected_output = 0.001
        
        assert abs(input_cost - expected_input) < 0.000001, f"Input cost calculation failed: {input_cost} != {expected_input}"
        assert abs(output_cost - expected_output) < 0.000001, f"Output cost calculation failed: {output_cost} != {expected_output}"
    
    print("✅ Cost calculations: SUCCESS")


def test_backward_compatibility():
    """Test that fallback pricing variables still work"""
    from market_parser_demo import TokenCostTracker
    
    # Test with generic fallback pricing (should be used when gpt-5-mini specific not available)
    test_env = {
        'OPENAI_INPUT_PRICE_PER_1M': '0.15',
        'OPENAI_OUTPUT_PRICE_PER_1M': '1.50'
    }
    
    with patch.dict(os.environ, test_env, clear=True):
        tracker = TokenCostTracker()
        
        # Should use fallback values when gpt-5-mini specific variables not set
        assert tracker.input_price_per_million == 0.15, f"Fallback pricing failed: {tracker.input_price_per_million}"
        assert tracker.output_price_per_million == 1.50, f"Fallback pricing failed: {tracker.output_price_per_million}"
    
    print("✅ Backward compatibility: SUCCESS")


def test_environment_file_update():
    """Test that .env.example has been updated correctly"""
    
    with open('.env.example', 'r') as f:
        content = f.read()
        
        # Check that new pricing variables exist
        assert 'OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25' in content
        assert 'OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00' in content
        
        # Check that model default is updated
        assert 'OPENAI_MODEL=gpt-5-mini' in content
        
        # Legacy pricing should still be present for backward compatibility
        assert 'OPENAI_GPT5_NANO_INPUT_PRICE_PER_1M=0.05' in content
        assert 'OPENAI_GPT5_NANO_OUTPUT_PRICE_PER_1M=0.40' in content
    
    print("✅ Environment file update: SUCCESS")


def test_cli_integration():
    """Test CLI integration with new model and pricing"""
    
    # Mock environment with gpt-5-mini pricing
    test_env = {
        'OPENAI_API_KEY': 'test-key',
        'POLYGON_API_KEY': 'test-polygon-key',
        'OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M': '0.25',
        'OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M': '2.00'
    }
    
    with patch.dict(os.environ, test_env, clear=True):
        from market_parser_demo import TokenCostTracker
        
        # Test that TokenCostTracker initializes with correct pricing
        tracker = TokenCostTracker()
        assert tracker.input_price_per_million == 0.25
        assert tracker.output_price_per_million == 2.00
    
    print("✅ CLI integration: SUCCESS")


def validate_migration_success() -> bool:
    """
    Run comprehensive validation of the gpt-5-mini migration
    Returns: True if all criteria met, False otherwise
    """
    success_criteria = [
        "Model name updated to gpt-5-mini in both CLI and GUI",
        "TokenCostTracker uses new OPENAI_GPT5_MINI_* environment variables", 
        "Cost calculations work correctly with new pricing (input: $0.25/1M, output: $2.00/1M)",
        "Backward compatibility maintained with fallback variables",
        "Environment file example updated with new defaults",
        "CLI integration works with new model configuration"
    ]
    
    try:
        test_model_name_migration()
        test_pricing_environment_variables()
        test_cost_calculations()
        test_backward_compatibility()
        test_environment_file_update()
        test_cli_integration()
        
        print(f"\n🎉 MIGRATION VALIDATION: SUCCESS")
        print("✅ All success criteria met:")
        for i, criterion in enumerate(success_criteria, 1):
            print(f"   {i}. {criterion}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ MIGRATION VALIDATION: FAILED - {str(e)}")
        return False


if __name__ == "__main__":
    # Run the validation suite
    print("🔄 Starting gpt-5-mini migration validation...")
    print("=" * 60)
    
    success = validate_migration_success()
    
    if success:
        print(f"\n✅ GPT-5-MINI MIGRATION: COMPLETE")
        print("🚀 Ready for Phase 2 re-architecture")
    else:
        print(f"\n❌ GPT-5-MINI MIGRATION: INCOMPLETE")
        print("🔧 Please check the failing tests and fix issues")
        sys.exit(1)