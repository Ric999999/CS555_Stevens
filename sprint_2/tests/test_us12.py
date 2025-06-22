import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us12 import check_parents_not_too_old

class TestUS12ParentsNotTooOld(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_valid_ages(self):
        gedcom = """0 @I1@ INDI
1 NAME John /Dad/
1 SEX M
1 BIRT
2 DATE 1 JAN 1970
1 FAMS @F1@
0 @I2@ INDI
1 NAME Jane /Mom/
1 SEX F
1 BIRT
2 DATE 1 JAN 1975
1 FAMS @F1@
0 @I3@ INDI
1 NAME Child /Young/
1 SEX M
1 BIRT
2 DATE 1 JAN 2000
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_parents_not_too_old(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_father_too_old(self):
        gedcom = """0 @I1@ INDI
1 NAME Old /Father/
1 SEX M
1 BIRT
2 DATE 1 JAN 1900
1 FAMS @F1@
0 @I2@ INDI
1 NAME Normal /Mother/
1 SEX F
1 BIRT
2 DATE 1 JAN 1970
1 FAMS @F1@
0 @I3@ INDI
1 NAME Child /Junior/
1 SEX M
1 BIRT
2 DATE 1 JAN 2000
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_parents_not_too_old(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("Father", result[0])

    def test_mother_too_old(self):
        gedcom = """0 @I1@ INDI
1 NAME Young /Dad/
1 SEX M
1 BIRT
2 DATE 1 JAN 1960
1 FAMS @F1@
0 @I2@ INDI
1 NAME Old /Mom/
1 SEX F
1 BIRT
2 DATE 1 JAN 1930
1 FAMS @F1@
0 @I3@ INDI
1 NAME Child /Youngest/
1 SEX M
1 BIRT
2 DATE 1 JAN 2000
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_parents_not_too_old(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("Mother", result[0])

    def test_both_parents_too_old(self):
        gedcom = """0 @I1@ INDI
1 NAME Ancient /Dad/
1 SEX M
1 BIRT
2 DATE 1 JAN 1920
1 FAMS @F1@
0 @I2@ INDI
1 NAME Ancient /Mom/
1 SEX F
1 BIRT
2 DATE 1 JAN 1930
1 FAMS @F1@
0 @I3@ INDI
1 NAME Child /Future/
1 SEX M
1 BIRT
2 DATE 1 JAN 2010
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_parents_not_too_old(path)
        os.unlink(path)
        self.assertEqual(len(result), 2)
        self.assertTrue(any("Father" in e for e in result))
        self.assertTrue(any("Mother" in e for e in result))

    def test_missing_birth_dates(self):
        gedcom = """0 @I1@ INDI
1 NAME Unknown /Dad/
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 NAME Unknown /Mom/
1 SEX F
1 FAMS @F1@
0 @I3@ INDI
1 NAME Child /Anon/
1 SEX M
1 BIRT
2 DATE 1 JAN 2000
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_parents_not_too_old(path)
        os.unlink(path)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
