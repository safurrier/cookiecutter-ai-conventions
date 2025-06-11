# Testing Conventions

[glob: "**/test_*.py", "**/*_test.py", "**/tests/**", "**/conftest.py"]
// Apply these rules to test files

## Testing Framework

Use pytest exclusively:
- No unittest.TestCase
- Use fixtures for setup
- Parametrize for multiple cases

## Test Structure

```python
def test_behavior_when_condition():
    """Test that behavior occurs when condition is met."""
    # Arrange - Set up test data
    
    # Act - Execute the behavior
    
    # Assert - Verify the outcome
```

## Progressive Testing Approach

1. **E2E Tests** - Complete user journeys
2. **Integration Tests** - Component interactions
3. **Unit Tests** - Individual functions

## Naming Conventions

- Files: `test_<module>.py` or `<module>_test.py`
- Functions: `test_<behavior>_when_<condition>`
- Classes: `Test<Component>` (when grouping tests)

## Fixtures

```python
@pytest.fixture
def user():
    """Create a test user."""
    return User(email="test@example.com")
```

- Scope appropriately (function, class, module, session)
- Name descriptively
- Document purpose

## Assertions

- Use specific assertions
- Include helpful messages
- One logical assertion per test

## File References

For complete testing conventions:
- @domains/testing/core.md

## Activation

- **Mode**: Glob-based
- **Files**: All test files
- **Priority**: High when writing or modifying tests