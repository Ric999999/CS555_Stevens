import unittest
from datetime import datetime, timedelta

# Import the function from us38.py
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from us38 import list_upcoming_birthdays


class TestUS38(unittest.TestCase):

    def setUp(self):
        today = datetime.today()

        # Birthday 10 days from now (should be included)
        self.indi_with_upcoming_bday = {
            "I1": {
                "NAME": "Alice Smith",
                "ALIVE": True,
                "BIRT": today + timedelta(days=10)
            }
        }

        # Birthday 40 days from now (should not be included)
        self.indi_with_future_bday = {
            "I2": {
                "NAME": "Bob Jones",
                "ALIVE": True,
                "BIRT": today + timedelta(days=40)
            }
        }

        # Dead individual (should be excluded)
        self.indi_dead = {
            "I3": {
                "NAME": "Charles Doe",
                "ALIVE": False,
                "BIRT": today + timedelta(days=5)
            }
        }

    def test_upcoming_birthday(self):
        results = list_upcoming_birthdays(self.indi_with_upcoming_bday)
        self.assertEqual(len(results), 1)
        self.assertIn("Alice Smith", results[0])

    def test_future_birthday(self):
        results = list_upcoming_birthdays(self.indi_with_future_bday)
        self.assertEqual(len(results), 0)

    def test_dead_individual(self):
        results = list_upcoming_birthdays(self.indi_dead)
        self.assertEqual(len(results), 0)

    def test_no_upcoming_birthdays(self):
        # Combine individuals with no valid upcoming birthdays
        individuals = {
            **self.indi_with_future_bday,
            **self.indi_dead
        }
        results = list_upcoming_birthdays(individuals)
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
