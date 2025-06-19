"""Test UV-first CLI architecture."""


def test_pyproject_toml_created_with_cli_scripts(cookies):
    """Test that pyproject.toml is created with CLI entry points."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    # Check pyproject.toml exists
    pyproject_file = result.project_path / "pyproject.toml"
    assert pyproject_file.exists()

    # Check it contains the right content
    content = pyproject_file.read_text(encoding="utf-8")
    assert "[project]" in content
    assert 'name = "test-ai-conventions"' in content
    assert "[project.scripts]" in content
    assert 'ai-conventions = "ai_conventions.cli:main"' in content
    # No separate commands anymore - they're all subcommands
    assert 'capture-learning = "ai_conventions.capture:main"' not in content
    assert 'sync-conventions = "ai_conventions.sync:main"' not in content
    assert 'conventions-config = "ai_conventions.config_cli:main"' not in content


def test_cli_module_structure_created(cookies):
    """Test that CLI module structure is created."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    # Check module structure
    ai_conventions_dir = result.project_path / "ai_conventions"
    assert ai_conventions_dir.exists()
    assert ai_conventions_dir.is_dir()

    # Check __init__.py
    init_file = ai_conventions_dir / "__init__.py"
    assert init_file.exists()

    # Check cli.py
    cli_file = ai_conventions_dir / "cli.py"
    assert cli_file.exists()
    content = cli_file.read_text(encoding="utf-8")
    assert "import click" in content or "from click import" in content
    assert "def main(" in content

    # Check commands directory
    commands_dir = ai_conventions_dir / "commands"
    assert commands_dir.exists()
    assert commands_dir.is_dir()

    # Check command files
    add_file = commands_dir / "add.py"
    assert add_file.exists()

    remove_file = commands_dir / "remove.py"
    assert remove_file.exists()

    config_file = commands_dir / "config.py"
    assert config_file.exists()

    sync_file = commands_dir / "sync.py"
    assert sync_file.exists()


def test_cli_status_command_exists(cookies):
    """Test that CLI status command is implemented."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    # Check cli.py contains status command
    cli_file = result.project_path / "ai_conventions" / "cli.py"
    content = cli_file.read_text(encoding="utf-8")
    assert "@main.command()" in content or "@cli.command()" in content
    assert "def status(" in content
    assert "claude" in content.lower()


def test_add_command_structure(cookies):
    """Test add command accepts domain parameter."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    # Check add.py has proper CLI structure
    add_file = result.project_path / "ai_conventions" / "commands" / "add.py"
    content = add_file.read_text(encoding="utf-8")
    assert "import click" in content or "from click import" in content
    assert "@click.argument" in content or "@click.option" in content
    assert "--domain" in content or "'domain'" in content


def test_auto_sync_functionality_exists(cookies):
    """Test auto-sync functionality is implemented."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude,cursor",
        }
    )

    assert result.exit_code == 0

    # Check auto-sync.py has proper implementation (no user-facing sync command, auto-sync is built-in)
    sync_file = result.project_path / "ai_conventions" / "commands" / "sync.py"
    content = sync_file.read_text(encoding="utf-8")
    assert "def auto_sync(" in content
    assert "provider" in content.lower() or "sync" in content.lower()


def test_pyproject_includes_dependencies(cookies):
    """Test that pyproject.toml includes necessary dependencies."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    pyproject_file = result.project_path / "pyproject.toml"
    content = pyproject_file.read_text(encoding="utf-8")

    # Check dependencies
    assert "dependencies" in content
    assert "click" in content
    assert "rich" in content
    assert "pyyaml" in content or "PyYAML" in content


def test_legacy_scripts_removed_when_cli_enabled(cookies):
    """Test that old Python scripts are removed when CLI is enabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    # Old command scripts should not exist in root commands dir
    root_commands_dir = result.project_path / "commands"
    if root_commands_dir.exists():
        # If root commands dir exists, it should only have .md files
        py_files = list(root_commands_dir.glob("*.py"))
        assert len(py_files) == 0, "Legacy .py scripts should be removed"

    # But new commands should exist in ai_conventions/commands/
    new_commands_dir = result.project_path / "ai_conventions" / "commands"
    assert new_commands_dir.exists()
    assert (new_commands_dir / "add.py").exists()
    assert (new_commands_dir / "remove.py").exists()
    assert (new_commands_dir / "config.py").exists()
    assert (new_commands_dir / "sync.py").exists()
