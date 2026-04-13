"""OutputFormatter - handles output formatting and writing."""

import argparse
import csv
import io
import json
import sys
from typing import Any, Dict, List, TextIO, Union

from ..utils import format_table


class OutputFormatter:
    """Handles output formatting and writing."""
    
    def __init__(self, args: argparse.Namespace):
        """Initialize OutputFormatter.
        
        Args:
            args: Parsed command-line arguments.
        """
        self.args = args
    
    def write_output(self, records: List[Dict[str, Any]], selected_columns: List[str], 
                     show_count: bool = False) -> None:
        """Write records to output in specified format.
        
        Args:
            records: List of records to output.
            selected_columns: Columns to include in output.
            show_count: Whether to prepend record count.
        """
        output_file = open(self.args.output, 'w', encoding=self.args.encoding, newline='') \
            if self.args.output else sys.stdout
        
        try:
            if self.args.output_format == 'csv':
                self._write_csv(output_file, records, selected_columns, show_count)
            elif self.args.output_format == 'json':
                self._write_json(output_file, records, selected_columns, show_count)
            elif self.args.output_format == 'table':
                self._write_table(output_file, records, selected_columns, show_count)
            else:  # raw
                self._write_raw(output_file, records, selected_columns, show_count)
        finally:
            if self.args.output:
                output_file.close()
    
    def _write_csv(self, output_file: Union[TextIO, io.TextIOBase], 
                    records: List[Dict[str, Any]], columns: List[str], show_count: bool) -> None:
        """Write records as CSV."""
        if show_count:
            output_file.write(f"Count: {len(records)}\n")
        
        writer = csv.DictWriter(output_file, fieldnames=columns, delimiter=self.args.delimiter)
        writer.writeheader()
        for row in records:
            writer.writerow({col: row.get(col, '') for col in columns})
    
    def _write_json(self, output_file: Union[TextIO, io.TextIOBase], 
                     records: List[Dict[str, Any]], columns: List[str], show_count: bool) -> None:
        """Write records as JSON."""
        if show_count:
            output_data = {
                'count': len(records),
                'data': [{col: row.get(col, '') for col in columns} for row in records]
            }
            json.dump(output_data, output_file, ensure_ascii=False, indent=2)
        else:
            json.dump(
                [{col: row.get(col, '') for col in columns} for row in records],
                output_file,
                ensure_ascii=False,
                indent=2
            )
        output_file.write('\n')
    
    def _write_table(self, output_file: Union[TextIO, io.TextIOBase], 
                      records: List[Dict[str, Any]], columns: List[str], show_count: bool) -> None:
        """Write records as ASCII table."""
        if show_count:
            output_file.write(f"Count: {len(records)}\n")
        
        output_file.write(format_table(records, columns, self.args.color))
        output_file.write('\n')
    
    def _write_raw(self, output_file: Union[TextIO, io.TextIOBase], 
                    records: List[Dict[str, Any]], columns: List[str], show_count: bool) -> None:
        """Write records as raw format (dictionary representation)."""
        if show_count:
            output_file.write(f"Count: {len(records)}\n")
        
        for row in records:
            subset = {col: row.get(col, '') for col in columns}
            output_file.write(f"{subset}\n")
