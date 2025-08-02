import unittest
import os
import sys
from datetime import datetime

# Add parent directory (sprint_3) to the import path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from us28 import parse_date, calculate_age, parse_gedcom

class TestUS28(unittest.TestCase):

    def test_parse_valid_date(self):
        self.assertEqual(parse_date("15 APR 1990"), datetime(1990, 4, 15))

    def test_parse_invalid_date(self):
        self.assertIsNone(parse_date("31 FEB 1990"))

    def test_calculate_age(self):
        birth = datetime(2000, 5, 20)
        today = datetime.today()
        expected_age = today.year - 2000 - ((today.month, today.day) < (5, 20))
        self.assertEqual(calculate_age(birth), expected_age)

    def test_sort_siblings_by_age(self):
        # Create a sample GEDCOM with two siblings
        gedcom_data = """0 @I1@ INDI
1 NAME Alice /Test/
1 BIRT
2 DATE 15 APR 1995
0 @I2@ INDI
1 NAME Bob /Test/
1 BIRT
2 DATE 20 FEB 1990
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@"""

        file_path = os.path.join(current_dir, "us28_sample.ged")
        with open(file_path, "w") as f:
            f.write(gedcom_data)

        individuals, families = parse_gedcom(file_path)
        os.remove(file_path)

        self.assertIn("I1", individuals)
        self.assertIn("I2", individuals)
        self.assertIn("F1", families)
        self.assertEqual(set(families["F1"]["CHIL"]), {"I1", "I2"})

        # Bob should be older than Alice
        bob_age = calculate_age(individuals["I2"]["BIRT"])
        alice_age = calculate_age(individuals["I1"]["BIRT"])
        self.assertGreater(bob_age, alice_age)

    def test_missing_birth_date(self):
        gedcom_data = """0 @I1@ INDI
1 NAME Jane /NoBirth/
0 @F1@ FAM
1 CHIL @I1@"""

        file_path = os.path.join(current_dir, "us28_nobirth.ged")
        with open(file_path, "w") as f:
            f.write(gedcom_data)

        individuals, families = parse_gedcom(file_path)
        os.remove(file_path)

        self.assertIn("I1", individuals)
        self.assertIsNone(individuals["I1"]["BIRT"])

    def test_single_child_family(self):
        gedcom_data = """0 @I1@ INDI
1 NAME Only /Child/
1 BIRT
2 DATE 10 JAN 2000
0 @F1@ FAM
1 CHIL @I1@"""

        file_path = os.path.join(current_dir, "us28_singlechild.ged")
        with open(file_path, "w") as f:
            f.write(gedcom_data)

        individuals, families = parse_gedcom(file_path)
        os.remove(file_path)

        self.assertEqual(len(families["F1"]["CHIL"]), 1)
        self.assertIn("I1", individuals)

    def test_multiple_families(self):
        gedcom_data = """0 @I1@ INDI
1 NAME Child /One/
1 BIRT
2 DATE 10 JAN 1990
0 @I2@ INDI
1 NAME Child /Two/
1 BIRT
2 DATE 10 JAN 1992
0 @I3@ INDI
1 NAME Child /Three/
1 BIRT
2 DATE 10 JAN 1988
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@
0 @F2@ FAM
1 CHIL @I3@"""

        file_path = os.path.join(current_dir, "us28_multifam.ged")
        with open(file_path, "w") as f:
            f.write(gedcom_data)

        individuals, families = parse_gedcom(file_path)
        os.remove(file_path)

        self.assertEqual(set(families["F1"]["CHIL"]), {"I1", "I2"})
        self.assertEqual(families["F2"]["CHIL"], ["I3"])
        self.assertEqual(len(individuals), 3)

if __name__ == "__main__":
    unittest.main()
