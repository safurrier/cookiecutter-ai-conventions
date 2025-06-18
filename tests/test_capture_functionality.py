"""Test capture command functionality."""

import os
import sys

import yaml
from click.testing import CliRunner


def test_capture_defaults_to_core_md(cookies):
    """Test that capture defaults to core.md when no --file specified."""
    bake_result = cookies.bake(
        extra_context={
            "project_slug": "test-capture",
            "enable_learning_capture": True,
        }
    )

    assert bake_result.exit_code == 0

    # Add the project to Python path
    sys.path.insert(0, str(bake_result.project_path))

    # Create domains directory
    domains_dir = bake_result.project_path / "domains"
    domains_dir.mkdir(exist_ok=True)

    # Change to project directory for the command
    original_cwd = os.getcwd()
    os.chdir(bake_result.project_path)

    try:
        from ai_conventions.capture import capture_command

        runner = CliRunner()
        cli_result = runner.invoke(capture_command, ["Always use type hints", "--domain", "python"])

        assert cli_result.exit_code == 0

        # Check that it went to core.md
        core_file = domains_dir / "python" / "core.md"
        assert core_file.exists()

        content = core_file.read_text()
        assert "Always use type hints" in content
        assert "pattern" in content  # default category

    finally:
        os.chdir(original_cwd)
        if str(bake_result.project_path) in sys.path:
            sys.path.remove(str(bake_result.project_path))


def test_capture_with_specific_file(cookies):
    """Test capture with --file option."""
    bake_result = cookies.bake(
        extra_context={
            "project_slug": "test-capture",
            "enable_learning_capture": True,
        }
    )

    assert bake_result.exit_code == 0

    sys.path.insert(0, str(bake_result.project_path))
    domains_dir = bake_result.project_path / "domains"
    domains_dir.mkdir(exist_ok=True)

    original_cwd = os.getcwd()
    os.chdir(bake_result.project_path)

    try:
        from ai_conventions.capture import capture_command

        runner = CliRunner()
        cli_result = runner.invoke(
            capture_command,
            ["Use semantic commit messages", "--domain", "git", "--file", "commits"],
        )

        assert cli_result.exit_code == 0

        # Check that it went to commits.md
        commits_file = domains_dir / "git" / "commits.md"
        assert commits_file.exists()

        content = commits_file.read_text()
        assert "Use semantic commit messages" in content

    finally:
        os.chdir(original_cwd)
        if str(bake_result.project_path) in sys.path:
            sys.path.remove(str(bake_result.project_path))


def test_capture_with_nested_file_path(cookies):
    """Test capture with nested file path like pr-summaries/guidelines."""
    bake_result = cookies.bake(
        extra_context={
            "project_slug": "test-capture",
            "enable_learning_capture": True,
        }
    )

    assert bake_result.exit_code == 0

    sys.path.insert(0, str(bake_result.project_path))
    domains_dir = bake_result.project_path / "domains"
    domains_dir.mkdir(exist_ok=True)

    original_cwd = os.getcwd()
    os.chdir(bake_result.project_path)

    try:
        from ai_conventions.capture import capture_command

        runner = CliRunner()
        cli_result = runner.invoke(
            capture_command,
            ["Keep PRs focused and small", "--domain", "git", "--file", "pr-summaries/guidelines"],
        )

        assert cli_result.exit_code == 0

        # Check that nested directory was created
        nested_file = domains_dir / "git" / "pr-summaries" / "guidelines.md"
        assert nested_file.exists()

        content = nested_file.read_text()
        assert "Keep PRs focused and small" in content

        # Check that parent directories were created
        assert (domains_dir / "git" / "pr-summaries").exists()

    finally:
        os.chdir(original_cwd)
        if str(bake_result.project_path) in sys.path:
            sys.path.remove(str(bake_result.project_path))


def test_capture_creates_central_log(cookies):
    """Test that captures are logged to central .ai-conventions-log.yaml."""
    bake_result = cookies.bake(
        extra_context={
            "project_slug": "test-capture",
            "enable_learning_capture": True,
        }
    )

    assert bake_result.exit_code == 0

    sys.path.insert(0, str(bake_result.project_path))
    domains_dir = bake_result.project_path / "domains"
    domains_dir.mkdir(exist_ok=True)

    original_cwd = os.getcwd()
    os.chdir(bake_result.project_path)

    try:
        from ai_conventions.capture import capture_command

        runner = CliRunner()
        cli_result = runner.invoke(
            capture_command,
            [
                "Test logging functionality",
                "--domain",
                "testing",
                "--file",
                "strategies",
                "--category",
                "pattern",
            ],
        )

        assert cli_result.exit_code == 0

        # Check that central log was created
        log_file = bake_result.project_path / ".ai-conventions-log.yaml"
        assert log_file.exists()

        # Check log content
        with open(log_file) as f:
            logs = yaml.safe_load(f)

        assert len(logs) == 1
        log_entry = logs[0]

        assert log_entry["domain"] == "testing"
        assert log_entry["file"] == "strategies.md"
        assert log_entry["category"] == "pattern"
        assert log_entry["pattern"] == "Test logging functionality"
        assert "domains/testing/strategies.md" in log_entry["target_file"]
        assert "timestamp" in log_entry

    finally:
        os.chdir(original_cwd)
        if str(bake_result.project_path) in sys.path:
            sys.path.remove(str(bake_result.project_path))


def test_capture_auto_adds_md_extension(cookies):
    """Test that .md extension is automatically added to file names."""
    bake_result = cookies.bake(
        extra_context={
            "project_slug": "test-capture",
            "enable_learning_capture": True,
        }
    )

    assert bake_result.exit_code == 0

    sys.path.insert(0, str(bake_result.project_path))
    domains_dir = bake_result.project_path / "domains"
    domains_dir.mkdir(exist_ok=True)

    original_cwd = os.getcwd()
    os.chdir(bake_result.project_path)

    try:
        from ai_conventions.capture import capture_command

        runner = CliRunner()
        cli_result = runner.invoke(
            capture_command,
            [
                "Test auto extension",
                "--domain",
                "git",
                "--file",
                "workflows",  # No .md extension
            ],
        )

        assert cli_result.exit_code == 0

        # Check that .md was automatically added
        workflows_file = domains_dir / "git" / "workflows.md"
        assert workflows_file.exists()

        # Should not create a file without extension
        workflows_file_no_ext = domains_dir / "git" / "workflows"
        assert not workflows_file_no_ext.exists()

    finally:
        os.chdir(original_cwd)
        if str(bake_result.project_path) in sys.path:
            sys.path.remove(str(bake_result.project_path))
