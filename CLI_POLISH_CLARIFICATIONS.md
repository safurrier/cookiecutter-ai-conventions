# CLI Polish Implementation Clarifications

This document outlines key implementation decisions needed for GitHub issues #86-90 (CLI Polish & Enhancement Tracker).

## Research Summary

Based on comprehensive analysis:
- **Current CLI**: 6 main commands (status, update, list, capture, sync, config)
- **Architecture**: Click + Rich with comprehensive testing infrastructure
- **Optional Features**: learning capture, context canary, domain composition can be disabled
- **Provider System**: Supports Claude, Cursor, Windsurf, Aider, etc.
- **Best Practices**: Research shows modern CLIs use GitOps auto-sync, add/remove patterns, progressive disclosure

## Implementation Clarification Questions

### 🔄 **Auto-Sync Implementation (#86)**
The research shows GitOps-style auto-sync is the modern standard.

**Questions:**

1. **Trigger mechanism**: Should auto-sync happen:
   - After every `add`/`remove` command? 
   - On file change detection (watch mode)?
   - On a timer (like every 5 minutes)?
   - All of the above with configuration options?

2. **Backward compatibility**: Should we:
   - Remove `sync` command entirely?
   - Keep `sync` as an alias that does nothing but warns?
   - Keep `sync` for manual/force sync scenarios?

### 📝 **Add/Remove Commands (#87)**
Research shows universal `add`/`remove` patterns across all package managers.

**Questions:**

1. **Scope of "capture" → "add"**: Should `add` command:
   - Just rename `capture` to `add` (minimal change)?
   - Also handle adding entire domains (like `ai-conventions add python`)?
   - Support both learning capture AND domain management?

2. **Remove functionality**: What should `remove` delete:
   - Last captured learning by default?
   - Specific learnings by pattern/timestamp?
   - Entire domains?
   - All of the above with different flags?

3. **Data structure**: How to identify items for removal:
   - By timestamp (remove last N)?
   - By content pattern matching?
   - By domain/file/category combination?
   - Interactive selection menu?

### 🧹 **Optional Features Removal (#90)**
Current config has `enable_learning_capture`, `enable_context_canary`, `enable_domain_composition`.

**Questions:**

1. **Integration approach**: Should we:
   - Remove config options and always enable everything?
   - Keep options but default them to `true`? 
   - Remove the options but keep the functionality toggleable via CLI flags?

2. **Migration**: For existing users with these disabled:
   - Force-enable on next update?
   - Show warning but respect current settings?
   - Migrate config automatically?

### 🔍 **CLI Audit Priorities (#88)**
Based on research and current commands, I see these UX issues.

**Confirm priorities:**

1. **Command discoverability**: New users might not understand:
   - What "capture" does (hence rename to "add")
   - When to use "update" vs "sync" vs "status"
   - How to get started (need `init` or `getting-started` command?)

2. **Missing commands** users might expect:
   - `init` - Set up new conventions repository
   - `doctor` - Diagnose installation issues  
   - `getting-started` - Interactive tutorial
   - `search` - Find specific conventions

3. **Command consolidation**: Should we merge any existing commands?

### 📚 **Documentation Scope (#89)**

**Questions:**

1. **Update scope**: Should we update:
   - Just CLI help text and command descriptions?
   - CLAUDE.md templates in cookiecutter?
   - MkDocs documentation site?
   - All of the above?

2. **New command documentation**: For new commands (`add`, `remove`, `init`, etc.), where should docs live?

## Implementation Strategy Questions

### 🎯 **Implementation Order & Scope**

Given these are 5 related issues:

**Questions:**

1. **Phased approach**: Should we implement:
   - All issues in one large PR?
   - Each issue as separate PR?
   - Group related issues (e.g., #86+#87 together, then #88+#89+#90)?

2. **Breaking changes**: These changes will break existing workflows. Should we:
   - Implement with deprecation warnings first?
   - Go straight to new behavior?
   - Provide migration guide/script?

3. **Testing strategy**: Focus on:
   - Unit tests for each command?
   - Integration tests for workflows?
   - User acceptance testing with real scenarios?

### 🚀 **Success Metrics**

How should we measure success:
- Reduced time-to-first-success for new users?
- Fewer support questions about CLI usage?
- Specific user workflows to optimize for?

## Current CLI Command Analysis

From technical analysis, here's what we have now:

### Existing Commands
- `ai-conventions status` - Check installation status
- `ai-conventions update` - Update conventions from upstream 
- `ai-conventions list` - List available domains
- `ai-conventions capture` - Capture new learning/patterns
- `ai-conventions sync` - Sync conventions to providers
- `ai-conventions config` - Configuration management

### Identified UX Issues
1. **Command names**: "capture" is not intuitive (should be "add")
2. **Manual sync friction**: Users must remember to sync after changes
3. **Optional complexity**: Users can disable useful features
4. **Missing onboarding**: No `init` or getting-started flow
5. **No removal capability**: Can't easily undo additions

### Proposed Command Structure (Based on Research)
```bash
ai-conventions add <pattern>         # Rename from capture
ai-conventions remove [pattern]      # New - remove last or specific
ai-conventions list                  # Keep existing
ai-conventions status                # Keep existing  
ai-conventions update                # Keep existing
ai-conventions config                # Keep existing
ai-conventions init                  # New - setup wizard
ai-conventions doctor                # New - diagnose issues
ai-conventions getting-started       # New - interactive tutorial
# Auto-sync removes need for manual sync command
```

## Clarifications Received

### ✅ **Resolved Decisions:**

**#86 Auto-sync:**
- ✅ Trigger after each add/remove command
- ✅ Remove sync command entirely (no backwards compatibility)

**#87 Add/Remove:**
- ✅ Rename capture → add
- ✅ Add supports both conventions and domain management
- ✅ Remove defaults to last entry, can specify last N
- ✅ Keep removal simple using log entries

**#90 Optional Features:**
- ✅ Remove config options, enable everything by default
- ✅ No migration concerns

**#89 Documentation:**
- ✅ Update all documentation (help flags, templates, MkDocs)

**Implementation Strategy:**
- ✅ Group related issues into separate branches/PRs
- ✅ Go straight to new behavior (no backwards compatibility)
- ✅ Follow existing testing patterns + comprehensive end-to-end testing

### ✅ **Final Clarifications Received:**

**#88 Command Consolidation:**
- ✅ Keep `status` as-is 
- ✅ Remove `update` command entirely
- ✅ Enhanced `list` with tree structure as default, option for domains-only

**Enhanced List Command:**
- ✅ Default behavior: tree structure (verbosity level 1)
- ✅ Option for domains-only: verbosity 0 or `list domains` subcommand
- ✅ Tree format with folder structure and .md files

**Domain Management in Add:**
- ✅ `ai-conventions add python/testing "Use pytest fixtures"` creates domain AND adds convention
- ✅ No confirmation prompts, just inform user what was created
- ✅ Nested structures: check each level, create as needed, last part is the file
- ✅ Example: `git/workflows/ci` → check git/, check workflows/, write to ci.md

**Init Command:**
- ✅ Punt for now - open separate GitHub issue about user journey and CLI/template separation

**Remove Command:**
- ✅ Simple approach: no args removes last entry with message
- ✅ `remove N` removes last N entries chronologically  
- ✅ No interactive menus, keep it simple

**PR Grouping:**
- ✅ Group 1: #86 + #87 (auto-sync + add/remove commands)
- ✅ Group 2: #88 + #90 (CLI audit + remove optional features)
- ✅ Group 3: #89 (documentation updates)

## 📋 **Ready for TDD Implementation Plan**

All clarifications complete. The implementation plan will cover:

1. **Group 1 (Issues #86 + #87)**: Auto-sync + Add/Remove Commands
   - Remove sync command, implement auto-sync after add/remove
   - Rename capture → add with domain management  
   - Implement remove command with log integration

2. **Group 2 (Issues #88 + #90)**: CLI Audit + Remove Optional Features
   - Remove update command
   - Enhanced list command with tree structure
   - Remove optional feature config options

3. **Group 3 (Issue #89)**: Documentation Updates
   - Update help text, templates, MkDocs
   - Comprehensive documentation for all new commands

4. **Additional Issue**: Init Command User Journey
   - Separate GitHub issue for future CLI/template separation consideration

---

**🚀 Proceeding to create detailed TDD implementation plan with test scenarios and implementation steps.**