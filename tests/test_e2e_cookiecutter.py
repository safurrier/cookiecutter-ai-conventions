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
        readme_content = (generated_project / "README.md").read_text()
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
        assert (generated_project / "commands").exists()
        assert (generated_project / "staging").exists()
        assert (generated_project / "commands" / "capture-learning.py").exists()
        assert (generated_project / "commands" / "review-learnings.py").exists()

    def test_learning_capture_disabled_removes_commands(self, tmp_path):
        """Test that learning capture disabled removes command directories."""
        # Arrange
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Act
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            extra_context={
                "enable_learning_capture": False,
            },
            output_dir=str(output_dir),
        )

        # Assert
        generated_project = Path(project_dir)
        assert not (generated_project / "commands").exists()
        assert not (generated_project / "staging").exists()

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
                "selected_providers": ["claude"],  # Single provider for now
            },
            output_dir=str(output_dir),
        )

        # Assert
        generated_project = Path(project_dir)
        providers_file = generated_project / ".selected_providers"
        assert providers_file.exists()

        content = providers_file.read_text()
        assert "claude" in content

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
                "selected_domains": ["git", "testing"],  # Use default domains
            },
            output_dir=str(output_dir),
        )

        # Assert
        generated_project = Path(project_dir)
        domains_dir = generated_project / "domains"

        assert (domains_dir / "git" / "core.md").exists()
        assert (domains_dir / "testing" / "core.md").exists()
        # Note: For now we can only test default domains due to cookiecutter limitations
