import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from us29 import us29_list_deceased

class TestUS29(unittest.TestCase):

    def test_deceased_individuals(self):
        individuals = {
            "I1": {"name": "John /Doe/", "death": "01 JAN 2000"},
            "I2": {"name": "Jane /Doe/", "death": None},
            "I3": {"name": "Bob /Smith/", "death": "15 FEB 1995"}
        }
        expected = [("I1", "John /Doe/"), ("I3", "Bob /Smith/")]
        result = us29_list_deceased(individuals)
        self.assertEqual(sorted(result), sorted(expected))

    def test_no_deceased_individuals(self):
        individuals = {
            "I1": {"name": "John /Doe/", "death": None},
            "I2": {"name": "Jane /Doe/", "death": None}
        }
        result = us29_list_deceased(individuals)
        self.assertEqual(result, [])

    def test_empty_individuals(self):
        individuals = {}
        result = us29_list_deceased(individuals)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
