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

def us29_list_deceased(individuals):
    """Returns a list of IDs for deceased individuals."""
    deceased = []
    for indi_id, indi_data in individuals.items():
        if indi_data.get('death'):
            deceased.append((indi_id, indi_data.get('name', 'Unknown')))
    return deceased

def write_output(deceased):
    output_file = os.path.join(os.path.dirname(__file__), "us29_output.txt")
    with open(output_file, "w") as out_file:
        if deceased:
            out_file.write("US29 - Deceased individuals:\n")
            for indi_id, name in deceased:
                out_file.write(f"{indi_id}: {name}\n")
        else:
            out_file.write("US29 - No deceased individuals found.\n")

if __name__ == "__main__":
    gedcom_file = "/Users/jeremy/Documents/GitHub/CS555_Stevens/M1B6.ged"
    print(f"Checking deceased individuals in {gedcom_file}...\n")

    individuals, families = process_gedcom_file(gedcom_file)
    deceased = us29_list_deceased(individuals)
    write_output(deceased)

    print("Validation complete. Results saved to 'us29_output.txt'.")
