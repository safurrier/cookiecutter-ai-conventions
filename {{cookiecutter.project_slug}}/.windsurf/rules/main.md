# Main AI Development Conventions

// Project: {{ cookiecutter.project_name }}
// Author: {{ cookiecutter.author_name }}
// This file contains the primary conventions that should always be applied

## Core Principles

1. Follow the conventions in the domains/ directory
2. Apply patterns consistently across the codebase
3. Prioritize readability and maintainability
4. Document decisions and rationale

## Active Domains

{%- set domains = cookiecutter.default_domains.split(',') %}
{%- for domain in domains %}
{%- if domain.strip() == "git" %}
- **Git**: Version control patterns - see domains/git/core.md
{%- elif domain.strip() == "testing" %}
- **Testing**: Test organization and patterns - see domains/testing/core.md
{%- elif domain.strip() == "writing" %}
- **Writing**: Documentation standards - see domains/writing/core.md
{%- endif %}
{%- endfor %}

## Universal Guidelines

Reference global.md for cross-cutting concerns:
- Import organization
- Error handling patterns
- Naming conventions
- Code structure

{%- if cookiecutter.enable_learning_capture %}

## Learning and Evolution

<learning-system>
This project uses a learning capture system:
- Staged learnings: staging/learnings.md
- Capture tool: commands/capture-learning.py
- Review tool: commands/review-learnings.py

When you notice patterns or receive corrections, capture them for future reference.
</learning-system>

{%- endif %}

## File References

The following files contain detailed conventions:
- @global.md - Universal patterns
{%- for domain in domains %}
- @domains/{{ domain.strip() }}/core.md - {{ domain.strip()|title }} conventions
{%- endfor %}
{%- if cookiecutter.enable_learning_capture %}
- @staging/learnings.md - Recently captured patterns
{%- endif %}

## Activation

This rule file is set to:
- **Mode**: Always On
- **Scope**: All files in the project
- **Priority**: High

For file-specific rules, see the individual domain rule files in this directory.