# AI Development Agent for {{ cookiecutter.project_name }}

You are an AI development assistant working on {{ cookiecutter.project_name }}. Follow these conventions and standards when generating or modifying code.

## Project Context

- **Project**: {{ cookiecutter.project_name }}
- **Author**: {{ cookiecutter.author_name }}
- **Purpose**: AI-assisted development with consistent conventions

{%- set domains = cookiecutter.default_domains.split(',') %}

## Development Standards

{%- if "git" in domains %}

### Version Control

When working with Git:
- Always use conventional commit format: `type(scope): description`
- Valid types: feat, fix, docs, style, refactor, test, chore
- Keep commit messages under 50 characters
- Use imperative mood ("Add feature" not "Added feature")
- Create descriptive branch names: feature/*, fix/*, docs/*
- Include tests with new features
- Reference issues in commits when applicable
{%- endif %}

{%- if "testing" in domains %}

### Testing Requirements

When writing or generating tests:
- Always use pytest for Python testing, never unittest
- Name test functions as `test_behavior_when_condition()`
- Include both positive (happy path) and negative (error) test cases
- Use fixtures for test data setup
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies appropriately
- Aim for comprehensive test coverage
{%- endif %}

{%- if "writing" in domains %}

### Documentation Standards

When writing documentation:
- Always include docstrings for public functions
- Use triple double quotes """Docstring"""
- Include type hints in function signatures
- Document parameters, return values, and exceptions
- Start with the problem being solved, not the solution
- Use active voice and clear language
- Include usage examples in docstrings
{%- endif %}

## Code Generation Guidelines

When generating new code:
1. Follow language-specific conventions (PEP 8 for Python, ESLint for JavaScript)
2. Use descriptive variable and function names
3. Keep functions focused and single-purpose
4. Handle errors gracefully with proper exception handling
5. Never hardcode secrets or credentials
6. Write self-documenting code with clear intent

{%- if "python" in domains %}

### Python Specific

- Use type hints for all function parameters and returns
- Organize imports: standard library, third-party, local
- Use f-strings for string formatting
- Prefer pathlib over os.path
- Use context managers for resource handling
{%- endif %}

## Interaction Patterns

When I ask you to:
- **"Create a new feature"** - Start with tests, then implementation
- **"Fix a bug"** - Reproduce with a test, then fix
- **"Refactor code"** - Ensure tests pass before and after
- **"Add documentation"** - Follow the documentation standards above

{%- if cookiecutter.enable_learning_capture %}

## Convention Evolution

This project uses a learning capture system. When you notice patterns that should be standardized:
- Point them out during our interactions
- Suggest additions to the convention system
- Help maintain consistency across the codebase
{%- endif %}

## Convention Improvement Workflow

**Use this workflow to continuously improve conventions based on user corrections and feedback.**

### Review & Capture Process

1. **Analyze interactions** for improvement opportunities:
   - Where did the user correct your approach?
   - What patterns emerged that aren't documented?
   - Which domain conventions were missed?

2. **Use CLI commands** to update conventions:

```bash
# Explore available convention domains
ai-conventions list

# Check installation status
ai-conventions status

{%- if cookiecutter.enable_learning_capture %}
# Capture learnings from user corrections
capture-learning "User feedback or correction" --domain [target] --category [type]

# Examples:
capture-learning "Use async/await for database calls" --domain python --category pattern
capture-learning "Avoid nested ternary operators" --domain global --category anti-pattern
{%- endif %}

# Sync updated conventions to AI providers  
ai-conventions sync
```

3. **Improve automatic loading**: Consider if context triggers should be enhanced to auto-load relevant domains.

This systematic approach ensures conventions evolve based on real development patterns and user feedback.

## File Organization

Understand the project structure:
- `domains/` - Convention definitions by domain
- `global.md` - Universal patterns and principles
{%- if cookiecutter.enable_learning_capture %}
- `staging/learnings.md` - Captured patterns for review
- `commands/` - Learning capture utilities
{%- endif %}
- `docs/` - Project documentation

## Safety and Security

Always:
- Validate user input before processing
- Use parameterized queries for databases
- Implement proper authentication and authorization
- Follow the principle of least privilege
- Keep dependencies up to date

Remember: The goal is to maintain consistent, high-quality code that follows established patterns while being open to improvements through the learning system.