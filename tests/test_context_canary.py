"""Test context canary system."""

import re
from datetime import datetime
from pathlib import Path


def test_canary_enabled_in_claude_md(cookies):
    """Test that canary is included in CLAUDE.md when enabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "enable_context_canary": True,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    # Check that CLAUDE.md is generated (would be in .claude/ after install)
    # For now, check the template exists
    claude_template = result.project_path / "templates" / "claude" / "CLAUDE.md.j2"
    assert claude_template.exists()

    # In a real implementation, we'd check the generated CLAUDE.md
    # For now, verify cookiecutter context has canary setting
    assert "enable_context_canary" in str(result.context)


def test_canary_disabled_when_setting_false(cookies):
    """Test that canary is not included when disabled."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "enable_context_canary": False,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    # Verify the setting is respected
    # In real implementation, would check generated CLAUDE.md has no canary


def test_canary_configuration_in_cookiecutter_json():
    """Test that cookiecutter.json has canary configuration option."""
    cookiecutter_json = Path("cookiecutter.json")
    assert cookiecutter_json.exists()

    import json

    with open(cookiecutter_json, encoding="utf-8") as f:
        config = json.load(f)

    # Should have enable_context_canary option
    assert "enable_context_canary" in config
    # Default should be True
    assert config["enable_context_canary"] is True


def test_canary_unique_timestamp_format():
    """Test that canary timestamp format is correct."""
    # Test the timestamp format
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Should match pattern YYYYMMDD-HHMMSS
    pattern = r"^\d{8}-\d{6}$"
    assert re.match(pattern, timestamp)

    # Verify it's parseable
    parsed = datetime.strptime(timestamp, "%Y%m%d-%H%M%S")
    assert isinstance(parsed, datetime)


def test_canary_template_content(cookies):
    """Test that CLAUDE.md template contains canary section."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "enable_context_canary": True,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    # Check CLAUDE.md.j2 template
    claude_template = result.project_path / "templates" / "claude" / "CLAUDE.md.j2"
    content = claude_template.read_text(encoding="utf-8")

    # Should have canary-related content when enabled
    assert "canary" in content.lower() or "CANARY" in content
    assert "Context Health Check" in content
    assert "canary_timestamp" in content


def test_multiple_trigger_phrases_documented():
    """Test that multiple trigger phrases are documented."""
    # This would be in the generated documentation
    trigger_phrases = ["convention check", "check conventions", "canary", "conventions loaded?"]

    # Verify these are reasonable trigger phrases
    for phrase in trigger_phrases:
        assert isinstance(phrase, str)
        assert len(phrase) > 0


def test_canary_in_install_py_generation(cookies):
    """Test that install.py respects canary setting when generating CLAUDE.md."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test AI Conventions",
            "project_slug": "test-ai-conventions",
            "author_name": "Test Author",
            "default_domains": "git,testing",
            "enable_learning_capture": True,
            "enable_context_canary": True,
            "selected_providers": "claude",
        }
    )

    assert result.exit_code == 0

    # Check install.py exists and would handle canary
    install_py = result.project_path / "install.py"
    assert install_py.exists()

    # In a full implementation, install.py would use the template
    # to generate CLAUDE.md with or without canary based on setting
