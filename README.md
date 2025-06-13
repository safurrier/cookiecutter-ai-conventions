# 🤖 AI Conventions: Stop Teaching Your AI The Same Things Over and Over

**Make your AI coding assistant understand your team's conventions in 30 seconds.**

[Quick Start](#make-your-ai-learn-your-style-in-2-minutes) • [Features](#-what-you-get) • [Examples](#real-examples-from-real-developers) • [Supported Tools](#-works-with-your-favorite-ai-tools) • [Migration Guide](docs/MIGRATION.md)

---

You know that moment when your AI suggests `import os` inside your function... again? 😤

Or writes "Updated stuff" when your team uses conventional commits?

Or forgets your API uses camelCase, not snake_case?

**What if your AI just... knew your preferences?**

## See It In Action

```bash
# Before: Your AI doesn't know your style
> "Write a Python function to read environment variables"

def get_env_var(name):
    import os  # ❌ Inline import
    return os.getenv(name, '')  # ❌ Wrong default
```

```bash
# After: Your AI knows your conventions
> "Write a Python function to read environment variables"

import os
from typing import Optional

def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with optional default.
    
    Args:
        name: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.environ.get(name, default)
```

## Make Your AI Learn Your Style in 2 Minutes

```bash
# One simple command to teach your AI your style (30 seconds)
curl -LsSf https://raw.githubusercontent.com/safurrier/cookiecutter-ai-conventions/main/bootstrap.sh | sh

# The bootstrap script simply:
# 1. Installs uv if needed
# 2. Runs cookiecutter to set up your conventions

# That's it! Your AI now knows:
# ✓ Your import style
# ✓ Your docstring format  
# ✓ Your type hints preferences
# ✓ Your error handling patterns
```

## 🎁 What You Get

After 30 seconds of setup, you'll have:

📁 **Your Own Conventions Repository**
```
my-conventions/
├── global.md              # Universal rules
├── domains/               # Organized by context
│   ├── git/              # Commit messages, workflows
│   ├── testing/          # Test patterns, fixtures
│   └── python/           # Language-specific rules
├── templates/            # AI tool configurations
└── install.py            # One-click updates
```

✨ **Features That Just Work**
- 🔄 **Auto-Loading** - Conventions load automatically in your AI tools
- 📝 **Learning Capture** - Save new patterns as you discover them
- 🎯 **Context Aware** - Different rules for different situations
- 👥 **Team Friendly** - Share via git, everyone stays in sync
- 🔧 **Tool Agnostic** - Works with Claude, Cursor, Copilot, and more
- 📈 **Living System** - Evolves with your codebase

## Real Examples from Real Developers

### Example: Consistent Commit Messages

**Problem:** Your team uses conventional commits, but your AI keeps suggesting generic messages.

**Solution:** After setup, your AI automatically knows:
```bash
# Your AI now suggests:
git commit -m "fix: resolve race condition in auth middleware"

# Instead of:
git commit -m "Fixed bug"
```

### Example: Testing Patterns

**Problem:** You use pytest fixtures, but your AI keeps writing unittest classes.

**Solution:** Your testing conventions are loaded automatically:
```python
# Your AI now writes:
def test_user_creation(db_session, test_user):
    """Test that users can be created with valid data."""
    user = User.create(email=test_user.email)
    assert user.id is not None
    
# Instead of:
class TestUser(unittest.TestCase):
    def setUp(self):
        # ...
```

## Capture Your Team's Wisdom

When you correct your AI, capture it for next time:

```bash
./commands/capture-learning.py

📚 Capture Development Learnings
================================
Learning title: Use team's custom logger instead of print()
Context: Debugging production issues
Problem: print() statements don't appear in our log aggregator
Solution: Always use logger.debug() or logger.info() from our custom logger
```

Now your AI will never suggest `print()` for debugging again.

## Start With Community Conventions

Choose from battle-tested conventions:

- **git** - Commit messages, branching strategies, PR descriptions
- **testing** - Pytest patterns, fixture design, test organization  
- **writing** - Documentation style, API docs, code comments
- **python** - Import style, type hints, error handling
- **More coming** - JavaScript, Go, Rust, DevOps...

## Installation

### Quick Start (Recommended)

One command, zero dependencies:

```bash
curl -LsSf https://raw.githubusercontent.com/safurrier/cookiecutter-ai-conventions/main/bootstrap.sh | sh
```

The bootstrap script is simple and straightforward - it just:
- ✅ Installs `uv` if needed (the modern Python package manager)
- ✅ Runs cookiecutter to generate your conventions repository

**Provider Selection:** When prompted, enter one or more providers separated by commas:
- Single: `claude`
- Multiple: `claude,cursor,windsurf`
- All: `claude,cursor,windsurf,aider,copilot,codex`

### Windows Installation

Windows users should use PowerShell:

```powershell
# Install uv first (see https://docs.astral.sh/uv/getting-started/installation/#windows)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Then run cookiecutter
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions
```

For detailed Windows installation options, see the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/#windows).

### Manual Installation

If you prefer to install step by step:

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Run cookiecutter
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions

# 3. Install CLI tools
cd my-ai-conventions
uv tool install .

# 4. Check installation
ai-conventions status
```

## How It Works

```
Your Code Editor → AI Assistant → Your Conventions → Better Suggestions
                                   ↑
                                   You control this
```

1. **Generate** your conventions repository
2. **Install** to `~/.claude/` (or other AI tools)
3. **Use** your AI normally - conventions load automatically
4. **Evolve** by capturing learnings when you spot patterns

## 🎯 Works With Your Favorite AI Tools

<table>
<tr>
<td>✅ <b>Claude</b></td>
<td>Auto-loads via CLAUDE.md, supports commands</td>
</tr>
<tr>
<td>✅ <b>Cursor</b></td>
<td>Legacy .cursorrules + modern MDC format</td>
</tr>
<tr>
<td>✅ <b>Windsurf</b></td>
<td>Character-aware rules with glob patterns</td>
</tr>
<tr>
<td>✅ <b>Aider</b></td>
<td>CONVENTIONS.md + .aider.conf.yml</td>
</tr>
<tr>
<td>✅ <b>GitHub Copilot</b></td>
<td>Instructions + prompt templates</td>
</tr>
<tr>
<td>✅ <b>OpenAI Codex</b></td>
<td>AGENTS.md + custom configuration</td>
</tr>
</table>

Each tool gets optimized configuration for its specific features.

## Next Steps After Installation

1. **Try it out** - Ask your AI to write code and see your conventions in action
2. **Capture patterns** - When you correct your AI, capture it: `./commands/capture-learning.py`
3. **Share with your team** - Push your conventions to git, let everyone benefit

## Contributing

We're building a library of high-quality convention domains. Contributions welcome!

- [Contributing Guide](CONTRIBUTING.md)
- [Create a new domain](docs/creating-domains.md)
- [Improve existing domains](community-domains/)

## License

MIT - Use freely in personal and commercial projects.

---

Built with ❤️ by developers tired of repeating themselves to AI.