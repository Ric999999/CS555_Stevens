import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gedcom_parser import process_gedcom_file

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), '%d %b %Y')
    except (ValueError, TypeError, AttributeError):
        return None

def us20_no_aunt_uncle_marriages(individuals, families):
    errors = []
    parent_map = {}
    for fam_id, fam in families.items():
        for child in fam.get("children", []):
            parent_map[child] = (fam.get("husb"), fam.get("wife"))

    for fam_id, fam in families.items():
        husb = fam.get("husb")
        wife = fam.get("wife")

        if not husb or not wife:
            continue

        # Find siblings of each spouse (their aunts/uncles to spouse)
        husb_siblings = set()
        wife_siblings = set()

        for fam2 in families.values():
            children = set(fam2.get("children", []))
            if husb in children:
                husb_siblings.update(children - {husb})
            if wife in children:
                wife_siblings.update(children - {wife})

        # Check if husband is uncle of wife
        if wife in parent_map:
            wife_parents = set(parent_map[wife])
            if husb in wife_siblings:
                errors.append(f"ERROR US20: Uncle {husb} married niece {wife} in family {fam_id}.")

        # Check if wife is aunt of husband
        if husb in parent_map:
            husb_parents = set(parent_map[husb])
            if wife in husb_siblings:
                errors.append(f"ERROR US20: Aunt {wife} married nephew {husb} in family {fam_id}.")

    return errors

if __name__ == "__main__":
    gedcom_file = "/Users/jeremy/Documents/GitHub/CS555_Stevens/M1B6.ged"
    individuals, families = process_gedcom_file(gedcom_file)
    errors = us20_no_aunt_uncle_marriages(individuals, families)

    output_file = os.path.join(os.path.dirname(__file__), "us20_output.txt")
    with open(output_file, "w") as out_file:
        if errors:
            out_file.write("US20 - AUNT/UNCLE MARRIAGE VIOLATIONS:\n")
            out_file.write("\n".join(errors))
        else:
            out_file.write("PASSED: US20: No aunt/uncle marriages found.\n")

    print(f"Validation complete. Results saved to '{output_file}'.")
