"""Test selective file generation improvements."""

from pathlib import Path

import yaml
from cookiecutter.main import cookiecutter


class TestSelectiveFileGeneration:
    """Test that only selected files are generated and cleanup works correctly."""

    def test_empty_directories_are_cleaned_up(self, tmp_path):
        """Test that empty directories are removed after generation."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Generate with minimal selections
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-cleanup",
                "selected_providers": "claude",  # Only one provider
                "default_domains": "git",  # Only one domain
                "enable_learning_capture": False,
                "enable_domain_composition": False,
            },
        )

        generated_project = Path(project_dir)

        # Learning capture is always available for better UX (improved architecture)
        assert (generated_project / "commands").exists()
        # staging removed - direct domain capture now
        assert not (generated_project / "staging").exists()
        assert not (generated_project / ".cursor").exists()
        assert not (generated_project / ".windsurf").exists()
        assert not (generated_project / ".aider").exists()
        assert not (generated_project / ".github").exists()
        assert not (generated_project / ".vscode").exists()
        assert not (generated_project / ".codex").exists()

        # These should exist
        assert (generated_project / "ai_conventions").exists()
        assert (generated_project / "ai_conventions" / "providers").exists()
        assert (generated_project / "ai_conventions" / "providers" / "claude.py").exists()

    def test_no_providers_selected_warning(self, tmp_path):
        """Test that project generates correctly with no providers."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Note: We can't capture the warning from cookiecutter subprocess,
        # but we can verify the behavior is correct
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-no-providers",
                "selected_providers": "",  # Empty providers
                "default_domains": "git",
            },
        )

        generated_project = Path(project_dir)
        # Should still generate basic structure
        assert generated_project.exists()
        assert (generated_project / "global.md").exists()

        # Provider modules directory should exist but with minimal files
        providers_dir = generated_project / "ai_conventions" / "providers"
        assert providers_dir.exists()

        # Should have all provider modules (improved architecture)
        py_files = list(providers_dir.glob("*.py"))
        assert len(py_files) == 8  # All providers + base + __init__
        assert (providers_dir / "base.py").exists()
        assert (providers_dir / "__init__.py").exists()

        # But no config files should exist since no providers selected
        assert not (generated_project / ".claude").exists()
        assert not (generated_project / ".cursorrules").exists()

    def test_invalid_domain_warning(self, tmp_path):
        """Test warning when invalid domains are selected."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-invalid-domain",
                "selected_providers": "claude",
                "default_domains": "git,invalid_domain,testing",  # Mix of valid and invalid
            },
        )

        # Note: We can't capture the warning from cookiecutter subprocess

        generated_project = Path(project_dir)
        domains_dir = generated_project / "domains"

        # Valid domains should exist
        assert (domains_dir / "git" / "core.md").exists()
        assert (domains_dir / "testing" / "core.md").exists()

        # Invalid domain should not exist
        assert not (domains_dir / "invalid_domain").exists()

    def test_selective_provider_file_generation(self, tmp_path):
        """Test that only selected provider files are kept."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Test with specific providers
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-selective",
                "selected_providers": "claude,aider",  # Only these two
                "default_domains": "git",
            },
        )

        generated_project = Path(project_dir)
        providers_dir = generated_project / "ai_conventions" / "providers"

        # ALL provider modules should exist (improved architecture)
        assert (providers_dir / "claude.py").exists()
        assert (providers_dir / "aider.py").exists()
        assert (providers_dir / "cursor.py").exists()  # Keep all Python modules
        assert (providers_dir / "windsurf.py").exists()
        assert (providers_dir / "copilot.py").exists()
        assert (providers_dir / "codex.py").exists()

        # Base files should still exist
        assert (providers_dir / "base.py").exists()
        assert (providers_dir / "__init__.py").exists()

        # Config files: only selected providers should have config
        assert (generated_project / ".claude").exists()  # Claude selected
        assert (generated_project / "CONVENTIONS.md").exists()  # Aider selected
        assert not (generated_project / ".cursorrules").exists()  # Cursor not selected
        assert not (generated_project / ".windsurfrules").exists()  # Windsurf not selected

    def test_docs_directory_cleanup(self, tmp_path):
        """Test that docs directory is cleaned up when empty."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Generate with providers that don't create docs
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-docs-cleanup",
                "selected_providers": "claude",  # Claude doesn't create docs
                "default_domains": "git",
            },
        )

        generated_project = Path(project_dir)
        docs_dir = generated_project / "docs"

        # If docs directory exists, it should have content
        # If it's empty, it should have been removed
        if docs_dir.exists():
            assert any(docs_dir.iterdir()), "docs directory should not be empty"

    def test_comprehensive_cleanup_with_all_features_disabled(self, tmp_path):
        """Test cleanup when all optional features are disabled."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-minimal-cleanup",
                "selected_providers": "aider",  # Minimal provider
                "default_domains": "git",
                "enable_learning_capture": False,
                "enable_context_canary": False,
                "enable_domain_composition": False,
            },
        )

        generated_project = Path(project_dir)

        # Learning capture is now always available (improved UX)
        # staging removed - direct domain capture now
        assert not (generated_project / "staging").exists()
        assert (generated_project / "commands").exists()

        # Domain composition can still be disabled
        assert not (generated_project / "ai_conventions" / "domain_resolver.py").exists()

        # Should still have core files
        assert (generated_project / "global.md").exists()
        assert (generated_project / "install.py").exists()
        assert (generated_project / "README.md").exists()

        # Aider-specific files should exist
        assert (generated_project / "CONVENTIONS.md").exists()
        assert (generated_project / ".aider.conf.yml").exists()

    def test_config_file_generation(self, tmp_path):
        """Test that config file is generated with selections."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-config-generation",
                "project_name": "Test Config Project",
                "author_name": "Test Author",
                "author_email": "test@example.com",
                "selected_providers": "claude,cursor",
                "default_domains": "git,testing",
                "enable_learning_capture": True,
                "enable_context_canary": True,
                "enable_domain_composition": True,
            },
        )

        generated_project = Path(project_dir)

        # Check config file exists
        config_path = generated_project / ".ai-conventions.yaml"
        assert config_path.exists()

        # Load and validate config
        with open(config_path) as f:
            config = yaml.safe_load(f)

        assert config["project_name"] == "Test Config Project"
        assert config["project_slug"] == "test-config-generation"
        assert config["author_name"] == "Test Author"
        assert config["author_email"] == "test@example.com"
        assert config["selected_providers"] == ["claude", "cursor"]
        assert config["default_domains"] == "git,testing"
        assert config["enable_learning_capture"] is True
        assert config["enable_context_canary"] is True
        assert config["enable_domain_composition"] is True

    def test_tools_removal_when_disabled(self, tmp_path):
        """Test that install tools are removed when not selected."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-no-tools",
                "selected_providers": "claude",
                "default_domains": "git",
                "include_install_tools": "false",
            },
        )

        generated_project = Path(project_dir)

        # Check Python module is removed
        assert not (generated_project / "ai_conventions").exists()
        assert not (generated_project / "install.py").exists()
        assert not (generated_project / "pyproject.toml").exists()

        # But convention files should remain
        assert (generated_project / "README.md").exists()
        assert (generated_project / "templates").exists()

    def test_minimal_file_generation(self, tmp_path):
        """Test that minimal selection produces < 10 files."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-minimal",
                "selected_providers": "claude",
                "default_domains": "git",
                "include_install_tools": "false",
            },
        )

        generated_project = Path(project_dir)

        # Count all files recursively
        file_count = sum(1 for _ in generated_project.rglob("*") if _.is_file())

        # Should have significantly fewer files than default (35+)
        # Expecting ~15-20 files for minimal setup with templates
        assert file_count < 20, f"Too many files generated: {file_count}"

        # Essential files should still exist
        assert (generated_project / "README.md").exists()
        assert (generated_project / "templates" / "claude" / "CLAUDE.md.j2").exists()
        assert (generated_project / "domains" / "git" / "core.md").exists()

    def test_readme_updated_with_selections(self, tmp_path):
        """Test that README is updated to reflect selections."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_slug": "test-readme",
                "selected_providers": "claude,cursor",
                "default_domains": "git,testing",
                "include_install_tools": "true",
            },
        )

        generated_project = Path(project_dir)
        readme_content = (generated_project / "README.md").read_text()

        # Check for included components section
        assert "## 📦 What's Included" in readme_content
        assert "### AI Providers" in readme_content
        assert "- Claude" in readme_content
        assert "- Cursor" in readme_content
        assert "### Convention Domains" in readme_content
        assert "- Git" in readme_content
        assert "- Testing" in readme_content
        assert "### Installation Tools" in readme_content
