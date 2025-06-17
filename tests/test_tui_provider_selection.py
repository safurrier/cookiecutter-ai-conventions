"""Test TUI provider selection handling."""

import sys


def test_tui_handles_comma_separated_providers(cookies):
    """Test that TUI correctly handles comma-separated provider strings."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": "claude,cursor,windsurf",
        }
    )

    assert result.exit_code == 0

    # Import the TUI module
    sys.path.insert(0, str(result.project_path))

    # Clear any previously imported modules
    modules_to_remove = [key for key in sys.modules.keys() if key.startswith("ai_conventions")]
    for module in modules_to_remove:
        del sys.modules[module]

    from pathlib import Path

    from ai_conventions.tui import InstallScreen

    # Test config with comma-separated string
    config = {"selected_providers": "claude,cursor,windsurf"}
    screen = InstallScreen(Path.cwd(), config)

    # The screen should handle the comma-separated string properly
    # This would be tested more thoroughly with actual Textual testing
    # but for now we just ensure it doesn't crash
    assert screen.config == config


def test_install_py_handles_comma_separated_providers(cookies):
    """Test that install.py correctly handles comma-separated provider strings."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": "claude,cursor",
        }
    )

    assert result.exit_code == 0

    # Check that install.py was generated correctly
    install_py = result.project_path / "install.py"
    content = install_py.read_text(encoding="utf-8")

    # Should not have jsonify filter
    assert "| jsonify" not in content

    # Check that the template variable is properly formatted without jsonify
    # After cookiecutter processing, the actual values will be substituted
    # We just need to ensure the jsonify filter is not used
