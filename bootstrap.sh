#!/bin/bash
# bootstrap.sh - Installer for cookiecutter-ai-conventions

set -e

# Function to ensure uv is available
ensure_uv() {
    if ! command -v uv >/dev/null 2>&1; then
        echo "Installing uv package manager..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        
        # Add to PATH for current session
        export PATH="$HOME/.cargo/bin:$PATH"
        export PATH="$HOME/.local/bin:$PATH"
        
        # Verify installation
        if ! command -v uv >/dev/null 2>&1; then
            echo "Error: uv installation failed"
            exit 1
        fi
    fi
}

# Ensure uv is available
ensure_uv

# Run cookiecutter with all arguments passed through
echo "Creating your AI conventions repository..."
if uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions "$@"; then
    echo
    echo "Success! Your AI conventions repository is ready."
    echo
    echo "Next steps:"
    echo "  1. cd into your new repository"
    echo "  2. Run 'uv tool install .' to install CLI commands"
    echo "  3. Run 'ai-conventions status' to check your setup"
fi