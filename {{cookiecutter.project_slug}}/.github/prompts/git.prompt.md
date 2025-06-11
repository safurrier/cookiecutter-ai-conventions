{%- if "git" in cookiecutter.default_domains.split(',') -%}
# Git Conventions Prompt

When working with Git in this project:

## Commit Messages
- Use conventional commit format: `type(scope): description`
- Valid types: feat, fix, docs, style, refactor, test, chore
- Keep the subject line under 50 characters
- Use imperative mood ("Add feature" not "Added feature")

## Branch Strategy
- feature/* - New features
- fix/* - Bug fixes  
- docs/* - Documentation updates
- chore/* - Maintenance tasks

## Pull Requests
- Clear, descriptive titles
- Link related issues with "Closes #123"
- Include a test plan
- List breaking changes if any

## Examples

Good commit messages:
- `feat(auth): add OAuth2 integration`
- `fix(api): handle null response correctly`
- `docs(readme): update installation steps`

Bad commit messages:
- `updated files`
- `fix bug`
- `WIP`
{%- endif -%}