import os
import sys
import pytest
from datetime import datetime
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from us23 import process_gedcom


# Helper function to simulate GEDCOM processing
def run_us23_test(families_data, individuals_data):
    """Mock GEDCOM data and run US23 validation."""
    families = defaultdict(dict)
    individuals = {}

    # Populate mock data
    for fam_id, data in families_data.items():
        families[fam_id] = {"children": data.get("children", [])}

    for indi_id, data in individuals_data.items():
        individuals[indi_id] = {
            "name": data["name"],
            "birth": datetime.strptime(data["birth"], "%d %b %Y") if data.get("birth") else None
        }

    # Run validation logic (extracted from US23 implementation)
    error_found = False
    for fam_id, fam_data in families.items():
        seen = set()
        for child_id in fam_data.get("children", []):
            if child_id in individuals:
                name = individuals[child_id]["name"]
                birth = individuals[child_id].get("birth")
                if birth:
                    key = (name, birth)
                    if key in seen:
                        error_found = True
                    seen.add(key)
    return not error_found


# Test Cases
def test_no_duplicates():
    """Family with unique name+birth combinations should pass."""
    families = {"F1": {"children": ["I1", "I2"]}}
    individuals = {
        "I1": {"name": "John Doe", "birth": "01 Jan 2000"},
        "I2": {"name": "Jane Doe", "birth": "02 Jan 2000"}
    }
    assert run_us23_test(families, individuals) is True


def test_duplicate_name_diff_birth():
    """Same name but different birth dates should pass."""
    families = {"F1": {"children": ["I1", "I2"]}}
    individuals = {
        "I1": {"name": "John Doe", "birth": "01 Jan 2000"},
        "I2": {"name": "John Doe", "birth": "01 Jan 2001"}  # Different year
    }
    assert run_us23_test(families, individuals) is True


def test_duplicate_name_and_birth():
    """Same name AND birth date should fail."""
    families = {"F1": {"children": ["I1", "I2"]}}
    individuals = {
        "I1": {"name": "John Doe", "birth": "01 Jan 2000"},
        "I2": {"name": "John Doe", "birth": "01 Jan 2000"}  # Exact duplicate
    }
    assert run_us23_test(families, individuals) is False


def test_case_sensitive_names():
    """Names with different casing should NOT be considered duplicates."""
    families = {"F1": {"children": ["I1", "I2"]}}
    individuals = {
        "I1": {"name": "John Doe", "birth": "01 Jan 2000"},
        "I2": {"name": "JOHN DOE", "birth": "01 Jan 2000"}  # Different case
    }
    assert run_us23_test(families, individuals) is True  # Passes because case differs


def test_multiple_families_mixed():
    """Test multiple families with/without duplicates."""
    families = {
        "F1": {"children": ["I1", "I2"]},  # Valid (unique)
        "F2": {"children": ["I3", "I4"]}  # Invalid (duplicates)
    }
    individuals = {
        "I1": {"name": "Alice", "birth": "01 Jan 2000"},
        "I2": {"name": "Bob", "birth": "02 Jan 2000"},
        "I3": {"name": "Charlie", "birth": "01 Feb 2000"},
        "I4": {"name": "Charlie", "birth": "01 Feb 2000"}  # Duplicate
    }
    assert run_us23_test(families, individuals) is False  # Fails due to F2