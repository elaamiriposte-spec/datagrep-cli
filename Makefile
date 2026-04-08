.PHONY: help install install-dev test lint format type-check clean build docs run version

# Default target
help:
	@echo "═══════════════════════════════════════════════════════════"
	@echo "  datagrep-cli Makefile"
	@echo "═══════════════════════════════════════════════════════════"
	@echo ""
	@echo "Available targets:"
	@echo "  make install          - Install dependencies"
	@echo "  make install-dev      - Install with development tools"
	@echo "  make test             - Run unit tests"
	@echo "  make test-verbose     - Run tests with verbose output"
	@echo "  make coverage         - Run tests with coverage report"
	@echo "  make lint             - Run pylint on source code"
	@echo "  make format           - Format code with black"
	@echo "  make isort            - Sort imports with isort"
	@echo "  make type-check       - Run type checking with mypy"
	@echo "  make quality          - Run all quality checks"
	@echo "  make clean            - Remove build artifacts and cache"
	@echo "  make clean-all        - Remove all generated files"
	@echo "  make build            - Build distribution packages"
	@echo "  make run              - Run the CLI (usage: make run CMD='datagrep ...')"
	@echo "  make version          - Show version information"
	@echo "  make help             - Show this help message"
	@echo ""

# Installation targets
install:
	pip install -e . > /dev/null 2>&1
	@echo "✓ Installed datagrep-cli"

install-dev:
	pip install -e ".[color,progress,excel,dev]" > /dev/null 2>&1
	@echo "✓ Installed datagrep-cli with dev dependencies"

# Testing targets
test:
	python -m unittest discover -s tests -p "*.py" -v

test-verbose:
	python -m unittest discover -s tests -p "*.py" -v 2>&1 | head -50

coverage:
	coverage run -m unittest discover -s tests -p "*.py"
	coverage report
	@echo ""
	@echo "Generating HTML coverage report..."
	coverage html
	@echo "✓ Coverage report generated at htmlcov/index.html"

# Quality checks
lint:
	@echo "Running pylint..."
	pylint src/datagrep.py --disable=all --enable=E,F || true

format:
	@echo "Formatting code with black..."
	black src/ tests/ scripts/ > /dev/null 2>&1
	@echo "✓ Code formatted"

isort:
	@echo "Sorting imports with isort..."
	isort src/ tests/ scripts/ > /dev/null 2>&1
	@echo "✓ Imports sorted"

type-check:
	@echo "Running mypy type checking..."
	mypy src/ --ignore-missing-imports || true

quality: lint type-check
	@echo "✓ All quality checks completed"

# Cleanup targets
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned"

clean-all: clean
	@echo "Cleaning all generated files..."
	rm -rf .venv/ htmlcov/ .coverage
	@echo "✓ All clean"

# Build target
build: clean
	@echo "Building distribution packages..."
	python -m build
	@echo "✓ Packages built in dist/"

# Run target (allows passing command)
run:
	@if [ -z "$(CMD)" ]; then \
		echo "Usage: make run CMD='datagrep data.csv field value'"; \
	else \
		python src/datagrep.py $(CMD); \
	fi

# Version
version:
	python -c "import sys; sys.path.insert(0, 'src'); import datagrep; print('datagrep', datagrep.__version__)"

.DEFAULT_GOAL := help
