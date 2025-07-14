import unittest
import tempfile
import os
from us25 import check_unique_child_name_and_birth

class TestUS25(unittest.TestCase):
    def write_temp_gedcom(self, content):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ged", mode="w")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_realistic_family_passes(self):
        content = """0 I01 INDI
1 NAME Juan /Valdez/
1 SEX M
1 BIRT
2 DATE 15 MAY 1940
1 DEAT
2 DATE 10 JUN 2005
1 FAMS F10
0 I02 INDI
1 NAME Maria /Jimenez/
1 SEX F
1 BIRT
2 DATE 20 AUG 1945
1 DEAT
2 DATE 5 MAR 1990
1 FAMS F10
1 FAMS F20
0 I03 INDI
1 NAME Roberto /Valdez/
1 SEX M
1 BIRT
2 DATE 12 JUL 1970
1 FAMC F10
1 FAMS F30
0 I04 INDI
1 NAME Susana /Valdez/
1 SEX F
1 BIRT
2 DATE 18 NOV 1972
1 FAMC F10
0 I05 INDI
1 NAME James /Wilson/
1 SEX M
1 BIRT
2 DATE 3 FEB 1950
1 FAMS F20
0 I06 INDI
1 NAME David /Valdez/
1 SEX M
1 BIRT
2 DATE 5 APR 1995
1 FAMC F30
0 I07 INDI
1 NAME Emily /Valdez/
1 SEX F
1 BIRT
2 DATE 8 SEP 1997
1 FAMC F30
0 I08 INDI
1 NAME Sarah /Wilson/
1 SEX F
1 BIRT
2 DATE 14 DEC 1992
1 FAMC F20
0 I09 INDI
1 NAME Linda /Brown/
1 SEX F
1 BIRT
2 DATE 22 MAR 1975
1 FAMS F30
0 F10 FAM
1 HUSB I01
1 WIFE I02
1 CHIL I03
1 CHIL I04
0 F20 FAM
1 HUSB I05
1 WIFE I02
1 CHIL I08
0 F30 FAM
1 HUSB I03
1 WIFE I09
1 CHIL I06
1 CHIL I07
"""
        path = self.write_temp_gedcom(content)
        result = check_unique_child_name_and_birth(path)
        os.remove(path)
        self.assertEqual(result, [])

    def test_duplicate_in_one_family_fails(self):
        content = """0 @I1@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 01 JAN 2000
0 @I2@ INDI
1 NAME John /Smith/
1 BIRT
2 DATE 01 JAN 2000
0 @I3@ INDI
1 NAME Jane /Smith/
1 BIRT
2 DATE 05 MAY 2005
0 @F1@ FAM
1 CHIL @I1@
1 CHIL @I2@
1 CHIL @I3@
"""
        path = self.write_temp_gedcom(content)
        result = check_unique_child_name_and_birth(path)
        os.remove(path)
        self.assertEqual(len(result), 1)
        self.assertIn("ERROR: US25", result[0])

    def test_same_name_different_families_pass(self):
        content = """0 @I1@ INDI
1 NAME Chris /Lee/
1 BIRT
2 DATE 10 OCT 2010
0 @I2@ INDI
1 NAME Chris /Lee/
1 BIRT
2 DATE 10 OCT 2010
0 @F1@ FAM
1 CHIL @I1@
0 @F2@ FAM
1 CHIL @I2@
"""
        path = self.write_temp_gedcom(content)
        result = check_unique_child_name_and_birth(path)
        os.remove(path)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()