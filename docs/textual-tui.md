# Textual TUI for AI Conventions

The AI Conventions template includes an optional Text User Interface (TUI) built with [Textual](https://textual.textualize.io/) for interactive installation and management.

## Features

- **Interactive Provider Selection**: Choose which AI tools to configure with checkboxes
- **Configuration Options**: Toggle features like learning capture, context canary, and domain composition
- **Live Installation Log**: See real-time feedback as conventions are installed
- **Cross-Platform**: Works in any terminal that supports modern terminal features

## Usage

### Running the TUI

After generating your project and installing dependencies:

```bash
cd your-project
uv tool install .
python install.py --tui
```

### TUI Interface

The TUI presents a split-screen interface:

1. **Left Panel - Provider Selection**:
   - Claude
   - Cursor  
   - Windsurf
   - Aider
   - Copilot
   - Codex

2. **Right Panel - Options**:
   - Enable Learning Capture
   - Enable Context Canary
   - Enable Domain Composition

3. **Bottom Panel - Installation Log**:
   - Real-time installation progress
   - Success/failure messages
   - Installation paths

### Keyboard Shortcuts

- `Tab` / `Shift+Tab`: Navigate between controls
- `Space`: Toggle checkboxes
- `Enter`: Activate buttons
- `q`: Quit the application
- `i`: Go to install screen

## Implementation Details

The TUI is implemented in `ai_conventions/tui.py` and includes:

- `ConventionsTUI`: Main application class
- `InstallScreen`: Primary installation interface
- Provider integration via the provider abstraction layer
- Configuration management integration

## Customization

You can customize the TUI by modifying:

1. **Styling**: Edit the CSS strings in the screen classes
2. **Layout**: Modify the `compose()` methods to change widget arrangement
3. **Functionality**: Add new screens or widgets for additional features

## Dependencies

The TUI requires Textual, which is automatically included when you select this feature during project generation. The dependency is managed via `pyproject.toml`:

```toml
dependencies = [
    "textual>=0.47.0",
    # ... other dependencies
]
```

## Future Enhancements

Potential improvements to the TUI:

1. **Configuration Editor**: Direct editing of config values
2. **Domain Manager**: Browse and manage available domains
3. **Provider Status**: Show current installation status for each provider
4. **Learning Review**: Interface for reviewing and promoting learnings
5. **Update Checker**: Check for template updates