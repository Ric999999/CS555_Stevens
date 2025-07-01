from collections import defaultdict
import sys


def normalize_name(name):
    """Normalize names by removing slashes and extra spaces, case insensitive"""
    normalized = ' '.join(name.replace("/", "").strip().lower().split())
    return normalized if normalized != "unknown" else None


def process_gedcom(filename, test_mode=False):
    individuals = {}
    families = defaultdict(dict)
    current_indi = None
    current_fam = None
    error_found = False

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(' ', 2)
            level = parts[0]
            tag = parts[1] if len(parts) > 1 else ''
            args = parts[2] if len(parts) > 2 else ''

            if level == '0' and args == 'INDI':
                current_indi = tag
                individuals[current_indi] = {'name': 'Unknown'}

            elif level == '0' and args.startswith('FAM'):
                current_fam = tag
                families[current_fam] = {'husband': None, 'wife': None}

            elif level == '1' and current_indi:
                if tag == 'NAME':
                    individuals[current_indi]['name'] = args

            elif level == '1' and current_fam:
                if tag == 'HUSB':
                    families[current_fam]['husband'] = args
                elif tag == 'WIFE':
                    families[current_fam]['wife'] = args

    seen_pairs = set()

    for fam_id, fam_data in families.items():
        husb_id = fam_data.get('husband')
        wife_id = fam_data.get('wife')

        husb_name = normalize_name(individuals.get(husb_id, {}).get('name', 'Unknown'))
        wife_name = normalize_name(individuals.get(wife_id, {}).get('name', 'Unknown'))

        # Skip if either spouse is unknown
        if husb_name is None or wife_name is None:
            continue

        spouse_pair = tuple(sorted((husb_name, wife_name)))

        if spouse_pair in seen_pairs:
            print(f"Error: US24: Duplicate spouse pair in family {fam_id}")
            error_found = True
        else:
            seen_pairs.add(spouse_pair)

    if not error_found:
        with open("us24_output.txt", "w") as f:
            f.write("PASSED: US24: No more than one family with the same spouses by name\n")
        if not test_mode:
            print("PASSED: US24: No more than one family with the same spouses by name")

    if test_mode:
        return not error_found
    sys.exit(1 if error_found else 0)


if __name__ == "__main__":
    gedcom_file = sys.argv[1] if len(sys.argv) > 1 else "../M1B6.ged"
    process_gedcom(gedcom_file)