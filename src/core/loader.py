"""DataLoader - handles file loading and format detection."""

import argparse
import csv
import io
import logging
from typing import Any, Dict, List, Optional, TextIO, Union

from utils import load_json_records, load_excel_records, open_input_file, check_file_size


class DataLoader:
    """Handles file loading, format detection, and column extraction."""
    
    def __init__(self, args: argparse.Namespace):
        """Initialize DataLoader with parsed arguments.
        
        Args:
            args: Parsed command-line arguments.
        """
        self.args = args
        self.records: List[Dict[str, Any]] = []
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
        
        # Always eager load to ensure file can be closed safely
        # Lazy loading would require keeping the file handle open
        self.records = list(reader)
        self.records_count = len(self.records)
        logging.debug("Loaded %d records from CSV file", self.records_count)
    
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
