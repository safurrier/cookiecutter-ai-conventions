# /review-learnings - Review and Promote Staged Learnings

Review learnings in staging and help promote stable patterns to appropriate domain files.

## Usage

Use this command to:
- Review accumulated learnings in staging
- Identify patterns ready for promotion to domain files
- Clean up staging by archiving processed learnings
- Ensure learnings get integrated into the stdlib

## Process

1. **Display staged learnings** from staging/learnings.md with numbers

2. **Analyze for promotion opportunities**:
   - Learnings that fit existing domain files
   - Patterns that suggest new domain files needed
   - Learnings ready to become core principles
   - Items that should be archived as one-time fixes

3. **Present promotion options**:
   ```
   Staged learnings ready for promotion:

   1. [Title] → domains/testing/pytest.md (fixture scopes section)
   2. [Title] → global.md (file access patterns)
   3. [Title] → domains/testing/core.md (new anti-pattern section)

   Select learnings to promote (e.g., "1,3"):
   ```

4. **Directly edit domain files** to add the promoted learnings in the appropriate sections.

5. **Archive processed learnings** by moving them from staging to archive files, then clear the staging file.

## Promotion Guidelines

### To new-CLAUDE.md (Automatic Loading)
- When learning type is "Improve Automatic Domain Loading"
- Update the Context → Domain Mapping table
- Add new trigger keywords or file patterns
- Ensures future automatic loading of conventions

### To domain/*/core.md
- Universal principles for that domain
- Essential patterns used frequently
- Critical anti-patterns to avoid

### To domain/*/specific.md
- Detailed implementation patterns
- Tool-specific configurations
- Advanced techniques

### To global.md
- Universal development principles
- Cross-domain patterns
- Project-agnostic best practices

### To archive/
- One-time fixes or very specific solutions
- Learnings that became obsolete
- Context-specific insights

## Review Schedule

- **Weekly**: Review staging for promotion candidates
- **Monthly**: Archive promoted learnings and clean staging
- **Quarterly**: Review domain files for consolidation opportunities

Keep the stdlib focused on reusable, actionable patterns rather than specific one-time fixes.

