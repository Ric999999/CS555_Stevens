import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gedcom_parser import process_gedcom_file

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), '%d %b %Y')
    except (ValueError, TypeError, AttributeError):
        return None

def us39_upcoming_birthdays(individuals):
    """Return list of (ID, Name, Birthday) for individuals with birthdays in next 30 days."""
    today = datetime.today()
    upcoming_birthdays = []

    for indi_id, indi in individuals.items():
        if indi.get("death"):
            continue  # Skip deceased

        birth_str = indi.get("birth")
        birth_date = parse_date(birth_str)
        if not birth_date:
            continue

        next_birthday = birth_date.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        days_until = (next_birthday - today).days
        if 0 <= days_until <= 30:
            upcoming_birthdays.append((indi_id, indi.get("name", "Unknown"), birth_date.strftime("%d %b")))

    return upcoming_birthdays

def write_output(birthdays):
    output_file = os.path.join(os.path.dirname(__file__), "us39_output.txt")
    with open(output_file, "w") as out_file:
        if birthdays:
            out_file.write("US39 - Upcoming Birthdays in Next 30 Days:\n")
            for indi_id, name, date in birthdays:
                out_file.write(f"{indi_id}: {name}, Birthday on {date}\n")
        else:
            out_file.write("US39 - No upcoming birthdays found in the next 30 days.\n")

if __name__ == "__main__":
    gedcom_file = "/Users/jeremy/Documents/GitHub/CS555_Stevens/M1B6.ged"
    print(f"Checking for upcoming birthdays in {gedcom_file}...\n")

    individuals, families = process_gedcom_file(gedcom_file)
    birthdays = us39_upcoming_birthdays(individuals)
    write_output(birthdays)

    print("Validation complete. Results saved to 'us39_output.txt'.")
