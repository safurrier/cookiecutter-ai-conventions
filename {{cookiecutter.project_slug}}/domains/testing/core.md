# Testing Core

Base testing principles and patterns for all test types.

## Philosophy

- Test behavior, not implementation
- Clear naming: test_behavior_when_condition
- Arrange-Act-Assert pattern
- Fast tests by default

## Best Practices

1. **Test Independence**: Each test should be able to run in isolation
2. **Clear Assertions**: One logical assertion per test
3. **Descriptive Names**: Test names should describe what they test
4. **DRY Setup**: Use fixtures for common setup

## Test Organization

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Component interaction tests
├── e2e/           # End-to-end tests
└── conftest.py    # Shared fixtures
```