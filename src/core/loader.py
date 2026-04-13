"""DataLoader - handles file loading and format detection."""

import argparse
import csv
import io
import logging
from typing import Any, Dict, Iterator, List, Optional, TextIO, Union

from ..utils import load_json_records, load_excel_records, open_input_file, check_file_size


def _should_load_eagerly(args: argparse.Namespace) -> bool:
    """Determine if records should be loaded eagerly (all at once) vs lazily.
    
    Eager loading is required for:
    - Inspection modes (--describe, --sample, --preview)
    - Filtering (--where, --sort, --empty, --not-empty)
    - Counting (--count, --show-count)
    - When no limit is specified
    
    Args:
        args: Parsed command-line arguments.
        
    Returns:
        True if should load all records eagerly, False for lazy loading.
    """
    inspection_modes: List[bool] = [args.describe, args.sample > 0, args.preview > 0]
    has_inspection = any(inspection_modes)
    has_filters = bool(args.where or args.sort or args.empty or args.not_empty)
    has_counting = bool(args.count or args.show_count)
    has_no_value = args.value is None
    
    # Need eager loading if:
    if has_no_value:  # Inspection mode without value
        return True
    if has_inspection:  # Any inspection mode
        return True
    if has_filters:  # Any filtering
        return True
    if has_counting:  # Any counting (need all records for accurate count)
        return True
    if not args.limit:  # No limit specified, need all for full output
        return True
    
    # Can use lazy loading: search with --limit, no filters, no inspection, no counting
    return False


class DataLoader:
    """Handles file loading, format detection, and column extraction."""
    
    def __init__(self, args: argparse.Namespace):
        """Initialize DataLoader with parsed arguments.
        
        Args:
            args: Parsed command-line arguments.
        """
        self.args = args
        self.records: Union[List[Dict[str, Any]], Iterator[Dict[str, Any]]] = []
        self.available_columns: List[str] = []
        self.records_count: Optional[int] = None
    
    def load(self) -> None:
        """Load data from input file.
        
        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file format is invalid.
        """
        check_file_size(self.args.input_file)
        
        with open_input_file(self.args.input_file, self.args.encoding) as csvfile:
            input_format = self._detect_format(csvfile)
            
            if input_format == 'csv':
                self._load_csv(csvfile)
            elif input_format == 'xlsx':
                self._load_excel()
            else:  # json
                self._load_json(csvfile)
    
    def _detect_format(self, csvfile: Union[TextIO, io.StringIO]) -> str:
        """Detect input file format.
        
        Args:
            csvfile: Opened file object.
            
        Returns:
            Format string: 'csv', 'json', or 'xlsx'.
        """
        input_format = self.args.input_format
        
        if input_format == 'auto':
            if self.args.input_file != '-' and self.args.input_file.lower().endswith('.json'):
                input_format = 'json'
            elif self.args.input_file != '-' and self.args.input_file.lower().endswith('.xlsx'):
                input_format = 'xlsx'
            elif self.args.input_file != '-' and self.args.input_file.lower().endswith('.csv'):
                input_format = 'csv'
            elif self.args.input_file == '-':
                text: str = csvfile.read()
                csvfile = io.StringIO(text)
                input_format = 'json' if text.lstrip().startswith(('{', '[')) else 'csv'
            else:
                input_format = 'csv'
        
        return input_format
    
    def _load_csv(self, csvfile: Union[TextIO, io.StringIO]) -> None:
        """Load data from CSV file.
        
        Args:
            csvfile: Opened CSV file object.
        """
        reader = csv.DictReader(csvfile, delimiter=self.args.delimiter)
        if not reader.fieldnames:
            raise ValueError('CSV input has no headers.')
        
        self.available_columns = list(reader.fieldnames)
        
        # Decide whether to load eagerly or lazily
        use_lazy = not _should_load_eagerly(self.args)
        if use_lazy:
            self.records = reader
            logging.debug("Using lazy loading mode for CSV search")
        else:
            self.records = list(reader)
            self.records_count = len(self.records)
            logging.debug("Using eager loading mode for CSV (loaded %d records)", self.records_count)
    
    def _load_json(self, csvfile: Union[TextIO, io.StringIO]) -> None:
        """Load data from JSON file.
        
        Args:
            csvfile: Opened JSON file object.
        """
        self.records = load_json_records(csvfile)
        self.records_count = len(self.records)
        
        # Extract columns from JSON
        seen = set()
        self.available_columns = []
        for row in self.records:
            for key in row.keys():
                if key not in seen:
                    seen.add(key)
                    self.available_columns.append(key)
        
        logging.debug("Loaded %d records from JSON file", self.records_count)
    
    def _load_excel(self) -> None:
        """Load data from Excel file."""
        self.records, self.available_columns = load_excel_records(self.args.input_file)
        self.records_count = len(self.records)
        logging.debug("Loaded %d records from Excel file", self.records_count)
    
    def get_columns_from_string(self, columns_str: str) -> List[str]:
        """Parse columns from comma-separated string.
        
        Args:
            columns_str: Comma-separated column names.
            
        Returns:
            List of column names.
        """
        if not columns_str:
            return list(self.available_columns)
        
        parsed = [col.strip() for col in columns_str.split(',') if col.strip()]
        return list(self.available_columns) if parsed == ['*'] else parsed
