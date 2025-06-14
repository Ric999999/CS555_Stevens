from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y")
    except ValueError:
        return None

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
                families[current_fam] = {}
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
                elif tag == "MARR":
                    if i + 1 < len(lines) and lines[i+1].strip().startswith("2 DATE"):
                        marriage_date = lines[i+1].strip().split("DATE")[1].strip()
                        families[current_fam]["married"] = parse_date(marriage_date)
                elif tag == "DIV":
                    if i + 1 < len(lines) and lines[i+1].strip().startswith("2 DATE"):
                        divorce_date = lines[i+1].strip().split("DATE")[1].strip()
                        families[current_fam]["divorced"] = parse_date(divorce_date)

    return individuals, families

def check_divorce_before_death(individuals, families):
    errors = []

    for fam_id, family in families.items():
        divorce_date = family.get("divorced")
        husband_id = family.get("husband")
        wife_id = family.get("wife")

        if not divorce_date:
            continue  # No divorce to check

        if husband_id and husband_id in individuals:
            husband_death = individuals[husband_id].get("death")
            if husband_death and divorce_date > husband_death:
                errors.append(
                    f"ERROR: US06: Divorce date {divorce_date.strftime('%d %b %Y')} "
                    f"is after husband's ({husband_id}) death on {husband_death.strftime('%d %b %Y')} in family {fam_id}"
                )

        if wife_id and wife_id in individuals:
            wife_death = individuals[wife_id].get("death")
            if wife_death and divorce_date > wife_death:
                errors.append(
                    f"ERROR: US06: Divorce date {divorce_date.strftime('%d %b %Y')} "
                    f"is after wife's ({wife_id}) death on {wife_death.strftime('%d %b %Y')} in family {fam_id}"
                )

    return errors

def write_output(errors, output_path="us06_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US06: All Divorces occurred before death of spouses.\n")

if __name__ == "__main__":
    gedcom_path = "../M1B6.ged"  # Adjust path if needed
    print(f"All marriages occur before death")

    individuals, families = parse_gedcom_file(gedcom_path)
    errors = check_divorce_before_death(individuals, families)
    write_output(errors)

    print("Validation complete. Results saved to 'us06_output.txt'.")
