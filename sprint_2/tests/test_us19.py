import unittest
import sys
import os

# Dynamically add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from us19 import us19_no_first_cousin_marriages

class TestUS19(unittest.TestCase):

    def test_no_cousin_marriage(self):
        individuals = {}
        families = {
            "F1": {"husb": "I1", "wife": "I2", "children": ["I3", "I4"]},
            "F2": {"husb": "I5", "wife": "I6", "children": ["I7", "I8"]},
            "F3": {"husb": "I3", "wife": "I6"},  # no cousin marriage
        }
        errors = us19_no_first_cousin_marriages(individuals, families)
        self.assertEqual(len(errors), 0)

    def test_cousin_marriage_detected(self):
        individuals = {}
        families = {
            "F1": {"husb": "I1", "wife": "I2", "children": ["I3", "I4"]},   # I3 & I4 are siblings
            "F2": {"husb": "I3", "wife": "I5", "children": ["I9"]},        # I9 = child of I3
            "F3": {"husb": "I4", "wife": "I6", "children": ["I10"]},       # I10 = child of I4
            "F4": {"husb": "I9", "wife": "I10"}                            # I9 marries cousin I10
        }
        errors = us19_no_first_cousin_marriages(individuals, families)
        self.assertTrue(any("ERROR US19" in e for e in errors), "Cousin marriage should have been detected")

    def test_empty_data(self):
        errors = us19_no_first_cousin_marriages({}, {})
        self.assertEqual(errors, [])

if __name__ == "__main__":
    unittest.main()
