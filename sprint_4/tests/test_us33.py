import unittest
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us33 import list_orphans

class TestUS33Orphans(unittest.TestCase):

    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_no_orphans(self):
        gedcom = """0 @I1@ INDI
1 NAME Parent 1
1 SEX M
1 DEAT
2 DATE 01 JAN 2020
1 FAMS @F1@
0 @I2@ INDI
1 NAME Parent 2
1 SEX F
1 DEAT
2 DATE 01 JAN 2020
1 FAMS @F1@
0 @I3@ INDI
1 NAME Adult Child
1 BIRT
2 DATE 01 JAN 2000
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_orphans(path)
        os.unlink(path)
        self.assertEqual(len(result), 0)

    def test_single_orphan(self):
        gedcom = """0 @I1@ INDI
1 NAME Parent 1
1 SEX M
1 DEAT
2 DATE 01 JAN 2020
1 FAMS @F1@
0 @I2@ INDI
1 NAME Parent 2
1 SEX F
1 DEAT
2 DATE 01 JAN 2020
1 FAMS @F1@
0 @I3@ INDI
1 NAME Child
1 BIRT
2 DATE 01 JAN 2010
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_orphans(path)
        os.unlink(path)
        self.assertEqual(len(result), 1)
        self.assertIn("Child", result[0][1])

    def test_missing_parent_death(self):
        gedcom = """0 @I1@ INDI
1 NAME Parent 1
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 NAME Parent 2
1 SEX F
1 DEAT
2 DATE 01 JAN 2020
1 FAMS @F1@
0 @I3@ INDI
1 NAME Child
1 BIRT
2 DATE 01 JAN 2010
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_orphans(path)
        os.unlink(path)
        self.assertEqual(len(result), 0)

    def test_multiple_orphans(self):
        gedcom = """0 @I1@ INDI
1 NAME Parent 1
1 SEX M
1 DEAT
2 DATE 01 JAN 2020
1 FAMS @F1@
0 @I2@ INDI
1 NAME Parent 2
1 SEX F
1 DEAT
2 DATE 01 JAN 2020
1 FAMS @F1@
0 @I3@ INDI
1 NAME Child 1
1 BIRT
2 DATE 01 JAN 2010
1 FAMC @F1@
0 @I4@ INDI
1 NAME Child 2
1 BIRT
2 DATE 01 JAN 2015
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
1 CHIL @I4@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_orphans(path)
        os.unlink(path)
        self.assertEqual(len(result), 2)
        self.assertTrue(any("Child 1" in o[1] for o in result))
        self.assertTrue(any("Child 2" in o[1] for o in result))

    def test_adult_child(self):
        gedcom = """0 @I1@ INDI
1 NAME Parent 1
1 SEX M
1 DEAT
2 DATE 01 JAN 2000
1 FAMS @F1@
0 @I2@ INDI
1 NAME Parent 2
1 SEX F
1 DEAT
2 DATE 01 JAN 2000
1 FAMS @F1@
0 @I3@ INDI
1 NAME Adult Child
1 BIRT
2 DATE 01 JAN 2000
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(gedcom)
        result = list_orphans(path)
        os.unlink(path)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()