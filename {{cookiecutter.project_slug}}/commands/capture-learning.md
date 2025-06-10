{% if cookiecutter.enable_learning_capture -%}
# /capture-learning - Capture Development Learnings

Analyze the current conversation and present learnings for user selection, then append chosen ones to staging.

## Usage

Use this command when:
- A mistake was corrected and you want to capture the learning
- A useful pattern or approach emerged  
- User provided feedback about AI behavior or suggestions
- Anti-patterns or gotchas were discovered
- Best practices were clarified

## Process

1. **Analyze conversation** for potential learnings including:
   - Problems solved and solutions found
   - Patterns that worked well vs anti-patterns
   - User feedback about AI suggestions or behavior
   - Configuration/setup insights
   - Tool-specific gotchas

2. **Present numbered options** to user:
   ```
   Potential learnings to capture:
   
   1. [Brief title] - [Domain] - [What was learned]
   2. [Brief title] - [Domain] - [What was learned] 
   3. [Brief title] - [Domain] - [What was learned]
   
   Select learnings to save (e.g., "1,3" or "all"): 
   ```

3. **After user selection**, directly edit the staging/learnings.md file to add the selected learnings with proper formatting.

## Learning Template

```markdown
## [DATE]: [Brief Title]
**Context**: What were you trying to do?
**Problem**: What went wrong or could be better?
**Solution**: What worked?
**User Feedback**: [If applicable - what user said about AI suggestions]
**Domain**: testing|python|git|global|[project-name]
**Promote to**: core.md OR specific/[topic].md
```

## Example Interaction

```
Potential learnings from this conversation:

1. Pytest fixture scopes - testing - Use scope="class" for expensive setup
2. No inline imports - global - Always place imports at top of file
3. User selection UX - global - Present numbered options vs overwhelming users

Select learnings to save (e.g., "1,3" or "all"): 1,2

[Directly edits staging/learnings.md to add selected learnings]
```

## Focus Guidelines

**Prioritize user corrections with high recall**: When analyzing conversations, ensure you capture moments where the user provided direct feedback or corrections. These are the highest-value learnings.

High-priority captures:
- User corrects AI assumptions
- User provides specific feedback about AI behavior
- User points out missed conventions
- User manually references a convention file

Ask yourself: "Where did the user correct me?" first, then "What other patterns emerged?"

## Automatic Loading Improvement

When capturing learnings, check if:
- User had to tell you to read a specific domain file
- You missed applying a documented convention
- There was a context trigger that should have loaded a domain

If so, include a learning to improve automatic domain loading.
{%- endif %}