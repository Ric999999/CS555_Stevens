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
            
            # Store family information
            if level == '0' and tag == 'FAM':
                current_fam = arguments
                families[current_fam] = {'id': current_fam, 'husb': None, 'wife': None}
            elif level == '1' and current_fam:
                if tag == 'HUSB':
                    families[current_fam]['husb'] = arguments
                elif tag == 'WIFE':
                    families[current_fam]['wife'] = arguments
    
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

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python gedcom_parser.py <filename>")
        sys.exit(1)
    
    process_gedcom_file(sys.argv[1])
