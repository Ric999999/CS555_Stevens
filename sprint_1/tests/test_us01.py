import sys
import os
import tempfile
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from us01 import is_date_before_today, check_dates_before_today

# ------------------ Tests for is_date_before_today ------------------

def test_is_date_before_today_past_date():
    assert is_date_before_today("01 JAN 2000") is True

def test_is_date_before_today_today_date():
    today_str = datetime.today().strftime("%d %b %Y")
    assert is_date_before_today(today_str) is False

def test_is_date_before_today_future_date():
    future = datetime.today() + timedelta(days=10)
    future_str = future.strftime("%d %b %Y")
    assert is_date_before_today(future_str) is False

def test_is_date_before_today_invalid_format():
    assert is_date_before_today("not a date") is False

def test_is_date_before_today_leap_year():
    assert is_date_before_today("29 FEB 2000") is True

# ------------------ Tests for check_dates_before_today ------------------

def write_gedcom_file(contents):
    fd, path = tempfile.mkstemp(text=True, suffix=".ged")
    with os.fdopen(fd, "w") as tmp:
        tmp.write(contents)
    return path

def test_check_dates_before_today_all_valid():
    contents = """0 @I1@ INDI
1 BIRT
2 DATE 15 MAY 1940
1 DEAT
2 DATE 16 JUN 2000
0 @F1@ FAM
1 MARR
2 DATE 18 JUL 1980
"""
    path = write_gedcom_file(contents)
    errors = check_dates_before_today(path)
    assert errors == []
    os.remove(path)

def test_check_dates_before_today_with_future_date():
    future = (datetime.today() + timedelta(days=5)).strftime("%d %b %Y")
    contents = f"""0 @I2@ INDI
1 BIRT
2 DATE {future}
"""
    path = write_gedcom_file(contents)
    errors = check_dates_before_today(path)
    assert any("is not before today's date" in e for e in errors)
    os.remove(path)

def test_check_dates_before_today_mixed_valid_and_invalid():
    future = (datetime.today() + timedelta(days=1)).strftime("%d %b %Y")
    contents = f"""0 @I1@ INDI
1 BIRT
2 DATE 12 JAN 1990
1 DEAT
2 DATE {future}
"""
    path = write_gedcom_file(contents)
    errors = check_dates_before_today(path)
    assert len(errors) == 1
    assert "DEAT date" in errors[0]
    os.remove(path)

def test_check_dates_before_today_bad_date_format():
    contents = """0 @I3@ INDI
1 BIRT
2 DATE BAD_DATE
"""
    path = write_gedcom_file(contents)
    errors = check_dates_before_today(path)
    assert len(errors) == 1
    assert "BIRT date 'BAD_DATE'" in errors[0]
    os.remove(path)

def test_check_dates_before_today_missing_date():
    contents = """0 @I4@ INDI
1 BIRT
"""
    path = write_gedcom_file(contents)
    errors = check_dates_before_today(path)
    assert errors == []
    os.remove(path)
