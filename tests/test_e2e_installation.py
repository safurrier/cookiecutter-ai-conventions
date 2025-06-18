"""End-to-end installation tests for complete workflow validation.

These tests verify the entire installation flow from cookiecutter generation
through provider installation.
"""

import subprocess
import sys
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


class TestE2EInstallation:
    """Test complete installation workflows end-to-end."""

    def test_single_provider_installation(self, tmp_path):
        """Test installation with single provider."""
        # Generate project
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_name": "Test Single Provider",
                "project_slug": "test-single-provider",
                "selected_providers": "claude",
                "default_domains": "git,testing",
                "enable_learning_capture": True,
            },
        )

        generated_project = Path(project_dir)

        # Verify generated structure
        assert generated_project.exists()
        assert (generated_project / "install.py").exists()
        assert (generated_project / "global.md").exists()
        assert (generated_project / "domains" / "git" / "core.md").exists()
        assert (generated_project / "domains" / "testing" / "core.md").exists()

        # Verify Claude-specific files (created by cookiecutter, not install)
        # Note: CLAUDE.md is created by running install.py, not by cookiecutter
        assert (generated_project / "templates" / "claude" / "CLAUDE.md.j2").exists()
        assert (generated_project / "commands").exists()
        assert (generated_project / "commands" / "capture-learning.md").exists()

        # Verify no other provider files exist
        assert not (generated_project / ".cursorrules").exists()
        assert not (generated_project / ".windsurfrules").exists()
        assert not (generated_project / "CONVENTIONS.md").exists()

        # Verify ALL provider modules exist (improved architecture)
        providers_dir = generated_project / "ai_conventions" / "providers"
        assert (providers_dir / "claude.py").exists()
        assert (providers_dir / "cursor.py").exists()  # Keep all Python modules
        assert (providers_dir / "windsurf.py").exists()
        assert (providers_dir / "aider.py").exists()
        assert (providers_dir / "copilot.py").exists()
        assert (providers_dir / "codex.py").exists()

    def test_multiple_provider_installation(self, tmp_path):
        """Test installation with multiple providers."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_name": "Test Multi Provider",
                "project_slug": "test-multi-provider",
                "selected_providers": "claude,cursor,windsurf",
                "default_domains": "git,testing,writing",
                "enable_learning_capture": True,
            },
        )

        generated_project = Path(project_dir)

        # Verify Claude template exists (only Claude has templates in cookiecutter)
        assert (generated_project / "templates" / "claude" / "CLAUDE.md.j2").exists()

        # Verify install.py exists which will create provider-specific files
        assert (generated_project / "install.py").exists()

        # Verify domains
        domains_dir = generated_project / "domains"
        assert (domains_dir / "git" / "core.md").exists()
        assert (domains_dir / "testing" / "core.md").exists()
        assert (domains_dir / "writing" / "core.md").exists()

        # Verify ALL provider modules exist (improved architecture - keep all Python modules)
        providers_dir = generated_project / "ai_conventions" / "providers"
        assert (providers_dir / "claude.py").exists()
        assert (providers_dir / "cursor.py").exists()
        assert (providers_dir / "windsurf.py").exists()
        assert (providers_dir / "aider.py").exists()  # Keep all Python modules
        assert (providers_dir / "copilot.py").exists()
        assert (providers_dir / "codex.py").exists()

        # But config files for unselected providers should NOT exist
        assert (generated_project / ".claude").exists()  # Claude selected
        assert (generated_project / ".cursorrules").exists()  # Cursor selected
        assert (generated_project / ".windsurfrules").exists()  # Windsurf selected
        assert not (generated_project / "CONVENTIONS.md").exists()  # Aider not selected
        assert not (generated_project / ".aider.conf.yml").exists()  # Aider not selected

    def test_minimal_installation(self, tmp_path):
        """Test minimal installation with all features disabled."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_name": "Test Minimal",
                "project_slug": "test-minimal",
                "selected_providers": "claude",
                "default_domains": "git",
                "enable_learning_capture": False,
                "enable_context_canary": False,
                "enable_domain_composition": False,
            },
        )

        generated_project = Path(project_dir)

        # Verify basic structure exists
        assert (generated_project / "install.py").exists()
        assert (generated_project / "global.md").exists()
        assert (generated_project / "templates" / "claude" / "CLAUDE.md.j2").exists()

        # Verify learning capture is always available (improved UX)
        # staging removed - direct domain capture now
        assert not (generated_project / "staging").exists()
        assert (generated_project / "commands").exists()
        
        # Domain composition can still be disabled
        assert not (generated_project / "ai_conventions" / "domain_resolver.py").exists()

        # With canary disabled, the template should not include canary content
        # but the template file itself will still have the conditional logic
        # We can verify the feature is disabled by checking the post-generation output

    def test_all_provider_combinations_generate_correctly(self, tmp_path):
        """Test that all individual providers generate correctly."""
        providers = ["claude", "cursor", "windsurf", "aider", "copilot", "codex"]

        for provider in providers:
            output_dir = tmp_path / f"output_{provider}"
            output_dir.mkdir()

            project_dir = cookiecutter(
                str(Path.cwd()),
                no_input=True,
                output_dir=str(output_dir),
                extra_context={
                    "project_name": f"Test {provider.capitalize()}",
                    "project_slug": f"test-{provider}",
                    "selected_providers": provider,
                },
            )

            generated_project = Path(project_dir)
            assert generated_project.exists(), f"Failed to generate project for {provider}"

            # Verify Claude template exists (only Claude has templates)
            if provider == "claude":
                assert (generated_project / "templates" / "claude" / "CLAUDE.md.j2").exists()

            # All providers should have install.py
            assert (generated_project / "install.py").exists()

            # Verify ALL provider modules exist (improved architecture)
            providers_dir = generated_project / "ai_conventions" / "providers"
            for check_provider in providers:
                assert (providers_dir / f"{check_provider}.py").exists()
            
            # Also verify base modules always exist
            assert (providers_dir / "base.py").exists()
            assert (providers_dir / "__init__.py").exists()

    @pytest.mark.slow
    def test_full_installation_with_subprocess(self, tmp_path):
        """Test full installation using subprocess to simulate real usage."""
        # This test actually runs cookiecutter as a subprocess
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "cookiecutter",
                ".",
                "--no-input",
                f"--output-dir={tmp_path}",
                "project_name=Test Subprocess",
                "project_slug=test-subprocess",
                "selected_providers=claude,cursor",
                "default_domains=git,testing",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Cookiecutter failed: {result.stderr}"

        # Verify project was created
        project_dir = tmp_path / "test-subprocess"
        assert project_dir.exists()

        # Verify basic structure
        assert (project_dir / "templates" / "claude" / "CLAUDE.md.j2").exists()
        assert (project_dir / "domains" / "git" / "core.md").exists()
        assert (project_dir / "install.py").exists()

        # Verify provider modules based on selection
        providers_dir = project_dir / "ai_conventions" / "providers"
        assert (providers_dir / "claude.py").exists()
        assert (providers_dir / "cursor.py").exists()

    def test_uvx_installation_workflow(self, tmp_path):
        """Test that uvx installation approach is documented in README."""
        # We now use uvx instead of bootstrap.sh
        readme_path = Path("README.md")
        assert readme_path.exists()

        content = readme_path.read_text(encoding="utf-8")
        assert "uvx cookiecutter" in content
        # Ensure we don't have any references to the old bootstrap method
        assert "bootstrap.sh" not in content
        assert "cookiecutter" in content
        assert "uv" in content

    def test_provider_file_structure_matches_specification(self, tmp_path):
        """Test that generated files match the expected structure for each provider."""
        test_cases = [
            {
                "provider": "claude",
                "expected_files": [
                    "templates/claude/CLAUDE.md.j2",
                    "ai_conventions/providers/claude.py",
                    "install.py",
                ],
            },
            {
                "provider": "cursor",
                "expected_files": [
                    "ai_conventions/providers/cursor.py",
                    "install.py",
                ],
            },
            {
                "provider": "windsurf",
                "expected_files": [
                    "ai_conventions/providers/windsurf.py",
                    "install.py",
                ],
            },
            {
                "provider": "aider",
                "expected_files": [
                    "ai_conventions/providers/aider.py",
                    "install.py",
                ],
            },
        ]

        for test_case in test_cases:
            output_dir = tmp_path / f"test_{test_case['provider']}"
            output_dir.mkdir()

            project_dir = cookiecutter(
                str(Path.cwd()),
                no_input=True,
                output_dir=str(output_dir),
                extra_context={
                    "project_slug": f"test-{test_case['provider']}",
                    "selected_providers": test_case["provider"],
                    "default_domains": "git,testing",
                    "enable_learning_capture": True,
                },
            )

            generated_project = Path(project_dir)

            for expected_file in test_case["expected_files"]:
                file_path = generated_project / expected_file
                assert file_path.exists(), f"Missing {expected_file} for {test_case['provider']}"

            # Check learning capture files when enabled
            if test_case["provider"] == "claude":
                assert (generated_project / "commands" / "capture-learning.md").exists()
                assert (generated_project / "commands" / "review-learnings.md").exists()

    def test_performance_under_2_minutes(self, tmp_path):
        """Test that generation completes in under 2 minutes."""
        import time

        start_time = time.time()

        # Generate project with all features enabled
        project_dir = cookiecutter(
            str(Path.cwd()),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context={
                "project_slug": "test-performance",
                "selected_providers": "claude,cursor,windsurf",
                "default_domains": "git,testing,writing",
                "enable_learning_capture": True,
                "enable_context_canary": True,
                "enable_domain_composition": True,
            },
        )

        end_time = time.time()
        duration = end_time - start_time

        assert duration < 120, f"Generation took {duration:.2f} seconds, exceeding 2 minute limit"
        assert Path(project_dir).exists()
