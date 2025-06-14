import os
from datetime import datetime
from io import StringIO
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from us03 import parse_date, process_gedcom

def test_parse_date_valid():
    """Test that parse_date correctly parses valid dates"""
    date_str = "15 MAR 1990"
    result = parse_date(date_str)
    assert result == datetime(1990, 3, 15)


def test_parse_date_invalid():
    """Test that parse_date returns None for invalid dates"""
    date_str = "31 FEB 2000"  # Invalid date
    result = parse_date(date_str)
    assert result is None


def test_process_gedcom_valid_sequence(tmp_path, monkeypatch):
    """Test that valid birth-death sequence produces no errors"""
    gedcom_content = """
    0 @I1@ INDI
    1 NAME John Doe
    1 BIRT
    2 DATE 01 JAN 1950
    1 DEAT
    2 DATE 01 JAN 2000
    """
    test_file = tmp_path / "valid.ged"
    test_file.write_text(gedcom_content)

    # Mock print to capture output
    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)

    process_gedcom(str(test_file))

    # Check no errors were printed
    assert "Error:" not in captured_output.getvalue()
    # Check output file was created with success message
    assert os.path.exists("us03_output.txt")
    with open("us03_output.txt") as f:
        assert "PASSED: US03: All Births before Death." in f.read()


def test_process_gedcom_invalid_sequence(tmp_path, monkeypatch):
    """Test that invalid birth-death sequence produces error"""
    gedcom_content = """
    0 @I1@ INDI
    1 NAME John Doe
    1 BIRT
    2 DATE 01 JAN 2000
    1 DEAT
    2 DATE 01 JAN 1990
    """
    test_file = tmp_path / "invalid.ged"
    test_file.write_text(gedcom_content)

    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)

    process_gedcom(str(test_file))

    # Check error was printed
    output = captured_output.getvalue()
    assert "Error:" in output
    assert "Born: 01 Jan 2000" in output
    assert "Died: 01 Jan 1990" in output
    # Check output file was not created
    assert not os.path.exists("us03_output.txt")


def test_process_gedcom_multiple_individuals(tmp_path, monkeypatch):
    """Test with multiple individuals including valid and invalid cases"""
    gedcom_content = """
    0 @I1@ INDI
    1 NAME Valid Person
    1 BIRT
    2 DATE 01 JAN 1960
    1 DEAT
    2 DATE 01 JAN 2020

    0 @I2@ INDI
    1 NAME Invalid Person
    1 BIRT
    2 DATE 01 JAN 2000
    1 DEAT
    2 DATE 01 JAN 1990
    """
    test_file = tmp_path / "mixed.ged"
    test_file.write_text(gedcom_content)

    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)

    process_gedcom(str(test_file))

    # Check error was printed for invalid case
    output = captured_output.getvalue()
    assert "Error:" in output
    assert "Invalid Person" in output
    assert "Born: 01 Jan 2000" in output
    assert "Died: 01 Jan 1990" in output
    assert not os.path.exists("us03_output.txt")


@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists("us03_output.txt"):
        os.remove("us03_output.txt")