"""Test Windsurf provider integration."""

import pytest
from pathlib import Path


def test_windsurf_creates_windsurfrules_file(cookies):
    """Test that selecting Windsurf creates a .windsurfrules file."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "windsurf"
        }
    )
    
    assert result.exit_code == 0
    assert result.exception is None
    
    # Check .windsurfrules exists
    windsurfrules_file = result.project_path / ".windsurfrules"
    assert windsurfrules_file.exists()
    
    # Check content includes project info and domains
    content = windsurfrules_file.read_text()
    assert "# AI Development Conventions" in content
    assert "Test AI Conventions" in content
    assert "git" in content
    assert "testing" in content


def test_windsurf_creates_rules_directory_structure(cookies):
    """Test that selecting Windsurf creates .windsurf/rules/ structure."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "windsurf"
        }
    )
    
    assert result.exit_code == 0
    
    # Check .windsurf/rules directory exists
    windsurf_rules_dir = result.project_path / ".windsurf" / "rules"
    assert windsurf_rules_dir.exists()
    assert windsurf_rules_dir.is_dir()
    
    # Check for rule files
    main_rules = windsurf_rules_dir / "main.md"
    assert main_rules.exists()


def test_windsurf_domain_specific_rules_with_globs(cookies):
    """Test that domain-specific rules include glob patterns."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing,writing",
            "enable_learning_capture": True,
            "selected_providers": "windsurf"
        }
    )
    
    assert result.exit_code == 0
    
    windsurf_rules_dir = result.project_path / ".windsurf" / "rules"
    
    # Check git rules with glob patterns
    git_rules = windsurf_rules_dir / "git.md"
    assert git_rules.exists()
    content = git_rules.read_text()
    assert '[glob: "**/.git*", "**/COMMIT_*"]' in content
    assert "conventional commits" in content.lower()
    
    # Check testing rules with glob patterns
    testing_rules = windsurf_rules_dir / "testing.md"
    assert testing_rules.exists()
    content = testing_rules.read_text()
    assert '**/test_*.py' in content and '**/*_test.py' in content and '**/tests/**' in content
    assert "pytest" in content.lower()


def test_windsurf_character_limit_awareness(cookies):
    """Test that generated files respect Windsurf's character limits."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing,writing",
            "enable_learning_capture": True,
            "selected_providers": "windsurf"
        }
    )
    
    assert result.exit_code == 0
    
    windsurf_rules_dir = result.project_path / ".windsurf" / "rules"
    
    # Check that individual rule files are under 6000 characters
    for rule_file in windsurf_rules_dir.glob("*.md"):
        content = rule_file.read_text()
        assert len(content) < 6000, f"{rule_file.name} exceeds 6000 character limit"


def test_windsurf_not_selected_no_files_created(cookies):
    """Test that Windsurf files are not created when not selected."""
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
    
    # Check no Windsurf files exist
    assert not (result.project_path / ".windsurfrules").exists()
    assert not (result.project_path / ".windsurf").exists()


def test_windsurf_setup_documentation_created(cookies):
    """Test that Windsurf setup documentation is created."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "windsurf"
        }
    )
    
    assert result.exit_code == 0
    
    # Check Windsurf setup docs exist
    windsurf_docs = result.project_path / "docs" / "windsurf-setup.md"
    assert windsurf_docs.exists()
    content = windsurf_docs.read_text()
    assert "Windsurf Setup Guide" in content
    assert ".windsurfrules" in content
    assert ".windsurf/rules" in content
    assert "character limit" in content.lower()


def test_windsurf_learning_capture_integration(cookies):
    """Test that learning capture mentions are included when enabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "windsurf"
        }
    )
    
    assert result.exit_code == 0
    
    # Check main rules mention learning capture
    main_rules = result.project_path / ".windsurf" / "rules" / "main.md"
    content = main_rules.read_text()
    assert "staging/learnings.md" in content
    assert "capture-learning" in content
    
    # Check .windsurfrules also mentions it
    windsurfrules = result.project_path / ".windsurfrules"
    content = windsurfrules.read_text()
    assert "Learning System" in content


def test_windsurf_without_learning_capture(cookies):
    """Test Windsurf rules when learning capture is disabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": False,
            "selected_providers": "windsurf"
        }
    )
    
    assert result.exit_code == 0
    
    # Check no learning capture mentions
    windsurfrules = result.project_path / ".windsurfrules"
    content = windsurfrules.read_text()
    assert "capture-learning" not in content
    assert "staging/learnings" not in content