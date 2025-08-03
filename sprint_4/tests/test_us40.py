import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to sys.path so we can import us40
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from us40 import us40_upcoming_anniversaries

class TestUS40(unittest.TestCase):

    def test_upcoming_anniversary(self):
        today = datetime.today()
        recent_anniversary = (today + timedelta(days=10)).strftime("%d %b %Y")

        individuals = {
            "I1": {"name": "John /Doe/", "death": None},
            "I2": {"name": "Jane /Smith/", "death": None}
        }

        families = {
            "F1": {
                "husb": "I1",
                "wife": "I2",
                "married": recent_anniversary
            }
        }

        result = us40_upcoming_anniversaries(individuals, families)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "F1")

    def test_anniversary_outside_30_days(self):
        future_anniversary = (datetime.today() + timedelta(days=45)).strftime("%d %b %Y")

        individuals = {
            "I3": {"name": "Bob /Brown/", "death": None},
            "I4": {"name": "Alice /White/", "death": None}
        }

        families = {
            "F2": {
                "husb": "I3",
                "wife": "I4",
                "married": future_anniversary
            }
        }

        result = us40_upcoming_anniversaries(individuals, families)
        self.assertEqual(result, [])

    def test_deceased_spouse(self):
        today = datetime.today()
        upcoming = (today + timedelta(days=5)).strftime("%d %b %Y")

        individuals = {
            "I5": {"name": "Sam /Lee/", "death": "01 JAN 2020"},
            "I6": {"name": "Ann /Lee/", "death": None}
        }

        families = {
            "F3": {
                "husb": "I5",
                "wife": "I6",
                "married": upcoming
            }
        }

        result = us40_upcoming_anniversaries(individuals, families)
        self.assertEqual(result, [])

    def test_missing_marriage_date(self):
        individuals = {
            "I7": {"name": "Joe /Missing/", "death": None},
            "I8": {"name": "Sue /Missing/", "death": None}
        }

        families = {
            "F4": {
                "husb": "I7",
                "wife": "I8"
            }
        }

        result = us40_upcoming_anniversaries(individuals, families)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
