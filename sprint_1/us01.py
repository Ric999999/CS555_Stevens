from datetime import datetime

def is_date_before_today(date_str):
    """
    Checks if the given GEDCOM date string is before today's date.
    GEDCOM format is expected to be 'DD MON YYYY', e.g., '15 MAY 1940'.
    """
    try:
        date = datetime.strptime(date_str, "%d %b %Y")
        return date < datetime.today()
    except ValueError:
        return False

def check_dates_before_today(file_path):
    """
    Reads a GEDCOM file and checks all BIRT, DEAT, MARR, and DIV dates
    to ensure they are before the current date.
    Returns a list of error strings.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    errors = []
    current_entity = ""
    date_tag = None

    for i, line in enumerate(lines):
        parts = line.strip().split(' ', 2)
        if len(parts) < 2:
            continue

        level, tag = parts[0], parts[1]

        # Track current individual/family ID
        if tag == "INDI" or tag == "FAM":
            current_entity = parts[2] if len(parts) > 2 else ""

        if tag in {"BIRT", "DEAT", "MARR", "DIV"}:
            date_tag = tag

        elif tag == "DATE" and date_tag:
            date_str = parts[2] if len(parts) > 2 else ""
            if not is_date_before_today(date_str):
                errors.append(
                    f"ERROR: US01: {date_tag} date '{date_str}' for {current_entity} "
                    f"is not before today's date (line {i+1})"
                )
            date_tag = None

    return errors

def write_output(errors, output_path="us01_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("All dates are valid and occur before today's date.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking dates in {gedcom_file}...\n")

    errors = check_dates_before_today(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us01_output.txt'.")
