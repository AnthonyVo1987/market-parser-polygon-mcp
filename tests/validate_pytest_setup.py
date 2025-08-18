#!/usr/bin/env python3
"""
PyTest Installation and Setup Validation Script
Purpose: Verify pytest infrastructure is working correctly
"""

import pytest
import sys
import os

def test_pytest_installation():
    """Verify pytest is properly installed"""
    assert pytest.__version__ is not None
    print(f"✅ PyTest version: {pytest.__version__}")

def test_module_imports():
    """Test that all project modules can be imported"""
    try:
        import src.json_parser
        import stock_data_fsm.states
        import market_parser_demo
        print("✅ All project modules import successfully")
    except ImportError as e:
        pytest.fail(f"❌ Module import failed: {e}")

def test_test_discovery():
    """Verify pytest can discover tests"""
    assert True

def test_project_structure():
    """Verify project structure is accessible"""
    assert os.path.exists("src"), "src directory should exist"
    assert os.path.exists("stock_data_fsm"), "stock_data_fsm directory should exist"
    assert os.path.exists("tests"), "tests directory should exist"
    print("✅ Project structure verified")

def test_python_path_configuration():
    """Verify Python path includes project directories"""
    import sys
    paths = [path for path in sys.path]
    # Check that current directory and project modules are in path
    assert any("market-parser-polygon-mcp" in path for path in paths), "Project root should be in Python path"
    print("✅ Python path configuration verified")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])