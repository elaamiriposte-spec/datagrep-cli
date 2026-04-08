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

## ⭐ Features

- **Multi-Format Support**: CSV, JSON, Excel (XLSX), and stdin
- **Flexible Search Modes**: Contains, exact, startswith, endswith, regex patterns
- **Advanced Filtering**: Pre-filter records with `--where` conditions (AND/OR logic)
- **Sorting**: Sort by column in ascending/descending order before searching
- **Unicode Support**: Full support for Arabic, Chinese, and other Unicode content
- **Multiple Output Formats**: CSV, JSON, ASCII table, raw dictionaries
- **Intelligent Modes**: Count-only, schema inspection, sampling
- **Performance Features**: Progress bars for large files, streaming where possible
- **Developer Friendly**: Complete type hints, comprehensive error messages, detailed logging
- **Flexible Deployment**: Traditional pip install, Docker support, shell completions
- **Configuration Files**: JSON-based defaults for repeatable operations
- **Well-Tested**: 26+ comprehensive unit tests with full code coverage

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

See [INSTALL.md](INSTALL.md) for detailed installation instructions and troubleshooting.

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

See [examples/](examples/) directory for more configuration examples.

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
```

**Column not found**
```bash
# Check available columns
datagrep data.csv --describe

# Use correct column name
datagrep data.csv "ColumnName" search_value
```

See [INSTALL.md](INSTALL.md) for more troubleshooting steps.

## 📖 Documentation

- [Installation Guide](INSTALL.md) - Detailed install instructions
- [Development Guide](DEVELOPMENT.md) - For contributors
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Code Review](CODE_REVIEW.md) - Architecture and improvements

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with Python 3.7+ and influenced by powerful Unix tools like `grep`, `sed`, and `awk`.

## 📮 Support

- Report bugs: [GitHub Issues](https://github.com/yourusername/datagrep-cli/issues)
- Ask questions: [GitHub Discussions](https://github.com/yourusername/datagrep-cli/discussions)
- View docs: [Full Documentation](https://github.com/yourusername/datagrep-cli#readme)

## 🔮 Future Enhancements

- [ ] Web UI for interactive searching
- [ ] Database support (PostgreSQL, MySQL)
- [ ] Parallel processing for large files
- [ ] Column statistics and aggregations
- [ ] Data validation profiles
- [ ] Export to additional formats (XML, Parquet, HDF5)
```

#### JSON output with progress

```bash
python search_csv.py large_file.csv name test --output-format json --progress
```

#### Excel input

```bash
python search_csv.py data.xlsx name John --input-format xlsx
```

#### Read from stdin

```bash
type arabic_sample.csv | python search_csv.py - name دبي --delimiter ,
```

#### Describe file schema

```bash
python search_csv.py arabic_sample.csv name --describe
```

This shows field names and sample values without searching.

## Options

- `--input-format`: `auto` (default), `csv`, `json`, `xlsx`
- `--mode`: `contains` (default), `exact`, `startswith`, `endswith`, `regex`
- `--ignore-case` or `-i`
- `--delimiter` or `-d` (default: `,`)
- `--encoding` (default: `utf-8`)
- `--output-format`: `csv` (default), `json`, `table`, `raw`
- `--select` or `-s` to choose output columns (default: all)
- `--output` or `-o` to write results to a file
- `--limit` or `-n` to stop after a number of matching rows
- `--sort` to sort by column:asc or column:desc
- `--where` to filter with conditions like "column > value"
- `--count` to only count matches
- `--config` to load settings from JSON file
- `--color` to colorize output (requires colorama)
- `--progress` to show progress bar (requires tqdm)
- `--preview` to show only the first N matching rows
- `--sample` to show the first N rows as sample
- `--verbose` or `-v` to enable verbose logging
- `--debug` to enable debug logging
- `--describe` to show field names and sample values
- `--help` to display usage details

## Where Conditions

Use `--where` for pre-filtering records. Supported operators:

- `==`, `!=`, `>`, `<`, `>=`, `<=` (numeric/string comparison)
- `contains`, `startswith`, `endswith` (string operations)
- `and`, `or` for combining conditions

Examples:
- `--where "age > 25"`
- `--where "name contains John"`
- `--where "city == London"`
- `--where "age > 25 and city == London"`
- `--where "name contains John or age < 30"`

## Configuration Files

Create a JSON file with default options:

```json
{
  "ignore_case": true,
  "output_format": "table",
  "color": true
}
```

Then use: `python search_csv.py file.csv name value --config config.json`

## Dependencies

Optional packages for enhanced features:
- `pip install colorama` for colored output
- `pip install tqdm` for progress bars
- `pip install openpyxl` for Excel support

## Testing

Run unit tests:

```bash
python tests.py
```

## Notes

- Input files must have consistent field names (CSV headers, JSON keys, Excel headers).
- Use UTF-8 encoded files for Arabic and other non-Latin data.
- Auto-detection works for `.csv`, `.json`, `.xlsx` extensions.
- For large files, use `--progress` to monitor processing.
