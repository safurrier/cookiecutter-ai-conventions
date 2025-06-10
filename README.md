# cookiecutter-ai-conventions

> 🌱 A framework for growing your own AI coding conventions

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/uv-latest-green.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Build and maintain your own self-improving AI conventions system. Start with community domains like git, testing, and writing - then grow your own conventions that adapt to your style over time.

## ✨ Features

- 🚀 **Zero-install setup** - One command, no dependencies required
- 📦 **Modular domains** - Pick only the conventions you need
- 🔄 **Self-improving** - Capture learnings as you code
- 🎯 **Tool agnostic** - Works with Claude (more tools coming)
- 📝 **Version controlled** - Your conventions evolve with your codebase

## 🚀 Quick Start

```bash
# One-liner setup (installs uv if needed)
curl -LsSf https://raw.githubusercontent.com/yourusername/cookiecutter-ai-conventions/main/bootstrap.sh | sh

# Or if you have uv installed
uvx cookiecutter gh:yourusername/cookiecutter-ai-conventions
```

Then:
```bash
cd my-ai-conventions
./install.py  # Select your domains
```

## 🎯 What's This For?

Ever notice how you correct your AI assistant with the same preferences repeatedly? 

- "Don't use inline imports"
- "Follow our commit message format"  
- "Use our testing patterns"

This tool lets you capture these preferences once and have them automatically loaded every time you code.

## 📚 How It Works

1. **Generate your conventions repo** - A personal, version-controlled set of conventions
2. **Choose domains** - Start with git, testing, writing (or create your own!)
3. **Install to your AI tools** - Currently Claude, more coming soon
4. **Capture learnings** - When you correct your AI, capture it for next time
5. **Evolve over time** - Your conventions improve as you use them

## 🏗️ Architecture

```
your-ai-conventions/
├── stdlib/
│   ├── domains/        # Your selected convention domains
│   ├── projects/       # Project-specific conventions
│   ├── staging/        # Learning capture area
│   └── global.md       # Universal rules
└── install.py          # Domain selector & installer
```

## 📦 Available Domains

### Bundled with Template
- **git** - Version control workflows and standards
- **testing** - Testing philosophy and patterns
- **writing** - Documentation and commit messages

### Coming Soon
- **python** - Python patterns and idioms
- **javascript** - JS/TS conventions
- **rust** - Rust best practices
- ...and more!

## 🤝 Contributing

We'd love your help! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to create new domains
- Submitting improvements
- Reporting issues

## 📄 License

MIT - See [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Inspired by the original CLAUDE.md automatic loading system. Built with [cookiecutter](https://github.com/cookiecutter/cookiecutter) and [Textual](https://github.com/Textualize/textual).
