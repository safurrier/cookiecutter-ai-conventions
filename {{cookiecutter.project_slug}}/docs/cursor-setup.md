# Cursor Setup Guide

This guide helps you set up your AI conventions with Cursor IDE.

## Installation

Your conventions are automatically configured for Cursor. The setup includes:
- `.cursorrules` file (legacy format for backwards compatibility)
- `.cursor/rules/` directory with modern MDC files

## How It Works

Cursor uses two systems for custom rules:

### 1. Legacy System (.cursorrules)
- Simple text file in project root
- Automatically loaded by Cursor
- Good for basic conventions

### 2. Modern System (.cursor/rules/)
- MDC (Markdown Cursor) format
- Supports metadata and file patterns
- More powerful and organized

Both are included in your project for maximum compatibility.

## Available Conventions

Your Cursor setup includes:

{%- set domains = cookiecutter.default_domains.split(',') %}
{% for domain in domains %}
{% if domain.strip() == "git" %}
- **Git**: Version control patterns, commit messages
{% elif domain.strip() == "testing" %}
- **Testing**: Test organization, pytest patterns
{% elif domain.strip() == "writing" %}
- **Writing**: Documentation style, technical writing
{% endif %}
{% endfor %}

## File Structure

```
{{ cookiecutter.project_slug }}/
├── .cursorrules              # Legacy format (auto-loaded)
└── .cursor/
    └── rules/
        ├── main.mdc          # Main conventions file
        {%- for domain in domains %}
        ├── {{ domain.strip() }}.mdc         # {{ domain.strip()|title }} domain rules
        {%- endfor %}
        └── ...
```

## MDC File Features

The modern MDC files support:
- **File pattern matching**: Rules apply only to specific file types
- **Metadata**: Description, scope, and behavior settings
- **File references**: Include other files with `@filepath` syntax
- **Always Apply**: Force rules to always be active

## Customization

### Adding New Rules

1. **Quick addition** (legacy):
   ```bash
   echo "Always use type hints in Python" >> .cursorrules
   ```

2. **Structured addition** (modern):
   Create a new MDC file in `.cursor/rules/`:
   ```mdc
   ---
   description: Python Type Hints
   globs: ["**/*.py"]
   ---
   
   # Python Type Hints
   
   Always use type hints for function signatures...
   ```

### Global vs Project Rules

- **Project rules**: Everything in this repository
- **Global rules**: Set in Cursor Settings > General > Rules for AI

{% if cookiecutter.enable_learning_capture %}
## Learning Capture

When you notice patterns:
1. Capture them: `./commands/capture-learning.py`
2. Review periodically: `./commands/review-learnings.py`
3. Update `.cursor/rules/` files with stable patterns
{% endif %}

## Troubleshooting

### Rules not loading?
1. Ensure files are in the correct location
2. Restart Cursor
3. Check Cursor Settings for conflicts

### Too many suggestions?
1. Adjust `alwaysApply` in MDC files
2. Use more specific file globs
3. Move some rules to manual activation

## Best Practices

1. **Keep rules focused**: One concept per MDC file
2. **Use examples**: Show good and bad patterns
3. **Update regularly**: Remove outdated conventions
4. **Test rules**: Verify AI follows your conventions

## Next Steps

1. Open Cursor in your project
2. Try generating code - conventions load automatically
3. Refine rules based on AI behavior
4. Share improvements with your team