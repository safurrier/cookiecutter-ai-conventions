"""End-to-end tests for template processing and Python file validity.

These tests ensure that:
1. All Python files are syntactically valid after Jinja2 processing
2. The generated project can be installed and run
3. Template variables are properly replaced
4. No unprocessed Jinja2 syntax remains in generated files
"""

import ast
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture
def unique_tool_name():
    """Generate a unique tool name for each test to avoid conflicts."""
    return f"test-tool-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def safe_uv_tool_cleanup(unique_tool_name):
    """Ensure UV tool cleanup after test."""
    yield unique_tool_name

    # Cleanup after test - uninstall by package name (which is the tool_name/project_slug)
    try:
        subprocess.run(
            ["uv", "tool", "uninstall", unique_tool_name],
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


class TestTemplateProcessing:
    """Test that all templates are processed correctly."""

    def test_all_python_files_are_syntactically_valid(self, tmp_path):
        """Test that all generated Python files compile without SyntaxError."""
        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act: Generate with all features enabled to test all code paths
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "enable_learning_capture": True,
                "enable_context_canary": True,
                "enable_domain_composition": True,
            },
            output_dir=str(output_dir),
        )

        # Assert: All Python files should be syntactically valid
        generated_project = Path(project_dir)
        python_files = list(generated_project.rglob("*.py"))

        assert len(python_files) > 0, "No Python files found in generated project"

        errors = []
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                # Check for unprocessed Jinja2 syntax
                if "{%" in content or "{{" in content:
                    errors.append(f"{py_file}: Contains unprocessed Jinja2 syntax")
                    continue

                # Try to compile the Python code
                ast.parse(content, filename=str(py_file))
            except SyntaxError as e:
                errors.append(f"{py_file}: {e}")

        if errors:
            pytest.fail("Python syntax errors found:\n" + "\n".join(errors))

    def test_all_imports_always_processed(self, tmp_path):
        """Test that all CLI imports are always available (improved architecture)."""
        # Test case 1: With learning capture enabled
        output_dir = tmp_path / "with_capture"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "enable_learning_capture": True,
            },
            output_dir=str(output_dir),
        )

        cli_py = Path(project_dir) / "ai_conventions" / "cli.py"
        content = cli_py.read_text(encoding="utf-8")

        # Should have all imports (better architecture)
        assert "from .capture import capture_command" in content
        assert "from .sync import sync_command" in content
        assert 'main.add_command(capture_command, name="capture")' in content
        # Should not have Jinja2 syntax
        assert "{%" not in content
        assert "cookiecutter" not in content

        # Test case 2: Even with learning capture "disabled", all imports should be available
        output_dir2 = tmp_path / "without_capture"
        output_dir2.mkdir()

        project_dir2 = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "enable_learning_capture": False,  # Architecture improvement: always available
            },
            output_dir=str(output_dir2),
        )

        cli_py2 = Path(project_dir2) / "ai_conventions" / "cli.py"
        content2 = cli_py2.read_text(encoding="utf-8")

        # Should have all imports (no conditional removal)
        assert "from .capture import capture_command" in content2
        assert "main.add_command(capture_command" in content2
        assert "from .sync import sync_command" in content2
        # Should not have Jinja2 syntax
        assert "{%" not in content2
        assert "cookiecutter" not in content2

    def test_project_metadata_is_replaced(self, tmp_path):
        """Test that project metadata variables are replaced correctly."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        custom_name = "Test AI Conventions"
        custom_email = "test@example.com"

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "project_name": custom_name,
                "author_email": custom_email,
            },
            output_dir=str(output_dir),
        )

        # Check install.py
        install_py = Path(project_dir) / "install.py"
        install_content = install_py.read_text(encoding="utf-8")

        assert f'"project_name": "{custom_name}"' in install_content
        assert f'"author_email": "{custom_email}"' in install_content
        assert "{{cookiecutter" not in install_content

        # Check README.md
        readme = Path(project_dir) / "README.md"
        readme_content = readme.read_text(encoding="utf-8")

        assert custom_name in readme_content
        assert "{{cookiecutter" not in readme_content

    def test_pyproject_toml_is_valid(self, tmp_path):
        """Test that pyproject.toml is properly processed and valid."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "project_name": "Test Project",
                "author_name": "Test Author",
                "author_email": "test@example.com",
            },
            output_dir=str(output_dir),
        )

        pyproject = Path(project_dir) / "pyproject.toml"
        content = pyproject.read_text(encoding="utf-8")

        # Should not have any template syntax
        assert "{{" not in content
        assert "{%" not in content

        # Should have proper values
        assert 'name = "test-project"' in content
        assert '"Test Author"' in content
        assert '"test@example.com"' in content

    def test_files_in_copy_without_render_are_not_processed(self, tmp_path):
        """Test that files in _copy_without_render list are not processed."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
        )

        # Check that community-domains files are copied as-is
        # These files might contain example Jinja2 syntax that should not be processed
        community_domains = Path(project_dir) / "community-domains"
        if community_domains.exists():
            # Any .md files in community-domains should be copied without processing
            for md_file in community_domains.rglob("*.md"):
                content = md_file.read_text(encoding="utf-8")
                # These files might legitimately contain template examples
                # so we just verify they exist and are readable
                assert len(content) > 0


class TestEndToEndUserJourney:
    """Test the complete user journey from generation to CLI usage."""

    @pytest.mark.skipif(sys.platform == "win32", reason="Shell command testing is Unix-specific")
    @pytest.mark.serial
    def test_generate_install_and_run_cli(self, tmp_path, safe_uv_tool_cleanup):
        """Test the full journey: generate → uv tool install → run CLI."""
        tool_name = safe_uv_tool_cleanup  # This is the unique tool name

        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act: Generate project with unique name
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "project_slug": tool_name,
                "enable_learning_capture": True,
            },
            output_dir=str(output_dir),
        )

        generated_project = Path(project_dir)

        # Assert: Project structure is correct
        assert (generated_project / "pyproject.toml").exists()
        assert (generated_project / "ai_conventions" / "__init__.py").exists()
        assert (generated_project / "ai_conventions" / "cli.py").exists()

        # Act: Install with UV tool (unique name prevents conflicts)
        result = subprocess.run(
            ["uv", "tool", "install", str(generated_project)],
            capture_output=True,
            text=True,
            cwd=str(generated_project),
        )

        assert result.returncode == 0, f"uv tool install failed: {result.stderr}"

        # Act: Run the CLI (command is always 'ai-conventions' regardless of project slug)
        result = subprocess.run(
            ["ai-conventions", "--version"],
            capture_output=True,
            text=True,
            shell=False,
        )

        assert result.returncode == 0, f"CLI execution failed: {result.stderr}"
        assert "0.1.0" in result.stdout

        # Act: Run status command
        result = subprocess.run(
            ["ai-conventions", "status"],
            capture_output=True,
            text=True,
            cwd=str(generated_project),
            shell=False,
        )

        assert result.returncode == 0, f"Status command failed: {result.stderr}"
        assert "AI Conventions Status" in result.stdout

    def test_python_import_paths_work(self, tmp_path):
        """Test that the generated package can be imported and used."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "enable_learning_capture": True,
            },
            output_dir=str(output_dir),
        )

        # Add the project to Python path
        sys.path.insert(0, str(project_dir))

        try:
            # Should be able to import the package

            # With learning capture enabled, these should also work

            # The main CLI group should be accessible
            from ai_conventions.cli import main

            assert hasattr(main, "commands")

        finally:
            # Clean up sys.path
            sys.path.remove(str(project_dir))


class TestShellCompatibility:
    """Test shell environment compatibility."""

    @pytest.mark.skipif(sys.platform == "win32", reason="Shell testing is Unix-specific")
    def test_subprocess_commands_work_in_sh(self, tmp_path):
        """Test that subprocess commands work in /bin/sh environment."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
        )

        # Test that install.py works with /bin/sh
        Path(project_dir) / "install.py"

        # Run with explicit /bin/sh shell
        result = subprocess.run(
            ["/bin/sh", "-c", f"cd {project_dir} && python install.py --help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"install.py failed in sh: {result.stderr}"
        assert "Install AI conventions" in result.stdout

    @pytest.mark.skipif(sys.platform == "win32", reason="Shell testing is Unix-specific")
    def test_no_shell_specific_aliases_in_scripts(self, tmp_path):
        """Test that generated scripts don't rely on shell-specific aliases."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
        )

        # Check all Python files for subprocess calls
        for py_file in Path(project_dir).rglob("*.py"):
            content = py_file.read_text(encoding="utf-8")

            # These patterns might indicate shell-specific usage
            problematic_patterns = [
                "shell=True",  # Using shell can introduce compatibility issues
                "~/",  # Shell expansion might not work consistently
                "cd ",  # Direct cd commands in subprocess
            ]

            for pattern in problematic_patterns:
                if pattern in content:
                    # Some uses might be legitimate, check context
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if pattern in line and not line.strip().startswith("#"):
                            # Check if it's in a subprocess call
                            context = "\n".join(lines[max(0, i - 2) : min(len(lines), i + 3)])
                            if "subprocess" in context or "run(" in context or "Popen" in context:
                                pytest.fail(
                                    f"Found potentially problematic shell usage in {py_file}:\n"
                                    f"Line {i + 1}: {line}\n"
                                    f"Context:\n{context}"
                                )
