# Example: Migrating from .cursorrules

This example shows how to migrate an existing `.cursorrules` file to the cookiecutter-ai-conventions format.

## Original .cursorrules

```
You are an expert full-stack developer specializing in React and Node.js.

Code Style:
- Use functional components with TypeScript
- Prefer hooks over class components  
- Follow Airbnb ESLint configuration
- Use named exports over default exports
- Keep components small and focused

Testing:
- Write tests for all new components
- Use React Testing Library
- Aim for 80% code coverage
- Test user behavior, not implementation details

Git:
- Use conventional commits (feat, fix, docs, etc.)
- Keep commits atomic and focused
- Write descriptive commit messages

API Development:
- RESTful endpoints with clear naming
- Always validate input data
- Return consistent error responses
- Document all endpoints with OpenAPI

General:
- Write self-documenting code
- Add JSDoc comments for complex functions
- Keep functions under 20 lines
- Prefer composition over inheritance
```

## Migrated Structure

### 1. global.md
```markdown
# Global Development Standards

## Code Quality
- Write self-documenting code with clear variable and function names
- Keep functions concise and focused (under 20 lines)
- Add JSDoc comments for complex functions
- Prefer composition over inheritance in design patterns

## Development Workflow
- Follow test-driven development practices
- Maintain consistent code style across the project
- Document architectural decisions
```

### 2. domains/javascript/core.md
```markdown
# JavaScript/TypeScript Development

## When This Applies
- Working with .js, .jsx, .ts, .tsx files
- Creating React components or Node.js modules
- Keywords: component, function, React, TypeScript, JavaScript

## Conventions

### Language Preferences
- Use TypeScript for all new files
- Prefer functional programming patterns
- Use async/await over callbacks or raw promises

### Module Structure
- Use named exports over default exports
- Keep modules focused on a single responsibility
- Organize imports: external → internal → relative

### Code Style
- Follow Airbnb ESLint configuration
- Use 2 spaces for indentation
- Place opening braces on the same line
```

### 3. domains/react/core.md
```markdown
# React Development

## When This Applies
- Creating or modifying React components
- Working with .jsx or .tsx files
- Keywords: component, useState, useEffect, React

## Conventions

### Component Architecture
- Use functional components with TypeScript
- Prefer hooks over class components
- Keep components small and focused
- Extract complex logic into custom hooks

### Component Organization
- One component per file
- Co-locate tests with components
- Group related components in feature folders

### State Management
- Use local state for component-specific data
- Lift state up when needed by multiple components
- Consider Context API before reaching for external libraries
```

### 4. domains/testing/core.md
```markdown
# Testing Standards

## When This Applies
- Writing test files (*.test.*, *.spec.*)
- Keywords: test, describe, it, expect
- Creating new features or fixing bugs

## Conventions

### Test Structure
- Write tests for all new components and functions
- Use React Testing Library for component tests
- Organize tests with clear describe blocks
- Name tests to describe expected behavior

### Testing Philosophy
- Test user behavior, not implementation details
- Aim for 80% code coverage
- Write integration tests for critical paths
- Keep tests independent and isolated

### Test Organization
- Co-locate test files with source code
- Use *.test.ts or *.spec.ts naming convention
- Group related tests in describe blocks
```

### 5. domains/git/core.md
```markdown
# Git Workflow

## When This Applies
- Creating commits, branches, or pull requests
- Keywords: commit, branch, merge, PR

## Conventions

### Commit Messages
- Use conventional commits format:
  - feat: new feature
  - fix: bug fix
  - docs: documentation changes
  - style: formatting changes
  - refactor: code restructuring
  - test: test additions or modifications
  - chore: maintenance tasks

### Commit Practices
- Keep commits atomic and focused
- Write descriptive commit messages
- Include ticket number when applicable
- Example: "feat(auth): add OAuth2 integration (#123)"

### Branch Strategy
- Create feature branches from main
- Use descriptive branch names
- Delete branches after merging
```

### 6. domains/api/core.md
```markdown
# API Development

## When This Applies
- Creating or modifying API endpoints
- Working with Express, Fastify, or similar
- Keywords: endpoint, route, REST, API

## Conventions

### Endpoint Design
- Follow RESTful naming conventions
- Use nouns for resources, not verbs
- Support standard HTTP methods
- Examples:
  - GET /api/users
  - POST /api/users
  - GET /api/users/:id
  - PUT /api/users/:id
  - DELETE /api/users/:id

### Data Handling
- Always validate input data
- Use middleware for common validations
- Sanitize user inputs
- Return consistent response formats

### Error Handling
- Return consistent error responses
- Include error code and message
- Use appropriate HTTP status codes
- Example error format:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Invalid email format",
      "field": "email"
    }
  }
  ```

### Documentation
- Document all endpoints with OpenAPI/Swagger
- Include request/response examples
- Specify required vs optional parameters
- Document error responses
```

## How to Use This Migration

1. Generate your new project:
   ```bash
   uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions
   ```

2. Select providers (e.g., cursor) and domains (e.g., javascript, react, testing, git, api)

3. Replace the generated domain files with the migrated content above

4. Customize further based on your team's specific needs

5. Test with your AI coding assistant to ensure conventions are being followed

## Tips for Successful Migration

- Start with the most important conventions first
- Test incrementally - don't migrate everything at once
- Get team feedback on the organization
- Iterate based on real usage
- Consider creating custom domains for project-specific conventions