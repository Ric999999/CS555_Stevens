import pytest
from collections import defaultdict

def validate_sibling_count(families):
    """
    Check if any family has 15 or more siblings.
    Returns False if any family violates the rule, else True.
    """
    for fam_id, fam_data in families.items():
        if len(fam_data.get('children', [])) >= 15:
            return False
    return True

def test_no_children():
    """Family with no children should pass."""
    families = {
        "F1": {"husband": "John", "wife": "Jane", "children": []}
    }
    assert validate_sibling_count(families) is True

def test_14_children():
    """Family with 14 children should pass."""
    families = {
        "F1": {"husband": "John", "wife": "Jane", "children": [f"C{i}" for i in range(1, 15)]}
    }
    assert validate_sibling_count(families) is True

def test_exactly_15_children():
    """Family with exactly 15 children should fail."""
    families = {
        "F1": {"husband": "John", "wife": "Jane", "children": [f"C{i}" for i in range(1, 16)]}
    }
    assert validate_sibling_count(families) is False

def test_20_children():
    """Family with 20 children should fail."""
    families = {
        "F1": {"husband": "John", "wife": "Jane", "children": [f"C{i}" for i in range(1, 21)]}
    }
    assert validate_sibling_count(families) is False

def test_multiple_families():
    """Test multiple families with valid/invalid sibling counts."""
    families = {
        "F1": {"children": [f"C{i}" for i in range(1, 10)]},
        "F2": {"children": [f"C{i}" for i in range(10, 30)]},
        "F3": {"children": []}  # Valid
    }
    assert validate_sibling_count(families) is False