# Command Options Reference

Complete reference for all command-line options and flags.

## Table of Contents

- [File Options](#file-options)
- [Search Options](#search-options)
- [Output Options](#output-options)
- [Filter Options](#filter-options)
- [Inspection Options](#inspection-options)
- [Display Options](#display-options)
- [Configuration Options](#configuration-options--)
- [Administrative Options](#administrative-options)

## File Options

### `input_file` / `--file`

Input file path to search.

**Type:** String (positional or flag)  
**Short Flag:** `-f`  
**Default:** Reads from stdin if not provided

**Usage:**
```bash
# Positional style
datagrep customers.csv name john

# Flag style
datagrep --file customers.csv --columns name --search john

# Read from stdin
datagrep - name john < data.csv
cat data.csv | datagrep - name john

# Read from stdin (explicit)
datagrep --file - --columns name --search john
```

**Supported Formats:**
- CSV (comma-separated, tab-separated)
- JSON (arrays, newline-delimited)
- Excel (XLSX, requires openpyxl)
- Plain text via stdin

### `--input-format`

Explicitly specify input file format.

**Type:** Choice `{auto,csv,json,xlsx}`  
**Default:** `auto` (auto-detect based on extension)

**Usage:**
```bash
# Explicit CSV parsing
datagrep data.txt name john --input-format csv

# Explicit JSON
datagrep data.json name john --input-format json

# Explicit Excel
datagrep data.xlsx name john --input-format xlsx
```

### `--encoding`

File encoding (input and output).

**Type:** String  
**Default:** `utf-8`

**Common Values:**
- `utf-8` - Unicode, international characters
- `latin-1` / `iso-8859-1` - Western European
- `cp1252` - Windows Western European
- `ascii` - ASCII only
- `gbk` / `gb2312` - Chinese
- `shift_jis` - Japanese

**Usage:**
```bash
# Specify encoding
datagrep data.csv name john --encoding latin-1

# UTF-8 with BOM
datagrep data.csv name john --encoding utf-8-sig
```

### `--delimiter`

CSV field delimiter character.

**Type:** String  
**Short Flag:** `-d`  
**Default:** `,` (comma)

**Usage:**
```bash
# Tab-separated values
datagrep data.tsv name john --delimiter $'\t'

# Semicolon delimiter
datagrep data.csv name john --delimiter ';'

# Pipe delimiter
datagrep data.txt name john --delimiter '|'

# Custom delimiter
datagrep data.txt name john --delimiter '::'
```

## Search Options

### `columns` / `--columns`

Which columns to search.

**Type:** String (comma-separated)  
**Default:** All columns in file

**Usage:**
```bash
# Single column
datagrep data.csv name john

# Multiple columns
datagrep data.csv "name,email" john

# Wildcard (all columns)
datagrep data.csv "*" john
```

**Note:** Column names are case-sensitive and must exactly match headers.

### `value` / `--search`

What value to search for.

**Type:** String  
**Short Flag:** `-S`

**Usage:**
```bash
# Simple string
datagrep data.csv name john

# With spaces (quote if needed)
datagrep data.csv name "John Doe"

# Regular expression (with --mode regex)
datagrep data.csv email "^[a-z]+@gmail\.com$" --mode regex
```

### `--mode`

Search mode/matching algorithm.

**Type:** Choice `{contains,exact,startswith,endswith,regex}`  
**Default:** `contains`

**Modes:**

| Mode | Behavior | Example | Matches |
|------|----------|---------|---------|
| `contains` | Substring match (default) | `"john"` | John Smith, johnny, nojohn |
| `exact` | Exact match only | `"John"` | John (not John Smith) |
| `startswith` | Prefix match | `"john"` | john@..., johndoe, JOHN... |
| `endswith` | Suffix match | `"@gmail.com"` | john@gmail.com, alice@gmail.com |
| `regex` | Regular expression | `"^j.*n$"` | john, jan, jawn (regex pattern) |

**Usage:**
```bash
# Substring (default)
datagrep data.csv name john

# Exact match
datagrep data.csv status active --mode exact

# Regex
datagrep data.csv email "^[a-z]+@.+\.com$" --mode regex
```

### `--ignore-case`

Case-insensitive matching.

**Type:** Flag (boolean)  
**Short Flag:** `-i`  
**Default:** `false` (case-sensitive)

**Usage:**
```bash
# Find 'john' in any case
datagrep data.csv name john --ignore-case

# Matches: John, JOHN, john, jOhN

# Works with all modes
datagrep data.csv email "@gmail.com" --mode endswith --ignore-case
```

## Output Options

### `--output-format`

Output format for results.

**Type:** Choice `{csv,json,table,raw}`  
**Default:** `csv`

**Formats:**

| Format | Description | Best For |
|--------|-------------|----------|
| `csv` | CSV format (default) | Files, data processing |
| `json` | JSON array format | APIs, data exchange |
| `table` | ASCII table | Console viewing |
| `raw` | Python dict per line | Custom parsing |

**Usage:**
```bash
# CSV (default)
datagrep data.csv name john

# JSON
datagrep data.csv name john --output-format json

# Table
datagrep data.csv name john --output-format table

# Raw
datagrep data.csv name john --output-format raw
```

### `--output`

Write results to file instead of stdout.

**Type:** String (file path)  
**Short Flag:** `-o`  
**Default:** stdout

**Usage:**
```bash
# Write to file
datagrep data.csv name john --output results.csv

# Different format
datagrep data.csv name john --output-format json --output results.json

# Absolute path
datagrep data.csv name john --output /tmp/results.csv
```

### `--select`

Output only specific columns.

**Type:** String (comma-separated)  
**Short Flag:** `-s`  
**Default:** All columns

**Usage:**
```bash
# Show only name and email
datagrep data.csv name john --select name,email

# Single column
datagrep data.csv name john --select email

# Works with all formats
datagrep data.csv name john --select name,email --output-format json
```

## Filter Options

### `--where`

Pre-filter records before searching.

**Type:** String (condition expression)  
**Default:** No filtering

**Syntax:**
- Operators: `==`, `!=`, `>`, `<`, `>=`, `<=`
- String ops: `contains`, `startswith`, `endswith`
- Logic: `and`, `or`

**Usage:**
```bash
# Greater than
datagrep data.csv status active --where "age > 25"

# String contains
datagrep data.csv product phone --where "description contains wireless"

# Multiple conditions (AND)
datagrep data.csv status active --where "age > 25 and salary >= 50000"

# Multiple conditions (OR)
datagrep data.csv city london --where "population > 1000000 or famous == true"

# Complex
datagrep data.csv product phone --where "price > 100 and stock > 0 and status == active"
```

### `--sort`

Sort results before searching.

**Type:** String (column:direction)  
**Default:** No sorting

**Direction:** `asc` (ascending) or `desc` (descending)

**Usage:**
```bash
# Sort ascending (A-Z, 0-9 first)
datagrep data.csv status active --sort name:asc

# Sort descending (Z-A, 9-0 first)
datagrep data.csv status active --sort salary:desc

# Combine with WHERE
datagrep data.csv status active --where "age > 20" --sort age:desc --limit 10
```

### `--empty`

Show only records where specified column is empty/null.

**Type:** Flag + column name  
**Default:** Show all (not just empty)

**Usage:**
```bash
# Find records with empty phone_number
datagrep data.csv phone_number --empty

# Use with select to see other columns
datagrep data.csv phone_number --empty --select name,email,status
```

### `--not-empty`

Show only records where specified column has a value.

**Type:** Flag + column name  
**Default:** Show all

**Usage:**
```bash
# Find customers with phone numbers
datagrep data.csv phone_number --not-empty

# Count customers with email addresses
datagrep data.csv email --not-empty --count
```

### `--limit`

Maximum number of matching records to return.

**Type:** Integer  
**Short Flag:** `-n`  
**Default:** `0` (unlimited)

**Usage:**
```bash
# First 10 matches
datagrep data.csv status active --limit 10

# First 100 matches
datagrep data.csv name john --limit 100

# Unlimited (all matches)
datagrep data.csv status active --limit 0
```

**Performance Tip:** Using `--limit` stops searching after finding N matches, which speeds up large file searches.

## Inspection Options

### `--describe`

Show file schema and sample records.

**Type:** Flag (boolean)  
**Default:** `false`

**Usage:**
```bash
# Describe file (no search value needed)
datagrep data.csv --describe

# Output: Column names and first 10 rows
```

**Output:**
```
Schema:
  - name
  - email
  - status
  - salary

Sample rows (first 10):
name        | email                 | status   | salary
------------|----------------------|----------|--------
John Smith  | john@example.com     | active   | 50000
Alice Brown | alice@example.com    | inactive | 60000
```

### `--sample`

Show first N rows (inspection mode).

**Type:** Integer  
**Default:** `0` (no sample)

**Usage:**
```bash
# Show first 5 rows
datagrep data.csv --sample 5

# Show first 20 rows
datagrep data.csv --sample 20
```

### `--preview`

Show first N matching records.

**Type:** Integer  
**Default:** `0` (unlimited)

**Usage:**
```bash
# Find first 5 matches
datagrep data.csv name john --preview 5

# Find first 20 matches of pattern
datagrep data.csv email "@gmail" --preview 20
```

**Difference from --limit:**
- `--limit`: Search efficiency (stop early)
- `--preview`: Output filtering (show first N of results)

## Display Options

### `--count`

Count matching records instead of showing them.

**Type:** Flag (boolean)  
**Default:** `false` (show records)

**Usage:**
```bash
# Count active customers
datagrep data.csv status active --count

# Count with WHERE filtering
datagrep data.csv status active --where "salary > 50000" --count

# Output: Just a number
# 47
```

### `--show-count`

Display count before showing results.

**Type:** Flag (boolean)  
**Default:** `false` (no count prefix)

**Usage:**
```bash
# Show count and results
datagrep data.csv status active --show-count

# Output:
# Count: 47
# (then the 47 records)
```

### `--color`

Colorize table output (if colorama installed).

**Type:** Flag (boolean)  
**Default:** `false` (no colors)

**Usage:**
```bash
# Colored table output
datagrep data.csv status active --output-format table --color

# Requires: pip install datagrep-cli[color]
```

### `--progress`

Show progress bar for large files (if tqdm installed).

**Type:** Flag (boolean)  
**Default:** `false` (no progress bar)

**Usage:**
```bash
# Show progress while searching
datagrep huge_file.csv status active --progress

# Requires: pip install datagrep-cli[progress]
```

### `--verbose`

Verbose logging (info level).

**Type:** Flag (boolean)  
**Short Flag:** `-v`  
**Default:** `false`

**Usage:**
```bash
# Show info messages
datagrep data.csv name john --verbose

# Output: Logging information about operations
```

### `--debug`

Debug logging (debug level).

**Type:** Flag (boolean)  
**Default:** `false`

**Usage:**
```bash
# Show debug messages (very verbose)
datagrep data.csv name john --debug

# Output: Detailed debug information
```

## Configuration Options

### `--config`

Load options from JSON configuration file.

**Type:** String (file path)  
**Default:** None

**Usage:**
```bash
# Create config file
cat > search.json << EOF
{
  "input_file": "customers.csv",
  "columns": "name",
  "search_value": "john",
  "where": "age > 25",
  "limit": 100,
  "output_format": "json",
  "ignore_case": true
}
EOF

# Use config
datagrep --config search.json --output results.json
```

**Note:** Command-line flags override config file settings.

## Administrative Options

### `--version`

Display version number.

**Type:** Flag (boolean)

**Usage:**
```bash
datagrep --version

# Output: datagrep 1.0.0
```

### `--help`

Display help message.

**Type:** Flag (boolean)  
**Short Flag:** `-h`

**Usage:**
```bash
datagrep --help

# Shows usage and all available options

# Help for specific feature
datagrep --help | grep "where"
```

## Examples by Task

### Task: Find active users

```bash
datagrep users.csv status active
datagrep --file users.csv --columns status --search active
```

### Task: Find and count

```bash
datagrep users.csv status active --count
datagrep users.csv status active --show-count
```

### Task:Find with filters

```bash
datagrep users.csv status active --where "age > 25 and salary >= 50000"
```

### Task: Export to JSON

```bash
datagrep users.csv status active --output-format json --output results.json
```

### Task: View as table

```bash
datagrep users.csv status active --output-format table --color --limit 20
```

### Task: Complex search

```bash
datagrep users.csv email @gmail.com \
  --where "status == active and age > 30" \
  --mode endswith \
  --ignore-case \
  --sort name:asc \
  --limit 10 \
  --select name,email,age \
  --output-format table \
  --show-count
```

### Task: Check file structure

```bash
datagrep data.csv --describe
datagrep data.csv --sample 10
```

## Option Combinations

### Valid Combinations

```
--file + --columns + --search       ✓ Normal search
--file + --describe                 ✓ Schema inspection
--file + --sample 5                 ✓ Sample rows
--search + --where + --limit        ✓ Filtered search with limit
--output + --output-format          ✓ Save to file in format
--count + --where                   ✓ Count filtered results
```

### Invalid Combinations (Errors)

```
--count + --show-count              ✗ Use one or the other
--output (no file specified)        ✗ Output where?
--limit 0                           ✗ Ignored, use unlimited
```

## Quick Reference Table

| Task | Command |
|------|---------|
| Show schema | `datagrep file.csv --describe` |
| Basic search | `datagrep file.csv column value` |
| Case-insensitive | `--ignore-case` |
| Limit results | `--limit 10` |
| Filter before search | `--where "col > val"` |
| Count results | `--count` |
| JSON output | `--output-format json` |
| Table output | `--output-format table` |
| Save to file | `--output results.csv` |
| Sort results | `--sort name:asc` |
| Select columns | `--select name,email` |
| Show empty cells | `--empty` |
| Regex search | `--mode regex` |
| Exact match | `--mode exact` |

For more help: `datagrep --help` or see [USAGE.md](USAGE.md)
