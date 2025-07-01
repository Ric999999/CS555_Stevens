import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us24 import process_gedcom, normalize_name

def test_normalize_name():
    """Test name normalization handles different formats"""
    assert normalize_name("John /Doe/") == "john doe"
    assert normalize_name("  Jane  /Smith/  ") == "jane smith"
    assert normalize_name("UNKNOWN") is None
    assert normalize_name("Unknown Person") == "unknown person"

def test_unique_spouse_pairs(tmp_path):
    """Test families with unique spouse pairs pass validation"""
    gedcom = """
0 I1 INDI
1 NAME John /Doe/
0 I2 INDI
1 NAME Jane /Smith/
0 I3 INDI
1 NAME Bob /Johnson/
0 I4 INDI
1 NAME Alice /Williams/
0 F1 FAM
1 HUSB I1
1 WIFE I2
0 F2 FAM
1 HUSB I3
1 WIFE I4
"""
    test_file = os.path.join(tmp_path, "test.ged")
    with open(test_file, "w") as f:
        f.write(gedcom)
    assert process_gedcom(test_file, test_mode=True) is True
    assert os.path.exists("us24_output.txt")

def test_unknown_spouses_ignored(tmp_path):
    """Test families with unknown spouses are ignored"""
    gedcom = """
0 I1 INDI
1 NAME John /Doe/
0 I2 INDI
1 NAME Unknown
0 F1 FAM
1 HUSB I1
1 WIFE I2
0 F2 FAM
1 HUSB I1
1 WIFE I2
"""
    test_file = os.path.join(tmp_path, "test.ged")
    with open(test_file, "w") as f:
        f.write(gedcom)
    assert process_gedcom(test_file, test_mode=True) is True

@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists("us24_output.txt"):
        os.remove("us24_output.txt")