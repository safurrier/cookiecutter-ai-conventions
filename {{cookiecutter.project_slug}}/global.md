# Global Conventions - Universal Rules

These conventions apply across all contexts and should always be followed.

## Code Quality

### No Inline Imports
- **ALWAYS place imports at the top of the file**
- This is frequently violated when adding new functionality
- Exception: Only when explicitly needed with comment explaining why

### Single Source of Truth
- Consolidate duplicate functions and constants
- Create centralized configuration
- Avoid scattered magic strings

## AI Interaction

### Natural Language
- Avoid phrases like "Updated X to Y" in outputs
- Write as a human would write
- No LLM tells or artifacts in generated content

### Explicit is Better Than Implicit
- State assumptions clearly
- Avoid magic behavior
- Make intent obvious in code

## Development Practices

### MODEST Principles
- **M**odularity: Create reusable, swappable components
- **O**rthogonality: Keep components independent  
- **D**ependency Injection: Pass dependencies explicitly
- **E**xplicitness: Avoid magic, make intent clear
- **S**ingle Responsibility: One reason to change
- **T**estability: Design for easy testing

### Error Handling
- Provide helpful error messages
- Include context about what went wrong
- Suggest how to fix the problem
- Never silently fail

## Learning Integration

When these conventions are violated:
1. Correct the issue
2. Consider capturing as a learning
3. Update relevant domain if pattern repeats
