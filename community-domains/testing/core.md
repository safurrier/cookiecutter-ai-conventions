# Testing Core - Essential Testing Guidance

## Testing Philosophy

### Write Tests That Give Confidence
- Tests should make you confident the code works
- If a test passes but you're still worried, improve the test
- Test behavior, not implementation details

### Test Pyramid
1. **Unit Tests** - Fast, focused, numerous
2. **Integration Tests** - Test component interactions
3. **E2E Tests** - Test complete user workflows

## Test Organization

### Naming Conventions
- Test files: `test_<module>.py` or `<module>_test.py`
- Test functions: `test_<what_it_does>`
- Be descriptive: `test_user_cannot_access_without_auth`

### Test Structure (AAA)
```python
def test_something():
    # Arrange - Set up test data
    user = create_test_user()
    
    # Act - Perform the action
    result = login(user)
    
    # Assert - Check the outcome
    assert result.status == "success"
```

## Best Practices

- **Keep Tests Independent**: Each test should run in isolation
- **Use Fixtures**: Share setup code, not test state
- **Test One Thing**: Each test should verify one behavior
- **Fast Tests**: Slow tests won't get run
- **Clear Failure Messages**: Make debugging easy

## When to Write Tests

- **Before Fixing Bugs**: Write a failing test first
- **When Adding Features**: TDD or test right after
- **During Refactoring**: Ensure behavior doesn't change
- **For Edge Cases**: Document tricky scenarios
