# Writing Conventions

[glob: "**/*.md", "**/README*", "**/docs/**", "**/CHANGELOG*", "**/*.rst"]
// Apply these rules to documentation files

## Documentation Principles

1. **Start with the problem** - Why does this exist?
2. **Show, then explain** - Examples before theory
3. **Progressive disclosure** - Simple first, complex later
4. **Active voice** - "Configure the server" not "The server is configured"

## Structure

### README Files
```markdown
# Project Name

One-line description of what this does.

## Problem

What problem does this solve?

## Quick Start

```bash
# Immediate value - get running fast
```

## Details

Progressive complexity...
```

### Code Comments
- Explain **why**, not what
- Document edge cases
- Keep synchronized with code
- Use docstrings for public APIs

## Technical Writing

### Good Example
```markdown
## Handling Authentication Errors

When your API key expires, you'll see:
```
Error 401: Unauthorized
```

Fix this by regenerating your key...
```

### Bad Example
```markdown
## Authentication

This section covers authentication.
```

## Commit Messages

Follow conventional commits - see git.md

## File References

For complete writing conventions:
- @domains/writing/core.md
- @domains/writing/commit-messages.md
- @domains/writing/pr-summaries.md

## Activation

- **Mode**: Glob-based
- **Files**: Documentation and markdown files
- **Priority**: High when writing documentation