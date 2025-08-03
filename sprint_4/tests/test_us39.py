import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to sys.path so we can import us39
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from us39 import us39_upcoming_birthdays

class TestUS39(unittest.TestCase):

    def test_upcoming_birthday(self):
        today = datetime.today()
        upcoming = (today + timedelta(days=10)).strftime("%d %b %Y")

        individuals = {
            "I01": {"name": "John /Doe/", "birth": upcoming, "death": None}
        }

        result = us39_upcoming_birthdays(individuals)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "I01")

    def test_birthday_outside_30_days(self):
        today = datetime.today()
        future = (today + timedelta(days=40)).strftime("%d %b %Y")

        individuals = {
            "I02": {"name": "Jane /Doe/", "birth": future, "death": None}
        }

        result = us39_upcoming_birthdays(individuals)
        self.assertEqual(result, [])

    def test_deceased_individual(self):
        today = datetime.today()
        upcoming = (today + timedelta(days=5)).strftime("%d %b %Y")

        individuals = {
            "I03": {"name": "Bob /Smith/", "birth": upcoming, "death": "01 JAN 2020"}
        }

        result = us39_upcoming_birthdays(individuals)
        self.assertEqual(result, [])

    def test_missing_birth_date(self):
        individuals = {
            "I04": {"name": "No /Birthday/", "birth": None, "death": None}
        }

        result = us39_upcoming_birthdays(individuals)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
