def parse_gedcom_line(line):
    line = line.strip()
    if not line:
        return None
    
    tokens = line.split(' ', 2)
    level = tokens[0]
    
    #Special cases for 0-level INDI and FAM tags
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
    
    #Special case: 1 DATE is not valid
    if level == '1' and tag == 'DATE':
        return False
    
    return tag in valid_tags.get(level, [])

def process_gedcom_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            print(f"--> {line}")
            
            parsed = parse_gedcom_line(line)
            if not parsed:
                continue
                
            level, tag, arguments = parsed
            valid = 'Y' if is_valid_tag(level, tag) else 'N'
            
            if level == '0' and tag in ['INDI', 'FAM']:
                output_args = arguments
            else:
                output_args = arguments if arguments else ''
            
            print(f"<-- {level}|{tag}|{valid}|{output_args}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python gedcom_parser.py <filename>")
        sys.exit(1)
    
    process_gedcom_file(sys.argv[1])
