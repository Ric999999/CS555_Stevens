import os
import sys
import pytest
from datetime import datetime

# Ensure the module can be imported from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from us05 import check_marriage_before_death  # Replace 'us05' with your actual filename

def test_marriage_before_death_valid():
    individuals = {
        "@I1@": {"death": datetime(2025, 5, 10)},
        "@I2@": {"death": datetime(2026, 7, 15)},
    }
    families = {
        "@F1@": {
            "husband": "@I1@",
            "wife": "@I2@",
            "married": datetime(2020, 6, 1),
        }
    }
    errors = check_marriage_before_death(individuals, families)
    assert errors == []

def test_marriage_after_husband_death():
    individuals = {
        "@I1@": {"death": datetime(2019, 5, 10)},
        "@I2@": {"death": datetime(2026, 7, 15)},
    }
    families = {
        "@F1@": {
            "husband": "@I1@",
            "wife": "@I2@",
            "married": datetime(2020, 6, 1),
        }
    }
    errors = check_marriage_before_death(individuals, families)
    assert any("after husband's" in err for err in errors)

def test_marriage_after_wife_death():
    individuals = {
        "@I1@": {"death": datetime(2026, 5, 10)},
        "@I2@": {"death": datetime(2019, 1, 1)},
    }
    families = {
        "@F1@": {
            "husband": "@I1@",
            "wife": "@I2@",
            "married": datetime(2020, 6, 1),
        }
    }
    errors = check_marriage_before_death(individuals, families)
    assert any("after wife's" in err for err in errors)

def test_marriage_after_both_deaths():
    individuals = {
        "@I1@": {"death": datetime(2018, 12, 31)},
        "@I2@": {"death": datetime(2019, 1, 1)},
    }
    families = {
        "@F1@": {
            "husband": "@I1@",
            "wife": "@I2@",
            "married": datetime(2020, 1, 1),
        }
    }
    errors = check_marriage_before_death(individuals, families)
    assert "after husband's" in errors[0]
    assert "after wife's" in errors[1]

def test_missing_marriage_date():
    individuals = {
        "@I1@": {"death": datetime(2020, 6, 1)},
        "@I2@": {"death": datetime(2020, 6, 1)},
    }
    families = {
        "@F1@": {
            "husband": "@I1@",
            "wife": "@I2@",
            # No marriage date
        }
    }
    errors = check_marriage_before_death(individuals, families)
    assert errors == []
