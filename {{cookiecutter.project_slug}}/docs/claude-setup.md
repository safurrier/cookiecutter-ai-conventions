# Claude Code Setup Guide

This guide helps you set up your AI conventions with Claude Code.

## Installation

Your conventions are automatically installed when you run `./install.py`. Claude Code will automatically find and load your CLAUDE.md file from:

- `~/.claude/CLAUDE.md` (global conventions)
- Project-specific CLAUDE.md files

## How It Works

Claude Code uses the CLAUDE.md file to:
1. Automatically load relevant convention domains based on context
2. Apply your team's patterns and best practices
3. Capture and evolve conventions over time

## Available Commands

{% if cookiecutter.enable_learning_capture %}
### /capture-learning
Captures learnings from the current conversation. Use this when:
- You correct Claude about a preference
- A new pattern emerges
- You discover a better approach

### /review-learnings
Reviews staged learnings and promotes stable patterns to your convention domains.
{% endif %}

## Automatic Domain Loading

Claude automatically loads convention domains based on context:

{%- set domains = cookiecutter.default_domains.split(',') %}
{% for domain in domains %}
{% if domain.strip() == "git" %}
- **Git operations**: Loads git conventions when you use git commands
{% elif domain.strip() == "testing" %}
- **Testing**: Loads testing conventions when working with test files
{% elif domain.strip() == "writing" %}
- **Writing**: Loads writing conventions for docs and commit messages
{% endif %}
{% endfor %}

## Troubleshooting

### Claude isn't using my conventions
1. Check that CLAUDE.md exists in `~/.claude/`
2. Verify the file contains your domain references
3. Restart Claude Code if needed

### Commands not available
1. Ensure learning capture was enabled during setup
2. Check that `.claude/commands/` directory exists
3. Commands should appear in Claude's slash command menu

## Next Steps

1. Start coding and watch Claude apply your conventions
2. {% if cookiecutter.enable_learning_capture %}Use `/capture-learning` when you notice patterns{% else %}Manually update domains as patterns emerge{% endif %}
3. Share successful conventions back to your team