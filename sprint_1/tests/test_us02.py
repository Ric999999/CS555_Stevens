import sys
import os
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from us02 import check_birth_before_marriage


def write_gedcom_file(contents):
    fd, path = tempfile.mkstemp(suffix=".ged")
    with os.fdopen(fd, "w") as tmp:
        tmp.write(contents)
    return path


def test_birth_before_marriage_valid():
    contents = """0 @I1@ INDI
1 BIRT
2 DATE 01 JAN 1980
1 FAMS @F1@
0 @I2@ INDI
1 BIRT
2 DATE 02 FEB 1982
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 03 MAR 2000
"""
    path = write_gedcom_file(contents)
    errors = check_birth_before_marriage(path)
    os.remove(path)
    assert errors == []


def test_birth_after_marriage_invalid():
    contents = """0 @I1@ INDI
1 BIRT
2 DATE 04 APR 2001
1 FAMS @F1@
0 @I2@ INDI
1 BIRT
2 DATE 02 FEB 1982
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 03 MAR 2000
"""
    path = write_gedcom_file(contents)
    errors = check_birth_before_marriage(path)
    os.remove(path)
    assert len(errors) == 1
    assert "HUSB @I1@" in errors[0]


def test_missing_birth_date_skipped():
    contents = """0 @I1@ INDI
1 NAME John /Doe/
1 FAMS @F1@
0 @I2@ INDI
1 BIRT
2 DATE 01 JAN 1980
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 01 JAN 2000
"""
    path = write_gedcom_file(contents)
    errors = check_birth_before_marriage(path)
    os.remove(path)
    assert errors == []


def test_missing_marriage_date_skipped():
    contents = """0 @I1@ INDI
1 BIRT
2 DATE 01 JAN 1970
1 FAMS @F1@
0 @I2@ INDI
1 BIRT
2 DATE 02 FEB 1972
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""
    path = write_gedcom_file(contents)
    errors = check_birth_before_marriage(path)
    os.remove(path)
    assert errors == []


def test_birth_on_marriage_and_other_spouse_after():
    contents = """0 @I1@ INDI
1 BIRT
2 DATE 05 MAY 1990
1 FAMS @F1@
0 @I2@ INDI
1 BIRT
2 DATE 02 FEB 1991
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 05 MAY 1990
"""
    path = write_gedcom_file(contents)
    errors = check_birth_before_marriage(path)
    os.remove(path)
    assert len(errors) == 1
    assert "WIFE @I2@" in errors[0]
    assert "02 Feb 1991" in errors[0]
    assert "05 May 1990" in errors[0]


def test_both_birth_equals_marriage_date():
    contents = """0 @I1@ INDI
1 BIRT
2 DATE 05 MAY 1990
1 FAMS @F1@
0 @I2@ INDI
1 BIRT
2 DATE 05 MAY 1990
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 05 MAY 1990
"""
    path = write_gedcom_file(contents)
    errors = check_birth_before_marriage(path)
    os.remove(path)
    assert errors == []
