import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us32 import list_multiple_births

class TestUS32MultipleBirths(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_no_multiple_births(self):
        gedcom = """0 @I1@ INDI
1 NAME John Doe
1 BIRT
2 DATE 10 JAN 2000
0 @I2@ INDI
1 NAME Jane Doe
1 BIRT
2 DATE 15 JAN 2000
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_multiple_births(path)
        os.unlink(path)
        self.assertEqual(result, [])

    def test_twins(self):
        gedcom = """0 @I1@ INDI
1 NAME Alice
1 BIRT
2 DATE 12 JAN 2001
0 @I2@ INDI
1 NAME Bob
1 BIRT
2 DATE 12 JAN 2001
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_multiple_births(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("multiple births", result[0])
        self.assertIn("@I1@", result[0])
        self.assertIn("@I2@", result[0])

    def test_triplets(self):
        gedcom = """0 @I1@ INDI
1 NAME Triplet1
1 BIRT
2 DATE 01 MAR 1999
0 @I2@ INDI
1 NAME Triplet2
1 BIRT
2 DATE 01 MAR 1999
0 @I3@ INDI
1 NAME Triplet3
1 BIRT
2 DATE 01 MAR 1999
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_multiple_births(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("@I1@", result[0])
        self.assertIn("@I2@", result[0])
        self.assertIn("@I3@", result[0])

    def test_across_multiple_families(self):
        gedcom = """0 @I1@ INDI
1 NAME Tom
1 BIRT
2 DATE 01 APR 2010
0 @I2@ INDI
1 NAME Tim
1 BIRT
2 DATE 01 APR 2010
0 @F1@ FAM
1 CHIL @I1@
0 @F2@ FAM
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_multiple_births(path)
        os.unlink(path)
        # Should NOT report as multiple birth: different families
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
