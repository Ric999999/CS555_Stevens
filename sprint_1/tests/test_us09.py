import unittest
import sys
import os

# Add project root to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from us09 import us09_birth_before_death_of_parents

class TestUS09(unittest.TestCase):

    def test_birth_after_mother_death(self):
        individuals = {
            'I01': {'birth': '2020-01-01'},
            'I02': {'death': '2019-01-01'}
        }
        families = {
            'F01': {
                'husb': 'NA',
                'wife': 'I02',
                'children': ['I01']
            }
        }
        errors = us09_birth_before_death_of_parents(individuals, families)
        self.assertTrue(any("mother" in e for e in errors))

    def test_birth_too_long_after_father_death(self):
        individuals = {
            'I01': {'birth': '2021-01-01'},
            'I02': {'death': '2020-01-01'}
        }
        families = {
            'F01': {
                'husb': 'I02',
                'wife': 'NA',
                'children': ['I01']
            }
        }
        errors = us09_birth_before_death_of_parents(individuals, families)
        self.assertTrue(any("father" in e for e in errors))

    def test_valid_birth(self):
        individuals = {
            'I01': {'birth': '2020-01-01'},
            'I02': {'death': '2021-01-01'},
            'I03': {'death': '2019-06-01'}
        }
        families = {
            'F01': {
                'husb': 'I03',
                'wife': 'I02',
                'children': ['I01']
            }
        }
        errors = us09_birth_before_death_of_parents(individuals, families)
        self.assertEqual(errors, [])

if __name__ == '__main__':
    unittest.main()
