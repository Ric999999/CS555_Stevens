import os
import pytest
from io import StringIO
from unittest.mock import patch, mock_open
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us15 import process_gedcom


@pytest.fixture
def gedcom_data_small_family():
    return """0 F1 FAM
1 HUSB John Smith
1 WIFE Jane Doe
1 CHIL Child1
1 CHIL Child2
"""


@pytest.fixture
def gedcom_data_large_family():
    return """0 F1 FAM
1 HUSB John Smith
1 WIFE Jane Doe
""" + "\n".join([f"1 CHIL Child{i}" for i in range(16)]) + "\n"


@pytest.fixture
def gedcom_data_multiple_families():
    return """0 F1 FAM
1 HUSB John Smith
1 WIFE Jane Doe
1 CHIL Child1
1 CHIL Child2

0 F2 FAM
1 HUSB Bob Johnson
1 WIFE Alice Brown
""" + "\n".join([f"1 CHIL Kid{i}" for i in range(20)]) + "\n"


def test_process_gedcom_with_small_family(capsys, gedcom_data_small_family):
    """Test with a family that has fewer than 15 children (should pass)"""
    with patch("builtins.open", mock_open(read_data=gedcom_data_small_family)):
        process_gedcom("dummy.ged")

        # Check output file was created with PASSED message
        assert os.path.exists("us15_output.txt")
        with open("us15_output.txt", "r") as f:
            content = f.read()
            assert "PASSED: US15: Number of Siblings <= 15" in content

        # Check no error was printed to stdout
        captured = capsys.readouterr()
        assert "Error: US15" not in captured.out


def test_process_gedcom_with_large_family(capsys, gedcom_data_large_family):
    """Test with a family that has 16 children (should fail)"""
    with patch("builtins.open", mock_open(read_data=gedcom_data_large_family)):
        process_gedcom("dummy.ged")

        # Check output file was NOT created
        assert not os.path.exists("us15_output.txt")

        # Check error was printed to stdout
        captured = capsys.readouterr()
        assert "Error: US15" in captured.out
        assert "has 16 siblings" in captured.out
        assert "John Smith and Jane Doe" in captured.out


def test_process_gedcom_with_multiple_families(capsys, gedcom_data_multiple_families):
    """Test with multiple families where one has too many children"""
    with patch("builtins.open", mock_open(read_data=gedcom_data_multiple_families)):
        process_gedcom("dummy.ged")

        # Check output file was NOT created (since one family failed)
        assert not os.path.exists("us15_output.txt")

        # Check error was printed for the correct family
        captured = capsys.readouterr()
        assert "Error: US15" in captured.out
        assert "Bob Johnson and Alice Brown" in captured.out
        assert "has 20 siblings" in captured.out
        # Make sure the small family wasn't mentioned in errors
        assert "John Smith" not in captured.out
        assert "Jane Doe" not in captured.out


def test_process_gedcom_with_empty_file(capsys):
    """Test with an empty GEDCOM file"""
    with patch("builtins.open", mock_open(read_data="")):
        process_gedcom("empty.ged")

        # Check output file was created with PASSED message
        assert os.path.exists("us15_output.txt")
        with open("us15_output.txt", "r") as f:
            content = f.read()
            assert "PASSED: US15: Number of Siblings <= 15" in content

        # Check no error was printed to stdout
        captured = capsys.readouterr()
        assert "Error: US15" not in captured.out


def test_process_gedcom_with_missing_file():
    """Test with a non-existent GEDCOM file"""
    with pytest.raises(FileNotFoundError):
        process_gedcom("nonexistent.ged")


def test_output_file_cleanup():
    """Clean up any output files created during testing"""
    if os.path.exists("us15_output.txt"):
        os.remove("us15_output.txt")