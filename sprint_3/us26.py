def check_family_roles_consistency(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}  # {ID: {"FAMC": set(), "FAMS": set()}}
    families = {}     # {FAM_ID: {"HUSB": ID, "WIFE": ID, "CHIL": set()}}
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
                individuals[current_id] = {"FAMC": set(), "FAMS": set()}
                indi_section, fam_section = True, False
            elif tag == "FAM":
                current_id = pointer
                families[current_id] = {"HUSB": None, "WIFE": None, "CHIL": set()}
                fam_section, indi_section = True, False
            continue

        tag = parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if indi_section:
            if tag == "FAMC":
                individuals[current_id]["FAMC"].add(argument)
            elif tag == "FAMS":
                individuals[current_id]["FAMS"].add(argument)

        elif fam_section:
            if tag == "HUSB":
                families[current_id]["HUSB"] = argument
            elif tag == "WIFE":
                families[current_id]["WIFE"] = argument
            elif tag == "CHIL":
                families[current_id]["CHIL"].add(argument)

    # Check consistency: individuals listed in family must reference that family
    for fam_id, fam in families.items():
        for role, indi_id in [("HUSB", fam["HUSB"]), ("WIFE", fam["WIFE"])]:
            if indi_id and fam_id not in individuals.get(indi_id, {}).get("FAMS", set()):
                errors.append(
                    f"ERROR: US26: {role} {indi_id} in family {fam_id} does not list this family in FAMS."
                )
        for child_id in fam["CHIL"]:
            if child_id and fam_id not in individuals.get(child_id, {}).get("FAMC", set()):
                errors.append(
                    f"ERROR: US26: Child {child_id} in family {fam_id} does not list this family in FAMC."
                )

    return errors

def write_output(errors, output_path="us26_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US26: All individuals correctly reference their family roles.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking family role consistency in {gedcom_file}...\n")

    errors = check_family_roles_consistency(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us26_output.txt'.")
