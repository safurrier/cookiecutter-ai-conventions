# AI Convention Migration Prompt

Copy and paste this template into your AI assistant to help migrate your existing conventions.

---

I need help migrating my existing AI coding conventions to the cookiecutter-ai-conventions format.

## My Current Conventions
[Paste your existing conventions here - can be multiple files, any format]

## Migration Request
Please analyze my conventions and:

1. **Identify Domains**: Group conventions into logical domains:
   - git (version control, commits, PRs)
   - testing (test structure, coverage, naming)
   - code style (formatting, naming, patterns)
   - documentation (comments, README, API docs)
   - architecture (file organization, design patterns)
   - [any custom domains specific to my conventions]

2. **Extract Triggering Contexts**: For each domain, identify:
   - Keywords that should trigger these conventions
   - File types or patterns where they apply
   - Specific actions (e.g., "when creating commits", "when writing tests")

3. **Format Conventions**: Structure them using this template:

```markdown
# Domain: [Name]

## When This Applies
- Trigger keywords: [list keywords]
- File patterns: [e.g., *.test.js, *.py]
- Actions: [e.g., creating commits, writing functions]

## Conventions

### [Category Name]
- [Specific convention with clear action]
- [Another convention]
- Example: [concrete example if helpful]

### [Another Category]
- [Specific convention]
```

4. **Suggest File Structure**: Recommend which conventions should go in:
   - `global.md` (universal conventions)
   - `domains/[name]/core.md` (domain-specific)
   - Provider-specific templates (if any are tool-specific)

5. **Highlight Patterns**: If you notice any:
   - Contradictions between conventions
   - Opportunities to consolidate similar rules
   - Missing conventions that would complement existing ones

Please maintain my team's specific requirements while improving clarity and organization. Use active voice and be specific about actions developers should take.