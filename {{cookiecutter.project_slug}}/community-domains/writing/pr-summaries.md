# Pull Request Summaries - Clear and Effective Communication

Guidelines for writing PR summaries that communicate changes clearly without sounding like AI-generated content.

## Core Principles

### Lead with Impact
Start with what changed for users, not implementation details:
- "Fixed login timeout issues" ✅
- "Implemented comprehensive authentication enhancements" ❌

### Use Natural Language
Write like you're explaining changes to a teammate:
- "Added dark mode toggle" ✅
- "Implemented comprehensive UI theming capabilities" ❌

### Be Specific
Include concrete details instead of vague improvements:
- "Progress tracker now shows 4 clear stages instead of jumping to 100%" ✅
- "Enhanced progress tracking functionality" ❌

## PR Summary Structure

### Title
Keep it direct and specific (50 characters or less):
```
Fix progress tracker stage display
Add user profile editing
Remove deprecated payment API
Update Docker setup for M1 Macs
```

### Summary Section
One sentence describing the main change:
```
## Summary
This PR fixes the progress tracker jumping from 10% directly to complete by showing clear stages.
```

### Changes Section
Group related changes, focus on user impact:
```
## Changes

**Progress Tracking**
- Fixed tracker jumping from "Extraction (10%)" to complete
- Now shows clear stages: "Extracting (1/4)" → "Analyzing (2/4)" etc.
- Added real-time updates without page refresh

**Error Handling**
- Fixed crash when processing large files
- Added user-friendly error messages
- Better handling of network timeouts

**UI Improvements**
- Dropdown selections now persist during updates
- Copy button works reliably with fallback options
- Error messages show helpful context
```

## Anti-Patterns to Avoid

### LLM Buzzwords
Replace these overused terms:

| Avoid | Use Instead |
|-------|-------------|
| "Comprehensive" | Specific details |
| "Enhanced" | "Improved" or "Fixed" |
| "Implemented" | "Added" or "Built" |
| "Optimized" | "Made faster" or "Reduced" |
| "Robust" | "Reliable" or specific benefit |
| "Seamless" | "Smooth" or omit |
| "Leverage" | "Use" |
| "Facilitate" | "Enable" or "Allow" |

### Over-Categorization and Bullet Point Symmetry
❌ Too many emoji categories and perfectly parallel structure:
```
### 🎯 Performance Enhancements
### 🔧 Infrastructure Improvements
### 🤖 AI Integration Optimizations
### 💻 User Experience Enhancements
### 📊 Observability Improvements
### 🧪 Testing Infrastructure
```

❌ Overly symmetric bullet points:
```
**Enhanced Planning Commands**
- Enhanced TDD planning with sub-agent delegation for parallel research
- Comprehensive research phase using WebSearch and WebFetch for domain knowledge
- Research-informed implementation with 2025+ best practices integration
- Streamlined upfront clarification protocol to prevent implementation rework
```

✅ Simple, clear groups with natural variation:
```
**Bug Fixes**
**New Features**
**Performance**
```

✅ Natural, varied bullet points:
```
**Planning Commands**
- Added TDD planning with research integration
- Now uses WebSearch and WebFetch to gather domain knowledge
- Includes upfront clarification to prevent rework
- Updated for 2025+ best practices
```

### Academic Language
❌ "This PR implements comprehensive TDD-driven fixes addressing several critical issues"
✅ "This PR fixes several bugs in the progress tracker and error handling"

## Natural Writing Techniques

### Use Active Voice
- "Added user authentication" ✅
- "User authentication was implemented" ❌

### Vary Structure and Avoid Uniform Formatting
Don't make every section identical with flat bullet lists:

❌ **Robotic pattern (flat lists of 4+ bullets everywhere):**
```
**Planning Commands**
- Enhanced TDD planning with sub-agent delegation
- Comprehensive research phase using WebSearch
- Research-informed implementation with best practices
- Streamlined upfront clarification protocol

**Writing Domain**
- Comprehensive writing guidance for documentation
- Anti-patterns for avoiding LLM-speak and buzzwords
- Specific guidance for git commit messages
- Integrated into global CLAUDE.md for loading
```

✅ **Natural variation with nested structure:**
```
**Planning Commands**
Added TDD planning with research integration:
- Uses WebSearch and WebFetch for domain knowledge
- Includes upfront clarification to prevent rework

**Writing Domain**
Created writing guidance to avoid LLM-speak. Key changes:
- Before/after examples for natural vs AI writing
- Commit message patterns
  - Use imperative mood
  - Avoid buzzwords like "enhance" and "implement"
- PR summary guidelines with anti-patterns

**Knowledge Base**
- Fixed NO INLINE IMPORTS rule with examples
- Added 80/20 principle for feature complexity
```

**Principles:**
- Use 1-3 bullet points, not 4-6
- Mix bullets with paragraphs and nested lists
- Nest related details under main points
- Some sections shouldn't use bullets at all

### Include Context When Helpful
```
**File Upload Fixes**
- Fixed memory leak when uploading large files
- Users were seeing crashes with files over 100MB
- Now processes files in chunks to prevent timeouts
```

### Show Before/After When Useful
```
**Progress Display**
- Before: "Extraction (10%)" → jumps to "Complete"
- After: "Extracting (1/4)" → "Analyzing (2/4)" → "Processing (3/4)" → "Complete (4/4)"
```

## Test Plan Section

### Be Specific About Testing
❌ Generic checklist:
```
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual testing completed
```

✅ Specific test scenarios:
```
**Tested scenarios:**
- Progress tracker shows all 4 stages during file processing
- Error messages appear when upload fails
- Dropdown selections persist during HTMX updates
- Copy button works in both Chrome and Firefox
```

### Manual Testing Notes
Include what you actually tested:
```
**Manual testing:**
- Uploaded 50MB file, progress showed all stages correctly
- Simulated network failure, got clear error message
- Tested on mobile, dropdowns work properly
```

## Common PR Types

### Bug Fixes
Focus on the problem and solution:
```
## Summary
Fixed users getting logged out unexpectedly during long sessions.

## Changes
- Session timeout now resets with user activity
- Added warning before session expires
- Fixed race condition in session renewal

**Problem:** Users lost work when filling out long forms
**Solution:** Activity-based session renewal instead of fixed timer
```

### New Features
Explain what users can now do:
```
## Summary
Added ability for users to export their data as PDF.

## Changes
- New "Export PDF" button in account settings
- Includes all user data and activity history
- Works with custom date ranges
- Sends download link via email for large exports
```

### Refactoring
Explain the benefit:
```
## Summary
Simplified payment processing code to make it easier to add new payment methods.

## Changes
- Extracted common payment logic into shared functions
- Removed duplicate code across Stripe, PayPal, and Apple Pay
- Added tests for payment method validation

**Why:** Adding new payment methods required copying lots of code. Now it's much simpler.
```

## Review Checklist

### Before Submitting
- [ ] Title describes the main change in plain English
- [ ] Summary explains impact in one sentence
- [ ] Changes focus on user benefits, not implementation
- [ ] No LLM buzzwords (comprehensive, enhanced, robust, etc.)
- [ ] Test plan includes specific scenarios tested
- [ ] Screenshots included for UI changes
- [ ] Breaking changes clearly marked

### Red Flags
- Every bullet point starts the same way
- Too many emoji categories
- Academic language for simple changes
- Vague improvements without specifics
- No mention of what was actually tested
- Generic statements that could apply to any PR

## Examples

### Good PR Summary
```
## Summary
Fixed the file upload progress bar jumping from 10% directly to complete.

## Changes
**Progress Display**
- Shows clear stages: "Uploading (1/3)" → "Processing (2/3)" → "Complete (3/3)"
- Updates in real-time without page refresh
- Added cancel button during upload

**Error Handling**
- Better error messages when upload fails
- Retry button for network errors
- Shows which files failed in batch uploads

## Testing
- Tested with files from 1MB to 500MB
- Simulated network failures to test error handling
- Verified progress display on mobile devices
```

### Avoid This Style
```
## Summary
This PR implements comprehensive enhancements to optimize the file upload experience through robust progress tracking mechanisms and enhanced error handling capabilities.

## Key Improvements
### 🎯 Progress Tracking Optimization
- Implemented granular stage-based progress visualization
- Enhanced real-time progress update mechanisms
- Optimized user experience through seamless progress indication

### 🔧 Error Handling Enhancement
- Implemented robust error handling infrastructure
- Enhanced error messaging capabilities
- Optimized error recovery mechanisms
```

The goal is clear communication that helps reviewers understand changes quickly and accurately.

