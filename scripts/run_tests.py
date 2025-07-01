#!/usr/bin/env python3
"""
Test runner script for SGLang RAG Demo

This script provides convenient ways to run different test suites
and generate reports for the project.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🧪 {description}")
    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def run_unit_tests():
    """Run unit tests only"""
    return run_command(
        ["python", "-m", "pytest", "tests/test_rag_system.py", "-v"],
        "Unit Tests (Core Components)"
    )


def run_smoke_tests():
    """Run smoke tests only"""
    return run_command(
        ["python", "-m", "pytest", "tests/test_smoke.py", "-v"],
        "Smoke Tests (Basic Functionality)"
    )


def run_integration_tests():
    """Run end-to-end integration tests"""
    return run_command(
        ["python", "-m", "pytest", "tests/test_e2e.py", "-v"],
        "Integration Tests (End-to-End)"
    )


def run_all_tests():
    """Run the complete test suite"""
    return run_command(
        ["python", "-m", "pytest", "tests/", "-v"],
        "Complete Test Suite"
    )


def run_tests_with_coverage():
    """Run tests with coverage report"""
    success = run_command(
        ["python", "-m", "pytest", "tests/", "--cov=src", "--cov-report=term-missing", "--cov-report=html"],
        "Tests with Coverage Report"
    )
    
    if success:
        print("\n📊 Coverage report generated in htmlcov/index.html")
    
    return success


def run_quick_tests():
    """Run tests that don't require API keys"""
    return run_command(
        ["python", "-m", "pytest", "tests/test_rag_system.py", "tests/test_smoke.py", "-v", "-k", "not llm_generation"],
        "Quick Tests (No API Keys Required)"
    )


def main():
    parser = argparse.ArgumentParser(description="SGLang RAG Demo Test Runner")
    parser.add_argument(
        "test_type",
        choices=["unit", "smoke", "integration", "all", "coverage", "quick"],
        help="Type of tests to run"
    )
    
    args = parser.parse_args()
    
    print("🚀 SGLang RAG Demo Test Runner")
    print("=" * 50)
    
    # Map test types to functions
    test_functions = {
        "unit": run_unit_tests,
        "smoke": run_smoke_tests,
        "integration": run_integration_tests,
        "all": run_all_tests,
        "coverage": run_tests_with_coverage,
        "quick": run_quick_tests,
    }
    
    # Run the selected test type
    success = test_functions[args.test_type]()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
