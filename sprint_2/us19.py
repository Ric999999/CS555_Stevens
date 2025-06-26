import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gedcom_parser import process_gedcom_file

def parse_date(date_str):
    """Parse date string to datetime object if possible."""
    try:
        return datetime.strptime(date_str.strip(), '%d %b %Y')
    except (ValueError, TypeError, AttributeError):
        return None

def us19_no_first_cousin_marriages(individuals, families):
    """Detects if first cousins are married and reports violations."""
    errors = []

    # Map individual -> parents
    parent_map = {}
    for fam_id, fam in families.items():
        for child in fam.get("children", []):
            parent_map[child] = (fam.get("husb"), fam.get("wife"))

    # Map individual -> grandparents
    grandparent_map = {}
    for indi, (father, mother) in parent_map.items():
        grandparents = set()
        for parent in (father, mother):
            grandparents.update(parent_map.get(parent, ()))
        grandparent_map[indi] = grandparents

    # Check for first cousin marriages
    for fam_id, fam in families.items():
        husb = fam.get("husb")
        wife = fam.get("wife")
        if not husb or not wife:
            continue

        husb_grandparents = grandparent_map.get(husb, set())
        wife_grandparents = grandparent_map.get(wife, set())

        if husb_grandparents & wife_grandparents:
            errors.append(
                f"ERROR US19: First cousins {husb} and {wife} are married in family {fam_id}."
            )

    return errors

if __name__ == "__main__":
    gedcom_file = "/Users/jeremy/Documents/GitHub/CS555_Stevens/M1B6.ged"
    individuals, families = process_gedcom_file(gedcom_file)
    errors = us19_no_first_cousin_marriages(individuals, families)

    output_file = os.path.join(os.path.dirname(__file__), "us19_output.txt")
    with open(output_file, "w") as out_file:
        if errors:
            out_file.write("US19 - FIRST COUSIN MARRIAGE VIOLATIONS:\n")
            out_file.write("\n".join(errors))
        else:
            out_file.write("PASSED: US19: No first cousin marriages found.\n")

    print(f"Validation complete. Results saved to '{output_file}'.")

