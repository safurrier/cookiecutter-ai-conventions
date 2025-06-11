# CLAUDE.md - Cookiecutter AI Conventions

## Project Overview
This is a cookiecutter template for creating AI development convention projects. It helps teams establish and maintain consistent coding standards when working with AI assistants like Claude, Cursor, Windsurf, and Aider.

## Quick Start Commands

### Development Setup
```bash
make setup          # Install dependencies and set up environment
make check          # Run all quality checks (lint, test)
make test           # Run tests
make lint           # Run linter
make format         # Format code
```

### Testing & Debugging
```bash
make test-verbose   # Run tests with verbose output
make test-coverage  # Run tests with coverage report
make ci-local       # Run CI checks locally (mimics GitHub Actions)
make test-cookiecutter  # Test template generation
```

### Common Workflows

#### 1. Before committing changes:
```bash
make check          # Runs lint + tests
```

#### 2. Fix code issues:
```bash
make format         # Auto-fix formatting and linting issues
```

#### 3. Debug CI failures locally:
```bash
make ci-local       # Runs the same checks as GitHub Actions
```

#### 4. Clean up:
```bash
make clean          # Remove all generated files
make clean-output   # Remove just test output directories
```

## Project Structure

```
.
├── {{cookiecutter.project_slug}}/     # Template directory
│   ├── domains/                       # Convention domains (empty, filled by hooks)
│   ├── commands/                      # Learning capture scripts
│   ├── templates/                     # Provider-specific templates
│   └── community-domains/             # Available domains (copied during generation)
├── hooks/                             # Cookiecutter hooks
│   ├── pre_gen_project.py            # Pre-generation hook (TUI)
│   └── post_gen_project.py           # Post-generation hook (setup)
├── tests/                             # Test suite
│   ├── test_e2e_cookiecutter.py      # End-to-end tests
│   ├── test_integration_hooks.py      # Integration tests
│   └── test_smoke_basic.py           # Smoke tests
└── community-domains/                 # Master domain repository
```

## Key Features

1. **Interactive Domain Selection**: TUI for choosing convention domains
2. **Learning Capture**: Commands to capture and evolve conventions
3. **Multi-Provider Support**: Templates for Claude, Cursor, Windsurf, Aider
4. **Progressive Testing**: E2E → Smoke → Integration test structure

## Testing Approach

We follow a progressive testing strategy:
- **E2E Tests**: Test complete cookiecutter generation
- **Smoke Tests**: Quick validation without generation
- **Integration Tests**: Test individual components

## Common Issues & Solutions

### Pre-commit hooks failing
```bash
# Reinstall pre-commit hooks
uv run pre-commit uninstall
uv run pre-commit install

# Or run without hooks
git commit --no-verify
```

### CI failing but works locally
```bash
# Run exact CI checks
make ci-local

# Check Python version
uv venv --python 3.12  # CI uses multiple versions
```

### Test failures
```bash
# Run specific test with details
uv run pytest tests/test_e2e_cookiecutter.py::TestE2ECookiecutterGeneration::test_generate_project_with_defaults -xvs

# Check test output
ls -la test-output*/
```

## Making Changes

1. **Always run tests before committing**:
   ```bash
   make check
   ```

2. **Format code automatically**:
   ```bash
   make format
   ```

3. **Test template generation**:
   ```bash
   make test-cookiecutter
   ```

## Build Commands Reference

All commands are in the Makefile. Run `make help` to see all available targets.

Key commands:
- `make setup` - Set up development environment
- `make check` - Run all quality checks
- `make ci-local` - Debug CI issues locally
- `make clean` - Clean all generated files