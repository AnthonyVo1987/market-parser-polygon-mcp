#!/usr/bin/env python3
"""
Comprehensive Bug Fix Test Runner
Executes all bug fix validation tests and provides comprehensive reporting.

This script runs:
1. test_default_ticker_fix.py - Bug #1 validation
2. test_response_parser_fix.py - Bug #2 validation  
3. test_bug_fixes_integration.py - Integration testing
4. Existing pytest suite - Regression validation

Success Criteria:
- All new test scripts pass with 100% success rate
- Existing pytest suite continues to pass (no regressions)
- Integration tests demonstrate 8-9/9 field extraction
- Default ticker functionality works in live application context
"""

import subprocess
import sys
import os
import time
from typing import Dict, List, Tuple, Any


class TestExecutor:
    """Manages test execution and comprehensive reporting"""
    
    def __init__(self):
        self.results = {}
        self.total_start_time = time.time()
        
    def run_test_script(self, script_name: str, description: str) -> Tuple[bool, str, float]:
        """Run a single test script and capture results"""
        print(f"🔄 Running {description}...")
        print(f"   Script: {script_name}")
        
        start_time = time.time()
        
        try:
            # Run the test script
            result = subprocess.run([
                sys.executable, script_name
            ], capture_output=True, text=True, timeout=120)
            
            execution_time = time.time() - start_time
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            if success:
                print(f"   ✅ PASSED ({execution_time:.1f}s)")
            else:
                print(f"   ❌ FAILED ({execution_time:.1f}s)")
                print(f"   Error output: {result.stderr[:200]}...")
            
            return success, output, execution_time
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            print(f"   ⏰ TIMEOUT ({execution_time:.1f}s)")
            return False, "Test timed out after 120 seconds", execution_time
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"   💥 ERROR ({execution_time:.1f}s): {e}")
            return False, f"Execution error: {e}", execution_time
    
    def run_pytest_suite(self) -> Tuple[bool, str, float]:
        """Run existing pytest suite for regression validation"""
        print("🧪 Running existing pytest suite for regression validation...")
        
        start_time = time.time()
        
        try:
            # Run pytest on key test files
            pytest_files = [
                "test_response_parser.py",
                "test_prompt_templates.py", 
                "stock_data_fsm/tests/",
                "test_integration.py"
            ]
            
            # Filter to only existing files
            existing_files = [f for f in pytest_files if os.path.exists(f)]
            
            if not existing_files:
                print("   ⚠️ No pytest files found - skipping regression validation")
                return True, "No pytest files found", 0.0
            
            result = subprocess.run([
                "uv", "run", "pytest", "-v", "--tb=short"
            ] + existing_files, capture_output=True, text=True, timeout=180)
            
            execution_time = time.time() - start_time
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            if success:
                print(f"   ✅ PASSED ({execution_time:.1f}s)")
            else:
                print(f"   ❌ FAILED ({execution_time:.1f}s)")
                print(f"   Some regression tests failed")
            
            return success, output, execution_time
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            print(f"   ⏰ TIMEOUT ({execution_time:.1f}s)")
            return False, "Pytest suite timed out", execution_time
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"   💥 ERROR ({execution_time:.1f}s): {e}")
            return False, f"Pytest execution error: {e}", execution_time
    
    def generate_summary_report(self) -> None:
        """Generate comprehensive summary report"""
        total_time = time.time() - self.total_start_time
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE BUG FIX VALIDATION SUMMARY")
        print("=" * 80)
        
        # Overall statistics
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"🎯 Overall Results:")
        print(f"   Total test suites: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   Total execution time: {total_time:.1f}s")
        print()
        
        # Individual test results
        print("📋 Individual Test Results:")
        for test_name, result in self.results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"   {status} - {test_name} ({result['time']:.1f}s)")
        print()
        
        # Critical bug validation status
        print("🔍 Critical Bug Validation Status:")
        
        bug1_status = self.results.get('Bug #1 - Default Ticker Fix', {}).get('success', False)
        bug2_status = self.results.get('Bug #2 - Response Parser Fix', {}).get('success', False)
        integration_status = self.results.get('Integration Testing', {}).get('success', False)
        regression_status = self.results.get('Regression Validation', {}).get('success', False)
        
        print(f"   Bug #1 (Default Ticker): {'✅ FIXED' if bug1_status else '❌ FAILED'}")
        print(f"   Bug #2 (Response Parser): {'✅ FIXED' if bug2_status else '❌ FAILED'}")
        print(f"   Integration Testing: {'✅ PASS' if integration_status else '❌ FAIL'}")
        print(f"   Regression Validation: {'✅ PASS' if regression_status else '❌ FAIL'}")
        print()
        
        # Deployment readiness assessment
        all_critical_passed = bug1_status and bug2_status and integration_status
        deployment_ready = all_critical_passed and regression_status
        
        print("🚀 Deployment Readiness Assessment:")
        if deployment_ready:
            print("   ✅ READY FOR DEPLOYMENT")
            print("   - All critical bugs are fixed")
            print("   - Integration tests pass")
            print("   - No regressions detected")
            print("   - Application should function correctly in production")
        else:
            print("   ❌ NOT READY FOR DEPLOYMENT")
            print("   Issues that must be resolved:")
            if not bug1_status:
                print("     - Bug #1 (Default Ticker) validation failed")
            if not bug2_status:
                print("     - Bug #2 (Response Parser) validation failed")
            if not integration_status:
                print("     - Integration testing failed")
            if not regression_status:
                print("     - Regression testing failed")
        print()
        
        # Next steps
        print("📋 Next Steps:")
        if deployment_ready:
            print("   1. ✅ All validations passed - ready for production")
            print("   2. 📊 Monitor field extraction rates in production")
            print("   3. 🔍 Validate user experience with default ticker")
            print("   4. 📈 Track performance metrics")
        else:
            print("   1. 🔧 Fix failing test cases")
            print("   2. 🔄 Re-run comprehensive validation")
            print("   3. 📊 Verify all tests pass before deployment")
            print("   4. 🛡️ Address any security or performance concerns")
        
        return deployment_ready


def main():
    """Main test execution coordinator"""
    print("🚀 Starting Comprehensive Bug Fix Validation")
    print("=" * 80)
    print("This test suite validates both critical bug fixes and their integration:")
    print("• Bug #1: Default ticker (NVDA) configuration")
    print("• Bug #2: Enhanced response parser (7-9/9 field extraction)")
    print("• Integration: End-to-end workflow validation")
    print("• Regression: Existing functionality preservation")
    print()
    
    executor = TestExecutor()
    
    # Test suite definitions
    test_suites = [
        {
            'script': 'test_default_ticker_fix.py',
            'name': 'Bug #1 - Default Ticker Fix',
            'description': 'Default Ticker (NVDA) Configuration Validation'
        },
        {
            'script': 'test_response_parser_fix.py', 
            'name': 'Bug #2 - Response Parser Fix',
            'description': 'Enhanced Response Parser (7-9/9 fields) Validation'
        },
        {
            'script': 'test_bug_fixes_integration.py',
            'name': 'Integration Testing',
            'description': 'Bug Fixes Integration & End-to-End Workflow'
        }
    ]
    
    # Execute individual test scripts
    for test_suite in test_suites:
        if not os.path.exists(test_suite['script']):
            print(f"⚠️ Warning: {test_suite['script']} not found - skipping")
            executor.results[test_suite['name']] = {
                'success': False,
                'output': 'Test script not found',
                'time': 0.0
            }
            continue
        
        success, output, exec_time = executor.run_test_script(
            test_suite['script'],
            test_suite['description']
        )
        
        executor.results[test_suite['name']] = {
            'success': success,
            'output': output,
            'time': exec_time
        }
    
    print()
    
    # Execute pytest suite for regression validation
    success, output, exec_time = executor.run_pytest_suite()
    executor.results['Regression Validation'] = {
        'success': success,
        'output': output,
        'time': exec_time
    }
    
    print()
    
    # Generate comprehensive report
    deployment_ready = executor.generate_summary_report()
    
    # Save detailed results to log file
    log_filename = f"comprehensive_bug_test_results_{int(time.time())}.log"
    with open(log_filename, 'w') as f:
        f.write("COMPREHENSIVE BUG FIX VALIDATION RESULTS\n")
        f.write("=" * 50 + "\n\n")
        
        for test_name, result in executor.results.items():
            f.write(f"TEST: {test_name}\n")
            f.write(f"SUCCESS: {result['success']}\n")
            f.write(f"TIME: {result['time']:.1f}s\n")
            f.write(f"OUTPUT:\n{result['output']}\n")
            f.write("-" * 40 + "\n\n")
    
    print(f"📝 Detailed results saved to: {log_filename}")
    
    # Exit with appropriate code
    sys.exit(0 if deployment_ready else 1)


if __name__ == '__main__':
    main()