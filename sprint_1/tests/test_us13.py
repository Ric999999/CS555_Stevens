import pytest
from datetime import datetime
from collections import defaultdict

def validate_sibling_spacing(siblings):
    """
    Check if siblings are either:
    - Twins (0-1 days apart), OR
    - At least 8 months (~243.5 days) apart.
    Returns False if any pair violates this rule.
    """
    siblings.sort(key=lambda x: x[1])

    for i in range(len(siblings) - 1):
        date1 = siblings[i][1]
        date2 = siblings[i + 1][1]
        days_diff = (date2 - date1).days

        if 2 <= days_diff < 243.5:
            return False

    return True


def test_twins_same_day():
    """Test twins born on the same day (valid)."""
    siblings = [
        ("John", datetime(2000, 1, 1)),
        ("Jane", datetime(2000, 1, 1))
    ]
    assert validate_sibling_spacing(siblings) is True


def test_twins_one_day_apart():
    """Test twins born 1 day apart (valid)."""
    siblings = [
        ("John", datetime(2000, 1, 1)),
        ("Jane", datetime(2000, 1, 2))
    ]
    assert validate_sibling_spacing(siblings) is True


def test_siblings_two_days_apart():
    """Test siblings born 2 days apart (invalid)."""
    siblings = [
        ("Alice", datetime(2000, 1, 1)),
        ("Bob", datetime(2000, 1, 3))
    ]
    assert validate_sibling_spacing(siblings) is False


def test_siblings_seven_months_apart():
    """Test siblings born 7 months apart (invalid)."""
    siblings = [
        ("Alice", datetime(2000, 1, 1)),
        ("Bob", datetime(2000, 8, 1))
    ]
    assert validate_sibling_spacing(siblings) is False


def test_siblings_eight_months_apart():
    """Test siblings born 8 months apart (valid)."""
    siblings = [
        ("Alice", datetime(2000, 1, 1)),
        ("Bob", datetime(2000, 9, 1))
    ]
    assert validate_sibling_spacing(siblings) is True