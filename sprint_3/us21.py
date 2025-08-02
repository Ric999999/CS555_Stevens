from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

def check_gender_for_roles(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}  # {ID: SEX}
    families = {}     # {ID: {"HUSB": ID, "WIFE": ID}}
    errors = []

    current_id = None
    indi_section = False
    fam_section = False

    for line in lines:
        parts = line.strip().split(" ", 2)
        if len(parts) < 2:
            continue

        level = parts[0]

        if level == "0" and len(parts) == 3:
            pointer, tag = parts[1], parts[2]
            if tag == "INDI":
                current_id = pointer
                individuals[current_id] = None
                indi_section, fam_section = True, False
            elif tag == "FAM":
                current_id = pointer
                families[current_id] = {"HUSB": None, "WIFE": None}
                fam_section, indi_section = True, False
            continue

        tag = parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if indi_section:
            if tag == "SEX":
                individuals[current_id] = argument

        elif fam_section:
            if tag in {"HUSB", "WIFE"}:
                families[current_id][tag] = argument

    # Check genders
    for fam_id, fam_data in families.items():
        husband = fam_data.get("HUSB")
        wife = fam_data.get("WIFE")

        if husband and individuals.get(husband) != "M":
            errors.append(
                f"ERROR: US21: Husband {husband} in family {fam_id} is not male."
            )

        if wife and individuals.get(wife) != "F":
            errors.append(
                f"ERROR: US21: Wife {wife} in family {fam_id} is not female."
            )

    return errors

def write_output(errors, output_path="us21_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US21: All family roles have correct gender assignments.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking gender roles in {gedcom_file}...\n")

    errors = check_gender_for_roles(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us21_output.txt'.")
