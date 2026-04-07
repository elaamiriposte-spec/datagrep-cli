import unittest
from search_csv import build_matcher, parse_where_condition, load_json_records, format_table
import io


class TestSearchCsv(unittest.TestCase):

    def test_build_matcher_contains(self):
        matcher = build_matcher('test', 'contains', False)
        self.assertTrue(matcher('this is a test'))
        self.assertFalse(matcher('no match'))

    def test_build_matcher_exact(self):
        matcher = build_matcher('test', 'exact', False)
        self.assertTrue(matcher('test'))
        self.assertFalse(matcher('testing'))

    def test_build_matcher_ignore_case(self):
        matcher = build_matcher('TEST', 'contains', True)
        self.assertTrue(matcher('this is a test'))
        self.assertTrue(matcher('THIS IS A TEST'))

    def test_build_matcher_regex(self):
        matcher = build_matcher(r'\d+', 'regex', False)
        self.assertTrue(matcher('abc123def'))
        self.assertFalse(matcher('abcdef'))

    def test_parse_where_condition_eq(self):
        where_func = parse_where_condition('age == 25')
        self.assertTrue(where_func({'age': '25'}))
        self.assertFalse(where_func({'age': '30'}))

    def test_parse_where_condition_gt(self):
        where_func = parse_where_condition('age > 25')
        self.assertTrue(where_func({'age': '30'}))
        self.assertFalse(where_func({'age': '20'}))

    def test_parse_where_condition_contains(self):
        where_func = parse_where_condition('name contains John')
        self.assertTrue(where_func({'name': 'John Doe'}))
        self.assertFalse(where_func({'name': 'Jane Doe'}))

    def test_load_json_records_array(self):
        json_data = '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]'
        records = load_json_records(io.StringIO(json_data))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]['name'], 'Alice')

    def test_load_json_records_newline(self):
        json_data = '{"name": "Alice", "age": 25}\n{"name": "Bob", "age": 30}\n'
        records = load_json_records(io.StringIO(json_data))
        self.assertEqual(len(records), 2)

    def test_format_table(self):
        rows = [{'name': 'Alice', 'age': '25'}, {'name': 'Bob', 'age': '30'}]
        fieldnames = ['name', 'age']
        table = format_table(rows, fieldnames)
        lines = table.split('\n')
        self.assertIn('name', lines[0])
        self.assertIn('Alice', lines[2])

    def test_format_table_empty(self):
        table = format_table([], ['name'])
        self.assertEqual(table, '')


if __name__ == '__main__':
    unittest.main()