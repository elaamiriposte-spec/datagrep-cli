"""Parsing utilities for datagrep - query parsing and matching."""

import operator
import re
from typing import Any, Callable, Dict, List

from .exceptions import DataGrepError


def build_matcher(value: str, mode: str, ignore_case: bool) -> Callable[[str], bool]:
    """Build a matcher function based on search mode.
    
    Args:
        value: Search string or pattern.
        mode: Search mode (contains, exact, startswith, endswith, regex).
        ignore_case: Whether to ignore case.
        
    Returns:
        Function that tests if text matches criteria.
        
    Raises:
        ValueError: If mode is unknown.
    """
    if ignore_case:
        value = value.lower()

    if mode == 'contains':
        return lambda text: value in text.lower() if ignore_case else value in text
    if mode == 'exact':
        return lambda text: text.lower() == value if ignore_case else text == value
    if mode == 'startswith':
        return lambda text: text.lower().startswith(value) if ignore_case else text.startswith(value)
    if mode == 'endswith':
        return lambda text: text.lower().endswith(value) if ignore_case else text.endswith(value)
    if mode == 'regex':
        flags: int = re.IGNORECASE if ignore_case else 0
        pattern: re.Pattern[str] = re.compile(value, flags)
        return lambda text: bool(pattern.search(text))
    raise ValueError(f'Unknown mode: {mode}')


def parse_where_condition(condition: str) -> Callable[[Dict[str, Any]], bool]:
    """Parse WHERE condition with AND/OR logic.
    
    Args:
        condition: Filter condition string like "name == John" or "age > 18 and city contains NYC".
        
    Returns:
        Function that evaluates condition on a row dictionary.
        
    Raises:
        DataGrepError: If condition format is invalid.
    """
    def parse_single(cond: str) -> Callable[[Dict[str, Any]], bool]:
        """Parse single condition."""
        parts: List[str] = cond.strip().split()
        if len(parts) != 3:
            raise DataGrepError(
                f'Error in WHERE condition: "{cond}"\n'
                f'  Expected format: "column operator value"\n'
                f'  Make sure to use spaces around the operator.\n'
                f'  Examples:\n'
                f'    --where "name == john"\n'
                f'    --where "age > 25"\n'
                f'    --where "status == active"'
            )
        col, op, val = parts
        ops: Dict[str, Callable[[Any, Any], bool]] = {
            '==': operator.eq,
            '!=': operator.ne,
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            'contains': lambda a, b: b in a,
            'startswith': lambda a, b: a.startswith(b),
            'endswith': lambda a, b: a.endswith(b),
        }
        if op not in ops:
            raise DataGrepError(
                f'Error: Unknown operator "{op}" in condition "{cond}"\n'
                f'  Valid operators are: ==, !=, >, <, >=, <=, contains, startswith, endswith\n'
                f'  Examples:\n'
                f'    --where "status == active"\n'
                f'    --where "age > 25"\n'
                f'    --where "name contains john"'
            )
        return lambda row: ops[op](str(row.get(col, '')), val)

    if ' and ' in condition:
        conditions: List[str] = condition.split(' and ')
        funcs: List[Callable[[Dict[str, Any]], bool]] = [parse_single(c) for c in conditions]
        return lambda row: all(f(row) for f in funcs)
    elif ' or ' in condition:
        conditions = condition.split(' or ')
        funcs = [parse_single(c) for c in conditions]
        return lambda row: any(f(row) for f in funcs)
    else:
        return parse_single(condition)
