"""End-to-end tests for the complete cookiecutter generation flow.

Following the progressive testing approach, these E2E tests verify the
complete user journey from template to generated project.
"""

from pathlib import Path

from cookiecutter.main import cookiecutter


class TestE2ECookiecutterGeneration:
    """Test the complete cookiecutter template generation user journey."""

    def test_generate_project_with_defaults(self, tmp_path):
        """Test generating a project with default settings."""
        # Act: Generate project with defaults
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
        )

        # Assert: Verify project was created
        generated_project = Path(project_dir)
        assert generated_project.exists()
        assert generated_project.name == "my-ai-conventions"

        # Assert: Check essential structure
        assert (generated_project / "global.md").exists()
        assert (generated_project / "README.md").exists()
        assert (generated_project / "install.py").exists()
        assert (generated_project / "domains").exists()

        # Assert: Default domains were copied
        assert (generated_project / "domains" / "git").exists()
        assert (generated_project / "domains" / "testing").exists()

    def test_generate_with_custom_project_name(self, tmp_path):
        """Test generating with a custom project name."""
        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "project_name": "My Custom Conventions",
                "project_slug": "my-custom-conventions",
            },
            output_dir=str(output_dir),
        )

        # Assert
        generated_project = Path(project_dir)
        assert generated_project.exists()
        assert generated_project.name == "my-custom-conventions"

        # Verify the name is used in files
        readme_content = (generated_project / "README.md").read_text(encoding="utf-8")
        assert "My Custom Conventions" in readme_content

    def test_learning_capture_enabled_includes_commands(self, tmp_path):
        """Test that learning capture enabled includes command directories."""
        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "enable_learning_capture": True,
            },
            output_dir=str(output_dir),
        )

        # Assert
        generated_project = Path(project_dir)
        # With default claude provider, should have Claude commands
        assert (generated_project / ".claude" / "commands").exists()
        # staging removed - direct domain capture now
        assert not (generated_project / "staging").exists()
        assert (generated_project / ".claude" / "commands" / "capture-learning.md").exists()
        assert (generated_project / ".claude" / "commands" / "review-learnings.md").exists()
        # Python scripts should be removed but commands directory exists with .md files
        commands_dir = generated_project / "commands"
        assert commands_dir.exists()
        assert not (commands_dir / "capture-learning.py").exists()
        assert not (commands_dir / "review-learnings.py").exists()
        assert (commands_dir / "capture-learning.md").exists()
        assert (commands_dir / "review-learnings.md").exists()

    def test_learning_capture_always_available(self, tmp_path):
        """Test that learning capture is always available for better UX."""
        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "enable_learning_capture": False,  # Even when disabled, should be available
            },
            output_dir=str(output_dir),
        )

        # Assert: Learning capture should always be available for better UX
        generated_project = Path(project_dir)
        assert (generated_project / "commands").exists()
        assert (generated_project / ".claude").exists()  # Default provider is Claude
        # staging removed - direct domain capture now
        assert not (generated_project / "staging").exists()
        
        # Verify specific learning capture files
        assert (generated_project / "commands" / "capture-learning.md").exists()
        assert (generated_project / ".claude" / "commands" / "capture-learning.md").exists()

    def test_provider_selection_creates_config(self, tmp_path):
        """Test that provider selection creates proper configuration."""
        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "selected_providers": "claude",  # Single provider for now
            },
            output_dir=str(output_dir),
        )

        # Assert
        generated_project = Path(project_dir)
        # Provider selection should configure the project correctly
        # With Claude provider, should have Claude commands
        assert (generated_project / ".claude").exists()
        # Check that the README mentions Claude setup
        readme_content = (generated_project / "README.md").read_text(encoding="utf-8")
        assert "Claude" in readme_content or "claude" in readme_content

    def test_all_domains_can_be_selected(self, tmp_path):
        """Test selecting all available domains."""
        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "default_domains": "git,testing",  # Use default domains
            },
            output_dir=str(output_dir),
        )

        # Assert
        generated_project = Path(project_dir)
        domains_dir = generated_project / "domains"

        assert (domains_dir / "git" / "core.md").exists()
        assert (domains_dir / "testing" / "core.md").exists()
        # Note: For now we can only test default domains due to cookiecutter limitations

    def test_python_files_are_processed_correctly(self, tmp_path):
        """Test that Python files with Jinja2 syntax are processed correctly."""
        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "enable_learning_capture": True,
            },
            output_dir=str(output_dir),
        )

        # Assert: Verify Python files don't contain unprocessed Jinja2 syntax
        generated_project = Path(project_dir)
        
        # Check cli.py - this file has conditional imports based on enable_learning_capture
        cli_py = generated_project / "ai_conventions" / "cli.py"
        assert cli_py.exists()
        cli_content = cli_py.read_text(encoding="utf-8")
        
        # Should not contain any Jinja2 syntax
        assert "{%" not in cli_content
        assert "{{" not in cli_content
        assert "cookiecutter." not in cli_content
        
        # Should contain the processed result
        assert "from .capture import capture_command" in cli_content
        
        # Check install.py - this file has cookiecutter variables
        install_py = generated_project / "install.py"
        assert install_py.exists()
        install_content = install_py.read_text(encoding="utf-8")
        
        # Should not contain any Jinja2 syntax
        assert "{{" not in install_content
        assert "cookiecutter." not in install_content
        
        # Should contain the processed values
        assert '"project_name": "My AI Conventions"' in install_content
