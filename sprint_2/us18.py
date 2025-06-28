from collections import defaultdict

def parse_gedcom(filename):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None

    with open(filename, "r") as file:
        for line in file:
            tokens = line.strip().split()
            if not tokens:
                continue

            level = tokens[0]
            if level == "0":
                if len(tokens) >= 3 and tokens[2] == "INDI":
                    current_individual = tokens[1].strip("@")
                    individuals[current_individual] = {"FAMC": [], "FAMS": []}
                elif len(tokens) >= 3 and tokens[2] == "FAM":
                    current_family = tokens[1].strip("@")
                    families[current_family] = {"HUSB": None, "WIFE": None, "CHIL": []}

            elif level == "1":
                tag = tokens[1]
                if tag in ["HUSB", "WIFE"] and current_family:
                    families[current_family][tag] = tokens[2].strip("@")
                elif tag == "CHIL" and current_family:
                    families[current_family]["CHIL"].append(tokens[2].strip("@"))
                elif tag == "FAMS" and current_individual:
                    individuals[current_individual]["FAMS"].append(tokens[2].strip("@"))
                elif tag == "FAMC" and current_individual:
                    individuals[current_individual]["FAMC"].append(tokens[2].strip("@"))

    return individuals, families

def check_sibling_marriage(filename):
    individuals, families = parse_gedcom(filename)
    errors = []

    # Build a map from family ID to set of children
    fam_children = {fam_id: set(info["CHIL"]) for fam_id, info in families.items()}

    # For each family (marriage), check if HUSB and WIFE share a FAMC
    for fam_id, fam in families.items():
        husb = fam["HUSB"]
        wife = fam["WIFE"]

        if not husb or not wife:
            continue

        # Get family sets for husband and wife
        husb_famc = set(individuals.get(husb, {}).get("FAMC", []))
        wife_famc = set(individuals.get(wife, {}).get("FAMC", []))

        # If they share a family as children, they're siblings
        if husb_famc & wife_famc:
            errors.append(
                f"ERROR: US18: Siblings {husb} and {wife} are married in family {fam_id}."
            )

    return errors

def write_output(errors, output_file="us18_output.txt"):
    with open(output_file, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("All marriages are valid. No siblings married each other.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking sibling marriages in {gedcom_file}...\n")

    errors = check_sibling_marriage(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us18_output.txt'.")
