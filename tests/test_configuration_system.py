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

    config_cli_path = result.project_path / "ai_conventions" / "config_cli.py"
    assert config_cli_path.exists()

    content = config_cli_path.read_text(encoding="utf-8")
    assert "@click.group()" in content
    assert "def show" in content
    assert "def validate" in content
    assert "def migrate" in content


def test_config_cli_command_registered(cookies):
    """Test that conventions-config command is registered."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    pyproject_path = result.project_path / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")

    assert "conventions-config" in content
    assert "ai_conventions.config_cli:main" in content


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
    assert "tomli" in content
    assert "tomli-w" in content


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
    """Test that multiple config formats are supported."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    config_path = result.project_path / "ai_conventions" / "config.py"
    content = config_path.read_text(encoding="utf-8")

    # Check for format support
    assert ".yaml" in content
    assert ".toml" in content
    assert ".json" in content
    assert "pyproject.toml" in content


def test_config_migration_functionality(cookies):
    """Test configuration migration between formats."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )

    assert result.exit_code == 0

    config_path = result.project_path / "ai_conventions" / "config.py"
    content = config_path.read_text(encoding="utf-8")

    assert "def migrate_config" in content
    assert "_load_yaml" in content
    assert "_save_yaml" in content
    assert "_load_toml" in content
    assert "_save_toml" in content
    assert "_load_json" in content
    assert "_save_json" in content


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

    assert "from pydantic import BaseModel" in content
    assert "@validator" in content
    assert "validate_providers" in content
    assert "validate_slug" in content
