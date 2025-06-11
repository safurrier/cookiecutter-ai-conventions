# {{ cookiecutter.project_name }}

Welcome to your personal AI conventions system! This README will walk you through using and growing your conventions.

## 🚀 Quick Start

### First Time Setup

You've already generated this repository. Now let's install it:

```bash
./install.py
```

This will:
1. Show available convention domains
2. Let you select which to install
3. Configure your AI tools to use them

### Verify It's Working

Ask your AI assistant:
> "What are my coding conventions?"

It should list the domains you installed.

## 📚 Your Conventions Structure

```
{{ cookiecutter.project_slug }}/
├── domains/           # Your active convention domains
│   ├── git/          # Git workflow patterns
│   ├── python/       # Python coding standards  
│   └── testing/      # Testing approaches
├── global.md         # Universal conventions
├── commands/         # Learning capture tools
└── staging/          # Captured learnings
```

## 🎯 Using Your Conventions

### Day-to-Day Usage

Just use your AI normally! Your conventions load automatically.

**Example**: Ask your AI to write a commit message
- Before: "Updated code"
- After: "fix: resolve race condition in auth middleware"

### When to Update Conventions

Update when you notice:
- Your AI making the same "mistake" repeatedly
- A new team pattern emerging
- A better way of doing something

{% if cookiecutter.enable_learning_capture %}
## 🔄 Capturing New Patterns

Found yourself correcting your AI? Capture it!

### 1. Run the Capture Command

```bash
./commands/capture-learning.py
```

### 2. Fill in the Details

```
Learning title: Use Repository pattern for data access
Context: Refactoring user service
Problem: AI suggested direct database queries in service layer
Solution: Always use repository pattern to separate data access
Domain: python
```

### 3. Review and Promote

After patterns prove stable (usually 1-2 weeks):

```bash
./commands/review-learnings.py

# Shows learnings ready for promotion
# Edit the suggested domain file
# Move the learning from staging/ to domains/
```
{% endif %}

## 🏢 Team Collaboration

### Share Your Conventions

```bash
# First time only
git init
git add -A
git commit -m "feat: initial conventions"
git remote add origin https://github.com/yourteam/conventions
git push -u origin main

# Updates
git add -A
git commit -m "feat: add repository pattern convention"
git push
```

### Team Member Setup

New team members run:
```bash
uvx cookiecutter gh:yourteam/conventions
cd team-conventions
./install.py
```

## 📝 Convention Best Practices

### DO Write Clear Examples

```markdown
## API Response Format

ALWAYS return responses in this format:

\```python
{
    "data": {...},      # The actual response
    "meta": {           # Metadata
        "timestamp": "2024-01-15T10:30:00Z",
        "version": "1.0"
    }
}
\```

NEVER return raw data without wrapper.
```

### DON'T Be Too Prescriptive

```markdown
## Variable Naming

❌ BAD: "All variables must be snake_case with prefix indicating type"
✅ GOOD: "Use descriptive names. Prefer `user_email` over `e` or `email_str`"
```

### DO Explain Why

```markdown
## Import Organization

Group imports in this order: standard library, third-party, local

WHY: Makes dependencies clear and prevents circular imports
```

## 🔧 Maintenance

### Regular Reviews

Monthly:
1. Review staged learnings
2. Promote stable patterns
3. Remove outdated conventions
4. Commit and push changes

### Health Checks

```bash
# See what's installed
cat ~/.claude/CLAUDE.md | grep "##.*Domain"

# Check for conflicts
grep -r "NEVER" domains/ | grep -i "always"

# Find empty sections
find domains -name "*.md" -exec grep -l "TODO" {} \;
```

## 🆘 Troubleshooting

### Conventions Not Loading?

1. Check installation:
   ```bash
   ls ~/.claude/CLAUDE.md
   ```

2. Restart your AI tool

3. Ask explicitly:
   > "Following my CLAUDE.md conventions, write a function..."

### Need Help?

- Check the [documentation](https://github.com/safurrier/cookiecutter-ai-conventions-experimental/tree/main/docs)
- Open an [issue](https://github.com/safurrier/cookiecutter-ai-conventions-experimental/issues)
- Share learnings with the community

## 🎉 You're All Set!

Start coding and watch your AI get smarter about YOUR preferences!

Remember: The best conventions are the ones that evolve with your needs. Capture, review, and refine regularly.

---

Generated with ❤️ by {{ cookiecutter.author_name }}