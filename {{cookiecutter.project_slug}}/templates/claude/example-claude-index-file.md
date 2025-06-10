# CLAUDE.md - AI Development Standard Library

This is the main router file for Claude's development context. It implements automatic domain loading based on the current task context.

## 🚨 CRITICAL: Automatic Domain Loading

**When working on ANY task, IMMEDIATELY follow this 3-step process:**

1. **Identify the context** - What kind of task is this? What files/commands are involved?
2. **Load relevant domain cores** - Read the appropriate domain core files based on context
3. **Apply the guidance** - Use the loaded patterns and conventions in your work

### Context → Domain Mapping

**AUTOMATICALLY load these domains when you detect:**

| Context | Load Domain | Trigger Keywords/Actions |
|---------|-------------|-------------------------|
| Python files (.py) | @domains/python/core.md | import, def, class, pytest, uv |
| Git commits | @domains/writing/commit-messages.md | git commit, commit message |
| Pull requests | @domains/writing/pr-summaries.md | gh pr create, PR description |
| Testing | @domains/testing/core.md | test_, pytest, assert, fixture, test patterns, parallel tests, testing approach |
| Documentation | @domains/writing/core.md | README, docs, comments |
| Git operations | @domains/git/core.md | git, branch, merge, rebase |

**Example:** User says "write a commit message" → You MUST first read commit-messages.md, then apply those patterns.

## Core Imports (Always Active)

### Universal Guidelines
@global.md

### Domain Knowledge (Auto-loaded based on context)
@domains/testing/core.md
@domains/python/core.md
@domains/git/core.md
@domains/writing/core.md
@domains/documentation/core.md

### Project Context (Auto-detected: dots repository)
@projects/dots/build.md
@projects/dots/context.md

### Learning System
@staging/learnings.md

## System Architecture

This CLAUDE.md system follows a **progressive context loading** approach:

1. **Global rules** (always active): Universal development principles
2. **Domain cores** (context-aware): Essential knowledge automatically loaded based on task
3. **Project-specific** (auto-detected): Build commands and context for current repo
4. **Learning capture** (continuous): New patterns staged for review and promotion

## Domain-Specific Loading Instructions

### Python Domain
**Auto-load @domains/python/core.md when:**
- Working with .py files
- User mentions Python, pip, uv, pytest
- Creating functions, classes, or modules
- Setting up virtual environments

**Then load specialized files if needed:**
- @domains/python/packaging.md - When dealing with requirements.txt, pyproject.toml, uv.lock
- @domains/python/cli-tools.md - When creating ANY CLI applications or command-line tools

### Git Domain
**Auto-load @domains/git/core.md when:**
- Any git command is used or mentioned
- Working with branches, commits, merges
- User asks about version control

**Then load specialized files if needed:**
- @domains/git/workflows.md - For advanced git patterns and branching strategies

### Writing Domain
**Auto-load specific files based on task:**
- @domains/writing/commit-messages.md - ALWAYS when writing commit messages
- @domains/writing/pr-summaries.md - ALWAYS when creating or editing PRs
- @domains/writing/core.md - When writing documentation or general text

### Testing Domain
**Auto-load @domains/testing/core.md when:**
- Files contain "test_" or "_test"
- User mentions testing, pytest, fixtures
- Writing test cases or assertions
- Discussing test patterns, parallel tests, or testing approaches

**Then load specialized files based on test type:**
- @domains/testing/unit-tests.md - For detailed pytest patterns
- @domains/testing/smoke-tests.md - For high-level validation
- @domains/testing/integration.md - For component testing
- @domains/testing/e2e-tests.md - For end-to-end testing
- @domains/testing/property-tests.md - For hypothesis/property-based testing

### Documentation Domain
**Auto-load @domains/documentation/core.md when:**
- Creating or editing README files
- Writing code comments or docstrings
- Creating technical documentation

## Usage Examples

### Automatic Loading in Action
```
User: "Help me write a commit message for these changes"
Claude: [IMMEDIATELY reads @domains/writing/commit-messages.md]
        [Applies natural language patterns, avoids LLM tells]
        "Add worktree management utilities"

User: "Create a Python CLI tool"
Claude: [IMMEDIATELY reads @domains/python/core.md]
        [THEN reads @domains/python/cli-tools.md]
        [Applies Click patterns and best practices]
```

### Manual Loading
Use these commands when you need specific context:
- `/load-specific domains/testing/unit-tests.md` - Load detailed testing patterns
- `/load-specific domains/python/packaging.md` - Load uv packaging guidance
- `/show-context` - Display currently loaded files

### Learning Capture
When patterns emerge or corrections are needed:
1. Use `/capture-learning` to format insights
2. Add to staging/learnings.md with target domain
3. Review weekly and promote stable patterns

## Available Domains

- **testing/**: Progressive testing approach (E2E → Smoke → Integration → Unit)
- **python/**: uv-based Python development patterns
- **git/**: Commit standards and workflow patterns
- **writing/**: Commit messages, PR summaries, and documentation writing
- **documentation/**: Effective AI context and knowledge capture patterns

## Available Projects

- **dots/**: This dotfiles repository (build commands, context)

## Specialized Documentation

Each domain contains both core principles and specialized guidance:

### Testing Domain
- core.md: Essential testing philosophy and patterns
- unit-tests.md: Pytest patterns and best practices
- smoke-tests.md: High-level system validation
- property-tests.md: Hypothesis-based property testing
- integration.md: Component interaction testing

### Python Domain
- core.md: Essential Python patterns and uv workflow
- packaging.md: uv project management
- cli-tools.md: Click patterns and CLI best practices

### Git Domain
- core.md: Essential git practices and standards
- workflows.md: Advanced git patterns

### Writing Domain
- core.md: Essential writing principles and patterns
- commit-messages.md: Git commit message standards and examples
- pr-summaries.md: Pull request description templates and best practices

## Evolution Process

This system evolves through use:
1. **Capture**: New learnings go to staging/learnings.md
2. **Review**: Weekly review of staged learnings
3. **Promote**: Stable patterns move to appropriate domain files
4. **Archive**: Historical learnings preserved for context

The goal is building a comprehensive, maintainable knowledge base that improves AI assistance quality over time while keeping context manageable.
