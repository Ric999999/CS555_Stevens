import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us25 import check_unique_child_name_and_birth

class TestUS25UniqueChildNameBirth(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_no_duplicates(self):
        gedcom = """0 @I1@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 01 JAN 2000
0 @I2@ INDI
1 NAME Jane /Smith/
1 BIRT
2 DATE 01 JAN 2000
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_child_name_and_birth(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_duplicate_name_and_birth(self):
        gedcom = """0 @I1@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 01 JAN 2000
0 @I2@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 01 JAN 2000
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_child_name_and_birth(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("ERROR: US25", result[0])

    def test_duplicate_name_different_birth(self):
        gedcom = """0 @I1@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 01 JAN 2000
0 @I2@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 02 JAN 2000
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_child_name_and_birth(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_duplicate_in_different_families(self):
        gedcom = """0 @I1@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 01 JAN 2000
0 @I2@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 01 JAN 2000
0 @F1@ FAM
1 CHIL @I1@
0 @F2@ FAM
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_child_name_and_birth(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_missing_birth_date(self):
        gedcom = """0 @I1@ INDI
1 NAME John /Smith/
0 @I2@ INDI
1 NAME John /Smith/
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = check_unique_child_name_and_birth(path)
        os.unlink(path)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
