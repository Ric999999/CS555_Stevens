import unittest
from datetime import datetime, timedelta
import sys, os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from us37 import list_recent_deaths

class TestUS37(unittest.TestCase):
    def setUp(self):
        """Prepare sample individuals and families for testing."""
        self.individuals = {
            "@I1@": {
                "NAME": "John Doe",
                "ALIVE": False,
                "DEATH": datetime.now() - timedelta(days=10),  # recent death
                "SPOUSE": ["@F1@"],
                "CHILDREN": []
            },
            "@I2@": {
                "NAME": "Jane Doe",
                "ALIVE": True,
                "DEATH": None,
                "SPOUSE": ["@F1@"],
                "CHILDREN": []
            },
            "@I3@": {
                "NAME": "Baby Doe",
                "ALIVE": True,
                "DEATH": None,
                "SPOUSE": [],
                "CHILDREN": []
            },
            "@I4@": {
                "NAME": "Old Person",
                "ALIVE": False,
                "DEATH": datetime.now() - timedelta(days=100),  # old death
                "SPOUSE": [],
                "CHILDREN": []
            }
        }

        self.families = {
            "@F1@": {
                "HUSB": "@I1@",
                "WIFE": "@I2@",
                "CHIL": ["@I3@"]
            }
        }

    def test_recent_death_with_family(self):
        results = list_recent_deaths(self.individuals, self.families)
        self.assertTrue(any("John Doe" in res for res in results))
        self.assertTrue(any("Jane Doe" in res for res in results))
        self.assertTrue(any("Baby Doe" in res for res in results))

    def test_old_death_ignored(self):
        results = list_recent_deaths(self.individuals, self.families)
        self.assertFalse(any("Old Person" in res for res in results))

    def test_no_recent_deaths(self):
        # Mark everyone alive or with old deaths
        self.individuals["@I1@"]["ALIVE"] = True
        self.individuals["@I1@"]["DEATH"] = None
        self.individuals["@I4@"]["DEATH"] = datetime.now() - timedelta(days=200)

        results = list_recent_deaths(self.individuals, self.families)
        self.assertEqual(results, [])

    def test_person_without_family(self):
        # Recent death but no family links
        self.individuals["@I4@"]["DEATH"] = datetime.now() - timedelta(days=5)
        results = list_recent_deaths(self.individuals, self.families)
        self.assertTrue(any("Old Person" in res for res in results))


if __name__ == "__main__":
    unittest.main()
