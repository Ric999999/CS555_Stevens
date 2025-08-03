from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

def list_multiple_births(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}  # {ID: {"NAME": str, "BIRT": date}}
    families = {}     # {ID: {"CHIL": [IDs]}}
    current_id = None
    indi_section = False
    fam_section = False

    for i, line in enumerate(lines):
        parts = line.strip().split(" ", 2)
        if len(parts) < 2:
            continue

        level = parts[0]

        if level == "0" and len(parts) == 3:
            pointer, tag = parts[1], parts[2]
            if tag == "INDI":
                current_id = pointer
                individuals[current_id] = {"NAME": "", "BIRT": None}
                indi_section, fam_section = True, False
            elif tag == "FAM":
                current_id = pointer
                families[current_id] = {"CHIL": []}
                fam_section, indi_section = True, False
            continue

        tag = parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if indi_section:
            if tag == "NAME":
                individuals[current_id]["NAME"] = argument
            elif tag == "BIRT":
                next_line = lines[i + 1].strip()
                if next_line.startswith("2 DATE"):
                    birthdate = parse_date(next_line[7:])
                    individuals[current_id]["BIRT"] = birthdate

        elif fam_section:
            if tag == "CHIL":
                families[current_id]["CHIL"].append(argument)

    # Identify multiple births
    results = []

    for fam_id, fam_data in families.items():
        birth_groups = {}  # {date: [IDs]}
        for child_id in fam_data["CHIL"]:
            birth = individuals.get(child_id, {}).get("BIRT")
            if birth:
                birth_groups.setdefault(birth, []).append(child_id)

        for birth_date, ids in birth_groups.items():
            if len(ids) > 1:
                label = birth_date.strftime("%d %b %Y") if birth_date else "Unknown"
                line = f"US32: Family {fam_id} has multiple births on {label}:"
                for cid in ids:
                    name = individuals[cid]["NAME"]
                    line += f" {cid} ({name}),"
                results.append(line.rstrip(','))

    return results

def write_output(results, output_path="us32_output.txt"):
    with open(output_path, "w") as f:
        if results:
            for line in results:
                f.write(line + "\n")
        else:
            f.write("PASSED: US32: No multiple births found.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking for multiple births in {gedcom_file}...\n")

    results = list_multiple_births(gedcom_file)
    write_output(results)

    print("Validation complete. Results saved to 'us32_output.txt'.")
