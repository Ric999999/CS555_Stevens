#lifespan validation
from datetime import datetime
from dateutil.relativedelta import relativedelta

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%d %b %Y")
    except:
        return None

def parse_individuals(filename):
    individuals = {}
    current_id = None
    current_tag = None

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(" ", 2)
            if not parts:
                continue
            level = parts[0]
            if level == "0" and len(parts) == 3 and parts[2] == "INDI":
                current_id = parts[1].strip("@")
                individuals[current_id] = {"birth": None, "death": None}
            elif level == "1":
                tag = parts[1]
                if tag in ["BIRT", "DEAT"]:
                    current_tag = tag
                else:
                    current_tag = None
            elif level == "2" and parts[1] == "DATE" and current_tag:
                date = parse_date(parts[2])
                if date:
                    individuals[current_id][current_tag.lower()] = date
    return individuals

def check_lifespan(individuals):
    today = datetime.today()
    errors = []

    for indi_id, data in individuals.items():
        birth = data["birth"]
        death = data["death"]
        if not birth:
            continue
        if death:
            age = relativedelta(death, birth).years
            if age > 150:
                errors.append(f"ERROR US07: INDIVIDUAL {indi_id} lived more than 150 years: {age}")
        else:
            age = relativedelta(today, birth).years
            if age > 150:
                errors.append(f"ERROR US07: INDIVIDUAL {indi_id} is alive and older than 150 years: {age}")
    return errors

def write_output(errors, output_file):
    with open(output_file, "w") as f:
        if errors:
            f.write("US07 - LIFESPAN VALIDATION FAILED:\n" + "\n".join(errors))
        else:
            f.write("US07 - LIFESPAN VALIDATION PASSED: All individuals are under 150 years old.")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    output_file = "us07_output.txt"
    print(f"Checking lifespan rules in {gedcom_file}...\n")

    individuals = parse_individuals(gedcom_file)
    errors = check_lifespan(individuals)
    write_output(errors, output_file)

    print("Validation complete. Results saved to 'us07_output.txt'.")
