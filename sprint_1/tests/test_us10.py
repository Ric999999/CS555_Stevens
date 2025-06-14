import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from us10 import us10_marriage_after_14

class TestUS10(unittest.TestCase):

    def test_valid_marriage(self):
        individuals = {
            'I01': {'birth': '1980-01-01'},
            'I02': {'birth': '1982-01-01'}
        }
        families = {
            'F01': {'husb': 'I01', 'wife': 'I02', 'married': '2000-01-01'}
        }
        errors = us10_marriage_after_14(individuals, families)
        self.assertEqual(errors, [])

    def test_husband_under_14(self):
        individuals = {
            'I01': {'birth': '1990-01-01'},
            'I02': {'birth': '1982-01-01'}
        }
        families = {
            'F01': {'husb': 'I01', 'wife': 'I02', 'married': '2002-01-01'}
        }
        errors = us10_marriage_after_14(individuals, families)
        self.assertTrue(any('I01' in e for e in errors))

    def test_wife_under_14(self):
        individuals = {
            'I01': {'birth': '1980-01-01'},
            'I02': {'birth': '1990-01-01'}
        }
        families = {
            'F01': {'husb': 'I01', 'wife': 'I02', 'married': '2002-01-01'}
        }
        errors = us10_marriage_after_14(individuals, families)
        self.assertTrue(any('I02' in e for e in errors))

    def test_both_under_14(self):
        individuals = {
            'I01': {'birth': '1995-01-01'},
            'I02': {'birth': '1995-06-01'}
        }
        families = {
            'F01': {'husb': 'I01', 'wife': 'I02', 'married': '2007-01-01'}
        }
        errors = us10_marriage_after_14(individuals, families)
        self.assertEqual(len(errors), 2)

    def test_missing_birth_or_marriage(self):
        individuals = {
            'I01': {},
            'I02': {'birth': '1982-01-01'}
        }
        families = {
            'F01': {'husb': 'I01', 'wife': 'I02', 'married': None}
        }
        errors = us10_marriage_after_14(individuals, families)
        self.assertEqual(errors, [])

if __name__ == '__main__':
    unittest.main()
