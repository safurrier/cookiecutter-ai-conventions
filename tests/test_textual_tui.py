"""Test Textual TUI functionality."""

import pytest
from pathlib import Path


def test_tui_module_created(cookies):
    """Test that TUI module is created."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )
    
    assert result.exit_code == 0
    
    tui_path = result.project_path / "ai_conventions" / "tui.py"
    assert tui_path.exists()
    
    content = tui_path.read_text()
    assert "from textual import" in content
    assert "class ConventionsTUI" in content
    assert "class InstallScreen" in content


def test_install_py_has_tui_support(cookies):
    """Test that install.py supports --tui flag."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )
    
    assert result.exit_code == 0
    
    install_path = result.project_path / "install.py"
    content = install_path.read_text()
    
    assert '--tui' in content
    assert 'from ai_conventions.tui import run_tui' in content


def test_textual_dependency_included(cookies):
    """Test that Textual is included in dependencies."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
        }
    )
    
    assert result.exit_code == 0
    
    pyproject_path = result.project_path / "pyproject.toml"
    content = pyproject_path.read_text()
    
    assert "textual" in content.lower()


def test_tui_provider_selection(cookies):
    """Test that TUI includes provider selection."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": ["claude", "cursor"],
        }
    )
    
    assert result.exit_code == 0
    
    tui_path = result.project_path / "ai_conventions" / "tui.py"
    content = tui_path.read_text()
    
    # Check for provider selection UI
    assert "Select AI Tool Providers" in content
    assert "Checkbox" in content
    assert "AVAILABLE_PROVIDERS" in content


def test_tui_configuration_options(cookies):
    """Test that TUI includes configuration options."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_learning_capture": True,
            "enable_context_canary": True,
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    tui_path = result.project_path / "ai_conventions" / "tui.py"
    content = tui_path.read_text()
    
    # Check for configuration options
    assert "Enable Learning Capture" in content
    assert "Enable Context Canary" in content
    assert "Enable Domain Composition" in content