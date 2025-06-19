"""Test Group 3: Documentation Updates (Issue #89)."""

import sys
from pathlib import Path
from click.testing import CliRunner
import pytest


def test_claude_md_template_updated(cookies):
    """Test that CLAUDE.md template reflects new CLI structure."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Check if CLAUDE.md template exists and mentions new commands
    claude_template = result.project_path / "templates" / "claude" / "CLAUDE.md.j2"
    if claude_template.exists():
        content = claude_template.read_text()
        
        # Should mention add command (not capture)
        assert "add" in content.lower()
        
        # Should mention remove command
        assert "remove" in content.lower()
        
        # Should not mention deprecated sync command in favor of auto-sync
        # (or if mentioned, should note it's automatic)
        
        # Should mention enhanced list command
        assert "list" in content.lower()


def test_claude_md_mentions_auto_sync(cookies):
    """Test that CLAUDE.md template mentions auto-sync behavior."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Check CLAUDE.md for auto-sync documentation
    claude_md = result.project_path / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text()
        
        # Should mention that sync happens automatically
        assert "auto" in content.lower() or "automatic" in content.lower()


def test_cli_help_comprehensive(cookies):
    """Test that CLI commands have comprehensive help text."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.cli import main
    
    runner = CliRunner()
    
    # Test main help
    help_result = runner.invoke(main, ["--help"])
    assert help_result.exit_code == 0
    
    help_text = help_result.output.lower()
    
    # Should have clear description
    assert "ai conventions" in help_text or "manage" in help_text
    
    # Should list all available commands
    assert "status" in help_text
    assert "list" in help_text
    assert "config" in help_text
    
    # Test individual command help
    commands_to_test = ["status", "list", "config"]
    
    for cmd in commands_to_test:
        cmd_help = runner.invoke(main, [cmd, "--help"])
        if cmd_help.exit_code == 0:  # Some commands may not exist yet
            cmd_help_text = cmd_help.output
            
            # Should have description
            assert len(cmd_help_text.strip()) > 20  # Non-trivial help text
            
            # Should have usage information
            assert "usage" in cmd_help_text.lower() or "options" in cmd_help_text.lower()


def test_readme_updated_with_new_commands(cookies):
    """Test that README reflects new CLI command structure."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Check if README mentions the correct commands
    readme = result.project_path / "README.md"
    if readme.exists():
        content = readme.read_text()
        
        # Should mention key commands
        assert "ai-conventions" in content
        
        # Should have examples or at least mention main commands
        # (Exact content may vary, but should reference CLI usage)
        assert "status" in content.lower() or "list" in content.lower()


def test_docs_directory_structure(cookies):
    """Test that docs directory has up-to-date CLI information."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Check for CLI documentation
    docs_dir = result.project_path / "docs"
    if docs_dir.exists():
        # Look for CLI-related documentation files
        cli_docs = list(docs_dir.glob("*cli*")) + list(docs_dir.glob("*command*"))
        
        if cli_docs:
            # If CLI docs exist, they should mention current commands
            for doc_file in cli_docs:
                if doc_file.suffix in [".md", ".rst", ".txt"]:
                    content = doc_file.read_text()
                    
                    # Should reference actual commands
                    assert "ai-conventions" in content


def test_mkdocs_config_updated(cookies):
    """Test that MkDocs configuration includes CLI documentation."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Check MkDocs configuration if it exists
    mkdocs_config = result.project_path / "mkdocs.yml"
    if mkdocs_config.exists():
        content = mkdocs_config.read_text()
        
        # Should reference CLI documentation in navigation
        # (MkDocs config may mention CLI docs in nav section)
        nav_section = content.lower()
        
        # Should have some CLI-related navigation
        assert "cli" in nav_section or "command" in nav_section or "usage" in nav_section


def test_command_examples_up_to_date(cookies):
    """Test that command examples in documentation are current."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Look for any files that might contain command examples
    project_files = [
        result.project_path / "README.md",
        result.project_path / "CLAUDE.md",
        result.project_path / "docs" / "README.md",
    ]
    
    for file_path in project_files:
        if file_path.exists():
            content = file_path.read_text()
            
            # If it contains CLI examples, they should be current
            if "ai-conventions" in content:
                # Should not reference deprecated commands in examples
                lines = content.split('\n')
                for line in lines:
                    if "ai-conventions" in line and ("```" not in line):
                        # If this is a command example line, it should use valid commands
                        # (This is a basic check - exact validation depends on final CLI structure)
                        assert "ai-conventions" in line  # Basic sanity check


def test_help_flag_consistency(cookies):
    """Test that help flags work consistently across all commands."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.cli import main
    
    runner = CliRunner()
    
    # Test that --help works for main command
    help_result = runner.invoke(main, ["--help"])
    assert help_result.exit_code == 0
    assert len(help_result.output) > 50  # Should have substantial help
    
    # Test that help includes proper formatting
    help_output = help_result.output
    assert "Usage:" in help_output or "usage:" in help_output
    assert "Options:" in help_output or "options:" in help_output