"""
Basic CLI smoke test for Market Parser

Simple functional validation following prototyping principles.
Tests basic CLI functionality without over-engineering.
"""

import subprocess
import sys
from pathlib import Path

from test_utils import run_test_suite


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
        result = subprocess.run(
            [sys.executable, str(cli_path), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode == 0:
            print("✅ CLI help command successful")
            return True
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
        print(f"❌ CLI not found at {cli_path}")
        return False

    except Exception as e:
        print(f"❌ CLI existence check error: {e}")
        return False


def main():
    """Run basic CLI smoke tests"""
    tests = [("CLI Existence", test_cli_exists), ("CLI Help Command", test_cli_help)]

    return run_test_suite(
        "CLI smoke tests", tests, "All CLI smoke tests passed!", "Some CLI smoke tests failed"
    )


if __name__ == "__main__":
    sys.exit(main())
