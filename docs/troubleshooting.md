# Troubleshooting Guide

## Common Issues and Solutions

### "My AI isn't using my conventions"

This is the most common issue. Let's debug it step by step.

#### 1. Verify Installation

First, check if your conventions are installed:

```bash
# For Claude
ls -la ~/.claude/CLAUDE.md

# Should show your file
# If not, run ./install.py again
```

#### 2. Test with Direct Question

Ask your AI directly:
> "What coding conventions should I follow?"

If it doesn't mention your conventions, they're not loading.

#### 3. Check File Contents

```bash
cat ~/.claude/CLAUDE.md | head -20

# Should show your domains and patterns
# If empty or wrong content, reinstall
```

#### 4. Force Reload

Some AI tools cache contexts:
- **Claude**: Start a new conversation
- **Cursor**: Restart the app
- **Other tools**: Check their documentation for context reloading

#### 5. Explicit Reference

As a test, explicitly mention your conventions:
> "Following my conventions in CLAUDE.md, write a Python function to..."

If this works but implicit doesn't, it's a loading issue.

---

### "Installation fails with permission errors"

```bash
# Error: Permission denied: '/home/user/.claude/CLAUDE.md'
```

**Solution:**
```bash
# Create directory with correct permissions
mkdir -p ~/.claude
chmod 755 ~/.claude

# Then reinstall
./install.py
```

---

### "Domain files not found during installation"

```bash
# Error: Domain 'python' not found
```

**Causes and Solutions:**

1. **Missing community-domains**:
   ```bash
   # Check if directory exists
   ls community-domains/
   
   # If missing, you may need to clone properly
   git clone https://github.com/safurrier/cookiecutter-ai-conventions-experimental
   ```

2. **Wrong directory structure**:
   ```bash
   # Ensure you're in the generated project
   pwd  # Should show: /path/to/my-ai-conventions
   ```

---

### "Learning capture commands not working"

```bash
# Error: ./commands/capture-learning.py: Permission denied
```

**Solution:**
```bash
# Make scripts executable
chmod +x commands/*.py

# Or use Python directly
python commands/capture-learning.py
```

---

### "Conventions work sometimes but not others"

This usually means your AI is getting conflicting context.

**Debug Steps:**

1. **Check for duplicates**:
   ```bash
   # Look for multiple CLAUDE.md files
   find ~ -name "CLAUDE.md" 2>/dev/null
   ```

2. **Simplify your conventions**:
   - Start with just one domain
   - Make sure patterns don't conflict
   - Use clear, unambiguous rules

3. **Test isolated patterns**:
   ```bash
   # Create a minimal test
   echo "Always use 'print' for debugging" > test-convention.md
   # Ask AI to debug something
   # It should use print
   ```

---

### "My team can't use my conventions"

When sharing conventions with your team:

1. **Check Git repository**:
   ```bash
   git remote -v  # Ensure it's pushed
   git status     # Check for uncommitted changes
   ```

2. **Verify they're using correct URL**:
   ```bash
   # They should run:
   uvx cookiecutter gh:yourteam/your-conventions-repo
   # NOT the original template
   ```

3. **Check their installation**:
   ```bash
   # Have them verify:
   ls ~/.claude/CLAUDE.md
   cat ~/.claude/CLAUDE.md | grep "your-domain"
   ```

---

### "Cookiecutter fails with template errors"

```bash
# Error: Unable to find git reference 'main'
```

**Solutions:**

1. **Use the correct branch**:
   ```bash
   # If using a fork
   uvx cookiecutter gh:yourfork/repo --checkout main
   ```

2. **Clone first approach**:
   ```bash
   git clone https://github.com/safurrier/cookiecutter-ai-conventions-experimental
   cd cookiecutter-ai-conventions-experimental
   uvx cookiecutter .
   ```

---

### "My custom domain isn't showing up"

You created a custom domain but it's not in the installer.

**Checklist:**

1. **Directory exists**:
   ```bash
   ls domains/yourcustom/
   # Should show your .md files
   ```

2. **Registry updated** (if needed):
   ```bash
   # Check if your domain needs registry entry
   grep "yourcustom" community-domains/registry.json
   ```

3. **Reinstall after changes**:
   ```bash
   ./install.py
   # Your domain should appear in the list
   ```

---

### "AI suggests outdated patterns"

Your AI keeps suggesting old patterns even after updating conventions.

**Solutions:**

1. **Clear and reinstall**:
   ```bash
   rm ~/.claude/CLAUDE.md
   ./install.py
   ```

2. **Be more explicit**:
   ```markdown
   ## DEPRECATED Patterns
   
   NEVER use these patterns:
   - unittest.TestCase (use pytest instead)
   - print() for debugging (use logger)
   - Inline imports
   ```

3. **Add positive examples**:
   ```markdown
   ALWAYS use these patterns:
   - pytest fixtures for test setup
   - logger.debug() for debugging
   - Top-level imports
   ```

---

### "Bootstrap script fails"

```bash
# Error: curl: command not found
```

**Alternative installation methods:**

1. **Install uv first, then use uvx**:
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Then run the command
   uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions
   ```

2. **Manual installation**:
   ```bash
   # Install uv first
   pip install uv
   # Then use cookiecutter
   uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions-experimental
   ```

3. **Direct Python**:
   ```bash
   pip install cookiecutter
   cookiecutter gh:safurrier/cookiecutter-ai-conventions-experimental
   ```

---

## Still Having Issues?

1. **Check existing issues**: [GitHub Issues](https://github.com/safurrier/cookiecutter-ai-conventions-experimental/issues)

2. **Open a new issue** with:
   - Your OS and Python version
   - Exact error message
   - Steps to reproduce
   - What you've already tried

3. **Community help**: Join our discussions for community support

Remember: Most issues are quick fixes. Don't hesitate to ask for help!