"""Test Claude provider integration."""


def test_claude_commands_included_when_provider_selected(cookies):
    """Test that Claude commands are included when Claude provider is selected."""
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
            "selected_providers": "cursor",
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


def test_claude_learning_capture_always_available(cookies):
    """Test that Claude learning capture is always available (improved UX)."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": False,  # Even when disabled, should be available
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None

    # Learning capture should always be available for better UX
    claude_dir = result.project_path / ".claude"
    commands_dir = result.project_path / "commands"
    assert claude_dir.exists()  # Claude config should exist since we selected Claude
    assert commands_dir.exists()  # Commands should always be available

    # Check specific learning capture files exist
    assert (claude_dir / "commands" / "capture-learning.md").exists()
    assert (commands_dir / "capture-learning.md").exists()


def test_claude_setup_docs_created(cookies):
    """Test that Claude setup documentation is created."""
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
    assert result.exception is None

    # Check Claude setup docs exist
    claude_setup = result.project_path / "docs" / "claude-setup.md"
    assert claude_setup.exists()
    assert "Claude Code Setup Guide" in claude_setup.read_text(encoding="utf-8")
