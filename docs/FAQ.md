# Frequently Asked Questions (FAQ)

Common questions and answers about datagrep-cli.

## Installation & Setup

### Q: How do I install datagrep?

**A:** 
```bash
# From PyPI (when published)
pip install datagrep-cli

# From source
git clone https://github.com/yourusername/datagrep-cli.git
cd datagrep-cli
pip install -e .
```

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

### Q: What Python versions are supported?

**A:** Python 3.7 or higher.

Check your version:
```bash
python --version
```

If you need Python 3.7, install from [python.org](https://www.python.org/downloads/).

### Q: How do I install optional features (colors, progress bars, Excel)?

**A:**
```bash
# Individual features
pip install datagrep-cli[color]
pip install datagrep-cli[progress]
pip install datagrep-cli[excel]

# All features
pip install datagrep-cli[color,progress,excel]
```

### Q: Where does datagrep get installed?

**A:** On your PATH, typically:
- **Linux/macOS:** `~/.local/bin/datagrep`
- **Windows:** `C:\Users\YourName\AppData\Local\Python\pythoncore-3.x-64\Scripts\datagrep.exe`
- **Anaconda:** `~/anaconda3/bin/datagrep`

## Basic Usage

### Q: How do I search a CSV file?

**A:**
```bash
# Show schema first
datagrep data.csv --describe

# Then search
datagrep data.csv name john
```

### Q: How do I search multiple columns?

**A:**
```bash
datagrep data.csv "name,email,phone" john
```

The tool will find "john" in any of these three columns.

### Q: Why is my search not finding anything?

**A:** 
1. **Check column names** - are they spelled correctly and capitalized?
   ```bash
   datagrep data.csv --describe  # See exact column names
   ```

2. **Check file encoding** - if data looks garbled:
   ```bash
   datagrep data.csv name john --encoding latin-1  # Try different encoding
   ```

3. **Check search term** - is the value present in the data?
   ```bash
   # Try case-insensitive
   datagrep data.csv name john --ignore-case
   ```

4. **Check file exists** - is the file path correct?
   ```bash
   ls data.csv  # Verify file exists
   ```

### Q: How do I search case-insensitively?

**A:**
```bash
datagrep data.csv name john --ignore-case
```

This will match: John, JOHN, john, jOhN, etc.

### Q: How do I search using regular expressions?

**A:**
```bash
# Email pattern
datagrep data.csv email "^[a-z]+@gmail\.com$" --mode regex

# Phone number pattern (XXX-XXX-XXXX)
datagrep data.csv phone "^[0-9]{3}-[0-9]{3}-[0-9]{4}$" --mode regex

# Any digits
datagrep data.csv zip "^[0-9]+$" --mode regex
```

## Filtering & Output

### Q: How do I filter results using WHERE?

**A:**
```bash
# Simple comparison
datagrep data.csv status active --where "age > 25"

# String operation
datagrep data.csv product phone --where "description contains wireless"

# Multiple conditions
datagrep data.csv status active --where "age > 25 and salary >= 50000"
```

### Q: How do I limit results?

**A:**
```bash
# Show only first 10 matches
datagrep data.csv status active --limit 10

# First 100 matches
datagrep data.csv status active --limit 100
```

Using `--limit` also speeds up large file searches by stopping early.

### Q: How do I save results to a file?

**A:**
```bash
# Save as CSV (default)
datagrep data.csv name john --output results.csv

# Save as JSON
datagrep data.csv name john --output-format json --output results.json

# Save as table
datagrep data.csv name john --output-format table --output results.txt
```

### Q: How do I get only specific columns in output?

**A:**
```bash
# Show only name and email
datagrep data.csv status active --select name,email

# With JSON output
datagrep data.csv status active --select name,email --output-format json
```

### Q: How do I count results without seeing them?

**A:**
```bash
datagrep data.csv status active --count

# Output: Just a number (47)
```

### Q: How do I count and see the results?

**A:**
```bash
datagrep data.csv status active --show-count

# Output:
# Count: 47
# (then the 47 records)
```

## File Formats

### Q: What file formats does datagrep support?

**A:** 
- **CSV** (default) - comma, tab, or custom separator
- **JSON** - arrays and newline-delimited JSON
- **Excel** - XLSX files (requires `pip install datagrep-cli[excel]`)
- **stdin** - pipe any text format

### Q: How do I specify file format?

**A:**
```bash
# Auto-detect (default)
datagrep data.csv name john
datagrep data.json name john
datagrep data.xlsx name john

# Explicit format
datagrep data.txt name john --input-format csv
datagrep data data name john --input-format json
```

### Q: How do I handle CSV files with custom delimiters?

**A:**
```bash
# Tab-separated values
datagrep data.tsv name john --delimiter $'\t'

# Semicolon-separated
datagrep data.csv name john --delimiter ';'

# Pipe-separated
datagrep data.txt name john --delimiter '|'
```

### Q: How do I specify file encoding?

**A:**
```bash
# UTF-8 (default)
datagrep data.csv name john

# Latin-1 (Western European)
datagrep data.csv name john --encoding latin-1

# Windows encoding
datagrep data.csv name john --encoding cp1252

# Chinese
datagrep data.csv name john --encoding gbk
```

Common encodings: `utf-8`, `latin-1`, `iso-8859-1`, `cp1252`, `gbk`, `shift_jis`

### Q: How do I search Excel files?

**A:**
```bash
# First, install Excel support
pip install datagrep-cli[excel]

# Then search
datagrep data.xlsx product iphone
```

## Advanced Features

### Q: How do I use stdin (pipe data)?

**A:**
```bash
# From pipe
cat data.csv | datagrep - name john

# From redirection
datagrep - name john < data.csv

# From command
grep active data.csv | datagrep - name john
```

### Q: How do I sort results?

**A:**
```bash
# Ascending (A-Z, 0-9)
datagrep data.csv status active --sort name:asc

# Descending (Z-A, 9-0)
datagrep data.csv status active --sort salary:desc
```

### Q: How do I find empty values?

**A:**
```bash
# Show records where email is empty
datagrep data.csv email --empty

# Show records where phone is not empty
datagrep data.csv phone --not-empty
```

### Q: How do I view file schema without searching?

**A:**
```bash
# Show column names and first 10 rows
datagrep data.csv --describe

# Show first N rows
datagrep data.csv --sample 20
```

### Q: How do I get colored output?

**A:**
```bash
# Install color support
pip install datagrep-cli[color]

# Then use color flag
datagrep data.csv status active --output-format table --color
```

## Output Formats

### Q: Which output formats are available?

**A:**
- **CSV** (default) - for files, further processing
- **JSON** - for APIs, data exchange
- **Table** - for console viewing
- **Raw** - Python dictionary format

### Q: How do I output as JSON?

**A:**
```bash
datagrep data.csv name john --output-format json
```

Output:
```json
[
  {"id": "1", "name": "John", "email": "john@example.com"},
  {"id": "2", "name": "John", "email": "john2@example.com"}
]
```

### Q: How do I output as a formatted table?

**A:**
```bash
datagrep data.csv name john --output-format table
```

Output:
```
id | name | email
---|------|-------------------
1  | John | john@example.com
2  | John | john2@example.com
```

## Performance & Large Files

### Q: How large can files be?

**A:** Currently optimized for files up to **1GB**.
- **< 100 MB**: Fast (seconds)
- **100 MB - 1 GB**: Moderate (seconds to minutes)
- **> 1 GB**: Slow, may use lots of memory

See [PERFORMANCE.md](PERFORMANCE.md) for optimization strategies.

### Q: How do I speed up searches?

**A:**
1. **Use `--limit`** - stops after finding N matches
   ```bash
   datagrep huge.csv status active --limit 1000
   ```

2. **Use `--where`** - pre-filter before searching
   ```bash
   datagrep huge.csv status active --where "salary > 50000"
   ```

3. **Search specific columns** - not all columns
   ```bash
   datagrep huge.csv email,name "john"  # Not all columns
   ```

4. **Use exact mode** - faster than substring
   ```bash
   datagrep huge.csv status "active" --mode exact
   ```

### Q: How do I handle very large files (> 1 GB)?

**A:** 
For now:
1. Split file into chunks
2. Process each chunk
3. Combine results

Future optimization planned for Phase 2.

### Q: Do I need to load the entire file into memory?

**A:** Currently yes, the design loads all data at once. This is:
- **Pro:** Simple, safe file I/O, fast searches
- **Con:** Uses memory proportional to file size

Phase 2 will add lazy loading for streaming large files.

## Troubleshooting

### Q: I get "command not found: datagrep"

**A:** The command is not on your PATH. Solutions:

1. **Reinstall:**
   ```bash
   pip install --force-reinstall datagrep-cli
   ```

2. **Use full path:**
   ```bash
   python -m datagrep data.csv name john
   ```

3. **Add to PATH manually** (if needed):
   - Find where pip installed it: `pip show datagrep-cli`
   - Add that directory to your PATH environment variable

### Q: I get "ModuleNotFoundError"

**A:** The package isn't installed correctly:

```bash
# Reinstall
pip uninstall datagrep-cli
pip cache purge
pip install datagrep-cli
```

### Q: My search results look corrupted

**A:** Likely an encoding issue:

```bash
# Try different encoding
datagrep data.csv name john --encoding latin-1
# or
datagrep data.csv name john --encoding cp1252
# or
datagrep data.csv name john --encoding gbk
```

### Q: Progress bar isn't showing

**A:** Install tqdm:
```bash
pip install datagrep-cli[progress]
```

Then use:
```bash
datagrep data.csv name john --progress
```

### Q: Colors aren't working

**A:** Install colorama:
```bash
pip install datagrep-cli[color]
```

Then use:
```bash
datagrep data.csv name john --output-format table --color
```

### Q: Excel files aren't working

**A:** Install openpyxl:
```bash
pip install datagrep-cli[excel]
```

Then:
```bash
datagrep data.xlsx name john
```

### Q: Exit code is 1 but there's no error message

**A:** Check stderr separately:
```bash
datagrep data.csv name john 2>&1 | cat  # Show full output
```

### Q: Search is very slow for large files

**A:** Try optimizations:
```bash
# Limit results
--limit 1000

# Pre-filter
--where "date > 2024-01-01"

# Exact search
--mode exact

# Specific columns
datagrep data.csv "email,name" "john"  # Not all
```

## Contributing

### Q: How do I contribute?

**A:** See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code style guide
- Testing requirements
- Pull request process
- Issue reporting

### Q: Where do I report bugs?

**A:** GitHub Issues:
- Go to https://github.com/yourusername/datagrep-cli/issues
- Click "New Issue"
- Include: Python version, command used, full error message

### Q: How do I request a feature?

**A:** GitHub Issues with label `enhancement`:
- Describe what you want
- Explain why it would be useful
- Include example usage

## Contact & Support

### Q: How do I get help?

**A:** In order of usefulness:
1. **This FAQ** - most common questions
2. **[USAGE.md](USAGE.md)** - detailed usage examples
3. **[OPTIONS.md](OPTIONS.md)** - all flags and options
4. **`datagrep --help`** - command-line help
5. **GitHub Issues** - for bugs or feature requests

### Q: Can I use datagrep in my application/script?

**A:** datagrep-cli is primarily a command-line tool. For Python integration:

```python
# Import and use modules directly
from src.core import DataLoader, SearchEngine, OutputFormatter
from src.utils import build_matcher

# Or
import subprocess
result = subprocess.run(['datagrep', 'data.csv', 'name', 'john'], 
                       capture_output=True, text=True)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for module documentation.

### Q: Is there an API?

**A:** Not yet. datagrep-cli is designed as a command-line tool.  
Integration APIs may be added in a future version.

For now, use the Python modules directly or pipe the command:
```bash
datagrep data.csv name john --output-format json | your-script.py
```

---

Can't find your answer? [Create an issue](https://github.com/yourusername/datagrep-cli/issues) or check the [main README](../README.md).
