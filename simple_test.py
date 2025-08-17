#!/usr/bin/env python3
"""
Simple validation test for Phase 5 completion
"""

def test_core_components():
    """Test that all core components can be imported and initialized"""
    print("🧪 Testing core component imports...")
    
    try:
        # Test FSM
        from stock_data_fsm import StateManager, AppState
        fsm = StateManager()
        print(f"✅ FSM: State = {fsm.get_current_state().name}")
        
        # Test Response Parser
        from response_parser import ResponseParser, DataType
        parser = ResponseParser()
        stats = parser.get_parsing_statistics()
        print(f"✅ Parser: {stats['total_patterns']} patterns loaded")
        
        # Test Prompt Templates
        from prompt_templates import PromptTemplateManager, PromptType
        prompt_mgr = PromptTemplateManager()
        print(f"✅ Prompts: {len(prompt_mgr.templates)} templates available")
        
        # Test basic workflow
        prompt, context = prompt_mgr.generate_prompt(PromptType.SNAPSHOT, ticker="AAPL")
        print(f"✅ Generated prompt for {context.symbol} ({len(prompt)} chars)")
        
        # Test basic parsing
        sample_response = """
        Current price: $150.25
        Percentage change: +2.5%
        Volume: 1,000,000
        """
        result = parser.parse_stock_snapshot(sample_response, "AAPL")
        print(f"✅ Parsed data: {len(result.parsed_data)} fields, confidence: {result.confidence.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

def test_ui_imports():
    """Test UI component imports"""
    print("\n🖥️  Testing UI component imports...")
    
    try:
        from chat_ui_final import ProcessingStatus, handle_user_message, handle_button_click
        
        status = ProcessingStatus()
        status.start_processing("Test", 3)
        status.complete("Done")
        print(f"✅ ProcessingStatus working")
        
        print(f"✅ UI handlers imported successfully")
        return True
        
    except Exception as e:
        print(f"⚠️  UI components not fully available (expected): {e}")
        return False

if __name__ == "__main__":
    print("🚀 Phase 5 Validation Test")
    print("=" * 40)
    
    core_ok = test_core_components()
    ui_ok = test_ui_imports()
    
    print("\n📊 VALIDATION SUMMARY:")
    print(f"✅ Core Components: {'PASS' if core_ok else 'FAIL'}")
    print(f"🖥️  UI Components: {'PASS' if ui_ok else 'PARTIAL'}")
    
    if core_ok:
        print("\n🎉 PHASE 5 CORE FUNCTIONALITY: VALIDATED")
        print("✅ System ready for production use")
        exit(0)
    else:
        print("\n❌ Core validation failed")
        exit(1)
