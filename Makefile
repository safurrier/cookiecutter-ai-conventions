# Makefile for cookiecutter-ai-conventions

# Python version
PYTHON_VERSION ?= 3.12

# Documentation server port (change if 8234 conflicts)
DOCS_PORT ?= 8234

# UV installer
UV_INSTALLER_URL := https://astral.sh/uv/install.sh
UV := $(shell which uv 2>/dev/null)

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)cookiecutter-ai-conventions$(NC)"
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

.PHONY: install-uv
install-uv: ## Install UV if not already installed
	@if [ -z "$(UV)" ]; then \
		echo "$(BLUE)Installing UV...$(NC)"; \
		curl -LsSf $(UV_INSTALLER_URL) | sh; \
	else \
		echo "$(GREEN)UV is already installed at $(UV)$(NC)"; \
	fi

.PHONY: setup
setup: install-uv ## Set up development environment
	@echo "$(BLUE)Setting up development environment...$(NC)"
	uv venv --python $(PYTHON_VERSION)
	uv pip install -e ".[dev]"
	uv run pre-commit install
	@echo "$(GREEN)Development environment ready!$(NC)"

.PHONY: test
test: ## Run tests with coverage
	@echo "$(BLUE)Running tests...$(NC)"
	@echo "$(YELLOW)Running parallel tests...$(NC)"
	uv run pytest -n auto -m "not serial"
	@echo "$(YELLOW)Running serial tests...$(NC)"
	uv run pytest -m "serial"

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	uv run pytest-watch

.PHONY: lint
lint: ## Run linting with ruff
	@echo "$(BLUE)Running linter...$(NC)"
	uv run ruff check .

.PHONY: format
format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	uv run ruff format .
	uv run ruff check --fix .

.PHONY: mypy
mypy: ## Run type checking with mypy
	@echo "$(BLUE)Running type checker...$(NC)"
	uv run mypy hooks tests

.PHONY: check
check: lint mypy test ## Run all checks (lint, type check, test)
	@echo "$(GREEN)All checks passed!$(NC)"

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks on all files
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	uv run pre-commit run --all-files

.PHONY: clean
clean: ## Clean up generated files
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf test-output/
	@echo "$(GREEN)Cleaned up!$(NC)"

.PHONY: test-cookiecutter
test-cookiecutter: ## Test the cookiecutter template generation
	@echo "$(BLUE)Testing cookiecutter template generation...$(NC)"
	rm -rf test-output
	uv run cookiecutter . --no-input -o test-output/
	@echo "$(GREEN)Template generated successfully in test-output/$(NC)"

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	@echo "$(BLUE)Running end-to-end tests...$(NC)"
	uv run pytest tests/test_e2e_cookiecutter.py -v

.PHONY: ci
ci: check ## Run CI checks (same as 'check')
	@echo "$(GREEN)CI checks passed!$(NC)"

.PHONY: ci-local
ci-local: ## Run CI checks locally (mimics GitHub Actions)
	@echo "$(BLUE)Running CI checks locally...$(NC)"
	@echo "$(YELLOW)1. Setting up environment...$(NC)"
	uv venv
	uv pip install -e ".[dev]"
	@echo "\n$(YELLOW)2. Running linter...$(NC)"
	uv run ruff check .
	@echo "\n$(YELLOW)3. Running formatter check...$(NC)"
	uv run ruff format --check .
	@echo "\n$(YELLOW)4. Running tests...$(NC)"
	uv run pytest -n auto -m "not serial"
	uv run pytest -m "serial"
	@echo "\n$(YELLOW)5. Testing cookiecutter generation...$(NC)"
	uv run cookiecutter . --no-input -o test-output/
	test -d test-output/my-ai-conventions
	@echo "\n$(GREEN)✅ All CI checks passed!$(NC)"

.PHONY: clean-output
clean-output: ## Clean test output directories
	rm -rf test-output*
	rm -rf temp-python-collab

# Documentation commands
.PHONY: docs-install
docs-install: ## Install documentation dependencies
	@echo "$(BLUE)Installing documentation dependencies...$(NC)"
	uv add --dev mkdocs-material "mkdocstrings[python]"
	@echo "$(GREEN)Documentation dependencies installed$(NC)"

.PHONY: docs-build
docs-build: ## Build documentation site
	@echo "$(BLUE)Building documentation...$(NC)"
	uv run mkdocs build --strict
	@echo "$(GREEN)Documentation built successfully$(NC)"
	@echo "📄 Site location: site/"
	@echo "🌐 Open site/index.html in your browser to view"

.PHONY: docs-serve
docs-serve: ## Serve documentation locally with live reload (accessible from network)
	@echo "$(BLUE)Starting documentation server with live reload...$(NC)"
	@echo "📍 Documentation will be available at:"
	@echo "   - Local: http://localhost:$(DOCS_PORT)"
	@echo "   - Network: http://$$(hostname -I | cut -d' ' -f1 2>/dev/null || echo "your-ip"):$(DOCS_PORT)"
	@echo "🔄 Changes will auto-reload (press Ctrl+C to stop)"
	@echo ""
	@echo "💡 To use a different port: make docs-serve DOCS_PORT=9999"
	uv run mkdocs serve --dev-addr 0.0.0.0:$(DOCS_PORT)

.PHONY: docs-check
docs-check: docs-build ## Check documentation build and links
	@echo "$(BLUE)Checking documentation...$(NC)"
	@echo "📊 Site size: $$(du -sh site/ | cut -f1)"
	@echo "📄 Pages built: $$(find site/ -name "*.html" | wc -l)"
	@echo "🔗 Checking for common issues..."
	@if grep -r "404" site/ >/dev/null 2>&1; then \
		echo "⚠️  Found potential 404 errors"; \
	else \
		echo "✅ No obvious 404 errors found"; \
	fi
	@if find site/ -name "*.html" -size 0 | grep -q .; then \
		echo "⚠️  Found empty HTML files"; \
		find site/ -name "*.html" -size 0; \
	else \
		echo "✅ No empty HTML files found"; \
	fi
	@echo "$(GREEN)Documentation check complete$(NC)"

.PHONY: docs-clean
docs-clean: ## Clean documentation build files
	@echo "$(BLUE)Cleaning documentation build files...$(NC)"
	rm -rf site/
	rm -rf .cache/
	@echo "$(GREEN)Documentation cleaned$(NC)"

# Default target
.DEFAULT_GOAL := help