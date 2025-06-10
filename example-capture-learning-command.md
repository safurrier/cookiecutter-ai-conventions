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
2. File access workaround - global - Claude Code can't edit outside cwd, use bash commands
3. User selection UX - global - Present numbered options vs overwhelming users

Select learnings to save (e.g., "1,3" or "all"): 1,2

[Provides bash commands to append selected learnings]
```

Focus on actionable insights that prevent future mistakes or capture user preferences about AI behavior.

## Focus Guidelines

**Prioritize user corrections with high recall**: When analyzing conversations, ensure you capture moments where the user provided direct feedback or corrections. These are the highest-value learnings. Also include other valuable patterns and insights that emerged.

High-priority captures (ensure high recall):
- User says "no inline imports" when you tried to add imports inside a function
- User corrects your assumptions about testing approaches or project conventions
- User provides specific feedback about AI suggestions or behavior
- User points out you missed checking project documentation
- **User had to manually reference a convention file** (signals automatic loading failure)

Also valuable to capture:
- Useful patterns or anti-patterns discovered during development
- Configuration insights or tool-specific gotchas
- Successful approaches that worked well
- Technical discoveries that could help future development

Ask yourself: "Where did the user correct me?" first, then "What other patterns emerged that would be useful to remember?"

## Automatic Loading Improvement

**When capturing learnings, specifically check for:**
- Did the user have to tell you to read a specific domain file?
- Did you miss applying a convention that was already documented?
- Was there a context trigger that should have loaded a domain but didn't?

If any of these occurred, include a special learning type:
```markdown
## [DATE]: Improve Automatic Domain Loading
**Context**: Working on [specific task]
**Problem**: Failed to automatically load @domains/[domain]/[file].md
**Trigger**: User had to say "read the [domain] conventions"
**Solution**: Add context trigger to new-CLAUDE.md mapping
**Domain**: global
**Promote to**: Update new-CLAUDE.md context mapping table
```

This creates a feedback loop where the system learns from its failures to automatically load the right context.

