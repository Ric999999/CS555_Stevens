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
                elif tag == "DEAT":
                    if i + 1 < len(lines) and lines[i+1].strip().startswith("2 DATE"):
                        death_date = lines[i+1].strip().split("DATE")[1].strip()
                        individuals[current_indi]["death"] = parse_date(death_date)

    return individuals

def list_recent_deaths(individuals):
    recent_deaths = []
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)

    for indi_id, data in individuals.items():
        death_date = data.get("death")
        if death_date and thirty_days_ago <= death_date <= today:
            recent_deaths.append(
                f"US36: RECENT DEATH: {data.get('name', 'Unknown')} ({indi_id}) died on {death_date.strftime('%d %b %Y')}"
            )

    return recent_deaths

def write_output(recent_deaths, output_path="us36_output.txt"):
    with open(output_path, "w") as f:
        if recent_deaths:
            for entry in recent_deaths:
                f.write(entry + "\n")
        else:
            f.write("PASSED: US36: No individuals died in the last 30 days.\n")

if __name__ == "__main__":
    gedcom_path = "../M1B6.ged"
    print("Checking for recent deaths (last 30 days)...")

    individuals = parse_gedcom_file(gedcom_path)
    recent_deaths = list_recent_deaths(individuals)
    write_output(recent_deaths)
