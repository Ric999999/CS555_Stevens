import pytest
from datetime import datetime
from collections import defaultdict

def validate_multiple_births(families, individuals):
    """
    Check if any family has >5 siblings born on the same date.
    Args:
        families: Dict of {fam_id: {children: [child_ids]}}
        individuals: Dict of {child_id: {birth: datetime}}
    Returns:
        False if any family violates the rule (sextuplets+), else True.
    """
    for fam_id, fam_data in families.items():
        birth_counts = defaultdict(int)
        for child_id in fam_data.get('children', []):
            birth_date = individuals.get(child_id, {}).get('birth')
            if birth_date:
                birth_counts[birth_date] += 1
                if birth_counts[birth_date] > 5:
                    return False
    return True

def test_quintuplets_valid():
    """Test 5 siblings born on the same date (valid)."""
    families = {"F1": {"children": ["C1", "C2", "C3", "C4", "C5"]}}
    individuals = {
        "C1": {"birth": datetime(2000, 1, 1)},
        "C2": {"birth": datetime(2000, 1, 1)},
        "C3": {"birth": datetime(2000, 1, 1)},
        "C4": {"birth": datetime(2000, 1, 1)},
        "C5": {"birth": datetime(2000, 1, 1)}
    }
    assert validate_multiple_births(families, individuals) is True

def test_sextuplets_invalid():
    """Test 6 siblings born on the same date (invalid)."""
    families = {"F1": {"children": ["C1", "C2", "C3", "C4", "C5", "C6"]}}
    individuals = {
        "C1": {"birth": datetime(2000, 1, 1)},
        "C2": {"birth": datetime(2000, 1, 1)},
        "C3": {"birth": datetime(2000, 1, 1)},
        "C4": {"birth": datetime(2000, 1, 1)},
        "C5": {"birth": datetime(2000, 1, 1)},
        "C6": {"birth": datetime(2000, 1, 1)}
    }
    assert validate_multiple_births(families, individuals) is False

def test_mixed_birth_dates_valid():
    """Test siblings with different birth dates (valid)."""
    families = {"F1": {"children": ["C1", "C2", "C3", "C4", "C5", "C6"]}}
    individuals = {
        "C1": {"birth": datetime(2000, 1, 1)},
        "C2": {"birth": datetime(2000, 1, 1)},
        "C3": {"birth": datetime(2001, 1, 1)},  
        "C4": {"birth": datetime(2000, 1, 2)},
        "C5": {"birth": datetime(2000, 1, 1)},
        "C6": {"birth": datetime(2000, 1, 1)}
    }
    assert validate_multiple_births(families, individuals) is True

def test_no_children_valid():
    """Test family with no children (valid)."""
    families = {"F1": {"children": []}}
    individuals = {}
    assert validate_multiple_births(families, individuals) is True

def test_multiple_families_mixed():
    """Test multiple families with valid/invalid birth groups."""
    families = {
        "F1": {"children": ["C1", "C2", "C3", "C4", "C5"]},
        "F2": {"children": ["C6", "C7", "C8", "C9", "C10", "C11"]}
    }
    individuals = {
        "C1": {"birth": datetime(2000, 1, 1)},
        "C2": {"birth": datetime(2000, 1, 1)},
        "C3": {"birth": datetime(2000, 1, 1)},
        "C4": {"birth": datetime(2000, 1, 1)},
        "C5": {"birth": datetime(2000, 1, 1)},
        "C6": {"birth": datetime(2001, 1, 1)},
        "C7": {"birth": datetime(2001, 1, 1)},
        "C8": {"birth": datetime(2001, 1, 1)},
        "C9": {"birth": datetime(2001, 1, 1)},
        "C10": {"birth": datetime(2001, 1, 1)},
        "C11": {"birth": datetime(2001, 1, 1)}
    }
    assert validate_multiple_births(families, individuals) is False