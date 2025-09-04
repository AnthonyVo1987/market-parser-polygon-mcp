"""
Pytest-compatible test suite for the FastAPI Prompt Templates API.

This file uses pytest conventions to make tests more discoverable
and integrate better with testing frameworks.
"""

import sys
from pathlib import Path
import pytest

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from fastapi.testclient import TestClient
from src.main import app
from src.api_models import (
    AnalysisType, PromptMode, GeneratePromptRequest, 
    ButtonAnalysisRequest, ChatAnalysisRequest
)
from src.prompt_templates import PromptTemplateManager, PromptType

@pytest.fixture
def client():
    """FastAPI test client fixture"""
    return TestClient(app)

def test_health_endpoint(client):
    """Test basic health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "message" in data

def test_api_health_endpoint(client):
    """Test API health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"

def test_template_list_endpoint(client):
    """Test template list endpoint"""
    response = client.get("/api/v1/prompts/templates")
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "conversational_only"
    assert data["total_count"] >= 3
    assert "templates" in data
    
    # Verify all templates are available
    for template_name, template_info in data["templates"].items():
        assert template_info["available"] is True

def test_system_status_endpoint(client):
    """Test system status endpoint"""
    response = client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "metrics" in data
    assert data["metrics"]["prompt_templates_loaded"] >= 3

def test_generate_prompt_valid(client):
    """Test prompt generation with valid input"""
    payload = {
        "template_type": "snapshot",
        "ticker": "AAPL",
        "custom_instructions": "Focus on recent performance",
        "mode": "conversational"
    }
    response = client.post("/api/v1/prompts/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["prompt"]) > 0
    assert data["ticker_context"]["symbol"] == "AAPL"
    assert data["ticker_context"]["confidence"] == 1.0
    assert data["template_type"] == "snapshot"

def test_generate_prompt_validation_error(client):
    """Test prompt generation with invalid input"""
    invalid_payload = {
        "template_type": "invalid_type",  # Invalid enum value
        "ticker": "TOOLONGTICKER"  # Invalid ticker
    }
    response = client.post("/api/v1/prompts/generate", json=invalid_payload)
    assert response.status_code == 422  # Validation error

def test_api_models():
    """Test API models functionality"""
    # Test enum values
    analysis_types = [t.value for t in AnalysisType]
    assert "snapshot" in analysis_types
    assert "technical" in analysis_types
    assert "support_resistance" in analysis_types
    
    # Test request validation
    request = GeneratePromptRequest(
        template_type=AnalysisType.SNAPSHOT,
        ticker="AAPL"
    )
    assert request.template_type == AnalysisType.SNAPSHOT
    assert request.ticker == "AAPL"
    
    # Test button analysis request
    button_request = ButtonAnalysisRequest(
        ticker="TSLA",
        analysis_type=AnalysisType.TECHNICAL
    )
    assert button_request.ticker == "TSLA"
    assert button_request.analysis_type == AnalysisType.TECHNICAL
    
    # Test chat analysis request
    chat_request = ChatAnalysisRequest(
        message="What's the current price of Apple stock?"
    )
    assert len(chat_request.message) > 0

def test_prompt_template_manager():
    """Test prompt template manager functionality"""
    manager = PromptTemplateManager()
    
    # Test template generation
    prompt, context = manager.generate_prompt(
        PromptType.SNAPSHOT,
        ticker="AAPL"
    )
    assert len(prompt) > 0
    assert context.symbol == "AAPL"
    assert context.confidence == 1.0
    
    # Test analysis type detection
    detected = manager.detect_analysis_type("Show me current market snapshot")
    assert detected == PromptType.SNAPSHOT

def test_integration_endpoints_sequence(client):
    """Test a sequence of API calls to ensure they work together"""
    # 1. Check system health
    health_response = client.get("/api/v1/health")
    assert health_response.status_code == 200
    
    # 2. Get available templates
    templates_response = client.get("/api/v1/prompts/templates")
    assert templates_response.status_code == 200
    templates_data = templates_response.json()
    
    # 3. Generate a prompt using an available template
    template_type = list(templates_data["templates"].keys())[0]
    prompt_payload = {
        "template_type": template_type,
        "ticker": "MSFT",
        "mode": "conversational"
    }
    prompt_response = client.post("/api/v1/prompts/generate", json=prompt_payload)
    assert prompt_response.status_code == 200
    
    # 4. Check system status after operations
    status_response = client.get("/api/v1/system/status")
    assert status_response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])