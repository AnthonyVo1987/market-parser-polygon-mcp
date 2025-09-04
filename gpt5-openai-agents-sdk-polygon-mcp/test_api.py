#!/usr/bin/env python3
"""
Simple API test script to validate the FastAPI endpoints.

This script tests the basic functionality of the prompt templates API
without requiring external services to be running.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from fastapi.testclient import TestClient
from src.main import app

def test_api_endpoints():
    """Test basic API endpoint functionality"""
    client = TestClient(app)
    
    print("🧪 Testing FastAPI Prompt Templates API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Status: {data['status']}")
    print(f"   ✓ Message: {data['message']}")
    
    # Test 2: API Health Check
    print("\n2. Testing API Health Check...")
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Status: {data['status']}")
    print(f"   ✓ Version: {data['version']}")
    
    # Test 3: Template List
    print("\n3. Testing Template List...")
    response = client.get("/api/v1/prompts/templates")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Mode: {data['mode']}")
    print(f"   ✓ Template count: {data['total_count']}")
    for template_name, template_info in data['templates'].items():
        print(f"   ✓ Template: {template_name} - Available: {template_info['available']}")
    
    # Test 4: System Status
    print("\n4. Testing System Status...")
    response = client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Status: {data['status']}")
    print(f"   ✓ API Version: {data['metrics']['api_version']}")
    print(f"   ✓ Templates Loaded: {data['metrics']['prompt_templates_loaded']}")
    
    # Test 5: Generate Prompt
    print("\n5. Testing Prompt Generation...")
    payload = {
        "template_type": "snapshot",
        "ticker": "AAPL",
        "custom_instructions": "Focus on recent performance",
        "mode": "conversational"
    }
    response = client.post("/api/v1/prompts/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Generated prompt length: {len(data['prompt'])} characters")
    print(f"   ✓ Ticker detected: {data['ticker_context']['symbol']}")
    print(f"   ✓ Confidence: {data['ticker_context']['confidence']}")
    print(f"   ✓ Template type: {data['template_type']}")
    
    # Test 6: Validation Error Handling
    print("\n6. Testing Validation Error Handling...")
    invalid_payload = {
        "template_type": "invalid_type",  # Invalid enum value
        "ticker": "TOOLONGTICKER"  # Invalid ticker
    }
    response = client.post("/api/v1/prompts/generate", json=invalid_payload)
    assert response.status_code == 422  # Validation error
    print("   ✓ Validation error handled correctly")
    
    print("\n🎉 All API tests passed successfully!")
    print("=" * 50)
    return True

def test_api_models():
    """Test API models functionality"""
    from src.api_models import (
        AnalysisType, PromptMode, GeneratePromptRequest, 
        ButtonAnalysisRequest, ChatAnalysisRequest
    )
    
    print("\n📊 Testing API Models")
    print("=" * 30)
    
    # Test enum values
    print("1. Testing enums...")
    print(f"   ✓ Analysis types: {[t.value for t in AnalysisType]}")
    print(f"   ✓ Prompt modes: {[m.value for m in PromptMode]}")
    
    # Test request validation
    print("\n2. Testing request validation...")
    try:
        request = GeneratePromptRequest(
            template_type=AnalysisType.SNAPSHOT,
            ticker="AAPL"
        )
        print(f"   ✓ Valid request created: {request.template_type}, {request.ticker}")
    except Exception as e:
        print(f"   ✗ Request validation failed: {e}")
        return False
    
    # Test button analysis request
    try:
        button_request = ButtonAnalysisRequest(
            ticker="TSLA",
            analysis_type=AnalysisType.TECHNICAL
        )
        print(f"   ✓ Button request created: {button_request.ticker}, {button_request.analysis_type}")
    except Exception as e:
        print(f"   ✗ Button request validation failed: {e}")
        return False
    
    # Test chat analysis request
    try:
        chat_request = ChatAnalysisRequest(
            message="What's the current price of Apple stock?"
        )
        print(f"   ✓ Chat request created: {len(chat_request.message)} chars")
    except Exception as e:
        print(f"   ✗ Chat request validation failed: {e}")
        return False
    
    print("\n✅ All API model tests passed!")
    return True

def test_integration_points():
    """Test integration with existing systems"""
    from src.prompt_templates import PromptTemplateManager, PromptType
    
    print("\n🔗 Testing Integration Points")
    print("=" * 35)
    
    # Test prompt manager
    manager = PromptTemplateManager()
    print("1. Testing PromptTemplateManager...")
    
    # Test template generation
    try:
        prompt, context = manager.generate_prompt(
            PromptType.SNAPSHOT,
            ticker="AAPL"
        )
        print(f"   ✓ Generated prompt: {len(prompt)} characters")
        print(f"   ✓ Ticker context: {context.symbol} (confidence: {context.confidence})")
    except Exception as e:
        print(f"   ✗ Prompt generation failed: {e}")
        return False
    
    # Test analysis type detection
    try:
        detected = manager.detect_analysis_type("Show me current market snapshot")
        print(f"   ✓ Analysis type detected: {detected}")
    except Exception as e:
        print(f"   ✗ Analysis type detection failed: {e}")
        return False
    
    print("\n✅ All integration tests passed!")
    return True

if __name__ == "__main__":
    print("🚀 Starting FastAPI Prompt Templates API Tests")
    print("=" * 60)
    
    try:
        # Test API models first
        if not test_api_models():
            print("❌ API models tests failed")
            sys.exit(1)
            
        # Test integration points
        if not test_integration_points():
            print("❌ Integration tests failed")
            sys.exit(1)
            
        # Test API endpoints
        if not test_api_endpoints():
            print("❌ API endpoint tests failed")
            sys.exit(1)
            
        print("\n🎊 ALL TESTS PASSED SUCCESSFULLY!")
        print("✅ FastAPI Prompt Templates API is ready for use")
        
    except Exception as e:
        print(f"\n❌ TEST SUITE FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)