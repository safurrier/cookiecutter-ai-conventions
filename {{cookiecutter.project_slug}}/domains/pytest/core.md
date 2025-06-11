---
extends: testing
---
# Pytest-specific Testing Patterns

This domain extends the base testing domain with pytest-specific conventions.

## Fixtures

- Use `@pytest.fixture` for reusable test setup
- Prefer function-scoped fixtures (default)
- Use `autouse=True` sparingly
- Name fixtures clearly: `mock_database`, `temp_config`

## Markers

```python
@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.parametrize("input,expected", [...])
```

## Assertions

- Use plain `assert` statements
- Leverage pytest's assertion introspection
- Custom assertions via `pytest.raises()` and `pytest.warns()`

## Configuration

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```