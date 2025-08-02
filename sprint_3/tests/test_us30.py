import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from us30 import us30_list_living_married

class TestUS30(unittest.TestCase):

    def test_living_married_individuals(self):
        individuals = {
            "I1": {"name": "John /Doe/", "death": None},
            "I2": {"name": "Jane /Doe/", "death": None},
            "I3": {"name": "Bob /Smith/", "death": "01 JAN 2020"},
            "I4": {"name": "Alice /Smith/", "death": None}
        }
        families = {
            "F1": {"husb": "I1", "wife": "I2"},
            "F2": {"husb": "I3", "wife": "I4"}
        }
        expected = [("I1", "John /Doe/"), ("I2", "Jane /Doe/"), ("I4", "Alice /Smith/")]
        result = us30_list_living_married(individuals, families)
        self.assertEqual(sorted(result), sorted(expected))

    def test_no_living_married_individuals(self):
        individuals = {
            "I1": {"name": "John /Doe/", "death": "01 JAN 2020"},
            "I2": {"name": "Jane /Doe/", "death": "01 JAN 2020"}
        }
        families = {
            "F1": {"husb": "I1", "wife": "I2"}
        }
        result = us30_list_living_married(individuals, families)
        self.assertEqual(result, [])

    def test_empty_data(self):
        individuals = {}
        families = {}
        result = us30_list_living_married(individuals, families)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
