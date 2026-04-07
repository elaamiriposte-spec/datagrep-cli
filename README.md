```
     _       _                                        _ _ 
  __| | __ _| |_ __ _  __ _ _ __ ___ _ __         ___| (_)
 / _` |/ _` | __/ _` |/ _` | '__/ _ \ '_ \ _____ / __| | |
| (_| | (_| | || (_| | (_| | | |  __/ |_) |_____| (__| | |
 \__,_|\__,_|\__\__,_|\__, |_|  \___| .__/       \___|_|_|
                      |___/         |_|                   
```

# datagrep-cli

A powerful Python utility to search and filter CSV, JSON, or Excel records by field values with flexible matching modes, sorting, and output formats.

## Features

- Search CSV, JSON, or Excel files
- Multiple search modes: substring, exact, startswith, endswith, regex
- Case-insensitive search
- UTF-8 support for Arabic and other Unicode content
- Pre-filter with `--where` conditions
- Sort results before searching
- Select specific output columns
- Output as CSV, JSON, table, or raw dictionaries
- Count-only mode
- Progress bars for large files
- Colored output
- Configuration files
- Read from file or stdin
- Automatic format detection

## Usage

```bash
python search_csv.py [input_file] [columns] [value] [options]
```

If no `columns` and `value` are provided, the tool displays the file schema and a sample of the first 10 rows.

### Examples

#### Show schema and sample (no search)

```bash
python search_csv.py arabic_sample.csv
```

This displays field names with samples and the first 10 rows.

#### Describe file schema

```bash
python search_csv.py arabic_sample.csv --describe
```

#### Count total records

```bash
python search_csv.py arabic_sample.csv --count
```

#### Show sample rows

```bash
python search_csv.py arabic_sample.csv --sample 5
```

#### Preview first rows

```bash
python search_csv.py arabic_sample.csv --preview 3
```

#### Search multiple columns

```bash
python search_csv.py arabic_sample.csv name,city دبي
```

#### Exact match with case-insensitive

```bash
python search_csv.py arabic_sample.csv name فاطمة --mode exact --ignore-case
```

#### Regex search

```bash
python search_csv.py arabic_sample.csv name "^أ" --mode regex
```

#### Filter and sort before searching

```bash
python search_csv.py english_sample.json name Alice --where "age > 25" --sort name:asc
```

#### Count matches only

```bash
python search_csv.py arabic_sample.csv city دبي --count
```

#### Select output columns

```bash
python search_csv.py arabic_sample.csv name دبي --select name,city
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
