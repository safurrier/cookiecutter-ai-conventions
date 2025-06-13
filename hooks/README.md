# Cookiecutter Hooks

This directory contains the pre- and post-generation hooks for the cookiecutter-ai-conventions template.

## Structure

- `pre_gen_project.py` - Interactive domain selection (runs before project generation)
- `post_gen_project.py` - Cleanup and configuration (runs after project generation)
- `models.py` - Data models (ProviderFiles, PROVIDER_REGISTRY)
- `constants.py` - Shared constants (DEFAULT_DOMAINS, INSTALL_TOOLS, etc.)

## Important Note on Imports

Due to how cookiecutter executes hooks (by creating temporary files), the hook files cannot reliably import from other files in this directory. Therefore:

1. **For development**: Use the separate `models.py` and `constants.py` files for better organization
2. **For execution**: The hook files contain inline copies of all necessary data structures and constants

**When making changes**: Always update both the separate files AND the inline definitions in the hook files.

## Hook Execution Flow

### Pre-generation Hook
1. Detects if running interactively
2. Loads domain registry (YAML file with available domains)
3. Presents domain selection UI (Rich TUI or simple text)
4. Stores selected domains for post-generation hook

### Post-generation Hook
1. Copies selected domains from community-domains to project
2. Creates configuration file (.ai-conventions.yaml)
3. Removes files for unselected providers
4. Handles provider-specific setup (permissions, renames, etc.)
5. Cleans up empty directories
6. Updates README with included components

## Testing

The hooks are tested through:
- `tests/test_integration_hooks.py` - Unit tests for hook functions
- `tests/test_e2e_cookiecutter.py` - End-to-end tests with actual cookiecutter
- `tests/test_smoke_basic.py` - Basic structure validation