# Contributing to cookiecutter-ai-conventions

Thank you for your interest in contributing! This project thrives on community contributions, especially new convention domains.

## Ways to Contribute

### 1. Creating New Domains

Domains are the heart of this project. To create a new domain:

1. **Choose a domain name** (e.g., `rust`, `docker`, `frontend`)

2. **Create the domain structure**:
   ```
   community-domains/
   └── your-domain/
       └── core.md         # Required: Core conventions
       └── advanced.md     # Optional: Advanced patterns
       └── examples.md     # Optional: Code examples
   ```

3. **Write clear, actionable conventions**:
   - Focus on "what to do" not "what not to do"
   - Include examples where helpful
   - Keep it scannable with good headers
   - Be opinionated but explain why

4. **Update the registry**:
   Add your domain to `community-domains/registry.yaml`:
   ```yaml
   - name: your-domain
     description: Brief description of what this covers
     author: your-github-username
     files:
       - core.md
       - advanced.md  # if you have additional files
     default: false  # true only for essential domains
   ```

### 2. Improving Existing Domains

- Fix typos or unclear explanations
- Add missing conventions
- Provide better examples
- Update outdated practices

### 3. Enhancing the Framework

- Improve the installer (`install.py`)
- Add new provider adapters (Cursor, Aider, etc.)
- Enhance the Textual TUI
- Fix bugs

## Pull Request Process

1. **Fork the repository**

2. **Create a feature branch**:
   ```bash
   git checkout -b add-rust-domain
   ```

3. **Make your changes**

4. **Test your changes**:
   - For new domains: Test with a generated project
   - For code changes: Run the test suite

5. **Commit with clear messages**:
   ```bash
   git commit -m "feat: Add Rust domain with safety conventions"
   ```

6. **Push and create PR**:
   - Fill out the PR template
   - Link any related issues
   - Be patient with reviews

## Domain Guidelines

### What Makes a Good Domain?

- **Focused**: Covers one area well (e.g., "react" not "frontend")
- **Practical**: Based on real usage, not theory
- **Opinionated**: Makes choices and explains them
- **Actionable**: Tells AI what to do
- **Living**: Can evolve with community input

### Domain File Structure

Each domain must have at least a `core.md` file:

```markdown
# [Domain] Core - Essential [Domain] Guidance

## Brief introduction paragraph

## Section 1
Clear guidance with examples

## Section 2
More patterns and practices

## Best Practices
- Bullet points for quick reference
- Keep these actionable
- Link to resources sparingly
```

## Code Style

- Python: Follow PEP 8
- Use type hints where helpful
- Keep it simple and readable
- Document complex logic

## Testing

Before submitting:
```bash
# Run tests
pytest tests/

# Test generation with your changes
cookiecutter . --no-input
cd my-ai-conventions
./install.py
```

## Getting Help

- Open an issue for questions
- Join discussions in existing issues
- Check existing domains for examples

## Recognition

Contributors will be:
- Listed in the domain registry
- Mentioned in release notes
- Thanked in our hearts ❤️

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

Thank you for helping make AI coding assistance better for everyone!
