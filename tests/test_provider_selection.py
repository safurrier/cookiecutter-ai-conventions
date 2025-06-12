"""Test provider selection functionality."""

import json
from pathlib import Path

import pytest


def test_single_provider_selection(cookies):
    """Test that single provider selection works."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-single-provider",
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    assert result.exception is None
    
    # Check Claude provider exists
    claude_provider = result.project_path / "ai_conventions" / "providers" / "claude.py"
    assert claude_provider.exists()
    
    # Check that the provider module was not removed
    assert not (result.project_path / "ai_conventions" / "providers" / "cursor.py").exists()


def test_multiple_provider_selection(cookies):
    """Test that multiple provider selection with comma separation works."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-multi-provider",
            "selected_providers": "claude,cursor,windsurf",
        }
    )
    
    assert result.exit_code == 0
    assert result.exception is None
    
    # Check all selected providers exist
    providers_dir = result.project_path / "ai_conventions" / "providers"
    assert (providers_dir / "claude.py").exists()
    assert (providers_dir / "cursor.py").exists()
    assert (providers_dir / "windsurf.py").exists()
    
    # Check unselected providers are removed
    assert not (providers_dir / "aider.py").exists()
    assert not (providers_dir / "copilot.py").exists()


def test_provider_selection_with_spaces(cookies):
    """Test that provider selection handles spaces correctly."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-spaces",
            "selected_providers": "claude, cursor, windsurf",
        }
    )
    
    assert result.exit_code == 0
    
    # Should still work with spaces
    providers_dir = result.project_path / "ai_conventions" / "providers"
    assert (providers_dir / "claude.py").exists()
    assert (providers_dir / "cursor.py").exists()
    assert (providers_dir / "windsurf.py").exists()


def test_all_providers_selection(cookies):
    """Test selecting all providers."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-all",
            "selected_providers": "claude,cursor,windsurf,aider,copilot,codex",
        }
    )
    
    assert result.exit_code == 0
    
    # All providers should exist
    providers_dir = result.project_path / "ai_conventions" / "providers"
    for provider in ["claude", "cursor", "windsurf", "aider", "copilot", "codex"]:
        assert (providers_dir / f"{provider}.py").exists()


def test_empty_provider_selection(cookies):
    """Test what happens with no providers selected."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-none",
            "selected_providers": "",
        }
    )
    
    assert result.exit_code == 0
    
    # Base provider module should still exist
    providers_init = result.project_path / "ai_conventions" / "providers" / "__init__.py"
    assert providers_init.exists()
    
    # But no specific provider modules
    providers_dir = result.project_path / "ai_conventions" / "providers"
    provider_files = list(providers_dir.glob("*.py"))
    # Should only have __init__.py and base.py
    assert len(provider_files) <= 2


def test_invalid_provider_handled_gracefully(cookies):
    """Test that invalid provider names are ignored."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-invalid",
            "selected_providers": "claude,invalid_provider,cursor",
        }
    )
    
    assert result.exit_code == 0
    
    # Valid providers should still exist
    providers_dir = result.project_path / "ai_conventions" / "providers"
    assert (providers_dir / "claude.py").exists()
    assert (providers_dir / "cursor.py").exists()
    
    # Invalid provider should not exist
    assert not (providers_dir / "invalid_provider.py").exists()


def test_cookiecutter_json_format():
    """Test that cookiecutter.json has correct format."""
    cookiecutter_json = Path("cookiecutter.json")
    with open(cookiecutter_json, encoding='utf-8') as f:
        config = json.load(f)
    
    # selected_providers should be a string, not an array
    assert isinstance(config["selected_providers"], str)
    assert config["selected_providers"] == "claude"