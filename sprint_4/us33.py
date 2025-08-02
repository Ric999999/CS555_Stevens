from datetime import datetime

def parse_date(date_str):
    """Convert GEDCOM date string to datetime.date object"""
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

def calculate_age(birth_date, death_date=None, reference_date=None):
    """Calculate age at death or current age if still alive"""
    ref_date = reference_date or datetime.now().date()
    if birth_date is None:
        return 0
    age = ref_date.year - birth_date.year
    if (ref_date.month, ref_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

def list_orphans(file_path):
    """Identify orphans (children <18 with deceased parents)"""
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}  # {ID: {"name": str, "birth": date, "death": date, "famc": str}}
    families = {}     # {ID: {"HUSB": id, "WIFE": id, "CHIL": [ids], "husb_death": date, "wife_death": date}}
    orphans = []

    current_id = None
    indi_section = False
    fam_section = False
    current_tag = None

    # Parse GEDCOM file
    for line in lines:
        parts = line.strip().split(" ", 2)
        if len(parts) < 2:
            continue

        level = parts[0]

        if level == "0":
            if len(parts) == 3:
                pointer, tag = parts[1], parts[2]
                if tag == "INDI":
                    current_id = pointer
                    individuals[current_id] = {"name": "Unknown", "birth": None, "death": None, "famc": None}
                    indi_section, fam_section = True, False
                elif tag == "FAM":
                    current_id = pointer
                    families[current_id] = {"HUSB": None, "WIFE": None, "CHIL": [], "husb_death": None, "wife_death": None}
                    fam_section, indi_section = True, False
            continue

        tag = parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if indi_section:
            if tag == "NAME":
                individuals[current_id]["name"] = argument
            elif tag == "BIRT":
                current_tag = "BIRT"
            elif tag == "DEAT":
                current_tag = "DEAT"
            elif tag == "FAMC":
                individuals[current_id]["famc"] = argument
            elif tag == "DATE" and current_tag:
                date = parse_date(argument)
                if current_tag == "BIRT":
                    individuals[current_id]["birth"] = date
                elif current_tag == "DEAT":
                    individuals[current_id]["death"] = date
                current_tag = None

        elif fam_section:
            if tag in {"HUSB", "WIFE"}:
                families[current_id][tag] = argument
            elif tag == "CHIL":
                families[current_id]["CHIL"].append(argument)
            elif tag == "DEAT":
                # Track parent deaths in family record
                role = "husb_death" if families[current_id]["HUSB"] else "wife_death"
                current_tag = role

    # Process parent death dates
    for fam_id, fam_data in families.items():
        if fam_data["HUSB"] and individuals.get(fam_data["HUSB"], {}).get("death"):
            fam_data["husb_death"] = individuals[fam_data["HUSB"]]["death"]
        if fam_data["WIFE"] and individuals.get(fam_data["WIFE"], {}).get("death"):
            fam_data["wife_death"] = individuals[fam_data["WIFE"]]["death"]

    # Identify orphans
    today = datetime.now().date()
    for indi_id, indi_data in individuals.items():
        if not indi_data["famc"] or not indi_data["birth"]:
            continue

        fam_id = indi_data["famc"]
        if fam_id not in families:
            continue

        age = calculate_age(indi_data["birth"], reference_date=today)
        if age >= 18:
            continue

        family = families[fam_id]
        both_parents_deceased = (family["husb_death"] is not None and
                                family["wife_death"] is not None)

        if both_parents_deceased:
            orphans.append((indi_id, indi_data["name"], age, fam_id))

    return orphans

def write_output(orphans, output_path="us33_output.txt"):
    """Write results to output file"""
    with open(output_path, "w") as f:
        if orphans:
            f.write("US33: List of Orphans (children <18 with deceased parents):\n")
            for orphan in sorted(orphans, key=lambda x: x[2]):  # Sort by age
                indi_id, name, age, fam_id = orphan
                f.write(f"- {name} (ID: {indi_id}), Age: {age}, Family: {fam_id}\n")
        else:
            f.write("PASSED: US33: There are no orphans.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Identifying orphans in {gedcom_file}...\n")

    orphans = list_orphans(gedcom_file)
    write_output(orphans)

    print("Orphan identification complete. Results saved to 'us33_output.txt'.")