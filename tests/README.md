# Image Renamer App - Test Suite

This directory contains automated tests for the Image Renamer application.

## Test Structure

- **Unit Tests**: Tests for individual components and functions
- **Integration Tests**: Tests for interactions between components
- **End-to-End Tests**: Tests for complete user workflows
- **Fixtures**: Shared test data and setup

## Running Tests

To run the tests, ensure you have the test dependencies installed:

```bash
pip install -r requirements.txt
```

Then execute the test suite using pytest:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=image_renamer

# Run specific test category
pytest tests/unit/
```

## Test Coverage Goals

- Core functionality: 80%+ coverage
- UI components: 70%+ coverage
- File operations: 90%+ coverage

## Adding New Tests

When adding new tests:

1. Place unit tests in the appropriate category subdirectory
2. Use existing fixtures from conftest.py where possible
3. Mock external dependencies like file system and tkinter
4. Follow the naming convention: `test_*.py` for files, `test_*` for functions

## CI Integration

These tests are automatically run on GitHub Actions for:
- All pushes to main, develop, and feature/* branches
- All pull requests to main and develop branches

See the workflow configuration in `.github/workflows/python-tests.yml`.
