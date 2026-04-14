# Installation Guide

Complete installation instructions for datagrep-cli on all platforms.

## Table of Contents

1. [Quick Install](#quick-install)
2. [From Source](#from-source)  
3. [Platform-Specific Guides](#platform-specific-guides)
4. [Verifying Installation](#verifying-installation)
5. [Troubleshooting](#troubleshooting)

## Quick Install

### Windows

```powershell
# Using pip (requires Python 3.7+)
pip install datagrep-cli

# Or in development mode
pip install -e .
```

### macOS / Linux

```bash
# Using pip
pip install datagrep-cli

# Or in development mode
pip install -e .
```

## Prerequisites

Ensure you have **Python 3.7 or higher** installed:

```bash
python --version
# Output should be: Python 3.x.x (where x >= 7)
```

If not installed, download from [python.org](https://www.python.org/downloads/)

## Installation Methods

### Method 1: From PyPI (When Published)

The easiest way once the package is on PyPI:

```bash
# Basic installation
pip install datagrep-cli

# With optional features
pip install datagrep-cli[color,progress,excel]
```

### Method 2: From Source (Development)

Clone the repository and install in editable mode:

```bash
# Clone the repository
git clone https://github.com/yourusername/datagrep-cli.git
cd datagrep-cli

# Install in development mode with all dependencies
pip install -e ".[color,progress,excel]"

# Verify installation
datagrep --version
```

### Method 3: Docker

Build and run in a Docker container:

```bash
# Build image
docker build -t datagrep:latest .

# Run container
docker run --rm -v $(pwd):/data datagrep:latest /data/file.csv name John

# Or with interactive shell
docker run --rm -it -v $(pwd):/data datagrep:latest bash
```

## Optional Dependencies

Install additional features as needed:

### Colored Output

For colorized table output and status messages:

```bash
# Using pip directly
pip install colorama>=0.4.3

# Or with datagrep
pip install datagrep-cli[color]
pip install -e ".[color]"  # From source
```

### Progress Bars

For progress bars when processing large files:

```bash
# Using pip directly
pip install tqdm>=4.50.0

# Or with datagrep
pip install datagrep-cli[progress]
pip install -e ".[progress]"  # From source
```

### Excel Support

To search and filter Excel (XLSX) files:

```bash
# Using pip directly
pip install openpyxl>=3.0.0

# Or with datagrep
pip install datagrep-cli[excel]
pip install -e ".[excel]"  # From source
```

### All Optional Features

Install everything at once:

```bash
# Using pip directly
pip install colorama tqdm openpyxl

# Or with datagrep
pip install datagrep-cli[color,progress,excel]
pip install -e ".[color,progress,excel]"  # From source
```

### Development Tools

For contributing to datagrep:

```bash
pip install datagrep-cli[dev,color,progress,excel]
# or from source
pip install -e ".[dev,color,progress,excel]"
```

Includes: pytest, pytest-cov, black, flake8, mypy, pylint, isort

## Platform-Specific Guides

### Windows

#### Using Anaconda

If you use Anaconda/Miniconda:

```powershell
# Create and activate environment
conda create -n datagrep python=3.10
conda activate datagrep

# Install from PyPI
pip install datagrep-cli[color,progress,excel]

# Or from source
git clone ...
cd datagrep-cli
pip install -e ".[color,progress,excel]"
```

#### Using Windows PowerShell

```powershell
# Check Python installation
python --version

# Install datagrep
pip install datagrep-cli

# Test installation
datagrep --help
```

#### Using Windows Command Prompt (CMD)

```cmd
# Check Python installation
python --version

# Install datagrep
pip install datagrep-cli

# Test installation
datagrep --help
```

#### Using Windows Subsystem for Linux (WSL)

```bash
# WSL behaves like Linux
python3 --version

# Install for Python 3
pip3 install datagrep-cli

# Test
datagrep --help
```

### macOS

#### Using Homebrew

If you have Homebrew installed:

```bash
# Install Python (if not using system Python)
brew install python@3.11

# Install datagrep
pip3 install datagrep-cli[color,progress,excel]

# Verify
datagrep --version
```

#### Using Native Python

```bash
# Check Python 3 is available
python3 --version

# Install datagrep
pip3 install datagrep-cli[color,progress,excel]

# Create alias (for convenience)
echo 'alias datagrep="python3 -m datagrep"' >> ~/.zshrc
# or ~/.bash_profile for bash
```

#### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv datagrep-env
source datagrep-env/bin/activate

# Install datagrep
pip install datagrep-cli[color,progress,excel]

# Deactivate when done
deactivate
```

### Linux

#### Ubuntu / Debian

```bash
# Install Python and pip (if not installed)
sudo apt-get update
sudo apt-get install python3 python3-pip

# Install datagrep
pip3 install datagrep-cli[color,progress,excel]

# Verify installation
datagrep --version
```

#### RHEL / CentOS / Fedora

```bash
# Install Python and pip (if not installed)
sudo dnf install python3 python3-pip

# Install datagrep
pip3 install datagrep-cli[color,progress,excel]

# Verify installation
datagrep --version
```

#### Generic Linux

```bash
# Install Python 3.7+ and pip using your package manager

# Install datagrep
pip install datagrep-cli[color,progress,excel]

# Verify installation
datagrep --version
```

## Verifying Installation

### Quick Verification

```bash
# Check version number
datagrep --version

# Should output: datagrep 1.0.0 (or higher version number)
```

### Full Verification

```bash
# Display help
datagrep --help

# Should show command-line interface documentation

# Test with sample file (if available)
datagrep examples/data/sample_customers.csv --describe

# Should display schema of the CSV file
```

### Manual Verification

```bash
# Check Python package installation
python -c "import datagrep; print(datagrep.__version__)"

# Should output: 1.0.0 (or version number)
```

## Troubleshooting

### "command not found: datagrep"

The `datagrep` command is not in your PATH. Solutions:

#### On Windows

```powershell
# If installed via pip in user mode:
# Add Python Scripts to PATH manually
# Edit: System Properties > Environment Variables > Edit PATH

# Or reinstall with:
pip install --upgrade --force-reinstall datagrep-cli

# Test with full path:
python -m datagrep --help
```

#### On macOS/Linux

```bash
# Check where pip installed the script
which pip

# If using pip3, try:
pip3 install datagrep-cli

# Or use directly:
python3 -m datagrep --help

# Add to PATH if needed:
export PATH="$PATH:$HOME/.local/bin"
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
```

### Permission Denied on Linux/macOS

If you see permission errors:

```bash
# Either reinstall for your user account
pip install --user datagrep-cli

# Or use sudo (not recommended)
sudo pip install datagrep-cli

# Then restart your terminal
```

### "ModuleNotFoundError: No module named 'datagrep'"

The package is installed but not in Python path:

```bash
# Verify Python can find it
python -c "import datagrep"

# If error, reinstall:
pip install --upgrade --force-reinstall datagrep-cli

# Or from source directory:
cd datagrep-cli
pip install -e .
```

### Python Version Mismatch

If you have multiple Python versions:

```bash
# Check which Python is default
python --version

# Ensure you're using Python 3.7+
python3 --version

# Install with specific version
python3 -m pip install datagrep-cli

# Or use explicit version manager
pyenv versions  # if using pyenv
pyenv install 3.10.0
pyenv shell 3.10.0
pip install datagrep-cli
```

### Optional Dependency Issues

If colored output or progress bars don't work:

```bash
# Install missing optional dependencies
pip install datagrep-cli[color,progress,excel]

# Or individually
pip install colorama tqdm openpyxl

# The tool works without them (just without those features)
```

### Issues with Excel Files

If Excel files cause "module 'openpyxl' has no attribute" errors:

```bash
# Reinstall openpyxl
pip uninstall openpyxl
pip install openpyxl>=3.0.0

# Or reinstall datagrep with excel support
pip install --upgrade datagrep-cli[excel]
```

### "ImportError: attempted relative import with no known parent package"

If running from source without proper installation:

```bash
# Ensure you're in the datagrep-cli directory
cd datagrep-cli

# Install in editable mode
pip install -e .

# Don't run src/datagrep.py directly
# Use: datagrep command  (or python -m datagrep)
```

### Still Having Issues?

1. Check Python version: `python --version` (should be 3.7+)
2. Check pip: `pip --version`
3. Uninstall and reinstall:
   ```bash
   pip uninstall datagrep-cli
   pip cache purge
   pip install --upgrade datagrep-cli[color,progress,excel]
   ```
4. Check GitHub issues: https://github.com/yourusername/datagrep-cli/issues
5. Create a new issue with:
   - Your OS and Python version
   - Installation command used
   - Full error message
   - Output of `pip show datagrep-cli`

## Uninstalling

To remove datagrep-cli:

```bash
# Using pip
pip uninstall datagrep-cli

# From source
cd datagrep-cli
pip uninstall datagrep-cli

# Or manually delete
# Look for installation directory: python -c "import datagrep; print(datagrep.__file__)"
```

## Next Steps

After installation:

1. Read the [Quick Start Guide](../README.md#quick-start)
2. Check [Usage Examples](USAGE.md)
3. Set up [Shell Completion](../README.md#shell-completion) (optional)
4. Review [FAQ](FAQ.md) for common questions
