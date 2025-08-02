import unittest
import os
import sys
from datetime import datetime

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from us27 import calculate_age, parse_date, parse_gedcom

class TestUS27(unittest.TestCase):
    
    def test_parse_date_valid(self):
        self.assertEqual(parse_date("15 APR 1990"), datetime(1990, 4, 15))

    def test_parse_date_invalid(self):
        self.assertIsNone(parse_date("32 JAN 1990"))  # Invalid day

    def test_calculate_age_alive(self):
        birth = datetime(2000, 1, 1)
        now = datetime.today()
        expected_age = now.year - birth.year - ((now.month, now.day) < (birth.month, birth.day))
        self.assertEqual(calculate_age(birth), expected_age)

    def test_calculate_age_deceased(self):
        birth = datetime(1950, 5, 20)
        death = datetime(2000, 5, 19)
        self.assertEqual(calculate_age(birth, death), 49)

    def test_parse_gedcom_minimal(self):
        # Create a temporary test GEDCOM file
        temp_file = os.path.join(current_dir, "test_sample.ged")
        with open(temp_file, "w") as f:
            f.write("""0 @I1@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 10 FEB 1980
1 DEAT
2 DATE 15 MAY 2020
""")
        individuals = parse_gedcom(temp_file)
        os.remove(temp_file)  # Clean up

        self.assertIn("I1", individuals)
        self.assertEqual(individuals["I1"]["NAME"], "John /Smith/")
        self.assertEqual(individuals["I1"]["BIRT"], datetime(1980, 2, 10))
        self.assertEqual(individuals["I1"]["DEAT"], datetime(2020, 5, 15))

if __name__ == "__main__":
    unittest.main()
