# Git Core - Essential Git Practices

This file contains the fundamental git patterns and practices for development work.

## Commit Standards

### Clean Commits
- **Remove all debug artifacts before committing**: No debug files, excessive print statements, temporary scripts, or debug HTML files
- Keep test output minimal and focused
- Clean up exploratory code and commented-out sections
- Verify no development artifacts remain in production code

### Commit Message Format
- Use clear, descriptive commit messages that explain the "why" not just the "what"
- First line should be a concise summary (50 characters or less)
- Use imperative mood: "add feature" not "added feature"
- Include context in the body when helpful

### AI Attribution Rules
- **Never reference Claude, Claude Code, or Anthropic** in commit messages
- **No AI attribution or co-authorship** in commits
- Keep all AI assistance invisible in git history

## Branch Naming

Follow consistent naming conventions:
- Feature branches: `feat/description`
- Bug fixes: `bug/description`
- Improvements: `improve/description`
- Documentation: `docs/description`
- Maintenance: `maint/description`

## Specialized Git Topics

For detailed guidance on specific git workflows, see:
- workflows.md: Advanced git patterns and team collaboration practices

