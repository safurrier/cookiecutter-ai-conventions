# Writing Core - Authentic Communication and Documentation

This file contains essential writing patterns for documentation, git commits, and technical communication that sounds natural and human.

## Writing Philosophy

Transform AI-generated or overly formal content into authentic, natural human writing while maintaining clarity and professionalism. Focus on identifying and removing telltale signs of LLM-generated text.

## Common LLM Patterns to Avoid

### Academic Buzzwords - NEVER Use These
These words are instant LLM tells. Avoid them completely:

| NEVER Use | Use Instead |
|-----------|-------------|
| intricate | complex, detailed, complicated |
| pivotal | key, important, essential |
| commendable | good, excellent |
| realm | field, area |
| showcase | show, demonstrate |
| delve | explore, examine |
| meticulous | careful, thorough |
| versatile | flexible, adaptable |
| notable | important, significant |
| comprehensive | complete, thorough |
| utilize | use |
| enhance | improve |
| capabilities | abilities |
| crucial | important |
| robust | reliable, stable |
| seamless | smooth |
| leverage | use |
| facilitate | help, enable |

### Overused Transitions - Avoid These Too
- "Additionally" - try: also, plus, and
- "Furthermore" - try: also, what's more
- "Moreover" - try: and, also
- "Effectively" - often unnecessary
- "Significantly" - try: notably, markedly

### Overly Emphatic Language
Avoid dramatic language that sounds artificial:

❌ **Too emphatic:**
- "Major breakthrough"
- "Game-changing feature" 
- "Cutting-edge technology"
- "Revolutionary approach"
- "Unprecedented improvement"

✅ **Natural tone:**
- "Fixed the bug"
- "Added new feature"
- "Updated the code"
- "Improved performance"
- "Better error handling"

## Git Commit Writing

### Commit Message Style
- **Use imperative mood**: "Add feature" not "Added feature"
- **Be specific and concise**: Focus on what changed and why
- **Avoid LLM language**: No "enhance," "implement," "utilize"
- **Natural language**: Write like you're telling a colleague

#### Good Examples
```
Fix login timeout issue when session expires
Add user preference toggle for dark mode
Remove deprecated API calls from payment flow
Update README with new installation steps
```

#### Avoid LLM Style
```
❌ Enhance user authentication capabilities by implementing robust session management
❌ Utilize comprehensive error handling to significantly improve user experience
❌ Showcase pivotal improvements to the intricate payment processing realm
❌ Add comprehensive SSH key management for Synology NAS access (uses "comprehensive")
❌ Fixed major LLM writing tells in documentation (uses "major")
❌ Created comprehensive SSH key management for Synology NAS access (uses "comprehensive" again!)
```

### Commit Body Guidelines
- **Explain the why, not just the what**
- **Use natural language and short sentences**
- **Include specific details that matter**
- **Avoid formal academic tone**

## Documentation Writing

### Natural Documentation Style
- **Write for humans, not algorithms**
- **Use conversational tone when appropriate**
- **Include practical examples**
- **Explain the "why" behind decisions**
- **Vary sentence length and structure**

### Anti-Patterns to Avoid
- Perfectly parallel structure throughout
- Uniform paragraph lengths
- Excessive use of transition words
- Generic statements that could apply anywhere
- Surface-level coverage of everything
- **Flat lists with identical bullet counts (the "4-bullet syndrome")**
- **Overly symmetric formatting across all sections**

### Structure Guidelines
- **Mix paragraph lengths intentionally**
- **Allow natural transitions, not forced ones**
- **Include specific, concrete examples**
- **Focus deeply on key points**
- **Use incomplete sentences for emphasis when appropriate**
- **Vary bullet point usage: 1-3 points max, not 4-6**
- **Mix bullets with paragraphs and nested lists naturally**
- **Some sections shouldn't use bullets at all**

## Technical Communication

### Email and Messages
- **Get to the point quickly**
- **Use natural conversational tone**
- **Include context without over-explaining**
- **End with clear next steps when needed**

### Code Comments
- **Explain the why, not the what**
- **Use natural language**
- **Be specific about edge cases**
- **Avoid formal academic language**

#### Good Examples
```python
# Retry up to 3 times because the API sometimes fails on first request
# Cache this result since the calculation is expensive and rarely changes
# Skip validation here - we already checked this upstream
```

#### Avoid
```python
# Implement comprehensive retry mechanism to enhance system reliability
# Utilize caching capabilities to significantly improve performance metrics
# Bypass validation procedures to optimize processing efficiency
```

## Content Enhancement Techniques

### Creating Authentic Voice
- **Include personal insights that feel genuine**
- **Add unexpected connections or observations**
- **Use specific examples from real experience**
- **Allow productive tangents that add value**
- **Mix technical and plain language naturally**

### Natural Flow Patterns
- **Make writing sound natural when read aloud**
- **Add conversational asides in parentheses**
- **Include brief, relevant digressions**
- **Use natural hesitations or qualifications**
- **Allow some repetition when it aids understanding**

### Breaking LLM Patterns
- **Vary explanation styles throughout**
- **Include relevant anecdotes sparingly**
- **Use concrete examples over abstract concepts**
- **Allow strategic imperfections for authenticity**
- **Focus deeply rather than covering everything superficially**

### Avoiding Bullet Point Symmetry (Major LLM Tell)

❌ **Classic LLM pattern - identical structure everywhere:**
```
## Authentication Features
- Enhanced login validation with comprehensive error handling
- Improved session management through optimized token processing
- Streamlined password reset with intuitive user experience
- Advanced security measures via multi-factor authentication

## Database Optimizations  
- Implemented efficient query caching for improved performance
- Enhanced connection pooling through optimized resource management
- Streamlined data validation with comprehensive error checking
- Advanced indexing strategies via intelligent query analysis
```

✅ **Natural variation:**
```
## Authentication Features
- Fixed login validation errors
- Sessions now last 24 hours instead of expiring randomly
- Password reset actually works on mobile now

## Database Changes
Made several performance improvements:
- Added query caching (50% faster page loads)
- Better connection pooling
  - Reduced connection overhead
  - Handles traffic spikes better
- Fixed slow queries on user search
```

**Key difference:** Natural writing mixes formats, uses different numbers of points, and includes explanatory text between sections.

## Quick Reference

### Before Publishing
Ask yourself:
- [ ] Does this sound like something I'd actually say?
- [ ] Are there too many "academic" words?
- [ ] Is every paragraph the same length?
- [ ] Does it flow naturally when read aloud?
- [ ] Are the examples specific and useful?
- [ ] Would a colleague understand this easily?

### Red Flags
- Every sentence has perfect parallel structure
- Excessive use of transition words
- Generic statements that could apply anywhere
- Formal tone for simple concepts
- No specific examples or concrete details
- Perfectly balanced arguments without natural emphasis
- **Every section has exactly the same number of bullet points**
- **Identical formatting patterns repeated throughout**
- **Long flat lists instead of nested structure when details are needed**
- **Using any word from the "NEVER Use" buzzword list**
- **Overly emphatic language like "major," "breakthrough," "game-changing"**

## Domain-Specific Guidance

For specialized writing in specific areas:
- commit-messages.md: Detailed git commit patterns and conventions
- documentation.md: Technical documentation best practices
- communication.md: Email, Slack, and team communication patterns