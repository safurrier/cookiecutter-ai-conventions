# 🚀 Migration Guide

Migrating your existing AI coding conventions to the cookiecutter-ai-conventions format is straightforward. This guide walks you through the process step-by-step.

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Migration Process](#migration-process)
- [AI Prompt Template](#ai-prompt-template)
- [Example Migrations](#example-migrations)
- [Manual Migration Steps](#manual-migration-steps)
- [Troubleshooting](#troubleshooting)

## 🎯 Quick Start

If you have existing conventions in any format (text files, markdown, YAML), you can migrate them in 3 steps:

1. **Gather** all your existing convention files
2. **Use** our AI prompt template to transform them
3. **Generate** your new conventions repository

```bash
# Generate your new conventions repo
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions

# Follow the prompts to select providers and domains
# Then add your migrated conventions to the generated files
```

## 🔄 Migration Process

### Step 1: Audit Your Current Conventions

First, locate all your existing conventions:

- `.cursorrules` files
- `CONVENTIONS.md` or `CONVENTIONS.txt`
- `.github/copilot-instructions.md`
- Any team wikis or documentation
- Coding standards documents
- PR templates with guidelines

### Step 2: Identify Domains

Group your conventions by domain:

- **Git**: Commit messages, branching, PR descriptions
- **Testing**: Test structure, naming, coverage requirements
- **Code Style**: Formatting, naming conventions, patterns
- **Documentation**: Comments, README structure, API docs
- **Architecture**: File organization, design patterns

### Step 3: Transform Using AI

Use the prompt template below with your preferred AI assistant.

## 🤖 AI Prompt Template

Copy and use this template with Claude, GPT-4, or another AI:

```markdown
I need help migrating my existing AI coding conventions to the cookiecutter-ai-conventions format.

## My Current Conventions
[Paste your existing conventions here - can be multiple files]

## Migration Request
Please analyze my conventions and:

1. **Identify Domains**: Group conventions into domains (git, testing, code style, documentation, etc.)

2. **Extract Triggering Contexts**: For each domain, identify when the conventions should apply:
   - Keywords that trigger the domain
   - File types or patterns
   - Specific actions (commits, PRs, tests)

3. **Format Conventions**: Structure them using this template:

```
# Domain: [Name]

## When This Applies
- Trigger: [context/keywords/actions]
- File patterns: [if applicable]

## Conventions
### [Category]
- [Specific convention]
- [Another convention]

### [Another Category]
- [Specific convention]
```

4. **Suggest File Structure**: 
   - Which conventions go in global.md
   - Which need separate domain files
   - Which are provider-specific

Please maintain my team's specific rules while improving clarity and organization.
```

## 📚 Example Migrations

### Example 1: Simple Text File → Structured Format

**Input** (CONVENTIONS.txt):
```
Always use async/await instead of promises
Use TypeScript for all new files  
Commit messages should follow conventional commits
Write tests for all new features
Use 2 spaces for indentation
```

**Output** (Migrated Structure):

`global.md`:
```markdown
# Global Conventions

## Code Quality Standards
- Write tests for all new features
- Maintain consistent code style across the project
```

`domains/git/core.md`:
```markdown
# Git Conventions

## When This Applies
- Any git operation
- Creating commits, branches, or PRs

## Conventions
### Commit Messages
- Follow conventional commits format
- Examples: feat:, fix:, docs:, chore:
```

`domains/javascript/core.md`:
```markdown
# JavaScript/TypeScript Conventions

## When This Applies
- Writing JavaScript or TypeScript code
- File extensions: .js, .ts, .jsx, .tsx

## Conventions
### Language Features
- Use async/await over Promise chains
- Prefer const over let/var

### File Standards
- All new files must be TypeScript
- Use 2 spaces for indentation
```

### Example 2: .cursorrules → Multi-Domain Format

**Input** (.cursorrules):
```
You are an expert React developer.
Always use functional components with hooks.
Follow the Airbnb style guide.
Write comprehensive tests using Jest and React Testing Library.
Use semantic commit messages.
Prefer composition over inheritance.
```

**Output** (Migrated Structure):

`domains/react/core.md`:
```markdown
# React Development

## When This Applies
- Creating React components
- Working with .jsx/.tsx files
- Keywords: component, React, hooks, useState

## Conventions
### Component Architecture
- Always use functional components with hooks
- Prefer composition over inheritance
- Follow Airbnb React style guide

### Testing Requirements
- Write comprehensive tests using Jest
- Use React Testing Library for component tests
- Test user interactions, not implementation
```

### Example 3: Multiple Files → Unified System

**Input** (Multiple sources):
- Team wiki with coding standards
- PR template with review checklist  
- Architecture decision records

**Output**: Organized into domains like architecture/, testing/, review/, etc.

## 🛠 Manual Migration Steps

If you prefer to migrate manually:

### 1. Create Domain Structure
```bash
# In your generated project
mkdir -p domains/{custom-domain}
```

### 2. Create Domain Files
```bash
# Create a new domain file
cat > domains/api/core.md << 'EOF'
# API Development

## When This Applies
- Creating or modifying API endpoints
- Working with REST or GraphQL

## Conventions
### Endpoint Design
- Use RESTful naming conventions
- Version APIs with /v1, /v2 prefixes

### Response Format
- Always return consistent error structures
- Include request ID in responses
EOF
```

### 3. Update Provider Templates

For provider-specific conventions, edit the templates:

```bash
# For Claude
edit templates/claude/CLAUDE.md.j2

# For Cursor  
edit templates/cursor/cursorrules.j2
```

### 4. Test Your Migration

```bash
# Reinstall to test
python install.py

# Or use the TUI
python install.py --tui
```

## ❓ Troubleshooting

### Common Issues

**Q: My conventions are too large for one file**  
A: Split them into multiple domain files. Each domain can have multiple files:
- `domains/testing/unit.md`
- `domains/testing/integration.md`
- `domains/testing/e2e.md`

**Q: I have provider-specific conventions**  
A: Add them to the provider templates:
- Claude: `templates/claude/CLAUDE.md.j2`
- Cursor: `templates/cursor/cursorrules.j2`
- Aider: `templates/aider/CONVENTIONS.md.j2`

**Q: Some conventions don't fit any domain**  
A: Add them to `global.md` or create a custom domain

**Q: How do I handle language-specific conventions?**  
A: Create language domains:
- `domains/python/core.md`
- `domains/javascript/core.md`
- `domains/rust/core.md`

### Getting Help

If you run into issues:

1. Check existing domains in `community-domains/` for examples
2. Use the AI prompt template for complex migrations
3. Open an issue with your specific use case

## 🎉 Next Steps

After migration:

1. **Test** your conventions with your AI tools
2. **Iterate** based on what works best
3. **Share** improvements back to the community
4. **Keep** conventions updated as your project evolves

Remember: The goal is consistency and clarity, not perfection. Start simple and evolve your conventions over time.