from datetime import datetime
import re

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y")
    except ValueError:
        return None

def extract_last_name(name):
    match = re.search(r'/([^/]+)/', name)
    return match.group(1) if match else None

def parse_gedcom_file(file_path):
    individuals = {}
    families = {}
    current_indi = None
    current_fam = None

    with open(file_path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        parts = lines[i].strip().split(" ", 2)
        level = parts[0]

        if level == "0":
            if len(parts) == 3 and parts[2] == "INDI":
                current_indi = parts[1].strip()
                individuals[current_indi] = {}
                current_fam = None
            elif len(parts) == 3 and parts[2] == "FAM":
                current_fam = parts[1].strip()
                families[current_fam] = {"children": []}
                current_indi = None
            else:
                current_indi = None
                current_fam = None
        elif level == "1":
            tag = parts[1]
            argument = parts[2] if len(parts) > 2 else ""

            if current_indi:
                if tag == "NAME":
                    individuals[current_indi]["name"] = argument
                elif tag == "SEX":
                    individuals[current_indi]["sex"] = argument
                elif tag == "BIRT":
                    if i + 1 < len(lines) and lines[i+1].strip().startswith("2 DATE"):
                        birth_date = lines[i+1].strip().split("DATE")[1].strip()
                        individuals[current_indi]["birth"] = parse_date(birth_date)
                elif tag == "DEAT":
                    if i + 1 < len(lines) and lines[i+1].strip().startswith("2 DATE"):
                        death_date = lines[i+1].strip().split("DATE")[1].strip()
                        individuals[current_indi]["death"] = parse_date(death_date)
            elif current_fam:
                if tag == "HUSB":
                    families[current_fam]["husband"] = argument
                elif tag == "WIFE":
                    families[current_fam]["wife"] = argument
                elif tag == "CHIL":
                    families[current_fam]["children"].append(argument)

    return individuals, families

def check_male_last_names(individuals, families):
    errors = []

    for fam_id, family in families.items():
        husband_id = family.get("husband")
        children_ids = family.get("children", [])

        if not husband_id or husband_id not in individuals:
            continue

        husband = individuals[husband_id]
        if husband.get("sex") != "M":
            continue

        husband_last_name = extract_last_name(husband.get("name", ""))
        if not husband_last_name:
            continue

        for child_id in children_ids:
            child = individuals.get(child_id, {})
            if child.get("sex") == "M":
                child_last_name = extract_last_name(child.get("name", ""))
                if child_last_name != husband_last_name:
                    errors.append(
                        f"ERROR: US16: Male child ({child_id}) '{child.get('name', '')}' in family {fam_id} "
                        f"does not have the same last name as the father '{husband.get('name', '')}'."
                    )
    return errors

def write_output(errors, output_path="us16_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US16: All male family members have the same last name.\n")

if __name__ == "__main__":
    gedcom_path = "../M1B6.ged"
    print("Checking that all male members have the same last name as the father...")

    individuals, families = parse_gedcom_file(gedcom_path)
    errors = check_male_last_names(individuals, families)
    write_output(errors)