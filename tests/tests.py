"""Comprehensive test suite for datagrep-cli."""

import unittest
import io
import json
import tempfile
import os
from datagrep import (
    build_matcher, parse_where_condition, load_json_records, format_table,
    validate_args, DataGrepError
)


class TestArgumentValidation(unittest.TestCase):
    """Test argument parsing and validation."""

    def test_inspection_mode_mutual_exclusivity(self):
        """Test that inspection modes are mutually exclusive."""
        args = type('Args', (), {
            'count': True, 'describe': False, 'sample': 0, 'preview': 0,
            'value': None, 'where': None, 'sort': None,
            'columns': None, 'limit': 0, 'mode': 'contains', 'ignore_case': False,
            'empty': False, 'not_empty': False
        })()
        
        args.count = False
        args.describe = True
        self.assertEqual(validate_args(args).describe, True)
        
        args.describe = True
        args.count = True
        with self.assertRaises(DataGrepError):
            validate_args(args)

    def test_inspection_mode_with_search(self):
        """Test that inspection modes cannot be used with search value."""
        args = type('Args', (), {
            'count': True, 'describe': False, 'sample': 0, 'preview': 0,
            'value': 'test', 'where': None, 'sort': None,
            'columns': None, 'limit': 0, 'mode': 'contains', 'ignore_case': False,
            'empty': False, 'not_empty': False
        })()
        
        with self.assertRaises(DataGrepError):
            validate_args(args)

    def test_search_filter_requires_value(self):
        """Test that --where and --sort can be used without search value."""
        # --where can be used independently without a search value
        args = type('Args', (), {
            'count': False, 'describe': False, 'sample': 0, 'preview': 0,
            'value': None, 'where': 'age > 25', 'sort': None,
            'columns': None, 'limit': 0, 'mode': 'contains', 'ignore_case': False,
            'empty': False, 'not_empty': False,
            'input_file': 'test.csv', 'output': None, 'encoding': 'utf-8',
            'select': None, 'file': None, 'search': None
        })()
        
        # Should not raise an error - --where can be used without a search value
        try:
            validate_args(args)
        except DataGrepError:
            self.fail("validate_args raised DataGrepError when --where is used without search value")


class TestSearchMatchers(unittest.TestCase):
    """Test search mode matchers."""

    def test_build_matcher_contains(self):
        """Test substring matching."""
        matcher = build_matcher('test', 'contains', False)
        self.assertTrue(matcher('this is a test'))
        self.assertTrue(matcher('testing'))
        self.assertFalse(matcher('no match'))

    def test_build_matcher_exact(self):
        """Test exact matching."""
        matcher = build_matcher('test', 'exact', False)
        self.assertTrue(matcher('test'))
        self.assertFalse(matcher('testing'))
        self.assertFalse(matcher('atest'))

    def test_build_matcher_startswith(self):
        """Test startswith matching."""
        matcher = build_matcher('test', 'startswith', False)
        self.assertTrue(matcher('test123'))
        self.assertTrue(matcher('testing'))
        self.assertFalse(matcher('atest'))

    def test_build_matcher_endswith(self):
        """Test endswith matching."""
        matcher = build_matcher('test', 'endswith', False)
        self.assertTrue(matcher('atest'))
        self.assertTrue(matcher('test'))
        self.assertFalse(matcher('test123'))

    def test_build_matcher_regex(self):
        """Test regex matching."""
        matcher = build_matcher(r'\d{2,4}', 'regex', False)
        self.assertTrue(matcher('abc123def'))
        self.assertTrue(matcher('12'))
        self.assertFalse(matcher('a'))

    def test_build_matcher_ignore_case(self):
        """Test case-insensitive matching."""
        matcher = build_matcher('TEST', 'contains', True)
        self.assertTrue(matcher('this is a test'))
        self.assertTrue(matcher('THIS IS A TEST'))
        self.assertTrue(matcher('TeSt'))

    def test_build_matcher_case_sensitive(self):
        """Test case-sensitive matching."""
        matcher = build_matcher('test', 'contains', False)
        self.assertTrue(matcher('this is a test'))
        self.assertFalse(matcher('THIS IS A TEST'))


class TestWhereConditions(unittest.TestCase):
    """Test where condition parsing."""

    def test_where_condition_eq(self):
        """Test equality comparison."""
        func = parse_where_condition('age == 25')
        self.assertTrue(func({'age': '25'}))
        self.assertFalse(func({'age': '30'}))

    def test_where_condition_ne(self):
        """Test not-equal comparison."""
        func = parse_where_condition('age != 25')
        self.assertFalse(func({'age': '25'}))
        self.assertTrue(func({'age': '30'}))

    def test_where_condition_gt(self):
        """Test greater-than comparison."""
        func = parse_where_condition('age > 25')
        self.assertTrue(func({'age': '30'}))
        self.assertFalse(func({'age': '20'}))
        self.assertFalse(func({'age': '25'}))

    def test_where_condition_lt(self):
        """Test less-than comparison."""
        func = parse_where_condition('age < 25')
        self.assertTrue(func({'age': '20'}))
        self.assertFalse(func({'age': '30'}))
        self.assertFalse(func({'age': '25'}))

    def test_where_condition_contains(self):
        """Test contains operation."""
        func = parse_where_condition('name contains John')
        self.assertTrue(func({'name': 'John Doe'}))
        self.assertTrue(func({'name': 'John'}))
        self.assertFalse(func({'name': 'Jane Doe'}))

    def test_where_condition_startswith(self):
        """Test startswith operation."""
        func = parse_where_condition('name startswith John')
        self.assertTrue(func({'name': 'John Doe'}))
        self.assertFalse(func({'name': 'Doe John'}))

    def test_where_condition_and(self):
        """Test AND logic."""
        func = parse_where_condition('age > 25 and city == London')
        self.assertTrue(func({'age': '30', 'city': 'London'}))
        self.assertFalse(func({'age': '20', 'city': 'London'}))
        self.assertFalse(func({'age': '30', 'city': 'Paris'}))

    def test_where_condition_or(self):
        """Test OR logic."""
        func = parse_where_condition('age < 20 or city == London')
        self.assertTrue(func({'age': '15', 'city': 'Paris'}))
        self.assertTrue(func({'age': '30', 'city': 'London'}))
        self.assertFalse(func({'age': '25', 'city': 'Paris'}))

    def test_where_condition_invalid(self):
        """Test invalid condition format."""
        with self.assertRaises(DataGrepError):
            parse_where_condition('invalid condition')


class TestJsonLoading(unittest.TestCase):
    """Test JSON record loading."""

    def test_load_json_array(self):
        """Test loading JSON array format."""
        data = '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]'
        records = load_json_records(io.StringIO(data))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]['name'], 'Alice')
        self.assertEqual(records[1]['age'], 30)

    def test_load_json_newline_delimited(self):
        """Test loading newline-delimited JSON."""
        data = '{"name": "Alice", "age": 25}\n{"name": "Bob", "age": 30}\n'
        records = load_json_records(io.StringIO(data))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]['name'], 'Alice')

    def test_load_json_invalid(self):
        """Test error on invalid JSON."""
        data = '{"name": "Alice"'
        with self.assertRaises(ValueError):
            load_json_records(io.StringIO(data))

    def test_load_json_single_object_error(self):
        """Test error on single object (not array)."""
        data = '{"name": "Alice"}'
        with self.assertRaises(ValueError):
            load_json_records(io.StringIO(data))


class TestTableFormatting(unittest.TestCase):
    """Test table output formatting."""

    def test_format_table_basic(self):
        """Test basic table formatting."""
        rows = [
            {'name': 'Alice', 'age': '25'},
            {'name': 'Bob', 'age': '30'}
        ]
        fields = ['name', 'age']
        table = format_table(rows, fields)
        
        self.assertIn('Alice', table)
        self.assertIn('Bob', table)
        self.assertIn('name', table)
        self.assertIn('age', table)

    def test_format_table_empty(self):
        """Test empty table formatting."""
        table = format_table([], ['name', 'age'])
        self.assertEqual(table, '')

    def test_format_table_alignment(self):
        """Test column alignment."""
        rows = [{'short': 'a', 'long': 'verylong'}]
        fields = ['short', 'long']
        table = format_table(rows, fields)
        lines = table.split('\n')
        
        self.assertTrue(all('|' in line for line in lines))


if __name__ == '__main__':
    unittest.main()
