import sys
from datetime import datetime, timedelta
import tempfile
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us36 import parse_date, parse_gedcom_file, list_recent_deaths, write_output

def test_parse_date_valid():
    assert parse_date("25 Jun 2025") == datetime(2025, 6, 25)

def test_parse_date_invalid():
    assert parse_date("Invalid Date") is None

def test_parse_gedcom_file_parses_death_date_correctly():
    gedcom_content = """0 @I1@ INDI
1 NAME Jane Doe
1 SEX F
1 DEAT
2 DATE 20 Jun 2025
"""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as tmp:
        tmp.write(gedcom_content)
        temp_path = tmp.name

    individuals = parse_gedcom_file(temp_path)
    os.unlink(temp_path)

    assert "@I1@" in individuals
    assert individuals["@I1@"]["name"] == "Jane Doe"
    assert individuals["@I1@"]["sex"] == "F"
    assert individuals["@I1@"]["death"] == datetime(2025, 6, 20)

def test_list_recent_deaths_detects_recent_death():
    recent_date = datetime.today() - timedelta(days=5)
    individuals = {
        "@I1@": {
            "name": "John Doe",
            "death": recent_date
        }
    }
    results = list_recent_deaths(individuals)
    assert len(results) == 1
    assert "John Doe" in results[0]

def test_write_output_creates_expected_file(tmp_path):
    test_data = ["US36: RECENT DEATH: Jane Doe (@I1@) died on 01 Jun 2025"]
    output_file = tmp_path / "test_output.txt"
    write_output(test_data, str(output_file))

    assert output_file.exists()
    with open(output_file, "r") as f:
        content = f.read().strip()
        assert "Jane Doe" in content
