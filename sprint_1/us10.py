
import sys
import os
from datetime import datetime

# Dynamically add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gedcom_parser import process_gedcom_file


def parse_date(date_str):
    """Parses a date string in YYYY-MM-DD format to a datetime object."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def us10_marriage_after_14(individuals, families):
    """
    Validates that individuals were at least 14 years old at the time of marriage.

    Args:
        individuals (dict): A dictionary of individuals.
        families (dict): A dictionary of families.

    Returns:
        list: List of error messages if validation fails.
    """
    errors = []
    for fam_id, family in families.items():
        marriage_date = parse_date(family.get("married"))
        if not marriage_date:
            continue

        for role in ['husb', 'wife']:
            person_id = family.get(role)
            birth_date = parse_date(individuals.get(person_id, {}).get("birth"))
            if birth_date:
                age_at_marriage = (marriage_date - birth_date).days / 365.25
                if age_at_marriage < 14:
                    errors.append(f"ERROR US10: {role.title()} {person_id} was married at {age_at_marriage:.1f} years in family {fam_id}.")
    return errors

def write_output(errors, output_file):
    """Writes validation results to a text file."""
    with open(output_file, "w") as f:
        if errors:
            f.write("US10 - MARRIAGE AGE RULE VIOLATIONS:\n" + "\n".join(errors))
        else:
            f.write("US10 - PASSED: All individuals were at least 14 years old at marriage.")

if __name__ == "__main__":
    gedcom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "M1B6.ged"))
    output_file = os.path.join(os.path.dirname(__file__), "us10_output.txt")
    print(f"Checking marriage-age rules in {gedcom_file}...")

    individuals, families = process_gedcom_file(gedcom_file)
    errors = us10_marriage_after_14(individuals, families)
    write_output(errors, output_file)

    print("Validation complete. Results saved to 'us10_output.txt'.")
