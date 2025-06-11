# Provider-Specific Setup

Each AI tool has its own way of loading conventions. Here's how to set up each one.

## Claude (Desktop & API)

Claude has the best support through the CLAUDE.md system.

### Installation
```bash
./install.py
# Automatically installs to ~/.claude/CLAUDE.md
```

### How It Works
- Claude automatically loads `~/.claude/CLAUDE.md` 
- Full context is available in every conversation
- No manual loading required

### Best Practices
- Keep CLAUDE.md under 8,000 tokens for best performance
- Use clear section headers for easy navigation
- Update through your conventions repo, not directly

### Verification
Ask Claude:
> "What conventions am I following?"

Claude should list your installed domains.

---

## Cursor

Full Cursor support with both legacy and modern MDC format.

### Installation
When you select Cursor as a provider, the template automatically creates:
- `.cursorrules` - Legacy format for backwards compatibility
- `.cursor/rules/*.mdc` - Modern MDC files with advanced features

### How It Works

#### Legacy Format (.cursorrules)
- Plain text file in project root
- Automatically loaded by Cursor
- Contains all your conventions in one file

#### Modern Format (.cursor/rules/)
- MDC (Markdown Cursor) files
- Supports metadata and file pattern matching
- Better organization with domain-specific files

### Features
- ✅ Automatic loading
- ✅ File pattern matching (MDC format)
- ✅ Domain-specific rules
- ✅ Works with existing projects
- ✅ Learning capture integration

### File Structure
```
your-project/
├── .cursorrules              # Legacy format
└── .cursor/
    └── rules/
        ├── main.mdc          # Main conventions
        ├── git.mdc           # Git-specific rules
        ├── testing.mdc       # Testing patterns
        └── writing.mdc       # Documentation style
```

### Best Practices
- Use MDC format for new rules (more powerful)
- Keep individual MDC files focused
- Use file globs to target specific file types
- Set `alwaysApply: false` for domain-specific rules

---

## Windsurf

Windsurf integration is in development.

### Planned Features
- Global cascade files
- Project-specific overrides  
- Automatic convention loading

### Current Workaround
1. Create `windsurf.cascade`:
   ```bash
   echo "# Windsurf Conventions" > windsurf.cascade
   cat domains/*/core.md >> windsurf.cascade
   ```

2. Import manually in Windsurf settings

---

## Aider

Aider support through `.aider.conf.yml` is coming.

### Planned Integration
```yaml
# .aider.conf.yml
conventions:
  source: ~/.ai-conventions/
  domains:
    - python
    - git
    - testing
```

### Current Workaround
Use Aider's `--read` flag:
```bash
aider --read ~/.claude/CLAUDE.md
```

---

## VS Code Copilot

While not directly supported, you can improve Copilot suggestions:

### Setup
1. Create workspace settings:
   ```json
   {
     "github.copilot.advanced": {
       "promptFiles": [
         "domains/python/core.md",
         "domains/git/core.md"
       ]
     }
   }
   ```

2. Include conventions as comments:
   ```python
   # Conventions: Always use type hints
   # Conventions: Prefer explicit imports
   ```

### Limitations
- No automatic loading
- Limited context understanding
- Best for simple patterns

---

## JetBrains AI Assistant

JetBrains IDEs (PyCharm, IntelliJ, etc.) have their own AI assistant.

### Setup
1. Create custom prompts in settings
2. Reference your conventions in prompts
3. Use live templates for common patterns

### Example Custom Prompt
```
When generating Python code, follow these conventions:
- Imports at top, grouped by type
- Type hints for all functions
- Docstrings in Google style
```

---

## Custom Integration

Want to integrate with a tool not listed here?

### Basic Integration Pattern

1. **Find the config location**:
   ```bash
   # Usually in:
   ~/.config/[tool]/
   ~/.[tool]/
   ```

2. **Export your conventions**:
   ```bash
   # Create a single file
   cat domains/*/core.md > conventions.md
   ```

3. **Add to tool's context**:
   - Look for: prompts, rules, templates, or context settings
   - Add your conventions file
   - Test with simple prompts

### Creating a Provider Integration

If you want to contribute a provider integration:

1. Research the tool's extension API
2. Create a loading mechanism
3. Test with multiple domains
4. Submit a PR with:
   - Integration code
   - Documentation
   - Installation script

---

## Provider Comparison

| Provider | Global Support | Auto-Load | Hot Reload | Context Size |
|----------|---------------|-----------|------------|--------------|
| Claude   | ✅ | ✅ | ✅ | 8K tokens |
| Cursor   | ✅ | ✅ | ❌ | Per-file |
| Windsurf | 🚧 | 🚧 | 🚧 | Unknown |
| Aider    | 🚧 | ❌ | ❌ | Unlimited |
| Copilot  | ❌ | ❌ | ❌ | Limited |

---

## Testing Your Provider Setup

Regardless of provider, test with these prompts:

1. **Basic Test**:
   > "Write a hello world function"
   
   Should follow your language conventions.

2. **Convention Test**:
   > "What are my coding conventions?"
   
   Should list your domains.

3. **Specific Pattern Test**:
   > "Write a test for user creation"
   
   Should follow your testing patterns.

If any test fails, check the provider-specific troubleshooting above.