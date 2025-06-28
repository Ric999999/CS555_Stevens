from collections import defaultdict

def parse_gedcom(filename):
    individuals = {}
    families = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

    indi_id = fam_id = None
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue

        level = parts[0]
        tag = parts[1] if parts[1] in ["INDI", "FAM"] else parts[2] if len(parts) > 2 and parts[2] in ["INDI", "FAM"] else None

        if tag == "INDI":
            indi_id = parts[1]
            individuals[indi_id] = {"FAMS": [], "FAMC": None}
        elif tag == "FAM":
            fam_id = parts[1]
            families[fam_id] = {"HUSB": None, "WIFE": None, "CHIL": []}
        elif tag == "FAMS" and indi_id:
            individuals[indi_id]["FAMS"].append(parts[2])
        elif tag == "FAMC" and indi_id:
            individuals[indi_id]["FAMC"] = parts[2]
        elif tag in ["HUSB", "WIFE"] and fam_id:
            families[fam_id][tag] = parts[2]
        elif tag == "CHIL" and fam_id:
            families[fam_id]["CHIL"].append(parts[2])

    return individuals, families

def is_descendant(individuals, families, ancestor, person):
    """DFS to check if 'person' is a descendant of 'ancestor'."""
    if ancestor not in individuals or person not in individuals:
        return False

    children = []
    for fam_id in individuals.get(ancestor, {}).get("FAMS", []):
        children += families.get(fam_id, {}).get("CHIL", [])

    visited = set()
    stack = list(children)

    while stack:
        current = stack.pop()
        if current == person:
            return True
        visited.add(current)
        for fam_id in individuals.get(current, {}).get("FAMS", []):
            stack.extend(families.get(fam_id, {}).get("CHIL", []))
    return False


def check_no_marriage_to_descendants(filename):
    individuals, families = parse_gedcom(filename)
    errors = []

    for fam_id, fam in families.items():
        husband = fam["HUSB"]
        wife = fam["WIFE"]

        if husband and wife:
            if is_descendant(individuals, families, husband, wife):
                errors.append(f"ERROR US17: {husband} is married to their descendant {wife} in family {fam_id}")
            if is_descendant(individuals, families, wife, husband):
                errors.append(f"ERROR US17: {wife} is married to their descendant {husband} in family {fam_id}")
    return errors

def write_output(errors, output_path="us17_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("All marriages verified. No parent married a descendant.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking parent-descendant marriages in {gedcom_file}...\n")

    errors = check_no_marriage_to_descendants(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us17_output.txt'.")
