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

def us40_upcoming_anniversaries(individuals, families):
    """Return list of (fam_id, Husband Name, Wife Name, Anniversary Date) for couples with upcoming anniversaries."""
    today = datetime.today()
    upcoming_anniversaries = []

    for fam_id, fam in families.items():
        married_str = fam.get("married")
        if not married_str:
            continue

        marriage_date = parse_date(married_str)
        if not marriage_date:
            continue

        husb_id = fam.get("husb")
        wife_id = fam.get("wife")

        if not husb_id or not wife_id:
            continue

        husb = individuals.get(husb_id, {})
        wife = individuals.get(wife_id, {})

        if husb.get("death") or wife.get("death"):
            continue  # skip if either spouse is deceased

        anniversary = marriage_date.replace(year=today.year)
        if anniversary < today:
            anniversary = anniversary.replace(year=today.year + 1)

        days_until = (anniversary - today).days
        if 0 <= days_until <= 30:
            husb_name = husb.get("name", "Unknown")
            wife_name = wife.get("name", "Unknown")
            formatted_date = marriage_date.strftime("%d %b")
            upcoming_anniversaries.append((fam_id, husb_name, wife_name, formatted_date))

    return upcoming_anniversaries

def write_output(anniversaries):
    output_file = os.path.join(os.path.dirname(__file__), "us40_output.txt")
    with open(output_file, "w") as out_file:
        if anniversaries:
            out_file.write("US40 - Upcoming Anniversaries in Next 30 Days:\n")
            for fam_id, husb, wife, date in anniversaries:
                out_file.write(f"{fam_id}: {husb} and {wife}, Anniversary on {date}\n")
        else:
            out_file.write("US40 - No upcoming anniversaries found in the next 30 days.\n")

if __name__ == "__main__":
    gedcom_file = "/Users/jeremy/Documents/GitHub/CS555_Stevens/M1B6.ged"
    print(f"Checking for upcoming anniversaries in {gedcom_file}...\n")

    individuals, families = process_gedcom_file(gedcom_file)
    anniversaries = us40_upcoming_anniversaries(individuals, families)
    write_output(anniversaries)

    print("Validation complete. Results saved to 'us40_output.txt'.")
