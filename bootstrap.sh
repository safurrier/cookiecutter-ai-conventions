#!/bin/bash
# bootstrap.sh - Installer for cookiecutter-ai-conventions

set -e

# Parse arguments
VERBOSE=false
USE_TUI=true
COOKIECUTTER_ARGS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --no-tui)
            USE_TUI=false
            shift
            ;;
        *)
            COOKIECUTTER_ARGS+=("$1")
            shift
            ;;
    esac
done

# Verbose logging function
log_verbose() {
    if [[ "$VERBOSE" == true ]]; then
        echo "[VERBOSE] $1"
    fi
}

# Check if uv is installed
if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv package manager..."
    log_verbose "Downloading uv installer from https://astral.sh/uv/install.sh"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    log_verbose "Added uv to PATH: $PATH"
else
    log_verbose "uv is already installed at: $(which uv)"
fi

# Run cookiecutter with all arguments passed through
echo "Creating your AI conventions repository..."
log_verbose "Running: uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions ${COOKIECUTTER_ARGS[*]}"
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions "${COOKIECUTTER_ARGS[@]}"

# Check if generation was successful
if [[ $? -eq 0 ]]; then
    echo
    log_verbose "Cookiecutter generation completed successfully"
    echo "Success! Your AI conventions repository is ready."
    echo
    
    # Find the generated directory (get the last created directory)
    project_dir=$(find . -maxdepth 1 -type d -name "*conventions*" -o -name "*ai*" | head -1)
    
    if [[ -n "$project_dir" && "$USE_TUI" == true ]]; then
        echo "Launching installation TUI..."
        log_verbose "Launching TUI from directory: $project_dir"
        cd "$project_dir"
        
        # Install the package and run TUI
        if uv tool install . >/dev/null 2>&1; then
            log_verbose "Package installed successfully"
            if command -v python3 >/dev/null 2>&1; then
                python3 install.py --tui
            else
                python install.py --tui
            fi
        else
            log_verbose "Failed to install package, falling back to direct TUI"
            if command -v python3 >/dev/null 2>&1; then
                python3 install.py --tui
            else
                python install.py --tui
            fi
        fi
        cd ..
    else
        echo "Next steps:"
        echo "  1. cd into your new repository"
        echo "  2. Run 'uv tool install .' to install CLI commands"
        echo "  3. Run 'python install.py --tui' for interactive setup"
        echo "  4. Run 'ai-conventions status' to check your setup"
    fi
    
    log_verbose "Bootstrap process completed"
else
    log_verbose "Cookiecutter generation failed with exit code: $?"
fi