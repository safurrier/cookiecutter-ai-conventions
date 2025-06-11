# OpenAI Codex Setup Guide

This guide helps you use your AI conventions with the OpenAI Codex CLI tool.

## Installation

Your conventions are automatically configured for Codex with:
- `AGENTS.md` - AI agent instructions (automatically loaded)
- `.codex/config.json` - Codex configuration
- `codex.sh` - Wrapper script for easy usage

## Prerequisites

1. **Install Node.js** (if not already installed):
   ```bash
   # macOS
   brew install node
   
   # Ubuntu/Debian
   sudo apt install nodejs npm
   ```

2. **Install Codex CLI**:
   ```bash
   npm install -g @openai/codex
   ```

3. **Set OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## How It Works

### Convention Loading

Codex uses AGENTS.md files to understand your project:

1. **Repository AGENTS.md** (./AGENTS.md)
   - Loaded automatically when you run `codex`
   - Contains all your project conventions
   - Tells the AI how to work with your code

2. **Global AGENTS.md** (~/.codex/AGENTS.md)
   - Optional global conventions
   - Applies to all projects

3. **Directory AGENTS.md** (any subdirectory)
   - Directory-specific conventions
   - Overrides for specific parts of your project

### File Structure

```
{{ cookiecutter.project_slug }}/
├── AGENTS.md           # Main AI agent instructions
├── .codex/            # Codex configuration
│   └── config.json    # Project settings
├── codex.sh           # Wrapper script
└── domains/           # Convention definitions
    {%- set domains = cookiecutter.default_domains.split(',') %}
    {%- for domain in domains %}
    ├── {{ domain.strip() }}/
    {%- endfor %}
    └── ...
```

## Usage

### Quick Start

1. **Navigate to your project**:
   ```bash
   cd {{ cookiecutter.project_slug }}
   ```

2. **Run Codex using the wrapper**:
   ```bash
   ./codex.sh
   ```

3. **Start coding with AI**:
   ```
   > Create a new function to validate user email addresses
   ```

### Direct Usage

You can also run Codex directly:
```bash
codex
```

The AGENTS.md file will be automatically loaded from your project root.

### Common Commands

**Feature Development**:
```
> Create a new feature for user authentication with tests
```
*Codex will follow your testing conventions*

**Bug Fixing**:
```
> Fix the bug in the data processing function
```
*Codex will create a test first, then fix*

**Refactoring**:
```
> Refactor the API client to use async/await
```
*Codex will ensure tests pass before and after*

**Documentation**:
```
> Add comprehensive docstrings to all public functions
```
*Codex will follow your documentation standards*

## Configuration

### Approval Modes

Edit `.codex/config.json` to change approval mode:
- **"Suggest"** (default) - Review each change
- **"Auto Edit"** - Auto-apply safe changes
- **"Full Auto"** - Apply all changes automatically

### Model Selection

Codex supports multiple models:
```bash
# Use a specific model
codex --model gpt-4

# List available models
codex --list-models
```

## Features

### Git Integration
- Codex understands your git repository
- Follows your commit conventions
- Can create branches and commits

### Test-First Development
{%- if "testing" in cookiecutter.default_domains.split(',') %}
- Enabled: Codex will write tests before implementation
- Uses pytest following your conventions
{%- else %}
- Disabled: Enable by adding "testing" domain
{%- endif %}

### Multi-File Editing
- Codex can work across multiple files
- Understands project structure
- Maintains consistency

{%- if cookiecutter.enable_learning_capture %}

## Learning Capture

When Codex suggests new patterns:
1. Review the suggestion
2. If it's a good pattern, capture it:
   ```bash
   ./commands/capture-learning.py
   ```
3. Review captured patterns periodically
{%- endif %}

## Best Practices

### 1. Clear Instructions
- Be specific about what you want
- Reference file names when relevant
- Mention test requirements explicitly

### 2. Incremental Changes
- Make small, focused changes
- Review each change carefully
- Run tests frequently

### 3. Convention Awareness
- Codex reads AGENTS.md on every start
- Update AGENTS.md as conventions evolve
- Be consistent with instructions

## Troubleshooting

### Codex not following conventions?
1. Check AGENTS.md exists and is readable
2. Verify you're in the project directory
3. Try restarting Codex

### API Key issues?
```bash
# Check if key is set
echo $OPENAI_API_KEY

# Set key in your shell profile
echo "export OPENAI_API_KEY='your-key'" >> ~/.bashrc
```

### Installation problems?
```bash
# Check Node.js version
node --version  # Should be 14+

# Reinstall Codex
npm uninstall -g @openai/codex
npm install -g @openai/codex
```

## Advanced Usage

### Custom Agents

Create specialized agents for different tasks:

1. **Create domain-specific AGENTS.md**:
   ```bash
   echo "# API Development Agent" > api/AGENTS.md
   ```

2. **Add specialized instructions**:
   ```markdown
   When working in the api/ directory:
   - Always validate request data
   - Return consistent error responses
   - Include OpenAPI documentation
   ```

### Integration with CI/CD

Use Codex in your pipeline:
```yaml
# .github/workflows/codex-check.yml
- name: Run Codex checks
  run: |
    codex --check "Verify all functions have tests"
```

## Next Steps

1. Install Codex: `npm install -g @openai/codex`
2. Set your API key
3. Run `./codex.sh` to start
4. Try: "Show me the project conventions"

Your AI assistant is now aware of all your project standards!