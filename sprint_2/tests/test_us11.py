import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us11 import check_no_bigamy

class TestUS11NoBigamy(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_no_bigamy_single_marriage(self):
        gedcom = """0 @I1@ INDI
1 NAME John /Doe/
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 NAME Jane /Smith/
1 SEX F
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 10 JAN 1990
1 DIV
2 DATE 10 JAN 2000
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_no_bigamy(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_bigamy_two_marriages_overlap(self):
        gedcom = """0 @I1@ INDI
1 NAME John /Doe/
1 SEX M
1 FAMS @F1@
1 FAMS @F2@
0 @I2@ INDI
1 NAME Alice /Brown/
1 SEX F
1 FAMS @F1@
0 @I3@ INDI
1 NAME Clara /Jones/
1 SEX F
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 10 JAN 1990
1 DIV
2 DATE 10 JAN 2000
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I3@
1 MARR
2 DATE 1 JAN 1999
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_no_bigamy(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("overlapping marriages", result[0])

    def test_bigamy_no_divorce(self):
        gedcom = """0 @I1@ INDI
1 NAME John /Doe/
1 SEX M
1 FAMS @F1@
1 FAMS @F2@
0 @I2@ INDI
1 NAME Anna /Lee/
1 SEX F
1 FAMS @F1@
0 @I3@ INDI
1 NAME Eve /White/
1 SEX F
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 1 JAN 1990
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I3@
1 MARR
2 DATE 1 JAN 2000
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_no_bigamy(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)

    def test_no_bigamy_divorced_then_remarried(self):
        gedcom = """0 @I1@ INDI
1 NAME Mark /Stone/
1 SEX M
1 FAMS @F1@
1 FAMS @F2@
0 @I2@ INDI
1 NAME Linda /Rose/
1 SEX F
1 FAMS @F1@
0 @I3@ INDI
1 NAME Holly /Moore/
1 SEX F
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 10 MAR 1980
1 DIV
2 DATE 10 MAR 1990
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I3@
1 MARR
2 DATE 11 MAR 1990
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_no_bigamy(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_multiple_families_no_overlap(self):
        gedcom = """0 @I1@ INDI
1 NAME Robert /Hill/
1 SEX M
1 FAMS @F1@
1 FAMS @F2@
1 FAMS @F3@
0 @I2@ INDI
1 NAME Wife1 /Test/
1 SEX F
1 FAMS @F1@
0 @I3@ INDI
1 NAME Wife2 /Test/
1 SEX F
1 FAMS @F2@
0 @I4@ INDI
1 NAME Wife3 /Test/
1 SEX F
1 FAMS @F3@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 1 JAN 1970
1 DIV
2 DATE 1 JAN 1980
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I3@
1 MARR
2 DATE 1 JAN 1981
1 DIV
2 DATE 1 JAN 1990
0 @F3@ FAM
1 HUSB @I1@
1 WIFE @I4@
1 MARR
2 DATE 1 JAN 1992
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_no_bigamy(path)
        os.unlink(path)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
