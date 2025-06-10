{% if cookiecutter.enable_learning_capture -%}
# /review-learnings - Review and Promote Learnings

Review staged learnings and provide guidance on promoting stable patterns to domain files.

## Usage

Use this command for periodic review of accumulated learnings:
- Weekly or bi-weekly review recommended
- When staging/learnings.md gets large
- Before major project milestones

## Process

1. **Display all staged learnings** from staging/learnings.md
   - Group by domain
   - Show capture date
   - Highlight patterns that appear multiple times

2. **Analyze for promotion readiness**:
   - Stable patterns (appeared multiple times)
   - Widely applicable (not project-specific)
   - Clear and actionable
   - Improves on existing conventions

3. **Suggest promotion targets**:
   ```
   Ready for promotion:
   
   1. "No inline imports" → global.md
      - Captured 3 times this month
      - Universal pattern
      
   2. "Pytest fixture naming" → domains/testing/core.md
      - Consistent pattern emerged
      - Enhances existing testing guidance
   
   3. "Component file structure" → projects/webapp/patterns.md
      - Project-specific but stable
   ```

4. **Provide promotion commands**:
   ```bash
   # Edit the target file to add the learning
   vim domains/testing/core.md
   
   # Remove from staging after promotion
   vim staging/learnings.md
   
   # Commit the promotion
   git add -A
   git commit -m "Promote testing patterns from staging"
   ```

## Promotion Guidelines

### To domain core.md files:
- Universal principles for that domain
- Patterns that apply broadly
- Essential knowledge

### To domain specific files:
- Advanced or specialized patterns
- Tool-specific guidance
- Optional practices

### To projects/:
- Project-specific patterns
- Team conventions
- Local workarounds

### To archive:
- One-time fixes
- Obsolete patterns
- Historical context

## Example Review Output

```
=== Staged Learnings Review ===

GLOBAL DOMAIN (2 learnings):
- "No inline imports" - Captured 3 times ✓ READY
- "Avoid magic numbers" - Captured once

TESTING DOMAIN (1 learning):  
- "Fixture scoping patterns" - Captured 2 times ✓ READY

PROJECT: webapp (1 learning):
- "API response format" - Project-specific

Suggested promotions:
1. Move "No inline imports" to global.md
2. Move "Fixture scoping patterns" to domains/testing/core.md

Archive after promotion? (y/n)
```

## Tips

- Don't promote too quickly - let patterns prove themselves
- Keep staging/learnings.md clean - archive old learnings
- Update existing sections rather than always adding new ones
- Consider creating new domain files for emerging topics
{%- endif %}