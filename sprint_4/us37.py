from datetime import datetime, timedelta

def parse_gedcom(filename):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None
    last_tag = None  # To keep track if DATE belongs to BIRT or DEAT

    with open(filename, "r") as file:
        for line in file:
            tokens = line.strip().split()
            if not tokens:
                continue

            level = tokens[0]
            if level == "0":
                current_individual = None
                current_family = None
                if len(tokens) >= 3 and tokens[2] == "INDI":
                    current_individual = tokens[1]
                    individuals[current_individual] = {
                        "NAME": None, "ALIVE": True, "BIRTH": None, "DEATH": None,
                        "SPOUSE": [], "CHILDREN": []
                    }
                elif len(tokens) >= 3 and tokens[2] == "FAM":
                    current_family = tokens[1]
                    families[current_family] = {"HUSB": None, "WIFE": None, "CHIL": []}

            elif level == "1":
                tag = tokens[1]
                last_tag = tag  # Track what the DATE will belong to

                if current_individual:
                    if tag == "NAME":
                        individuals[current_individual]["NAME"] = " ".join(tokens[2:])
                    elif tag == "DEAT":
                        individuals[current_individual]["ALIVE"] = False
                    elif tag == "FAMS":
                        individuals[current_individual]["SPOUSE"].append(tokens[2])
                elif current_family:
                    if tag in ["HUSB", "WIFE"]:
                        families[current_family][tag] = tokens[2]
                    elif tag == "CHIL":
                        families[current_family]["CHIL"].append(tokens[2])

            elif level == "2" and tokens[1] == "DATE":
                date_str = " ".join(tokens[2:])
                date_obj = datetime.strptime(date_str, "%d %b %Y")

                # Only assign dates to individuals if we are currently in one
                if current_individual:
                    if last_tag == "BIRT":
                        individuals[current_individual]["BIRTH"] = date_obj
                    elif last_tag == "DEAT":
                        individuals[current_individual]["DEATH"] = date_obj

    return individuals, families


def list_recent_deaths(individuals, families):
    """Find individuals who died in the last 30 days and list their spouses and children."""
    recent_deaths = []
    today = datetime.now()

    for indi_id, indi in individuals.items():
        if not indi["ALIVE"] and indi["DEATH"]:
            days_since_death = (today - indi["DEATH"]).days
            if days_since_death <= 30:
                name = indi["NAME"]
                recent_deaths.append(f"Recent Death: {name} (died {indi['DEATH'].strftime('%d %b %Y')})")

                # Find living spouses and children
                for fam_id in indi["SPOUSE"]:
                    fam = families.get(fam_id, {})
                    spouse_ids = [fam.get("HUSB"), fam.get("WIFE")]
                    for spouse_id in spouse_ids:
                        if spouse_id and spouse_id != indi_id:
                            spouse = individuals.get(spouse_id, {})
                            if spouse.get("ALIVE", False):
                                recent_deaths.append(f"  Living Spouse: {spouse.get('NAME')}")

                    for child_id in fam.get("CHIL", []):
                        child = individuals.get(child_id, {})
                        if child.get("ALIVE", False):
                            recent_deaths.append(f"  Living Descendant: {child.get('NAME')}")

    return recent_deaths


def write_output(results, output_file="us37_output.txt"):
    with open(output_file, "w") as f:
        if results:
            for line in results:
                f.write(line + "\n")
        else:
            f.write("No individuals died in the last 30 days.\n")


if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Processing recent deaths from {gedcom_file}...\n")

    individuals, families = parse_gedcom(gedcom_file)
    results = list_recent_deaths(individuals, families)
    write_output(results)

    print("Validation complete. Results saved to 'us37_output.txt'.")
