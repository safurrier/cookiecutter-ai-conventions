"""Test remove command functionality."""

import sys
from pathlib import Path

import yaml
from click.testing import CliRunner


def test_remove_command_removes_last_entry_by_default(cookies):
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
                "target_file": "domains/python/core.md",
            },
            {
                "timestamp": "2024-01-01 13:00:00",
                "domain": "python",
                "file": "core.md",
                "category": "pattern",
                "pattern": "Latest pattern",
                "target_file": "domains/python/core.md",
            },
        ]
        Path(".ai-conventions-log.yaml").write_text(yaml.dump(log_data))

        # Remove should remove the latest entry
        result_cmd = runner.invoke(main, ["remove"])

        assert result_cmd.exit_code == 0
        assert "Removed" in result_cmd.output or "removed" in result_cmd.output

        # Log should have one less entry
        updated_log = yaml.safe_load(Path(".ai-conventions-log.yaml").read_text())
        assert len(updated_log) == 1
        assert updated_log[0]["pattern"] == "Old pattern"


def test_remove_command_removes_multiple_entries(cookies):
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
            {
                "timestamp": "2024-01-01 10:00:00",
                "pattern": "Entry 1",
                "domain": "python",
                "file": "core.md",
                "category": "pattern",
                "target_file": "domains/python/core.md",
            },
            {
                "timestamp": "2024-01-01 11:00:00",
                "pattern": "Entry 2",
                "domain": "python",
                "file": "core.md",
                "category": "pattern",
                "target_file": "domains/python/core.md",
            },
            {
                "timestamp": "2024-01-01 12:00:00",
                "pattern": "Entry 3",
                "domain": "python",
                "file": "core.md",
                "category": "pattern",
                "target_file": "domains/python/core.md",
            },
        ]
        Path(".ai-conventions-log.yaml").write_text(yaml.dump(log_data))

        # Remove last 2 entries
        result_cmd = runner.invoke(main, ["remove", "2"])

        assert result_cmd.exit_code == 0

        # Should have 1 entry left
        updated_log = yaml.safe_load(Path(".ai-conventions-log.yaml").read_text())
        assert len(updated_log) == 1
        assert updated_log[0]["pattern"] == "Entry 1"


def test_remove_command_handles_empty_log(cookies):
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
        assert (
            "nothing to remove" in result_cmd.output.lower() or "empty" in result_cmd.output.lower()
        )


def test_remove_command_handles_no_log_file(cookies):
    """Test graceful handling when no log file exists."""
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
        assert "no learning log found" in result_cmd.output.lower()


def test_remove_command_handles_excessive_count(cookies):
    """Test handling when trying to remove more entries than exist."""
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
        # Create log with only 2 entries
        log_data = [
            {
                "timestamp": "2024-01-01 10:00:00",
                "pattern": "Entry 1",
                "domain": "python",
                "file": "core.md",
                "category": "pattern",
                "target_file": "domains/python/core.md",
            },
            {
                "timestamp": "2024-01-01 11:00:00",
                "pattern": "Entry 2",
                "domain": "python",
                "file": "core.md",
                "category": "pattern",
                "target_file": "domains/python/core.md",
            },
        ]
        Path(".ai-conventions-log.yaml").write_text(yaml.dump(log_data))

        # Try to remove 5 entries
        result_cmd = runner.invoke(main, ["remove", "5"])

        assert result_cmd.exit_code == 0
        assert "Only" in result_cmd.output and "available" in result_cmd.output

        # Should remove all entries
        updated_log = yaml.safe_load(Path(".ai-conventions-log.yaml").read_text())
        assert len(updated_log) == 0


def test_remove_command_validates_positive_count(cookies):
    """Test that remove command validates positive count."""
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
        # Create a log file
        log_data = [
            {
                "timestamp": "2024-01-01 10:00:00",
                "pattern": "Entry 1",
                "domain": "python",
                "file": "core.md",
                "category": "pattern",
                "target_file": "domains/python/core.md",
            }
        ]
        Path(".ai-conventions-log.yaml").write_text(yaml.dump(log_data))

        # Try to remove 0 or negative entries
        result_cmd = runner.invoke(main, ["remove", "0"])

        assert result_cmd.exit_code == 0
        assert "must be positive" in result_cmd.output.lower()


def test_remove_command_shows_removed_entries(cookies):
    """Test that remove command shows what was removed."""
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
        log_data = [
            {
                "timestamp": "2024-01-01 10:00:00",
                "pattern": "Test pattern for removal",
                "domain": "python",
                "file": "core.md",
                "category": "pattern",
                "target_file": "domains/python/core.md",
            }
        ]
        Path(".ai-conventions-log.yaml").write_text(yaml.dump(log_data))

        # Remove entry
        result_cmd = runner.invoke(main, ["remove"])

        assert result_cmd.exit_code == 0
        assert "Test pattern for removal" in result_cmd.output
        assert "python/core.md" in result_cmd.output
