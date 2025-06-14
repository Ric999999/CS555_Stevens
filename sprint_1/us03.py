import sys
from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d %b %Y')
    except ValueError:
        return None

def process_gedcom(filename):
    individuals = {}
    current_indi = None
    birth_date = None
    death_date = None
    birth_flag = False
    death_flag = False
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
                # Check previous individual for birth > death
                if current_indi and birth_date and death_date and birth_date > death_date:
                    name = individuals[current_indi]['name']
                    print(f"Error: {current_indi} {name} - "
                          f"Born: {birth_date.strftime('%d %b %Y')}, "
                          f"Died: {death_date.strftime('%d %b %Y')}")
                    error_found = True

                current_indi = tag
                birth_date = None
                death_date = None
                birth_flag = False
                death_flag = False
                individuals[current_indi] = {'name': 'Unknown'}

            elif level == '1' and current_indi:
                if tag == 'NAME':
                    individuals[current_indi]['name'] = args
                elif tag == 'BIRT':
                    birth_flag = True
                    death_flag = False
                elif tag == 'DEAT':
                    death_flag = True
                    birth_flag = False

            elif level == '2' and tag == 'DATE' and current_indi:
                date = parse_date(args)
                if date:
                    if birth_flag:
                        birth_date = date
                        individuals[current_indi]['birth'] = date
                        birth_flag = False
                    elif death_flag:
                        death_date = date
                        individuals[current_indi]['death'] = date
                        death_flag = False

                        if birth_date and birth_date > death_date:
                            name = individuals[current_indi]['name']
                            print(f"Error: {current_indi} {name} - "
                                  f"Born: {birth_date.strftime('%d %b %Y')}, "
                                  f"Died: {death_date.strftime('%d %b %Y')}")
                            error_found = True

    if current_indi and birth_date and death_date and birth_date > death_date:
        name = individuals[current_indi]['name']
        print(f"Error: {current_indi} {name} - "
              f"Born: {birth_date.strftime('%d %b %Y')}, "
              f"Died: {death_date.strftime('%d %b %Y')}")
        error_found = True

    if not error_found:
        with open("output.txt", "w") as out_file:
            out_file.write("PASSED: US03: All Births before Death.\n")

if __name__ == "__main__":
    gedcom_file = "../M1B6.ged"
    process_gedcom(gedcom_file)