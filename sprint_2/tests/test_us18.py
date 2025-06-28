import unittest
import sys
import os

# Ensure the parent folder (sprint_2) is in the Python path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

import us18  

class TestUS18(unittest.TestCase):
    def setUp(self):
        self.valid_individuals = {
            "I1": {"FAMC": ["F1"], "FAMS": ["F2"]},
            "I2": {"FAMC": ["F3"], "FAMS": ["F2"]},
            "I3": {"FAMC": [], "FAMS": []}
        }
        self.valid_families = {
            "F1": {"HUSB": "I10", "WIFE": "I11", "CHIL": ["I1"]},
            "F3": {"HUSB": "I12", "WIFE": "I13", "CHIL": ["I2"]},
            "F2": {"HUSB": "I1", "WIFE": "I2", "CHIL": []}
        }

        self.sibling_marriage_families = {
            "F1": {"HUSB": "I10", "WIFE": "I11", "CHIL": ["I1", "I2"]},
            "F2": {"HUSB": "I1", "WIFE": "I2", "CHIL": []}
        }

    def run_with_mock(self, mock_individuals, mock_families):
        original_parser = us18.parse_gedcom
        us18.parse_gedcom = lambda _: (mock_individuals, mock_families)
        errors = us18.check_sibling_marriage("mock")
        us18.parse_gedcom = original_parser  # restore original
        return errors

    def test_no_sibling_marriage(self):
        errors = self.run_with_mock(self.valid_individuals, self.valid_families)
        self.assertEqual(errors, [])

    def test_detect_sibling_marriage(self):
        individuals = {
            "I1": {"FAMC": ["F1"], "FAMS": ["F2"]},
            "I2": {"FAMC": ["F1"], "FAMS": ["F2"]}
        }
        errors = self.run_with_mock(individuals, self.sibling_marriage_families)
        self.assertEqual(len(errors), 1)
        self.assertIn("US18", errors[0])

    def test_missing_spouse(self):
        individuals = {
            "I1": {"FAMC": ["F1"], "FAMS": ["F2"]},
            "I2": {"FAMC": ["F1"], "FAMS": ["F2"]}
        }
        families = {
            "F1": {"HUSB": "I10", "WIFE": "I11", "CHIL": ["I1", "I2"]},
            "F2": {"HUSB": "I1", "WIFE": None, "CHIL": []}
        }
        errors = self.run_with_mock(individuals, families)
        self.assertEqual(errors, [])

    def test_multiple_family_links(self):
        individuals = {
            "I1": {"FAMC": ["F1", "F3"], "FAMS": ["F2"]},
            "I2": {"FAMC": ["F3"], "FAMS": ["F2"]}
        }
        families = {
            "F1": {"HUSB": "I10", "WIFE": "I11", "CHIL": ["I1"]},
            "F3": {"HUSB": "I12", "WIFE": "I13", "CHIL": ["I1", "I2"]},
            "F2": {"HUSB": "I1", "WIFE": "I2", "CHIL": []}
        }
        errors = self.run_with_mock(individuals, families)
        self.assertEqual(len(errors), 1)

    def test_empty_data(self):
        errors = self.run_with_mock({}, {})
        self.assertEqual(errors, [])

if __name__ == "__main__":
    unittest.main()
