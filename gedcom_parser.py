from datetime import datetime

def parse_gedcom_line(line):
    line = line.strip()
    if not line:
        return None

    tokens = line.split(' ', 2)
    level = tokens[0]

    if level == '0':
        if len(tokens) > 2 and tokens[2] in ['INDI', 'FAM']:
            tag = tokens[2]
            arguments = tokens[1]
        else:
            tag = tokens[1] if len(tokens) > 1 else ''
            arguments = tokens[2] if len(tokens) > 2 else ''
    else:
        tag = tokens[1] if len(tokens) > 1 else ''
        arguments = tokens[2] if len(tokens) > 2 else ''

    return level, tag, arguments

def is_valid_tag(level, tag):
    valid_tags = {
        '0': ['INDI', 'FAM', 'HEAD', 'TRLR', 'NOTE'],
        '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'],
        '2': ['DATE']
    }

    if level == '1' and tag == 'DATE':
        return False

    return tag in valid_tags.get(level, [])

def process_gedcom_file(filename):
    individuals = {}
    families = {}
    current_indi = None
    current_fam = None
    # Flags to track whether the next DATE tag is a birth, death, or marriage date
    expecting_birth = False
    expecting_death = False
    expecting_marriage = False

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parsed = parse_gedcom_line(line)
            if not parsed:
                continue

            level, tag, arguments = parsed

            # Store individual information
            if level == '0' and tag == 'INDI':
                current_indi = arguments
                individuals[current_indi] = {'id': current_indi, 'name': None}
            elif level == '1' and current_indi:
                if tag == 'NAME':
                    individuals[current_indi]['name'] = arguments
                elif tag == 'BIRT':
                    # Birth date will come next line (DATE)
                    expecting_birth = True
                elif tag == 'DEAT':
                    # Death date will come next line (DATE)
                    expecting_death = True

            # Store family information
            if level == '0' and tag == 'FAM':
                current_fam = arguments
                families[current_fam] = {'id': current_fam, 'husb': None, 'wife': None}
            elif level == '1' and current_fam:
                if tag == 'HUSB':
                    families[current_fam]['husb'] = arguments
                elif tag == 'WIFE':
                    families[current_fam]['wife'] = arguments
                elif tag == 'CHIL':
                    # Add child to list of children in this family
                    families[current_fam].setdefault('children', []).append(arguments)
                elif tag == 'MARR':
                    # Marriage date will come on next DATE line
                    expecting_marriage = True

            elif tag == 'DATE':
                date_value = arguments
                # Assign the date to the correct context based on previously seen tag
                if expecting_birth and current_indi:
                    individuals[current_indi]['birth'] = date_value
                    expecting_birth = False
                elif expecting_death and current_indi:
                    individuals[current_indi]['death'] = date_value
                    expecting_death = False
                elif expecting_marriage and current_fam:
                    families[current_fam]['married'] = date_value
                    expecting_marriage = False

    # Print individuals sorted by ID
    print("\nIndividuals:")
    for indi_id in sorted(individuals.keys()):
        indi = individuals[indi_id]
        print(f"{indi['id']}: {indi['name'] or 'Unknown'}")

    # Print families sorted by ID with spouse names
    print("\nFamilies:")
    for fam_id in sorted(families.keys()):
        fam = families[fam_id]
        husb_name = individuals.get(fam['husb'], {}).get('name', 'Unknown') if fam['husb'] else 'Unknown'
        wife_name = individuals.get(fam['wife'], {}).get('name', 'Unknown') if fam['wife'] else 'Unknown'
        print(f"{fam['id']}: Husband {fam['husb'] or '?'} ({husb_name}), Wife {fam['wife'] or '?'} ({wife_name})")

    # Run validations for US09 and US10 and print any errors
    errors_us09 = us09_birth_before_death_of_parents(individuals, families)
    errors_us10 = us10_marriage_after_14(individuals, families)

    print("\nValidation Errors:")
    for error in errors_us09 + errors_us10:
        print(error)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def us09_birth_before_death_of_parents(individuals, families):
    errors = []
    for fam_id, family in families.items():
        children = family.get("children", [])
        father_id = family.get("husb")
        mother_id = family.get("wife")

        father_death = parse_date(individuals.get(father_id, {}).get("death"))
        mother_death = parse_date(individuals.get(mother_id, {}).get("death"))

        for child_id in children:
            child_birth = parse_date(individuals.get(child_id, {}).get("birth"))
            if not child_birth:
                continue

            if mother_death and child_birth > mother_death:
                errors.append(f"ERROR US09: Child {child_id} born after mother's death in family {fam_id}.")

            if father_death and (child_birth - father_death).days > 273:
                errors.append(f"ERROR US09: Child {child_id} born more than 9 months after father's death in family {fam_id}.")
    return errors

def us10_marriage_after_14(individuals, families):
    errors = []
    for fam_id, family in families.items():
        marriage_date = parse_date(family.get("married"))
        if not marriage_date:
            continue

        for role in ['husb', 'wife']:
            person_id = family.get(role)
            birth_date = parse_date(individuals.get(person_id, {}).get("birth"))
            if birth_date:
                age_at_marriage = (marriage_date - birth_date).days / 365.25
                if age_at_marriage < 14:
                    errors.append(f"ERROR US10: {role.title()} {person_id} was married at {age_at_marriage:.1f} years in family {fam_id}.")
    return errors

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python gedcom_parser.py <filename>")
        sys.exit(1)

    process_gedcom_file(sys.argv[1])
