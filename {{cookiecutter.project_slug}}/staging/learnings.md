{% if cookiecutter.enable_learning_capture -%}
# Staged Learnings

This file captures new patterns, corrections, and insights as they emerge during development. Items here are reviewed periodically and promoted to appropriate domain files.

## Format for New Learnings

```markdown
## [DATE]: [Brief Title]
**Context**: What were you trying to do?
**Problem**: What went wrong or could be better?
**Solution**: What worked?
**Domain**: testing|python|git|global|[project-name]
**Promote to**: core.md OR specific/[topic].md
```

## Current Learnings

<!-- New learnings will be added here as they occur -->

---

*With symlink mode: This file is automatically synced between your conventions repository and AI tools for real-time learning capture.*
{%- endif %}