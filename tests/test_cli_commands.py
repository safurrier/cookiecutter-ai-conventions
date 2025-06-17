"""Test CLI command functionality."""

import sys


def test_cli_commands_available_after_install(cookies):
    """Test that CLI commands are available after installation."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_learning_capture": True,
        }
    )

    assert result.exit_code == 0

    # Check pyproject.toml has entry points
    pyproject = result.project_path / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")

    assert "[project.scripts]" in content
    assert 'my-project = "ai_conventions.cli:main"' in content
    assert 'capture-learning = "ai_conventions.capture:main"' in content
    assert 'sync-conventions = "ai_conventions.sync:main"' in content


def test_ai_conventions_status_command(cookies):
    """Test the ai-conventions status command structure."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    # Check CLI module exists
    cli_module = result.project_path / "ai_conventions" / "cli.py"
    assert cli_module.exists()

    content = cli_module.read_text(encoding="utf-8")

    # Check for status command
    assert "@click.command()" in content or "@main.command()" in content
    assert "def status" in content

    # Check it uses Click
    assert "import click" in content
    assert "@click.group(" in content


def test_capture_learning_command_structure(cookies):
    """Test the capture-learning command structure."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_learning_capture": True,
        }
    )

    assert result.exit_code == 0

    # Check capture module exists
    capture_module = result.project_path / "ai_conventions" / "capture.py"
    assert capture_module.exists()

    content = capture_module.read_text(encoding="utf-8")

    # Check main function (might have parameters due to @click.command decorator)
    assert "def capture_command(" in content or "def main(" in content

    # Check it imports necessary modules
    assert "from pathlib import Path" in content

    # Check for learning capture logic
    assert "learnings" in content.lower() or "capture" in content.lower()


def test_sync_conventions_command_structure(cookies):
    """Test the sync-conventions command structure."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    # Check sync module exists
    sync_module = result.project_path / "ai_conventions" / "sync.py"
    assert sync_module.exists()

    content = sync_module.read_text(encoding="utf-8")

    # Check main function
    assert "def sync_command(" in content or "def main(" in content

    # Check for sync logic
    assert "sync" in content.lower() or "install" in content.lower()


def test_cli_help_command(cookies):
    """Test that CLI provides help."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))

    # Import and test the CLI
    from ai_conventions.cli import main
    from click.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output


def test_cli_status_command_execution(cookies):
    """Test executing the status command."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": "claude,cursor",
        }
    )

    assert result.exit_code == 0

    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))

    # Import and test the CLI
    from ai_conventions.cli import main
    from click.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(main, ["status"])

    assert result.exit_code == 0
    # Should show something about installation status
    assert "claude" in result.output.lower() or "provider" in result.output.lower()


def test_cli_list_command_execution(cookies):
    """Test executing the list command."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "default_domains": "git,testing",
        }
    )

    assert result.exit_code == 0

    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))

    # Import and test the CLI
    from ai_conventions.cli import main
    from click.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(main, ["list"])

    assert result.exit_code == 0
    # Should list domains
    assert "git" in result.output or "testing" in result.output or "domain" in result.output.lower()


def test_commands_removed_when_learning_disabled(cookies):
    """Test that learning commands are removed when disabled."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_learning_capture": False,
        }
    )

    assert result.exit_code == 0

    # Check that capture-learning command is not in pyproject.toml
    pyproject = result.project_path / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")

    # Main CLI should still be there
    assert 'my-project = "ai_conventions.cli:main"' in content

    # But capture-learning should not be there
    assert "capture-learning" not in content


def test_cli_shell_completion_support(cookies):
    """Test that CLI supports shell completion."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    # Check CLI module for completion support
    cli_module = result.project_path / "ai_conventions" / "cli.py"
    content = cli_module.read_text(encoding="utf-8")

    # Click automatically provides completion support when using @click.group()
    assert "@click.group(" in content
