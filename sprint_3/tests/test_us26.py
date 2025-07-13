import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us26 import check_family_roles_consistency

class TestUS26FamilyRoleConsistency(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_all_roles_specified(self):
        gedcom = """0 @I1@ INDI
1 FAMS @F1@
0 @I2@ INDI
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_family_roles_consistency(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_missing_fams_for_husband(self):
        gedcom = """0 @I1@ INDI
0 @F1@ FAM
1 HUSB @I1@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_family_roles_consistency(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("HUSB", result[0])

    def test_missing_famc_for_child(self):
        gedcom = """0 @I2@ INDI
0 @F1@ FAM
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_family_roles_consistency(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("Child", result[0])

    def test_missing_both_links(self):
        gedcom = """0 @I1@ INDI
0 @I2@ INDI
0 @F1@ FAM
1 HUSB @I1@
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_family_roles_consistency(path)
        os.unlink(path)
        self.assertEqual(len(result), 2)
        self.assertTrue(any("HUSB" in e for e in result))
        self.assertTrue(any("Child" in e for e in result))

    def test_roles_specified_but_not_used(self):
        gedcom = """0 @I1@ INDI
1 FAMS @F1@
0 @I2@ INDI
1 FAMC @F1@
0 @F1@ FAM
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_family_roles_consistency(path)
        os.unlink(path)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
