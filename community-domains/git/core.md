# Git Core - Essential Git Development Guidance

## Commit Standards

### Commit Message Format
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Separate subject from body with a blank line
- Body should wrap at 72 characters

### Commit Message Examples
```
Add user authentication system

Implement JWT-based authentication with refresh tokens.
Includes middleware for protecting routes and user
session management.
```

## Branching Strategy

### Branch Naming
- `feature/` - New features
- `fix/` - Bug fixes
- `chore/` - Maintenance tasks
- `docs/` - Documentation updates

### Branch Workflow
1. Create branch from main
2. Make focused commits
3. Push and create PR
4. Review and merge

## Best Practices

- **Commit Often**: Small, focused commits are better than large ones
- **Write Meaningful Messages**: Future you will thank present you
- **Never Force Push to Main**: Protect shared history
- **Use .gitignore**: Don't commit generated files or secrets
- **Review Before Committing**: Use `git diff` to check changes
