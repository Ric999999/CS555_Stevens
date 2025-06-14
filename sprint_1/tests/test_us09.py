import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from us09 import us09_birth_before_death_of_parents

class TestUS09(unittest.TestCase):
    def test_child_after_mother_death(self):
        individuals = {
            'I1': {'birth': '2001-01-01'},
            'M1': {'death': '2000-01-01'},
            'F1': {}
        }
        families = {
            'F1': {'husb': 'F1', 'wife': 'M1', 'children': ['I1']}
        }
        errors = us09_birth_before_death_of_parents(individuals, families)
        self.assertTrue(any("mother's death" in e for e in errors))

    def test_child_too_late_after_father_death(self):
        individuals = {
            'I2': {'birth': '2001-01-01'},
            'M2': {},
            'F2': {'death': '1999-01-01'}
        }
        families = {
            'F2': {'husb': 'F2', 'wife': 'M2', 'children': ['I2']}
        }
        errors = us09_birth_before_death_of_parents(individuals, families)
        self.assertTrue(any("father's death" in e for e in errors))

    def test_child_valid_birth(self):
        individuals = {
            'I3': {'birth': '2000-01-01'},
            'M3': {'death': '2005-01-01'},
            'F3': {'death': '1999-05-01'}
        }
        families = {
            'F3': {'husb': 'F3', 'wife': 'M3', 'children': ['I3']}
        }
        errors = us09_birth_before_death_of_parents(individuals, families)
        self.assertEqual(errors, [])

    def test_no_death_dates(self):
        individuals = {
            'I4': {'birth': '2001-01-01'},
            'M4': {},
            'F4': {}
        }
        families = {
            'F4': {'husb': 'F4', 'wife': 'M4', 'children': ['I4']}
        }
        errors = us09_birth_before_death_of_parents(individuals, families)
        self.assertEqual(errors, [])

    def test_missing_birth_date(self):
        individuals = {
            'I5': {},
            'M5': {'death': '2005-01-01'},
            'F5': {'death': '2004-01-01'}
        }
        families = {
            'F5': {'husb': 'F5', 'wife': 'M5', 'children': ['I5']}
        }
        errors = us09_birth_before_death_of_parents(individuals, families)
        self.assertEqual(errors, [])

if __name__ == '__main__':
    unittest.main()
