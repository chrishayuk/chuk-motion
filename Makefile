.PHONY: help install dev clean test test-fast test-unit test-integration test-watch coverage
.PHONY: lint format format-check typecheck quality check security audit
.PHONY: docs serve-docs examples build publish-test publish
.PHONY: serve debug watch update-deps check-deps freeze ci pre-commit

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Project settings
PROJECT_NAME := chuk-mcp-remotion
PYTHON := python3
UV := uv
PYTEST := pytest
RUFF := ruff
MYPY := mypy

##@ General

help: ## Display this help message
	@echo "$(BLUE)Remotion MCP Server - Development Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(BLUE)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(GREEN)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

install: ## Install project dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(UV) pip install -e .
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

dev: install ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	$(UV) pip install -e ".[dev]"
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

clean: ## Remove build artifacts and cache
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✓ Cleaned$(NC)"

##@ Testing

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	$(UV) run $(PYTEST) tests/ -v
	@echo "$(GREEN)✓ Tests passed$(NC)"

test-fast: ## Run tests in parallel
	@echo "$(BLUE)Running tests in parallel...$(NC)"
	$(UV) run $(PYTEST) tests/ -v -n auto
	@echo "$(GREEN)✓ Tests passed$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	$(UV) run $(PYTEST) tests/ -v -m "not integration"
	@echo "$(GREEN)✓ Unit tests passed$(NC)"

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	$(UV) run $(PYTEST) tests/ -v -m "integration"
	@echo "$(GREEN)✓ Integration tests passed$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	$(UV) run $(PYTEST) tests/ -v --looponfail

coverage: ## Generate test coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	$(UV) run $(PYTEST) tests/ --cov=src/chuk_mcp_remotion --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/$(NC)"

##@ Code Quality

lint: ## Run linting checks
	@echo "$(BLUE)Running linting...$(NC)"
	$(UV) run $(RUFF) check src/ tests/
	@echo "$(GREEN)✓ Linting passed$(NC)"

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	$(UV) run $(RUFF) format src/ tests/
	$(UV) run $(RUFF) check --fix src/ tests/
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Check code formatting without changes
	@echo "$(BLUE)Checking code formatting...$(NC)"
	$(UV) run $(RUFF) format --check src/ tests/
	@echo "$(GREEN)✓ Formatting check passed$(NC)"

typecheck: ## Run type checking with mypy
	@echo "$(BLUE)Running type checks...$(NC)"
	$(UV) run $(MYPY) src/chuk_mcp_remotion
	@echo "$(GREEN)✓ Type checking passed$(NC)"

quality: lint format-check typecheck ## Run all quality checks
	@echo "$(GREEN)✓ All quality checks passed$(NC)"

check: lint typecheck test ## Run all checks (lint, typecheck, test)
	@echo "$(GREEN)✓ All checks passed$(NC)"

##@ Security

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	@echo "$(YELLOW)Note: Install bandit and safety for security checks$(NC)"
	@echo "  pip install bandit safety"
	@which bandit > /dev/null && bandit -r src/ || echo "$(YELLOW)⚠ bandit not installed$(NC)"
	@which safety > /dev/null && safety check || echo "$(YELLOW)⚠ safety not installed$(NC)"

audit: security ## Alias for security checks

##@ Documentation

docs: ## Build documentation
	@echo "$(BLUE)Building documentation...$(NC)"
	@echo "$(YELLOW)Documentation in docs/ folder$(NC)"
	@ls -la docs/
	@echo "$(GREEN)✓ Documentation available$(NC)"

serve-docs: ## Serve documentation locally
	@echo "$(BLUE)Serving documentation...$(NC)"
	@echo "$(YELLOW)Opening docs in browser...$(NC)"
	@open docs/themes.md || xdg-open docs/themes.md || echo "View docs/themes.md"

##@ Examples

examples: ## Run all example scripts
	@echo "$(BLUE)Running examples...$(NC)"
	@for example in examples/*.py; do \
		echo "$(YELLOW)Running $$example...$(NC)"; \
		$(UV) run $(PYTHON) $$example || exit 1; \
	done
	@echo "$(GREEN)✓ All examples ran successfully$(NC)"

example-simple: ## Run a simple example
	@echo "$(BLUE)Running simple example...$(NC)"
	$(UV) run $(PYTHON) examples/explore_design_system.py
	@echo "$(GREEN)✓ Example completed$(NC)"

example-code: ## Run code display example
	@echo "$(BLUE)Running code display example...$(NC)"
	$(UV) run $(PYTHON) examples/code_display.py
	@echo "$(GREEN)✓ Example completed$(NC)"

example-preview: ## Run preview generation example
	@echo "$(BLUE)Running preview generation example...$(NC)"
	$(UV) run $(PYTHON) examples/generate_preview.py
	@echo "$(GREEN)✓ Example completed$(NC)"

##@ Build & Deploy

build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	$(PYTHON) -m build
	@echo "$(GREEN)✓ Build complete$(NC)"
	@ls -lh dist/

publish-test: build ## Publish to TestPyPI
	@echo "$(BLUE)Publishing to TestPyPI...$(NC)"
	$(PYTHON) -m twine upload --repository testpypi dist/*
	@echo "$(GREEN)✓ Published to TestPyPI$(NC)"

publish: build ## Publish to PyPI
	@echo "$(RED)Publishing to PyPI...$(NC)"
	@echo "$(YELLOW)Are you sure? This will publish to production PyPI.$(NC)"
	@read -p "Type 'yes' to continue: " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		$(PYTHON) -m twine upload dist/*; \
		echo "$(GREEN)✓ Published to PyPI$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

##@ Development Workflow

serve: ## Run the MCP server in HTTP mode
	@echo "$(BLUE)Starting MCP server...$(NC)"
	$(UV) run $(PYTHON) -m $(PROJECT_NAME).server http --port 8000

serve-stdio: ## Run the MCP server in STDIO mode
	@echo "$(BLUE)Starting MCP server (STDIO mode)...$(NC)"
	$(UV) run $(PYTHON) -m $(PROJECT_NAME).server stdio

debug: ## Run server with debug logging
	@echo "$(BLUE)Starting MCP server with debug logging...$(NC)"
	MCP_LOG_LEVEL=DEBUG $(UV) run $(PYTHON) -m $(PROJECT_NAME).server http --port 8000

watch: ## Watch for changes and run tests
	@echo "$(BLUE)Watching for changes...$(NC)"
	$(UV) run $(PYTEST) tests/ -v --looponfail

##@ Dependencies

update-deps: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	$(UV) pip list --outdated
	@echo "$(YELLOW)Run 'uv pip install --upgrade <package>' to update$(NC)"

check-deps: ## Check for outdated dependencies
	@echo "$(BLUE)Checking dependencies...$(NC)"
	$(UV) pip list --outdated

freeze: ## Freeze current dependencies
	@echo "$(BLUE)Freezing dependencies...$(NC)"
	$(UV) pip freeze > requirements-frozen.txt
	@echo "$(GREEN)✓ Dependencies frozen to requirements-frozen.txt$(NC)"

##@ CI/CD

ci: quality test ## Run CI checks (quality + tests)
	@echo "$(GREEN)✓ CI checks passed$(NC)"

pre-commit: format lint ## Run pre-commit checks
	@echo "$(GREEN)✓ Pre-commit checks passed$(NC)"

##@ Quick Commands

q: quality ## Quick alias for quality checks
t: test ## Quick alias for test
f: format ## Quick alias for format
s: serve ## Quick alias for serve

# Default target
.DEFAULT_GOAL := help
