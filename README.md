```
     _       _                                        _ _ 
  __| | __ _| |_ __ _  __ _ _ __ ___ _ __         ___| (_)
 / _` |/ _` | __/ _` |/ _` | '__/ _ \ '_ \ _____ / __| | |
| (_| | (_| | || (_| | (_| | | |  __/ |_) |_____| (__| | |
 \__,_|\__,_|\__\__,_|\__, |_|  \___| .__/       \___|_|_|
                      |___/         |_|                   
```

# datagrep-cli

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Type Hints](https://img.shields.io/badge/typing-compatible-brightgreen)](https://github.com/python/typeshed)
[![Test Status](https://img.shields.io/badge/tests-passing-brightgreen)]()



A powerful, production-ready Python CLI tool to search and filter CSV, JSON, or Excel records with flexible matching modes, advanced filtering, sorting, and multiple output formats.

**⚠️ Version 1.0:** Optimized for files up to **1GB**. See [docs/PERFORMANCE.md](docs/PERFORMANCE.md) for file size limits, strategies, and Phase 2+ optimization roadmap.

## ⭐ Features

- **Multi-Format Support**: CSV, JSON, Excel (XLSX), and stdin
- **Flexible Search Modes**: Contains, exact, startswith, endswith, regex patterns
- **Advanced Filtering**: Pre-filter with `--where` conditions (AND/OR logic)
- **Sorting**: Sort by column before searching
- **Unicode Support**: Full support for Arabic, Chinese, and other Unicode content
- **Multiple Output Formats**: CSV, JSON, table, raw dictionaries
- **Schema Inspection**: View field names and samples without searching
- **Performance Conscious**: File size warnings, progress bars, configurable limits
- **Complete Type Hints**: 100% type annotation for IDE support and type checking
- **Shell Completions**: Auto-completion for bash, zsh, fish, PowerShell
- **Configuration Files**: Reusable JSON configs for common workflows
- **Well-Tested**: 26+ unit tests with 95%+ code coverage

## � Table of Contents

1. [Installation](#-installation) - Install datagrep
2. [Quick Start](#-quick-start) - 5-minute getting started guide
3. [CLI Syntax Styles](#-cli-syntax-styles) - Positional vs flag style
4. [Detailed Usage](#-detailed-usage) - Complete command reference
5. [Real-World Examples](#-real-world-examples) - Common use cases
6. [Options Reference](#-options-reference) - All flags explained
7. [Shell Completion](#-shell-completion) - Auto-completion setup
8. [Troubleshooting](#-troubleshooting) - Common issues and solutions
9. [FAQ](#-faq) - Frequently asked questions
10. [Contributing](#-contributing) - How to contribute
11. [Documentation](#-documentation) - Additional guides

## �📦 Installation

### Quick Start

```bash
# Install from PyPI
pip install datagrep-cli

# Or install in development mode with all dependencies
pip install -e "git+https://github.com/yourusername/datagrep-cli.git#egg=datagrep-cli[color,progress,excel]"
```

### With Optional Dependencies

```bash
# Colored output
pip install datagrep-cli[color]

# Progress bars
pip install datagrep-cli[progress]

# Excel support
pip install datagrep-cli[excel]

# All extras
pip install datagrep-cli[color,progress,excel]

# Development (includes testing tools)
pip install datagrep-cli[dev,color,progress,excel]
```

### Docker

```bash
# Build image
docker build -t datagrep .

# Run
docker run --rm -v $(pwd):/data datagrep /data/file.csv name John
```

### From Source

```bash
git clone https://github.com/yourusername/datagrep-cli.git
cd datagrep-cli
pip install -e ".[color,progress,excel]"
datagrep --version
```

See [docs/INSTALL.md](docs/INSTALL.md) for detailed installation instructions and troubleshooting.

## �️ System Requirements & Compatibility

### Minimum Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.7 or higher (3.10+ recommended) |
| **Operating System** | Windows, macOS, Linux, WSL |
| **Memory** | 512 MB (files up to 1GB) |
| **Disk Space** | ~50 MB for installation |

### Python Version Support

- ✅ Python 3.7 (minimum support)
- ✅ Python 3.8, 3.9, 3.10, 3.11, 3.12+  
- ✅ PyPy 3.8+ (alternative implementation)

**Check your Python version:**
```bash
python --version
# Output should be 3.7 or higher
```

### Supported Operating Systems

| OS | Status | Notes |
|----|--------|-------|
| **Windows** | ✅ Full Support | PowerShell, CMD, WSL |
| **macOS** | ✅ Full Support | Intel and Apple Silicon |
| **Linux** | ✅ Full Support | Any major distribution |
| **WSL** | ✅ Full Support | Windows Subsystem for Linux |

### Supported File Formats

| Format | Status | Notes |
|--------|--------|-------|
| **CSV** | ✅ Built-in | Default format |
| **JSON** | ✅ Built-in | Arrays and NDJSON |
| **Excel (XLSX)** | ✅ Optional | Requires openpyxl |
| **stdin** | ✅ Built-in | Pipe any format |

### Optional Dependencies

| Feature | Package | Install Command |
|---------|---------|-----------------|
| **Color Output** | colorama | `pip install datagrep-cli[color]` |
| **Progress Bars** | tqdm | `pip install datagrep-cli[progress]` |
| **Excel Support** | openpyxl | `pip install datagrep-cli[excel]` |
| **All Features** | All above | `pip install datagrep-cli[color,progress,excel]` |
| **Development** | pytest, coverage | `pip install datagrep-cli[dev]` |

**Verify installation:**
```bash
datagrep --version
# Output: datagrep 1.0.0 (or higher)
```

If the command is not found, see [Troubleshooting Installation](docs/INSTALL.md#troubleshooting).

## �🚀 Quick Start

- Example  (Modular):

```bash
python -m src.datagrep examples/data/sample_customers.csv --columns first_name --search j  --where "status == active" --select first_name  --output-format json

```

- Output:

```json
[
  {
    "first_name": "Benjie"
  },
  {
    "first_name": "Marjorie"
  }
]
```

### Show file schema and sample

```bash
# Display field names and first 10 rows
datagrep data.csv
```

### Basic search

```bash
# Find all records where 'name' contains 'John'
datagrep data.csv name John

# Case-insensitive search
datagrep data.csv name john --ignore-case

# Exact match
datagrep data.csv name "John Smith" --mode exact
```

### Advanced filtering

```bash
# Search with pre-filtering
datagrep data.csv name alice --where "age > 25"

# Combine filters with AND/OR
datagrep data.csv name alice --where "age > 25 and city == London"

# Sort results
datagrep data.csv email alice --sort name:asc --output-format table
```

### Different formats

```bash
# Work with JSON
datagrep data.json email alice

# Excel files
datagrep data.xlsx product notebook --input-format xlsx

# JSON output
datagrep data.csv name john --output-format json

# Formatted table
datagrep data.csv city london --output-format table --color
```

## � Getting Started for Beginners

Follow these 5 steps to start using datagrep:

### Step 1: Verify Installation

```bash
# Check if datagrep is installed
datagrep --version

# Should output: datagrep 1.0.0 (or higher)
```

If you see "command not found", install with:
```bash
pip install datagrep-cli
```

### Step 2: Inspect Your Data

```bash
# See what columns are available (no search needed)
datagrep your_data.csv

# This shows schema and first 10 rows
```

Output shows:
- **Schema**: List of field names available for searching
- **Sample rows**: First 10 records to understand data structure

### Step 3: Search Your Data

```bash
# Find records where 'name' contains 'John'
datagrep your_data.csv name John

# Results show matching records in CSV format
```

### Step 4: Refine Your Search

```bash
# Case-insensitive search (ignore uppercase/lowercase)
datagrep your_data.csv name john --ignore-case

# Exact match (whole value only)
datagrep your_data.csv name "John Smith" --mode exact

# Search multiple columns at once
datagrep your_data.csv "name,email" john
```

### Step 5: Format Your Results

```bash
# Pretty table output
datagrep your_data.csv name john --output-format table

# JSON format (for use with other tools)
datagrep your_data.csv name john --output-format json

# Save to file
datagrep your_data.csv name john --output results.csv
```

### Common First-Time Commands

```bash
# See all records
datagrep data.csv --describe

# Find records (basic)
datagrep data.csv column_name search_value

# Find records (ignore case)
datagrep data.csv column_name search_value --ignore-case

# View results as table
datagrep data.csv column_name search_value --output-format table

# Save results
datagrep data.csv column_name search_value --output results.csv
```

## �🎨 CLI Syntax Styles

DataGrep supports **two complementary syntax styles**, both fully supported and compatible:

### Positional Arguments Style (Legacy)

The classic, concise style with positional arguments:

```bash
# Format: datagrep FILE COLUMNS VALUE [OPTIONS]
datagrep data.csv name john
datagrep data.csv "name,email" alice --ignore-case
datagrep data.csv city london --output-format table
```

**Best for:** Quick commands, scripting, muscle memory

### Explicit Flags Style (Modern)

The self-documenting style with explicit flags:

```bash
# Format: datagrep --file FILE --columns COLUMNS --search VALUE [OPTIONS]
datagrep --file data.csv --columns name --search john
datagrep --file data.csv --columns name,email --search alice --ignore-case
datagrep --file data.csv --columns city --search london --output-format table
```

**Best for:** Complex commands, clarity, team collaboration, discoverability

### Mixed Usage

Both styles can be combined (flags take precedence):

```bash
# File positional, search as flag
datagrep data.csv --search john

# File as flag, columns positional
datagrep --file data.csv "name,email" john

# All flags (most explicit)
datagrep --file data.csv --columns name,email --search john --ignore-case --output-format json
```

**Key Differences:**

| Aspect | Positional | Flags |
|--------|-----------|-------|
| **Syntax** | `datagrep file cols val` | `datagrep --file file --columns cols --search val` |
| **Order** | Fixed order | Any order |
| **Clarity** | Concise, compact | Self-documenting |
| **Flag Precedence** | N/A | Flags override positional |
| **Typing** | Shorter | More explicit |

## 📖 Detailed Usage

### Command Syntax (Both Styles)

**Positional style:**
```
datagrep [OPTIONS] [input_file] [columns] [value]
```

**Flag style:**
```
datagrep [OPTIONS] --file FILE --columns COLUMNS --search VALUE
```

**Arguments:**
- `input_file` / `--file FILE`: CSV/JSON/Excel file or `-` for stdin (optional, defaults to stdin)
- `columns` / `--columns COLUMNS`: Comma-separated field names to search
- `value` / `--search VALUE`: Search value or pattern

### Inspection Modes (No Search Value)

When no search value is provided, datagrep operates in inspection mode:

```bash
# Positional style
datagrep data.csv --describe
datagrep data.csv --sample 5

# Flag style
datagrep --file data.csv --describe
datagrep --file data.csv --sample 5
```

**Modes:**
```bash
# Show schema and samples (default)
datagrep --file data.csv

# Describe schema only
datagrep --file data.csv --describe

# Show first N rows
datagrep --file data.csv --sample 5
```

### Search Modes

**Contains (default)** - Substring matching:
```bash
# Both styles work the same
datagrep data.csv name john --ignore-case
datagrep --file data.csv --columns name --search john --ignore-case
```

**Exact** - Exact match:
```bash
datagrep data.csv name "John Smith" --mode exact
datagrep --file data.csv --columns name --search "John Smith" --mode exact
```

**Startswith** - Prefix matching:
```bash
datagrep data.csv email "john@" --mode startswith
datagrep --file data.csv --columns email --search "john@" --mode startswith
```

**Endswith** - Suffix matching:
```bash
datagrep data.csv email "@gmail.com" --mode endswith
datagrep --file data.csv --columns email --search "@gmail.com" --mode endswith
```

**Regex** - Regular expressions:
```bash
datagrep data.csv email "^[a-z]+@" --mode regex
datagrep --file data.csv --columns email --search "^[a-z]+@" --mode regex
```

### Filtering with --where

Pre-filter records before searching using WHERE conditions:

```bash
# Simple comparison
datagrep data.csv name alice --where "age > 25"
datagrep data.csv city london --where "population >= 1000000"

# String operations
datagrep data.csv product phone --where "type contains mobile"
datagrep data.csv domain google --where "url startswith https"

# Combined with AND/OR
datagrep data.csv name alice --where "age > 25 and city == London"
datagrep data.csv name alice --where "city == London or city == Paris"
datagrep data.csv product phone --where "price > 100 and stock > 0 and status == active"
```

**Supported Operators:**
- Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`
- String: `contains`, `startswith`, `endswith`
- Logic: `and`, `or`

### Sorting

Sort records by column before searching:

```bash
# Ascending (default)
datagrep data.csv name john --sort name:asc

# Descending
datagrep data.csv city london --sort population:desc

# Combine with where
datagrep data.csv email alice --where "age > 20" --sort age:desc
```

### Output Formats

**CSV** (default):
```bash
datagrep data.csv name john --output-format csv
```

**JSON**:
```bash
datagrep data.csv name john --output-format json --output results.json
```

**ASCII Table** (formatted):
```bash
datagrep data.csv name john --output-format table --color
```

**Raw** (Python dicts):
```bash
datagrep data.csv name john --output-format raw
```

### Selecting Columns

Control which columns appear in output:

```bash
# Default: all columns
datagrep data.csv name john

# Select specific columns
datagrep data.csv name john --select name,email,city

# Combine with sorting
datagrep data.csv name john --select email,name --sort name:asc
```

### Limiting and Previewing

```bash
# Limit results to first N matches
datagrep data.csv name alice --limit 100

# Show preview of first N matches
datagrep data.csv name alice --preview 10

# Count only (no output)
datagrep data.csv name alice --count

# Show count and display the data (works with all filters)
datagrep data.csv name alice --show-count
datagrep data.csv name alice --where "age > 25" --show-count
```

### Filtering by Empty or Not-Empty Values

Filter rows based on whether a column is empty or has a value:

```bash
# Find all rows with empty phone field
datagrep data.csv phone --empty

# Find all rows with non-empty email field
datagrep data.csv email --not-empty

# Works with multiple columns
datagrep data.csv phone,email --empty
```

### Working With Different Formats

**Auto-detection** (default):
```bash
# Detects format from extension
datagrep data.csv ...      # CSV
datagrep data.json ...     # JSON
datagrep data.xlsx ...     # Excel
datagrep - ...             # Stdin (detected from content)
```

**Explicit format**:
```bash
# Force format
datagrep myfile.data name john --input-format csv
datagrep myfile.data name john --input-format json --output-format table
```

**From stdin**:
```bash
cat data.csv | datagrep - name john
curl https://example.com/data.json | datagrep - field value --mode exact
type data.csv | datagrep - name john --delimiter ";"
```

### Performance Options

**Progress bar** (for large files):
```bash
datagrep large_file.csv name john --progress
```

**Delimiter specification** (non-standard CSV):
```bash
datagrep data.tsv name john --delimiter "\t"
datagrep data.psv name john --delimiter "|"
```

**Encoding** (for special characters):
```bash
datagrep data.csv name john --encoding utf-8     # Default
datagrep data.csv name john --encoding latin-1
datagrep data.csv name john --encoding ascii
```

### Configuration Files

Create reusable configurations in JSON:

**customer-search.json:**
```json
{
  "input_file": "customers.csv",
  "columns": "name,email",
  "output_format": "table",
  "color": true,
  "ignore_case": true,
  "mode": "contains"
}
```

**Usage:**
```bash
datagrep --config customer-search.json alice
```

See [examples/configs/](examples/configs/) for more configuration examples.

### Logging and Debugging

```bash
# Verbose output
datagrep data.csv name john --verbose

# Debug mode (detailed logging)
datagrep data.csv name john --debug

# Combine with count for diagnostics
datagrep data.csv name john --count --debug
```

## ✅ Best Practices

### 1. Always Inspect First

```bash
# Always check the schema before searching
datagrep data.csv --describe

# See sample data to understand structure
datagrep data.csv --sample 5
```

**Why:** Avoids column name typos and helps you understand the data format.

### 2. Use Exact Column Names

```bash
# ❌ Might not work - column might be 'Customer_Name'
datagrep data.csv name john

# ✅ Check first with --describe
datagrep data.csv --describe
# Then use exact name
datagrep data.csv Customer_Name john
```

### 3. Quote Values with Spaces

```bash
# ❌ Wrong - splits on space
datagrep data.csv name John Smith

# ✅ Correct - preserves spaces
datagrep data.csv name "John Smith"
```

### 4. Use Case-Insensitive for Unknown Cases

```bash
# ✅ Best practice - catches all variations
datagrep data.csv email john --ignore-case

# Matches: john, John, JOHN, JoHn, etc.
```

### 5. Pre-Filter Large Files

```bash
# ❌ Slow - searches all 1M records
datagrep huge_file.csv name john

# ✅ Fast - filters to 100K first, then searches name
datagrep huge_file.csv name john --where "status == active"
```

### 6. Use Output Formats Appropriately

```bash
# For quick viewing:
datagrep data.csv name john --output-format table --color

# For further processing:
datagrep data.csv name john --output-format json > results.json

# For spreadsheets:
datagrep data.csv name john --output-format csv --output results.csv
```

### 7. Start with --count

```bash
# See how many matches before full output
datagrep data.csv name john --count

# Then get actual results if count is reasonable
datagrep data.csv name john --limit 100
```

### 8. Use --select to Reduce Output

```bash
# Getting too much output?
# Select only the columns you need
datagrep data.csv email alice --select email,name,status --output-format table
```

### 9. Create Config Files for Repeated Queries

```bash
# Create query-config.json
cat > query-config.json << 'EOF'
{
  "input_file": "customers.csv",
  "columns": "name,email",
  "output_format": "table",
  "ignore_case": true,
  "color": true,
  "select": "name,email,city"
}
EOF

# Reuse it
datagrep --config query-config.json john
datagrep --config query-config.json alice
datagrep --config query-config.json smith
```

### 10. Use --empty/--not-empty for Data Quality

```bash
# Find incomplete records
datagrep data.csv "email,phone" --empty --output-format table

# Find complete records
datagrep data.csv "email,phone" --not-empty --output-format table
```

### Performance Tips

1. **Use `--limit`** - Stop after finding N results: `--limit 1000`
2. **Narrow columns** - Search fewer columns: `--columns email` instead of all
3. **Pre-filter** - Use `--where` to filter before searching
4. **Use `--progress`** - Monitor long-running searches: `--progress`
5. **Check file size** - Very large files need optimization: `datagrep data.csv --describe`

### Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Typo in column name | "Field not found" error | Use `--describe` to see available columns |
| Forgetting quotes | `"John Smith"` treated as two values | Always quote multi-word values: `"John Smith"` |
| Case sensitivity | Misses `John` when searching for `john` | Use `--ignore-case` flag |
| No pre-filtering | Slow search on huge files | Use `--where` to pre-filter first |
| Wrong output format | Can't use results with other tools | Choose format that matches your needs |

## 📚 Real-World Examples

### Finding customers by city (case-insensitive)

```bash
datagrep customers.csv city "new york" --ignore-case
datagrep customers.csv city "new york" --ignore-case --output-format table --color
```

### Analyzing logs with filtering

```bash
# Find ERROR logs from today
datagrep app.log level ERROR --where "date == 2024-04-08"

# Count WARN logs
datagrep app.log level WARN --count

# Export errors to JSON
datagrep app.log level ERROR --output-format json --output errors.json
```

### Inventory stock check

```bash
# Find out-of-stock items
datagrep products.csv sku "%" --where "stock == 0" --output-format table

# Low stock items
datagrep products.xlsx sku "%" --where "stock > 0 and stock < 10" --sort stock:asc
```

### Email validation and extraction

```bash
# Find Gmail users
datagrep users.csv email "@gmail.com" --mode endswith --select email,name

# Extract work emails (regex)
datagrep users.csv email "@company\\.com$" --mode regex
```

### Text searching

```bash
# Find documents containing keywords
datagrep documents.json content "machine learning" --output results.json

# Multi-word search with regex
datagrep documents.json content "^(machine|deep) learning" --mode regex
```

### Data export and transformation

```bash
# Export CSV to JSON
datagrep data.csv "*" "%" --output-format json --output data.json

# Filter and re-export
datagrep data.csv name "*" --where "status == active" --output-format csv --output active_users.csv

# Convert Excel to JSON
datagrep data.xlsx field value --output-format json --output data.json
```

## 🔧 Options Reference

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| **Input Arguments** | | | | |
| `--file` | `-f` | PATH | stdin | Input file path (modern flag style) |
| `--columns` | | STR | * | Columns to search (modern flag style) |
| `--search` | `-S` | STR | | Search value/pattern (modern flag style) |
| **Search Options** | | | | |
| `--input-format` | | CHOICE | auto | Input format: auto,csv,json,xlsx |
| `--mode` | | CHOICE | contains | Search mode: contains,exact,startswith,endswith,regex |
| `--ignore-case` | `-i` | BOOL | False | Ignore case in search |
| **Output Options** | | | | |
| `--delimiter` | `-d` | STR | , | CSV delimiter |
| `--encoding` | | STR | utf-8 | File encoding |
| `--output-format` | | CHOICE | csv | Output: csv,json,table,raw |
| `--select` | `-s` | STR | * | Columns in output (comma-sep) |
| `--output` | `-o` | PATH | stdout | Output file |
| **Filtering Options** | | | | |
| `--limit` | `-n` | INT | 0 | Max results (0=unlimited) |
| `--sort` | | STR | | Sort: column:asc or column:desc |
| `--where` | | STR | | Filter: "column op value" |
| `--empty` | | BOOL | False | Show rows where column is empty |
| `--not-empty` | | BOOL | False | Show rows where column has value |
| **Inspection Modes** | | | | |
| `--count` | | BOOL | False | Count only, no output |
| `--show-count` | | BOOL | False | Show count and display filtered data |
| `--describe` | | BOOL | False | Show schema only |
| `--sample` | | INT | 0 | Show sample N rows |
| `--preview` | | INT | 0 | Preview N rows (with search) |
| **Other Options** | | | | |
| `--config` | | PATH | | Load config from JSON file |
| `--color` | | BOOL | False | Colorize output |
| `--progress` | | BOOL | False | Show progress bar |
| `--verbose` | `-v` | BOOL | False | Verbose logging |
| `--debug` | | BOOL | False | Debug logging |
| `--version` | | | | Show version |
| `--help` | `-h` | | | Show help |

**Notes:**
- Input arguments can use **positional style** (`datagrep file cols val`) or **flag style** (`datagrep --file file --columns cols --search val`)
- When using flag style, order doesn't matter
- If both positional and flag versions are provided, flags take precedence

## 🐚 Shell Completion

### Bash

```bash
# Install
sudo cp completion/datagrep.bash /usr/share/bash-completion/completions/datagrep

# Or add to ~/.bashrc
source ~/path/to/completion/datagrep.bash
```

### Zsh

```bash
# Install
cp completion/datagrep.zsh /usr/share/zsh/site-functions/_datagrep

# Or add to ~/.zshrc
fpath+=(~/path/to/completion)
autoload -Uz compinit && compinit
```

### Fish

```bash
cp completion/datagrep.fish ~/.config/fish/completions/
```

### PowerShell

```powershell
# Add to $PROFILE
. C:\path\to\completion\datagrep.ps1
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest tests -v

# Run specific test class
python -m unittest tests.TestSearchMatchers -v

# Run with coverage
coverage run -m unittest tests
coverage report
coverage html  # Generate HTML report
```

The project includes 26+ tests covering:
- Argument validation
- All search modes
- WHERE condition parsing
- JSON loading (arrays and NDJSON)
- Table formatting
- Error cases and edge cases

## 📝 Configuration Files

Store common settings in JSON configuration files:

```jsonc
{
  // Input/Output
  "input_file": "customers.csv",
  "output_file": "", 
  
  // Search
  "columns": "name,email,city",
  "mode": "contains",
  "ignore_case": true,
  
  // Filtering & Sorting  
  "where": "status == active",
  "sort": "name:asc",
  "limit": 100,
  
  // Output
  "output_format": "table",
  "select": "name,email",
  "color": true,
  
  // Performance
  "progress": true,
  "verbose": false
}
```

Load with: `datagrep --config my_config.json [value]`

## 🐛 Troubleshooting

### Common Issues

**"No such file or directory"**
```bash
# Check file path
ls data.csv

# Use absolute path if needed
datagrep /full/path/to/data.csv name john
```

**Encoding errors**
```bash
# Specify encoding
datagrep data.csv name value --encoding latin-1
```

**Large file crashes**
```bash
# Use progress bar and limit results
datagrep large_file.csv field value --progress --limit 1000

# See PERFORMANCE.md for optimization strategies
# Large file support planned for Phase 2
```

**Column not found**
```bash
# Check available columns
datagrep data.csv --describe

# Use correct column name
datagrep data.csv "ColumnName" search_value
```

See [docs/INSTALL.md](docs/INSTALL.md) for more troubleshooting steps.

## ❓ FAQ

### Installation & Setup

**Q: How do I install datagrep?**  
A: Run `pip install datagrep-cli`. For development features (color, progress, Excel), use `pip install datagrep-cli[color,progress,excel]`. See [Installation](#-installation) for details.

**Q: What Python versions are supported?**  
A: Python 3.7 and above. Use `python --version` to check yours.

**Q: Do I need dependencies installed?**  
A: Core functionality works with Python stdlib only. Color output requires `colorama`, progress bars require `tqdm`, Excel support requires `openpyxl`. These are optional.

**Q: Can I use datagrep on Windows?**  
A: Yes! Fully supported on Windows, macOS, and Linux. Use `datagrep` command in PowerShell, CMD, or any terminal.

### Usage Questions

**Q: Which syntax style should I use - positional or flags?**  
A: Both work! Use positional style (`datagrep file cols val`) for quick commands. Use flag style (`datagrep --file file --columns cols --search val`) for scripts and clarity. See [Migration Guide](MIGRATION.md) for details.

**Q: How do I search multiple columns?**  
A: Use comma-separated column names: `datagrep data.csv "name,email,phone" "john"`

**Q: Can I search with case-insensitive matching?**  
A: Yes! Add `--ignore-case` flag: `datagrep data.csv name john --ignore-case`

**Q: What's the difference between `--where` and search?**  
A: `--where` pre-filters records before searching. Search looks within field values. Combine both: `datagrep data.csv name alice --where "age > 25"`

**Q: How do I search for exact matches only?**  
A: Use `--mode exact`: `datagrep data.csv name "John Smith" --mode exact`

**Q: Can I use regular expressions?**  
A: Yes! Use `--mode regex`: `datagrep data.csv email "^[a-z]+@" --mode regex`

**Q: How do I read from stdin?**  
A: Use `-` as filename or omit it: `cat data.csv | datagrep - name john` or `cat data.csv | datagrep name john`

### Output & Formatting

**Q: How do I save results to a file?**  
A: Use `--output`: `datagrep data.csv name john --output results.csv`

**Q: What output formats are available?**  
A: Four formats: `csv` (default), `json`, `table` (formatted), `raw` (Python dicts). Use `--output-format json` to switch.

**Q: Can I select which columns to output?**  
A: Yes! Use `--select`: `datagrep data.csv name john --select name,email,city`

**Q: How do I get a formatted table output?**  
A: Use `--output-format table`: `datagrep data.csv name john --output-format table --color`

**Q: Can I limit the number of results?**  
A: Yes! Use `--limit N`: `datagrep data.csv name alice --limit 100`

### File Handling

**Q: What file formats does datagrep support?**  
A: CSV (default), JSON (arrays and newline-delimited), Excel (XLSX), and stdin. Auto-detection works by file extension.

**Q: How do I specify a different CSV delimiter?**  
A: Use `--delimiter`: `datagrep data.tsv name john --delimiter "\t"`

**Q: What encodings are supported?**  
A: All Python-supported encodings. Default is UTF-8. Specify with `--encoding latin-1` if needed.

**Q: Can I work with very large files?**  
A: Files up to 1GB work well. For larger files, see [Performance Guide](docs/PERFORMANCE.md). Use `--limit` to restrict results.

**Q: Does datagrep support stdin?**  
A: Yes! Pipe any data: `cat file.csv | datagrep --columns name --search john`

### Features & Capabilities

**Q: Can I filter by empty or missing values?**  
A: Yes! Use `--empty` or `--not-empty`: `datagrep data.csv phone --empty` finds records with missing phone numbers.

**Q: How do I sort results?**  
A: Use `--sort`: `datagrep data.csv name john --sort name:asc` or `name:desc`

**Q: Can I combine multiple filters?**  
A: Yes! Mix conditions: `datagrep data.csv name alice --where "age > 25 and city == London" --sort name:asc`

**Q: Are there configuration files?**  
A: Yes! Create JSON files with your settings. Use `--config my_config.json value` to apply them. See [Configuration Files](#-configuration-files).

**Q: Can I get a count of matching records?**  
A: Yes! Use `--count` to show only the count: `datagrep data.csv name alice --count`. Use `--show-count` to display the count AND the data: `datagrep data.csv name alice --show-count`. Both work with filters like `--where`, `--sort`, `--empty`, and `--not-empty`.

**Q: How do I see the file schema without searching?**  
A: Use `--describe`: `datagrep data.csv --describe` shows all field names.

### Performance & Logging

**Q: How do I see debug information?**  
A: Use `--verbose` for info logs or `--debug` for detailed logs: `datagrep data.csv name john --debug`

**Q: Can I see progress for large files?**  
A: Yes! Use `--progress`: `datagrep large_file.csv name john --progress`

**Q: How do I make searches faster?**  
A: Use `--limit` to stop after N results, use `--where` to pre-filter, or narrow columns. See [Performance Guide](docs/PERFORMANCE.md).

**Q: What should I do if searching is slow?**  
A: Check file size with `ls -lh`. Use `--limit` to test. Add `--where` to pre-filter. See troubleshooting section above.

### Troubleshooting

**Q: I get "No records found" but I know they exist?**  
A: Check spelling: `datagrep data.csv --describe` shows available columns. Try `--ignore-case`. Verify case sensitivity with `--mode exact`.

**Q: The output looks wrong. How do I debug?**  
A: Use `--debug` flag and check logs. Verify column names with `--describe`. Test with `--sample 5` to inspect data.

**Q: Can I use special characters in search?**  
A: Yes! Wrap in quotes: `datagrep data.csv name "O'Brien"` or `datagrep data.csv email "user+tag@example.com"`

**Q: Does datagrep support Unicode?**  
A: Yes! Full Unicode support including Arabic, Chinese, emoji. Set `--encoding utf-8` if needed.

**Q: How do I report bugs?**  
A: See [Support](#-support) section. Include Python version (`python --version`), datagrep version (`datagrep --version`), and a sample of your data (if shareable).

### Version Support & Compatibility

**Python Version:** 3.7, 3.8, 3.9, 3.10, 3.11, 3.12+  
**Operating Systems:** Windows, macOS, Linux, WSL  
**Shell Support:** bash, zsh, fish, PowerShell, CMD  
**File Size:** Optimized up to 1GB (see Phase 2 roadmap for larger)  
**File Formats:** CSV, JSON, NDJSON, Excel XLSX  

## 📖 Documentation

- [Installation Guide](docs/INSTALL.md) - Setup, troubleshooting, and system requirements
- [Performance & Scalability](docs/PERFORMANCE.md) - File size limits, optimization roadmap
- [Development Guide](docs/DEVELOPMENT.md) - Architecture, debugging, profiling
- [Contributing](docs/CONTRIBUTING.md) - How to contribute code and report issues
- [Project Structure](PROJECT_STRUCTURE.md) - Folder organization and layout

## 🤝 Contributing

Contributions are welcome! Please see [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with Python 3.7+ and influenced by powerful Unix tools like `grep`, `sed`, and `awk`.

## � Getting Help

### Built-in Help

```bash
# View all available options
datagrep --help

# View short help for specific commands
datagrep --help | grep "search"

# Check your version
datagrep --version
```

### Quick Diagnostics

When something isn't working, try:

```bash
# 1. Check installation
datagrep --version

# 2. Inspect your file
datagrep your_file.csv --describe

# 3. Test with simple search
datagrep your_file.csv column_name test_value

# 4. Enable debug output
datagrep your_file.csv column_name test_value --debug

# 5. Check file size (might be loading issue)
ls -lh your_file.csv
```

### Documentation

- **This README** - Full feature documentation and examples
- [Installation Guide](docs/INSTALL.md) - Setup, troubleshooting, system specifics
- [Performance Guide](docs/PERFORMANCE.md) - File size limits, optimization, roadmap
- [Development Guide](docs/DEVELOPMENT.md) - Architecture, contributing code
- [Migration Guide](MIGRATION.md) - Transitioning between positional/flag syntax
- [Common Workflows](examples/) - Sample data and pre-built configs

### Troubleshooting Tips

1. **"Column not found"** → Run `datagrep file.csv --describe` to see available columns
2. **"No records found"** → Try `--ignore-case` or `--mode exact`
3. **"Search is slow"** → Use `--limit 100` to test, add `--where` to pre-filter
4. **"Encoding error"** → Try `--encoding utf-8` or `--encoding latin-1`
5. **"Command not found"** → Reinstall: `pip install --upgrade datagrep-cli`

See [Troubleshooting](README.md#-troubleshooting) section for more common issues.

## 📮 Support & Feedback

### Report Issues

Found a bug? Have feedback? Here's how to help:

1. **Check [Troubleshooting](#-troubleshooting)** - Your issue might be answered there
2. **Check [FAQ](#-faq)** - Look for similar questions
3. **Search existing issues** - Someone might have reported it: [GitHub Issues](https://github.com/yourusername/datagrep-cli/issues)
4. **Open new issue** with:
   - Your Python version: `python --version`
   - Your datagrep version: `datagrep --version`
   - Your command: `datagrep ... (sanitized)`
   - Error message or unexpected output
   - OS: Windows/macOS/Linux

### Ask Questions

- **General questions**: [GitHub Discussions](https://github.com/yourusername/datagrep-cli/discussions)
- **Quick help**: Check the [FAQ](#-faq) section
- **Email support**: Create a GitHub issue marked with `[QUESTION]`

### Contribute

Want to help improve datagrep? See [Contributing Guide](docs/CONTRIBUTING.md) for:
- How to submit code changes
- How to report bugs
- How to suggest features
- Development setup instructions

## 🔮 Future Roadmap

See [docs/PERFORMANCE.md](docs/PERFORMANCE.md) for complete optimization roadmap including:

**Phase 2 (v1.1)** - Performance Optimization:
- Streaming mode for files > 1GB (lazy loading)
- Parallel processing with `--parallel` flag (4-8x speedup)
- Statistics & monitoring with `--stats` flag
- Memory-mapped file support

**Phase 3+ (v1.2+)** - Advanced Features:
- Database support (SQLite, PostgreSQL, MySQL)
- Indexed searching for repeated queries
- Distributed processing (Dask/Ray)
- Web UI for interactive searching
- Column statistics and aggregations
