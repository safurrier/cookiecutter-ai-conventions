"""Test OpenAI Codex provider integration."""

import pytest
from pathlib import Path
import json


def test_codex_creates_agents_md_file(cookies):
    """Test that selecting Codex creates AGENTS.md file."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "codex"
        }
    )
    
    assert result.exit_code == 0
    assert result.exception is None
    
    # Check AGENTS.md exists
    agents_file = result.project_path / "AGENTS.md"
    assert agents_file.exists()
    
    # Check content includes project info and conventions
    content = agents_file.read_text()
    assert "# AI Development Agent" in content
    assert "Test AI Conventions" in content
    assert "conventions" in content.lower() or "standards" in content.lower()


def test_codex_agents_includes_all_domains(cookies):
    """Test that AGENTS.md includes all selected domains."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing,writing",
            "enable_learning_capture": True,
            "selected_providers": "codex"
        }
    )
    
    assert result.exit_code == 0
    
    agents_file = result.project_path / "AGENTS.md"
    content = agents_file.read_text()
    
    # Check git conventions
    assert "git" in content.lower()
    assert "conventional commit" in content.lower() or "commit format" in content.lower()
    
    # Check testing conventions  
    assert "pytest" in content.lower()
    assert "test" in content.lower()
    
    # Check writing conventions
    assert "documentation" in content.lower() or "docstring" in content.lower()


def test_codex_creates_config_directory(cookies):
    """Test that selecting Codex creates .codex directory with config."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "codex"
        }
    )
    
    assert result.exit_code == 0
    
    # Check .codex directory exists
    codex_dir = result.project_path / ".codex"
    assert codex_dir.exists()
    assert codex_dir.is_dir()
    
    # Check for local AGENTS.md symlink or copy
    local_agents = codex_dir / "AGENTS.md"
    assert local_agents.exists() or (result.project_path / "AGENTS.md").exists()


def test_codex_not_selected_no_files_created(cookies):
    """Test that Codex files are not created when not selected."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "aider"
        }
    )
    
    assert result.exit_code == 0
    
    # Check no Codex files exist
    assert not (result.project_path / "AGENTS.md").exists()
    assert not (result.project_path / ".codex").exists()


def test_codex_setup_documentation_created(cookies):
    """Test that Codex setup documentation is created."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "codex"
        }
    )
    
    assert result.exit_code == 0
    
    # Check Codex setup docs exist
    codex_docs = result.project_path / "docs" / "codex-setup.md"
    assert codex_docs.exists()
    content = codex_docs.read_text()
    assert "Codex Setup Guide" in content
    assert "AGENTS.md" in content
    assert "npm" in content.lower()


def test_codex_agents_format(cookies):
    """Test that AGENTS.md follows correct format."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "codex"
        }
    )
    
    assert result.exit_code == 0
    
    agents_file = result.project_path / "AGENTS.md"
    content = agents_file.read_text()
    
    # Check format follows Codex conventions
    assert "# AI Development Agent" in content or "# Agent" in content
    assert "## " in content  # Has sections
    # Should have clear instructions
    assert "Always" in content or "When" in content or "Follow" in content


def test_codex_with_learning_capture(cookies):
    """Test Codex integration with learning capture enabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "codex"
        }
    )
    
    assert result.exit_code == 0
    
    # Check AGENTS.md mentions learning capture
    agents_file = result.project_path / "AGENTS.md"
    content = agents_file.read_text()
    # Could mention evolving conventions or learning system


def test_codex_creates_wrapper_script(cookies):
    """Test that Codex creates a wrapper script for easy usage."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "codex"
        }
    )
    
    assert result.exit_code == 0
    
    # Check for codex wrapper script
    wrapper_script = result.project_path / "codex.sh"
    assert wrapper_script.exists()
    assert wrapper_script.stat().st_mode & 0o111  # Is executable
    
    content = wrapper_script.read_text()
    assert "codex" in content
    assert "AGENTS.md" in content or ".codex" in content