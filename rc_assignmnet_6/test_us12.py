# import us12  # IMPORTANT: Smelly version
import us12_refactored as us12

def test_parents_not_too_old():
    errors = us12.check_parents_not_too_old("test_data.ged")
    assert any("Father" in e for e in errors)
    assert any("Mother" in e for e in errors)

def test_pass_case(tmp_path):
    content = """0 @I1@ INDI
1 NAME John /Doe/
1 SEX M
1 BIRT
2 DATE 01 JAN 1950
0 @I2@ INDI
1 NAME Jane /Smith/
1 SEX F
1 BIRT
2 DATE 01 JAN 1955
0 @I3@ INDI
1 NAME Baby /Doe/
1 SEX M
1 BIRT
2 DATE 01 JAN 1980
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
    test_file = tmp_path / "pass_case.ged"
    test_file.write_text(content)
    errors = us12.check_parents_not_too_old(str(test_file))
    assert not errors
