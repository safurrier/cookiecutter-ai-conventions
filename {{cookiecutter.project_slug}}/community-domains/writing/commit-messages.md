# Git Commit Messages - Natural and Effective Communication

Detailed patterns for writing clear, natural git commit messages that communicate effectively with your team.

## Core Principles

### Imperative Mood
Write commits as instructions to the codebase:
- "Add user authentication" ✅
- "Added user authentication" ❌
- "Adding user authentication" ❌

### Natural Language
Write like you're telling a teammate what you did:
- "Fix crash when user logs out" ✅
- "Implement comprehensive logout functionality enhancement" ❌

## Message Structure

### First Line (50 characters or less)
```
Fix login timeout when session expires
Add dark mode toggle to user preferences
Remove deprecated payment API calls
Update installation docs for new requirements
```

### Body (when needed)
Explain the why, not just the what:
```
Fix login timeout when session expires

Users were getting logged out unexpectedly after 15 minutes
even when actively using the app. Changed session check
from server-side timer to activity-based renewal.

Fixes issue where users lost work during long form submissions.
```

## Common Commit Types

### Bug Fixes
Focus on the problem being solved:
```
Fix memory leak in file upload component
Resolve crash when processing large CSV files
Fix incorrect tax calculation for Canadian orders
Prevent duplicate emails when user clicks signup twice
```

### New Features
Describe what the user can now do:
```
Add ability to export data as PDF
Let users upload profile pictures
Enable two-factor authentication for admin accounts
Add search functionality to order history
```

### Refactoring
Explain the improvement:
```
Simplify user validation logic
Extract common database queries into helper functions
Move payment processing to separate service
Clean up unused CSS and JavaScript files
```

### Documentation
Be specific about what was updated:
```
Update README with Docker setup instructions
Add API documentation for new webhook endpoints
Fix typos in installation guide
Document new environment variables
```

## Anti-Patterns to Avoid

### Too Vague
❌ "Update code"
❌ "Fix issues"
❌ "Improve functionality"
❌ "Make changes"

### Too LLM-y
❌ "Implement comprehensive authentication enhancement"
❌ "Utilize advanced caching mechanisms to optimize performance"
❌ "Enhance user experience through intuitive interface improvements"

### Too Technical for First Line
❌ "Refactor UserAuthenticationService.validateCredentials() to improve error handling"
✅ "Fix unclear error messages during login"

### Missing Context
❌ "Fix bug" (which bug?)
❌ "Add feature" (which feature?)
❌ "Update tests" (for what?)

## Commit Body Best Practices

### Include Context
```
Remove user data export feature

This feature was causing performance issues and wasn't
being used by many users. Analytics show less than 2%
adoption over 6 months.

Will reconsider if demand increases or we can solve
the performance problems.
```

### Explain Technical Decisions
```
Switch from Redis to in-memory cache for session storage

Redis was overkill for our session needs and added
deployment complexity. In-memory storage is simpler
and performs better for our use case.

Sessions will be lost on server restart, but that's
acceptable since sessions expire after 24 hours anyway.
```

### Reference Issues When Helpful
```
Fix email notification delays

Email queue was backing up during high traffic periods.
Added retry logic and better error handling.

Closes #1234
Related to performance improvements in #1200
```

## Team Communication

### Consider Your Audience
Write for the developer who will read this in 6 months (including yourself):
- Provide enough context to understand the change
- Explain decisions that might not be obvious
- Include links to relevant discussions or tickets

### Breaking Changes
Be extra clear about changes that affect other developers:
```
BREAKING: Change API response format for user endpoints

User data now includes additional fields and nested objects.
See migration guide in docs/api-migration.md

This affects:
- Mobile app (needs update)
- Analytics dashboard (backward compatible)
- Third-party integrations (may need updates)
```

## Quick Reference

### Good Commit First Lines
- Start with a verb in imperative mood
- Be specific about what changed
- Keep under 50 characters
- Use natural, conversational language
- Focus on the user impact when possible

### When to Include Body
- Breaking changes or API modifications
- Bug fixes that need context about the problem
- Performance improvements with metrics
- Complex refactoring that affects multiple areas
- Decisions that future developers might question

### Formatting Tips
- Use bullet points sparingly (1-3 points max, not flat lists)
- Include relevant issue numbers
- Keep lines under 72 characters in body
- Use blank lines to separate logical sections
- Bold or CAPS for breaking changes only when necessary

### Avoid LLM Patterns in Body
❌ **Robotic formatting with identical structure:**
```
Enhanced user authentication system with comprehensive improvements:
- Implemented robust session management capabilities
- Optimized login validation mechanisms
- Enhanced error handling infrastructure
- Streamlined user experience optimization
```

✅ **Natural variation:**
```
Fix user authentication issues

Login validation was failing for users with special characters
in passwords. Added proper escaping and improved error messages.

Also cleaned up session handling - sessions now last 24 hours
instead of expiring randomly.
```

The goal is clear communication, not perfect formatting.

