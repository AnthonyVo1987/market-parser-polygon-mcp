"""
Basic API smoke test for Market Parser

Simple functional validation following prototyping principles.
Tests basic API health endpoint without over-engineering.
"""

import sys
from pathlib import Path

import requests

from test_utils import run_test_suite


def test_api_health():
    """Test that API health endpoint responds correctly"""
    try:
        # Default API URL
        api_url = "http://localhost:8000"

        # Note: API URL is now centralized in config/app.config.json
        # Environment variables are only used for API keys

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
            print(f"❌ API returned unexpected response: {data}")
            return False
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
        print(
            "   Make sure FastAPI server is running with: uv run uvicorn src.main:app --host 0.0.0.0 --port 8000"
        )
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
        print(f"❌ Backend not found at {backend_path}")
        return False

    except Exception as e:
        print(f"❌ Backend structure test error: {e}")
        return False


def main():
    """Run basic API smoke tests"""
    tests = [
        ("Backend Structure", test_backend_structure),
        ("API Reachability", test_api_reachable),
        ("API Health Endpoint", test_api_health),
    ]

    result = run_test_suite(
        "API smoke tests", tests, "All API smoke tests passed!", "Some API smoke tests failed"
    )

    if result != 0:
        print("\nℹ️  Note: API tests may fail if backend server is not running")
        print(
            "   Start backend with: cd /path/to/project && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000"
        )

    return result


if __name__ == "__main__":
    sys.exit(main())
