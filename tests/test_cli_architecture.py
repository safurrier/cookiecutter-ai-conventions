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
            "selected_providers": "claude"
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
    assert 'capture-learning = "ai_conventions.capture:main"' in content
    assert 'sync-conventions = "ai_conventions.sync:main"' in content


def test_cli_module_structure_created(cookies):
    """Test that CLI module structure is created."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude"
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
    assert "def main()" in content

    # Check capture.py
    capture_file = ai_conventions_dir / "capture.py"
    assert capture_file.exists()

    # Check sync.py
    sync_file = ai_conventions_dir / "sync.py"
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
            "selected_providers": "claude"
        }
    )

    assert result.exit_code == 0

    # Check cli.py contains status command
    cli_file = result.project_path / "ai_conventions" / "cli.py"
    content = cli_file.read_text(encoding="utf-8")
    assert "@main.command()" in content or "@cli.command()" in content
    assert "def status(" in content
    assert "claude" in content.lower()


def test_capture_learning_command_structure(cookies):
    """Test capture-learning command accepts domain parameter."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude"
        }
    )

    assert result.exit_code == 0

    # Check capture.py has proper CLI structure
    capture_file = result.project_path / "ai_conventions" / "capture.py"
    content = capture_file.read_text(encoding="utf-8")
    assert "import click" in content or "from click import" in content
    assert "@click.argument" in content or "@click.option" in content
    assert "--domain" in content or "'domain'" in content


def test_sync_conventions_command_exists(cookies):
    """Test sync-conventions command is implemented."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude,cursor"
        }
    )

    assert result.exit_code == 0

    # Check sync.py has proper implementation
    sync_file = result.project_path / "ai_conventions" / "sync.py"
    content = sync_file.read_text(encoding="utf-8")
    assert "def main(" in content or "def sync_conventions(" in content
    assert "provider" in content.lower()


def test_pyproject_includes_dependencies(cookies):
    """Test that pyproject.toml includes necessary dependencies."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "claude"
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
            "selected_providers": "claude"
        }
    )

    assert result.exit_code == 0

    # Old command scripts should not exist
    commands_dir = result.project_path / "commands"
    if commands_dir.exists():
        # If commands dir exists, it should only have .md files
        py_files = list(commands_dir.glob("*.py"))
        assert len(py_files) == 0, "Legacy .py scripts should be removed"
