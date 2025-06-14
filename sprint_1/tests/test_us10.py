import unittest
import sys
import os

# Add project root to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from us10 import us10_marriage_after_14

class TestUS10(unittest.TestCase):

    def test_marriage_under_14(self):
        individuals = {
            'I01': {'birth': '2000-01-01'},
            'I02': {'birth': '2000-01-01'}
        }
        families = {
            'F01': {
                'husb': 'I01',
                'wife': 'I02',
                'married': '2013-12-31'
            }
        }
        errors = us10_marriage_after_14(individuals, families)
        self.assertTrue(any("ERROR US10" in e for e in errors))

    def test_marriage_exactly_14(self):
        individuals = {
            'I01': {'birth': '2000-01-01'},
            'I02': {'birth': '2000-01-01'}
        }
        families = {
            'F01': {
                'husb': 'I01',
                'wife': 'I02',
                'married': '2014-01-01'
            }
        }
        errors = us10_marriage_after_14(individuals, families)
        self.assertEqual(errors, [])

    def test_missing_marriage_date(self):
        individuals = {
            'I01': {'birth': '1990-01-01'},
            'I02': {'birth': '1990-01-01'}
        }
        families = {
            'F01': {
                'husb': 'I01',
                'wife': 'I02',
                # missing married
            }
        }
        errors = us10_marriage_after_14(individuals, families)
        self.assertEqual(errors, [])

if __name__ == '__main__':
    unittest.main()
