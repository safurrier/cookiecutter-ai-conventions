#!/usr/bin/env bash

# Codex wrapper script for {{ cookiecutter.project_name }}
# Ensures proper context loading and convention awareness

# Check if codex is installed
if ! command -v codex &> /dev/null; then
    echo "❌ Codex CLI not found. Please install it first:"
    echo "   npm install -g @openai/codex"
    exit 1
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY environment variable not set"
    echo "   Please set your API key:"
    echo "   export OPENAI_API_KEY='your-key-here'"
    exit 1
fi

# Ensure we're in the project directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Check if AGENTS.md exists
if [ ! -f "AGENTS.md" ]; then
    echo "[WARNING] AGENTS.md not found. AI will not have project conventions."
fi

# Print startup message
echo "[INFO] Starting Codex with {{ cookiecutter.project_name }} conventions..."
echo "[INFO] Project root: $PROJECT_ROOT"
echo "[INFO] Conventions: AGENTS.md"
{%- if cookiecutter.enable_learning_capture %}
echo "[INFO] Learning capture: Enabled"
{%- endif %}
echo ""

# Start Codex with proper context
exec codex "$@"