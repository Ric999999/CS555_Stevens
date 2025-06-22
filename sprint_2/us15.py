import sys
from collections import defaultdict

def process_gedcom(filename):
    families = defaultdict(dict)
    current_fam = None
    error_found = False

    # First pass: collect family data
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(' ', 2)
            level = parts[0]
            tag = parts[1] if len(parts) > 1 else ''
            args = parts[2] if len(parts) > 2 else ''

            if level == '0' and args.startswith('FAM'):
                current_fam = tag
                families[current_fam] = {'children': []}

            elif level == '1' and current_fam:
                if tag == 'HUSB':
                    families[current_fam]['husband'] = args
                elif tag == 'WIFE':
                    families[current_fam]['wife'] = args
                elif tag == 'CHIL':
                    families[current_fam]['children'].append(args)

    # Check for families with 15+ siblings
    for fam_id, fam_data in families.items():
        siblings = fam_data.get('children', [])
        if len(siblings) >= 15:
            husband = fam_data.get('husband', 'Unknown')
            wife = fam_data.get('wife', 'Unknown')
            print(f"Error: US15: Family {fam_id} ({husband} and {wife}) "
                  f"has {len(siblings)} siblings (max 15 allowed)")
            error_found = True

    if not error_found:
        with open("us15_output.txt", "w") as out_file:
            out_file.write("PASSED: US15: Number of Siblings <= 15\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    process_gedcom(gedcom_file)