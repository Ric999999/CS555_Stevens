from datetime import datetime

def parse_date(date_str):
    """Convert GEDCOM date string to datetime.date object"""
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

def calculate_age(birth_date, reference_date=None):
    """Calculate age at reference date (or current date if None)"""
    if not birth_date:
        return 0
    ref_date = reference_date or datetime.now().date()
    age = ref_date.year - birth_date.year
    if (ref_date.month, ref_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

def list_large_age_differences(file_path):
    """Identify couples where one spouse is at least twice as old as the other"""
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}  # {ID: {"name": str, "birth": date}}
    families = {}     # {ID: {"HUSB": id, "WIFE": id, "MARR_DATE": date}}
    large_age_diffs = []

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
                    individuals[current_id] = {"name": "Unknown", "birth": None}
                    indi_section, fam_section = True, False
                elif tag == "FAM":
                    current_id = pointer
                    families[current_id] = {"HUSB": None, "WIFE": None, "MARR_DATE": None}
                    fam_section, indi_section = True, False
            continue

        tag = parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if indi_section:
            if tag == "NAME":
                individuals[current_id]["name"] = argument
            elif tag == "BIRT":
                current_tag = "BIRT"
            elif tag == "DATE" and current_tag == "BIRT":
                individuals[current_id]["birth"] = parse_date(argument)
                current_tag = None

        elif fam_section:
            if tag in {"HUSB", "WIFE"}:
                families[current_id][tag] = argument
            elif tag == "MARR":
                current_tag = "MARR"
            elif tag == "DATE" and current_tag == "MARR":
                families[current_id]["MARR_DATE"] = parse_date(argument)
                current_tag = None

    # Check age differences
    for fam_id, fam_data in families.items():
        husband_id = fam_data.get("HUSB")
        wife_id = fam_data.get("WIFE")
        marriage_date = fam_data.get("MARR_DATE")

        if not husband_id or not wife_id or not marriage_date:
            continue

        husband = individuals.get(husband_id, {})
        wife = individuals.get(wife_id, {})

        if not husband.get("birth") or not wife.get("birth"):
            continue

        hub_age = calculate_age(husband["birth"], marriage_date)
        wife_age = calculate_age(wife["birth"], marriage_date)

        if hub_age >= 2 * wife_age:
            large_age_diffs.append((
                fam_id,
                husband["name"],
                hub_age,
                wife["name"],
                wife_age
            ))
        elif wife_age >= 2 * hub_age:
            large_age_diffs.append((
                fam_id,
                wife["name"],
                wife_age,
                husband["name"],
                hub_age
            ))

    return large_age_diffs

def write_output(results, output_path="us34_output.txt"):
    """Write results to output file"""
    with open(output_path, "w") as f:
        if results:
            f.write("US34: Couples with large age differences (≥2X):\n")
            for fam_id, older_name, older_age, younger_name, younger_age in results:
                ratio = older_age / younger_age
                f.write(
                    f"- Family {fam_id}: {older_name} ({older_age} years) is "
                    f"{ratio:.1f}x older than {younger_name} ({younger_age} years)\n"
                )
        else:
            f.write("PASSED: US34: No large (>2X) age differences found.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking for large age differences in {gedcom_file}...\n")

    large_diffs = list_large_age_differences(gedcom_file)
    write_output(large_diffs)

    print("Age difference check complete. Results saved to 'us34_output.txt'.")