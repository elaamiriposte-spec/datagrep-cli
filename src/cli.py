"""CLI - Command-line interface for datagrep."""

import argparse
import logging
import re
import sys
from typing import Any, Callable, Dict, List, Union

from .core import DataLoader, OutputFormatter, SearchEngine
from .utils import DataGrepError, format_table, load_config, parse_where_condition

__version__ = "1.0.0"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Supports both styles:
    - Legacy positional: datagrep file.csv columns value
    - Modern flags: datagrep --file file.csv --columns columns --search value
    
    Returns:
        Namespace with parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog='datagrep',
        description='Search CSV, JSON, or Excel records by field values with flexible matching modes.',
        epilog='Use - for input_file to read from stdin. Inspection modes do not require search parameters. Supports both positional args (legacy) and explicit flags (modern).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True
    )
    
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}',
        help='Show version and exit.'
    )
    
    # Legacy positional arguments (optional, for backward compatibility)
    parser.add_argument('input_file', nargs='?', default=None, help='(Legacy positional) Input file path or - for stdin.')
    parser.add_argument('columns', nargs='?', default=None, help='(Legacy positional) Comma-separated field names to search.')
    parser.add_argument('value', nargs='?', default=None, help='(Legacy positional) Search value or pattern.')
    
    # Modern explicit flags (optional, take precedence over positional)
    parser.add_argument(
        '--file', '-f', dest='file_flag', default=None,
        help='Input file path or - for stdin (modern flag style).'
    )
    parser.add_argument(
        '--columns', dest='columns_flag', default=None,
        help='Comma-separated field names to search (modern flag style).'
    )
    parser.add_argument(
        '--search', '-S', dest='search_flag', default=None,
        help='Search value or pattern (modern flag style).'
    )
    
    parser.add_argument(
        '--input-format', choices=['auto', 'csv', 'json', 'xlsx'], default='auto',
        help='Input format: auto-detect (default), csv, json, or xlsx.'
    )
    parser.add_argument(
        '--mode', choices=['contains', 'exact', 'startswith', 'endswith', 'regex'],
        default='contains',
        help='Search mode: contains (default), exact, startswith, endswith, or regex.'
    )
    parser.add_argument(
        '--ignore-case', '-i', action='store_true', help='Ignore case while searching.'
    )
    parser.add_argument(
        '--delimiter', '-d', default=',', help='CSV delimiter for input/output (default: ,).'
    )
    parser.add_argument(
        '--encoding', default='utf-8', help='Input/output file encoding (default: utf-8).'
    )
    parser.add_argument(
        '--output-format', choices=['csv', 'json', 'table', 'raw'], default='csv',
        help='Output format: csv (default), json, table, or raw.'
    )
    parser.add_argument(
        '--select', '-s', default='*',
        help='Comma-separated fields to include in output (default: all).'
    )
    parser.add_argument(
        '--output', '-o', help='Write results to file instead of stdout.'
    )
    parser.add_argument(
        '--limit', '-n', type=int, default=0,
        help='Maximum matching rows to print (0=unlimited, default).'
    )
    parser.add_argument(
        '--sort', help='Sort by column: "name:asc" or "name:desc" before searching.'
    )
    parser.add_argument(
        '--where', help='Filter records with condition: "column op value" (or/and supported).'
    )
    parser.add_argument(
        '--empty', action='store_true', help='Show only rows where specified column is empty.'
    )
    parser.add_argument(
        '--not-empty', action='store_true', help='Show only rows where specified column has a value.'
    )
    parser.add_argument(
        '--count', action='store_true', help='Only count matching/filtered records (works with --where, --sort, --empty, --not-empty).'
    )
    parser.add_argument(
        '--show-count', action='store_true', help='Show count of matching/filtered records followed by the data.'
    )
    parser.add_argument(
        '--config', help='Load configuration from JSON file.'
    )
    parser.add_argument(
        '--color', action='store_true', help='Colorize output (requires colorama).'
    )
    parser.add_argument(
        '--progress', action='store_true', help='Show progress bar for large files (requires tqdm).'
    )
    parser.add_argument(
        '--preview', type=int, default=0, help='Show first N matching rows only (0=unlimited).'
    )
    parser.add_argument(
        '--sample', type=int, default=0, help='Show first N rows as sample (inspection mode).'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true', help='Enable verbose logging.'
    )
    parser.add_argument(
        '--debug', action='store_true', help='Enable debug logging.'
    )
    parser.add_argument(
        '--describe', action='store_true', help='Show file schema and sample data (inspection mode).'
    )
    
    args = parser.parse_args()
    return _reconcile_args(args)


def _reconcile_args(args: argparse.Namespace) -> argparse.Namespace:
    """Reconcile positional and flag-based arguments for backward compatibility.
    
    Priority: flags > positional arguments
    
    Args:
        args: Parsed arguments with both positional and flag versions.
        
    Returns:
        Reconciled arguments with consolidated values.
    """
    # Reconcile input_file / --file flag
    args.input_file = args.file_flag or args.input_file or '-'
    
    # Reconcile columns / --columns flag
    if args.columns_flag:
        args.columns = args.columns_flag
    
    # Reconcile value / --search flag
    if args.search_flag:
        args.value = args.search_flag
    
    # Remove flag attributes to avoid confusion
    delattr(args, 'file_flag')
    delattr(args, 'columns_flag')
    delattr(args, 'search_flag')
    
    return args


def validate_args(args: argparse.Namespace) -> argparse.Namespace:
    """Validate argument combinations and constraints.
    
    Args:
        args: Parsed arguments to validate.
        
    Returns:
        Validated arguments namespace.
        
    Raises:
        DataGrepError: When invalid argument combinations are detected.
    """
    # --count and --show-count are mutually exclusive
    if args.count and args.show_count:
        raise DataGrepError(
            'Error: Cannot use --count and --show-count together.\n'
            '  Choose one:\n'
            '    --count          (show only the count)\n'
            '    --show-count     (show count + data)'
        )
    
    # Inspection modes (--describe, --sample, --preview) - mutually exclusive
    inspection_modes: List[bool] = [args.describe, args.sample > 0, args.preview > 0]
    inspection_count: int = sum(inspection_modes)
    
    if inspection_count > 1:
        raise DataGrepError('Cannot combine --describe, --sample, and --preview. Use only one.')
    
    in_inspection_mode: bool = inspection_count > 0
    
    # --count cannot be combined with other inspection modes (--describe, --sample, --preview)
    if args.count and in_inspection_mode:
        raise DataGrepError('Cannot combine --count with --describe, --sample, or --preview.')
    
    # Inspection modes cannot be used with search value
    if in_inspection_mode and args.value is not None:
        raise DataGrepError('Inspection modes (--describe, --sample, --preview) cannot be used with search value.')
    
    # Validate --empty and --not-empty
    if args.empty and args.not_empty:
        raise DataGrepError(
            'Error: Cannot use --empty and --not-empty together.\n'
            '  Use only one filter at a time.\n'
            '  Examples:\n'
            '    datagrep file.csv phone --empty\n'
            '    datagrep file.csv email --not-empty'
        )
    
    if (args.empty or args.not_empty) and args.value is not None:
        raise DataGrepError(
            'Error: --empty and --not-empty filters do not take a search value.\n'
            '  These filters check if columns are empty/non-empty, not for specific values.\n'
            '  Incorrect: datagrep file.csv phone "123" --empty ❌\n'
            '  Correct:   datagrep file.csv phone --empty ✓'
        )
    
    if (args.empty or args.not_empty) and not args.columns:
        raise DataGrepError(
            'Error: --empty and --not-empty require a column name.\n'
            '  Specify which column to check.\n'
            '  Examples:\n'
            '    datagrep file.csv phone --empty\n'
            '    datagrep file.csv "email,phone" --empty'
        )
    
    if (args.empty or args.not_empty) and (args.where or args.sort):
        raise DataGrepError(
            'Error: Cannot combine --empty/--not-empty with --where or --sort.\n'
            '  These filters are mutually exclusive.\n'
            '  Choose one approach:\n'
            '    datagrep file.csv phone --empty\n'
            '    datagrep file.csv name john --where "age > 25"'
        )
    
    # Validate --where condition format if provided
    if args.where:
        try:
            # Try parsing the WHERE condition to catch format errors early
            parse_where_condition(args.where)
        except DataGrepError as e:
            raise DataGrepError(
                f'Error in --where condition: {str(e)}\n'
                '  Format: "column operator value"\n'
                '  Operators: ==, !=, >, <, >=, <=, contains, startswith, endswith\n'
                '  Logic: AND, OR\n'
                '  Examples:\n'
                '    --where "age > 25"\n'
                '    --where "status == active"\n'
                '    --where "status == active and age > 25"'
            )
    
    # Validate --sort format if provided
    if args.sort:
        if ':' not in args.sort:
            raise DataGrepError(
                'Error: Invalid --sort format.\n'
                '  Format: "column:asc" or "column:desc"\n'
                '  Examples:\n'
                '    --sort name:asc\n'
                '    --sort age:desc'
            )
        col, order = args.sort.split(':')
        if order.lower() not in ('asc', 'desc'):
            raise DataGrepError(
                f'Error: Invalid sort order "{order}".\n'
                '  Use "asc" (ascending) or "desc" (descending).\n'
                '  Examples:\n'
                '    --sort name:asc\n'
                '    --sort age:desc'
            )
    
    # Note: --count and --show-count work with:
    # - Search values (regular search)
    # - Filters (--where, --sort, --empty, --not-empty)
    # - But NOT with inspection modes (--describe, --sample, --preview)
    
    if args.value and not args.columns:
        args.columns = '*'
    
    return args


def main() -> None:
    """Main entry point for datagrep CLI."""
    args: argparse.Namespace = parse_args()
    args = validate_args(args)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    elif args.verbose:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING)

    # Load config if provided
    if args.config:
        config = load_config(args.config)
        for key, value in config.items():
            if hasattr(args, key):
                setattr(args, key, value)

    try:
        # Load data
        loader = DataLoader(args)
        loader.load()
        
        available_columns = loader.available_columns
        columns = loader.get_columns_from_string(args.columns) if args.columns else list(available_columns)
        selected_columns = loader.get_columns_from_string(args.select) if args.select else list(available_columns)

        # Handle inspection modes (no search value)
        if args.describe:
            print("Schema:")
            for col in available_columns:
                print(f"  - {col}")
            return
        
        if args.sample:
            records = loader.records if isinstance(loader.records, list) else list(loader.records)
            sample_rows = records[:args.sample]
            print(format_table(sample_rows, available_columns, args.color))
            return
        
        if args.preview and not args.value:
            records = loader.records if isinstance(loader.records, list) else list(loader.records)
            preview_rows = records[:args.preview]
            print(format_table(preview_rows, available_columns, args.color))
            return

        # Handle filters without search value
        if not args.value:
            if args.empty or args.not_empty or args.where or args.sort:
                engine = SearchEngine(loader.records, available_columns, args)
                filtered_records = engine.apply_filters()
                
                if args.count:
                    print(len(filtered_records) if isinstance(filtered_records, list) else sum(1 for _ in filtered_records))
                    return
                
                if not filtered_records:
                    print("No records match the filter.")
                    return
                
                # Ensure columns are valid
                if selected_columns == ['*']:
                    selected_columns = available_columns
                
                # Output results
                if isinstance(filtered_records, list):
                    formatter = OutputFormatter(args)
                    formatter.write_output(filtered_records, selected_columns, args.show_count)
                else:
                    filtered_records = list(filtered_records)
                    formatter = OutputFormatter(args)
                    formatter.write_output(filtered_records, selected_columns, args.show_count)
                return
            
            # Show schema and sample when no search value and no filters
            print("Schema:")
            for col in available_columns:
                print(f"  - {col}")
            print("\nSample rows (first 10):")
            records = loader.records if isinstance(loader.records, list) else list(loader.records)
            sample_rows = records[:10]
            if sample_rows:
                print(format_table(sample_rows, available_columns, args.color))
            return

        # Validate columns exist
        if columns == ['*']:
            columns = available_columns
        if selected_columns == ['*']:
            selected_columns = available_columns

        missing_search = [col for col in columns if col not in available_columns]
        if missing_search:
            raise ValueError(
                f"Error: Search column(s) not found: {', '.join(missing_search)}\n"
                f"  Available columns in this file: {', '.join(available_columns)}\n"
                f"  Check the column names are spelled correctly (case-sensitive).\n"
                f"  Use --describe to see all available columns."
            )

        missing_select = [col for col in selected_columns if col not in available_columns]
        if missing_select:
            raise ValueError(
                f"Error: --select column(s) not found: {', '.join(missing_select)}\n"
                f"  Available columns in this file: {', '.join(available_columns)}\n"
                f"  Check the column names are spelled correctly (case-sensitive).\n"
                f"  Use --describe to see all available columns."
            )

        # Search path (args.value is provided)
        engine = SearchEngine(loader.records, available_columns, args)
        
        # Apply pre-search filters
        if args.where or args.sort or args.empty or args.not_empty:
            engine.records = engine.apply_filters()
        
        # Perform search
        if args.count:
            # Count matches only
            from .utils import build_matcher
            matcher = build_matcher(args.value, args.mode, args.ignore_case)
            count = 0
            for row in engine.records:
                if any(matcher(str(row.get(col, ''))) for col in columns):
                    count += 1
                    if args.limit and count >= args.limit:
                        break
            print(count)
            logging.info("Found %d matching records", count)
            return
        
        # Search with output
        matches = engine.search(columns)
        
        if args.preview and matches:
            matches = matches[:args.preview]
            logging.info("Preview limited to first %d matches", args.preview)

        # Output results
        if not matches:
            print(
                f"No records found where any of {', '.join(columns)} {args.mode} '{args.value}'",
                file=sys.stderr
            )
            return
        
        formatter = OutputFormatter(args)
        formatter.write_output(matches, selected_columns, args.show_count)

    except FileNotFoundError:
        print(
            f"Error: File not found: '{args.input_file}'\n"
            f"  The file does not exist at that path.\n"
            f"  Check the path and file name (case-sensitive on Linux/Mac).\n"
            f"  Try using: pwd (to see current directory) and ls/dir (to list files)",
            file=sys.stderr
        )
        sys.exit(1)
    except UnicodeDecodeError:
        print(
            f"Error: Failed to decode '{args.input_file}' with encoding {args.encoding}.\n"
            f"  This file may be encoded differently (e.g., UTF-8 vs Latin-1).\n"
            f"  Try using a different encoding with: --encoding utf-8 or --encoding latin-1\n"
            f"  To detect encoding: file {args.input_file}",
            file=sys.stderr
        )
        sys.exit(1)
    except (ValueError, DataGrepError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except re.error as exc:
        print(
            f"Regex error: Invalid regular expression pattern\n"
            f"  Error details: {exc}\n"
            f"  Check your --search value for special regex characters or syntax errors.\n"
            f"  If using --mode regex, ensure the pattern is valid regex (not a simple string).\n"
            f"  Examples of valid regex patterns:\n"
            f"    --mode regex --search '^[A-Z]'          (starts with capital letter)\n"
            f"    --mode regex --search '[0-9]{{3}}-[0-9]{{4}}' (phone number pattern)",
            file=sys.stderr
        )
        sys.exit(1)
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}", file=sys.stderr)
        sys.exit(1)
