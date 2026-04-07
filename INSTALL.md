# Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: Development Installation from Source

Clone or navigate to the datagrep-cli directory and install in development mode:

```bash
pip install -e .
```

This allows you to make modifications to the source code and see them reflected immediately.

### Method 2: Production Installation from Source

```bash
pip install .
```

### Method 3: Install with Optional Dependencies

Install with color support:
```bash
pip install -e ".[color]"
```

Install with progress bar support:
```bash
pip install -e ".[progress]"
```

Install with Excel support:
```bash
pip install -e ".[excel]"
```

Install with all optional dependencies:
```bash
pip install -e ".[color,progress,excel]"
```

Install development tools for testing:
```bash
pip install -e ".[dev]"
```

## After Installation

Once installed, you can use `datagrep` from anywhere:

```bash
datagrep [input_file] [columns] [value] [options]
```

### Quick Examples

```bash
# Count total records
datagrep data.csv --count

# Describe schema
datagrep data.json --describe

# Show first 5 rows
datagrep data.xlsx --sample 5

# Search for 'Alice' in name column
datagrep data.csv name Alice

# Search with filtering
datagrep data.json name Bob --where "age > 25"

# Export results to JSON
datagrep data.csv email @company.com --output-format json --output results.json
```

## Uninstallation

```bash
pip uninstall datagrep-cli
```

## Troubleshooting

### Command not found: `datagrep`

Ensure the installation completed successfully:
```bash
pip show datagrep-cli
```

If installed but not found, the Python scripts directory may not be in your PATH. Use:
```bash
python -m datagrep [options]
```

### Optional dependency errors

If you get import errors for colorama, tqdm, or openpyxl, install the relevant optional dependencies:

```bash
pip install colorama tqdm openpyxl
```

Or use the extras installation:
```bash
pip install datagrep-cli[color,progress,excel]
```

## Development

To set up a development environment:

```bash
git clone https://github.com/yourusername/datagrep-cli.git
cd datagrep-cli
pip install -e ".[dev]"
```

Run tests:
```bash
python -m unittest tests -v
```

Format code:
```bash
black datagrep.py
```

Lint code:
```bash
flake8 datagrep.py
```
