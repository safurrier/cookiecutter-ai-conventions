"""Test Group 1: Auto-sync + Add/Remove Commands (Issues #86 + #87)."""

import sys
import tempfile
from pathlib import Path
from click.testing import CliRunner
import yaml
import pytest


def test_add_command_triggers_auto_sync(cookies):
    """Test that add command automatically syncs to all providers."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    # Create domains directory
    domains_dir = result.project_path / "domains" / "python"
    domains_dir.mkdir(parents=True, exist_ok=True)
    
    from ai_conventions.cli import main
    
    runner = CliRunner()
    
    # Test that add command exists and triggers auto-sync
    with runner.isolated_filesystem():
        # Create domains directory in isolated filesystem
        Path("domains").mkdir()
        
        # This should trigger auto-sync after adding
        result_cmd = runner.invoke(main, ["add", "Use type hints", "--domain", "python"])
        
        # Should succeed (when implemented)
        assert result_cmd.exit_code == 0
        
        # Should contain auto-sync message
        assert "auto-sync" in result_cmd.output.lower() or "synced" in result_cmd.output.lower()


def test_remove_command_triggers_auto_sync(cookies):
    """Test that remove command automatically syncs to all providers."""
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
    
    # Test that remove command exists and triggers auto-sync
    with runner.isolated_filesystem():
        # Create domains directory and log file
        Path("domains").mkdir()
        log_file = Path(".ai-conventions-log.yaml")
        log_file.write_text(yaml.dump([{
            "timestamp": "2024-01-01 12:00:00",
            "domain": "python",
            "file": "core.md",
            "category": "pattern",
            "pattern": "Use type hints",
            "target_file": "domains/python/core.md"
        }]))
        
        # This should trigger auto-sync after removing
        result_cmd = runner.invoke(main, ["remove"])
        
        # Should succeed (when implemented)
        assert result_cmd.exit_code == 0
        
        # Should contain auto-sync message
        assert "auto-sync" in result_cmd.output.lower() or "synced" in result_cmd.output.lower()


def test_add_command_replaces_capture(cookies):
    """Test that capture command is renamed to add."""
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
    
    # Test that add command works
    with runner.isolated_filesystem():
        Path("domains").mkdir()
        
        result_cmd = runner.invoke(main, ["add", "Use type hints", "--domain", "python"])
        assert result_cmd.exit_code == 0
    
    # Test that capture command no longer exists
    result_capture = runner.invoke(main, ["capture", "test"])
    assert result_capture.exit_code != 0  # Should fail - command doesn't exist


def test_add_creates_domain_structure(cookies):
    """Test that add command creates domain structure automatically."""
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
    
    with runner.isolated_filesystem():
        # Start with no domains directory
        assert not Path("domains").exists()
        
        # Add should create the entire structure
        result_cmd = runner.invoke(main, ["add", "python/testing", "Use pytest fixtures"])
        
        assert result_cmd.exit_code == 0
        
        # Should create domains/python/testing.md
        assert Path("domains/python/testing.md").exists()
        
        # Should inform user what was created
        assert "created" in result_cmd.output.lower()


def test_add_handles_nested_structure(cookies):
    """Test that add command handles nested domain structures."""
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
    
    with runner.isolated_filesystem():
        # Add nested structure
        result_cmd = runner.invoke(main, ["add", "git/workflows/ci", "Use GitHub Actions"])
        
        assert result_cmd.exit_code == 0
        
        # Should create domains/git/workflows/ci.md
        assert Path("domains/git/workflows/ci.md").exists()
        
        # Content should be added
        content = Path("domains/git/workflows/ci.md").read_text()
        assert "Use GitHub Actions" in content


def test_remove_last_entry_by_default(cookies):
    """Test that remove command removes the last entry by default."""
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
    
    with runner.isolated_filesystem():
        # Create log with entries
        Path("domains/python").mkdir(parents=True)
        Path("domains/python/core.md").write_text("# Python\n\n## Test entry\nSome content\n")
        
        log_data = [
            {
                "timestamp": "2024-01-01 12:00:00",
                "domain": "python", 
                "file": "core.md",
                "category": "pattern",
                "pattern": "Old pattern",
                "target_file": "domains/python/core.md"
            },
            {
                "timestamp": "2024-01-01 13:00:00",
                "domain": "python",
                "file": "core.md", 
                "category": "pattern",
                "pattern": "Latest pattern",
                "target_file": "domains/python/core.md"
            }
        ]
        Path(".ai-conventions-log.yaml").write_text(yaml.dump(log_data))
        
        # Remove should remove the latest entry
        result_cmd = runner.invoke(main, ["remove"])
        
        assert result_cmd.exit_code == 0
        assert "removed" in result_cmd.output.lower()
        
        # Log should have one less entry
        updated_log = yaml.safe_load(Path(".ai-conventions-log.yaml").read_text())
        assert len(updated_log) == 1
        assert updated_log[0]["pattern"] == "Old pattern"


def test_remove_multiple_entries(cookies):
    """Test that remove N removes the last N entries."""
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
    
    with runner.isolated_filesystem():
        # Create log with multiple entries
        log_data = [
            {"timestamp": "2024-01-01 10:00:00", "pattern": "Entry 1", "domain": "python", "file": "core.md", "category": "pattern", "target_file": "domains/python/core.md"},
            {"timestamp": "2024-01-01 11:00:00", "pattern": "Entry 2", "domain": "python", "file": "core.md", "category": "pattern", "target_file": "domains/python/core.md"},
            {"timestamp": "2024-01-01 12:00:00", "pattern": "Entry 3", "domain": "python", "file": "core.md", "category": "pattern", "target_file": "domains/python/core.md"},
        ]
        Path(".ai-conventions-log.yaml").write_text(yaml.dump(log_data))
        
        # Remove last 2 entries
        result_cmd = runner.invoke(main, ["remove", "2"])
        
        assert result_cmd.exit_code == 0
        
        # Should have 1 entry left
        updated_log = yaml.safe_load(Path(".ai-conventions-log.yaml").read_text())
        assert len(updated_log) == 1
        assert updated_log[0]["pattern"] == "Entry 1"


def test_remove_from_empty_log(cookies):
    """Test graceful handling when trying to remove from empty log."""
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
    
    with runner.isolated_filesystem():
        # No log file exists
        result_cmd = runner.invoke(main, ["remove"])
        
        assert result_cmd.exit_code == 0
        assert "nothing to remove" in result_cmd.output.lower() or "empty" in result_cmd.output.lower()


def test_sync_command_removed(cookies):
    """Test that sync command is removed from CLI."""
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
    
    # Sync command should no longer exist
    result_cmd = runner.invoke(main, ["sync"])
    assert result_cmd.exit_code != 0  # Should fail - command doesn't exist
    
    # Help should not show sync command
    help_result = runner.invoke(main, ["--help"])
    assert help_result.exit_code == 0
    assert "sync" not in help_result.output.lower()