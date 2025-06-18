"""Tests for bootstrap script removal and uvx installation documentation."""

from pathlib import Path


class TestBootstrapRemoval:
    """Test bootstrap script removal and uvx documentation."""

    def test_bootstrap_script_removed_from_template_root(self):
        """Test that bootstrap.sh has been removed from template root."""
        bootstrap_path = Path(__file__).parent.parent / "bootstrap.sh"
        assert not bootstrap_path.exists(), "bootstrap.sh should be removed from template root"

    def test_readme_mentions_uvx_after_bootstrap_removal(self):
        """Test that README mentions uvx installation after bootstrap removal."""
        readme_path = Path(__file__).parent.parent / "README.md"
        readme_content = readme_path.read_text()

        # After the fix, README should mention uvx instead of bootstrap.sh
        uvx_mentioned = "uvx cookiecutter" in readme_content
        bootstrap_mentioned = "bootstrap.sh" in readme_content

        # Now README should mention uvx and not bootstrap.sh
        assert uvx_mentioned, "README should mention uvx cookiecutter after bootstrap removal"
        assert not bootstrap_mentioned, "README should not mention bootstrap.sh after removal"

    def test_bootstrap_script_not_copied_to_generated_project(self, cookies):
        """Test that bootstrap.sh is not copied to generated projects."""
        result = cookies.bake()

        bootstrap_path = result.project_path / "bootstrap.sh"
        assert not bootstrap_path.exists(), "bootstrap.sh should not be copied to generated project"
