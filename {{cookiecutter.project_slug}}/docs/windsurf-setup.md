# Windsurf Setup Guide

This guide helps you set up your AI conventions with Windsurf IDE.

## Installation

Your conventions are automatically configured for Windsurf with:
- `.windsurfrules` file in the project root
- `.windsurf/rules/` directory with advanced rule files

## How It Works

Windsurf uses a dual-file system for maximum flexibility:

### 1. Root Rules (.windsurfrules)
- Simple markdown file
- Automatically loaded by Windsurf
- Contains all conventions in one place
- Good for quick reference

### 2. Advanced Rules (.windsurf/rules/)
- Multiple markdown files
- Support for glob patterns
- File-specific rule activation
- Better organization for large projects

## File Structure

```
{{ cookiecutter.project_slug }}/
├── .windsurfrules            # Main rules file (auto-loaded)
└── .windsurf/
    └── rules/
        ├── main.md           # Primary conventions
        {%- set domains = cookiecutter.default_domains.split(',') %}
        {%- for domain in domains %}
        ├── {{ domain.strip() }}.md          # {{ domain.strip()|title }} domain rules
        {%- endfor %}
        └── ...
```

## Rule Features

### Glob Patterns
Domain-specific rules use glob patterns for targeted application:
- `[glob: "**/test_*.py"]` - Apply to test files
- `[glob: "**/*.md"]` - Apply to documentation
- `[glob: "src/**/*.js"]` - Apply to JavaScript in src/

### Activation Modes
- **Always On**: Rules always active
- **Manual**: Activated by @mentioning
- **Model Decision**: AI decides when to apply
- **Glob**: Applied to matching files

### Character Limits
- Individual files: 6,000 characters max
- Total rules: 12,000 characters max
- If exceeded, global rules take priority

## Available Conventions

Your Windsurf setup includes:

{%- for domain in domains %}
{% if domain.strip() == "git" %}
- **Git**: Version control patterns, commit messages
  - Glob: `"**/.git*", "**/COMMIT_*"`
{% elif domain.strip() == "testing" %}
- **Testing**: Test organization, pytest patterns
  - Glob: `"**/test_*.py", "**/*_test.py", "**/tests/**"`
{% elif domain.strip() == "writing" %}
- **Writing**: Documentation style, technical writing
  - Glob: `"**/*.md", "**/README*", "**/docs/**"`
{% endif %}
{% endfor %}

## Using Cascade AI

Windsurf's Cascade AI will automatically:
1. Load your conventions based on context
2. Apply file-specific rules using globs
3. Suggest patterns from your domains
4. Respect your project preferences

### Commands
- **Write Mode**: Modifies code following conventions
- **Chat Mode**: Answers questions using convention context

{% if cookiecutter.enable_learning_capture %}
## Learning Capture

When you notice patterns:
1. Capture them: `./commands/capture-learning.py`
2. Review periodically: `./commands/review-learnings.py`
3. Add stable patterns to `.windsurf/rules/`
{% endif %}

## Customization

### Adding New Rules

1. **Quick addition** (root file):
   ```bash
   echo "## New Convention" >> .windsurfrules
   echo "Always validate input data" >> .windsurfrules
   ```

2. **Advanced addition** (rule file):
   Create a new file in `.windsurf/rules/`:
   ```markdown
   # API Conventions
   
   [glob: "**/api/**/*.py"]
   
   ## Response Format
   Always return JSON with status and data fields...
   ```

### Modifying Activation

Edit the header of any rule file:
```markdown
[glob: "**/*.py"]
// Change from always-on to glob-based
```

## Troubleshooting

### Rules not loading?
1. Check file locations are correct
2. Verify character limits aren't exceeded
3. Restart Windsurf
4. Check Windsurf settings for conflicts

### Too many suggestions?
1. Use glob patterns to limit scope
2. Change activation mode to manual
3. Split large rule files

### Character limit issues?
1. Split rules into multiple files
2. Use references instead of duplicating
3. Focus on essential patterns

## Best Practices

1. **Use globs** for file-specific rules
2. **Keep files focused** on one domain
3. **Reference don't repeat** - point to detailed docs
4. **Update regularly** based on team feedback
5. **Monitor limits** - stay under 6k chars per file

## Next Steps

1. Open your project in Windsurf
2. Cascade AI will automatically load rules
3. Test with code generation
4. Refine rules based on results