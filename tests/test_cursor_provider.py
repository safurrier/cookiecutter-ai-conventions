"""Test Cursor provider integration."""



def test_cursor_creates_legacy_cursorrules_file(cookies):
    """Test that selecting Cursor creates a .cursorrules file."""
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

    # Check .cursorrules exists
    cursorrules_file = result.project_path / ".cursorrules"
    assert cursorrules_file.exists()

    # Check content includes domain references
    content = cursorrules_file.read_text(encoding='utf-8')
    assert "# AI Development Conventions" in content
    assert "git" in content
    assert "testing" in content


def test_cursor_creates_modern_mdc_structure(cookies):
    """Test that selecting Cursor creates modern .cursor/rules/ structure."""
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

    # Check .cursor/rules directory exists
    cursor_rules_dir = result.project_path / ".cursor" / "rules"
    assert cursor_rules_dir.exists()
    assert cursor_rules_dir.is_dir()

    # Check for MDC files
    main_rules = cursor_rules_dir / "main.mdc"
    assert main_rules.exists()

    # Check MDC content has proper format
    content = main_rules.read_text(encoding='utf-8')
    assert "---" in content  # MDC metadata delimiter
    assert "description:" in content
    assert "# AI Development Conventions" in content


def test_cursor_mdc_files_have_correct_metadata(cookies):
    """Test that MDC files have proper metadata."""
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

    # Check main.mdc metadata
    main_rules = result.project_path / ".cursor" / "rules" / "main.mdc"
    content = main_rules.read_text(encoding='utf-8')

    # Should have metadata section
    assert content.startswith("---")
    assert "description: AI development conventions for Test AI Conventions" in content
    assert "alwaysApply: true" in content

    # Should reference domain files
    assert "@domains/git/core.md" in content
    assert "@domains/testing/core.md" in content


def test_cursor_not_selected_no_files_created(cookies):
    """Test that Cursor files are not created when not selected."""
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

    # Check no Cursor files exist
    assert not (result.project_path / ".cursorrules").exists()
    assert not (result.project_path / ".cursor").exists()


def test_cursor_setup_documentation_created(cookies):
    """Test that Cursor setup documentation is created."""
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

    # Check Cursor setup docs exist
    cursor_docs = result.project_path / "docs" / "cursor-setup.md"
    assert cursor_docs.exists()
    assert "Cursor Setup Guide" in cursor_docs.read_text(encoding='utf-8')
    assert ".cursorrules" in cursor_docs.read_text(encoding='utf-8')
    assert ".cursor/rules" in cursor_docs.read_text(encoding='utf-8')


def test_cursor_multiple_domains_creates_separate_mdc_files(cookies):
    """Test that multiple domains create separate MDC files."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing,writing",
            "enable_learning_capture": True,
            "selected_providers": "cursor"
        }
    )

    assert result.exit_code == 0

    cursor_rules_dir = result.project_path / ".cursor" / "rules"

    # Check for domain-specific MDC files
    assert (cursor_rules_dir / "git.mdc").exists()
    assert (cursor_rules_dir / "testing.mdc").exists()
    assert (cursor_rules_dir / "writing.mdc").exists()

    # Check git.mdc content
    git_content = (cursor_rules_dir / "git.mdc").read_text(encoding='utf-8')
    assert "Git Conventions" in git_content
    assert "@domains/git/core.md" in git_content


def test_cursor_cursorrules_without_learning_capture(cookies):
    """Test .cursorrules content when learning capture is disabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": False,
            "selected_providers": "cursor"
        }
    )

    assert result.exit_code == 0

    cursorrules_file = result.project_path / ".cursorrules"
    content = cursorrules_file.read_text(encoding='utf-8')

    # Should not mention learning capture
    assert "capture-learning" not in content
    assert "staging/learnings" not in content
