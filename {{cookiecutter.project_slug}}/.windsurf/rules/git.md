# Git Conventions

[glob: "**/.git*", "**/COMMIT_*"]
// Apply these rules to git-related files and commit messages

## Commit Message Format

Use conventional commits format:
```
type(scope): subject

body

footer
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc)
- **refactor**: Code refactoring
- **test**: Test additions or modifications
- **chore**: Build process or auxiliary tool changes

### Examples

Good:
```
feat(auth): add OAuth2 Google provider

- Implement GoogleOAuth class
- Add refresh token logic
- Update user model

Closes #123
```

Bad:
```
fixed stuff
```

## Branch Naming

- feature/* - New features
- fix/* - Bug fixes
- docs/* - Documentation updates
- refactor/* - Code refactoring

## Pull Requests

1. Clear, descriptive title
2. Link related issues
3. Include test plan
4. List breaking changes

## File References

For complete git conventions:
- @domains/git/core.md

## Activation

- **Mode**: Glob-based
- **Files**: Git configuration and commit messages
- **Priority**: High when working with version control