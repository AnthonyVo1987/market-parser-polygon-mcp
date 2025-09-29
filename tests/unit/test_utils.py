"""Shared utilities for unit tests to eliminate code duplication."""

from typing import Callable, List, Tuple


def run_test_suite(
    suite_name: str,
    tests: List[Tuple[str, Callable[[], bool]]],
    success_message: str = "All tests passed!",
    failure_message: str = "Some tests failed",
) -> int:
    """
    Run a suite of tests and return exit code.

    Args:
        suite_name: Name of the test suite
        tests: List of (test_name, test_function) tuples
        success_message: Message to display on success
        failure_message: Message to display on failure

    Returns:
        0 on success, 1 on failure
    """
    print(f"🔍 Running {suite_name}...")
    print("=" * 50)

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
        print(f"🎉 {success_message}")
        return 0
    print(f"⚠️ {failure_message}")
    return 1
