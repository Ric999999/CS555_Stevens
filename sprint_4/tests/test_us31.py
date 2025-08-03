import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us31 import list_living_singles

class TestUS31LivingSingles(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_no_singles(self):
        gedcom = """0 @I1@ INDI
1 NAME John Doe
1 SEX M
1 BIRT
2 DATE 10 JAN 1990
1 FAMS @F1@
1 DEAT
2 DATE 12 FEB 2020
0 @I2@ INDI
1 NAME Jane Doe
1 SEX F
1 BIRT
2 DATE 15 MAR 1992
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_living_singles(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_one_living_single(self):
        gedcom = """0 @I1@ INDI
1 NAME Solo Person
1 SEX M
1 BIRT
2 DATE 01 JAN 2000
0 @I2@ INDI
1 NAME Married Person
1 SEX F
1 BIRT
2 DATE 01 JAN 2000
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_living_singles(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("@I1@", result[0])
        self.assertIn("Solo Person", result[0])

    def test_multiple_living_singles(self):
        gedcom = """0 @I1@ INDI
1 NAME Alice
1 SEX F
1 BIRT
2 DATE 10 OCT 1995
0 @I2@ INDI
1 NAME Bob
1 SEX M
1 BIRT
2 DATE 20 NOV 1990
0 @I3@ INDI
1 NAME Carol
1 SEX F
1 BIRT
2 DATE 05 MAY 1985
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_living_singles(path)
        os.unlink(path)
        self.assertEqual(len(result), 2)
        self.assertTrue(any("Alice" in r for r in result))
        self.assertTrue(any("Bob" in r for r in result))

    def test_dead_unmarried_not_included(self):
        gedcom = """0 @I1@ INDI
1 NAME Ghost Person
1 SEX M
1 BIRT
2 DATE 01 JAN 1900
1 DEAT
2 DATE 01 JAN 2000
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_living_singles(path)
        os.unlink(path)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
