# {{ cookiecutter.project_name }}

Your personal AI conventions repository, powered by [cookiecutter-ai-conventions](https://github.com/yourusername/cookiecutter-ai-conventions).

## 🚀 Quick Start

1. **Install your conventions**:
   ```bash
   ./install.py
   ```
   This will let you select which convention domains to include (git, testing, writing, etc.)

2. **Start using with Claude** (or other configured AI tools)

3. **Capture learnings** as you work (if enabled)

## 📁 Structure

```
{{ cookiecutter.project_slug }}/
├── domains/        # Your selected convention domains
├── projects/       # Project-specific conventions
├── staging/        # Learning capture area{% if cookiecutter.enable_learning_capture %}
├── commands/       # AI slash commands{% endif %}
├── global.md       # Universal rules
└── install.py      # Installation script
```

## 📚 Managing Domains

### View Installed Domains
```bash
ls domains/
```

### Add More Domains
```bash
./install.py  # Re-run to see all available domains
```

### Create Custom Domains
```bash
mkdir domains/mycompany
echo "# My Company Conventions" > domains/mycompany/core.md
```

Then update your AI tool configuration to include the new domain.

{% if cookiecutter.enable_learning_capture %}
## 📝 Capturing Learnings

When your AI assistant makes a mistake or you notice a pattern:

1. Use `/capture-learning` in Claude (if using Claude)
2. Or manually add to `staging/learnings.md`
3. Periodically review and promote learnings to appropriate domains

Example learning format:
```markdown
## 2024-01-15: No Inline Imports
**Context**: Adding error handling to a function
**Problem**: AI added import inside the function
**Solution**: Always place imports at the top of the file
**Domain**: global
**Promote to**: global.md
```
{% endif %}

## 🔄 Updating

Pull new features and domains from upstream:

```bash
git fetch upstream
git merge upstream/main --allow-unrelated-histories
./install.py  # Check for new domains
```

## 🛠️ Customization

### Adding Project-Specific Conventions

Create a directory for your project:
```bash
mkdir projects/my-project
echo "# My Project Conventions" > projects/my-project/context.md
```

### Modifying Global Rules

Edit `global.md` to add rules that apply everywhere.

## 📖 Available Domains

Run `./install.py` to see all available domains and their descriptions.

## 🤝 Contributing

To contribute new domains back to the community:
1. Create your domain in `domains/`
2. Test it thoroughly
3. Submit a PR to the cookiecutter-ai-conventions repository

---

Generated with ❤️ by {{ cookiecutter.author_name }}
