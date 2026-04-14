# Architecture Guide

Documentation of datagrep-cli's modular architecture and design decisions.

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Module Descriptions](#module-descriptions)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Extension Points](#extension-points)

## Overview

datagrep-cli follows a **modular, layered architecture** that separates concerns and makes the codebase maintainable and testable:

```
┌─────────────────────────────────┐
│   CLI Layer (cli.py)            │  - Argument parsing
│   - Orchestration               │  - Validation
│   - Entry point                 │  - Workflow control
└──────────┬──────────────────────┘
           │
    ┌──────┴───────┬──────────────┬────────────┐
    │              │              │            │
┌───▼────┐   ┌────▼──┐  ┌───────▼──┐  ┌──────▼────┐
│ Core/  │   │Core/  │  │  Core/   │  │  Core/    │
│loader  │   │engine │  │formatter │  │  __init__ │
│(Load)  │   │(Find) │  │ (Output) │  │           │
└────────┘   └───────┘  └──────────┘  └───────────┘
    │              │              │
    └──────┬───────┴──────────────┘
           │
    ┌──────▼──────────────────┐
    │  Utils Layer            │
    │  - exceptions.py        │  - Custom exceptions
    │  - io.py                │  - File I/O utils
    │  - parsing.py           │  - Query parsing
    │  - formatting.py        │  - Output formatting
    └─────────────────────────┘
```

## Project Structure

```
datagrep-cli/
├── src/
│   ├── __init__.py              # Package marker
│   ├── datagrep.py              # Entry point (7 lines)
│   ├── cli.py                   # CLI orchestration (450+ lines)
│   ├── core/
│   │   ├── __init__.py          # Exports main classes
│   │   ├── loader.py            # DataLoader class
│   │   ├── engine.py            # SearchEngine class
│   │   └── formatter.py         # OutputFormatter class
│   └── utils/
│       ├── __init__.py          # Exports utilities
│       ├── exceptions.py        # Custom exception (DataGrepError)
│       ├── io.py                # File I/O helpers
│       ├── parsing.py           # WHERE clause parsing
│       └── formatting.py        # ASCII table formatting
├── tests/
│   ├── __init__.py
│   └── tests.py                 # Unit tests (26+ tests)
├── completion/                  # Shell completion scripts
│   ├── datagrep.bash
│   ├── datagrep.zsh
│   ├── datagrep.fish
│   └── datagrep.ps1
├── examples/
│   ├── configs/                 # Config templates
│   └── data/                    # Sample data files
├── docs/                        # Documentation
├── setup.py                     # Setup configuration
├── pyproject.toml              # PEP 518 config
├── Makefile                    # Development commands
└── README.md                   # Main documentation
```

## Module Descriptions

### Entry Point: `src/datagrep.py`

**Purpose:** Minimal entry point for the distribution.

**Responsibility:** 
- Import `main()` from cli module
- Execute when installed as console script

**Code:**
```python
from cli import main

__version__ = "1.0.0"

if __name__ == "__main__":
    main()
```

**Key Points:**
- Reduced from 1100 lines to 7 lines (refactored)
- Uses absolute imports for console script support
- Allows `datagrep` command to work globally

### CLI Orchestration: `src/cli.py`

**Purpose:** Main workflow orchestrator and CLI interface.

**Responsibilities:**
- Parse command-line arguments
- Validate argument combinations
- Orchestrate the search workflow
- Handle errors and provide user feedback

**Key Components:**

1. **Argument Parsing**
   ```python
   def parse_args() -> argparse.Namespace
   ```
   - Supports legacy positional: `datagrep file cols val`
   - Supports modern flags: `datagrep --file file --columns cols --search val`
   - Flags take precedence over positional

2. **Argument Validation**
   ```python
   def validate_args(args: argparse.Namespace) -> None
   ```
   - Ensures required combinations exist
   - Validates mutual exclusivity (--count vs --show-count)
   - Checks file existence

3. **WHERE Parsing**
   ```python
   def parse_where_condition(where_str: str) -> Callable
   ```
   - Parses WHERE conditions with AND/OR logic
   - Supports operators: ==, !=, >, <, >=, <=
   - Delegates to `parsing.py` for implementation

4. **Main Workflow**
   ```python
   def main() -> None
   ```
   - Creates DataLoader, SearchEngine, OutputFormatter instances
   - Orchestrates: load → filter → search → output
   - Handles all error cases gracefully

**Code Structure (300+ of 450 lines is error handling)**

### Data Loading: `src/core/loader.py`

**Purpose:** Load data from various file formats.

**Class:** `DataLoader`

**Key Methods:**

1. **`load()`** - Main entry point
   - Detects file format
   - Delegates to appropriate loader
   - Opens file and reads data

2. **`_detect_format()`** - Auto-detect file type
   - Checks file extension
   - Falls back to content inspection
   - Supports: CSV, JSON, XLSX

3. **`_load_csv()`** - Load CSV files
   - Uses `csv.DictReader` for column headers
   - Always eager-loads to ensure file can close safely
   - Sets `available_columns` and `records`

4. **`_load_json()`** - Load JSON files
   - Supports JSON arrays: `[{...}, {...}]`
   - Supports NDJSON: newline-delimited objects
   - Extracts columns from object keys

5. **`_load_excel()`** - Load Excel files (optional)
   - Uses `openpyxl` to read XLSX
   - Requires `[excel]` dependency
   - Converts rows to dictionaries

**Data Structure:**
```python
self.records: List[Dict[str, Any]]        # Loaded records
self.available_columns: List[str]          # Column names
self.records_count: Optional[int]          # Total record count
```

**Why Eager Loading?**
- Originally tried lazy loading with iterators
- Problem: CSV DictReader needs open file, but file closes after `with` block
- Solution: Load all records into memory during `load()` call
- Trade-off: More memory, but safer file I/O, no lazy iterator bugs

### Search Engine: `src/core/engine.py`

**Purpose:** Perform searching and filtering operations.

**Class:** `SearchEngine`

**Key Methods:**

1. **`search()`** - Find matching records
   - Takes column names to search
   - Returns list of matching records
   - Respects `--limit` option for early termination

2. **`apply_filters()`** - Apply WHERE/sort/empty filters
   - Called before searching
   - Returns filtered record list
   - Supports: WHERE, SORT, EMPTY, NOT-EMPTY

**Implementation:**
```python
# Flow:
1. Apply WHERE conditions (pre-filter)
2. Sort if requested  
3. Apply EMPTY/NOT-EMPTY filters
4. Search for value in specified columns
5. Respect --limit for performance
```

**Data Flow:**
```
Input Records → Filter (WHERE) → Sort → Filter (EMPTY) → Search → Output
```

### Output Formatting: `src/core/formatter.py`

**Purpose:** Convert results to desired output format.

**Class:** `OutputFormatter`

**Key Methods:**

1. **`write_output()`** - Main entry, delegates to format handler
   - Determines format (CSV/JSON/Table/Raw)
   - Handles file vs stdout output
   - Manages file opening/closing safely

2. **`_write_csv()`** - CSV format
   - Uses `csv.DictWriter` for consistent output
   - Maintains column order
   - Handles encoding

3. **`_write_json()`** - JSON format
   - Pretty-prints with indentation
   - Supports `--show-count` mode
   - Ensures UTF-8 encoding

4. **`_write_table()`** - ASCII table format
   - Calls `format_table()` from utils
   - Adds colors if `--color` flag set
   - Aligned columns for readability

5. **`_write_raw()`** - Raw dictionary format
   - One dict per line
   - Python literal syntax
   - Useful for parsing with tools

**File Handling:**
```python
# Safe file closing
output_file = open(...) if args.output else sys.stdout
try:
    # Write logic
finally:
    if args.output:  # Only close if WE opened it
        output_file.close()
    # Never close sys.stdout
```

### Utilities Package: `src/utils/`

#### `exceptions.py` - Custom Exceptions

```python
class DataGrepError(Exception):
    """Base exception for all datagrep errors."""
```

**Usage:**
```python
raise DataGrepError("Column 'xyz' not found in data")
```

#### `io.py` - File I/O Utilities

**Key Functions:**

1. **`open_input_file()`** - Unified input opening
   - Handles file paths
   - Handles stdin (`-` argument)
   - Manages encoding

2. **`load_json_records()`** - JSON loading helper
   - Parses JSON arrays
   - Parses NDJSON (newline-delimited)
   - Error handling

3. **`load_excel_records()`** - Excel loading helper
   - Uses `openpyxl` for XLSX
   - Returns list of dictionaries
   - Column extraction

4. **`build_matcher()`** - Search matching function
   - Factory for search functions
   - Supports: contains, exact, startswith, endswith, regex
   - Returns callable: `bool = matcher(value)`

5. **`check_file_size()`** - Performance warnings
   - Warns if file > 500MB
   - Warns if file > 1GB (may be slow)
   - Doesn't stop processing

#### `parsing.py` - Query Parsing

**Key Functions:**

1. **`parse_where_condition()`** - Parse WHERE strings
   - Input: `"age > 25 and name != john"`
   - Returns: Callable that filters records
   - Supports: AND, OR, operators

2. **`build_matcher()`** - Re-exported from io.py
   - Creates matching function
   - Used by search engine

#### `formatting.py` - Output Utils

**Key Functions:**

1. **`format_table()`** - ASCII table formatting
   - Aligns columns
   - Handles long values (truncation)
   - Supports optional colors (via colorama)

**Example:**
```
id | name        | email
---|-------------|-------------------------
1  | John Smith  | john@example.com
2  | Alice Brown | alice@example.com
```

## Data Flow

### Complete Search Workflow

```
1. User Input
   └─> datagrep customers.csv status active --where "age > 25" --limit 10

2. CLI Layer (cli.py)
   ├─> parse_args() → Namespace object
   ├─> validate_args() → Check for errors
   └─> main() → Orchestrate workflow

3. Loading Phase (DataLoader)
   ├─> detect_format() → "csv"
   ├─> _load_csv() → Load all records into memory
   └─> Set: records, available_columns

4. Filtering Phase (SearchEngine)
   ├─> apply_filters()
   │   ├─> Parse WHERE "age > 25"
   │   ├─> Filter records where age > 25
   │   └─> Return filtered list
   └─> Return: List[Dict] with ~N records

5. Searching Phase (SearchEngine)
   ├─> search(columns=["status"])
   │   ├─> For each record
   │   ├─> Check if status contains "active"
   │   ├─> Respect limit=10
   │   └─> Collect matches
   └─> Return: List[Dict] with ≤10 records

6. Output Phase (OutputFormatter)
   ├─> Determine format: CSV (default)
   ├─> Select columns: all (or via --select)
   ├─> _write_csv()
   │   ├─> Open stdout or file
   │   ├─> Write headers
   │   ├─> Write record rows
   │   └─> Close if file output
   └─> Done

7. User Output
   └─> CSV records printed to stdout or file
```

### Memory and Performance

```
File Size → Memory Usage
────────────────────────────
1 MB   → ~3-5 MB (3-5x expansion)
10 MB  → ~30-50 MB
100 MB → ~300-500 MB
1 GB   → ~3-5 GB (may be slow/hit limits)
```

**Optimization Strategy:**
- Eager loading: Safe file I/O, simple to understand
- Future: Lazy loading for 1GB+ files (Phase 2)

## Design Patterns

### 1. Factory Pattern
`build_matcher()` creates different matching functions based on mode:

```python
def build_matcher(value, mode, ignore_case):
    if mode == "exact":
        return lambda field: exact_match(field, value)
    elif mode == "regex":
        return lambda field: re.match(pattern, field)
    # ...
```

### 2. Strategy Pattern
Each search mode is a different strategy:
- Contains strategy
- Exact strategy  
- Regex strategy
- etc.

### 3. Template Method Pattern
`OutputFormatter` uses template method for output:

```python
def write_output(self):
    if format == 'csv':
        self._write_csv()
    elif format == 'json':
        self._write_json()
    # Subclasses override write methods
```

### 4. Separation of Concerns
- **CLI**: Argument handling only
- **Loader**: Data loading only
- **Engine**: Search logic only
- **Formatter**: Output formatting only
- **Utils**: Shared utilities

### 5. Dependency Injection
Classes receive dependencies through constructor:

```python
class SearchEngine:
    def __init__(self, records, columns, args):
        # Records injected, not loaded internally
        self.records = records
```

## Extension Points

### Adding a New Search Mode

1. Add mode to argument parser (cli.py):
```python
"--mode {contains,exact,...,mymode}"
```

2. Update `build_matcher()` (io.py):
```python
def build_matcher(value, mode, ignore_case):
    ...
    elif mode == "mymode":
        return lambda field: my_match(field, value)
```

3. Add tests (tests.py)

### Adding a New Output Format

1. Add format to argument parser (cli.py):
```python
"--output-format {csv,json,table,raw,myformat}"
```

2. Add method to OutputFormatter (formatter.py):
```python
def _write_myformat(self, output_file, records, columns, show_count):
    # Implementation
```

3. Update `write_output()` to dispatch:
```python
elif self.args.output_format == 'myformat':
    self._write_myformat(...)
```

### Adding a New Input Format

1. Add format to argument parser (cli.py):
```python
"--input-format {auto,csv,json,xlsx,myformat}"
```

2. Add method to DataLoader (loader.py):
```python
def _detect_myformat(self, csvfile):
    # Detection logic
    
def _load_myformat(self, csvfile):
    # Loading logic
    self.records = ...
```

3. Update `load()` to dispatch:
```python
elif input_format == 'myformat':
    self._load_myformat()
```

### Adding a New WHERE Operator

1. Update WHERE parser (parsing.py):
```python
if operator == "my_op":
    # Implement comparison logic
```

2. Add tests (tests.py)

## Testing Structure

Tests are in `tests/tests.py` with 26+ test cases:

```python
class TestDataLoader:
    def test_load_csv()
    def test_load_json()
    def test_detect_format()

class TestSearchEngine:
    def test_search_contains()
    def test_search_exact()
    def test_apply_filters()

class TestOutputFormatter:
    def test_format_csv()
    def test_format_json()
    def test_format_table()

class TestIntegration:
    def test_full_workflow()
    def test_pipes()
```

## Performance Considerations

### Current Optimizations

1. **Eager loading**: Safe file I/O, predictable memory
2. **Early termination**: `--limit` stops searching early
3. **WHERE filtering**: Pre-filter before searching
4. **File size warnings**: Alerts users to potential issues

### Future Optimizations (Phase 2)

1. **Lazy loading**: Streaming for massive files (1GB+)
2. **Parallel search**: Multi-threaded pattern matching
3. **Compression support**: Handle gzip/bzip2 files
4. **Caching**: Cache loaded files for repeated searches
5. **Indexing**: Optional index for fast searches on large files

## Dependencies

### Core (No Dependencies)
- Python 3.7+ (standard library only)

### Optional
- `colorama` - Terminal colors
- `tqdm` - Progress bars
- `openpyxl` - Excel support

### Development
- `pytest` - Testing
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking
- `pylint` - Code quality

## Summary

The architecture prioritizes:
1. **Clarity**: Easy to understand code flow
2. **Testability**: Units are independently testable
3. **Maintainability**: Changes in one module don't affect others
4. **Extensibility**: Easy to add new features
5. **Performance**: Reasonable defaults for typical usage
6. **Robustness**: Comprehensive error handling
