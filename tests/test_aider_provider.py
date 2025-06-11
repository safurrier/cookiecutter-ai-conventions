"""Test Aider provider integration."""

import pytest
from pathlib import Path


def test_aider_creates_conventions_md_file(cookies):
    """Test that selecting Aider creates a CONVENTIONS.md file."""
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
    assert result.exception is None
    
    # Check CONVENTIONS.md exists
    conventions_file = result.project_path / "CONVENTIONS.md"
    assert conventions_file.exists()
    
    # Check content includes project info and domains
    content = conventions_file.read_text(encoding='utf-8')
    assert "# Coding Standards" in content
    assert "Test AI Conventions" in content
    assert "git" in content.lower()
    assert "testing" in content.lower()


def test_aider_creates_conf_yml_file(cookies):
    """Test that selecting Aider creates .aider.conf.yml file."""
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
    
    # Check .aider.conf.yml exists
    conf_file = result.project_path / ".aider.conf.yml"
    assert conf_file.exists()
    
    # Check content references CONVENTIONS.md
    content = conf_file.read_text(encoding='utf-8')
    assert "read: CONVENTIONS.md" in content or "read-only: CONVENTIONS.md" in content


def test_aider_conventions_includes_all_domains(cookies):
    """Test that CONVENTIONS.md includes all selected domains."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing,writing",
            "enable_learning_capture": True,
            "selected_providers": "aider"
        }
    )
    
    assert result.exit_code == 0
    
    conventions_file = result.project_path / "CONVENTIONS.md"
    content = conventions_file.read_text(encoding='utf-8')
    
    # Check git conventions
    assert "## Git Conventions" in content or "## Version Control" in content
    assert "conventional commits" in content.lower() or "commit format" in content.lower()
    
    # Check testing conventions
    assert "## Testing" in content
    assert "pytest" in content.lower()
    
    # Check writing conventions
    assert "## Documentation" in content or "## Writing" in content
    assert "docstrings" in content.lower() or "documentation" in content.lower()


def test_aider_conf_yml_includes_extra_read_files(cookies):
    """Test that .aider.conf.yml includes domain files when configured."""
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
    
    conf_file = result.project_path / ".aider.conf.yml"
    content = conf_file.read_text(encoding='utf-8')
    
    # Should list CONVENTIONS.md and potentially domain files
    assert "CONVENTIONS.md" in content
    # Optionally could include: domains/git/core.md, etc.


def test_aider_not_selected_no_files_created(cookies):
    """Test that Aider files are not created when not selected."""
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
    
    # Check no Aider files exist
    assert not (result.project_path / "CONVENTIONS.md").exists()
    assert not (result.project_path / ".aider.conf.yml").exists()


def test_aider_setup_documentation_created(cookies):
    """Test that Aider setup documentation is created."""
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
    
    # Check Aider setup docs exist
    aider_docs = result.project_path / "docs" / "aider-setup.md"
    assert aider_docs.exists()
    content = aider_docs.read_text(encoding='utf-8')
    assert "Aider Setup Guide" in content
    assert "CONVENTIONS.md" in content
    assert ".aider.conf.yml" in content
    assert "--read" in content


def test_aider_learning_capture_integration(cookies):
    """Test that learning capture is mentioned when enabled."""
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
    
    # Check CONVENTIONS.md mentions learning capture
    conventions_file = result.project_path / "CONVENTIONS.md"
    content = conventions_file.read_text(encoding='utf-8')
    assert "staging/learnings.md" in content or "Learning Capture" in content
    
    # Check .aider.conf.yml might include staging/learnings.md
    conf_file = result.project_path / ".aider.conf.yml"
    content = conf_file.read_text(encoding='utf-8')
    # Could optionally include staging/learnings.md in read list


def test_aider_without_learning_capture(cookies):
    """Test Aider configuration when learning capture is disabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": False,
            "selected_providers": "aider"
        }
    )
    
    assert result.exit_code == 0
    
    # Check no learning capture mentions
    conventions_file = result.project_path / "CONVENTIONS.md"
    content = conventions_file.read_text(encoding='utf-8')
    assert "capture-learning" not in content
    assert "staging/learnings" not in content