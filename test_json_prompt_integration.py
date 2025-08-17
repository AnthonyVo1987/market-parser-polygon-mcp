#!/usr/bin/env python3
"""
JSON Response Generation System Integration Test

This test validates that the JSON prompt system integrates properly with the 
existing prompt templates and JSON schemas designed by the API architect.
"""

import json
import sys
import traceback
from datetime import datetime
from typing import Dict, Any

from prompt_templates import (
    PromptTemplateManager, 
    PromptType, 
    TickerContext
)
from json_schemas import (
    schema_registry,
    AnalysisType,
    generate_example_responses
)


def test_json_prompt_generation() -> Dict[str, Any]:
    """Test that JSON prompts are generated correctly for all analysis types"""
    print("🧪 Testing JSON Prompt Generation...")
    
    manager = PromptTemplateManager()
    results = {
        "test_name": "json_prompt_generation",
        "passed": True,
        "details": {},
        "issues": []
    }
    
    test_ticker = "AAPL"
    
    for prompt_type in PromptType:
        try:
            prompt, context = manager.generate_prompt(prompt_type, ticker=test_ticker)
            
            # Validate prompt contains JSON requirements
            has_json_requirements = (
                "JSON" in prompt and 
                "schema" in prompt.lower() and
                "CRITICAL RESPONSE REQUIREMENTS" in prompt
            )
            
            # Validate context
            context_valid = (
                context.symbol == test_ticker and
                context.confidence > 0 and
                context.source == "explicit"
            )
            
            results["details"][prompt_type.value] = {
                "prompt_length": len(prompt),
                "has_json_requirements": has_json_requirements,
                "context_valid": context_valid,
                "success": True
            }
            
            if not has_json_requirements:
                results["issues"].append(f"{prompt_type.value}: Missing JSON requirements")
                results["passed"] = False
                
            if not context_valid:
                results["issues"].append(f"{prompt_type.value}: Invalid context")
                results["passed"] = False
                
        except Exception as e:
            results["details"][prompt_type.value] = {
                "success": False,
                "error": str(e)
            }
            results["issues"].append(f"{prompt_type.value}: {e}")
            results["passed"] = False
    
    return results


def test_schema_integration() -> Dict[str, Any]:
    """Test that JSON schemas are properly integrated"""
    print("📋 Testing Schema Integration...")
    
    manager = PromptTemplateManager()
    results = {
        "test_name": "schema_integration",
        "passed": True,
        "details": {},
        "issues": []
    }
    
    # Test schema availability
    schemas_info = manager.get_available_schemas()
    results["details"]["registry_available"] = schemas_info["available"]
    
    if not schemas_info["available"]:
        results["issues"].append("Schema registry not available")
        results["passed"] = False
    
    # Test each schema type
    for schema_type, info in schemas_info["schemas"].items():
        results["details"][f"schema_{schema_type}"] = info
        
        if not info["available"]:
            results["issues"].append(f"Schema {schema_type} not available")
            results["passed"] = False
        
        if info["fallback_used"]:
            results["issues"].append(f"Schema {schema_type} using fallback")
    
    return results


def test_example_json_generation() -> Dict[str, Any]:
    """Test that example JSON responses are valid"""
    print("💾 Testing Example JSON Generation...")
    
    results = {
        "test_name": "example_json_generation",
        "passed": True,
        "details": {},
        "issues": []
    }
    
    # Generate examples from the API architect's system
    try:
        examples = generate_example_responses()
        
        for example_type, example_data in examples.items():
            if example_type == "error":
                continue  # Skip error example for this test
                
            try:
                # Test JSON serialization round-trip
                json_str = json.dumps(example_data, indent=2)
                parsed_back = json.loads(json_str)
                
                # Validate required fields
                required_checks = {
                    "has_metadata": "metadata" in parsed_back,
                    "has_timestamp": "metadata" in parsed_back and "timestamp" in parsed_back["metadata"],
                    "has_ticker": "metadata" in parsed_back and "ticker_symbol" in parsed_back["metadata"],
                    "has_schema_version": "metadata" in parsed_back and "schema_version" in parsed_back["metadata"]
                }
                
                all_checks_passed = all(required_checks.values())
                
                results["details"][example_type] = {
                    "json_valid": True,
                    "size_bytes": len(json_str),
                    "required_fields": required_checks,
                    "all_checks_passed": all_checks_passed
                }
                
                if not all_checks_passed:
                    results["issues"].append(f"{example_type}: Missing required fields")
                    results["passed"] = False
                    
            except json.JSONDecodeError as e:
                results["details"][example_type] = {
                    "json_valid": False,
                    "error": str(e)
                }
                results["issues"].append(f"{example_type}: Invalid JSON - {e}")
                results["passed"] = False
                
    except Exception as e:
        results["issues"].append(f"Failed to generate examples: {e}")
        results["passed"] = False
    
    return results


def test_system_prompt_integration() -> Dict[str, Any]:
    """Test that system prompts are enhanced for JSON output"""
    print("🤖 Testing System Prompt Integration...")
    
    manager = PromptTemplateManager()
    results = {
        "test_name": "system_prompt_integration",
        "passed": True,
        "details": {},
        "issues": []
    }
    
    base_prompt = "You are a financial analyst."
    
    try:
        enhanced_prompt = manager.get_enhanced_system_prompt(base_prompt)
        
        # Check for JSON-specific enhancements
        json_checks = {
            "has_base_prompt": base_prompt in enhanced_prompt,
            "has_json_requirements": "JSON" in enhanced_prompt,
            "has_schema_adherence": "schema" in enhanced_prompt.lower(),
            "has_data_types": "data types" in enhanced_prompt.lower(),
            "has_validation": "validation" in enhanced_prompt.lower()
        }
        
        all_checks_passed = all(json_checks.values())
        
        results["details"] = {
            "enhanced_length": len(enhanced_prompt),
            "original_length": len(base_prompt),
            "json_checks": json_checks,
            "all_checks_passed": all_checks_passed
        }
        
        if not all_checks_passed:
            results["issues"].append("Enhanced system prompt missing JSON requirements")
            results["passed"] = False
            
    except Exception as e:
        results["issues"].append(f"System prompt enhancement failed: {e}")
        results["passed"] = False
    
    return results


def run_comprehensive_tests() -> Dict[str, Any]:
    """Run all JSON response generation system tests"""
    print("🚀 JSON Response Generation System - Comprehensive Tests")
    print("=" * 60)
    
    all_results = {
        "test_suite": "json_response_generation_system",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "overall_passed": True,
        "tests": {},
        "summary": {}
    }
    
    # Run all tests
    test_functions = [
        test_json_prompt_generation,
        test_schema_integration,
        test_example_json_generation,
        test_system_prompt_integration
    ]
    
    for test_func in test_functions:
        try:
            result = test_func()
            test_name = result["test_name"]
            all_results["tests"][test_name] = result
            
            if not result["passed"]:
                all_results["overall_passed"] = False
                
            # Print test result
            status = "✅ PASSED" if result["passed"] else "❌ FAILED"
            print(f"{status} {test_name}")
            
            if result["issues"]:
                for issue in result["issues"]:
                    print(f"   ⚠️  {issue}")
                    
        except Exception as e:
            print(f"❌ FAILED {test_func.__name__}: {e}")
            traceback.print_exc()
            all_results["overall_passed"] = False
    
    # Generate summary
    total_tests = len(test_functions)
    passed_tests = sum(1 for t in all_results["tests"].values() if t["passed"])
    
    all_results["summary"] = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": total_tests - passed_tests,
        "success_rate": passed_tests / total_tests if total_tests > 0 else 0.0
    }
    
    print("\n" + "=" * 60)
    print(f"📊 Test Summary:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    print(f"   Success Rate: {all_results['summary']['success_rate']:.1%}")
    
    if all_results["overall_passed"]:
        print("🎉 All tests passed! JSON Response Generation System is ready.")
    else:
        print("🔧 Some tests failed. Review issues above.")
    
    return all_results


if __name__ == "__main__":
    try:
        results = run_comprehensive_tests()
        
        # Exit with appropriate code
        sys.exit(0 if results["overall_passed"] else 1)
        
    except Exception as e:
        print(f"💥 Test suite failed with error: {e}")
        traceback.print_exc()
        sys.exit(1)