#!/bin/bash
# bootstrap.sh - Zero dependency setup for cookiecutter-ai-conventions

set -e  # Exit on error

echo "🚀 Setting up cookiecutter-ai-conventions..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH for current session
    if [ -f "$HOME/.cargo/env" ]; then
        source "$HOME/.cargo/env"
    fi
    
    echo "✅ uv installed successfully"
fi

# Run cookiecutter using uvx (no installation needed)
echo "🏗️  Creating your AI conventions repository..."
uvx cookiecutter gh:yourusername/cookiecutter-ai-conventions "$@"

echo "✨ Setup complete! Check the generated directory for next steps."
