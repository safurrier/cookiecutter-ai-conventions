"""Test shorthand domain syntax resolution."""

import sys
from pathlib import Path

# Add the cookiecutter project directory to the path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "{{cookiecutter.project_slug}}"))

from ai_conventions.domain_resolver import resolve_shorthand_syntax


class TestShorthandSyntax:
    """Test shorthand domain syntax resolution."""

    def test_basic_domain_shorthand(self):
        """Test basic domain shorthand resolves correctly."""
        content = "Load %writing conventions for this task."
        expected = "Load @domains/writing/core.md conventions for this task."
        assert resolve_shorthand_syntax(content) == expected

    def test_domain_section_shorthand(self):
        """Test domain section shorthand resolves correctly."""
        content = "Follow %writing%commit-messages when creating commits."
        expected = "Follow @domains/writing/commit-messages.md when creating commits."
        assert resolve_shorthand_syntax(content) == expected

    def test_multiple_shorthand_references(self):
        """Test multiple shorthand references in same content."""
        content = "Use %git for version control and %testing%unit-tests for testing."
        expected = "Use @domains/git/core.md for version control and @domains/testing/unit-tests.md for testing."
        assert resolve_shorthand_syntax(content) == expected

    def test_mixed_shorthand_and_regular_syntax(self):
        """Test shorthand works alongside existing @domains syntax."""
        content = "Load @domains/python/core.md and %writing%pr-summaries for this PR."
        expected = "Load @domains/python/core.md and @domains/writing/pr-summaries.md for this PR."
        assert resolve_shorthand_syntax(content) == expected

    def test_shorthand_with_hyphens_and_underscores(self):
        """Test shorthand works with hyphens and underscores in names."""
        content = "Use %web-api%error-handling and %database_queries patterns."
        expected = (
            "Use @domains/web-api/error-handling.md and @domains/database_queries/core.md patterns."
        )
        assert resolve_shorthand_syntax(content) == expected

    def test_no_shorthand_syntax_unchanged(self):
        """Test content without shorthand syntax remains unchanged."""
        content = "Regular text with @domains/git/core.md and no shorthand."
        assert resolve_shorthand_syntax(content) == content

    def test_malformed_shorthand_unchanged(self):
        """Test malformed shorthand syntax remains unchanged."""
        content = "Malformed %% or %domain%% syntax should not change."
        assert resolve_shorthand_syntax(content) == content

    def test_shorthand_at_start_and_end(self):
        """Test shorthand syntax at start and end of content."""
        content = "%writing is important for %testing%e2e"
        expected = "@domains/writing/core.md is important for @domains/testing/e2e.md"
        assert resolve_shorthand_syntax(content) == expected

    def test_complex_document_with_shorthand(self):
        """Test complex document with multiple shorthand references."""
        content = """
        # Project Conventions
        
        Follow %git%branching for branch naming.
        Use %testing patterns for all tests.
        Apply %writing%commit-messages for commits.
        
        Also load @domains/python/core.md as usual.
        """  # noqa: W293

        expected = """
        # Project Conventions
        
        Follow @domains/git/branching.md for branch naming.
        Use @domains/testing/core.md patterns for all tests.
        Apply @domains/writing/commit-messages.md for commits.
        
        Also load @domains/python/core.md as usual.
        """  # noqa: W293

        assert resolve_shorthand_syntax(content) == expected
