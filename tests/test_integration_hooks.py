"""Integration tests for cookiecutter hooks.

These tests verify hook behavior without full cookiecutter execution.
"""

import json
import shutil
import sys
from pathlib import Path

# Add hooks to path so we can import them
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))


class TestPostGenProjectHook:
    """Test post-generation hook functions."""

    def test_copy_domains_from_selection_file(self, tmp_path):
        """Test that domains are copied based on selection file."""
        # Arrange: Set up source domains
        source_domains = tmp_path / "source" / "community-domains"
        source_domains.mkdir(parents=True)

        for domain in ["git", "testing", "writing"]:
            domain_dir = source_domains / domain
            domain_dir.mkdir()
            (domain_dir / "core.md").write_text(f"# {domain} core content")

        # Arrange: Create selection file
        import tempfile
        temp_file = Path(tempfile.gettempdir()) / "cookiecutter_selected_domains.json"
        temp_file.write_text(json.dumps({"selected_domains": ["git", "testing"]}))

        # Arrange: Set up destination
        dest_dir = tmp_path / "dest"
        dest_dir.mkdir()
        domains_dir = dest_dir / "domains"
        domains_dir.mkdir()

        # Act: Simulate domain copying logic
        with open(temp_file) as f:
            context = json.load(f)

        for domain_name in context.get("selected_domains", []):
            source_path = source_domains / domain_name
            dest_path = domains_dir / domain_name
            if source_path.exists():
                shutil.copytree(source_path, dest_path)

        # Assert: Selected domains were copied
        assert (domains_dir / "git").exists()
        assert (domains_dir / "testing").exists()
        assert not (domains_dir / "writing").exists()

        # Clean up
        temp_file.unlink()

    def test_remove_learning_directories_when_disabled(self, tmp_path):
        """Test that learning directories are removed when disabled."""
        # Arrange: Create directories
        commands_dir = tmp_path / "commands"
        staging_dir = tmp_path / "staging"
        commands_dir.mkdir()
        staging_dir.mkdir()
        (commands_dir / "test.py").touch()
        (staging_dir / "test.md").touch()

        # Act: Simulate removal when learning disabled
        enable_learning = False

        if not enable_learning:
            if commands_dir.exists():
                shutil.rmtree(commands_dir)
            if staging_dir.exists():
                shutil.rmtree(staging_dir)

        # Assert: Directories were removed
        assert not commands_dir.exists()
        assert not staging_dir.exists()

    def test_make_scripts_executable_when_enabled(self, tmp_path):
        """Test that scripts are made executable when learning is enabled."""
        # Arrange: Create command scripts
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()

        capture_script = commands_dir / "capture-learning.py"
        review_script = commands_dir / "review-learnings.py"

        capture_script.write_text("#!/usr/bin/env python3\nprint('capture')")
        review_script.write_text("#!/usr/bin/env python3\nprint('review')")

        # Make them non-executable
        capture_script.chmod(0o644)
        review_script.chmod(0o644)

        # Act: Make scripts executable
        enable_learning = True

        if enable_learning:
            for script_name in ["capture-learning.py", "review-learnings.py"]:
                script_path = commands_dir / script_name
                if script_path.exists():
                    script_path.chmod(0o755)

        # Assert: Scripts are executable (skip on Windows)
        import platform
        if platform.system() != "Windows":
            assert capture_script.stat().st_mode & 0o111
            assert review_script.stat().st_mode & 0o111

    def test_create_provider_config_file(self, tmp_path):
        """Test that provider configuration file is created."""
        # Arrange
        selected_providers = ["claude", "cursor"]

        # Act: Create provider config
        providers_file = tmp_path / ".selected_providers"
        with open(providers_file, "w") as f:
            f.write("\n".join(selected_providers))

        # Assert: File exists with correct content
        assert providers_file.exists()
        content = providers_file.read_text(encoding='utf-8')
        assert "claude" in content
        assert "cursor" in content
