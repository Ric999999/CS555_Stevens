from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

def check_no_bigamy(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}  # {ID: {"FAMS": []}}
    families = {}     # {ID: {"HUSB": None, "WIFE": None, "MARR": date, "DIV": date}}
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
                individuals[current_id] = {"FAMS": []}
                indi_section, fam_section = True, False
            elif tag == "FAM":
                current_id = pointer
                families[current_id] = {"HUSB": None, "WIFE": None, "MARR": None, "DIV": None}
                fam_section, indi_section = True, False
            continue

        tag = parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if indi_section:
            if tag == "FAMS":
                individuals[current_id]["FAMS"].append(argument)

        elif fam_section:
            if tag in {"HUSB", "WIFE"}:
                families[current_id][tag] = argument
            elif tag == "MARR":
                date_context = "MARR"
            elif tag == "DIV":
                date_context = "DIV"
            elif tag == "DATE" and date_context:
                families[current_id][date_context] = parse_date(argument)
                date_context = None

    # Bigamy check
    for indi_id, data in individuals.items():
        fams = data["FAMS"]
        marriages = []

        for fam_id in fams:
            fam = families.get(fam_id)
            if not fam:
                continue
            start = fam.get("MARR")
            end = fam.get("DIV") or datetime.today().date()
            if start:
                marriages.append((start, end, fam_id))

        marriages.sort()  # Sort by start date

        for i in range(len(marriages)):
            for j in range(i + 1, len(marriages)):
                start1, end1, fam1 = marriages[i]
                start2, end2, fam2 = marriages[j]
                if start2 < end1:
                    errors.append(
                        f"ERROR: US11: Individual {indi_id} has overlapping marriages "
                        f"in families {fam1} and {fam2} ({start1}–{end1} overlaps with {start2}–{end2})"
                    )

    return errors

def write_output(errors, output_path="us11_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US11: No individual is married to multiple people simultaneously.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking no bigamy rule in {gedcom_file}...\n")

    errors = check_no_bigamy(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us11_output.txt'.")
