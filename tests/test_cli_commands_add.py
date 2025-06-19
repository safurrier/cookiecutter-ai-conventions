"""Test add command functionality."""

import sys
from pathlib import Path

import yaml
from click.testing import CliRunner


def test_add_command_basic_functionality(cookies):
    """Test that add command works with basic domain/file pattern."""
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
        # Create domains directory
        Path("domains").mkdir()

        # Test basic add command
        result_cmd = runner.invoke(main, ["add", "Use type hints", "--domain", "python"])

        assert result_cmd.exit_code == 0
        assert "Convention added" in result_cmd.output

        # Check file was created
        assert Path("domains/python/core.md").exists()
        content = Path("domains/python/core.md").read_text()
        assert "Use type hints" in content


def test_add_command_creates_domain_structure(cookies):
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
        result_cmd = runner.invoke(
            main, ["add", "Use pytest fixtures", "--domain", "python", "--file", "testing"]
        )

        assert result_cmd.exit_code == 0

        # Should create domains/python/testing.md
        assert Path("domains/python/testing.md").exists()

        # Should inform user what was created
        assert "Created" in result_cmd.output or "created" in result_cmd.output


def test_add_command_with_custom_file(cookies):
    """Test add command with custom file option."""
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
        Path("domains").mkdir()

        # Test with custom file
        result_cmd = runner.invoke(
            main, ["add", "Use semantic commit messages", "--domain", "git", "--file", "commits"]
        )

        assert result_cmd.exit_code == 0

        # Should create domains/git/commits.md
        assert Path("domains/git/commits.md").exists()
        content = Path("domains/git/commits.md").read_text()
        assert "Use semantic commit messages" in content


def test_add_command_with_category(cookies):
    """Test add command with category option."""
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
        Path("domains").mkdir()

        # Test with category
        result_cmd = runner.invoke(
            main,
            ["add", "Avoid global variables", "--domain", "python", "--category", "anti-pattern"],
        )

        assert result_cmd.exit_code == 0

        # Check category appears in file
        content = Path("domains/python/core.md").read_text()
        assert "anti-pattern" in content


def test_add_command_creates_log_entry(cookies):
    """Test that add command creates proper log entries."""
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
        Path("domains").mkdir()

        # Add a convention
        result_cmd = runner.invoke(main, ["add", "Test pattern", "--domain", "python"])

        assert result_cmd.exit_code == 0

        # Check log file was created
        assert Path(".ai-conventions-log.yaml").exists()

        # Check log content
        with open(".ai-conventions-log.yaml") as f:
            log_data = yaml.safe_load(f)

        assert len(log_data) == 1
        assert log_data[0]["pattern"] == "Test pattern"
        assert log_data[0]["domain"] == "python"
        assert log_data[0]["file"] == "core.md"


def test_add_command_appends_to_existing_file(cookies):
    """Test that add command appends to existing files."""
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
        # Create existing domain structure
        Path("domains/python").mkdir(parents=True)
        Path("domains/python/core.md").write_text("# Existing content\n")

        # Add a convention
        result_cmd = runner.invoke(main, ["add", "New pattern", "--domain", "python"])

        assert result_cmd.exit_code == 0

        # Check content was appended
        content = Path("domains/python/core.md").read_text()
        assert "Existing content" in content
        assert "New pattern" in content


def test_add_command_requires_domain(cookies):
    """Test that add command requires domain parameter."""
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
        # Test without domain - should fail
        result_cmd = runner.invoke(main, ["add", "Some pattern"])

        assert result_cmd.exit_code != 0
