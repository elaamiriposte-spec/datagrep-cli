# Development Guide

This guide provides everything you need to set up a development environment and contribute to datagrep-cli.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)
- [Common Development Tasks](#common-development-tasks)
- [Debugging](#debugging)
- [Performance Profiling](#performance-profiling)

## Prerequisites

- Python 3.7+
- pip
- git
- A code editor (VSCode, PyCharm, etc.)

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/datagrep-cli.git
cd datagrep-cli
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install in Development Mode

```bash
# Install with all optional dependencies and dev tools
pip install -e ".[dev,color,progress,excel]"

# Or install specific extras:
pip install -e ".[color]"      # For colorized output
pip install -e ".[progress]"   # For progress bars
pip install -e ".[excel]"      # For Excel support
```

### 4. Verify Installation

```bash
# Check that datagrep is in your PATH
which datagrep

# Run help
datagrep --help

# Run tests
python -m unittest tests -v
```

## Project Structure

```
datagrep-cli/
├── datagrep.py              # Main executable module
├── tests.py                 # Comprehensive unit tests
├── setup.py                 # Traditional setuptools configuration
├── pyproject.toml           # Modern Python packaging
├── py.typed                 # Type hints marker
├── .gitignore               # Git ignore rules
├── completion/              # Shell completions
│   ├── datagrep.bash        # Bash completion
│   ├── datagrep.zsh         # Zsh completion
│   ├── datagrep.fish        # Fish shell completion
│   └── datagrep.ps1         # PowerShell completion
├── examples/                # Example configs and data
│   ├── *.config.json        # Configuration examples
│   └── sample_*.{csv,json}  # Sample data files
├── .github/                 # GitHub-specific files
│   └── workflows/           # CI/CD workflows
├── README.md                # User documentation
├── INSTALL.md               # Installation guide
├── CODE_REVIEW.md           # Technical review
├── CONTRIBUTING.md          # Contribution guidelines
├── DEVELOPMENT.md           # This file
└── LICENSE                  # License file
```

## Architecture Overview

### Core Components

1. **Argument Parsing** (`parse_args()`)
   - Handles CLI argument parsing using argparse
   - Provides help text and option definitions

2. **Validation** (`validate_args()`)
   - Enforces mutual exclusivity of inspection modes
   - Validates argument combinations
   - Raises `DataGrepError` for invalid configurations

3. **Data Loading**
   - `load_json_records()`: Handles JSON arrays and line-delimited JSON
   - `load_excel_records()`: Loads XLSX files using openpyxl
   - `open_input_file()`: Manages file handling and stdin

4. **Filtering & Matching**
   - `parse_where_condition()`: Parses WHERE clauses with AND/OR
   - `build_matcher()`: Creates search functions for different modes

5. **Output Formatting**
   - `format_table()`: ASCII table formatting with optional colors
   - Multiple output formats: CSV, JSON, table, raw

### Data Flow

```
User Input (CLI)
      ↓
parse_args() → Namespace
      ↓
validate_args() → Validated Namespace
      ↓
load_config() → Optional config merging
      ↓
Load Data File (CSV/JSON/XLSX)
      ↓
Apply WHERE filter (optional)
      ↓
Apply SORT (optional)
      ↓
Build matcher → Search function
      ↓
Execute Search/Inspection
      ↓
Format Output
      ↓
Print/Write Results
```

## Common Development Tasks

### Adding a New Search Mode

1. Update `build_matcher()`:
```python
def build_matcher(value: str, mode: str, ignore_case: bool) -> Callable[[str], bool]:
    # ... existing code ...
    if mode == 'fuzzy':
        return lambda text: fuzzy_match(text, value)
```

2. Update `parse_args()`:
```python
parser.add_argument(
    '--mode', choices=['contains', 'exact', 'startswith', 'endswith', 'regex', 'fuzzy'],
    ...
)
```

3. Add tests in `tests.py`:
```python
def test_fuzzy_matching(self):
    matcher = build_matcher('abc', 'fuzzy', False)
    self.assertTrue(matcher('a_b_c'))
    self.assertFalse(matcher('xyz'))
```

### Adding a New Output Format

1. Update `format_table()` or create new formatter
2. Add option to `parse_args()`
3. Handle in `main()` output section:
```python
elif args.output_format == 'xml':
    output_file.write(format_xml(matches, selected_columns))
```

### Adding Configuration Options

1. Add argument in `parse_args()`
2. Handle in `main()` after loading config
3. Add to `load_config()` if file-based
4. Document in README and examples

### Running Linting

```bash
# Install linting tools
pip install black pylint mypy flake8

# Run formatters
black datagrep.py
isort datagrep.py

# Check code quality
pylint datagrep.py
flake8 datagrep.py

# Type checking
mypy datagrep.py --strict
```

## Debugging

### Enable Debug Output

```bash
# Run with verbose logging
datagrep data.csv name john -v

# Enable debug mode
datagrep data.csv name john --debug
```

### Debug Within IDE

#### VSCode

1. Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: datagrep",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/datagrep.py",
            "console": "integratedTerminal",
            "args": ["data.csv", "name", "john"]
        }
    ]
}
```

2. Set breakpoints and run debugger

#### PyCharm

1. Right-click `datagrep.py` → "Run 'datagrep'"
2. Or use Run → Edit Configurations to add custom configuration
3. Set breakpoints and debug

### Common Issues

**ImportError: No module named 'colorama'**
```bash
pip install colorama
```

**File encoding errors**
```bash
# Specify encoding
datagrep data.csv name john --encoding latin-1
```

**Out of Memory on large files**
```bash
# Use stdin for streaming (if applicable)
cat huge_file.csv | datagrep - name john
```

## Performance Profiling

### Profile Execution Time

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Run your code
main()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Run with profiling
python -m memory_profiler datagrep.py data.csv name john
```

### Benchmark Large Files

```bash
import time

start = time.time()
datagrep large_file.csv name value --count
end = time.time()

print(f"Execution time: {end - start:.2f}s")
```

## Documentation Standards

### Docstring Format

Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description explaining the function's behavior,
    parameters, and any important details.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of return value.
        
    Raises:
        DataGrepError: When something goes wrong.
        ValueError: When value is invalid.
    """
    pass
```

### Type Hints

All functions must have complete type hints:

```python
from typing import Dict, List, Optional, Callable, Any, Tuple

def process_data(
    records: List[Dict[str, Any]],
    filter_fn: Optional[Callable[[Dict[str, Any]], bool]] = None
) -> Tuple[List[Dict[str, Any]], int]:
    """Process records with optional filtering."""
    pass
```

## Useful Commands

```bash
# Run specific test
python -m unittest tests.TestSearchMatchers.test_contains_matching -v

# Generate test coverage report
coverage run -m unittest tests && coverage report

# Create distribution packages
python -m build

# Upload to PyPI (after testing)
python -m twine upload dist/*

# Clean build artifacts
rm -rf build/ dist/ *.egg-info
```

## Getting Help

- Check existing code comments and docstrings
- Review closed issues for similar problems
- Ask in project discussions
- Open an issue with detailed description

Happy coding! 🚀
