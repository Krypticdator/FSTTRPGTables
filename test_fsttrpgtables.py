import unittest
from fsttrpgtables.models import Table
from fsttrpgtables.db import FuzionTable


class testTableModel(unittest.TestCase):
    def test_constructor_without_load(self):
        t = Table('test', load_from_name=False)
        self.assertEqual(t.max, 0)

    def test_constructor(self):
        t = Table('test')
        print(t)
        self.assertEqual(t.max, 3)

    def test_table_adding_options(self):
        t = Table('test', load_from_name=False)
        t.add_option(1, 2, 'result1', leads_to=None, identifier='first0')
        t.add_option(3, 3, 'result2', leads_to=None, identifier='first1')

        self.assertEqual(t.get_result(index=1).re, 'result1')
        self.assertEqual(t.get_result(index=2).re, 'result1')
        self.assertEqual(t.get_result(index=3).re, 'result2')

    def test_table_random_option(self):
        t = Table('test', load_from_name=False)
        t.add_option(1, 1, 'result', leads_to=None, identifier='first')
        result = t.random_result()
        self.assertEqual(result, 'result')