# Usage Guide

Comprehensive guide to using datagrep-cli with real-world examples.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Command Structure](#command-structure)
3. [Search Modes](#search-modes)
4. [Filtering with WHERE](#filtering-with-where)
5. [Output Formats](#output-formats)
6. [Inspection Modes](#inspection-modes)
7. [Real-World Examples](#real-world-examples)
8. [Advanced Techniques](#advanced-techniques)
9. [Performance Tips](#performance-tips)

## Quick Start

### 1. Show File Schema

```bash
datagrep customers.csv --describe
```

Output:
```
Schema:
  - customer_id
  - first_name
  - last_name
  - email
  - phone_number
  - status
```

### 2. Basic Search

```bash
datagrep customers.csv first_name John
```

Finds all customers with "John" in their first name.

### 3. Search Multiple Columns

```bash
datagrep customers.csv "first_name,last_name,email" John
```

Searches all three columns for "John".

### 4. Search with Options

```bash
datagrep customers.csv email gmail --mode contains --ignore-case --limit 10
```

## Command Structure

### Positional Style

```
datagrep <file> <columns> <value> [options]
```

Examples:
```bash
datagrep data.csv name john
datagrep data.csv "name,email" alice --limit 5
datagrep data.json product iphone --output-format json
```

### Flag Style

```
datagrep [options] --file <file> --columns <columns> --search <value>
```

Examples:
```bash
datagrep --file data.csv --columns name --search john
datagrep --file data.csv --columns "name,email" --search alice --limit 5
datagrep --file data.json --columns product --search iphone --output-format json
```

### Arguments Explained

| Argument | Purpose | Example |
|----------|---------|---------|
| `input_file` | File to search (CSV/JSON/Excel) or `-` for stdin | `data.csv` or `-` |
| `columns` | Columns to search (comma-separated) | `name` or `name,email` |
| `value` | What you're searching for | `john` or `john.*` |

## Search Modes

### Contains (Default)

Matches any substring (case-sensitive):

```bash
# Find rows where 'email' contains 'gmail'
datagrep users.csv email gmail

# Both "john@gmail.com" and "gmail@gmail.com" match
```

### Exact Match

Whole field value only:

```bash
# Find exact status = "active"
datagrep users.csv status active --mode exact

# Won't match "active_user" or anything else
```

### Starts With

Prefix matching:

```bash
# Find emails starting with "john"
datagrep users.csv email "john" --mode startswith

# Matches: john@gmail.com, john.doe@example.com
# But not: nojohn@gmail.com
```

### Ends With

Suffix matching:

```bash
# Find emails ending with @gmail.com
datagrep users.csv email "@gmail.com" --mode endswith

# Matches: john@gmail.com, alice@gmail.com
# But not: john@gmail.com.uk
```

### Regex (Regular Expressions)

Pattern matching:

```bash
# Find valid email addresses
datagrep users.csv email "^[a-z]+@[a-z]+\.[a-z]+$" --mode regex

# Find phone starting with 555 (3 digits total)
datagrep users.csv phone "^555-" --mode regex

# Find all numbers
datagrep data.csv value "^[0-9]+$" --mode regex
```

### Case-Insensitive

Works with any search mode:

```bash
# Find 'john' regardless of case
datagrep users.csv name john --ignore-case

# Matches: John, JOHN, john, jOhN

# Works with all modes
datagrep users.csv name john --mode exact --ignore-case
datagrep users.csv email "@GMAIL.COM" --mode endswith --ignore-case
```

## Filtering with WHERE

Pre-filter records before searching using WHERE conditions:

### Simple Comparisons

```bash
# Greater than
datagrep sales.csv product laptop --where "price > 500"

# Less than
datagrep sales.csv product laptop --where "quantity < 10"

# Equal to
datagrep sales.csv city london --where "population == 9000000"

# Not equal to
datagrep sales.csv product laptop --where "status != discontinued"

# Greater than or equal
datagrep sales.csv employee bob --where "salary >= 60000"

# Less than or equal
datagrep sales.csv order item --where "amount <= 100"
```

### String Operations

```bash
# String contains
datagrep products.csv category --where "description contains wireless"

# String starts with
datagrep users.csv email --where "domain startswith gmail"

# String ends with
datagrep logs.csv message --where "level endswith ERROR"
```

### Combining Conditions (AND)

```bash
# All conditions must be true
datagrep users.csv active --where "age > 25 and city == London and salary >= 50000"

# Multi-line for clarity
datagrep sales.csv product --where "price > 100 and stock > 0 and status == active"
```

### Combining Conditions (OR)

```bash
# At least one condition must be true
datagrep cities.csv population --where "country == USA or country == UK or country == Canada"

# Multiple cities
datagrep users.csv city --where "city == London or city == New York or city == Tokyo"
```

### Complex WHERE Expressions

```bash
# Mix AND and OR
datagrep products.csv product --where "category == Electronics and (brand == Apple or brand == Samsung) and price < 1000"

# Note: AND has priority over OR, use proper logic
datagrep sales.csv item --where "status == shipped and (payment_method == credit_card or payment_method == paypal)"
```

## Output Formats

### CSV (Default)

```bash
datagrep users.csv name john
# or explicit
datagrep users.csv name john --output-format csv
```

Output:
```
id,name,email,status
1,John Smith,john@example.com,active
2,John Doe,john.doe@example.com,inactive
```

### JSON

```bash
datagrep users.csv name john --output-format json
```

Output:
```json
[
  {
    "id": "1",
    "name": "John Smith",
    "email": "john@example.com",
    "status": "active"
  },
  {
    "id": "2",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "status": "inactive"
  }
]
```

### Table

```bash
datagrep users.csv name john --output-format table
```

Output:
```
id | name        | email                 | status
---|-------------|------------------------|--------
1  | John Smith  | john@example.com      | active
2  | John Doe    | john.doe@example.com  | inactive
```

### Raw Dictionary

```bash
datagrep users.csv name john --output-format raw
```

Output:
```
{'id': '1', 'name': 'John Smith', 'email': 'john@example.com', 'status': 'active'}
{'id': '2', 'name': 'John Doe', 'email': 'john.doe@example.com', 'status': 'inactive'}
```

## Inspection Modes

Examine your data without searching.

### Describe (Schema)

```bash
datagrep data.csv --describe
```

Shows column names and first 10 sample rows.

### Sample Rows

```bash
# Show first 5 rows
datagrep data.csv --sample 5

# Show first 20 rows
datagrep data.csv --sample 20
```

### Preview

```bash
# Show first 5 matching results
datagrep data.csv name john --preview 5
```

### Count

```bash
# Count total matches
datagrep data.csv name john --count

# With WHERE filter
datagrep data.csv status active --where "salary > 50000" --count
```

### Show Count

```bash
# Display count before showing results
datagrep data.csv name john --show-count
```

Output:
```
Count: 47
id,name,email,status
...
```

## Real-World Examples

### Example 1: Customer Search

```bash
# Find all active customers
datagrep customers.csv status active

# Active customers with high purchases
datagrep customers.csv status active --where "total_purchases > 5000"

# Top 10 active customers by purchases
datagrep customers.csv status active --sort total_purchases:desc --limit 10

# Export to JSON
datagrep customers.csv status active --output-format json --output active_customers.json
```

### Example 2: Product Inventory

```bash
# Find products by category
datagrep products.csv category Electronics

# Out-of-stock items
datagrep products.csv stock 0 --mode exact --where "category == Electronics"

# Products: name and price, sorted by price
datagrep products.csv category Electronics --select name,price --sort price:asc

# Table format with colors (if colorama installed)
datagrep products.csv category Electronics --output-format table --color
```

### Example 3: Log Analysis

```bash
# Find error messages
datagrep app.log level ERROR

# Recent errors (last modified logs first)
datagrep app.log level ERROR --sort timestamp:desc --limit 100

# Specific error pattern
datagrep app.log message "database connection" --mode contains

# Count errors per service
datagrep app.log level ERROR --where "service == api" --count
```

### Example 4: Email Search

```bash
# Find Gmail users
datagrep users.csv email "@gmail.com" --mode endswith

# Case-insensitive email search
datagrep users.csv email "john" --ignore-case

# Email validation
datagrep users.csv email "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" --mode regex

# Corporate email addresses
datagrep users.csv email "@company.com" --mode endswith --count
```

### Example 5: Sales Data

```bash
# Find orders over $1000
datagrep orders.csv amount 1000 --where "amount > 1000"

# Recent orders (sorted by date)
datagrep orders.csv status completed --sort date:desc --limit 50

# Orders by customer with JSON output
datagrep orders.csv customer_id C001 --output-format json --output customer_orders.json

# High-value completed orders
datagrep orders.csv status completed --where "total > 5000" --output-format table
```

### Example 6: Data Validation

```bash
# Find invalid phone numbers (not exactly 10 digits)
datagrep data.csv phone "^[0-9]{10}$" --mode regex --not-empty

# Find records with missing email
datagrep users.csv email --empty

# Find non-standard statuses (should be active/inactive)
datagrep users.csv status "[^(active|inactive)]" --mode regex
```

### Example 7: Unicode/International Data

```bash
# Search in Arabic text
datagrep customers.csv name محمد

# Search in Chinese text
datagrep products.csv name 中文

# Case-insensitive search
datagrep users.csv city Paris --ignore-case
```

### Example 8: Pipeline with Other Commands

```bash
# Use with cat
cat huge_file.csv | datagrep - status active | head -20

# Combine with grep
datagrep users.csv status active | grep "john"

# Chain with other commands
datagrep users.csv status active --output-format json | jq '.[] | .email'

# Count results using wc
datagrep users.csv status active | wc -l
```

### Example 9: Working with stdin

```bash
# From pipe
echo -e "name,age\nJohn,30\nAlice,25" | datagrep - name John

# From redirection
datagrep - status active < data.csv

# From command substitution
datagrep <(cat data.csv) name john
```

### Example 10: Batch Processing

```bash
# Process multiple files
for file in data_*.csv; do
    echo "=== $file ==="
    datagrep "$file" status active --count
done

# Export all matches to separate files
datagrep customers.csv status active --output active.json --output-format json
datagrep customers.csv status inactive --output inactive.json --output-format json
```

## Advanced Techniques

### Sorting Results

```bash
# Sort before searching (limited records)
datagrep data.csv city london --sort name:asc

# Sort descending
datagrep data.csv city london --sort population:desc

# Multiple column preference (first sort, then search)
datagrep data.csv status active --sort salary:desc --limit 20
```

### Selecting Specific Columns

```bash
# Include only certain columns in output
datagrep customers.csv status active --select name,email,phone

# Works with all output formats
datagrep customers.csv status active --select name,email --output-format json
datagrep customers.csv status active --select name,email --output-format table
```

### Combining Multiple Filters

```bash
# WHERE + EMPTY + SORT
datagrep data.csv status active --where "age > 25" --not-empty --sort age:desc

# WHERE + LIMIT + SELECT
datagrep data.csv department HR --where "salary > 60000" --limit 10 --select name,salary,email

# All together
datagrep users.csv status active \
  --where "age > 20 and city == London" \
  --sort salary:desc \
  --limit 5 \
  --select name,email,salary \
  --output-format json \
  --output top_earners.json
```

### Working with Large Files

```bash
# Show progress and limit results
datagrep huge_file.csv status active --progress --limit 1000

# Use in background
nohup datagrep 1gb_file.csv status active --output results.json --output-format json &

# Check a sample before full search
datagrep 1gb_file.csv --sample 100
```

### Configuration Files

```bash
# Create reusable config
cat > search_config.json << EOF
{
  "input_file": "customers.csv",
  "columns": "status",
  "search_value": "active",
  "output_format": "json",
  "where": "salary > 50000",
  "limit": 100,
  "ignore_case": false
}
EOF

# Use config
datagrep --config search_config.json
```

### Error Handling

```bash
# Check exit code
datagrep data.csv name john
echo $?  # 0 = success, 1 = error

# Suppress stderr
datagrep nonexistent.csv name john 2>/dev/null

# Capture error
ERROR=$(datagrep data.csv name john 2>&1 | grep "Error:")
if [ -n "$ERROR" ]; then echo "Search failed"; fi
```

## Performance Tips

### For Large Files

1. **Limit results early:**
   ```bash
   datagrep huge.csv status active --limit 1000
   ```

2. **Use WHERE filters to reduce dataset:**
   ```bash
   datagrep huge.csv status active --where "date > 2024-01-01" --limit 1000
   ```

3. **Search specific columns only:**
   Instead of default all, specify columns:
   ```bash
   datagrep huge.csv email,phone "john"  # Only 2 columns
   ```

4. **Use exact mode for known values:**
   ```bash
   datagrep huge.csv status "active" --mode exact  # Faster than contains
   ```

5. **Save output incrementally:**
   ```bash
   datagrep huge.csv status active --output results.csv
   # Better than piping through other commands
   ```

### For Complex Searches

```bash
# 1. First, validate your data
datagrep data.csv --describe

# 2. Test on a sample
datagrep data.csv --sample 100 | grep pattern

# 3. Run the full search with limits
datagrep data.csv pattern --limit 1000

# 4. Then process larger batches
datagrep data.csv pattern --limit 10000
```

## Troubleshooting

### No Results Found

```bash
# Check if column name is correct
datagrep data.csv --describe

# Check if search value matches
datagrep data.csv name john --ignore-case  # Try case-insensitive

# Check encoding
datagrep data.csv name john --encoding utf-8
```

### Performance Issues

```bash
# Check file size
ls -lh large_file.csv

# Limit results to speed up
datagrep large_file.csv status active --limit 100

# Use specific columns instead of all
datagrep large_file.csv status,email "active"
```

### Character Encoding

```bash
# Specify encoding if UTF-8 doesn't work
datagrep data.csv name john --encoding latin-1

# Common encodings: utf-8, latin-1, iso-8859-1, cp1252
```

For more help, see [FAQ.md](FAQ.md) or check the [GitHub issues](https://github.com/yourusername/datagrep-cli/issues).
