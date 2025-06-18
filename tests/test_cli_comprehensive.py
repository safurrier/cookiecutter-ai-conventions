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
                expected_output_contains="Available Domains",
                description="List command should work and show domains",
            ),
            CLITestCase(
                command_args=["update", "--check"],
                expected_exit_code=0,
                expected_output_not_contains="Error",
                description="Update check should work without errors",
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

    def test_all_config_cli_commands(self):
        """Test all config CLI commands using table-driven approach."""
        test_cases = [
            CLITestCase(
                command_args=["--help"],
                expected_exit_code=0,
                expected_output_contains="Usage:",
                description="Config help should work",
                cli_module="ai_conventions.config_cli",
                cli_function="config",
            ),
            CLITestCase(
                command_args=["show"],
                expected_exit_code=0,
                expected_output_not_contains="Error loading config",
                description="Config show should work without errors",
                cli_module="ai_conventions.config_cli",
                cli_function="config",
            ),
            CLITestCase(
                command_args=["validate"],
                expected_exit_code=0,
                expected_output_contains="Configuration is valid",
                description="Config validate should work",
                cli_module="ai_conventions.config_cli",
                cli_function="config",
            ),
        ]

        from ai_conventions.config_cli import config_command
        from click.testing import CliRunner

        runner = CliRunner()

        for case in test_cases:
            with self.subTest(case=case):
                result = runner.invoke(config_command, case.command_args)

                self.assertEqual(
                    result.exit_code,
                    case.expected_exit_code,
                    f"Config command {case.command_args} failed with exit code {result.exit_code}. "
                    f"Output: {result.output}",
                )

                if case.expected_output_contains:
                    self.assertIn(
                        case.expected_output_contains,
                        result.output,
                        f"Config command {case.command_args} output should contain '{case.expected_output_contains}'",
                    )

                if case.expected_output_not_contains:
                    self.assertNotIn(
                        case.expected_output_not_contains,
                        result.output,
                        f"Config command {case.command_args} output should not contain '{case.expected_output_not_contains}'",
                    )

    def test_all_sync_cli_commands(self):
        """Test sync CLI commands using table-driven approach."""
        test_cases = [
            CLITestCase(
                command_args=["--help"],
                expected_exit_code=0,
                expected_output_contains="Usage:",
                description="Sync help should work",
                cli_module="ai_conventions.sync",
                cli_function="main",
            ),
            CLITestCase(
                command_args=["--provider", "claude"],
                expected_exit_code=0,
                expected_output_not_contains="Error",
                description="Sync to specific provider should work",
                cli_module="ai_conventions.sync",
                cli_function="main",
            ),
        ]

        from ai_conventions.sync import main as sync_main
        from click.testing import CliRunner

        runner = CliRunner()

        for case in test_cases:
            with self.subTest(case=case):
                result = runner.invoke(sync_main, case.command_args)

                self.assertEqual(
                    result.exit_code,
                    case.expected_exit_code,
                    f"Sync command {case.command_args} failed with exit code {result.exit_code}. "
                    f"Output: {result.output}",
                )

                if case.expected_output_contains:
                    self.assertIn(
                        case.expected_output_contains,
                        result.output,
                        f"Sync command {case.command_args} output should contain '{case.expected_output_contains}'",
                    )

                if case.expected_output_not_contains:
                    self.assertNotIn(
                        case.expected_output_not_contains,
                        result.output,
                        f"Sync command {case.command_args} output should not contain '{case.expected_output_not_contains}'",
                    )


if __name__ == "__main__":
    unittest.main()
