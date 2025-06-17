# Developing

This guide covers how to set up the development environment and contribute to the cookiecutter-ai-conventions project.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/safurrier/cookiecutter-ai-conventions.git
cd cookiecutter-ai-conventions

# Set up development environment
make setup

# Run tests
make check
```

## Development Environment Setup

### Prerequisites

- Python 3.12+ (recommended)
- UV package manager (will be installed automatically)

### Setup

```bash
# Install UV and set up the environment
make setup
```

This will:
- Install UV if not present
- Create a virtual environment with Python 3.12
- Install the project in editable mode with dev dependencies
- Set up pre-commit hooks

## Key Make Commands

### Testing

```bash
make test           # Run all tests (parallel + serial)
make test-watch     # Run tests in watch mode
make test-e2e       # Run end-to-end tests only
make ci-local       # Run CI checks locally (mimics GitHub Actions)
```

### Code Quality

```bash
make lint           # Run linting with ruff
make format         # Format code with ruff
make mypy           # Run type checking
make check          # Run all checks (lint + type + test)
make pre-commit     # Run pre-commit hooks on all files
```

### Template Testing

```bash
make test-cookiecutter  # Test template generation
make clean-output       # Clean test output directories
```

### Development Workflow

```bash
make clean          # Clean up generated files
make help           # Show all available commands
```

## Testing from Branches

You can test the cookiecutter template directly from a Git branch:

### Test from Current Branch

```bash
# Test the current working branch
uvx cookiecutter . --no-input

# Test with custom values
uvx cookiecutter . --no-input \
  project_name="My Test Project" \
  selected_providers="claude,cursor"
```

### Test from Remote Branch

```bash
# Test from a specific branch on GitHub
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions \
  --checkout feature-branch \
  --no-input

# Test from a pull request
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions \
  --checkout pull/123/head \
  --no-input
```

### Test with Interactive Mode

```bash
# Use the TUI for provider/domain selection
uvx cookiecutter . 

# Or from a branch
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions \
  --checkout your-branch-name
```

## Project Structure

```
.
├── docs/                    # Documentation
├── hooks/                   # Cookiecutter hooks
│   ├── pre_gen_project.py  # Pre-generation TUI
│   └── post_gen_project.py # Post-generation setup
├── tests/                   # Test suite
│   ├── test_e2e_*.py       # End-to-end tests
│   ├── test_*.py           # Unit tests
│   └── conftest.py         # Test configuration
├── {{cookiecutter.project_slug}}/  # Template directory
│   ├── ai_conventions/     # Python package
│   ├── domains/            # Convention domains
│   ├── templates/          # Provider templates
│   └── community-domains/  # Available domains
├── community-domains/       # Master domain repository
├── cookiecutter.json       # Template configuration
├── Makefile                # Development commands
└── pyproject.toml          # Project configuration
```

## Testing Strategy

We follow a progressive testing approach:

1. **E2E Tests** (`test_e2e_*.py`): Test complete cookiecutter generation
2. **Integration Tests**: Test component interactions
3. **Unit Tests**: Test individual functions and classes
4. **Smoke Tests**: Quick validation without full generation

### Test Markers

- `@pytest.mark.serial`: Tests that must run sequentially (not in parallel)
- `@pytest.mark.slow`: Longer-running tests
- `@pytest.mark.skipif`: Platform-specific tests

## Common Development Tasks

### Adding a New Provider

1. Add provider files to `{{cookiecutter.project_slug}}/ai_conventions/providers/`
2. Update `PROVIDER_REGISTRY` in `hooks/post_gen_project.py`
3. Add tests in `tests/test_*_provider.py`
4. Update documentation

### Adding a New Domain

1. Add domain files to `community-domains/`
2. Update domain selection in `hooks/pre_gen_project.py`
3. Add tests for domain functionality
4. Update documentation

### Modifying the TUI

1. Edit `hooks/pre_gen_project.py` for the Textual TUI
2. Test with `make test-cookiecutter`
3. Ensure both interactive and `--no-input` modes work

## Debugging Tips

### Test Failures

```bash
# Run specific test with verbose output
uv run pytest tests/test_specific.py::test_function -xvs

# Run tests without parallel execution
uv run pytest -m "not serial"

# Debug E2E failures by checking generated output
make test-cookiecutter
ls -la test-output/
```

### Template Issues

```bash
# Generate template and inspect
make test-cookiecutter
cd test-output/my-ai-conventions/
uv tool install .
ai-conventions status
```

### CI Failures

```bash
# Run exact CI checks locally
make ci-local
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `make check`
5. Commit with conventional commit format: `feat: add new feature`
6. Push and create a pull request

### Commit Message Format

```
type: description

Types: feat, fix, docs, style, refactor, test, chore
```

Examples:
- `feat: add Windsurf provider support`
- `fix: resolve CLI import errors`
- `docs: update installation instructions`

## Release Process

1. Update version in relevant files
2. Run full test suite: `make check`
3. Create release PR
4. Tag release: `git tag v1.0.0`
5. Push tags: `git push --tags`

## Performance Considerations

- Template generation should complete in under 30 seconds
- UV tool installation should complete in under 60 seconds
- Test suite should complete in under 5 minutes
- Use parallel testing where possible (`pytest -n auto`)

## Troubleshooting

### UV Installation Issues

```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or restart shell
```

### Virtual Environment Issues

```bash
# Clean and recreate environment
rm -rf .venv
make setup
```

### Test Isolation Issues

```bash
# Clean test artifacts
make clean
make clean-output
```

For more troubleshooting help, see [troubleshooting.md](troubleshooting.md).