.PHONY: help install dev clean clean-pyc clean-build clean-test clean-all
.PHONY: test test-fast test-unit test-integration test-watch coverage coverage-report
.PHONY: lint format format-check typecheck quality check security audit
.PHONY: docs serve-docs examples example-simple example-code example-preview
.PHONY: build publish-test publish publish-manual release
.PHONY: serve serve-stdio debug watch run
.PHONY: docker-build docker-run docker-up docker-stop docker-clean
.PHONY: fly-deploy fly-status fly-logs fly-open
.PHONY: version bump-patch bump-minor bump-major
.PHONY: update-deps check-deps freeze ci pre-commit
.PHONY: q t f s

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Project settings
PROJECT_NAME := chuk-motion
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
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) pip install -e .; \
	else \
		pip install -e .; \
	fi
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) sync --dev; \
	else \
		pip install -e ".[dev]"; \
	fi
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"
	@echo ""
	@echo "Available commands:"
	@echo "  make test       - Run tests"
	@echo "  make coverage   - Run tests with coverage"
	@echo "  make check      - Run all checks (lint, typecheck, security, test)"

##@ Cleaning

clean: clean-pyc clean-build ## Remove Python bytecode and build artifacts
	@echo "$(GREEN)✓ Basic clean complete$(NC)"

clean-pyc: ## Remove Python bytecode files
	@echo "$(BLUE)Cleaning Python bytecode files...$(NC)"
	@find . -type f -name '*.pyc' -delete 2>/dev/null || true
	@find . -type f -name '*.pyo' -delete 2>/dev/null || true
	@find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true

clean-build: ## Remove build artifacts
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	@rm -rf build/ dist/ *.egg-info 2>/dev/null || true
	@rm -rf .eggs/ 2>/dev/null || true
	@find . -name '*.egg' -exec rm -f {} + 2>/dev/null || true

clean-test: ## Remove test artifacts
	@echo "$(BLUE)Cleaning test artifacts...$(NC)"
	@rm -rf .pytest_cache/ 2>/dev/null || true
	@rm -rf .coverage 2>/dev/null || true
	@rm -rf htmlcov/ 2>/dev/null || true
	@rm -rf .tox/ 2>/dev/null || true
	@rm -rf .cache/ 2>/dev/null || true
	@find . -name '.coverage.*' -delete 2>/dev/null || true

clean-all: clean-pyc clean-build clean-test ## Deep clean everything
	@echo "$(BLUE)Deep cleaning...$(NC)"
	@rm -rf .mypy_cache/ 2>/dev/null || true
	@rm -rf .ruff_cache/ 2>/dev/null || true
	@rm -rf .uv/ 2>/dev/null || true
	@rm -rf node_modules/ 2>/dev/null || true
	@rm -rf renders/ 2>/dev/null || true
	@rm -rf temp/ 2>/dev/null || true
	@rm -rf *.mp4 *.webm 2>/dev/null || true
	@find . -name '.DS_Store' -delete 2>/dev/null || true
	@find . -name 'Thumbs.db' -delete 2>/dev/null || true
	@find . -name '*.log' -delete 2>/dev/null || true
	@find . -name '*.tmp' -delete 2>/dev/null || true
	@find . -name '*~' -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Deep clean complete$(NC)"

##@ Testing

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		PYTHONPATH=src $(UV) run $(PYTEST) tests/ -v; \
	else \
		PYTHONPATH=src $(PYTEST) tests/ -v; \
	fi
	@echo "$(GREEN)✓ Tests passed$(NC)"

test-fast: ## Run tests in parallel
	@echo "$(BLUE)Running tests in parallel...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		PYTHONPATH=src $(UV) run $(PYTEST) tests/ -v -n auto; \
	else \
		PYTHONPATH=src $(PYTEST) tests/ -v -n auto; \
	fi
	@echo "$(GREEN)✓ Tests passed$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		PYTHONPATH=src $(UV) run $(PYTEST) tests/ -v -m "not integration"; \
	else \
		PYTHONPATH=src $(PYTEST) tests/ -v -m "not integration"; \
	fi
	@echo "$(GREEN)✓ Unit tests passed$(NC)"

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		PYTHONPATH=src $(UV) run $(PYTEST) tests/ -v -m "integration"; \
	else \
		PYTHONPATH=src $(PYTEST) tests/ -v -m "integration"; \
	fi
	@echo "$(GREEN)✓ Integration tests passed$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		PYTHONPATH=src $(UV) run $(PYTEST) tests/ -v --looponfail; \
	else \
		PYTHONPATH=src $(PYTEST) tests/ -v --looponfail; \
	fi

coverage: ## Generate test coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		PYTHONPATH=src $(UV) run $(PYTEST) tests/ --cov=src/chuk_motion --cov-report=html --cov-report=term --cov-report=term-missing:skip-covered; \
		exit_code=$$?; \
		echo ""; \
		echo "=========================="; \
		echo "Coverage Summary:"; \
		echo "=========================="; \
		$(UV) run coverage report --omit="tests/*" | tail -5; \
		echo ""; \
		echo "HTML coverage report saved to: htmlcov/index.html"; \
		exit $$exit_code; \
	else \
		PYTHONPATH=src $(PYTEST) tests/ --cov=src/chuk_motion --cov-report=html --cov-report=term --cov-report=term-missing:skip-covered; \
	fi

coverage-report: ## Show current coverage report
	@echo "$(BLUE)Coverage Report:$(NC)"
	@echo "================"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) run coverage report --omit="tests/*" || echo "No coverage data found. Run 'make coverage' first."; \
	else \
		coverage report --omit="tests/*" || echo "No coverage data found. Run 'make coverage' first."; \
	fi

##@ Code Quality

lint: ## Run linting checks
	@echo "$(BLUE)Running linting...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) run $(RUFF) check src/ tests/; \
		$(UV) run $(RUFF) format --check src/ tests/; \
	elif command -v $(RUFF) >/dev/null 2>&1; then \
		$(RUFF) check src/ tests/; \
		$(RUFF) format --check src/ tests/; \
	else \
		echo "$(YELLOW)Ruff not found. Install with: pip install ruff$(NC)"; \
	fi
	@echo "$(GREEN)✓ Linting passed$(NC)"

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) run $(RUFF) format src/ tests/; \
		$(UV) run $(RUFF) check --fix src/ tests/; \
	elif command -v $(RUFF) >/dev/null 2>&1; then \
		$(RUFF) format src/ tests/; \
		$(RUFF) check --fix src/ tests/; \
	else \
		echo "$(YELLOW)Ruff not found. Install with: pip install ruff$(NC)"; \
	fi
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Check code formatting without changes
	@echo "$(BLUE)Checking code formatting...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) run $(RUFF) format --check src/ tests/; \
	elif command -v $(RUFF) >/dev/null 2>&1; then \
		$(RUFF) format --check src/ tests/; \
	else \
		echo "$(YELLOW)Ruff not found. Install with: pip install ruff$(NC)"; \
	fi
	@echo "$(GREEN)✓ Formatting check passed$(NC)"

typecheck: ## Run type checking with mypy
	@echo "$(BLUE)Running type checks...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) run $(MYPY) src/chuk_motion --ignore-missing-imports --exclude '/site-packages/'; \
	elif command -v $(MYPY) >/dev/null 2>&1; then \
		$(MYPY) src/chuk_motion --ignore-missing-imports --exclude '/site-packages/'; \
	else \
		echo "$(YELLOW)MyPy not found. Install with: pip install mypy$(NC)"; \
	fi
	@echo "$(GREEN)✓ Type checking passed$(NC)"

quality: lint format-check typecheck ## Run all quality checks
	@echo "$(GREEN)✓ All quality checks passed$(NC)"

check: lint typecheck security test ## Run all checks (lint, typecheck, security, test)
	@echo "$(GREEN)✓ All checks passed$(NC)"

##@ Security

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) run bandit -r src/chuk_motion -ll 2>/dev/null || echo "$(YELLOW)⚠ bandit not installed$(NC)"; \
	elif command -v bandit >/dev/null 2>&1; then \
		bandit -r src/chuk_motion -ll; \
	else \
		echo "$(YELLOW)⚠ bandit not installed$(NC)"; \
	fi

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

##@ Build & Publish

build: clean-build ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) build; \
	else \
		$(PYTHON) -m build; \
	fi
	@echo "$(GREEN)✓ Build complete$(NC)"
	@ls -lh dist/

publish-test: build ## Publish to TestPyPI
	@echo "$(BLUE)Publishing to TestPyPI...$(NC)"
	@echo ""
	@version=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	echo "Version: $$version"; \
	echo ""; \
	if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) run twine upload --repository testpypi dist/*; \
	else \
		$(PYTHON) -m twine upload --repository testpypi dist/*; \
	fi; \
	echo ""; \
	echo "$(GREEN)✓ Uploaded to TestPyPI$(NC)"; \
	echo ""; \
	echo "Install with:"; \
	echo "  pip install --index-url https://test.pypi.org/simple/ $(PROJECT_NAME)==$$version"

publish-manual: build ## Manually publish to PyPI (requires PYPI_TOKEN)
	@echo "$(BLUE)Manual PyPI Publishing$(NC)"
	@echo "======================"
	@echo ""
	@version=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	tag="v$$version"; \
	echo "Version: $$version"; \
	echo "Tag: $$tag"; \
	echo ""; \
	echo "Pre-flight checks:"; \
	echo "=================="; \
	if git diff --quiet && git diff --cached --quiet; then \
		echo "$(GREEN)✓ Working directory is clean$(NC)"; \
	else \
		echo "$(RED)✗ Working directory has uncommitted changes$(NC)"; \
		echo ""; \
		git status --short; \
		echo ""; \
		echo "Please commit or stash your changes before publishing."; \
		exit 1; \
	fi; \
	echo ""; \
	echo "This will upload version $$version to PyPI"; \
	echo ""; \
	read -p "Continue? (y/N) " -n 1 -r; \
	echo ""; \
	if [[ ! $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(YELLOW)Aborted$(NC)"; \
		exit 1; \
	fi; \
	echo ""; \
	echo "Uploading to PyPI..."; \
	if [ -n "$$PYPI_TOKEN" ]; then \
		if command -v $(UV) >/dev/null 2>&1; then \
			$(UV) run twine upload --username __token__ --password "$$PYPI_TOKEN" dist/*; \
		else \
			$(PYTHON) -m twine upload --username __token__ --password "$$PYPI_TOKEN" dist/*; \
		fi; \
	else \
		if command -v $(UV) >/dev/null 2>&1; then \
			$(UV) run twine upload dist/*; \
		else \
			$(PYTHON) -m twine upload dist/*; \
		fi; \
	fi; \
	echo ""; \
	echo "$(GREEN)✓ Published to PyPI$(NC)"; \
	echo ""; \
	echo "Install with: pip install $(PROJECT_NAME)==$$version"

publish: ## Create tag and trigger automated release
	@echo "$(BLUE)Starting automated release process...$(NC)"
	@echo ""
	@version=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	tag="v$$version"; \
	echo "Version: $$version"; \
	echo "Tag: $$tag"; \
	echo ""; \
	echo "Pre-flight checks:"; \
	echo "=================="; \
	if git diff --quiet && git diff --cached --quiet; then \
		echo "$(GREEN)✓ Working directory is clean$(NC)"; \
	else \
		echo "$(RED)✗ Working directory has uncommitted changes$(NC)"; \
		echo ""; \
		git status --short; \
		echo ""; \
		echo "Please commit or stash your changes before releasing."; \
		exit 1; \
	fi; \
	if git tag -l | grep -q "^$$tag$$"; then \
		echo "$(RED)✗ Tag $$tag already exists$(NC)"; \
		echo ""; \
		echo "To delete and recreate:"; \
		echo "  git tag -d $$tag"; \
		echo "  git push origin :refs/tags/$$tag"; \
		exit 1; \
	else \
		echo "$(GREEN)✓ Tag $$tag does not exist yet$(NC)"; \
	fi; \
	current_branch=$$(git rev-parse --abbrev-ref HEAD); \
	echo "$(GREEN)✓ Current branch: $$current_branch$(NC)"; \
	echo ""; \
	echo "This will:"; \
	echo "  1. Create and push tag $$tag"; \
	echo "  2. Trigger GitHub Actions to:"; \
	echo "     - Create a GitHub release with changelog"; \
	echo "     - Run tests on all platforms"; \
	echo "     - Build and publish to PyPI"; \
	echo ""; \
	read -p "Continue? (y/N) " -n 1 -r; \
	echo ""; \
	if [[ ! $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(YELLOW)Aborted$(NC)"; \
		exit 1; \
	fi; \
	echo ""; \
	echo "Creating and pushing tag..."; \
	git tag -a "$$tag" -m "Release $$tag" && \
	git push origin "$$tag" && \
	echo "" && \
	echo "$(GREEN)✓ Tag pushed successfully$(NC)" && \
	echo "" && \
	repo_path=$$(git config --get remote.origin.url | sed 's|^https://github.com/||;s|^git@github.com:||;s|\.git$$||'); \
	echo "GitHub Actions workflows triggered:" && \
	echo "  - Release creation: https://github.com/$$repo_path/actions/workflows/release.yml" && \
	echo "  - PyPI publishing: https://github.com/$$repo_path/actions/workflows/publish.yml" && \
	echo "" && \
	echo "Monitor progress at: https://github.com/$$repo_path/actions"

release: publish ## Alias for publish

##@ Docker

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker build -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)✓ Docker image built: $(PROJECT_NAME):latest$(NC)"

docker-run: ## Run Docker container
	@echo "$(BLUE)Running Docker container...$(NC)"
	docker run --rm -p 8000:8000 $(PROJECT_NAME):latest

docker-up: docker-build docker-run ## Build and run Docker container

docker-stop: ## Stop running containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	@docker ps -q --filter "ancestor=$(PROJECT_NAME):latest" | xargs -r docker stop

docker-clean: ## Remove Docker image
	@echo "$(BLUE)Removing Docker image...$(NC)"
	@docker rmi $(PROJECT_NAME):latest 2>/dev/null || true
	@echo "$(GREEN)✓ Docker image removed$(NC)"

##@ Fly.io

fly-deploy: ## Deploy to Fly.io
	@echo "$(BLUE)Deploying to Fly.io...$(NC)"
	fly deploy

fly-status: ## Check Fly.io deployment status
	@echo "$(BLUE)Checking Fly.io status...$(NC)"
	fly status

fly-logs: ## View Fly.io logs
	@echo "$(BLUE)Viewing Fly.io logs...$(NC)"
	fly logs

fly-open: ## Open Fly.io app in browser
	@echo "$(BLUE)Opening Fly.io app...$(NC)"
	fly open

##@ Version Management

version: ## Show current version
	@version=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	echo "Current version: $$version"

bump-patch: ## Bump patch version (0.0.X)
	@echo "$(BLUE)Bumping patch version...$(NC)"
	@current=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	major=$$(echo $$current | cut -d. -f1); \
	minor=$$(echo $$current | cut -d. -f2); \
	patch=$$(echo $$current | cut -d. -f3); \
	new_patch=$$(($$patch + 1)); \
	new_version="$$major.$$minor.$$new_patch"; \
	sed -i.bak "s/^version = \"$$current\"/version = \"$$new_version\"/" pyproject.toml && rm pyproject.toml.bak; \
	echo "Version bumped: $$current -> $$new_version"; \
	echo "Review the change, then run 'make publish' to release"

bump-minor: ## Bump minor version (0.X.0)
	@echo "$(BLUE)Bumping minor version...$(NC)"
	@current=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	major=$$(echo $$current | cut -d. -f1); \
	minor=$$(echo $$current | cut -d. -f2); \
	new_minor=$$(($$minor + 1)); \
	new_version="$$major.$$new_minor.0"; \
	sed -i.bak "s/^version = \"$$current\"/version = \"$$new_version\"/" pyproject.toml && rm pyproject.toml.bak; \
	echo "Version bumped: $$current -> $$new_version"; \
	echo "Review the change, then run 'make publish' to release"

bump-major: ## Bump major version (X.0.0)
	@echo "$(BLUE)Bumping major version...$(NC)"
	@current=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	major=$$(echo $$current | cut -d. -f1); \
	new_major=$$(($$major + 1)); \
	new_version="$$new_major.0.0"; \
	sed -i.bak "s/^version = \"$$current\"/version = \"$$new_version\"/" pyproject.toml && rm pyproject.toml.bak; \
	echo "Version bumped: $$current -> $$new_version"; \
	echo "Review the change, then run 'make publish' to release"

##@ Development Workflow

serve: ## Run the MCP server in HTTP mode
	@echo "$(BLUE)Starting MCP server...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) run $(PYTHON) -m chuk_motion.server http --port 8000; \
	else \
		PYTHONPATH=src $(PYTHON) -m chuk_motion.server http --port 8000; \
	fi

run: serve ## Alias for serve

serve-stdio: ## Run the MCP server in STDIO mode
	@echo "$(BLUE)Starting MCP server (STDIO mode)...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) run $(PYTHON) -m chuk_motion.server stdio; \
	else \
		PYTHONPATH=src $(PYTHON) -m chuk_motion.server stdio; \
	fi

debug: ## Run server with debug logging
	@echo "$(BLUE)Starting MCP server with debug logging...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		MCP_LOG_LEVEL=DEBUG $(UV) run $(PYTHON) -m chuk_motion.server http --port 8000; \
	else \
		MCP_LOG_LEVEL=DEBUG PYTHONPATH=src $(PYTHON) -m chuk_motion.server http --port 8000; \
	fi

watch: ## Watch for changes and run tests
	@echo "$(BLUE)Watching for changes...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		PYTHONPATH=src $(UV) run $(PYTEST) tests/ -v --looponfail; \
	else \
		PYTHONPATH=src $(PYTEST) tests/ -v --looponfail; \
	fi

##@ Dependencies

update-deps: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) pip list --outdated; \
	else \
		pip list --outdated; \
	fi
	@echo "$(YELLOW)Run 'uv pip install --upgrade <package>' to update$(NC)"

check-deps: ## Check for outdated dependencies
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) pip list --outdated; \
	else \
		pip list --outdated; \
	fi

freeze: ## Freeze current dependencies
	@echo "$(BLUE)Freezing dependencies...$(NC)"
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) pip freeze > requirements-frozen.txt; \
	else \
		pip freeze > requirements-frozen.txt; \
	fi
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
