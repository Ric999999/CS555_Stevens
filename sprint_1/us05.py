from datetime import datetime

def parse_gedcom(file_path):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None
    date_context = None

    with open(file_path, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        parts = line.strip().split(" ", 2)
        if len(parts) < 2:
            continue

        level = parts[0]
        tag = parts[1]
        argument = parts[2] if len(parts) == 3 else ""

        if level == "0":
            date_context = None
            if "INDI" in argument:
                current_individual = tag
                individuals[current_individual] = {
                    "id": current_individual,
                    "name": "",
                    "death": None
                }
                current_family = None
            elif "FAM" in argument:
                current_family = tag
                families[current_family] = {
                    "id": current_family,
                    "husband": None,
                    "wife": None,
                    "married": None
                }
                current_individual = None

        elif level == "1":
            if tag == "NAME" and current_individual:
                individuals[current_individual]["name"] = argument
            elif tag == "DEAT" and current_individual:
                date_context = "DEAT"
            elif tag == "HUSB" and current_family:
                families[current_family]["husband"] = argument
            elif tag == "WIFE" and current_family:
                families[current_family]["wife"] = argument
            elif tag == "MARR" and current_family:
                date_context = "MARR"
            else:
                date_context = None

        elif level == "2" and tag == "DATE":
            try:
                date_obj = datetime.strptime(argument, "%d %b %Y")
                if date_context == "DEAT" and current_individual:
                    individuals[current_individual]["death"] = date_obj
                elif date_context == "MARR" and current_family:
                    families[current_family]["married"] = date_obj
                date_context = None
            except ValueError:
                continue

    return individuals, families

def check_marriage_before_death(individuals, families):
    errors = []

    for fam_id, family in families.items():
        marriage_date = family.get("married")
        husband_id = family.get("husband")
        wife_id = family.get("wife")

        if not marriage_date:
            continue

        if husband_id and husband_id in individuals:
            husband_death = individuals[husband_id].get("death")
            if husband_death and marriage_date > husband_death:
                errors.append(
                    f"ERROR: US05: Marriage date {marriage_date.strftime('%d %b %Y')} "
                    f"is after husband's ({husband_id}) death on {husband_death.strftime('%d %b %Y')} in family {fam_id}"
                )

        if wife_id and wife_id in individuals:
            wife_death = individuals[wife_id].get("death")
            if wife_death and marriage_date > wife_death:
                errors.append(
                    f"ERROR: US05: Marriage date {marriage_date.strftime('%d %b %Y')} "
                    f"is after wife's ({wife_id}) death on {wife_death.strftime('%d %b %Y')} in family {fam_id}"
                )

    return errors

def write_output(errors, output_path="us05_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US05: All marriages occur before death of spouses.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking marriage before death in {gedcom_file}...\n")

    individuals, families = parse_gedcom(gedcom_file)
    errors = check_marriage_before_death(individuals, families)
    write_output(errors)

    print("Validation complete. Results saved to 'us05_output.txt'.")
