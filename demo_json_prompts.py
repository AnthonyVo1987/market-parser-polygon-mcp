#!/usr/bin/env python3
"""
JSON Response Generation System Demo

This script demonstrates the new JSON-based prompt generation system
that integrates with the API architect's schemas.
"""

import json
from prompt_templates import PromptTemplateManager, PromptType

def demo_json_prompts():
    """Demonstrate JSON prompt generation for all analysis types"""
    
    print("🚀 JSON Response Generation System Demo")
    print("=" * 60)
    
    manager = PromptTemplateManager()
    
    # Test ticker
    ticker = "AAPL"
    
    print(f"📊 Generating JSON prompts for {ticker}...\n")
    
    for prompt_type in PromptType:
        print(f"🔍 {prompt_type.value.upper()} ANALYSIS")
        print("-" * 40)
        
        # Generate the JSON prompt
        prompt, context = manager.generate_prompt(prompt_type, ticker=ticker)
        
        # Show key sections of the prompt
        sections = prompt.split("###")
        
        for section in sections[:4]:  # Show first few sections
            if section.strip():
                title = section.split('\n')[0].strip()
                if title:
                    print(f"📋 {title}")
                    
                    # Show a preview of the content
                    content_lines = section.split('\n')[1:6]  # First 5 lines
                    for line in content_lines:
                        if line.strip():
                            print(f"   {line.strip()[:80]}{'...' if len(line.strip()) > 80 else ''}")
                    print()
        
        print(f"📏 Total prompt size: {len(prompt):,} characters")
        print(f"🎯 Context: {context.symbol} ({context.source}, confidence: {context.confidence})")
        print("\n" + "="*60 + "\n")

def demo_schema_availability():
    """Show schema availability and integration status"""
    
    print("📋 Schema Integration Status")
    print("=" * 40)
    
    manager = PromptTemplateManager()
    schemas_info = manager.get_available_schemas()
    
    print(f"Schema Registry: {'✅ Available' if schemas_info['available'] else '❌ Not Available'}")
    print()
    
    for schema_type, info in schemas_info['schemas'].items():
        status_icon = "✅" if info['available'] else "⚠️"
        fallback_note = " (using fallback)" if info['fallback_used'] else ""
        
        print(f"{status_icon} {schema_type.upper()}")
        print(f"   Schema ID: {info.get('schema_id', 'N/A')}")
        print(f"   Status: {'Available' if info['available'] else 'Missing'}{fallback_note}")
        print()

def demo_system_prompt_enhancement():
    """Show how system prompts are enhanced for JSON"""
    
    print("🤖 System Prompt Enhancement Demo")
    print("=" * 50)
    
    manager = PromptTemplateManager()
    
    base_prompt = "You are an expert financial analyst."
    enhanced_prompt = manager.get_enhanced_system_prompt(base_prompt)
    
    print("📝 Original System Prompt:")
    print(f'   "{base_prompt}"')
    print()
    
    print("🔧 Enhanced System Prompt (showing JSON additions):")
    enhancement_part = enhanced_prompt.replace(base_prompt, "").strip()
    
    # Show key lines from the enhancement
    lines = enhancement_part.split('\n')
    for line in lines[:15]:  # First 15 lines of enhancement
        if line.strip():
            print(f"   {line}")
    
    if len(lines) > 15:
        print(f"   ... and {len(lines) - 15} more lines")
    
    print()
    print(f"📏 Enhancement added {len(enhancement_part)} characters")

if __name__ == "__main__":
    # Run all demos
    demo_json_prompts()
    demo_schema_availability()
    demo_system_prompt_enhancement()
    
    print("🎉 JSON Response Generation System Demo Complete!")
    print("Ready for production integration with AI agents.")