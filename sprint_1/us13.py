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

    for fam_id, fam_data in families.items():
        children = fam_data.get('children', [])
        if len(children) < 2:
            continue

        siblings = []
        for child_id in children:
            if child_id in individuals and 'birth' in individuals[child_id]:
                siblings.append((child_id, individuals[child_id]['birth']))

        siblings.sort(key=lambda x: x[1])

        for i in range(len(siblings) - 1):
            child1, date1 = siblings[i]
            child2, date2 = siblings[i + 1]

            delta = date2 - date1
            days_diff = delta.days

            if 2 <= days_diff < 243.5:
                name1 = individuals[child1]['name']
                name2 = individuals[child2]['name']
                print(f"Error: US13: Siblings {child1} {name1} and {child2} {name2} "
                      f"have invalid spacing: {days_diff} days apart "
                      f"({date1.strftime('%d %b %Y')} and {date2.strftime('%d %b %Y')})")
                error_found = True

    if not error_found:
        with open("us13_output.txt", "w") as out_file:
            out_file.write("PASSED: US13: Sibling Spacing Correct\n")


if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    process_gedcom(gedcom_file)