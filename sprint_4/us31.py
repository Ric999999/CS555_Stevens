from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

def list_living_singles(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    individuals = {}  # {ID: {"NAME": str, "DEAT": bool, "FAMS": []}}
    current_id = None
    indi_section = False

    for i, line in enumerate(lines):
        parts = line.strip().split(" ", 2)
        if len(parts) < 2:
            continue

        level = parts[0]

        if level == "0" and len(parts) == 3:
            pointer, tag = parts[1], parts[2]
            if tag == "INDI":
                current_id = pointer
                individuals[current_id] = {"NAME": "", "DEAT": False, "FAMS": []}
                indi_section, fam_section = True, False
            elif tag == "FAM":
                indi_section, fam_section = False, True
            continue

        tag = parts[1]
        argument = parts[2] if len(parts) > 2 else ""

        if indi_section:
            if tag == "NAME":
                individuals[current_id]["NAME"] = argument
            elif tag == "FAMS":
                individuals[current_id]["FAMS"].append(argument)
            elif tag == "DEAT":
                individuals[current_id]["DEAT"] = True

    # Check for living singles
    singles = []

    for indi_id, data in individuals.items():
        is_alive = not data["DEAT"]
        is_unmarried = len(data["FAMS"]) == 0

        if is_alive and is_unmarried:
            singles.append(f"{indi_id}: {data['NAME']}")

    return singles

def write_output(results, output_path="us31_output.txt"):
    with open(output_path, "w") as f:
        if results:
            f.write("US31: Living single individuals:\n")
            for line in results:
                f.write(line + "\n")
        else:
            f.write("PASSED: US31: No living single individuals found.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking for living single individuals in {gedcom_file}...\n")

    results = list_living_singles(gedcom_file)
    write_output(results)

    print("Validation complete. Results saved to 'us31_output.txt'.")
