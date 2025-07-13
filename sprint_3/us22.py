def check_unique_ids(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    indi_ids = set()
    fam_ids = set()
    errors = []

    seen = set()

    for line in lines:
        parts = line.strip().split(" ", 2)
        if len(parts) == 3 and parts[0] == "0":
            pointer, tag = parts[1], parts[2]
            if tag == "INDI":
                if pointer in seen:
                    errors.append(f"ERROR: US22: Duplicate individual ID {pointer}.")
                else:
                    seen.add(pointer)
                    indi_ids.add(pointer)
            elif tag == "FAM":
                if pointer in seen:
                    errors.append(f"ERROR: US22: Duplicate family ID {pointer}.")
                else:
                    seen.add(pointer)
                    fam_ids.add(pointer)

    return errors

def write_output(errors, output_path="us22_output.txt"):
    with open(output_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("PASSED: US22: All individual and family IDs are unique.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    print(f"Checking unique IDs in {gedcom_file}...\n")

    errors = check_unique_ids(gedcom_file)
    write_output(errors)

    print("Validation complete. Results saved to 'us22_output.txt'.")
