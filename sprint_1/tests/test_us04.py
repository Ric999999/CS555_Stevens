import os
from datetime import datetime
from io import StringIO
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from us04 import parse_date, process_gedcom


def test_parse_date_valid():
    """Test that parse_date correctly parses valid dates"""
    date_str = "15 MAR 1990"
    result = parse_date(date_str)
    assert result == datetime(1990, 3, 15)


def test_process_gedcom_valid_sequence(tmp_path, monkeypatch):
    """Test that valid marriage-divorce sequence produces no errors"""
    gedcom_content = """
    0 @F1@ FAM
    1 MARR
    2 DATE 01 JAN 1990
    1 DIV
    2 DATE 01 JAN 2000
    """
    test_file = tmp_path / "valid.ged"
    test_file.write_text(gedcom_content)

    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)

    process_gedcom(str(test_file))

    assert "Error:" not in captured_output.getvalue()
    assert os.path.exists("us04_output.txt")
    with open("us04_output.txt") as f:
        assert "PASSED: US04: All Marriages before Divorce." in f.read()


def test_process_gedcom_invalid_sequence(tmp_path, monkeypatch):
    """Test that invalid divorce before marriage produces error"""
    gedcom_content = """
    0 @F1@ FAM
    1 MARR
    2 DATE 01 JAN 2000
    1 DIV
    2 DATE 01 JAN 1990
    """
    test_file = tmp_path / "invalid.ged"
    test_file.write_text(gedcom_content)

    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)

    process_gedcom(str(test_file))

    output = captured_output.getvalue()
    assert "Error:" in output
    assert "Divorce on 01 Jan 1990" in output
    assert "before marriage on 01 Jan 2000" in output
    assert not os.path.exists("us04_output.txt")


def test_process_gedcom_marriage_only(tmp_path, monkeypatch):
    """Test with marriage date but no divorce date"""
    gedcom_content = """
    0 @F1@ FAM
    1 MARR
    2 DATE 01 JAN 1990
    """
    test_file = tmp_path / "marriage_only.ged"
    test_file.write_text(gedcom_content)

    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)

    process_gedcom(str(test_file))

    assert "Error:" not in captured_output.getvalue()
    assert os.path.exists("us04_output.txt")
    with open("us04_output.txt") as f:
        assert "PASSED: US04: All Marriages before Divorce." in f.read()


def test_process_gedcom_multiple_families(tmp_path, monkeypatch):
    """Test with multiple families including valid and invalid cases"""
    gedcom_content = """
    0 @F1@ FAM
    1 MARR
    2 DATE 01 JAN 1980
    1 DIV
    2 DATE 01 JAN 1990

    0 @F2@ FAM
    1 MARR
    2 DATE 01 JAN 2000
    1 DIV
    2 DATE 01 JAN 1990
    """
    test_file = tmp_path / "mixed.ged"
    test_file.write_text(gedcom_content)

    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)

    process_gedcom(str(test_file))

    output = captured_output.getvalue()
    assert "Error:" in output
    assert "@F2" in output  # The invalid family
    assert "Divorce on 01 Jan 1990" in output
    assert "before marriage on 01 Jan 2000" in output
    assert not os.path.exists("us04_output.txt")


@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists("us04_output.txt"):
        os.remove("us04_output.txt")