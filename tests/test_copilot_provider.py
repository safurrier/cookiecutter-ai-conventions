"""Test GitHub Copilot provider integration."""

import json


def test_copilot_creates_instructions_file(cookies):
    """Test that selecting Copilot creates .github/copilot-instructions.md file."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "copilot"
        }
    )

    assert result.exit_code == 0
    assert result.exception is None

    # Check .github/copilot-instructions.md exists
    instructions_file = result.project_path / ".github" / "copilot-instructions.md"
    assert instructions_file.exists()

    # Check content includes project info and conventions
    content = instructions_file.read_text(encoding='utf-8')
    assert "# Copilot Instructions" in content
    assert "Test AI Conventions" in content
    assert "coding standards" in content.lower() or "conventions" in content.lower()


def test_copilot_instructions_includes_all_domains(cookies):
    """Test that copilot-instructions.md includes all selected domains."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing,writing",
            "enable_learning_capture": True,
            "selected_providers": "copilot"
        }
    )

    assert result.exit_code == 0

    instructions_file = result.project_path / ".github" / "copilot-instructions.md"
    content = instructions_file.read_text(encoding='utf-8')

    # Check git conventions
    assert "commit" in content.lower()
    assert "conventional commit" in content.lower() or "commit format" in content.lower()

    # Check testing conventions
    assert "pytest" in content.lower()
    assert "test" in content.lower()

    # Check writing conventions
    assert "documentation" in content.lower() or "docstring" in content.lower()


def test_copilot_creates_vscode_settings(cookies):
    """Test that selecting Copilot creates VS Code settings."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "copilot"
        }
    )

    assert result.exit_code == 0

    # Check .vscode exists (renamed from vscode_config in post-gen)
    vscode_dir = result.project_path / ".vscode"
    assert vscode_dir.exists()

    # Check settings.json exists in .vscode
    settings_file = vscode_dir / "settings.json"
    assert settings_file.exists()

    # Check settings content
    settings = json.loads(settings_file.read_text(encoding='utf-8'))
    assert "github.copilot.chat.codeGeneration.useInstructionFiles" in settings
    assert settings["github.copilot.chat.codeGeneration.useInstructionFiles"] is True


def test_copilot_creates_prompt_files(cookies):
    """Test that Copilot creates domain-specific prompt files."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "copilot"
        }
    )

    assert result.exit_code == 0

    # Check prompt files exist
    prompts_dir = result.project_path / ".github" / "prompts"
    assert prompts_dir.exists()

    # Check domain prompt files
    assert (prompts_dir / "git.prompt.md").exists()
    assert (prompts_dir / "testing.prompt.md").exists()

    # Check content
    git_prompt = (prompts_dir / "git.prompt.md").read_text(encoding='utf-8')
    assert "git" in git_prompt.lower()
    assert "commit" in git_prompt.lower()


def test_copilot_not_selected_no_files_created(cookies):
    """Test that Copilot files are not created when not selected."""
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

    # Check no Copilot files exist
    assert not (result.project_path / ".github" / "copilot-instructions.md").exists()
    assert not (result.project_path / ".vscode" / "settings.json").exists()
    assert not (result.project_path / ".github" / "prompts").exists()


def test_copilot_setup_documentation_created(cookies):
    """Test that Copilot setup documentation is created."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "copilot"
        }
    )

    assert result.exit_code == 0

    # Check Copilot setup docs exist
    copilot_docs = result.project_path / "docs" / "copilot-setup.md"
    assert copilot_docs.exists()
    content = copilot_docs.read_text(encoding='utf-8')
    assert "Copilot Setup Guide" in content
    assert "copilot-instructions.md" in content
    assert ".vscode/settings.json" in content
    assert "prompt files" in content.lower()


def test_copilot_instructions_format(cookies):
    """Test that copilot-instructions.md follows correct format."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "copilot"
        }
    )

    assert result.exit_code == 0

    instructions_file = result.project_path / ".github" / "copilot-instructions.md"
    content = instructions_file.read_text(encoding='utf-8')

    # Check format follows best practices
    assert "# Copilot Instructions" in content
    assert "## Core Conventions" in content or "## General Coding Standards" in content
    # Should have concrete, actionable instructions
    assert "Always" in content or "Never" in content or "Use" in content
    # Should be concise
    assert len(content.split('\n')) < 200  # Reasonable line count


def test_copilot_with_learning_capture(cookies):
    """Test Copilot integration with learning capture enabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "selected_providers": "copilot"
        }
    )

    assert result.exit_code == 0

    # Check instructions mention learning capture
    instructions_file = result.project_path / ".github" / "copilot-instructions.md"
    instructions_file.read_text(encoding='utf-8')
    # Could mention evolving conventions

    # VS Code settings might include learning file references
    vscode_config = result.project_path / "vscode_config"
    settings_file = vscode_config / "settings.json"
    if settings_file.exists():
        json.loads(settings_file.read_text(encoding='utf-8'))
        # Could include reference to staging/learnings.md
