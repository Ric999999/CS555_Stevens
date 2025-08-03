from datetime import datetime, timedelta

def parse_gedcom(filename):
    individuals = {}
    current_individual = None
    pending_birth = False

    with open(filename, "r") as file:
        for line in file:
            tokens = line.strip().split()
            if not tokens:
                continue

            level = tokens[0]
            if level == "0" and len(tokens) >= 3 and tokens[2] == "INDI":
                current_individual = tokens[1].strip("@")
                individuals[current_individual] = {"NAME": "", "BIRT": None, "ALIVE": True}
            elif level == "1":
                tag = tokens[1]
                if tag == "NAME" and current_individual:
                    individuals[current_individual]["NAME"] = " ".join(tokens[2:])
                elif tag == "DEAT" and current_individual:
                    individuals[current_individual]["ALIVE"] = False
                elif tag == "BIRT" and current_individual:
                    pending_birth = True
            elif level == "2" and tokens[1] == "DATE" and pending_birth and current_individual:
                try:
                    individuals[current_individual]["BIRT"] = datetime.strptime(" ".join(tokens[2:]), "%d %b %Y")
                except ValueError:
                    print(f"Invalid date format for {individuals[current_individual]['NAME']}: {' '.join(tokens[2:])}")
                pending_birth = False

    return individuals

def list_upcoming_birthdays(individuals):
    today = datetime.today()
    next_30_days = today + timedelta(days=30)
    upcoming = []

    for indi_id, indi in individuals.items():
        if indi["ALIVE"] and indi["BIRT"]:
            # Adjust birthday year to the current year
            birthday_this_year = indi["BIRT"].replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # Debugging
            #print(f"Checking {indi['NAME']} -> Birthday: {birthday_this_year.strftime('%d %b %Y')}")

            if today <= birthday_this_year <= next_30_days:
                upcoming.append(f"{indi['NAME']} has a birthday on {birthday_this_year.strftime('%d %b')}")

    return upcoming

def write_output(upcoming, output_file):
    with open(output_file, "w") as f:
        if upcoming:
            f.write("Upcoming birthdays in the next 30 days:\n")
            for entry in upcoming:
                f.write(entry + "\n")
        else:
            f.write("No upcoming birthdays in the next 30 days.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    output_file = "us38_output.txt"

    print(f"Processing birthdays from {gedcom_file}...\n")
    individuals = parse_gedcom(gedcom_file)
    upcoming = list_upcoming_birthdays(individuals)
    write_output(upcoming, output_file)

    print(f"\nValidation complete. Results saved to '{output_file}'.")
