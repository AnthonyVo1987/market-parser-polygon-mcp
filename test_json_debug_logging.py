#!/usr/bin/env python3
"""
Test Script for Comprehensive JSON Debug Logging

This script validates that the comprehensive JSON debug logging system
is working correctly by simulating the JSON workflow with test data.

Usage:
    python test_json_debug_logging.py
"""

import json
import time
import logging
from json_debug_logger import json_debug_logger, create_workflow_id

def test_json_workflow_logging():
    """Test the complete JSON workflow logging system"""
    
    print("🧪 Testing Comprehensive JSON Debug Logging System")
    print("=" * 60)
    
    # Test 1: Basic workflow creation and tracking
    print("\n📋 Test 1: Workflow Creation and Tracking")
    workflow_id = create_workflow_id("snapshot", "AAPL")
    print(f"Created workflow ID: {workflow_id}")
    
    # Sample AI response for testing
    test_response = """{
    "snapshot_data": {
        "current_price": 175.43,
        "percentage_change": 2.1,
        "dollar_change": 3.61,
        "volume": 45623890,
        "vwap": 174.82,
        "open": 173.20,
        "high": 176.15,
        "low": 172.85,
        "close": 171.82
    },
    "metadata": {
        "confidence_score": 0.95,
        "data_timestamp": "2025-08-17T15:30:00Z",
        "source": "polygon_api"
    }
}"""
    
    # Start workflow
    metrics = json_debug_logger.start_json_workflow(
        workflow_id, "snapshot", "AAPL", test_response
    )
    print("✅ Workflow started successfully")
    
    # Test 2: JSON extraction logging
    print("\n📋 Test 2: JSON Extraction Logging")
    time.sleep(0.015)  # Simulate extraction time
    
    try:
        extracted_json = json.loads(test_response)
        json_debug_logger.log_json_extraction(
            workflow_id, 15.2, extracted_json, "direct_parse", True
        )
        print("✅ JSON extraction logged successfully")
    except Exception as e:
        print(f"❌ JSON extraction test failed: {e}")
        return False
    
    # Test 3: Schema validation logging
    print("\n📋 Test 3: Schema Validation Logging")
    time.sleep(0.008)  # Simulate validation time
    
    validation_result = {
        'valid': True,
        'schema_version': '1.0.0',
        'validation_timestamp': '2025-08-17T15:30:00Z',
        'error_message': None
    }
    
    json_debug_logger.log_schema_validation(
        workflow_id, 8.1, validation_result, "snapshot"
    )
    print("✅ Schema validation logged successfully")
    
    # Test 4: Parsing results logging
    print("\n📋 Test 4: Parsing Results Logging")
    time.sleep(0.025)  # Simulate parsing time
    
    class MockParseResult:
        def __init__(self):
            self.matched_patterns = ['price_pattern', 'volume_pattern', 'change_pattern']
            self.failed_patterns = ['vwap_pattern']
    
    mock_result = MockParseResult()
    json_debug_logger.log_parsing_results(
        workflow_id, 24.8, mock_result, "high", 9, ["Minor precision loss in VWAP calculation"]
    )
    print("✅ Parsing results logged successfully")
    
    # Test 5: DataFrame conversion logging
    print("\n📋 Test 5: DataFrame Conversion Logging")
    time.sleep(0.012)  # Simulate conversion time
    
    json_debug_logger.log_dataframe_conversion(
        workflow_id, 11.5, (9, 2), True, 487, ["snapshot_data", "metadata"]
    )
    print("✅ DataFrame conversion logged successfully")
    
    # Test 6: FSM state transition logging
    print("\n📋 Test 6: FSM State Transition Logging")
    
    json_debug_logger.log_fsm_state_transition(
        workflow_id, "parse", "parse_success", "parsing_complete",
        {"confidence": "high", "field_count": 9, "json_valid": True}
    )
    print("✅ FSM state transition logged successfully")
    
    # Test 7: Raw JSON output logging
    print("\n📋 Test 7: Raw JSON Output Logging")
    
    formatted_json = json.dumps(extracted_json, indent=2)
    json_debug_logger.log_raw_json_output(
        workflow_id, "snapshot", formatted_json, True
    )
    print("✅ Raw JSON output logged successfully")
    
    # Test 8: Complete workflow
    print("\n📋 Test 8: Workflow Completion")
    
    final_metrics = json_debug_logger.complete_workflow(
        workflow_id, "high", 9, True
    )
    print(f"✅ Workflow completed. Final metrics: {final_metrics}")
    
    # Test 9: Error condition logging
    print("\n📋 Test 9: Error Condition Logging")
    
    error_workflow_id = create_workflow_id("technical", "INVALID")
    error_response = "Invalid response from API"
    
    json_debug_logger.start_json_workflow(
        error_workflow_id, "technical", "INVALID", error_response
    )
    
    try:
        raise ValueError("Test error for logging")
    except Exception as e:
        error_context = {
            'button_type': 'technical',
            'ticker': 'INVALID',
            'response_size': len(error_response),
            'error_step': 'json_extraction'
        }
        json_debug_logger.log_error_condition(error_workflow_id, e, error_context)
        print("✅ Error condition logged successfully")
    
    # Test 10: Cleanup test
    print("\n📋 Test 10: Workflow Cleanup")
    
    active_workflows = json_debug_logger.get_active_workflows()
    print(f"Active workflows before cleanup: {len(active_workflows)}")
    
    json_debug_logger.cleanup_stale_workflows(max_age_seconds=1)
    
    active_workflows_after = json_debug_logger.get_active_workflows()
    print(f"Active workflows after cleanup: {len(active_workflows_after)}")
    print("✅ Workflow cleanup tested successfully")
    
    return True

def test_workflow_id_generation():
    """Test workflow ID generation"""
    print("\n📋 Testing Workflow ID Generation")
    
    # Test various scenarios
    test_cases = [
        ("snapshot", "AAPL"),
        ("support_resistance", "GOOGL"),
        ("technical", "TSLA"),
        ("snapshot", "BRK.A"),  # Test with dots
        ("technical", ""),       # Test with empty ticker
    ]
    
    generated_ids = []
    for button_type, ticker in test_cases:
        workflow_id = create_workflow_id(button_type, ticker)
        generated_ids.append(workflow_id)
        print(f"  {button_type} + {ticker or 'empty'} → {workflow_id}")
        time.sleep(0.001)  # Ensure unique timestamps
    
    # Verify uniqueness
    if len(generated_ids) == len(set(generated_ids)):
        print("✅ All workflow IDs are unique")
        return True
    else:
        print("❌ Duplicate workflow IDs detected")
        return False

def test_log_file_creation():
    """Test that log files are created properly"""
    print("\n📋 Testing Log File Creation")
    
    import os
    
    # Check if the log files exist or get created
    log_files = [
        'json_workflow_debug.log',
        'comprehensive_json_debug.log'
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"✅ Log file exists: {log_file}")
        else:
            print(f"⚠️  Log file not found (will be created on first use): {log_file}")
    
    # Test writing to logger
    json_debug_logger.logger.info("🧪 Test log entry from test script")
    
    return True

def main():
    """Main test function"""
    print("🔍 Comprehensive JSON Debug Logging Test Suite")
    print("=" * 60)
    
    # Configure logging for test
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('test_json_debug.log', mode='w')
        ]
    )
    
    # Run tests
    tests = [
        ("Workflow ID Generation", test_workflow_id_generation),
        ("Log File Creation", test_log_file_creation),
        ("JSON Workflow Logging", test_json_workflow_logging),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ PASSED: {test_name}")
                passed += 1
            else:
                print(f"❌ FAILED: {test_name}")
        except Exception as e:
            print(f"💥 ERROR in {test_name}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! JSON debug logging system is ready.")
        print("📄 Check test_json_debug.log for detailed test output")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)