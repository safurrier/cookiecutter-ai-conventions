# GitHub Copilot Setup Guide

This guide helps you use your AI conventions with GitHub Copilot in VS Code.

## Installation

Your conventions are automatically configured for GitHub Copilot with:
- `.github/copilot-instructions.md` - Main instructions file (automatically loaded)
- `.vscode/settings.json` - VS Code configuration
- `.github/prompts/*.prompt.md` - Domain-specific prompt files

## How It Works

### Automatic Convention Loading

GitHub Copilot now has official support for project conventions:

1. **Copilot Instructions** (`.github/copilot-instructions.md`)
   - Automatically loaded in every chat
   - Provides context for all code generation
   - Contains your project's coding standards

2. **VS Code Settings** (`.vscode/settings.json`)
   - Enables instruction file support
   - Adds additional generation instructions
   - References convention files

3. **Prompt Files** (`.github/prompts/`)
   - Domain-specific guidance
   - Can be attached to specific requests
   - Organized by convention domain

### File Structure

```
{{ cookiecutter.project_slug }}/
├── .github/
│   ├── copilot-instructions.md    # Main instructions (auto-loaded)
│   └── prompts/                    # Domain-specific prompts
│       {%- set domains = cookiecutter.default_domains.split(',') %}
│       {%- for domain in domains %}
│       ├── {{ domain.strip() }}.prompt.md
{%- endfor %}
│       └── ...
└── .vscode/
    └── settings.json               # VS Code configuration
```

## Features

### Automatic Loading
- Copilot automatically reads `.github/copilot-instructions.md`
- No manual configuration needed
- Works in VS Code, Visual Studio, and GitHub.com

### Model Support
GitHub Copilot now supports multiple models:
- GPT-4o (default)
- Claude 3.5 Sonnet
- Gemini 1.5 Pro

### Context Awareness
Your conventions are included in:
- Code completions
- Chat responses
- Code reviews
- Inline suggestions

## Usage

### Basic Usage

1. **Open VS Code** in your project
2. **Start coding** - Copilot automatically uses your conventions
3. **Chat with Copilot** - Ask questions about your standards

### Verification

Test that your conventions are loaded:

1. Open Copilot Chat (Cmd+I or Ctrl+I)
2. Ask: "What are the coding conventions for this project?"
3. Copilot should list your configured standards

### Using Prompt Files

Attach domain-specific prompts:

```
@workspace What's the testing convention? #file:.github/prompts/testing.prompt.md
```

### Examples

**Code Generation**:
```
Generate a new test for the user authentication function
```
*Copilot will follow your pytest conventions*

**Convention Questions**:
```
How should I format commit messages in this project?
```
*Copilot will reference your git conventions*

## Best Practices

### 1. Keep Instructions Concise
- Short, actionable statements work best
- Focus on "always" and "never" rules
- Include concrete examples

### 2. Update Regularly
- Review instructions quarterly
- Add new patterns as they emerge
- Remove outdated guidelines

### 3. Test Your Setup
Regularly verify Copilot is following conventions:
- Generate sample code
- Check adherence to standards
- Refine instructions as needed

{% if cookiecutter.enable_learning_capture %}
## Learning Capture

When you notice patterns Copilot should follow:

1. Update `.github/copilot-instructions.md`
2. Capture learnings: `./commands/capture-learning.py`
3. Review and update instructions periodically
{% endif %}

## Customization

### Adding New Instructions

Edit `.github/copilot-instructions.md`:
```markdown
## New Convention
- Always validate user input
- Never trust external data
```

### Creating Domain Prompts

Add new prompt files to `.github/prompts/`:
```bash
echo "# API Design Prompt" > .github/prompts/api.prompt.md
```

### VS Code Settings

Modify `.vscode/settings.json` for additional instructions:
```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "Use async/await for all API calls"
    }
  ]
}
```

## Troubleshooting

### Conventions Not Loading?

1. **Check file location**: `.github/copilot-instructions.md`
2. **Verify VS Code setting**: `useInstructionFiles` should be `true`
3. **Restart VS Code**
4. **Check Copilot Chat** - Look for "References" section

### Too Many Suggestions?

1. Make instructions more specific
2. Use "never" for anti-patterns
3. Focus on your team's actual standards

### Model Selection

Choose the right model:
- **GPT-4o**: General purpose, fast
- **Claude 3.5**: Complex reasoning, detailed code
- **Gemini 1.5**: Large context, multi-file

## Advanced Features

### Copilot Extensions

Your conventions work with:
- Pull request summaries
- Code review comments
- Documentation generation
- Test generation

### Multi-File Context

Copilot can now:
- Understand project structure
- Reference multiple files
- Follow cross-file conventions

## Next Steps

1. Open your project in VS Code
2. Verify conventions are loaded (Cmd+I, ask about conventions)
3. Start coding with Copilot
4. Refine instructions based on results

Your conventions are now integrated with GitHub Copilot!