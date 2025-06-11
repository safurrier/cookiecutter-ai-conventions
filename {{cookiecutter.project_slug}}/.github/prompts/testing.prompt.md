{%- if "testing" in cookiecutter.default_domains.split(',') -%}
# Testing Conventions Prompt

When writing tests for this project:

## Framework
- Always use pytest, never unittest
- Use fixtures for test data setup
- Prefer parametrize for multiple test cases

## Test Structure
```python
def test_behavior_when_condition():
    """Test that behavior occurs when condition is met."""
    # Arrange - Set up test data
    user = User(name="test")
    
    # Act - Execute the behavior
    result = user.save()
    
    # Assert - Verify the outcome
    assert result.id is not None
    assert result.created_at is not None
```

## Naming Conventions
- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_<behavior>_when_<condition>`
- Test classes: `TestClassName`

## Coverage Requirements
- Each new function needs tests
- Include positive test cases (happy path)
- Include negative test cases (error handling)
- Test edge cases and boundaries

## Best Practices
- One assertion per test when possible
- Use descriptive test names
- Mock external dependencies
- Keep tests independent
- Fast tests are good tests
{%- endif -%}