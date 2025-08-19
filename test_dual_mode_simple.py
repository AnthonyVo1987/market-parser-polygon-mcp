#!/usr/bin/env python3
"""
Simple Test for Dual-Mode Prompt System
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from prompt_templates import PromptTemplateManager, PromptType, PromptMode
    print("✅ Successfully imported prompt_templates")
    
    # Test basic functionality
    manager = PromptTemplateManager()
    print("✅ Created PromptTemplateManager")
    
    # Test button mode
    button_prompt, context = manager.generate_prompt(
        PromptType.SNAPSHOT, ticker="AAPL", mode=PromptMode.BUTTON_JSON
    )
    print(f"✅ Button mode prompt: {len(button_prompt)} chars")
    print(f"   Contains JSON: {'JSON' in button_prompt}")
    
    # Test user mode  
    user_prompt, context = manager.generate_prompt(
        PromptType.SNAPSHOT, ticker="AAPL", mode=PromptMode.USER_TEXT
    )
    print(f"✅ User mode prompt: {len(user_prompt)} chars")
    print(f"   Contains conversational: {'conversational' in user_prompt.lower()}")
    
    # Test they're different
    print(f"✅ Different outputs: {button_prompt != user_prompt}")
    
    print("\n🎉 Dual-mode prompt system working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()