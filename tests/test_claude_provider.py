"""Test Claude provider integration."""

import pytest
from pathlib import Path


def test_claude_commands_included_when_provider_selected(cookies):
    """Test that Claude commands are included when Claude provider is selected."""
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
    assert result.exception is None
    
    # Check Claude commands exist
    claude_commands_dir = result.project_path / ".claude" / "commands"
    assert claude_commands_dir.exists()
    assert (claude_commands_dir / "capture-learning.md").exists()
    assert (claude_commands_dir / "review-learnings.md").exists()
    
    # Check Python commands are removed but directory still exists with .md files
    commands_dir = result.project_path / "commands"
    assert commands_dir.exists()
    # Python scripts should be removed
    assert not (commands_dir / "capture-learning.py").exists()
    assert not (commands_dir / "review-learnings.py").exists()
    # But .md files should remain
    assert (commands_dir / "capture-learning.md").exists()
    assert (commands_dir / "review-learnings.md").exists()


def test_claude_commands_removed_when_provider_not_selected(cookies):
    """Test that Claude commands are removed when Claude is not selected."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "cursor"
        }
    )
    
    assert result.exit_code == 0
    assert result.exception is None
    
    # Check Claude commands don't exist
    claude_dir = result.project_path / ".claude"
    assert not claude_dir.exists()
    
    # Check commands directory exists with .md files but no .py files
    commands_dir = result.project_path / "commands"
    assert commands_dir.exists()
    # Python scripts should be removed
    assert not (commands_dir / "capture-learning.py").exists()
    assert not (commands_dir / "review-learnings.py").exists()
    # But .md files should remain
    assert (commands_dir / "capture-learning.md").exists()
    assert (commands_dir / "review-learnings.md").exists()


def test_all_commands_removed_when_learning_disabled(cookies):
    """Test that all commands are removed when learning is disabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": False,
            "selected_providers": "claude"
        }
    )
    
    assert result.exit_code == 0
    assert result.exception is None
    
    # Check no command directories exist
    claude_dir = result.project_path / ".claude"
    commands_dir = result.project_path / "commands"
    assert not claude_dir.exists()
    assert not commands_dir.exists()


def test_claude_setup_docs_created(cookies):
    """Test that Claude setup documentation is created."""
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
    assert result.exception is None
    
    # Check Claude setup docs exist
    claude_setup = result.project_path / "docs" / "claude-setup.md"
    assert claude_setup.exists()
    assert "Claude Code Setup Guide" in claude_setup.read_text()