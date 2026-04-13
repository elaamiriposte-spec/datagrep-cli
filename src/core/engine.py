"""SearchEngine - handles filtering and searching operations."""

import argparse
import logging
from typing import Any, Callable, Dict, Iterator, List, Union

from ..utils import build_matcher, parse_where_condition

try:
    import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class SearchEngine:
    """Handles filtering and searching operations."""
    
    def __init__(self, records: Union[List[Dict[str, Any]], Iterator[Dict[str, Any]]], 
                 available_columns: List[str], args: argparse.Namespace):
        """Initialize SearchEngine.
        
        Args:
            records: List or iterator of record dictionaries.
            available_columns: List of available column names.
            args: Parsed command-line arguments.
        """
        self.records = records
        self.available_columns = available_columns
        self.args = args
    
    def apply_filters(self) -> Union[List[Dict[str, Any]], Iterator[Dict[str, Any]]]:
        """Apply all filters (where, sort, empty, not-empty).
        
        Returns:
            Filtered records (list or iterator).
        """
        records = self.records
        
        # Convert to list for filtering if needed
        if not isinstance(records, list):
            records = list(records)
        
        # Apply where filter
        if self.args.where:
            logging.debug("Applying where filter: %s", self.args.where)
            where_func = parse_where_condition(self.args.where)
            records = [r for r in records if where_func(r)]
            logging.info("After where filter: %d records", len(records))
        
        # Apply empty filter
        if self.args.empty:
            logging.debug("Filtering for empty values in columns: %s", self.args.columns)
            filter_cols = [col.strip() for col in self.args.columns.split(',') if col.strip()]
            records = [r for r in records if any(str(r.get(col, '')).strip() == '' for col in filter_cols)]
            logging.info("After empty filter: %d records", len(records))
        
        # Apply not-empty filter
        if self.args.not_empty:
            logging.debug("Filtering for non-empty values in columns: %s", self.args.columns)
            filter_cols = [col.strip() for col in self.args.columns.split(',') if col.strip()]
            records = [r for r in records if any(str(r.get(col, '')).strip() != '' for col in filter_cols)]
            logging.info("After not-empty filter: %d records", len(records))
        
        # Apply sorting
        if self.args.sort:
            logging.debug("Applying sort: %s", self.args.sort)
            sort_col, sort_order = self.args.sort.split(':')
            reverse = sort_order.lower() == 'desc'
            records.sort(key=lambda r: str(r.get(sort_col, '')), reverse=reverse)
            logging.info("Records sorted by %s %s", sort_col, sort_order)
        
        return records
    
    def search(self, columns: List[str]) -> List[Dict[str, Any]]:
        """Search records for matching values.
        
        Args:
            columns: Columns to search in.
            
        Returns:
            List of matching records.
        """
        matcher = build_matcher(self.args.value, self.args.mode, self.args.ignore_case)
        logging.debug("Searching for '%s' in columns: %s", self.args.value, ', '.join(columns))
        
        matches: List[Dict[str, Any]] = []
        count = 0
        records = self.records
        
        # Apply progress bar if needed
        if self.args.progress and TQDM_AVAILABLE:
            if isinstance(records, list) and len(records) > 1000:
                records = tqdm.tqdm(records)
            elif not isinstance(records, list):
                records = tqdm.tqdm(records)
        
        for row in records:
            if any(matcher(str(row.get(col, ''))) for col in columns):
                matches.append(row)
                count += 1
                if self.args.limit and count >= self.args.limit:
                    break
        
        logging.info("Found %d matching records", len(matches))
        return matches
