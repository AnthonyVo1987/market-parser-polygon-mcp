"""
Basic API smoke test for Market Parser

Simple functional validation following prototyping principles.
Tests basic API health endpoint without over-engineering.
"""

import requests
import time
import os
from pathlib import Path

def test_api_health():
    """Test that API health endpoint responds correctly"""
    try:
        # Default API URL
        api_url = "http://localhost:8000"
        
        # Check for custom API URL from environment
        env_api_url = os.getenv("VITE_API_URL")
        if env_api_url:
            api_url = env_api_url
            
        health_url = f"{api_url}/health"
        
        print(f"🔗 Testing API at: {health_url}")
        
        # Make request to health endpoint with timeout
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("✅ API health check successful")
                print(f"   Response: {data}")
                return True
            else:
                print(f"❌ API returned unexpected response: {data}")
                return False
        else:
            print(f"❌ API health check failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ API connection failed - server may not be running")
        return False
    except requests.exceptions.Timeout:
        print("❌ API health check timed out")
        return False
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def test_api_reachable():
    """Test that API server is reachable on expected ports"""
    try:
        ports_to_check = [8000, 8001, 3001]  # Common API ports
        
        for port in ports_to_check:
            try:
                api_url = f"http://localhost:{port}"
                response = requests.get(f"{api_url}/health", timeout=3)
                
                if response.status_code == 200:
                    print(f"✅ API found and responding on port {port}")
                    return True
                    
            except requests.exceptions.ConnectionError:
                continue  # Try next port
            except Exception:
                continue  # Try next port
        
        print("❌ API not reachable on any standard ports")
        print("   Make sure FastAPI server is running with: uv run uvicorn src.main:app --host 0.0.0.0 --port 8000")
        return False
        
    except Exception as e:
        print(f"❌ API reachability test error: {e}")
        return False

def test_backend_structure():
    """Test that backend structure exists at expected location"""
    try:
        project_root = Path(__file__).parent.parent
        backend_path = project_root / "src" / "main.py"
        
        if backend_path.exists():
            print(f"✅ Backend found at {backend_path}")
            return True
        else:
            print(f"❌ Backend not found at {backend_path}")
            return False
            
    except Exception as e:
        print(f"❌ Backend structure test error: {e}")
        return False

def main():
    """Run basic API smoke tests"""
    print("🔍 Running API smoke tests...")
    print("=" * 50)
    
    tests = [
        ("Backend Structure", test_backend_structure),
        ("API Reachability", test_api_reachable),
        ("API Health Endpoint", test_api_health)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   Test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API smoke tests passed!")
        return 0
    else:
        print("⚠️ Some API smoke tests failed")
        print("\nℹ️  Note: API tests may fail if backend server is not running")
        print("   Start backend with: cd /path/to/project && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000")
        return 1

if __name__ == "__main__":
    exit(main())