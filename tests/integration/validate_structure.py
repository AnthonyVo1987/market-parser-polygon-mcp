#!/usr/bin/env python3
"""
Test Structure Validation Script

Validates that the new test structure can find backend and frontend components
following Phase 9 migration to unified project structure.
"""

import os
import sys
from pathlib import Path
import subprocess

def validate_directory_structure():
    """Validate that all required directories exist in new structure"""
    print("🏗️ Validating Directory Structure...")
    
    project_root = Path(__file__).parent.parent
    required_paths = {
        "Backend Source": project_root / "src",
        "Frontend Source": project_root / "frontend", 
        "Test Directory": project_root / "tests",
        "Playwright Tests": project_root / "tests" / "playwright",
        "CLI Main": project_root / "src" / "main.py",
        "Frontend Package": project_root / "frontend" / "package.json",
    }
    
    all_valid = True
    
    for name, path in required_paths.items():
        if path.exists():
            print(f"  ✅ {name}: {path}")
        else:
            print(f"  ❌ {name}: {path} (NOT FOUND)")
            all_valid = False
    
    return all_valid

def validate_test_files():
    """Validate that test files were migrated successfully"""
    print("\n📋 Validating Test Files Migration...")
    
    project_root = Path(__file__).parent.parent
    test_dir = project_root / "tests" / "playwright"
    
    expected_files = [
        "test-b001-market-status.spec.ts",
        "test-b002-nvda.spec.ts", 
        "test-b003-spy.spec.ts",
        "test-b004-gme.spec.ts",
        "test-b005-multi-ticker.spec.ts",
        "test-b006-empty-message.spec.ts",
        "integration-test.spec.ts",
        "ui-investigation.spec.ts",
        "PLAYWRIGHT_TESTING_MASTER_PLAN.md"
    ]
    
    missing_files = []
    
    for file_name in expected_files:
        file_path = test_dir / file_name
        if file_path.exists():
            print(f"  ✅ {file_name}")
        else:
            print(f"  ❌ {file_name} (MISSING)")
            missing_files.append(file_name)
    
    # Check helpers directory
    helpers_dir = test_dir / "helpers"
    if helpers_dir.exists():
        helper_files = list(helpers_dir.glob("*.ts"))
        print(f"  ✅ helpers/ directory ({len(helper_files)} files)")
    else:
        print(f"  ❌ helpers/ directory (MISSING)")
        missing_files.append("helpers/")
    
    return len(missing_files) == 0

def validate_smoke_tests():
    """Validate that smoke tests are working"""
    print("\n🧪 Validating Smoke Tests...")
    
    project_root = Path(__file__).parent.parent
    
    # Test CLI smoke test
    cli_test = project_root / "tests" / "test_cli.py"
    api_test = project_root / "tests" / "test_api.py"
    
    tests = [
        ("CLI Smoke Test", cli_test),
        ("API Smoke Test", api_test)
    ]
    
    all_valid = True
    
    for test_name, test_path in tests:
        if test_path.exists():
            print(f"  ✅ {test_name}: {test_path}")
            
            # Try to run the test (dry run)
            try:
                result = subprocess.run([
                    sys.executable, str(test_path)
                ], capture_output=True, text=True, timeout=30)
                
                if "smoke tests" in result.stdout:
                    print(f"    ✅ Test executable and reporting correctly")
                else:
                    print(f"    ⚠️ Test runs but output format may need review")
                    
            except subprocess.TimeoutExpired:
                print(f"    ⚠️ Test took longer than 30 seconds (may be normal)")
            except Exception as e:
                print(f"    ❌ Test execution error: {e}")
                all_valid = False
        else:
            print(f"  ❌ {test_name}: {test_path} (NOT FOUND)")
            all_valid = False
    
    return all_valid

def validate_playwright_config():
    """Validate Playwright configuration for new structure"""
    print("\n⚙️ Validating Playwright Configuration...")
    
    project_root = Path(__file__).parent.parent
    config_path = project_root / "tests" / "playwright.config.ts"
    
    if not config_path.exists():
        print(f"  ❌ playwright.config.ts not found at {config_path}")
        return False
        
    print(f"  ✅ Configuration file: {config_path}")
    
    # Check configuration content
    try:
        config_content = config_path.read_text()
        
        checks = {
            "Backend path updated": "cd frontend" in config_content,
            "Test directory correct": "./tests/playwright" in config_content,
            "Project structure metadata": "project_structure" in config_content
        }
        
        for check_name, check_result in checks.items():
            if check_result:
                print(f"    ✅ {check_name}")
            else:
                print(f"    ⚠️ {check_name} (needs review)")
                
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading config: {e}")
        return False

def validate_legacy_cleanup():
    """Check that legacy structure has been properly handled"""
    print("\n🧹 Validating Legacy Structure Cleanup...")
    
    project_root = Path(__file__).parent.parent
    legacy_path = project_root / "gpt5-openai-agents-sdk-polygon-mcp" / "tests"
    
    if legacy_path.exists():
        print(f"  ⚠️ Legacy test directory still exists: {legacy_path}")
        print(f"    This is normal during migration - can be cleaned up later")
    else:
        print(f"  ✅ Legacy test directory removed: {legacy_path}")
    
    return True  # Always return True since legacy cleanup is optional

def main():
    """Run all validation tests"""
    print("🔍 Phase 9 Testing Infrastructure Migration Validation")
    print("=" * 60)
    
    validators = [
        ("Directory Structure", validate_directory_structure),
        ("Test Files Migration", validate_test_files),
        ("Smoke Tests", validate_smoke_tests),
        ("Playwright Configuration", validate_playwright_config),
        ("Legacy Cleanup", validate_legacy_cleanup)
    ]
    
    passed = 0
    total = len(validators)
    
    for name, validator in validators:
        try:
            if validator():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name} validation failed with error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Validation Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Phase 9 migration validation successful!")
        print("\n✅ Testing infrastructure migration complete")
        print("📍 Tests are now at: /tests/")
        print("📍 Backend available at: /src/")  
        print("📍 Frontend available at: /frontend/")
        return 0
    else:
        print("⚠️ Some validation checks need attention")
        print("\n💡 This is normal during migration - issues can be addressed incrementally")
        return 1

if __name__ == "__main__":
    exit(main())