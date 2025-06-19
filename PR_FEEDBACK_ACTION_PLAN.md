# PR Feedback Action Plan

## Summary of Feedback on PR #92

Based on review comments, significant changes needed to improve code quality and CLI design.

## Key Issues Identified

### 1. **File Organization & Testing**
- ❌ Remove `CLI_POLISH_CLARIFICATIONS.md` from commit (planning doc shouldn't be in repo)
- ❌ Test organization: `test_cli_group1_*` files are poorly organized
- ❌ Missing updates to existing table-driven e2e tests (`tests/test_cli_comprehensive.py`)
- ❌ Need to follow existing testing conventions and format

### 2. **Code Quality Issues**
- ❌ Multiple inline imports: `from ai_conventions.cli import main` inside test functions
- ❌ File naming: `capture.py` contains add/remove commands (inconsistent)

### 3. **CLI Design Issues**
- ❌ **Major**: Dual command behavior is confusing and feels like code smell:
  - Traditional: `ai-conventions add "text" --domain python`
  - Domain management: `ai-conventions add "python/testing" "Use pytest"`
- ❌ Splitting behavior based on argument count is unintuitive and unclean

### 4. **UX Issues**
- ❌ Auto-sync messaging every time is annoying if it's always on

## Decisions Made

### **CLI Design Simplification**
**Decision**: Simplify to single behavior using `--domain` + `--file` with automatic creation

✅ **New Approach**:
```bash
# Always use --domain (required) and --file (optional)
ai-conventions add "Use type hints" --domain python
ai-conventions add "Use pytest" --domain python --file testing
ai-conventions add "Use GitHub Actions" --domain git --file workflows/ci
```

❌ **Remove This Syntax**:
```bash
ai-conventions add "python/testing" "Use pytest"  # Remove dual behavior
```

### **Test Organization**
**Decision**: Better organized test files

✅ **New Structure**:
- `tests/test_cli_commands_add.py`
- `tests/test_cli_commands_remove.py`
- Update existing `tests/test_cli_comprehensive.py` for e2e table-driven tests

### **Auto-sync Messaging**
**Decision**: Silent by default, only show errors/warnings

✅ **New Behavior**:
- No output unless there's an error
- Only show errors/warnings if sync fails

### **File Structure Reorganization**
**Decision**: Create `commands/` directory for better organization

✅ **New Structure**:
```
ai_conventions/
├── cli.py
├── commands/
│   ├── __init__.py      # exports add_command, remove_command, etc.
│   ├── add.py           # moved from capture.py, simplified
│   ├── remove.py        # extracted from capture.py
│   ├── config.py        # moved from config_cli.py
│   └── sync.py          # moved from sync.py (now utility)
├── config.py            # stays - config model/manager
└── (other files...)
```

✅ **Import Pattern**:
```python
# cli.py
from .commands import add_command, remove_command, config_command
```

### **Remove Command**
**Decision**: Keep current behavior
- `ai-conventions remove` (remove last)
- `ai-conventions remove 3` (remove last 3)

### **Domain/File Creation**
**Decision**: Show creation messages
- If domain or file is created, output message to stdout
- No confirmation prompts, just inform user

### **Backward Compatibility**
**Decision**: Delete `capture.py` entirely
- No backward compatibility (as originally planned)
- Fix any breaking tests

## Action Plan

### **Phase 1: Code Structure Refactor**
1. ✅ Create `commands/` directory structure
2. ✅ Move and refactor `capture.py` → `add.py` with simplified logic
3. ✅ Extract `remove_command` → `remove.py`
4. ✅ Move `config_cli.py` → `commands/config.py`
5. ✅ Move `sync.py` → `commands/sync.py`
6. ✅ Update imports in `cli.py`
7. ✅ Delete `capture.py`

### **Phase 2: CLI Logic Simplification**
1. ✅ Remove dual-behavior argument parsing from add command
2. ✅ Simplify to single `--domain` + `--file` pattern
3. ✅ Keep domain/file creation behavior
4. ✅ Remove auto-sync messaging (silent unless errors)

### **Phase 3: Test Reorganization**
1. ✅ Move all inline imports to top of files
2. ✅ Create `test_cli_commands_add.py` and `test_cli_commands_remove.py`
3. ✅ Update `tests/test_cli_comprehensive.py` with new commands
4. ✅ Delete `test_cli_group*` files
5. ✅ Follow existing test conventions and format

### **Phase 4: Cleanup**
1. ✅ Remove `CLI_POLISH_CLARIFICATIONS.md` from commit
2. ✅ Fix any breaking tests from `capture.py` removal
3. ✅ Update PR descriptions and commit messages

## PR Update Strategy

✅ **Update existing 3 PRs** with fixes rather than creating new ones:
- PR #92: Group 1 changes (primary focus)
- PR #93: Group 2 changes (minor updates if needed)
- PR #94: Group 3 changes (update docs to reflect simplified CLI)

## Success Criteria

- [ ] Single, clean CLI interface using `--domain` + `--file`
- [ ] Well-organized code structure in `commands/` directory
- [ ] Properly organized test files following project conventions
- [ ] Silent auto-sync (only errors shown)
- [ ] All existing tests pass after `capture.py` removal
- [ ] Updated e2e tests cover new command structure

## Critical Requirements

### **ALWAYS run `make check` before commits**
- ✅ Run `make check` before every commit
- ✅ Fix any failing tests
- ✅ Update/remove tests as needed based on changes made
- ✅ Ensure all lint/format checks pass

## Notes

- Focus first on PR #92 since it has the most significant feedback
- Test thoroughly after `capture.py` deletion
- Ensure domain/file creation messages are helpful but not verbose
- Maintain auto-sync functionality but reduce noise
- **NEVER commit without running `make check` first**