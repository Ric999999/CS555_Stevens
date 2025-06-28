import unittest
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from us17 import is_descendant

class TestUS17(unittest.TestCase):
    def setUp(self):
        self.individuals = {
            "@I1@": {"FAMS": ["@F1@"], "FAMC": None},
            "@I2@": {"FAMS": [], "FAMC": "@F1@"},
            "@I3@": {"FAMS": [], "FAMC": "@F1@"}
        }

        self.families = {
            "@F1@": {"HUSB": "@I1@", "WIFE": "@I4@", "CHIL": ["@I2@", "@I3@"]}
        }

    def test_descendant_positive(self):
        self.assertTrue(is_descendant(self.individuals, self.families, "@I1@", "@I2@"))

    def test_descendant_negative(self):
        self.assertFalse(is_descendant(self.individuals, self.families, "@I2@", "@I1@"))

    def test_descendant_sibling(self):
        self.assertFalse(is_descendant(self.individuals, self.families, "@I2@", "@I3@"))

    def test_descendant_self(self):
        self.assertFalse(is_descendant(self.individuals, self.families, "@I2@", "@I2@"))

    def test_descendant_empty(self):
        self.assertFalse(is_descendant(self.individuals, self.families, "@I99@", "@I2@"))

if __name__ == "__main__":
    unittest.main()
