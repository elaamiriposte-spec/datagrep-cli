"""Formatting utilities for datagrep - output formatting."""

from typing import Any, Dict, List

try:
    from colorama import Fore, Style
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


def format_table(rows: List[Dict[str, Any]], fieldnames: List[str], color: bool = False) -> str:
    """Format records as aligned ASCII table.
    
    Args:
        rows: List of record dictionaries.
        fieldnames: Column names to include.
        color: Whether to use ANSI color codes.
        
    Returns:
        Formatted table string.
    """
    if not rows:
        return ''

    widths: Dict[str, int] = {field: len(field) for field in fieldnames}
    for row in rows:
        for field in fieldnames:
            widths[field] = max(widths[field], len(str(row.get(field, ''))))

    header_parts: List[str] = [field.ljust(widths[field]) for field in fieldnames]
    if color and COLORAMA_AVAILABLE:
        header: str = Fore.CYAN + ' | '.join(header_parts) + Style.RESET_ALL
        separator: str = Fore.YELLOW + '-+-'.join('-' * widths[field] for field in fieldnames) + Style.RESET_ALL
    else:
        header = ' | '.join(header_parts)
        separator = '-+-'.join('-' * widths[field] for field in fieldnames)
    lines: List[str] = [header, separator]
    for row in rows:
        line_parts = [str(row.get(field, '')).ljust(widths[field]) for field in fieldnames]
        lines.append(' | '.join(line_parts))
    return '\n'.join(lines)
