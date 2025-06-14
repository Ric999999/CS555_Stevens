import os
import sys
from datetime import datetime
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from us06 import parse_date, check_divorce_before_death

def test_parse_date_valid():
    assert parse_date("14 JUN 2020") == datetime(2020, 6, 14)

def test_parse_date_invalid():
    assert parse_date("2020-06-14") is None

def test_divorce_before_death_valid():
    individuals = {
        "@I1@": {"death": datetime(2025, 1, 1)},
        "@I2@": {"death": datetime(2026, 1, 1)},
    }
    families = {
        "@F1@": {
            "husband": "@I1@",
            "wife": "@I2@",
            "divorced": datetime(2020, 1, 1),
        }
    }
    errors = check_divorce_before_death(individuals, families)
    assert errors == []

def test_divorce_after_husband_death():
    individuals = {
        "@I1@": {"death": datetime(2020, 1, 1)},
        "@I2@": {"death": datetime(2026, 1, 1)},
    }
    families = {
        "@F1@": {
            "husband": "@I1@",
            "wife": "@I2@",
            "divorced": datetime(2021, 1, 1),
        }
    }
    errors = check_divorce_before_death(individuals, families)
    assert any("after husband's" in err for err in errors)

def test_divorce_after_wife_death():
    individuals = {
        "@I1@": {"death": datetime(2026, 1, 1)},
        "@I2@": {"death": datetime(2020, 1, 1)},
    }
    families = {
        "@F1@": {
            "husband": "@I1@",
            "wife": "@I2@",
            "divorced": datetime(2021, 1, 1),
        }
    }
    errors = check_divorce_before_death(individuals, families)
    assert any("after wife's" in err for err in errors)
