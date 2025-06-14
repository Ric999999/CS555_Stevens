from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y")
    except ValueError:
        return None

def check_birth_before_marriage(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}
    families = {}
    errors = []

    current_id = None
    indi_section = False
    fam_section = False
    date_context = None

    for i, line in enumerate(lines):
        parts = line.strip().split(' ', 2)
        if len(parts) < 2:
            continue

        level, tag = parts[0], parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if len(parts) == 3 and parts[2] == "INDI":
            current_id = parts[1]
            individuals[current_id] = {"BIRT": None, "FAMS": []}
            indi_section, fam_section = True, False

        elif len(parts) == 3 and parts[2] == "FAM":
            current_id = parts[1]
            families[current_id] = {"HUSB": None, "WIFE": None, "MARR": None}
            fam_section, indi_section = True, False

        elif indi_section:
            if tag == "BIRT":
                date_context = "BIRT"
            elif tag == "FAMS":
                individuals[current_id]["FAMS"].append(argument)
            elif tag == "DATE" and date_context == "BIRT":
                individuals[current_id]["BIRT"] = parse_date(argument)
                date_context = None

        elif fam_section:
            if tag == "HUSB" or tag == "WIFE":
                families[current_id][tag] = argument
            elif tag == "MARR":
                date_context = "MARR"
            elif tag == "DATE" and date_context == "MARR":
                families[current_id]["MARR"] = parse_date(argument)
                date_context = None

    # Compare birth dates to marriage dates
    for fam_id, fam_data in families.items():
        marr_date = fam_data["MARR"]
        if not marr_date:
            continue

        for role in ["HUSB", "WIFE"]:
            indi_id = fam_data[role]
            if not indi_id or indi_id not in individuals:
                continue
            birth_date = individuals[indi_id]["BIRT"]
            if birth_date and birth_date > marr_date:
                errors.append(
                    f"ERROR: US02: {role} {indi_id} birth date {birth_date.strftime('%d %b %Y')} "
                    f"is after marriage date {marr_date.strftime('%d %b %Y')} in family {fam_id}"
                )

    return errors

def write_output(errors, output_path="us02_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US02: All individuals were born before their marriages.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking birth-before-marriage in {gedcom_file}...\n")

    errors = check_birth_before_marriage(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us02_output.txt'.")
