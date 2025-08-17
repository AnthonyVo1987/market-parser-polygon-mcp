#!/usr/bin/env python3
"""
Production Bug Test Runner

This script runs the comprehensive production bug test suite and provides
detailed reporting on critical system vulnerabilities.

Usage:
    python run_production_tests.py
    uv run python run_production_tests.py
"""

import sys
import subprocess
import time
import logging
from pathlib import Path

def setup_logging():
    """Configure logging for test execution"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('production_test_run.log')
        ]
    )
    return logging.getLogger(__name__)

def run_production_tests():
    """Run the comprehensive production bug test suite"""
    logger = setup_logging()
    
    logger.info("🔍 Starting Production Bug Test Suite")
    logger.info("=" * 60)
    
    # Ensure we're in the correct directory
    script_dir = Path(__file__).parent
    test_file = script_dir / "test_production_bugs.py"
    
    if not test_file.exists():
        logger.error(f"❌ Test file not found: {test_file}")
        return False
    
    logger.info(f"📋 Test Coverage:")
    logger.info(f"   • Response parsing failures (field extraction monitoring)")
    logger.info(f"   • Message history corruption (None content validation)")
    logger.info(f"   • FSM error recovery (complete state transition testing)")
    logger.info(f"   • Integration scenarios (combined failure modes)")
    logger.info("")
    
    # Run the tests
    start_time = time.time()
    
    try:
        logger.info("⚡ Executing test suite...")
        result = subprocess.run(
            [sys.executable, str(test_file)],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        duration = time.time() - start_time
        
        # Log the output
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    logger.info(f"TEST: {line}")
        
        if result.stderr:
            for line in result.stderr.strip().split('\n'):
                if line.strip() and 'INFO' not in line and 'DEBUG' not in line:
                    logger.warning(f"TEST_WARN: {line}")
        
        logger.info(f"⏱️  Test execution completed in {duration:.2f} seconds")
        
        # Interpret results
        if result.returncode == 0:
            logger.info("✅ ALL PRODUCTION BUG TESTS PASSED!")
            logger.info("🛡️  System is validated for production deployment")
            logger.info("")
            logger.info("📊 Critical Bug Prevention Status:")
            logger.info("   ✅ Response parsing failures - PROTECTED")
            logger.info("   ✅ Message history corruption - PROTECTED") 
            logger.info("   ✅ FSM error recovery - PROTECTED")
            logger.info("   ✅ Integration vulnerabilities - PROTECTED")
            return True
        else:
            logger.error("❌ PRODUCTION BUG TESTS FAILED!")
            logger.error("🚨 Critical vulnerabilities detected - deployment blocked")
            logger.error(f"   Exit code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("⏰ Test execution timed out after 5 minutes")
        return False
    except Exception as e:
        logger.error(f"💥 Test execution failed with error: {e}")
        return False

def main():
    """Main entry point"""
    success = run_production_tests()
    
    if success:
        print("\n🎉 Production bug test validation PASSED")
        print("💚 System is ready for production deployment")
        sys.exit(0)
    else:
        print("\n💥 Production bug test validation FAILED")
        print("🔴 System requires fixes before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()