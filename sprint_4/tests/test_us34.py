import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us34 import list_large_age_differences

class TestUS34AgeDifferences(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_no_large_differences(self):
        gedcom = """0 @I1@ INDI
1 NAME John Smith
1 BIRT
2 DATE 01 JAN 1970
1 FAMS @F1@
0 @I2@ INDI
1 NAME Mary Smith
1 BIRT
2 DATE 01 JAN 1975
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 01 JAN 2000
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_large_age_differences(path)
        os.unlink(path)
        self.assertEqual(len(result), 0)

    def test_exactly_double_age(self):
        gedcom = """0 @I1@ INDI
1 NAME John Elder
1 BIRT
2 DATE 01 JAN 1980
1 FAMS @F1@
0 @I2@ INDI
1 NAME Mary Younger
1 BIRT
2 DATE 01 JAN 1990
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 01 JAN 2010
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_large_age_differences(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)  # Exactly 2x difference should now be flagged
        self.assertIn("John Elder", result[0][1])
        self.assertIn("Mary Younger", result[0][3])

    def test_just_below_double_age(self):
        gedcom = """0 @I1@ INDI
1 NAME John Elder
1 BIRT
2 DATE 01 JAN 1980
1 FAMS @F1@
0 @I2@ INDI
1 NAME Mary Younger
1 BIRT
2 DATE 01 JAN 1991
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 01 JAN 2010
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_large_age_differences(path)
        os.unlink(path)
        self.assertEqual(len(result), 0)  # 1.9x difference should not be flagged

    def test_just_above_double_age(self):
        gedcom = """0 @I1@ INDI
1 NAME John Elder
1 BIRT
2 DATE 01 JAN 1980
1 FAMS @F1@
0 @I2@ INDI
1 NAME Mary Younger
1 BIRT
2 DATE 01 JAN 1989
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 01 JAN 2010
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_large_age_differences(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)  # 2.1x difference should be flagged

    def test_wife_exactly_double_age(self):
        gedcom = """0 @I1@ INDI
1 NAME John Younger
1 BIRT
2 DATE 01 JAN 1990
1 FAMS @F1@
0 @I2@ INDI
1 NAME Mary Elder
1 BIRT
2 DATE 01 JAN 1980
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 01 JAN 2010
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_large_age_differences(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)  # Wife exactly 2x older should be flagged
        self.assertIn("Mary Elder", result[0][1])
        self.assertIn("John Younger", result[0][3])

if __name__ == '__main__':
    unittest.main()