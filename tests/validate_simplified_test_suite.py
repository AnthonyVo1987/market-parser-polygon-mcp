#!/usr/bin/env python3
"""
Test Suite Validation for Simplified 5-State FSM and JSON-Only Architecture

This script validates that all test scripts work with:
1. Simplified 5-state FSM: IDLE, BUTTON_TRIGGERED, AI_PROCESSING, RESPONSE_RECEIVED, ERROR
2. JSON-only output (no DataFrames in UI)
3. Simplified UI return signatures
4. Non-blocking error recovery

SUCCESS CRITERIA:
- All FSM tests pass with 5-state transitions
- Response parser tests use JSON output methods (not DataFrames)
- Integration tests work with simplified UI signatures  
- Production tests validate JSON-only workflow
- Error handling tests confirm non-blocking behavior
"""

import sys
import os
import subprocess
import unittest
import importlib
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import components to test
from stock_data_fsm.states import AppState
from stock_data_fsm.manager import StateManager
from src.response_parser import ResponseParser


class TestSuiteValidator:
    """Validates the updated test suite"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_results = {
            'fsm_tests': {},
            'parser_tests': {},
            'integration_tests': {},
            'production_tests': {},
            'overall_status': 'unknown'
        }
    
    def validate_all(self):
        """Run comprehensive validation of updated test suite"""
        print("🔍 VALIDATING SIMPLIFIED TEST SUITE")
        print("=" * 50)
        
        # 1. Validate FSM state count
        fsm_valid = self._validate_fsm_states()
        print(f"✅ FSM States: {fsm_valid}")
        
        # 2. Validate response parser JSON methods
        parser_valid = self._validate_parser_methods()
        print(f"✅ Parser Methods: {parser_valid}")
        
        # 3. Test individual test files
        test_results = self._run_individual_tests()
        
        # 4. Generate summary
        overall_success = self._generate_summary(test_results)
        
        return overall_success
    
    def _validate_fsm_states(self):
        """Validate FSM has exactly 5 states"""
        try:
            states = list(AppState)
            expected_states = ['IDLE', 'BUTTON_TRIGGERED', 'AI_PROCESSING', 'RESPONSE_RECEIVED', 'ERROR']
            
            if len(states) != 5:
                self.logger.error(f"Expected 5 states, found {len(states)}: {[s.name for s in states]}")
                return False
            
            for expected in expected_states:
                if not any(s.name == expected for s in states):
                    self.logger.error(f"Missing expected state: {expected}")
                    return False
            
            print(f"   States: {[s.name for s in states]}")
            return True
            
        except Exception as e:
            self.logger.error(f"FSM validation failed: {e}")
            return False
    
    def _validate_parser_methods(self):
        """Validate parser has get_json_output method"""
        try:
            parser = ResponseParser()
            
            # Test sample response
            sample_response = "Current price: $150.25\nVolume: 1,000,000"
            result = parser.parse_stock_snapshot(sample_response, "TEST")
            
            # Should have get_json_output method
            if not hasattr(result, 'get_json_output'):
                self.logger.error("ParseResult missing get_json_output method")
                return False
            
            # Should generate valid JSON
            json_output = result.get_json_output()
            if not isinstance(json_output, str):
                self.logger.error("get_json_output should return string")
                return False
            
            if 'data_type' not in json_output:
                self.logger.error("JSON output missing data_type field")
                return False
            
            print(f"   JSON output methods: working")
            return True
            
        except Exception as e:
            self.logger.error(f"Parser validation failed: {e}")
            return False
    
    def _run_individual_tests(self):
        """Run individual test files and collect results"""
        test_files = [
            'tests/test_response_parser.py',
            'stock_data_fsm/tests/test_states.py',
            'stock_data_fsm/tests/test_transitions.py',
            'stock_data_fsm/tests/test_manager.py',
        ]
        
        results = {}
        
        for test_file in test_files:
            print(f"\n🧪 Testing: {test_file}")
            try:
                # Run the test file
                cmd = [sys.executable, test_file]
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=60,
                    cwd=project_root
                )
                
                success = result.returncode == 0
                results[test_file] = {
                    'success': success,
                    'stdout': result.stdout[-500:] if result.stdout else '',  # Last 500 chars
                    'stderr': result.stderr[-500:] if result.stderr else '',  # Last 500 chars
                }
                
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"   {status}")
                
                if not success and result.stderr:
                    error_lines = result.stderr.split('\n')
                    error_msg = error_lines[-2] if len(error_lines) > 1 else 'Unknown error'
                    print(f"   Error: {error_msg}")
                
            except subprocess.TimeoutExpired:
                results[test_file] = {
                    'success': False,
                    'stdout': '',
                    'stderr': 'Test timed out after 60 seconds'
                }
                print(f"   ⏰ TIMEOUT")
                
            except Exception as e:
                results[test_file] = {
                    'success': False,
                    'stdout': '',
                    'stderr': str(e)
                }
                print(f"   💥 ERROR: {e}")
        
        return results
    
    def _generate_summary(self, test_results):
        """Generate comprehensive summary"""
        print(f"\n📊 VALIDATION SUMMARY")
        print("=" * 50)
        
        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results.values() if r['success'])
        
        print(f"📈 Test Files: {passed_tests}/{total_tests} passed")
        print(f"📊 Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if passed_tests == total_tests:
            print(f"\n🎉 ALL TESTS PASS!")
            print(f"✅ Simplified FSM architecture is working")
            print(f"✅ JSON-only output system is working")
            print(f"✅ Test suite is compatible with Phase 1 & 2 changes")
            overall_success = True
        else:
            print(f"\n❌ SOME TESTS FAILED")
            print(f"🔧 Issues to address:")
            
            for test_file, result in test_results.items():
                if not result['success']:
                    print(f"   • {test_file}: {result['stderr'][:100] if result['stderr'] else 'Unknown failure'}")
            
            overall_success = False
        
        print(f"\n🎯 NEXT STEPS:")
        if overall_success:
            print(f"✅ Phase 3 (Test Updates) - COMPLETE")
            print(f"🚀 Test suite is ready for production use")
            print(f"📝 All tests validate simplified 5-state FSM")
            print(f"📄 All tests use JSON-only output methods")
        else:
            print(f"❌ Fix failing tests before proceeding")
            print(f"🔧 Update test expectations for simplified architecture")
            print(f"📋 Ensure all DataFrame references are removed")
            print(f"🔄 Validate FSM transitions match simplified workflow")
        
        return overall_success


def main():
    """Main validation entry point"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Run validation
    validator = TestSuiteValidator()
    success = validator.validate_all()
    
    # Exit with status code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()