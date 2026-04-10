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

## 📦 Installation

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

## 🚀 Quick Start

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

## 📖 Detailed Usage

### Command Syntax

```
datagrep [OPTIONS] [input_file] [columns] [value]
```

**Arguments:**
- `input_file`: CSV/JSON/Excel file or `-` for stdin (optional, defaults to stdin)
- `columns`: Comma-separated field names to search, or leave empty for inspection mode
- `value`: Search value or pattern

### Inspection Modes (No Search Value)

When no search value is provided, datagrep operates in inspection mode:

```bash
# Show schema and samples
datagrep data.csv

# Describe schema only
datagrep data.csv --describe

# Show first N rows
datagrep data.csv --sample 5

# Show first N matching rows (when searching)
datagrep data.csv email gmail --preview 10

# Count total records
datagrep data.csv --count
```

### Search Modes

**Contains (default)** - Substring matching:
```bash
datagrep data.csv name john
datagrep data.csv name john --ignore-case  # Case-insensitive
```

**Exact** - Exact match:
```bash
datagrep data.csv name "John Smith" --mode exact
```

**Startswith** - Prefix matching:
```bash
datagrep data.csv email "john@" --mode startswith
```

**Endswith** - Suffix matching:
```bash
datagrep data.csv email "@gmail.com" --mode endswith
```

**Regex** - Regular expressions:
```bash
datagrep data.csv email "^[a-z]+@" --mode regex
datagrep data.csv phone "\\d{3}-\\d{4}" --mode regex
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
| `--input-format` | | CHOICE | auto | Input format: auto,csv,json,xlsx |
| `--mode` | | CHOICE | contains | Search mode: contains,exact,startswith,endswith,regex |
| `--ignore-case` | `-i` | BOOL | False | Ignore case in search |
| `--delimiter` | `-d` | STR | , | CSV delimiter |
| `--encoding` | | STR | utf-8 | File encoding |
| `--output-format` | | CHOICE | csv | Output: csv,json,table,raw |
| `--select` | `-s` | STR | * | Columns in output (comma-sep) |
| `--output` | `-o` | PATH | stdout | Output file |
| `--limit` | `-n` | INT | 0 | Max results (0=unlimited) |
| `--sort` | | STR | | Sort: column:asc or column:desc |
| `--where` | | STR | | Filter: "column op value" |
| `--empty` | | BOOL | False | Show rows where column is empty |
| `--not-empty` | | BOOL | False | Show rows where column has value |
| `--count` | | BOOL | False | Count only, no output |
| `--config` | | PATH | | Load config from JSON file |
| `--color` | | BOOL | False | Colorize output |
| `--progress` | | BOOL | False | Show progress bar |
| `--preview` | | INT | 0 | Preview N rows (0=unlimited) |
| `--sample` | | INT | 0 | Show sample N rows |
| `--verbose` | `-v` | BOOL | False | Verbose logging |
| `--debug` | | BOOL | False | Debug logging |
| `--describe` | | BOOL | False | Show schema only |
| `--version` | | | | Show version |
| `--help` | `-h` | | | Show help |

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

## 📮 Support

- Report bugs: [GitHub Issues](https://github.com/yourusername/datagrep-cli/issues)
- Ask questions: [GitHub Discussions](https://github.com/yourusername/datagrep-cli/discussions)
- View docs: [Full Documentation](https://github.com/yourusername/datagrep-cli#readme)

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
