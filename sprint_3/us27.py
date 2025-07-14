from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y")
    except ValueError:
        return None

def calculate_age(birth_date, death_date=None):
    today = datetime.today()
    end_date = death_date if death_date else today
    return end_date.year - birth_date.year - ((end_date.month, end_date.day) < (birth_date.month, birth_date.day))

def parse_gedcom(filename):
    individuals = {}
    current_individual = None
    birth_flag = False
    death_flag = False

    with open(filename, "r") as file:
        for line in file:
            tokens = line.strip().split(" ", 2)
            if not tokens:
                continue

            level = tokens[0]

            if level == "0":
                if len(tokens) >= 3 and tokens[2] == "INDI":
                    current_individual = tokens[1].strip("@")
                    individuals[current_individual] = {"NAME": "", "BIRT": None, "DEAT": None}
                    birth_flag = False
                    death_flag = False
                else:
                    current_individual = None  # not an individual record
            elif current_individual:
                tag = tokens[1]
                args = tokens[2] if len(tokens) > 2 else ""

                if tag == "NAME":
                    individuals[current_individual]["NAME"] = args
                elif tag == "BIRT":
                    birth_flag = True
                elif tag == "DEAT":
                    death_flag = True
                elif tag == "DATE":
                    date = parse_date(args)
                    if birth_flag:
                        individuals[current_individual]["BIRT"] = date
                        birth_flag = False
                    elif death_flag:
                        individuals[current_individual]["DEAT"] = date
                        death_flag = False

    return individuals

def list_individuals_with_age(gedcom_file, output_file):
    individuals = parse_gedcom(gedcom_file)
    with open(output_file, "w") as f:
        for ind_id, info in individuals.items():
            name = info.get("NAME", "(no name)")
            birth = info.get("BIRT")
            death = info.get("DEAT")

            if birth:
                age = calculate_age(birth, death)
                if death:
                    age_info = f"Age at death: {age}"
                else:
                    age_info = f"Current age: {age}"
            else:
                age_info = "Birth date unknown"

            f.write(f"{ind_id}: {name}, {age_info}\n")

if __name__ == "__main__":
    gedcom_path = "../M1B6.ged"
    output_path = "us27_output.txt"
    print(f"Processing individuals from {gedcom_path}...\n")
    list_individuals_with_age(gedcom_path, output_path)
    print(f"Results saved to '{output_path}'.")
