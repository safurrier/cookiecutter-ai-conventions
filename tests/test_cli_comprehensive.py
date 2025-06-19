"""Comprehensive CLI testing using table-driven patterns (2025 best practices)."""

import os
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pytest


@dataclass
class CLITestCase:
    """Test case for CLI command testing."""

    command_args: list[str]
    expected_exit_code: int
    expected_output_contains: Optional[str] = None
    expected_output_not_contains: Optional[str] = None
    description: str = ""
    cli_module: str = "ai_conventions.cli"
    cli_function: str = "main"


@pytest.mark.serial
class TestCLIComprehensive(unittest.TestCase):
    """Comprehensive CLI testing using 2025 table-driven patterns."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests."""
        # Create a test project
        import shutil

        from cookiecutter.main import cookiecutter

        cls.test_dir = Path(__file__).parent.parent / "test-output-cli"
        # Clean up any existing test directory
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)
        cls.test_dir.mkdir(exist_ok=True)

        cls.project_dir = cookiecutter(
            str(Path(__file__).parent.parent),
            no_input=True,
            output_dir=str(cls.test_dir),
        )
        cls.project_path = Path(cls.project_dir)

        # Add to Python path
        sys.path.insert(0, str(cls.project_path))

        # Change to project directory for commands that need it
        cls.original_cwd = os.getcwd()
        os.chdir(cls.project_path)

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        # Restore original directory
        os.chdir(cls.original_cwd)

        # Remove from sys.path
        if str(cls.project_path) in sys.path:
            sys.path.remove(str(cls.project_path))

        # Clean up test directory
        import shutil

        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)

    def test_all_main_cli_commands(self):
        """Test all main CLI commands using table-driven approach."""
        test_cases = [
            CLITestCase(
                command_args=["--help"],
                expected_exit_code=0,
                expected_output_contains="Usage:",
                description="Help command should work",
            ),
            CLITestCase(
                command_args=["--version"],
                expected_exit_code=0,
                expected_output_contains="ai-conventions",
                description="Version command should work",
            ),
            CLITestCase(
                command_args=["status"],
                expected_exit_code=0,
                expected_output_contains="Status",
                description="Status command should work without errors",
            ),
            CLITestCase(
                command_args=["list"],
                expected_exit_code=0,
                expected_output_contains="Domain Structure",
                description="List command should work and show domain structure",
            ),
            CLITestCase(
                command_args=["list", "--domains-only"],
                expected_exit_code=0,
                expected_output_contains="Available Domains",
                description="List domains-only should work",
            ),
            CLITestCase(
                command_args=["add", "Test pattern", "--domain", "python"],
                expected_exit_code=0,
                expected_output_contains="Convention added",
                description="Add command should work",
            ),
            CLITestCase(
                command_args=["remove"],
                expected_exit_code=0,
                expected_output_not_contains="Error",
                description="Remove command should handle empty log gracefully",
            ),
            CLITestCase(
                command_args=["config", "--show"],
                expected_exit_code=0,
                expected_output_contains="Configuration",
                description="Config show should work",
            ),
        ]

        from ai_conventions.cli import main
        from click.testing import CliRunner

        runner = CliRunner()

        for case in test_cases:
            with self.subTest(case=case):
                result = runner.invoke(main, case.command_args)

                self.assertEqual(
                    result.exit_code,
                    case.expected_exit_code,
                    f"Command {case.command_args} failed with exit code {result.exit_code}. "
                    f"Output: {result.output}",
                )

                if case.expected_output_contains:
                    self.assertIn(
                        case.expected_output_contains,
                        result.output,
                        f"Command {case.command_args} output should contain '{case.expected_output_contains}'",
                    )

                if case.expected_output_not_contains:
                    self.assertNotIn(
                        case.expected_output_not_contains,
                        result.output,
                        f"Command {case.command_args} output should not contain '{case.expected_output_not_contains}'",
                    )

    def test_removed_commands_no_longer_exist(self):
        """Test that removed commands (sync, update, capture) no longer exist."""
        test_cases = [
            CLITestCase(
                command_args=["sync"],
                expected_exit_code=2,  # Click returns 2 for unknown commands
                expected_output_contains="No such command",
                description="Sync command should no longer exist",
            ),
            CLITestCase(
                command_args=["update"],
                expected_exit_code=2,
                expected_output_contains="No such command",
                description="Update command should no longer exist",
            ),
            CLITestCase(
                command_args=["capture"],
                expected_exit_code=2,
                expected_output_contains="No such command",
                description="Capture command should no longer exist",
            ),
        ]

        from ai_conventions.cli import main
        from click.testing import CliRunner

        runner = CliRunner()

        for case in test_cases:
            with self.subTest(case=case):
                result = runner.invoke(main, case.command_args)

                self.assertEqual(
                    result.exit_code,
                    case.expected_exit_code,
                    f"Command {case.command_args} should not exist but got exit code {result.exit_code}. "
                    f"Output: {result.output}",
                )

                if case.expected_output_contains:
                    self.assertIn(
                        case.expected_output_contains,
                        result.output,
                        f"Command {case.command_args} output should contain '{case.expected_output_contains}'",
                    )

    def test_new_command_functionality(self):
        """Test that new commands work correctly."""
        # Create domains directory first
        domains_dir = Path("domains")
        domains_dir.mkdir(exist_ok=True)

        test_cases = [
            CLITestCase(
                command_args=["add", "--help"],
                expected_exit_code=0,
                expected_output_contains="Add a new learning",
                description="Add command help should work",
            ),
            CLITestCase(
                command_args=["remove", "--help"],
                expected_exit_code=0,
                expected_output_contains="Remove the last",
                description="Remove command help should work",
            ),
            CLITestCase(
                command_args=["config", "--help"],
                expected_exit_code=0,
                expected_output_contains="Manage AI Conventions",
                description="Config command help should work",
            ),
        ]

        from ai_conventions.cli import main
        from click.testing import CliRunner

        runner = CliRunner()

        for case in test_cases:
            with self.subTest(case=case):
                result = runner.invoke(main, case.command_args)

                self.assertEqual(
                    result.exit_code,
                    case.expected_exit_code,
                    f"Command {case.command_args} failed with exit code {result.exit_code}. "
                    f"Output: {result.output}",
                )

                if case.expected_output_contains:
                    self.assertIn(
                        case.expected_output_contains,
                        result.output,
                        f"Command {case.command_args} output should contain '{case.expected_output_contains}'",
                    )


if __name__ == "__main__":
    unittest.main()
