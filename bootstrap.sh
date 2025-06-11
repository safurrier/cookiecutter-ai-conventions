#!/bin/bash
# bootstrap.sh - Zero-dependency installer for cookiecutter-ai-conventions

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Cookiecutter AI Conventions Installer${NC}"
echo "======================================="
echo

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for uv
if ! command_exists uv; then
    echo -e "${YELLOW}📦 Installing uv package manager...${NC}"
    
    OS=$(detect_os)
    
    if [[ "$OS" == "windows" ]]; then
        # Windows installation
        echo "Detected Windows environment"
        if command_exists powershell; then
            powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
        else
            echo -e "${RED}❌ PowerShell not found. Please install uv manually:${NC}"
            echo "   https://github.com/astral-sh/uv"
            exit 1
        fi
    else
        # Unix-like installation (macOS, Linux)
        echo "Detected Unix-like environment ($OS)"
        if command_exists curl; then
            curl -LsSf https://astral.sh/uv/install.sh | sh
        elif command_exists wget; then
            wget -qO- https://astral.sh/uv/install.sh | sh
        else
            echo -e "${RED}❌ Neither curl nor wget found. Please install one of them first.${NC}"
            exit 1
        fi
        
        # Add to PATH for current session
        export PATH="$HOME/.cargo/bin:$PATH"
        
        # Source shell config if available
        if [[ -f "$HOME/.bashrc" ]]; then
            source "$HOME/.bashrc"
        elif [[ -f "$HOME/.zshrc" ]]; then
            source "$HOME/.zshrc"
        fi
    fi
    
    # Verify installation
    if ! command_exists uv; then
        echo -e "${RED}❌ Failed to install uv${NC}"
        echo "Please install manually from: https://github.com/astral-sh/uv"
        exit 1
    fi
    
    echo -e "${GREEN}✅ uv installed successfully${NC}"
else
    echo -e "${GREEN}✅ uv is already installed${NC}"
fi

# Parse command line arguments
BRANCH=""
EXTRA_ARGS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --branch=*)
            BRANCH="${1#*=}"
            shift
            ;;
        *)
            EXTRA_ARGS="$EXTRA_ARGS $1"
            shift
            ;;
    esac
done

# Run cookiecutter
echo
echo -e "${YELLOW}📝 Creating your AI conventions repository...${NC}"
echo

# Build the command
if [[ -n "$BRANCH" ]]; then
    echo "Using branch: $BRANCH"
    COOKIECUTTER_CMD="uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions --checkout \"$BRANCH\"$EXTRA_ARGS"
else
    COOKIECUTTER_CMD="uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions$EXTRA_ARGS"
fi

# Execute cookiecutter
eval $COOKIECUTTER_CMD

# Check if cookiecutter succeeded
if [[ $? -eq 0 ]]; then
    echo
    echo -e "${GREEN}✨ Success! Your AI conventions repository is ready.${NC}"
    echo
    echo "Next steps:"
    echo "  1. cd into your new repository"
    echo "  2. Run 'uv tool install .' to install CLI commands"
    echo "  3. Run 'ai-conventions status' to check your setup"
    echo "  4. Start capturing your conventions!"
    echo
    echo "Quick start:"
    echo -e "  ${BLUE}cd <your-project-name>${NC}"
    echo -e "  ${BLUE}uv tool install .${NC}"
    echo -e "  ${BLUE}ai-conventions status${NC}"
    echo
else
    echo
    echo -e "${RED}❌ Failed to create repository${NC}"
    echo "Please check the error messages above"
    exit 1
fi