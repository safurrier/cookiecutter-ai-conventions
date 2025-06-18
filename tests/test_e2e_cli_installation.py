"""End-to-end tests for CLI installation and naming."""

import sys


class TestE2ECLIInstallation:
    """Test CLI installation, naming, and basic functionality."""

    def test_generated_project_has_correct_cli_name(self, cookies):
        """Test that pyproject.toml uses correct CLI name regardless of project slug."""
        result = cookies.bake(
            extra_context={
                "project_slug": "my-custom-project",  # Different from expected CLI name
                "project_name": "My Custom Project",
            }
        )

        pyproject_path = result.project_path / "pyproject.toml"
        pyproject_content = pyproject_path.read_text()

        # Should use 'ai-conventions' not project slug
        assert 'ai-conventions = "ai_conventions.cli:main"' in pyproject_content
        # Should NOT contain project slug in CLI script entries (but name field is OK)
        scripts_section = pyproject_content.split("[project.scripts]")[1].split("[")[0]
        assert '"my-custom-project"' not in scripts_section

        # Verify no separate CLI tools (they're all subcommands now)
        assert 'capture-learning = "ai_conventions.capture:main"' not in pyproject_content
        assert 'sync-conventions = "ai_conventions.sync:main"' not in pyproject_content
        assert 'conventions-config = "ai_conventions.config_cli:main"' not in pyproject_content

    def test_bootstrap_script_not_in_generated_project(self, cookies):
        """Test that bootstrap.sh is not included in generated projects."""
        result = cookies.bake()

        bootstrap_path = result.project_path / "bootstrap.sh"
        assert not bootstrap_path.exists(), "bootstrap.sh should not exist in generated project"

    def test_cli_commands_can_be_imported(self, cookies):
        """Test that CLI commands can be imported without errors."""
        result = cookies.bake()

        # Add the project to Python path
        sys.path.insert(0, str(result.project_path))

        try:
            # These imports should work
            from ai_conventions.cli import main
            from ai_conventions.config_cli import config_command
            from ai_conventions.sync import main as sync_main

            # Verify they are callable
            assert callable(main)
            assert callable(sync_main)
            assert callable(config_command)

        except ImportError as e:
            raise AssertionError(f"CLI modules should be importable: {e}") from e
        finally:
            # Clean up sys.path
            if str(result.project_path) in sys.path:
                sys.path.remove(str(result.project_path))

    def test_cli_help_works_after_generation(self, cookies):
        """Test that CLI help command works in generated project."""
        result = cookies.bake()

        # Add the project to Python path
        sys.path.insert(0, str(result.project_path))

        try:
            from ai_conventions.cli import main
            from click.testing import CliRunner

            runner = CliRunner()
            result_cmd = runner.invoke(main, ["--help"])

            assert result_cmd.exit_code == 0, f"Help command should work: {result_cmd.output}"
            assert "Usage:" in result_cmd.output
            assert "Commands:" in result_cmd.output

        finally:
            # Clean up sys.path
            if str(result.project_path) in sys.path:
                sys.path.remove(str(result.project_path))
