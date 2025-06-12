# ❓ Frequently Asked Questions

Quick answers to common questions about AI Conventions.

## General Questions

### What is this project?

AI Conventions is a cookiecutter template that helps you create and maintain consistent coding conventions across all your AI tools (Claude, Cursor, Copilot, etc.). Instead of repeatedly telling your AI the same preferences, you define them once and they load automatically.

### How is this different from just using .cursorrules?

While `.cursorrules` works for Cursor, this system:
- Works across multiple AI tools (Claude, Cursor, Windsurf, Aider, Copilot, Codex)
- Organizes conventions by domain (git, testing, APIs, etc.)
- Supports learning capture to evolve over time
- Enables team sharing via git
- Provides tool-specific optimizations

### Do I need to know Python?

No! While the system uses Python for installation, you don't need to know Python to use it. The conventions themselves are written in plain Markdown.

### Is this free?

Yes! This is an open-source project (MIT licensed). Use it freely for personal or commercial projects.

## Installation Questions

### Which providers should I select?

Select only the AI tools you actually use:
- `claude` - If you use Claude.ai desktop app
- `cursor` - If you use Cursor editor
- `windsurf` - If you use Windsurf editor
- `aider` - If you use the Aider CLI tool
- `copilot` - If you use GitHub Copilot
- `codex` - If you use OpenAI Codex

You can always add more later.

### What domains should I choose?

Start with the basics:
- `git` - Version control conventions (recommended for everyone)
- `testing` - If you write tests
- Your primary language (`python`, `javascript`, etc.)

You can add custom domains anytime.

### Can I use this with my existing conventions?

Yes! See the [Migration Guide](MIGRATION.md) for converting existing conventions to this format.

### Where are conventions installed?

Depends on the provider:
- Claude: `~/.claude/CLAUDE.md`
- Cursor: Project root `.cursorrules` and `.cursor/rules/`
- Windsurf: Project root `.windsurfrules` and `.windsurf/rules/`
- Aider: Project root `CONVENTIONS.md`
- Copilot: `.github/copilot-instructions.md`
- Codex: Project root `AGENTS.md`

## Usage Questions

### How do I know if my conventions are working?

Test with a simple prompt:
1. Ask your AI to write a function
2. Check if it follows your conventions (imports, naming, etc.)
3. If using canary feature, type "canary" to verify loading

### Can I use different conventions for different projects?

Yes! Each project can have its own conventions repository. Just:
1. Generate separate convention repos for each project
2. Install them to project-specific locations
3. Your AI will use the appropriate conventions based on context

### How do I update my conventions?

For personal use:
```bash
# Edit your domain files
cd my-conventions
# Reinstall
python install.py
```

For teams:
```bash
# Edit, commit, push
git add -A
git commit -m "Update API conventions"
git push

# Team members pull and reinstall
git pull
python install.py
```

### What if my AI ignores certain conventions?

Some tips:
1. Be specific and actionable (not "write good code" but "use descriptive variable names like user_email not ue")
2. Use consistent formatting across all conventions
3. Avoid contradictions between domains
4. Test with explicit prompts first

## Features Questions

### What is learning capture?

Learning capture lets you save new patterns as you discover them. When you correct your AI or find a better pattern, capture it:
```bash
capture-learning
# Follow prompts to document the learning
```

These get staged for review and can be promoted to permanent conventions.

### What is the context canary?

The context canary is a way to verify your conventions are loaded. When enabled, you can type "canary" or "check conventions" and your AI will respond with a timestamp, confirming conventions are active.

### What is domain composition?

Domain composition lets one domain inherit from another. For example:
- `pytest` domain extends `testing` domain
- `fastapi` domain extends `api` domain

This prevents duplication and keeps conventions DRY.

### Can I create custom domains?

Absolutely! Just:
1. Create a new directory in `domains/`
2. Add your `core.md` file with conventions
3. Reinstall with `python install.py`

## Team Questions

### How do we share conventions?

1. Create a git repository for your conventions
2. Team members clone and install
3. Updates are shared via git pull/push
4. Everyone stays in sync

### Can different team members use different AI tools?

Yes! During setup, each person selects their preferred providers. The core conventions remain the same, but each tool gets its optimized format.

### How do we handle conflicting preferences?

1. Discuss and agree on team standards
2. Document the decision in conventions
3. Use domain composition for language/framework-specific variations
4. Allow personal overrides for non-critical preferences

## Troubleshooting Questions

### Why aren't my conventions loading?

See the [Troubleshooting Guide](troubleshooting.md) for detailed steps. Quick checks:
1. Verify installation location
2. Restart your AI tool
3. Check file permissions
4. Test with explicit mention

### Can I uninstall this?

Yes, simply delete the installed files:
```bash
# Remove Claude conventions
rm ~/.claude/CLAUDE.md

# Remove project files
rm -rf my-conventions
```

### Will this slow down my AI?

No. Conventions are loaded once at the start of a session. The impact is minimal (typically <100ms) and happens only on initialization.

### Does this work with AI API calls?

This system is designed for interactive AI tools. For API usage, you'd need to manually include conventions in your prompts or system messages.

## Contributing Questions

### How can I contribute?

We welcome contributions! You can:
1. Improve existing domains
2. Add new domains
3. Fix bugs
4. Improve documentation
5. Share your conventions as examples

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

### I found a bug, what should I do?

1. Check if it's already reported in [Issues](https://github.com/safurrier/cookiecutter-ai-conventions/issues)
2. If not, create a new issue with:
   - Description of the bug
   - Steps to reproduce
   - Your environment (OS, Python version)
   - Error messages

### Can I create a provider for a new AI tool?

Yes! To add support for a new AI tool:
1. Study existing providers in `ai_conventions/providers/`
2. Create a new provider class
3. Add templates for the tool's format
4. Submit a PR with tests

## Still Have Questions?

- 📧 Open an [issue](https://github.com/safurrier/cookiecutter-ai-conventions/issues)
- 💬 Join the [discussions](https://github.com/safurrier/cookiecutter-ai-conventions/discussions)
- 📚 Read the [full documentation](../README.md)

Remember: There are no stupid questions. If you're wondering about something, others probably are too!