# 🚀 Getting Started Guide

This guide walks you through setting up AI conventions for your project, from installation to daily use.

## 📋 Prerequisites

- A terminal/command prompt
- Git (for version control)
- That's it! The installer handles everything else

## 🎯 Quick Start (2 minutes)

### 1. Run the Installer

```bash
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions
```

### 2. Answer the Prompts

You'll be asked a few questions:

```
project_name [My AI Conventions]: Team Conventions
author_name [Your Name]: Alice Developer
selected_providers [claude]: claude,cursor
default_domains [git,testing]: git,testing,python
enable_learning_capture [y]: y
```

### 3. Install and Use

```bash
cd team-conventions
python install.py

# That's it! Your AI now knows your conventions
```

## 📖 Detailed Setup

### Step 1: Choose Your Providers

Select which AI tools you use (comma-separated):

- `claude` - Claude.ai desktop app
- `cursor` - Cursor editor
- `windsurf` - Windsurf editor
- `aider` - Aider CLI tool
- `copilot` - GitHub Copilot
- `codex` - OpenAI Codex

Example: `claude,cursor` or just `claude`

### Step 2: Select Convention Domains

Choose starter domains or add your own later:

- `git` - Version control best practices
- `testing` - Test patterns and structure
- `writing` - Documentation standards
- `python` - Python-specific conventions
- Custom domains can be added anytime

### Step 3: Configure Features

- **Learning Capture** - Save new patterns as you discover them
- **Context Canary** - Verify conventions are loaded
- **Domain Composition** - Let domains inherit from each other

## 🔧 Installation Options

### Option 1: Bootstrap Script (Recommended)

The bootstrap script handles everything:
- Installs `uv` package manager if needed
- Runs cookiecutter with the template
- Provides clear next steps

### Option 2: Manual Installation

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run cookiecutter
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions

# Install CLI tools
cd my-conventions
uv tool install .
```

### Option 3: Using Existing Tools

If you have Python and pip:
```bash
pip install cookiecutter
cookiecutter gh:safurrier/cookiecutter-ai-conventions
```

## 📁 Understanding Your Setup

After installation, you'll have:

```
my-conventions/
├── global.md                 # Universal conventions
├── domains/                  # Domain-specific rules
│   ├── git/core.md          # Git conventions
│   └── testing/core.md      # Testing patterns
├── templates/               # AI tool configurations
│   └── claude/CLAUDE.md.j2  # Claude template
├── install.py               # Installation script
└── README.md               # Your documentation
```

### Key Files Explained

**global.md** - Rules that apply everywhere
```markdown
# Global Conventions
- Use descriptive variable names
- Follow team style guide
- Document complex logic
```

**domains/[name]/core.md** - Context-specific rules
```markdown
# Git Conventions

## When This Applies
- Creating commits, branches, PRs
- Keywords: git, commit, branch

## Conventions
- Use conventional commits
- Branch names: feature/description
```

## 🎮 Using Your Conventions

### With Claude

Your conventions load automatically when you:
1. Open Claude desktop app
2. Start a new conversation
3. Ask coding questions

Test it: "Write a Python function to validate email addresses"

### With Cursor

Conventions are loaded from:
- `.cursorrules` (legacy)
- `.cursor/rules/*.md` (modern MDC)

### With Other Tools

Each tool has its own configuration method. Run `ai-conventions status` to see what's installed.

## 📝 Capturing New Patterns

When you spot a pattern worth saving:

### Option 1: CLI Command
```bash
capture-learning

# Follow the prompts to document:
# - What you learned
# - Why it matters
# - How to apply it
```

### Option 2: Manual Addition
1. Edit the appropriate domain file
2. Add your convention
3. Run `python install.py` to update

### Example: Capturing a Testing Pattern

You discover your team prefers pytest fixtures over setup methods:

```bash
capture-learning

Learning: Use pytest fixtures instead of setUp methods
Context: Writing Python tests
Domain: testing
```

This gets added to your conventions and shared with your team.

## 🔄 Keeping Conventions Updated

### For Individuals
```bash
# Update all AI tools with latest conventions
cd my-conventions
python install.py
```

### For Teams
```bash
# Share via git
git add -A
git commit -m "docs: add API error handling conventions"
git push

# Team members pull and reinstall
git pull
python install.py
```

## ⚡ Pro Tips

### 1. Start Small
Don't try to document everything at once. Start with your most repeated corrections.

### 2. Be Specific
Instead of: "Write good commit messages"
Better: "Use conventional commits: feat:, fix:, docs:"

### 3. Include Examples
```markdown
## API Endpoints
- Use REST naming: GET /users, POST /users
- Return consistent errors:
  ```json
  {"error": {"code": "NOT_FOUND", "message": "User not found"}}
  ```
```

### 4. Review Weekly
Set a reminder to review captured learnings and promote good ones to permanent conventions.

### 5. Test Your Conventions
After installing, test with real coding tasks to ensure they're working as expected.

## 🆘 Getting Help

- **Installation Issues**: Check [Troubleshooting](troubleshooting.md)
- **Convention Ideas**: Browse [community domains](https://github.com/safurrier/cookiecutter-ai-conventions/tree/main/community-domains)
- **Feature Requests**: Open an [issue](https://github.com/safurrier/cookiecutter-ai-conventions/issues)

## 🎉 Next Steps

1. ✅ Installation complete
2. 📝 Try your first coding task with AI
3. 🔄 Capture your first learning
4. 👥 Share with your team
5. 🌟 Contribute improvements back

Welcome to consistent AI coding! 🚀