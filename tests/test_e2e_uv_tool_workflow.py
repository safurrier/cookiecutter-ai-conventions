"""End-to-end tests for UV tool workflow with cookiecutter generation.

This module tests the complete workflow from cookiecutter generation through
UV tool installation and command execution, addressing the gap where template
tests pass but real UV workflows fail.

Following the progressive testing approach:
- E2E: Complete generation → UV tool install → command execution
- Validation: Branch-based testing and real-world usage simulation
- Performance: Ensures operations complete within reasonable timeframes
"""

import subprocess
import sys
import time
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

# Performance thresholds based on 2025 UV best practices
PERFORMANCE_THRESHOLDS = {
    'generation': 30,    # 30s for cookiecutter generation
    'uv_install': 60,    # 60s for UV tool install
    'uv_command': 30,    # 30s for UV command execution
}


def monitor_performance(operation_name: str, threshold: float = None):
    """Decorator to monitor operation performance."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time

            max_duration = threshold or PERFORMANCE_THRESHOLDS.get(operation_name, 60)
            if duration > max_duration:
                pytest.fail(
                    f"{operation_name} took {duration:.2f}s, exceeding {max_duration}s threshold"
                )

            return result
        return wrapper
    return decorator


def safe_uv_tool_cleanup(tool_name: str):
    """Safely cleanup UV tool with proper error handling."""
    try:
        result = subprocess.run(
            ["uv", "tool", "uninstall", tool_name],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,  # OK if tool wasn't installed
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def generate_test_project(tmp_path: Path, project_name: str, project_slug: str, **extra_context):
    """Generate a test project with consistent setup."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    context = {
        "project_name": project_name,
        "project_slug": project_slug,
    }
    context.update(extra_context)

    start_time = time.time()
    project_dir = cookiecutter(
        str(Path.cwd()),
        no_input=True,
        output_dir=str(output_dir),
        extra_context=context,
    )
    generation_duration = time.time() - start_time

    # Performance check for generation
    if generation_duration > PERFORMANCE_THRESHOLDS['generation']:
        pytest.fail(f"Project generation took {generation_duration:.2f}s, exceeding threshold")

    return Path(project_dir)


class TestE2EUVToolWorkflow:
    """Test complete UV tool workflow from generation to execution."""

    @pytest.mark.slow
    def test_complete_uv_tool_workflow(self, tmp_path):
        """Test that generated project can be installed and used as UV tool.

        This is the core E2E test that should FAIL initially because:
        1. Template doesn't have proper UV tool configuration
        2. pyproject.toml missing [project.scripts] section
        3. No CLI entry point defined
        """
        # Arrange: Generate project with UV tool support
        generated_project = generate_test_project(
            tmp_path,
            "Test UV Tool",
            "test-uv-tool",
            enable_learning_capture=True,
        )
        tool_name = "test-uv-tool"

        try:
            # Act: Install as UV tool with performance monitoring
            start_time = time.time()
            install_result = subprocess.run(
                ["uv", "tool", "install", str(generated_project)],
                capture_output=True,
                text=True,
                timeout=PERFORMANCE_THRESHOLDS['uv_install'],
            )
            install_duration = time.time() - start_time

            # Assert: Tool installation succeeds
            assert install_result.returncode == 0, (
                f"UV tool install failed: {install_result.stderr}\n"
                f"Generated project: {generated_project}\n"
                f"Install duration: {install_duration:.2f}s"
            )

            # Performance check
            if install_duration > PERFORMANCE_THRESHOLDS['uv_install']:
                pytest.fail(f"UV install took {install_duration:.2f}s, exceeding threshold")

            # Assert: Tool is available via uv tool list
            list_result = subprocess.run(
                ["uv", "tool", "list"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            assert tool_name in list_result.stdout

        finally:
            # Cleanup: Always remove UV tool
            safe_uv_tool_cleanup(tool_name)

    @pytest.mark.slow
    def test_uv_tool_command_execution(self, tmp_path):
        """Test that UV tool commands execute successfully.

        This should FAIL initially because:
        1. CLI commands not properly configured
        2. Entry points missing or incorrect
        3. Command help/version not implemented
        """
        # Arrange: Generate and install UV tool
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_name": "Test Commands",
                "project_slug": "test-commands",
            },
        )

        generated_project = Path(project_dir)
        tool_name = "test-commands"

        try:
            # Install UV tool
            install_result = subprocess.run(
                ["uv", "tool", "install", str(generated_project)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            assert install_result.returncode == 0, f"Install failed: {install_result.stderr}"

            # Act & Assert: Test --help command
            help_result = subprocess.run(
                [tool_name, "--help"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            assert help_result.returncode == 0, f"Help command failed: {help_result.stderr}"
            assert "Usage:" in help_result.stdout or "usage:" in help_result.stdout

            # Act & Assert: Test --version command
            version_result = subprocess.run(
                [tool_name, "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            assert version_result.returncode == 0, f"Version command failed: {version_result.stderr}"
            assert "0.1.0" in version_result.stdout  # Default version from template

        finally:
            # Cleanup
            subprocess.run(
                ["uv", "tool", "uninstall", tool_name],
                capture_output=True,
                check=False,
            )

    @pytest.mark.slow
    def test_uv_tool_status_command(self, tmp_path):
        """Test that generated tool has working status command.

        This should FAIL initially because:
        1. Status command not implemented
        2. CLI subcommands not configured
        3. Rich table output not working
        """
        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_name": "Test Status",
                "project_slug": "test-status",
            },
        )

        generated_project = Path(project_dir)
        tool_name = "test-status"

        try:
            # Install UV tool
            subprocess.run(
                ["uv", "tool", "install", str(generated_project)],
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )

            # Act: Execute status command
            status_result = subprocess.run(
                [tool_name, "status"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Assert: Status command works
            assert status_result.returncode == 0, f"Status command failed: {status_result.stderr}"
            # Should contain provider information
            assert "Provider" in status_result.stdout or "Status" in status_result.stdout

        finally:
            # Cleanup
            subprocess.run(
                ["uv", "tool", "uninstall", tool_name],
                capture_output=True,
                check=False,
            )

    def test_cookiecutter_branch_checkout_support(self, tmp_path):
        """Test cookiecutter generation from specific branch.

        This should FAIL initially because:
        1. Current branch might not exist for testing
        2. Branch-specific configuration not implemented
        3. Template variations between branches not handled
        """
        # Skip if we can't test branch checkout (in CI or no git history)
        try:
            # Check if we have git branches available
            branch_result = subprocess.run(
                ["git", "branch", "-a"],
                cwd=str(Path.cwd()),
                capture_output=True,
                text=True,
                timeout=10,
            )

            if branch_result.returncode != 0 or "origin/" not in branch_result.stdout:
                pytest.skip("No git branches available for branch testing")

        except subprocess.TimeoutExpired:
            pytest.skip("Git command timed out")
        except FileNotFoundError:
            pytest.skip("Git not available")

        # Arrange: Try to generate from current branch (should work)
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act: Generate with explicit branch checkout
        # Note: Using current branch as a test case
        current_branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(Path.cwd()),
            capture_output=True,
            text=True,
        ).stdout.strip()

        if not current_branch or current_branch == "HEAD":
            pytest.skip("Cannot determine current branch for testing")

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            checkout=current_branch,  # This is the key feature being tested
            output_dir=str(output_dir),
            extra_context={
                "project_name": "Branch Test",
                "project_slug": "branch-test",
            },
        )

        # Assert: Project generated successfully from branch
        generated_project = Path(project_dir)
        assert generated_project.exists()
        assert generated_project.name == "branch-test"

        # Basic structure should exist regardless of branch
        assert (generated_project / "README.md").exists()
        assert (generated_project / "install.py").exists()

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="UV tool PATH handling differs on Windows"
    )
    def test_uv_tool_cross_platform_compatibility(self, tmp_path):
        """Test UV tool works across different platforms.

        This should FAIL initially on some platforms because:
        1. Path handling differences between OS
        2. Script entry point format variations
        3. UV tool installation path differences
        """
        # This test focuses on Unix-like systems for now
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_name": "Cross Platform",
                "project_slug": "cross-platform",
            },
        )

        generated_project = Path(project_dir)
        tool_name = "cross-platform"

        try:
            # Test installation
            subprocess.run(
                ["uv", "tool", "install", str(generated_project)],
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )

            # Test that tool is in PATH and executable
            which_result = subprocess.run(
                ["which", tool_name],
                capture_output=True,
                text=True,
                timeout=10,
            )

            assert which_result.returncode == 0, f"Tool not found in PATH: {which_result.stderr}"

            # Test execution
            exec_result = subprocess.run(
                [tool_name, "--help"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            assert exec_result.returncode == 0, f"Tool execution failed: {exec_result.stderr}"

        finally:
            subprocess.run(
                ["uv", "tool", "uninstall", tool_name],
                capture_output=True,
                check=False,
            )

    def test_uv_environment_isolation(self, tmp_path):
        """Test that UV tool installation doesn't pollute global environment.

        This should FAIL initially because:
        1. UV tool isolation not properly configured
        2. Dependencies might leak into global space
        3. Virtual environment handling incorrect
        """
        # Arrange: Clean up any existing test tools first
        test_prefixes = ["test-", "isolation-", "my-ai-", "ai-conventions"]

        existing_tools = subprocess.run(
            ["uv", "tool", "list"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Clean up any existing test tools
        for line in existing_tools.stdout.split('\n'):
            if line.strip() and not line.startswith(' '):
                tool_name = line.split()[0]
                for prefix in test_prefixes:
                    if tool_name.startswith(prefix):
                        subprocess.run(
                            ["uv", "tool", "uninstall", tool_name],
                            capture_output=True,
                            check=False,
                        )
                        break

        # Check clean initial state
        initial_tools = subprocess.run(
            ["uv", "tool", "list"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Count actual tools (lines that don't start with space or dash)
        initial_tool_count = len([
            line for line in initial_tools.stdout.split('\n')
            if line.strip() and not line.startswith(' ') and not line.startswith('-')
        ])

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_name": "Isolation Test",
                "project_slug": "isolation-test",
            },
        )

        generated_project = Path(project_dir)
        tool_name = "isolation-test"

        try:
            # Install tool
            subprocess.run(
                ["uv", "tool", "install", str(generated_project)],
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )

            # Verify tool is isolated
            after_install_tools = subprocess.run(
                ["uv", "tool", "list"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Should have exactly one more tool
            after_tool_count = len([
                line for line in after_install_tools.stdout.split('\n')
                if line.strip() and not line.startswith(' ') and not line.startswith('-')
            ])

            assert after_tool_count == initial_tool_count + 1, (
                f"Expected {initial_tool_count + 1} tools, got {after_tool_count}\n"
                f"Tools: {after_install_tools.stdout}"
            )

            # Tool should be listed
            assert tool_name in after_install_tools.stdout

        finally:
            # Cleanup and verify removal
            subprocess.run(
                ["uv", "tool", "uninstall", tool_name],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            # Verify tool was removed
            final_tools = subprocess.run(
                ["uv", "tool", "list"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            final_tool_count = len([
                line for line in final_tools.stdout.split('\n')
                if line.strip() and not line.startswith(' ') and not line.startswith('-')
            ])

            assert final_tool_count == initial_tool_count, (
                f"Tool cleanup failed. Expected {initial_tool_count} tools, got {final_tool_count}"
            )

