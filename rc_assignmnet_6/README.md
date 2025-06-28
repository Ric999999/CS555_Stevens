# CS555 - Assignment: GEDCOM User Story Refactoring (US12)

## Rui Costa

## Overview

This assignment demonstrates:

- Identifying **two bad smells** in the original implementation of US12.
- Refactoring the code to eliminate these bad smells.
- Verifying with `pytest` that both the original and refactored solutions work correctly.

---

## 1. Original code (`us12.py`)

The file `us12.py` implements US12 (parents not too old compared to children) using a simple parser for GEDCOM files.

### Bad Smells Identified

#### 🐞 Bad Smell #1 — Duplicated parent checks
In `check_parents_not_too_old`:
```python
if father_birth:
    age_diff = ...
    if age_diff > 80:
        errors.append(...)
if mother_birth:
    age_diff = ...
    if age_diff > 60:
        errors.append(...)
````

* This violates **DRY (Don’t Repeat Yourself)**.
* Harder to maintain or change logic for calculating age difference.

#### 🐞 Bad Smell #2 — Fragile global state for parsing dates

In the parsing loop:

```python
elif tag == "BIRT":
    date_context = "BIRT"
elif tag == "DATE" and date_context == "BIRT":
    individuals[current_id]["BIRT"] = parse_date(argument)
    date_context = None
```

* Uses a global-like `date_context` to remember the previous tag.
* Fragile if more tags (like `DEAT` or `MARR`) are added, or if context is lost.

---

## 2. Tests on original code

The file `test_us12.py` contains `pytest` tests:

* Tests that the age violations in `test_data.ged` correctly produce errors for both father and mother.
* Tests a compliant family structure to ensure it passes with no errors.

### Pytest results (original code)

Saved in `smelly_test_output.txt`:

```
============================= test session starts ==============================
collected 2 items
test_us12.py ..                                                           [100%]
============================== 2 passed in 0.01s ==============================
```

✅ Confirms the original (but smelly) code works.

---

## 3. Refactored code (`us12_refactored.py`)

### Refactoring to remove bad smells

#### Fix #1: Extract duplicate logic into helper function

```python
def check_parent_age_difference(parent_birth, child_birth, max_age_diff, parent_role, parent_id, child_id, fam_id):
    ...
```

* Eliminates repeated calculations for father and mother.
* Easier to maintain if age rules change.

#### Fix #2: Use local parsing state instead of global

```python
current_date_tag = None
...
elif tag in {"BIRT", "DEAT"}:
    current_date_tag = tag
elif tag == "DATE" and current_date_tag == "BIRT":
    individuals[current_id]["BIRT"] = parse_date(argument)
    current_date_tag = None
```

* Safer and clearer than the old `date_context`.
* Ready to extend for future tags like `DEAT`.

---

## 4. Tests on refactored code

Re-ran the same `pytest` tests, importing the refactored module.

### Pytest results (refactored code)

Saved in `refactored_test_output.txt`:

```
============================= test session starts ==============================
collected 2 items
test_us12.py ..                                                           [100%]
============================== 2 passed in 0.01s ==============================
```

✅ Confirms the refactored solution preserves functionality.

---

## 5. Submission contents

| File                         | Description                              |
| ---------------------------- | ---------------------------------------- |
| `us12.py`                    | Original code (with explicit bad smells) |
| `test_data.ged`              | GEDCOM data to trigger parent age errors |
| `test_us12.py`               | Pytest tests used for both versions      |
| `smelly_test_output.txt`     | Pytest output on original code           |
| `us12_refactored.py`         | Refactored code fixing both bad smells   |
| `refactored_test_output.txt` | Pytest output on refactored code         |
| `README.md`                  | This summary document                    |
