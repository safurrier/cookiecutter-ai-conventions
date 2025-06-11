# Copilot Instructions for {{ cookiecutter.project_name }}

These are the coding standards and conventions for {{ cookiecutter.project_name }}. Always follow these guidelines when generating code.

## Project Information

- **Project**: {{ cookiecutter.project_name }}
- **Author**: {{ cookiecutter.author_name }}

{%- set domains = cookiecutter.default_domains.split(',') %}

## Core Conventions

{%- if "git" in domains %}

### Git Conventions

- Always use conventional commit format: `type(scope): description`
- Commit types: feat, fix, docs, style, refactor, test, chore
- Keep commit messages under 50 characters
- Use imperative mood in commit messages ("Add" not "Added")
- Branch naming: feature/*, fix/*, docs/*
- Include tests with new features
- Link issues in pull requests
{%- endif %}

{%- if "testing" in domains %}

### Testing Standards

- Always use pytest for Python testing, never unittest
- Test function names must describe the behavior: `test_behavior_when_condition()`
- Include both positive and negative test cases
- Use fixtures for test data setup
- Follow Arrange-Act-Assert pattern
- Mock external dependencies
- Aim for high code coverage
{%- endif %}

{%- if "writing" in domains %}

### Documentation Standards

- Always include docstrings for public functions
- Use triple double quotes for docstrings
- Include type hints in function signatures
- Document parameters, returns, and exceptions
- Start documentation with the problem being solved
- Use active voice in documentation
- Include code examples in docstrings
{%- endif %}

## General Coding Standards

- Clear, descriptive variable and function names
- Consistent error handling patterns
- No hardcoded secrets or credentials
- Follow language-specific conventions (PEP 8 for Python, etc.)
- Keep functions focused and single-purpose
- Prefer composition over inheritance
- Write self-documenting code

{%- if "python" in domains %}

### Python Specific

- Use type hints for all function parameters and returns
- Group imports: standard library, third-party, local
- One import per line
- Use f-strings for string formatting
- Context managers for resource handling
- Dataclasses for data structures
{%- endif %}

{%- if cookiecutter.enable_learning_capture %}

## Convention Evolution

This project captures and evolves coding patterns. When you notice repeated patterns or corrections, they should be captured for future reference.
{%- endif %}

## Key Principles

1. **Clarity over cleverness** - Write code that is easy to understand
2. **Consistency** - Follow established patterns in the codebase
3. **Test everything** - New code needs tests
4. **Document intent** - Explain why, not just what
5. **Handle errors gracefully** - Anticipate and handle failure cases

When in doubt, look at existing code in the project for examples of these conventions in practice.