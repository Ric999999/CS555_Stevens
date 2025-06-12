
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

def us09_birth_before_death_of_parents(individuals, families):
    """
    Ensures children are born before their mother's death and no more than 9 months
    after their father's death.

    Args:
        individuals (dict): A dictionary of individuals.
        families (dict): A dictionary of families.

    Returns:
        list: List of error messages if validation fails.
    """
    errors = []
    for fam_id, family in families.items():
        children = family.get("children", [])
        father_id = family.get("husb")
        mother_id = family.get("wife")
        father_death = parse_date(individuals.get(father_id, {}).get("death"))
        mother_death = parse_date(individuals.get(mother_id, {}).get("death"))

        for child_id in children:
            child_birth = parse_date(individuals.get(child_id, {}).get("birth"))
            if not child_birth:
                continue
            if mother_death and child_birth > mother_death:
                errors.append(f"ERROR US09: Child {child_id} born after mother's death in family {fam_id}.")
            if father_death and (child_birth - father_death).days > 273:
                errors.append(f"ERROR US09: Child {child_id} born more than 9 months after father's death in family {fam_id}.")
    return errors

def write_output(errors, output_file):
    """Writes validation results to a text file."""
    with open(output_file, "w") as f:
        if errors:
            f.write("US09 - PARENT DEATH RULE VIOLATIONS:\n" + "\n".join(errors))
        else:
            f.write("US09 - PASSED: All children born before mother’s death and within 9 months of father’s death.")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    gedcom_file = os.path.abspath(os.path.join(base_dir, "testing.ged"))
    output_file = os.path.join(base_dir, "us09_output.txt")

    print(f"Checking parent-death rules in {gedcom_file}...")

    individuals, families = process_gedcom_file(gedcom_file)
    errors = us09_birth_before_death_of_parents(individuals, families)
    write_output(errors, output_file)

    print("Validation complete. Results saved to 'us09_output.txt'.")
    