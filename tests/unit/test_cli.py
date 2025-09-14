"""
Basic CLI smoke test for Market Parser

Simple functional validation following prototyping principles.
Tests basic CLI functionality without over-engineering.
"""

import subprocess
import sys
import os
from pathlib import Path

def test_cli_help():
    """Test that CLI shows help information"""
    try:
        # Get the project root directory
        project_root = Path(__file__).parent.parent
        cli_path = project_root / "src" / "main.py"
        
        if not cli_path.exists():
            print(f"❌ CLI not found at {cli_path}")
            return False
            
        # Run CLI with --help flag
        result = subprocess.run([
            sys.executable, str(cli_path), "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ CLI help command successful")
            return True
        else:
            print(f"❌ CLI help failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ CLI help command timed out")
        return False
    except Exception as e:
        print(f"❌ CLI test error: {e}")
        return False

def test_cli_exists():
    """Test that CLI file exists and is executable"""
    try:
        project_root = Path(__file__).parent.parent
        cli_path = project_root / "src" / "main.py"
        
        if cli_path.exists():
            print(f"✅ CLI found at {cli_path}")
            return True
        else:
            print(f"❌ CLI not found at {cli_path}")
            return False
            
    except Exception as e:
        print(f"❌ CLI existence check error: {e}")
        return False

def main():
    """Run basic CLI smoke tests"""
    print("🔍 Running CLI smoke tests...")
    print("=" * 50)
    
    tests = [
        ("CLI Existence", test_cli_exists),
        ("CLI Help Command", test_cli_help)
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
        print("🎉 All CLI smoke tests passed!")
        return 0
    else:
        print("⚠️ Some CLI smoke tests failed")
        return 1

if __name__ == "__main__":
    exit(main())