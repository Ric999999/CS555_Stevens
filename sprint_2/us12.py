from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

def check_parents_not_too_old(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}  # ID -> {BIRT: date, SEX: M/F}
    families = {}     # ID -> {HUSB, WIFE, CHIL: list}
    errors = []

    current_id = None
    indi_section = False
    fam_section = False
    date_context = None

    for i, line in enumerate(lines):
        parts = line.strip().split(" ", 2)
        if len(parts) < 2:
            continue

        level = parts[0]

        if level == "0" and len(parts) == 3:
            pointer, tag = parts[1], parts[2]
            if tag == "INDI":
                current_id = pointer
                individuals[current_id] = {"BIRT": None, "SEX": None}
                indi_section, fam_section = True, False
            elif tag == "FAM":
                current_id = pointer
                families[current_id] = {"HUSB": None, "WIFE": None, "CHIL": []}
                fam_section, indi_section = True, False
            continue

        tag = parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if indi_section:
            if tag == "SEX":
                individuals[current_id]["SEX"] = argument
            elif tag == "BIRT":
                date_context = "BIRT"
            elif tag == "DATE" and date_context == "BIRT":
                individuals[current_id]["BIRT"] = parse_date(argument)
                date_context = None

        elif fam_section:
            if tag in {"HUSB", "WIFE"}:
                families[current_id][tag] = argument
            elif tag == "CHIL":
                families[current_id]["CHIL"].append(argument)

    # Age difference check
    for fam_id, fam in families.items():
        father_id = fam.get("HUSB")
        mother_id = fam.get("WIFE")
        children_ids = fam.get("CHIL", [])

        father_birth = individuals.get(father_id, {}).get("BIRT")
        mother_birth = individuals.get(mother_id, {}).get("BIRT")

        for child_id in children_ids:
            child_birth = individuals.get(child_id, {}).get("BIRT")

            if not child_birth:
                continue

            if father_birth:
                age_diff = (child_birth - father_birth).days / 365.25
                if age_diff > 80:
                    errors.append(
                        f"ERROR: US12: Father {father_id} in family {fam_id} is too old "
                        f"({int(age_diff)} years older than child {child_id})"
                    )

            if mother_birth:
                age_diff = (child_birth - mother_birth).days / 365.25
                if age_diff > 60:
                    errors.append(
                        f"ERROR: US12: Mother {mother_id} in family {fam_id} is too old "
                        f"({int(age_diff)} years older than child {child_id})"
                    )

    return errors

def write_output(errors, output_path="us12_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US12: All parents are within allowed age difference from children.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking parent age constraints in {gedcom_file}...\n")

    errors = check_parents_not_too_old(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us12_output.txt'.")
