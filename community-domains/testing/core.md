# Testing Core - Essential Testing Guidance

This file contains the fundamental testing principles and approaches that apply to most testing scenarios.

## Testing Philosophy

### Progressive Testing Approach
Follow this evolution timeline for sustainable testing:

```
End-to-End Tests (Start here)
    ↓
Smoke Tests (Add next)
    ↓
Integration Tests (Then add these)
    ↓
Unit Tests & Property-Based Tests (Refine with these)
```

### When to Write Tests Decision Tree

```
Is this a critical user path?
├── Yes → Write end-to-end/smoke test first
└── No → Does it contain complex business logic?
    ├── Yes → Is it well understood and stable?
    │   ├── Yes → Write unit tests
    │   └── No → Write integration tests, refine with unit tests later
    └── No → Is it an integration point?
        ├── Yes → Write integration tests
        └── No → Minimal testing
```

## Universal Testing Principles

1. **Test Behavior, Not Implementation** ⭐
   - Focus on *what* the code does, not *how* it does it
   - Tests should remain valid even if implementation changes
   - Validate observable outcomes rather than internal state
   - **Avoid checking for specific strings in outputs** - this is often a code smell that couples tests to implementation details

2. **Arrange-Act-Assert Pattern**
   - **Arrange**: Set up test data and conditions
   - **Act**: Execute the behavior being tested
   - **Assert**: Verify the expected outcome

3. **Strategic Use of Test Doubles** 🚨
   - **AVOID mocks and patching** - they're a huge code smell and couple tests to implementation
   - **Prefer test doubles, fakes, and stubs** - they test behavior without implementation coupling
   - Use real objects when possible to catch integration issues early
   - Only replace external dependencies and side effects
   - Create test doubles at architectural boundaries, not for every dependency

4. **Test Organization and Documentation**
   - **Good tests double as documentation** - they should clearly show how code is intended to be used
   - Group related tests logically in classes or modules
   - **Consolidate and categorize tests properly**: Avoid scattered test files across the project. Consolidate similar tests (e.g., multiple browser test files) into proper categories and remove duplicates
   - Use descriptive test names: `test_[unit_of_work]_[scenario]_[expected_outcome]`
   - One logical assertion per test (multiple related assertions okay)

5. **Table-Driven Testing**
   - Use parametrized tests or data structures to test multiple scenarios efficiently
   - Reduces duplication while maintaining clarity
   - Makes it easy to add new test cases

## Test Cost Awareness

Not all code deserves the same testing investment:

| Code Type | Recommended Testing |
|-----------|---------------------|
| Critical business logic | High unit test coverage |
| Integration points | Thorough integration tests |
| Simple additive features (logging, formatting) | Minimal or no testing - focus on straightforward implementation |
| Simple operations | Minimal testing |
| Volatile exploratory code | Smoke tests only until stable |
| Third-party code | Test your usage, not their implementation |

**Match testing rigor to feature complexity**: Complex features (UI interactions, data models, external integrations) benefit from comprehensive TDD. Simple additive features just need straightforward implementation.

## Project Testing Integration

### Check Project Documentation First
- **Look for project-specific test commands** like `make test-smoke` with optimizations (`-n auto`, timeouts)
- Use project conventions rather than generic pytest commands

### CI Integration
- **Exclude API-using tests from CI**: Any test category that makes real API calls must be excluded from CI pytest markers
- Use skipif guards for tests that require external services
- Design test suites to run reliably in CI environments without external dependencies

### Read Existing Tests for Patterns
- **Study existing test files before writing new tests** to understand project conventions
- Look for preferred mocking approach, fixture usage, and external service handling patterns

## Common Commands (pytest)

- **Run tests**: `python -m pytest` or `pytest`
- **Run single test**: `pytest -k "<test_name>"` or `pytest <file_path>::<test_name>`
- **Fast feedback**: Always examine existing test patterns before writing new tests

## Key Anti-Patterns to Avoid

- Testing implementation details instead of behavior
- **Checking for specific strings in outputs** (brittle and couples to implementation)
- **Overuse of mocks and patching** (major code smell - prefer fakes/stubs)
- Complex test setup (use builders and factories)
- Test interdependence (each test should be independent)
- Too many assertions in a single test
- Poor test names that don't explain the scenario

