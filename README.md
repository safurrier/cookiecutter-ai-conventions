# Stop Repeating Yourself to Your AI Assistant

You know that moment when your AI suggests `import os` at the top of your function... again?

Or formats a commit message like "Updated stuff" when your team uses conventional commits?

What if your AI just... knew your preferences?

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
# Install and generate your conventions (one-time setup)
curl -LsSf https://raw.githubusercontent.com/safurrier/cookiecutter-ai-conventions-experimental/main/bootstrap.sh | sh

# That's it! Your AI now knows:
# ✓ Your import style
# ✓ Your docstring format  
# ✓ Your type hints preferences
# ✓ Your error handling patterns
```

## What Just Happened?

You created a personal conventions system that:
1. **Loads automatically** when you use Claude, Cursor, or other AI tools
2. **Grows with you** - capture new patterns as you discover them
3. **Version controls** your preferences alongside your code

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

This will:
- ✅ Install `uv` if needed (cross-platform)
- ✅ Run the cookiecutter template
- ✅ Guide you through setup
- ✅ Provide next steps

**Provider Selection:** When prompted, enter one or more providers separated by commas:
- Single: `claude`
- Multiple: `claude,cursor,windsurf`
- All: `claude,cursor,windsurf,aider,copilot,codex`

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

## Supported AI Tools

- ✅ **Claude** - Full support via CLAUDE.md
- 🚧 **Cursor** - Coming soon (currently via .cursorrules)
- 🚧 **Windsurf** - Coming soon
- 🚧 **Aider** - Coming soon

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