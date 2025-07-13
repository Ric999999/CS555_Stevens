from datetime import datetime
from collections import defaultdict

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

def check_unique_child_name_and_birth(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}
    families = defaultdict(list)
    errors = []

    current_id = None
    indi_section = False
    fam_section = False
    parsing_birth = False

    for i, line in enumerate(lines):
        parts = line.strip().split(" ", 2)
        if len(parts) < 2:
            continue

        level = parts[0]

        if level == "0":
            parsing_birth = False  # Reset birth flag on new record
            if len(parts) == 3:
                pointer, tag = parts[1], parts[2]
                if tag == "INDI":
                    current_id = pointer
                    individuals[current_id] = {"NAME": None, "BIRT": None}
                    indi_section, fam_section = True, False
                elif tag == "FAM":
                    current_id = pointer
                    fam_section, indi_section = True, False
                continue

        tag = parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if indi_section:
            if tag == "NAME":
                individuals[current_id]["NAME"] = argument
            elif tag == "BIRT":
                parsing_birth = True
            elif tag == "DATE" and parsing_birth:
                individuals[current_id]["BIRT"] = parse_date(argument)
                parsing_birth = False

        elif fam_section:
            if tag == "CHIL":
                families[current_id].append(argument)

    # Check each family for duplicate child names and birth dates
    for fam_id, child_ids in families.items():
        seen = set()
        for child_id in child_ids:
            child = individuals.get(child_id)
            if not child:
                continue
            key = (child["NAME"], child["BIRT"])
            if key in seen:
                errors.append(
                    f"ERROR: US25: Family {fam_id} has more than one child named {child['NAME']} born on {child['BIRT']}."
                )
            else:
                seen.add(key)

    return errors

def write_output(errors, output_path="us25_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US25: All families have uniquely named children by birth date.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking unique child names and birth dates in {gedcom_file}...\n")

    errors = check_unique_child_name_and_birth(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us25_output.txt'.")