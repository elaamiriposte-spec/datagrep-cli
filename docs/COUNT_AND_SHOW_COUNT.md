# --count and --show-count Features Documentation

## Overview

The `--count` and `--show-count` flags have been enhanced to work with all types of filters and searches, providing flexible ways to count and display matching records.

## Features

### 1. `--count` Flag

Shows ONLY the count of matching records without displaying the data itself.

#### Usage Patterns

**With search value:**
```bash
# Count all records containing 'active' in status column
python src/datagrep.py data.csv status "active" --count
# Output: 939

# Count records matching search with specific mode
python src/datagrep.py data.csv email "example" --mode startswith --count
```

**With filters (no search value):**
```bash
# Count all active records using WHERE condition
python src/datagrep.py data.csv --where "status == active" --count
# Output: 460

# Count records matching multiple conditions
python src/datagrep.py data.csv --where "status == active and city == London" --count

# Count sorted records (returns count at the sort position limit)
python src/datagrep.py data.csv --sort registration_date:desc --count
```

**With --empty/--not-empty filters:**
```bash
# Count records with empty phone number
python src/datagrep.py data.csv phone_number --empty --count
# Output: 85

# Count records with non-empty email
python src/datagrep.py data.csv email --not-empty --count
# Output: 950
```

### 2. `--show-count` Flag

Shows the count of matching records FOLLOWED BY the matching data itself. Provides both summary and detail information.

#### Usage Patterns

**With WHERE filter:**
```bash
# Show count and filtered data in table format
python src/datagrep.py data.csv --where "status == active" --show-count

# Output:
# Count: 460
# [table with 460 active records]
```

**With CSV output:**
```bash
python src/datagrep.py data.csv --where "status == inactive" --show-count --output-format csv
# Output:
# Count: 540
# [CSV data with 540 inactive records]
```

**With JSON output (includes count as property):**
```bash
python src/datagrep.py data.csv --where "city == London" --show-count --output-format json
# Output (JSON):
# {
#   "count": 24,
#   "data": [
#     { "name": "Jane Doe", ... },
#     ...
#   ]
# }
```

**With search + filter combination:**
```bash
# Search for 'john' in name column AND filtered by active status
python src/datagrep.py data.csv name "john" --where "status == active" --show-count
# Shows count of records where name contains 'john' AND status == active
```

### 3. Combining with Other Flags

Both flags work seamlessly with other options:

```bash
# Count with limit
python src/datagrep.py data.csv status "active" --count --limit 100

# Count with selected columns (show-count)
python src/datagrep.py data.csv --where "status == active" --show-count --select "name,email,status"

# Count with sorting
python src/datagrep.py data.csv --where "status == active" --show-count --sort "total_purchases:desc"

# Count with case-insensitive search
python src/datagrep.py data.csv status "ACTIVE" --ignore-case --count

# Count with regex mode
python src/datagrep.py data.csv email ".*@gmail\\.com" --mode regex --count
```

## Usage Examples

### Example 1: Filter and Count

Count how many customers have active status:
```bash
$ python src/datagrep.py examples/data/sample_customers.csv --where "status == active" --count
460
```

### Example 2: Show Count and Data

Show count and displayed filtered customers with specific columns:
```bash
$ python src/datagrep.py examples/data/sample_customers.csv --where "status == active" --show-count --select "customer_id,first_name,last_name,status"

Count: 460
customer_id | first_name  | last_name | status
...
```

### Example 3: JSON Output with Count

Get filtered data as JSON with count property:
```bash
$ python src/datagrep.py examples/data/sample_customers.csv --where "city == London" --show-count --output-format json

{
  "count": 24,
  "data": [
    {
      "customer_id": "6",
      "first_name": "Jane",
      "city": "London",
      ...
    },
    ...
  ]
}
```

### Example 4: Complex Filtering

Count records matching complex conditions:
```bash
# Count active customers in London with more than 5000 purchases
$ python src/datagrep.py examples/data/sample_customers.csv --where "status == active and city == London and total_purchases > 5000" --count
```

Note: The third condition `total_purchases > 5000` won't work directly in WHERE clause. Instead, use:
```bash
# Search for active status combined with WHERE filtering
$ python src/datagrep.py examples/data/sample_customers.csv status active --where "city == London" --count
```

## Restrictions and Limitations

1. **Mutually Exclusive**: `--count` and `--show-count` cannot be used together
   ```bash
   # ERROR: Cannot use both
   python src/datagrep.py data.csv status "active" --count --show-count
   ```

2. **Incompatible with Inspection Modes**: Cannot combine with `--describe`, `--sample`, or `--preview`
   ```bash
   # ERROR: Cannot combine
   python src/datagrep.py data.csv --count --describe
   ```

3. **Default Precision**: Filters may not perfectly match complex conditions. Use search + filter combination for best results.

## Implementation Details

### Filter Application Order

When using `--count` or `--show-count` with multiple filtering options:

1. WHERE condition filter applied first (if provided)
2. Sort applied (if provided)
3. Limit applied (if --limit specified)
4. Count calculated
5. Data output (for --show-count)

### JSON Output Format

When using `--show-count` with `--output-format json`:
```json
{
  "count": <number of records>,
  "data": [<array of record objects>]
}
```

For regular use (without `--show-count`):
```json
[<array of record objects>]
```

### Performance Considerations

- `--count` requires eager loading (all records in memory) to ensure accurate counts
- Large files may cause significant memory usage
- For very large files, consider using `--where` with `--limit` to reduce data volume

## Backward Compatibility

All changes are 100% backward compatible:
- Existing `--count` usage with search values continues to work
- Existing `--show-count` (if previously used) continues to work
- All other flags and behaviors unchanged

## Testing

All functionality is covered by unit tests in `tests/tests.py`:
- `test_search_filter_requires_value` - Validates --count with filters
- WHERE condition tests
- Integration tests for complex scenarios

Run tests:
```bash
python -m unittest tests.tests -v
```

## Migration from Previous Behavior

Previously, `--count` only worked with search values (counts matching search results).

Now, `--count` also works with:
- `--where` filters
- `--sort` operations  
- `--empty`/`--not-empty` filters
- Combinations of the above

Example migration:
```bash
# Old usage (still works)
python src/datagrep.py data.csv status "active" --count

# New usage (also works)
python src/datagrep.py data.csv --where "status == active" --count
```

## Related Commands

- `--where` - Filter records by condition
- `--sort` - Sort records before counting  
- `--limit` - Limit count to first N records
- `--select` - Choose columns for output
- `--output-format` - Control output format (csv, json, table, raw)
- `--describe` - Show schema and sample (incompatible with --count)

## Future Enhancements

Potential future improvements:
- Streaming count for very large files (without loading all to memory)
- Count summary by group (e.g., count by status)
- Pagination support with count information
- Conditional counting (count records matching multiple independent conditions)
