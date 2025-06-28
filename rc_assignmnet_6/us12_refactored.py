from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

def check_parent_age_difference(parent_birth, child_birth, max_age_diff, parent_role, parent_id, child_id, fam_id):
    if not parent_birth or not child_birth:
        return None
    age_diff = (child_birth - parent_birth).days / 365.25
    if age_diff > max_age_diff:
        return (
            f"ERROR: US12: {parent_role} {parent_id} in family {fam_id} is too old "
            f"({int(age_diff)} years older than child {child_id})"
        )
    return None

def check_parents_not_too_old(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}
    families = {}
    errors = []

    current_id = None
    indi_section = False
    fam_section = False
    current_date_tag = None  # cleaner than global mutable state

    for line in lines:
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
            elif tag in {"BIRT", "DEAT"}:
                current_date_tag = tag
            elif tag == "DATE" and current_date_tag == "BIRT":
                individuals[current_id]["BIRT"] = parse_date(argument)
                current_date_tag = None

        elif fam_section:
            if tag in {"HUSB", "WIFE"}:
                families[current_id][tag] = argument
            elif tag == "CHIL":
                families[current_id]["CHIL"].append(argument)

    for fam_id, fam in families.items():
        father_id = fam.get("HUSB")
        mother_id = fam.get("WIFE")
        children_ids = fam.get("CHIL", [])

        father_birth = individuals.get(father_id, {}).get("BIRT")
        mother_birth = individuals.get(mother_id, {}).get("BIRT")

        for child_id in children_ids:
            child_birth = individuals.get(child_id, {}).get("BIRT")

            result = check_parent_age_difference(father_birth, child_birth, 80, "Father", father_id, child_id, fam_id)
            if result:
                errors.append(result)

            result = check_parent_age_difference(mother_birth, child_birth, 60, "Mother", mother_id, child_id, fam_id)
            if result:
                errors.append(result)

    return errors
