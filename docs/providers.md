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

Full Windsurf support with advanced rule system and glob patterns.

### Installation
When you select Windsurf as a provider, the template automatically creates:
- `.windsurfrules` - Main rules file in project root
- `.windsurf/rules/*.md` - Advanced rule files with glob patterns

### How It Works

#### Root Rules (.windsurfrules)
- Markdown file automatically loaded by Windsurf
- Contains all conventions in one place
- Simple and straightforward

#### Advanced Rules (.windsurf/rules/)
- Multiple markdown files for better organization
- Glob pattern support for file-specific rules
- Character limit aware (6k per file, 12k total)
- Different activation modes

### Features
- ✅ Automatic loading
- ✅ Glob pattern matching
- ✅ Domain-specific rule files
- ✅ Character limit compliance
- ✅ Multiple activation modes
- ✅ Cascade AI integration

### File Structure
```
your-project/
├── .windsurfrules            # Main rules file
└── .windsurf/
    └── rules/
        ├── main.md           # Primary conventions
        ├── git.md            # Git rules with globs
        ├── testing.md        # Testing patterns
        └── writing.md        # Documentation style
```

### Activation Modes
- **Always On**: Rules always active
- **Manual**: Activated by @mentioning
- **Model Decision**: AI decides when to apply
- **Glob**: Applied to matching files

### Best Practices
- Keep individual files under 6,000 characters
- Use glob patterns for targeted rules
- Reference detailed docs instead of duplicating
- Monitor total character count (12k limit)

---

## Aider

Full Aider support with automatic convention loading.

### Installation
When you select Aider as a provider, the template automatically creates:
- `CONVENTIONS.md` - Main conventions file (automatically loaded)
- `.aider.conf.yml` - Configuration with auto-loading setup
- `docs/aider-setup.md` - Complete setup guide

### How It Works

#### Convention Loading
- Aider automatically reads `CONVENTIONS.md` on startup
- Domain files included as read-only context
- No manual loading required

#### Configuration
The `.aider.conf.yml` file sets up:
```yaml
# Auto-loaded files
read: CONVENTIONS.md

# Read-only domain files
read-only:
  - global.md
  - domains/git/core.md
  - domains/testing/core.md
  # ... other selected domains
```

### Features
- ✅ Automatic convention loading
- ✅ Domain-specific context
- ✅ Test command integration
- ✅ Learning capture support
- ✅ Multiple model support
- ✅ Git integration

### File Structure
```
your-project/
├── CONVENTIONS.md       # Main conventions (auto-loaded)
├── .aider.conf.yml     # Aider configuration
├── domains/            # Domain conventions
│   ├── git/core.md
│   ├── testing/core.md
│   └── ...
└── docs/
    └── aider-setup.md  # Setup guide
```

### Best Practices
- Let Aider automatically load conventions
- Use chat mode to ask about standards
- Configure test/lint commands in `.aider.conf.yml`
- Keep CONVENTIONS.md concise and clear

### Usage
```bash
# Just run aider - conventions load automatically
aider

# Work on specific files
aider src/main.py tests/

# Use a specific model
aider --model gpt-4o
```

---

## GitHub Copilot

Full GitHub Copilot support with official convention files.

### Installation
When you select Copilot as a provider, the template automatically creates:
- `.github/copilot-instructions.md` - Main instructions file (automatically loaded)
- `.vscode/settings.json` - VS Code configuration
- `.github/prompts/*.prompt.md` - Domain-specific prompt files
- `docs/copilot-setup.md` - Complete setup guide

### How It Works

#### Convention Loading
- Copilot automatically reads `.github/copilot-instructions.md`
- Instructions included in every chat and code generation
- No manual configuration required

#### VS Code Integration
The `.vscode/settings.json` file enables:
```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "Follow the conventions in .github/copilot-instructions.md"
    }
  ]
}
```

### Features
- ✅ Official convention file support
- ✅ Automatic loading in VS Code
- ✅ Domain-specific prompt files
- ✅ Multi-model support (GPT-4o, Claude 3.5, Gemini)
- ✅ Works on GitHub.com
- ✅ Pull request integration

### File Structure
```
your-project/
├── .github/
│   ├── copilot-instructions.md    # Main instructions
│   └── prompts/                    # Domain prompts
│       ├── git.prompt.md
│       ├── testing.prompt.md
│       └── writing.prompt.md
└── .vscode/
    └── settings.json               # VS Code config
```

### Best Practices
- Keep instructions concise and actionable
- Use "Always" and "Never" for clear rules
- Include concrete examples
- Update based on team feedback

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
| Windsurf | ✅ | ✅ | ❌ | 12K total |
| Aider    | ✅ | ✅ | ❌ | Unlimited |
| Copilot  | ✅ | ✅ | ❌ | Per-chat |

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