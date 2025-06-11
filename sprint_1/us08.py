#birth before marriage
from datetime import datetime
from dateutil.relativedelta import relativedelta

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%d %b %Y")
    except:
        return None

def parse_gedcom(gedcom_file):
    individuals = {}
    families = {}
    current_id = None
    in_individual = False
    in_family = False
    current_tag = None

    with open(gedcom_file, "r") as file:
        for line in file:
            parts = line.strip().split(" ", 2)
            if not parts:
                continue
            level = parts[0]

            if level == "0":
                current_tag = None
                if len(parts) == 3:
                    if parts[2] == "INDI":
                        current_id = parts[1].strip("@")
                        individuals[current_id] = {"birth": None, "famc": None}
                        in_individual = True
                        in_family = False
                    elif parts[2] == "FAM":
                        current_id = parts[1].strip("@")
                        families[current_id] = {"marriage": None, "divorce": None, "children": []}
                        in_family = True
                        in_individual = False
            elif level == "1":
                tag = parts[1]
                current_tag = tag
                if in_individual:
                    if tag == "BIRT":
                        current_tag = "BIRT"
                    elif tag == "FAMC":
                        individuals[current_id]["famc"] = parts[2].strip("@")
                        current_tag = None
                elif in_family:
                    if tag in ["MARR", "DIV"]:
                        current_tag = tag
                    elif tag == "CHIL":
                        families[current_id]["children"].append(parts[2].strip("@"))
                        current_tag = None
            elif level == "2" and parts[1] == "DATE":
                date = parse_date(parts[2])
                if in_individual and current_tag == "BIRT":
                    individuals[current_id]["birth"] = date
                elif in_family:
                    if current_tag == "MARR":
                        families[current_id]["marriage"] = date
                    elif current_tag == "DIV":
                        families[current_id]["divorce"] = date

    return individuals, families

def check_birth_before_marriage(individuals, families):
    errors = []
    for fam_id, fam in families.items():
        marriage = fam["marriage"]
        divorce = fam["divorce"]
        for child_id in fam["children"]:
            birth = individuals.get(child_id, {}).get("birth")
            if not birth:
                continue
            if marriage and birth < marriage:
                errors.append(f"ERROR US08: FAMILY {fam_id} - Child {child_id} born before marriage date {marriage.strftime('%d %b %Y')}")
            if divorce and birth > divorce + relativedelta(months=+9):
                errors.append(f"ERROR US08: FAMILY {fam_id} - Child {child_id} born more than 9 months after divorce on {divorce.strftime('%d %b %Y')}")
    return errors

def write_output(errors, output_file):
    with open(output_file, "w") as f:
        if errors:
            f.write("US08 - BIRTH BEFORE MARRIAGE VALIDATION FAILED:\n" + "\n".join(errors))
        else:
            f.write("US08 - BIRTH BEFORE MARRIAGE VALIDATION PASSED: All children born within valid parental marriage windows.")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    output_file = "us08_output.txt"
    print(f"Checking parental marriage constraints in {gedcom_file}...\n")

    individuals, families = parse_gedcom(gedcom_file)
    errors = check_birth_before_marriage(individuals, families)
    write_output(errors, output_file)

    print("Validation complete. Results saved to 'us08_output.txt'.")
