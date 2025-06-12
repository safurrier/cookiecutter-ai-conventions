"""Test selective file generation improvements."""

import pytest
from pathlib import Path
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
        
        # These directories should NOT exist if empty
        assert not (generated_project / "commands").exists()
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
        
        # Should only have base.py and __init__.py (no provider modules)
        py_files = list(providers_dir.glob("*.py"))
        assert len(py_files) == 2
        assert all(f.name in ["base.py", "__init__.py"] for f in py_files)

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
        
        # Selected providers should exist
        assert (providers_dir / "claude.py").exists()
        assert (providers_dir / "aider.py").exists()
        
        # Unselected providers should NOT exist
        assert not (providers_dir / "cursor.py").exists()
        assert not (providers_dir / "windsurf.py").exists()
        assert not (providers_dir / "copilot.py").exists()
        assert not (providers_dir / "codex.py").exists()
        
        # Base files should still exist
        assert (providers_dir / "base.py").exists()
        assert (providers_dir / "__init__.py").exists()

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
        
        # Should NOT have these optional features
        assert not (generated_project / "staging").exists()
        assert not (generated_project / "commands").exists()
        assert not (generated_project / "ai_conventions" / "domain_resolver.py").exists()
        
        # Should still have core files
        assert (generated_project / "global.md").exists()
        assert (generated_project / "install.py").exists()
        assert (generated_project / "README.md").exists()
        
        # Aider-specific files should exist
        assert (generated_project / "CONVENTIONS.md").exists()
        assert (generated_project / ".aider.conf.yml").exists()