#!/bin/bash
# Development environment setup script for datagrep-cli
# Run this script to set up a complete development environment

set -e

echo "╔════════════════════════════════════════════╗"
echo "║   datagrep-cli Development Setup           ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Check if Python 3.7+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment
echo ""
echo "Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ Build tools upgraded"

# Install package with all dependencies
echo ""
echo "Installing datagrep-cli with all dependencies..."
pip install -e ".[color,progress,excel,dev]" > /dev/null 2>&1
echo "✓ Package installed with all extras"

# Run tests
echo ""
echo "Running test suite..."
python -m unittest tests -v 2>&1 | head -20
echo ""
echo "ℹ️  Run 'python -m unittest tests -v' to see full test output"

# Display summary
echo ""
echo "╔════════════════════════════════════════════╗"
echo "║   Setup Complete!                          ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "Quick start:"
echo "  1. Activate environment: source .venv/bin/activate"
echo "  2. Run tests:           python -m unittest tests -v"
echo "  3. Run linter:          pylint src/datagrep.py"
echo "  4. Format code:         black src/"
echo "  5. Type check:          mypy src/"
echo "  6. Run the tool:        datagrep --help"
echo ""
