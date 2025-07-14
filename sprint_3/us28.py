from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y")
    except ValueError:
        return None

def calculate_age(birth_date):
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def parse_gedcom(filename):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None
    birth_flag = False

    with open(filename, "r") as file:
        for line in file:
            tokens = line.strip().split(" ", 2)
            if not tokens:
                continue

            level = tokens[0]

            if level == "0":
                if len(tokens) >= 3 and tokens[2] == "INDI":
                    current_individual = tokens[1].strip("@")
                    individuals[current_individual] = {"NAME": "", "BIRT": None}
                    birth_flag = False
                elif len(tokens) >= 3 and tokens[2] == "FAM":
                    current_family = tokens[1].strip("@")
                    families[current_family] = {"CHIL": []}
                    current_individual = None
                else:
                    current_individual = None
                    current_family = None
            elif current_individual:
                tag = tokens[1]
                args = tokens[2] if len(tokens) > 2 else ""
                if tag == "NAME":
                    individuals[current_individual]["NAME"] = args
                elif tag == "BIRT":
                    birth_flag = True
                elif tag == "DATE" and birth_flag:
                    individuals[current_individual]["BIRT"] = parse_date(args)
                    birth_flag = False
            elif current_family:
                tag = tokens[1]
                args = tokens[2] if len(tokens) > 2 else ""
                if tag == "CHIL":
                    families[current_family]["CHIL"].append(args.strip("@"))

    return individuals, families

def list_siblings_by_age(gedcom_file, output_file):
    individuals, families = parse_gedcom(gedcom_file)

    with open(output_file, "w") as f:
        for fam_id, fam in families.items():
            children = fam.get("CHIL", [])
            sibling_list = []

            for child_id in children:
                individual = individuals.get(child_id)
                if individual and individual.get("BIRT"):
                    age = calculate_age(individual["BIRT"])
                    sibling_list.append((individual["NAME"], age))
                else:
                    sibling_list.append((individual["NAME"] if individual else "Unknown", "Unknown"))

            sibling_list.sort(key=lambda x: (x[1] if isinstance(x[1], int) else -1), reverse=True)

            f.write(f"Family {fam_id} Siblings by Age (Oldest First):\n")
            for name, age in sibling_list:
                f.write(f"  {name}, Age: {age}\n")
            f.write("\n")

if __name__ == "__main__":
    gedcom_path = "../M1B6.ged"
    output_path = "us28_output.txt"
    print(f"Listing siblings by age from {gedcom_path}...\n")
    list_siblings_by_age(gedcom_path, output_path)
    print(f"Results saved to '{output_path}'.")
