# 0x03-Unittests_and_integration_tests

This directory contains unit tests and integration tests for the GitHub org client utilities.

## Files

- `utils.py` - Utility functions including `access_nested_map`, `get_json`, and `memoize`
- `client.py` - GitHub organization client implementation
- `test_utils.py` - Parameterized unit tests for the utility functions
- `fixtures.py` - Test fixtures for integration tests

## Running Tests

```bash
python3 -m unittest test_utils.py -v
```

## Test Requirements

The tests verify that:
- `access_nested_map()` returns correct results for valid inputs
- Tests use `@parameterized.expand` decorator
- Each test case is concise (1-2 lines in test body)
- All tests follow proper Python coding standards
