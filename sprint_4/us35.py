from datetime import datetime, timedelta

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y")
    except ValueError:
        return None

def parse_gedcom_file(file_path):
    individuals = {}
    current_indi = None

    with open(file_path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        parts = lines[i].strip().split(" ", 2)
        level = parts[0]

        if level == "0":
            if len(parts) == 3 and parts[2] == "INDI":
                current_indi = parts[1].strip()
                individuals[current_indi] = {}
            else:
                current_indi = None
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

    return individuals

def list_recent_births(individuals):
    recent_births = []
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)

    for indi_id, data in individuals.items():
        birth_date = data.get("birth")
        if birth_date and thirty_days_ago <= birth_date <= today:
            recent_births.append(
                f"US35: RECENT BIRTH: {data.get('name', 'Unknown')} ({indi_id}) was born on {birth_date.strftime('%d %b %Y')}"
            )

    return recent_births

def write_output(recent_births, output_path="us35_output.txt"):
    with open(output_path, "w") as f:
        if recent_births:
            for entry in recent_births:
                f.write(entry + "\n")
        else:
            f.write("PASSED: US35: No individuals born in the last 30 days.\n")

if __name__ == "__main__":
    gedcom_path = "../M1B6.ged"
    print(f"Checking for recent births (last 30 days)...")

    individuals = parse_gedcom_file(gedcom_path)
    recent_births = list_recent_births(individuals)
    write_output(recent_births)