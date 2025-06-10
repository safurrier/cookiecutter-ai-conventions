# Commit Messages - Git Commit Writing Standards

## The Seven Rules

1. **Separate subject from body with a blank line**
2. **Limit the subject line to 50 characters**
3. **Capitalize the subject line**
4. **Do not end the subject line with a period**
5. **Use the imperative mood in the subject line**
6. **Wrap the body at 72 characters**
7. **Use the body to explain what and why vs. how**

## Format

```
<type>: <subject>

<body>

<footer>
```

## Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Formatting, missing semicolons, etc.
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **test**: Adding missing tests
- **chore**: Maintain. Changes to build process, auxiliary tools, libraries

## Examples

### Simple Change
```
fix: Prevent race condition in user signup
```

### Complex Change
```
feat: Add OAuth2 authentication

Implement Google and GitHub OAuth2 providers using Passport.js.
Users can now sign in using their existing accounts instead of
creating new credentials.

Closes #123
```

### Breaking Change
```
refactor!: Change API response format

BREAKING CHANGE: API responses now use snake_case instead of
camelCase for all field names. Clients will need to update
their parsing logic.

Migration guide: docs/migrations/v2-api.md
```

## Tips

- **Think like a historian**: What would you want to know in 6 months?
- **Reference issues**: Use "Fixes #123" to auto-close issues
- **Be specific**: "Fix bug" helps no one
- **Group related changes**: One logical change per commit
