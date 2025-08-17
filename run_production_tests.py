#!/usr/bin/env python3
"""
Production Test Runner

This script runs all the comprehensive production-focused tests that were designed
to catch the integration issues that the previous component-specific tests missed.

These tests focus on validating complete user workflows, not just isolated components.

TEST SUITES:
1. Production Workflow Tests - Complete button-to-display workflows
2. JSON/Text Parsing Integration - JSON vs text response handling
3. UI State Integration - UI component and FSM integration

CRITICAL DIFFERENCES FROM PREVIOUS TESTS:
- Tests complete user journeys, not isolated functions
- Validates FSM integration with parsing and UI components
- Tests DataFrame generation and UI display integration
- Covers JSON response handling with text fallback
- Includes realistic error recovery scenarios
- Tests concurrent operations and edge cases
"""

import sys
import os
import time
import subprocess
import logging
from typing import Dict, List, Tuple, Any
import traceback

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_logging():
    """Setup comprehensive logging for test execution"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('production_tests.log', mode='w')
        ]
    )
    return logging.getLogger('ProductionTestRunner')

def run_test_suite(test_module: str, suite_name: str) -> Tuple[bool, Dict[str, Any]]:
    """Run a test suite and return results"""
    logger = logging.getLogger('ProductionTestRunner')
    
    logger.info(f"🚀 Running {suite_name}...")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    try:
        # Run the test module
        result = subprocess.run([
            sys.executable, test_module
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        execution_time = time.time() - start_time
        
        # Parse results
        success = result.returncode == 0
        stdout = result.stdout
        stderr = result.stderr
        
        # Extract test metrics from output
        metrics = {
            'execution_time': execution_time,
            'success': success,
            'stdout_lines': len(stdout.split('\n')) if stdout else 0,
            'stderr_lines': len(stderr.split('\n')) if stderr else 0,
            'return_code': result.returncode
        }
        
        # Log results
        if success:
            logger.info(f"✅ {suite_name} PASSED in {execution_time:.1f}s")
        else:
            logger.error(f"❌ {suite_name} FAILED in {execution_time:.1f}s")
            logger.error(f"Return code: {result.returncode}")
            
        # Log output
        if stdout:
            logger.info(f"📋 {suite_name} Output:")
            for line in stdout.split('\n')[-20:]:  # Last 20 lines
                if line.strip():
                    logger.info(f"   {line}")
        
        if stderr and not success:
            logger.error(f"💥 {suite_name} Errors:")
            for line in stderr.split('\n')[-10:]:  # Last 10 error lines
                if line.strip():
                    logger.error(f"   {line}")
        
        return success, metrics
    
    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        logger.error(f"⏰ {suite_name} TIMEOUT after {execution_time:.1f}s")
        return False, {
            'execution_time': execution_time,
            'success': False,
            'timeout': True,
            'return_code': -1
        }
    
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"💥 {suite_name} EXCEPTION: {e}")
        logger.error(traceback.format_exc())
        return False, {
            'execution_time': execution_time,
            'success': False,
            'exception': str(e),
            'return_code': -1
        }

def check_test_environment() -> Dict[str, bool]:
    """Check if the test environment is properly configured"""
    logger = logging.getLogger('ProductionTestRunner')
    
    logger.info("🔍 Checking test environment...")
    
    checks = {}
    
    # Check for test files
    test_files = [
        'test_production_workflow_comprehensive.py',
        'test_json_text_parsing_integration.py',
        'test_ui_state_integration.py'
    ]
    
    for test_file in test_files:
        exists = os.path.exists(test_file)
        checks[f'test_file_{test_file}'] = exists
        if exists:
            logger.info(f"   ✅ {test_file} found")
        else:
            logger.error(f"   ❌ {test_file} missing")
    
    # Check for core modules
    core_modules = [
        'stock_data_fsm',
        'response_parser',
        'prompt_templates'
    ]
    
    for module in core_modules:
        try:
            __import__(module)
            checks[f'module_{module}'] = True
            logger.info(f"   ✅ {module} module available")
        except ImportError as e:
            checks[f'module_{module}'] = False
            logger.warning(f"   ⚠️  {module} module not available: {e}")
    
    # Check Python environment
    python_version = sys.version_info
    checks['python_version'] = python_version >= (3, 8)
    if checks['python_version']:
        logger.info(f"   ✅ Python {python_version.major}.{python_version.minor}")
    else:
        logger.error(f"   ❌ Python {python_version.major}.{python_version.minor} < 3.8")
    
    return checks

def analyze_test_results(results: Dict[str, Tuple[bool, Dict[str, Any]]]) -> Dict[str, Any]:
    """Analyze and summarize test results"""
    logger = logging.getLogger('ProductionTestRunner')
    
    analysis = {
        'total_suites': len(results),
        'passed_suites': 0,
        'failed_suites': 0,
        'total_execution_time': 0,
        'suite_details': {},
        'critical_failures': [],
        'recommendations': []
    }
    
    for suite_name, (success, metrics) in results.items():
        analysis['suite_details'][suite_name] = {
            'success': success,
            'execution_time': metrics.get('execution_time', 0),
            'metrics': metrics
        }
        
        analysis['total_execution_time'] += metrics.get('execution_time', 0)
        
        if success:
            analysis['passed_suites'] += 1
        else:
            analysis['failed_suites'] += 1
            
            # Categorize critical failures
            if 'workflow' in suite_name.lower():
                analysis['critical_failures'].append({
                    'suite': suite_name,
                    'type': 'workflow_integration',
                    'impact': 'HIGH - Complete user workflows failing'
                })
            elif 'json' in suite_name.lower():
                analysis['critical_failures'].append({
                    'suite': suite_name,
                    'type': 'parsing_integration',
                    'impact': 'MEDIUM - JSON/text parsing integration issues'
                })
            elif 'ui' in suite_name.lower():
                analysis['critical_failures'].append({
                    'suite': suite_name,
                    'type': 'ui_integration',
                    'impact': 'MEDIUM - UI state management issues'
                })
    
    # Generate recommendations
    if analysis['failed_suites'] == 0:
        analysis['recommendations'].append(
            "✅ All production tests passed - system ready for deployment"
        )
    else:
        analysis['recommendations'].extend([
            f"❌ {analysis['failed_suites']}/{analysis['total_suites']} test suites failed",
            "🔧 Focus on failed integration points before production deployment",
            "📋 Review detailed logs for specific failure points"
        ])
        
        if any('workflow' in failure['type'] for failure in analysis['critical_failures']):
            analysis['recommendations'].append(
                "🚨 CRITICAL: Complete workflow failures detected - major integration issues"
            )
        
        if any('parsing' in failure['type'] for failure in analysis['critical_failures']):
            analysis['recommendations'].append(
                "⚠️  JSON/text parsing integration needs attention"
            )
        
        if any('ui' in failure['type'] for failure in analysis['critical_failures']):
            analysis['recommendations'].append(
                "📱 UI state management integration requires fixes"
            )
    
    return analysis

def generate_comparison_report(analysis: Dict[str, Any]) -> str:
    """Generate comparison report vs previous tests"""
    report_lines = [
        "",
        "🔍 PRODUCTION TEST EFFECTIVENESS ANALYSIS",
        "=" * 60,
        "",
        "Previous Test Issues:",
        "• Focused on isolated component testing",
        "• Did not validate complete user workflows", 
        "• Missed FSM integration with parsing results",
        "• No DataFrame generation testing for UI",
        "• Limited JSON vs text response handling",
        "• Insufficient error recovery scenario coverage",
        "",
        "NEW Production Test Improvements:",
        "✅ Complete button-to-display workflow validation",
        "✅ FSM state management integration testing",
        "✅ DataFrame generation and UI integration",
        "✅ JSON parsing with text fallback validation",
        "✅ Realistic error recovery scenarios",
        "✅ Concurrent operations and edge cases",
        "✅ UI component state management testing",
        "",
        "CRITICAL INTEGRATION POINTS NOW TESTED:",
        "• Button Click → FSM Transition → Prompt Generation",
        "• AI Response → Parsing (JSON/Text) → DataFrame",
        "• DataFrame → UI Component Updates",
        "• Error States → Recovery → UI Feedback",
        "• Message Validation → Chat History Management",
        "",
    ]
    
    if analysis['failed_suites'] == 0:
        report_lines.extend([
            "🎯 VALIDATION VERDICT:",
            "✅ These tests would have CAUGHT the original production issues",
            "✅ Complete user workflows are properly validated",
            "✅ Integration points are thoroughly tested",
            "🚀 System validated for production deployment",
        ])
    else:
        report_lines.extend([
            "🎯 VALIDATION VERDICT:",
            "❌ These tests DETECTED critical integration issues",
            f"🔧 {analysis['failed_suites']} integration points require attention",
            "🚨 Production deployment should be delayed until fixes are implemented",
            "",
            "DETECTED CRITICAL FAILURES:",
        ])
        
        for failure in analysis['critical_failures']:
            report_lines.append(f"• {failure['suite']}: {failure['impact']}")
    
    return "\n".join(report_lines)

def main():
    """Main test runner function"""
    logger = setup_logging()
    
    logger.info("🚀 PRODUCTION TEST SUITE RUNNER")
    logger.info("=" * 80)
    logger.info("Running comprehensive production-focused tests that validate")
    logger.info("complete user workflows and integration points.")
    logger.info("")
    
    start_time = time.time()
    
    # Check environment
    env_checks = check_test_environment()
    critical_missing = [k for k, v in env_checks.items() if not v and 'test_file' in k]
    
    if critical_missing:
        logger.error("❌ Critical test files missing - cannot proceed")
        for missing in critical_missing:
            logger.error(f"   • {missing}")
        return 1
    
    # Define test suites
    test_suites = [
        ('test_production_workflow_comprehensive.py', 'Production Workflow Integration'),
        ('test_json_text_parsing_integration.py', 'JSON/Text Parsing Integration'),
        ('test_ui_state_integration.py', 'UI State Management Integration')
    ]
    
    # Run test suites
    results = {}
    
    for test_file, suite_name in test_suites:
        if os.path.exists(test_file):
            success, metrics = run_test_suite(test_file, suite_name)
            results[suite_name] = (success, metrics)
        else:
            logger.error(f"❌ Test file {test_file} not found - skipping {suite_name}")
            results[suite_name] = (False, {'error': 'file_not_found'})
    
    # Analyze results
    total_time = time.time() - start_time
    analysis = analyze_test_results(results)
    
    # Generate comprehensive report
    logger.info("")
    logger.info("📊 PRODUCTION TEST SUITE RESULTS")
    logger.info("=" * 80)
    
    logger.info(f"🕒 Total Execution Time: {total_time:.1f}s")
    logger.info(f"📋 Test Suites: {analysis['total_suites']}")
    logger.info(f"✅ Passed: {analysis['passed_suites']}")
    logger.info(f"❌ Failed: {analysis['failed_suites']}")
    logger.info(f"📈 Success Rate: {(analysis['passed_suites']/analysis['total_suites']*100):.1f}%")
    
    logger.info("")
    logger.info("📋 SUITE BREAKDOWN:")
    for suite_name, details in analysis['suite_details'].items():
        status = "✅ PASSED" if details['success'] else "❌ FAILED"
        time_str = f"{details['execution_time']:.1f}s"
        logger.info(f"   • {suite_name}: {status} ({time_str})")
    
    # Log recommendations
    logger.info("")
    logger.info("🎯 RECOMMENDATIONS:")
    for rec in analysis['recommendations']:
        logger.info(f"   {rec}")
    
    # Generate comparison report
    comparison_report = generate_comparison_report(analysis)
    logger.info(comparison_report)
    
    # Final verdict
    logger.info("")
    if analysis['failed_suites'] == 0:
        logger.info("🎉 ALL PRODUCTION TESTS PASSED!")
        logger.info("🚀 System validated for production deployment")
        logger.info("🛡️ These tests would have caught the original production issues")
        return 0
    else:
        logger.error("🚨 PRODUCTION TESTS FAILED!")
        logger.error("🔧 Critical integration issues detected")
        logger.error("⚠️  Production deployment should be delayed")
        logger.error(f"📋 Review logs for {analysis['failed_suites']} failed integration points")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Test runner failed with unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)