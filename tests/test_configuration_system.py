"""Test configuration management system."""


def test_config_module_created(cookies):
    """Test that config module is created."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    config_path = result.project_path / "ai_conventions" / "config.py"
    assert config_path.exists()

    content = config_path.read_text(encoding="utf-8")
    assert "class ConventionsConfig" in content
    assert "class ConfigManager" in content
    assert "pydantic" in content


def test_config_cli_module_created(cookies):
    """Test that config CLI module is created."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    config_cli_path = result.project_path / "ai_conventions" / "commands" / "config.py"
    assert config_cli_path.exists()

    content = config_cli_path.read_text(encoding="utf-8")
    assert "@click.command()" in content
    assert "def config_command" in content
    # Config command now handles show/set/reset functionality
    assert "--show" in content or "--set" in content


def test_config_cli_command_registered(cookies):
    """Test that config functionality is available as subcommand."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    # Config is now a subcommand of ai-conventions
    cli_path = result.project_path / "ai_conventions" / "cli.py"
    cli_content = cli_path.read_text(encoding="utf-8")

    # Check that config is imported and registered as subcommand
    assert "from .commands" in cli_content and "config_command" in cli_content
    assert 'main.add_command(config_command, name="config")' in cli_content

    # Check that config command module exists
    config_cli_path = result.project_path / "ai_conventions" / "commands" / "config.py"
    assert config_cli_path.exists()


def test_config_dependencies_included(cookies):
    """Test that configuration dependencies are included."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    pyproject_path = result.project_path / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")

    assert "pydantic" in content
    # YAML-only now, tomli dependencies removed
    assert "PyYAML" in content or "pyyaml" in content


def test_install_py_uses_config_manager(cookies):
    """Test that install.py uses ConfigManager."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    install_path = result.project_path / "install.py"
    content = install_path.read_text(encoding="utf-8")

    assert "from ai_conventions.config import ConfigManager" in content
    assert "self.config_manager = ConfigManager" in content
    assert "config_obj = self.config_manager.load_config()" in content


def test_config_formats_supported(cookies):
    """Test that YAML-only config format is supported."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    config_path = result.project_path / "ai_conventions" / "config.py"
    content = config_path.read_text(encoding="utf-8")

    # Check for YAML-only support
    assert ".yaml" in content
    assert ".yml" in content
    # TOML/JSON support removed
    assert 'CONFIG_EXTENSIONS = [".yaml", ".yml"]' in content


def test_config_migration_functionality(cookies):
    """Test configuration default creation functionality."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    config_path = result.project_path / "ai_conventions" / "config.py"
    content = config_path.read_text(encoding="utf-8")

    # Migration removed, only default creation
    assert "def create_default_config" in content
    assert "_load_yaml" in content
    assert "_save_yaml" in content
    # TOML/JSON migration removed
    assert "yaml.safe_load" in content


def test_config_validation_with_pydantic(cookies):
    """Test that configuration uses Pydantic validation."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    config_path = result.project_path / "ai_conventions" / "config.py"
    content = config_path.read_text(encoding="utf-8")

    # Check for Pydantic v2 syntax (with fallback support)
    assert "from pydantic import BaseModel" in content or "PYDANTIC_AVAILABLE" in content
    assert "@field_validator" in content or "@validator" in content  # Support both v1 and v2
    assert "validate_providers" in content
    assert "validate_slug" in content
