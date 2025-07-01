#No more than one individual with the same name and birth

import sys
from datetime import datetime
from collections import defaultdict


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d %b %Y')
    except ValueError:
        return None


def process_gedcom(filename):
    individuals = {}
    families = defaultdict(dict)
    current_indi = None
    current_fam = None
    birth_date = None
    birth_flag = False
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
                birth_flag = False

            elif level == '0' and args.startswith('FAM'):
                current_fam = tag
                families[current_fam] = {'children': []}

            elif level == '1' and current_indi:
                if tag == 'NAME':
                    individuals[current_indi]['name'] = args
                elif tag == 'BIRT':
                    birth_flag = True
                elif tag == 'FAMC':
                    if 'famc' not in individuals[current_indi]:
                        individuals[current_indi]['famc'] = []
                    individuals[current_indi]['famc'].append(args)

            elif level == '1' and current_fam:
                if tag == 'HUSB':
                    families[current_fam]['husband'] = args
                elif tag == 'WIFE':
                    families[current_fam]['wife'] = args
                elif tag == 'CHIL':
                    families[current_fam]['children'].append(args)

            elif level == '2' and tag == 'DATE' and current_indi and birth_flag:
                date = parse_date(args)
                if date:
                    individuals[current_indi]['birth'] = date
                    birth_flag = False

    # Check for duplicate name+birth in families
    for fam_id, fam_data in families.items():
        seen = set()
        for child_id in fam_data.get('children', []):
            if child_id in individuals:
                name = individuals[child_id]['name']
                birth = individuals[child_id].get('birth')
                if birth:
                    key = (name, birth)
                    if key in seen:
                        print(f"Error: US23: Family {fam_id} has multiple individuals named "
                              f"'{name}' born on {birth.strftime('%d %b %Y')}")
                        error_found = True
                    seen.add(key)

    if not error_found:
        with open("us23_output.txt", "w") as out_file:
            out_file.write("PASSED: US23: No more than one individual with the same name and birth\n")


if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    process_gedcom(gedcom_file)