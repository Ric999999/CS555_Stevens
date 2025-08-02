import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us22 import check_unique_ids

class TestUS22UniqueIDs(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_unique_ids(self):
        gedcom = """0 @I1@ INDI
1 SEX M
0 @I2@ INDI
1 SEX F
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_ids(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_duplicate_individual_ids(self):
        gedcom = """0 @I1@ INDI
1 SEX M
0 @I1@ INDI
1 SEX F
0 @F1@ FAM
1 HUSB @I1@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_ids(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("Duplicate individual ID", result[0])

    def test_duplicate_family_ids(self):
        gedcom = """0 @I1@ INDI
1 SEX M
0 @F1@ FAM
1 HUSB @I1@
0 @F1@ FAM
1 HUSB @I1@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_ids(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("Duplicate family ID", result[0])

    def test_multiple_duplicates(self):
        gedcom = """0 @I1@ INDI
1 SEX M
0 @I1@ INDI
1 SEX F
0 @F1@ FAM
1 HUSB @I1@
0 @F1@ FAM
1 HUSB @I1@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_ids(path)
        os.unlink(path)
        self.assertEqual(len(result), 2)
        self.assertTrue(any("Duplicate individual ID" in e for e in result))
        self.assertTrue(any("Duplicate family ID" in e for e in result))

    def test_empty_file(self):
        gedcom = ""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_ids(path)
        os.unlink(path)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
