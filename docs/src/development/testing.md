# Testing Guide

The SGLang RAG Demo includes comprehensive testing to ensure code quality and reliability.

## Test Structure

The test suite is organized into multiple categories:

```
tests/
├── test_rag_system.py      # Unit tests for core components
├── test_smoke.py           # Smoke tests for basic functionality
├── test_e2e.py            # End-to-end integration tests
└── test_smoke_pytest.py   # Additional smoke tests
```

## Running Tests

### Full Test Suite

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run tests with coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Specific Test Categories

```bash
# Unit tests - Core component functionality
python -m pytest tests/test_rag_system.py -v

# Smoke tests - Basic functionality verification
python -m pytest tests/test_smoke.py -v

# End-to-end tests - Complete workflow testing
python -m pytest tests/test_e2e.py -v
```

## Test Categories

### Unit Tests (`test_rag_system.py`)

Tests individual components in isolation:

- **VectorStore**: Initialization, document chunk operations, embedding functionality
- **DocumentProcessor**: File loading, text processing, chunking strategies
- **LLMProvider**: Client initialization, response generation
- **RAGPipeline**: Query processing, response generation

### Smoke Tests (`test_smoke.py`)

Quick verification of basic functionality:

- System initialization
- Document loading without errors
- Vector index operations
- Query processing pipeline
- Error handling verification

### End-to-End Tests (`test_e2e.py`)

Complete workflow testing:

- Document loading → Index building → Query processing
- Multi-perspective analysis workflows
- Performance benchmarking
- Full pipeline integration

## Running Tests Without API Keys

Most tests can run without API configuration. The test suite is designed to:

- Mock external API calls where possible
- Skip tests that require real API keys
- Test error handling for invalid/missing credentials

```bash
# Run tests that don't require API keys
python -m pytest tests/test_rag_system.py tests/test_smoke.py -k "not llm_generation"
```

## Test Configuration

Tests use the same configuration system as the main application:

```python
# Tests automatically use test-specific settings
# No need to configure API keys for most tests
```

## Expected Test Results

When running the full test suite:

- **Unit tests**: Should all pass regardless of API key configuration
- **Smoke tests**: Should all pass, may show warnings for missing API keys
- **E2E tests**: May fail LLM generation without valid API keys (expected behavior)

Example output:
```
======================================= test session starts =======================================
collected 15 items

tests/test_e2e.py .F                                                          [ 13%]
tests/test_rag_system.py ........                                             [ 66%]
tests/test_smoke.py ...                                                        [ 86%]
tests/test_smoke_pytest.py ..                                                  [100%]

========================== 1 failed, 14 passed in 29.52s ==========================
```

The failed test is expected when API keys are not configured.

## Writing New Tests

### Test Structure

```python
import sys
from pathlib import Path
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem

class TestNewFeature:
    def test_feature_functionality(self):
        """Test description"""
        # Test implementation
        assert True
```

### Best Practices

1. **Isolation**: Each test should be independent
2. **Mocking**: Mock external dependencies (API calls, file I/O)
3. **Error Testing**: Test both success and failure scenarios
4. **Documentation**: Clear test descriptions and comments
5. **Performance**: Keep tests fast and efficient

## Continuous Integration

The test suite is designed to work in CI environments:

- No external dependencies required for core tests
- Configurable API key requirements
- Clear pass/fail criteria
- Detailed error reporting

## Debugging Tests

```bash
# Run with detailed output
python -m pytest tests/ -v -s

# Run specific test with debugging
python -m pytest tests/test_rag_system.py::TestVectorStore::test_initialization -v -s

# Drop into debugger on failure
python -m pytest tests/ --pdb
```

## Performance Testing

The test suite includes performance benchmarks:

```bash
# Run performance tests
python -m pytest tests/test_e2e.py -k performance -v

# Generate benchmark reports
python scripts/benchmark_retrieval.py
```
