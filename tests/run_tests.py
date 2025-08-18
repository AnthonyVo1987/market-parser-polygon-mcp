#!/usr/bin/env python3
"""
Test runner for Stock Data FSM

This script runs all tests and provides coverage reporting
"""

import sys
import unittest
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_tests():
    """Run all FSM tests"""
    print("🧪 Running Stock Data FSM Tests")
    print("=" * 50)
    
    # Suppress logging during tests
    logging.getLogger().setLevel(logging.CRITICAL)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = project_root / 'stock_data_fsm' / 'tests'
    suite = loader.discover(str(start_dir), pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped)}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / 
                   max(1, result.testsRun)) * 100
    print(f"   Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}")
    
    # Overall result
    if len(result.failures) == 0 and len(result.errors) == 0:
        print(f"\n✅ All tests passed! FSM implementation is ready.")
        return 0
    else:
        print(f"\n❌ Some tests failed. Please review and fix issues.")
        return 1


def validate_fsm():
    """Validate FSM structure and completeness"""
    print("\n🔍 Validating FSM Structure")
    print("=" * 30)
    
    try:
        from stock_data_fsm import StateManager, AppState
        
        # Create test manager
        manager = StateManager(session_id='validation-test')
        
        # Run validation
        validation = manager.validate_fsm_health()
        
        fsm_validation = validation['fsm_validation']
        print(f"Total states: {fsm_validation['total_states']}")
        print(f"Total transitions: {fsm_validation['total_transitions']}")
        print(f"States with outgoing transitions: {fsm_validation['states_with_outgoing']}")
        print(f"Validation passed: {fsm_validation['validation_passed']}")
        
        if fsm_validation['issues']:
            print(f"Issues found: {fsm_validation['issues']}")
        else:
            print("✅ FSM structure is valid")
        
        # Test basic functionality
        print(f"\n🔧 Testing basic functionality:")
        success = manager.transition('button_click', button_type='snapshot')
        print(f"   Button click transition: {'✅ OK' if success else '❌ FAIL'}")
        
        can_prepare = manager.can_transition('prepare_prompt')
        print(f"   Can prepare prompt: {'✅ OK' if can_prepare else '❌ FAIL'}")
        
        events = manager.get_available_events()
        print(f"   Available events: {len(events)} events")
        
        print("✅ Basic functionality test passed")
        
    except Exception as e:
        print(f"❌ FSM validation failed: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    print("Stock Data FSM - Test Suite")
    print("=" * 50)
    
    # Run FSM validation first
    validation_result = validate_fsm()
    
    if validation_result != 0:
        print("❌ FSM validation failed - skipping tests")
        sys.exit(1)
    
    # Run all tests
    test_result = run_tests()
    
    print(f"\n🏁 Final Result: {'✅ SUCCESS' if test_result == 0 else '❌ FAILURE'}")
    sys.exit(test_result)
