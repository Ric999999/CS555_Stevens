import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us21 import check_gender_for_roles

class TestUS21GenderRoles(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_correct_genders(self):
        gedcom = """0 @I1@ INDI
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 SEX F
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_gender_for_roles(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_husband_wrong_gender(self):
        gedcom = """0 @I1@ INDI
1 SEX F
1 FAMS @F1@
0 @I2@ INDI
1 SEX F
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_gender_for_roles(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("Husband", result[0])

    def test_wife_wrong_gender(self):
        gedcom = """0 @I1@ INDI
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 SEX M
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_gender_for_roles(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("Wife", result[0])

    def test_both_wrong_genders(self):
        gedcom = """0 @I1@ INDI
1 SEX F
1 FAMS @F1@
0 @I2@ INDI
1 SEX M
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_gender_for_roles(path)
        os.unlink(path)
        self.assertEqual(len(result), 2)
        self.assertTrue(any("Husband" in e for e in result))
        self.assertTrue(any("Wife" in e for e in result))

    def test_missing_sex(self):
        gedcom = """0 @I1@ INDI
1 FAMS @F1@
0 @I2@ INDI
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_gender_for_roles(path)
        os.unlink(path)
        # None of them are explicitly the wrong gender, should still flag both
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
