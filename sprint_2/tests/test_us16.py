import sys
import pytest
from datetime import datetime, timedelta
import tempfile
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us16 import parse_date, extract_last_name, check_male_last_names

def test_parse_date_valid():
    date_str = "25 Dec 2020"
    expected = datetime(2020, 12, 25)
    assert parse_date(date_str) == expected

def test_parse_date_invalid():
    date_str = "31 Feb 2020"
    assert parse_date(date_str) is None

def test_extract_last_name_valid():
    name = "John /Doe/"
    assert extract_last_name(name) == "Doe"

def test_extract_last_name_invalid():
    name = "John Doe"
    assert extract_last_name(name) is None

def test_check_male_last_names_mismatch():
    individuals = {
        "@I1@": {"name": "John /Smith/", "sex": "M"},
        "@I2@": {"name": "James /Brown/", "sex": "M"},
        "@I3@": {"name": "Anna /Smith/", "sex": "F"},
    }
    families = {
        "@F1@": {
            "husband": "@I1@",
            "wife": "@I3@",
            "children": ["@I2@"]
        }
    }
    errors = check_male_last_names(individuals, families)
    assert len(errors) == 1
    assert "James /Brown/" in errors[0]
    assert "John /Smith/" in errors[0]