# Configuration Management System

The AI Conventions template includes a comprehensive configuration management system with support for multiple formats, validation, and migration between formats.

## Features

- **Multiple Format Support**: YAML, TOML, JSON, and pyproject.toml
- **Pydantic Validation**: Type-safe configuration with automatic validation
- **Format Migration**: Convert between configuration formats
- **CLI Tools**: Command-line interface for configuration management
- **Auto-discovery**: Automatically finds configuration files in standard locations

## Configuration Schema

The configuration uses Pydantic models for validation:

```python
class ConventionsConfig(BaseModel):
    project_name: str
    project_slug: str
    author_name: str
    author_email: Optional[str]
    selected_providers: list[str]
    enable_learning_capture: bool = True
    enable_context_canary: bool = True
    enable_domain_composition: bool = True
    default_domains: str = "git,testing"
```

## File Locations

The configuration system searches for files in this order:

1. `.ai-conventions.yaml` / `.ai-conventions.yml`
2. `.ai-conventions.toml`
3. `.ai-conventions.json`
4. `ai-conventions.yaml` / `ai-conventions.yml`
5. `ai-conventions.toml`
6. `ai-conventions.json`
7. `pyproject.toml` (under `[tool.ai-conventions]`)

## CLI Commands

The `conventions-config` command provides several subcommands:

### Show Configuration

Display the current configuration:

```bash
# Show as YAML (default)
conventions-config show

# Show as JSON
conventions-config show -f json

# Show as TOML
conventions-config show -f toml

# Show specific file
conventions-config show -p /path/to/config.yaml
```

### Validate Configuration

Check if a configuration file is valid:

```bash
conventions-config validate

# Validate specific file
conventions-config validate -p config.toml
```

### Initialize Configuration

Create a new configuration file interactively:

```bash
# Create YAML config (default)
conventions-config init

# Create TOML config
conventions-config init -f toml

# Create JSON config
conventions-config init -f json

# Specify output path
conventions-config init -p my-config.yaml
```

### Migrate Configuration

Convert between formats:

```bash
# Convert YAML to TOML
conventions-config migrate config.yaml toml

# Convert to JSON with custom output
conventions-config migrate config.yaml json -o settings.json

# Convert from pyproject.toml to standalone YAML
conventions-config migrate pyproject.toml yaml
```

## Format Examples

### YAML Format

```yaml
project_name: My AI Project
project_slug: my-ai-project
author_name: Jane Developer
author_email: jane@example.com
selected_providers:
  - claude
  - cursor
  - aider
enable_learning_capture: true
enable_context_canary: true
enable_domain_composition: true
default_domains: git,testing,python
```

### TOML Format

```toml
project_name = "My AI Project"
project_slug = "my-ai-project"
author_name = "Jane Developer"
author_email = "jane@example.com"
selected_providers = ["claude", "cursor", "aider"]
enable_learning_capture = true
enable_context_canary = true
enable_domain_composition = true
default_domains = "git,testing,python"
```

### JSON Format

```json
{
  "project_name": "My AI Project",
  "project_slug": "my-ai-project",
  "author_name": "Jane Developer",
  "author_email": "jane@example.com",
  "selected_providers": ["claude", "cursor", "aider"],
  "enable_learning_capture": true,
  "enable_context_canary": true,
  "enable_domain_composition": true,
  "default_domains": "git,testing,python"
}
```

### pyproject.toml Format

```toml
[tool.ai-conventions]
project_name = "My AI Project"
project_slug = "my-ai-project"
author_name = "Jane Developer"
author_email = "jane@example.com"
selected_providers = ["claude", "cursor", "aider"]
enable_learning_capture = true
enable_context_canary = true
enable_domain_composition = true
default_domains = "git,testing,python"
```

## Programmatic Usage

You can also use the configuration system programmatically:

```python
from ai_conventions.config import ConfigManager, ConventionsConfig

# Load configuration
manager = ConfigManager()
config = manager.load_config()

# Create new configuration
new_config = ConventionsConfig(
    project_name="My Project",
    project_slug="my-project",
    author_name="Developer",
    selected_providers=["claude", "cursor"]
)

# Save configuration
manager.save_config(new_config, format_type="yaml")

# Migrate between formats
manager.migrate_config(
    source_path=Path("config.yaml"),
    target_format="toml"
)

# Validate configuration
valid, errors = manager.validate_config()
```

## Environment Variables

The configuration system also supports environment variable overrides:

- `AI_CONVENTIONS_PROJECT_NAME`
- `AI_CONVENTIONS_AUTHOR_NAME`
- `AI_CONVENTIONS_PROVIDERS` (comma-separated)

## Best Practices

1. **Version Control**: Commit your configuration file to version control
2. **Format Choice**: 
   - Use YAML for human-friendly editing with comments
   - Use TOML for Python projects (can be part of pyproject.toml)
   - Use JSON for programmatic generation/consumption
3. **Validation**: Always validate after manual edits
4. **Migration**: Use the migration tool when changing formats to ensure data integrity