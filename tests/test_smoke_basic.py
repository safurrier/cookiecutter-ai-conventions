"""Smoke tests for quick validation of the cookiecutter template.

These tests provide fast feedback without running full template generation.
"""

import json
from pathlib import Path


class TestSmokeTemplateStructure:
    """Quick validation of template structure and configuration."""

    def test_cookiecutter_json_is_valid(self):
        """Test that cookiecutter.json is valid JSON with required fields."""
        # Arrange
        cookiecutter_path = Path("cookiecutter.json")

        # Act & Assert
        assert cookiecutter_path.exists(), "cookiecutter.json must exist"

        with open(cookiecutter_path) as f:
            config = json.load(f)

        # Assert: Required fields exist
        assert "project_name" in config
        assert "project_slug" in config
        assert "author_name" in config
        assert "author_email" in config
        assert "selected_providers" in config
        assert "enable_learning_capture" in config
        assert "default_domains" in config

    def test_essential_template_files_exist(self):
        """Test that essential template files are present."""
        # Arrange
        template_dir = Path("{{cookiecutter.project_slug}}")

        # Assert: Template directory exists
        assert template_dir.exists()

        # Assert: Essential files exist
        essential_files = [
            "global.md",
            "README.md",
            "install.py",
            "templates/claude/CLAUDE.md.j2",
        ]

        for file_path in essential_files:
            assert (template_dir / file_path).exists(), f"{file_path} must exist"

    def test_hooks_exist_and_are_executable(self):
        """Test that cookiecutter hooks exist."""
        # Arrange
        hooks_dir = Path("hooks")

        # Assert
        assert hooks_dir.exists()
        assert (hooks_dir / "pre_gen_project.py").exists()
        assert (hooks_dir / "post_gen_project.py").exists()

    def test_domain_registry_is_valid(self):
        """Test that the domain registry is valid JSON."""
        # Arrange
        registry_path = Path("community-domains/registry.json")

        # Act & Assert
        assert registry_path.exists()

        with open(registry_path) as f:
            registry = json.load(f)

        # Assert: Registry has expected structure
        assert "version" in registry
        assert "domains" in registry
        assert isinstance(registry["domains"], list)

        # Assert: Each domain has required fields
        for domain in registry["domains"]:
            assert "name" in domain
            assert "description" in domain
            assert "files" in domain
            assert isinstance(domain["files"], list)

    def test_all_registered_domains_exist(self):
        """Test that all domains in registry have corresponding directories."""
        # Arrange
        registry_path = Path("community-domains/registry.json")
        domains_dir = Path("community-domains")

        with open(registry_path) as f:
            registry = json.load(f)

        # Act & Assert
        for domain in registry["domains"]:
            domain_name = domain["name"]
            domain_path = domains_dir / domain_name

            assert domain_path.exists(), f"Domain {domain_name} directory must exist"

            # Check all listed files exist
            for file_name in domain["files"]:
                file_path = domain_path / file_name
                assert file_path.exists(), f"Domain file {file_path} must exist"

    def test_learning_capture_files_conditional(self):
        """Test that learning capture files exist in template."""
        # Arrange
        template_dir = Path("{{cookiecutter.project_slug}}")

        # Assert: Conditional directories exist in template
        assert (template_dir / "commands").exists()
        # staging removed - direct domain capture now
        assert not (template_dir / "staging").exists()

        # Assert: Command files exist
        assert (template_dir / "commands" / "capture-learning.md").exists()
        assert (template_dir / "commands" / "review-learnings.md").exists()
        assert (template_dir / "commands" / "capture-learning.py").exists()
        assert (template_dir / "commands" / "review-learnings.py").exists()

        # staging removed - direct domain capture now
        # Learnings go directly to domains instead
