# Configuration Reference

The AI Conventions system uses YAML configuration files for customization and provider settings.

## Configuration Files

### Project Configuration (`.ai-conventions.yaml`)

Located in your project root, this file controls project-specific settings:

```yaml
# Project metadata
project:
  name: "My AI Project"
  author: "Your Name"
  description: "AI development conventions for my project"

# Provider configuration
providers:
  claude:
    enabled: true
    auto_sync: true
    use_symlinks: true
    install_path: "~/.claude"
  
  cursor:
    enabled: true
    auto_sync: false
    use_symlinks: false
    install_path: ".cursorrules"
  
  windsurf:
    enabled: false
    
  aider:
    enabled: true
    auto_sync: true

# Domain settings
domains:
  # Default domains to include
  default: 
    - git
    - testing
    - writing
  
  # Custom domain paths
  custom_paths:
    - "./custom-domains/"
    - "~/shared-domains/"
  
  # Domain composition settings
  composition:
    enabled: true
    max_depth: 3
    circular_check: true

# Learning capture system
learning_capture:
  enabled: true
  auto_review: "weekly"  # never, daily, weekly, monthly
  archive_after: "90d"   # Archive learnings after N days
  categories:
    - pattern
    - fix
    - anti-pattern
    - tool-specific
    - other

# Context detection
context_detection:
  enabled: true
  triggers:
    git: ["git", "commit", "branch", "merge", "rebase"]
    testing: ["test_", "pytest", "assert", "fixture"]
    writing: ["README", "docs", "commit message"]
  
# Advanced settings
advanced:
  template_engine: "jinja2"
  context_compression: true
  canary_system: true
  debug_mode: false
```

### Global Configuration (`~/.ai-conventions/config.yaml`)

System-wide settings that apply across all projects:

```yaml
# Global preferences
global:
  default_providers: [claude, cursor]
  auto_update_check: true
  telemetry: false

# Provider defaults
provider_defaults:
  use_symlinks: true
  auto_sync: true
  backup_on_sync: true

# Domain registry
domain_registry:
  # Community domain sources
  sources:
    - url: "https://github.com/ai-conventions/community-domains"
      branch: "main"
      update_frequency: "weekly"
  
  # Local domain collections
  local_collections:
    - path: "~/domains/work/"
      name: "Work Domains"
    - path: "~/domains/personal/"
      name: "Personal Domains"

# CLI preferences
cli:
  default_output_format: "rich"  # rich, plain, json
  confirmation_prompts: true
  color_output: true
```

## Provider-Specific Configuration

### Claude Provider

```yaml
providers:
  claude:
    enabled: true
    
    # Installation settings
    install_path: "~/.claude"
    use_symlinks: true
    backup_existing: true
    
    # Sync behavior
    auto_sync: true
    sync_on_change: true
    
    # Template settings
    template_path: "./templates/claude/"
    context_variables:
      canary_timestamp: true
      project_info: true
    
    # Features
    features:
      learning_capture: true
      domain_composition: true
      context_canary: true
      shorthand_syntax: true
```

### Cursor Provider

```yaml
providers:
  cursor:
    enabled: true
    
    # File configuration
    rules_file: ".cursorrules"
    config_dir: ".cursor/"
    
    # Installation mode
    use_symlinks: false  # Cursor works better with copies
    
    # Content settings
    include_imports: true
    include_context_mapping: true
    max_file_size: "50KB"
    
    # Rule formatting
    format:
      line_length: 80
      include_examples: true
      group_by_domain: true
```

### Windsurf Provider

```yaml
providers:
  windsurf:
    enabled: true
    
    # Configuration files
    rules_file: ".windsurfrules"
    config_dir: ".windsurf/"
    
    # Features
    features:
      cascading_rules: true
      project_context: true
      file_watchers: true
    
    # Performance
    performance:
      lazy_loading: true
      cache_rules: true
      max_context_size: "100KB"
```

## Domain Configuration

### Domain Structure

Each domain can have its own configuration in `domain.yaml`:

```yaml
# domains/testing/domain.yaml
domain:
  name: "testing"
  description: "Testing patterns and best practices"
  version: "1.2.0"
  
# Inheritance
extends:
  - base
  - quality-assurance

# Files in this domain
files:
  core.md: "Core testing conventions"
  unit-tests.md: "Unit testing patterns"
  e2e-tests.md: "End-to-end testing strategies"
  
# Context triggers
triggers:
  keywords: ["test", "pytest", "assert", "fixture", "mock"]
  file_patterns: ["*_test.py", "test_*.py", "tests/**/*.py"]
  commands: ["pytest", "python -m pytest"]

# Provider compatibility
providers:
  claude: true
  cursor: true
  windsurf: true
  aider: true

# Learning capture
learning:
  auto_capture: true
  review_frequency: "monthly"
  categories: ["pattern", "anti-pattern", "tool-specific"]
```

### Domain Registry

The community domain registry (`community-domains/registry.json`) lists available domains:

```json
{
  "domains": {
    "git": {
      "name": "Git Workflows",
      "description": "Version control best practices",
      "version": "2.1.0",
      "maintainer": "ai-conventions",
      "tags": ["vcs", "git", "workflows"],
      "files": ["core.md", "commit-messages.md", "branching.md"],
      "dependencies": ["global"],
      "providers": ["claude", "cursor", "windsurf", "aider"]
    },
    "testing": {
      "name": "Testing Patterns",
      "description": "Testing strategies and best practices",
      "version": "1.8.0",
      "maintainer": "ai-conventions",
      "tags": ["testing", "quality", "automation"],
      "files": ["core.md", "unit-tests.md", "e2e-tests.md"],
      "dependencies": ["global"],
      "providers": ["claude", "cursor", "windsurf", "aider"]
    }
  },
  "collections": {
    "web-development": {
      "name": "Web Development",
      "domains": ["javascript", "typescript", "react", "api-design"],
      "description": "Complete web development conventions"
    }
  }
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_CONVENTIONS_HOME` | Base directory for conventions | `~/.ai-conventions` |
| `AI_CONVENTIONS_CONFIG` | Global configuration file | `~/.ai-conventions/config.yaml` |
| `AI_CONVENTIONS_PROJECT_CONFIG` | Project configuration file | `./.ai-conventions.yaml` |
| `AI_CONVENTIONS_DEBUG` | Enable debug logging | `false` |
| `AI_CONVENTIONS_NO_TELEMETRY` | Disable telemetry | `false` |
| `AI_CONVENTIONS_OFFLINE` | Offline mode (no updates) | `false` |

## Configuration Validation

The system validates configuration files on startup:

```bash
# Validate current configuration
ai-conventions config validate

# Validate specific config file
ai-conventions config validate --file .ai-conventions.yaml

# Show configuration schema
ai-conventions config schema
```

## Migration from Legacy Configurations

### From .cursorrules

```bash
# Migrate existing .cursorrules to AI conventions
ai-conventions migrate --from cursorrules --file .cursorrules
```

### From Custom Systems

```yaml
# Migration configuration
migration:
  source: "custom"
  mapping:
    # Map file patterns to domains
    "lint-rules.md": "quality/linting"
    "git-standards.md": "git/core"
    "test-guidelines.md": "testing/core"
  
  # Transformation rules
  transformations:
    - from: "# Rule:"
      to: "## Convention:"
    - from: "❌ Don't"
      to: "**Anti-pattern:**"
```

## Best Practices

### Configuration Organization

1. **Keep project configs minimal** - Use global defaults where possible
2. **Document custom settings** - Add comments explaining non-standard choices
3. **Version control** - Include `.ai-conventions.yaml` in git
4. **Environment-specific** - Use different configs for dev/staging/prod

### Security Considerations

1. **No secrets in config** - Use environment variables for sensitive data
2. **Validate inputs** - Always validate configuration before applying
3. **Backup before changes** - Enable backup_on_sync for safety
4. **Review permissions** - Check file permissions on configuration files

### Performance Optimization

1. **Use symlinks** - Faster than copying for large domain collections
2. **Enable caching** - Reduce repeated domain resolution
3. **Limit context size** - Prevent excessive memory usage
4. **Lazy loading** - Only load domains when needed