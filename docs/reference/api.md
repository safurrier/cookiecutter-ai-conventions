# API Reference

This section provides comprehensive API documentation for the AI Conventions system.

!!! note "Template Documentation"
    This is the API reference for the cookiecutter template. When you generate a project, the API will be available under your project's module structure.

## Overview

The AI Conventions system consists of several core modules:

### Core Components

- **Domain Resolver**: Handles domain inheritance and composition
- **Provider System**: Manages AI tool integrations (Claude, Cursor, Windsurf, etc.)
- **CLI System**: Command-line interface for managing conventions
- **Learning Capture**: Automatic pattern detection and evolution
- **Configuration**: Project and global settings management

### Module Structure

```
ai_conventions/
├── __init__.py           # Package initialization
├── cli.py               # Command-line interface
├── config.py            # Configuration management
├── domain_resolver.py   # Domain inheritance system
├── capture.py           # Learning capture system
├── sync.py              # Provider synchronization
├── tui.py              # Text user interface
└── providers/          # Provider implementations
    ├── __init__.py
    ├── base.py         # Base provider interface
    ├── claude.py       # Claude provider
    ├── cursor.py       # Cursor provider
    ├── windsurf.py     # Windsurf provider
    ├── aider.py        # Aider provider
    └── ...
```

## Key Classes and Functions

### Domain Resolution

The domain resolver handles loading and composing convention domains:

```python
from ai_conventions.domain_resolver import DomainResolver, resolve_shorthand_syntax

# Create resolver
resolver = DomainResolver(domains_path=Path("domains"))

# Resolve domain with inheritance
content = resolver.resolve_domain("testing")

# Convert shorthand syntax
text = "Use %testing patterns"
resolved = resolve_shorthand_syntax(text)
# Result: "Use @domains/testing/core.md patterns"
```

### Provider System

Base provider interface for AI tool integrations:

```python
from ai_conventions.providers.base import BaseProvider, ProviderCapabilities

class MyProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "my-tool"
    
    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            supports_imports=True,
            supports_commands=True,
            max_context_tokens=100_000,
            file_watch_capable=False,
            symlink_capable=True,
            config_format='markdown'
        )
```

### CLI Usage

The CLI provides commands for managing conventions:

```python
from ai_conventions.cli import main

# Available commands:
# - ai-conventions status
# - ai-conventions list  
# - ai-conventions sync
# - capture-learning
```

## Configuration Schema

Configuration files use YAML format:

```yaml
# .ai-conventions.yaml
project:
  name: "My Project"
  author: "Your Name"

providers:
  claude:
    enabled: true
    auto_sync: true
    use_symlinks: true

domains:
  default: [git, testing, writing]
  
learning_capture:
  enabled: true
  auto_review: weekly
```

## Extension Points

### Custom Providers

Create custom AI tool providers:

```python
from ai_conventions.providers.base import BaseProvider

class CustomProvider(BaseProvider):
    # Implement required methods
    def install(self) -> InstallResult:
        # Custom installation logic
        pass
```

### Custom Domains

Create domain files with YAML frontmatter:

```markdown
---
extends: base-domain
triggers: ["custom", "keywords"]
---

# Custom Domain

Custom conventions and patterns...
```

## Development

For development and testing:

```bash
# Install in development mode
uv tool install --editable .

# Run tests
uv run pytest

# Build documentation
uv run mkdocs build
```