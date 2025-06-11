# Coding Standards

This document defines the coding standards and conventions for {{ cookiecutter.project_name }}.

Unless otherwise specified, follow language-specific best practices (PEP8 for Python, ESLint for JavaScript, etc.).

## Project Information

- **Project**: {{ cookiecutter.project_name }}
- **Author**: {{ cookiecutter.author_name }}
- **Conventions Source**: domains/ directory

{%- set domains = cookiecutter.default_domains.split(',') %}

{%- if "git" in domains %}

## Git Conventions

### Commit Messages
- Use conventional commit format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep subject line under 50 characters
- Use imperative mood ("Add feature" not "Added feature")

### Branch Naming
- feature/* - New features
- fix/* - Bug fixes
- docs/* - Documentation changes

### Pull Requests
- Clear, descriptive titles
- Link related issues
- Include test plan

For complete git conventions, see: domains/git/core.md
{%- endif %}

{%- if "testing" in domains %}

## Testing

### Framework
- Use pytest for Python testing (not unittest)
- Follow progressive testing approach: E2E → Integration → Unit

### Test Structure
```python
def test_behavior_when_condition():
    """Test that behavior occurs when condition is met."""
    # Arrange - Set up test data
    # Act - Execute the behavior  
    # Assert - Verify the outcome
```

### Requirements
- Each new function needs comprehensive tests
- Include positive ("happy path") test cases
- Include negative (error-handling) test cases
- Use descriptive test names

For complete testing conventions, see: domains/testing/core.md
{%- endif %}

{%- if "writing" in domains %}

## Documentation

### Code Documentation
- Include detailed docstrings for all public functions
- Use triple double quotes ("""Docstring""")
- Include type hints in function signatures
- Document edge cases and assumptions

### Technical Writing
- Start with the problem, not the solution
- Use concrete examples
- Active voice
- Progressive disclosure of complexity

For complete writing conventions, see: domains/writing/core.md
{%- endif %}

## Code Layout

### General Principles
- Keep functions short and focused
- Limit line length appropriately for the language
- Group related functionality
- Clear separation of concerns

### Naming
- Use descriptive, meaningful names
- Follow language-specific conventions:
  - Python: snake_case for functions/variables, PascalCase for classes
  - JavaScript: camelCase for functions/variables, PascalCase for classes
- UPPER_CASE for constants

## Security

- Never hardcode secrets or credentials
- Use environment variables for sensitive data
- Validate all external input
- Follow principle of least privilege

{%- if cookiecutter.enable_learning_capture %}

## Learning Capture

This project uses a learning capture system to evolve conventions:
- New insights are captured in staging/learnings.md
- Use commands/capture-learning.py to record patterns
- Periodically review and promote stable patterns

When you notice repeated patterns or corrections, capture them for future reference.
{%- endif %}

## Additional Resources

For detailed, domain-specific conventions, refer to:
{%- for domain in domains %}
- domains/{{ domain.strip() }}/core.md - {{ domain.strip()|title }} conventions
{%- endfor %}
- global.md - Universal patterns

---

These conventions are living documents. They evolve based on team experience and project needs.