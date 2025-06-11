# Aider Setup Guide

This guide helps you use your AI conventions with Aider, the AI pair programming tool.

## Installation

Your conventions are automatically configured for Aider with:
- `CONVENTIONS.md` file in the project root
- `.aider.conf.yml` configuration file

## Quick Start

1. **Install Aider**:
   ```bash
   pip install aider-chat
   ```

2. **Run Aider** in your project:
   ```bash
   cd {{ cookiecutter.project_slug }}
   aider
   ```

   Aider will automatically load your conventions from `CONVENTIONS.md`.

## How It Works

### Convention Loading

Aider uses two main files:

1. **CONVENTIONS.md** - Your project coding standards
   - Automatically loaded by Aider
   - Provides context for all AI interactions
   - Includes domain-specific conventions

2. **.aider.conf.yml** - Aider configuration
   - Sets up automatic convention loading
   - Configures read-only domain files
   - Defines project preferences

### File Structure

```
{{ cookiecutter.project_slug }}/
├── CONVENTIONS.md       # Main conventions (auto-loaded)
├── .aider.conf.yml     # Aider configuration
├── domains/            # Domain-specific conventions
│   {%- set domains = cookiecutter.default_domains.split(',') %}
│   {%- for domain in domains %}
│   ├── {{ domain.strip() }}/
│   │   └── core.md
{%- endfor %}
│   └── ...
├── global.md           # Universal patterns
{%- if cookiecutter.enable_learning_capture %}
└── staging/
    └── learnings.md    # Captured patterns
{%- endif %}
```

## Command Line Usage

### Basic Commands

```bash
# Start Aider with your conventions
aider

# Work on specific files
aider src/main.py tests/test_main.py

# Use a specific model
aider --model gpt-4o

# Read additional context
aider --read docs/api-design.md
```

### Working with Conventions

Your conventions are automatically loaded, but you can:

```bash
# Explicitly reference conventions
aider --read CONVENTIONS.md --read-only domains/

# Focus on specific domains
aider --read-only domains/testing/core.md
```

## Configuration Details

Your `.aider.conf.yml` includes:

```yaml
# Auto-loaded files
read: CONVENTIONS.md

# Read-only domain files
read-only:
  - global.md
{%- for domain in domains %}
  - domains/{{ domain.strip() }}/core.md
{%- endfor %}

# Project settings
auto-commits: false
test-cmd: {% if "testing" in domains %}pytest{% else %}# your test command{% endif %}
```

## Best Practices

### 1. Let Aider Read Conventions

Aider automatically loads `CONVENTIONS.md`. Trust it to:
- Follow your coding standards
- Apply domain patterns
- Maintain consistency

### 2. Use Chat Mode Effectively

```bash
# Ask about conventions
> What are our git commit conventions?

# Request convention-following code
> Create a test following our testing patterns

# Validate against conventions
> Does this code follow our standards?
```

### 3. Leverage Domain Knowledge

Your domains are loaded as read-only context:
{%- for domain in domains %}
{% if domain.strip() == "git" %}
- **Git**: Commit messages, branching, workflows
{%- elif domain.strip() == "testing" %}
- **Testing**: Pytest patterns, test structure
{%- elif domain.strip() == "writing" %}
- **Writing**: Documentation style, clarity
{%- endif %}
{%- endfor %}

{% if cookiecutter.enable_learning_capture %}
## Learning Capture

When you notice patterns:

1. **During Aider session**:
   ```
   > I notice we always validate input this way...
   ```

2. **Capture the learning**:
   ```bash
   ./commands/capture-learning.py
   ```

3. **Review periodically**:
   ```bash
   ./commands/review-learnings.py
   ```
{% endif %}

## Advanced Usage

### Custom Configuration

Modify `.aider.conf.yml` for:

```yaml
# Different model
model: claude-3-opus

# Editor integration
editor-model: gpt-4o

# Voice mode
voice-language: en
```

### Project-Specific Context

Add project files to context:

```yaml
read:
  - CONVENTIONS.md
  - docs/architecture.md
  - API.md
```

### Testing Integration

Aider can run tests automatically:

```yaml
test-cmd: pytest tests/
auto-test: true
```

## Troubleshooting

### Conventions Not Loading?

1. Check file exists: `CONVENTIONS.md`
2. Verify `.aider.conf.yml` syntax
3. Run with explicit read: `aider --read CONVENTIONS.md`

### Too Much Context?

1. Use `--read-only` for reference files
2. Limit to specific domains
3. Use `.aiderignore` file

### Model Selection

Choose models based on task:
- `gpt-4o`: General coding
- `claude-3-opus`: Complex reasoning
- `gpt-3.5-turbo`: Quick tasks

## Command Reference

| Command | Description |
|---------|-------------|
| `aider` | Start with conventions |
| `aider --help` | Show all options |
| `aider --read FILE` | Add file to context |
| `aider --read-only DIR/` | Add directory as reference |
| `aider --model MODEL` | Use specific model |
| `aider --test` | Run tests after changes |

## Next Steps

1. Install Aider: `pip install aider-chat`
2. Navigate to your project
3. Run `aider` - conventions load automatically
4. Start coding with AI assistance!

For more information:
- [Aider Documentation](https://aider.chat/)
- [Configuration Options](https://aider.chat/docs/config.html)
- Your conventions: `CONVENTIONS.md`