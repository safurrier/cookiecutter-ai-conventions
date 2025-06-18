# CLI Reference

The AI Conventions CLI provides commands for managing convention domains, syncing with AI providers, and capturing learnings.

## Installation

```bash
# Install from your generated project
cd your-project
uv tool install .

# Or install in development mode
uv tool install --editable .
```

## Core Commands

### `ai-conventions status`

Check installation status for all AI providers.

```bash
ai-conventions status
```

**Output:**
```
AI Provider Status:

✅ Claude: Installed at ~/.claude
   - CLAUDE.md: ✅ Present
   - domains/: ✅ Synced (3 domains)
   - Commands: ✅ Available

❌ Cursor: Not configured
   - .cursorrules: ❌ Missing
   - .cursor/: ❌ Not found

🔄 Windsurf: Partially configured
   - .windsurfrules: ✅ Present
   - Conventions: ⚠️  Out of sync
```

### `ai-conventions list`

List all available convention domains and their descriptions.

```bash
ai-conventions list

# Filter by domain type
ai-conventions list --type core
ai-conventions list --type custom
```

**Output:**
```
Available Convention Domains:

Core Domains:
  git          Git workflows and commit standards
  testing      Testing patterns and philosophy  
  writing      Technical writing and documentation

Custom Domains:
  api-design   REST API design principles
  security     Security best practices
```

### `ai-conventions sync`

Sync conventions to configured AI providers.

```bash
# Sync to all providers
ai-conventions sync

# Sync to specific provider
ai-conventions sync --provider claude
ai-conventions sync --provider cursor

# Force sync (overwrite existing)
ai-conventions sync --force

# Dry run (show what would be synced)
ai-conventions sync --dry-run
```

**Options:**
- `--provider`: Target specific provider
- `--force`: Overwrite existing files
- `--dry-run`: Preview changes without applying
- `--verbose`: Show detailed output

## Learning Capture Commands

### `capture-learning`

Capture development learnings and patterns for future use.

```bash
# Basic usage
capture-learning "Always use type hints for public functions"

# With domain and category
capture-learning "Mock external APIs in tests" --domain testing --category pattern

# Interactive mode
capture-learning
```

**Options:**
- `--domain, -d`: Target domain for the learning
- `--file, -f`: Append to specific staging file
- `--category, -c`: Learning category (pattern, fix, anti-pattern, tool-specific, other)

**Categories:**
- **pattern**: Best practices and recommended approaches
- **fix**: Solutions to common problems
- **anti-pattern**: Things to avoid
- **tool-specific**: Tool or framework specific guidance
- **other**: General insights

**Examples:**

```bash
# Capture a coding pattern
capture-learning "Use pathlib instead of os.path for file operations" \
  --domain python --category pattern

# Capture an anti-pattern
capture-learning "Avoid global variables for configuration" \
  --domain global --category anti-pattern

# Capture a fix
capture-learning "Use scope='class' for expensive test fixtures" \
  --domain testing --category fix

# Interactive mode with prompts
capture-learning
# Prompts will guide you through:
# - What pattern or learning did you discover?
# - Which domain does this belong to?
# - Category selection
```

### Learning Management

```bash
# Review captured learnings
ai-conventions review

# Promote learnings to domains
ai-conventions promote --learning-id 123

# Archive old learnings
ai-conventions archive --older-than 30d
```

## Configuration Commands

### `ai-conventions config`

Manage configuration settings.

```bash
# Show current configuration
ai-conventions config show

# Set provider preferences
ai-conventions config set providers.claude.auto_sync true
ai-conventions config set providers.cursor.use_symlinks false

# List available domains
ai-conventions config domains list

# Add custom domain
ai-conventions config domains add my-domain ./domains/my-domain/
```

## Advanced Usage

### Workflow Examples

**Daily Development Workflow:**
```bash
# 1. Check status
ai-conventions status

# 2. Start coding with AI assistant
# (AI automatically loads relevant conventions)

# 3. Capture learnings from AI interactions
capture-learning "User corrected commit message format" \
  --domain git --category fix

# 4. Sync updates to all providers
ai-conventions sync
```

**Convention Maintenance:**
```bash
# Review and organize captured learnings
ai-conventions review

# Update domains based on learnings
ai-conventions promote --interactive

# Sync updated conventions
ai-conventions sync --force
```

### Debug and Troubleshooting

```bash
# Verbose output for debugging
ai-conventions status --verbose
ai-conventions sync --verbose --dry-run

# Check configuration
ai-conventions config validate

# Reset provider configuration
ai-conventions reset --provider claude --confirm
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0    | Success |
| 1    | General error |
| 2    | Configuration error |
| 3    | Provider error |
| 4    | Domain not found |
| 5    | Sync failed |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_CONVENTIONS_HOME` | Base directory for conventions | `~/.ai-conventions` |
| `AI_CONVENTIONS_CONFIG` | Configuration file path | `~/.ai-conventions.yaml` |
| `AI_CONVENTIONS_DEBUG` | Enable debug logging | `false` |

## Configuration File

The configuration file (`.ai-conventions.yaml`) supports:

```yaml
providers:
  claude:
    enabled: true
    auto_sync: true
    use_symlinks: true
  cursor:
    enabled: true
    auto_sync: false
    
domains:
  default: [git, testing, writing]
  custom_paths:
    - ./custom-domains/
    
learning_capture:
  enabled: true
  auto_review: weekly
  archive_after: 90d
```