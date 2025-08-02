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

def us30_list_living_married(individuals, families):
    """Returns a list of living married individuals (ID and name)."""
    living_married = []

    for fam in families.values():
        husb_id = fam.get("husb")
        wife_id = fam.get("wife")

        for indi_id in [husb_id, wife_id]:
            if indi_id and individuals.get(indi_id):
                indi = individuals[indi_id]
                if not indi.get('death'):  # Check alive
                    living_married.append((indi_id, indi.get('name', 'Unknown')))

    return living_married

def write_output(living_married):
    output_file = os.path.join(os.path.dirname(__file__), "us30_output.txt")
    with open(output_file, "w") as out_file:
        if living_married:
            out_file.write("US30 - Living married individuals:\n")
            for indi_id, name in living_married:
                out_file.write(f"{indi_id}: {name}\n")
        else:
            out_file.write("US30 - No living married individuals found.\n")

if __name__ == "__main__":
    gedcom_file = "/Users/jeremy/Documents/GitHub/CS555_Stevens/M1B6.ged"
    print(f"Checking living married individuals in {gedcom_file}...\n")

    individuals, families = process_gedcom_file(gedcom_file)
    living_married = us30_list_living_married(individuals, families)
    write_output(living_married)

    print("Validation complete. Results saved to 'us30_output.txt'.")
