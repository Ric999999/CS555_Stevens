import sys
from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d %b %Y')
    except ValueError:
        return None

def process_gedcom(filename):
    current_fam = None
    marr_date = None
    div_date = None
    fams = {}

    marr_flag = False
    div_flag = False

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(' ', 2)
            level = parts[0]
            tag = parts[1] if len(parts) > 1 else ''
            args = parts[2] if len(parts) > 2 else ''
            
            if level == '0' and args == 'FAM':
                # Check previous family for divorce before marriage
                if current_fam and marr_date and div_date and marr_date > div_date:
                    print(f"Error: {current_fam} - Divorce on {div_date.strftime('%d %b %Y')} "
                          f"before marriage on {marr_date.strftime('%d %b %Y')}")
                
                current_fam = tag
                marr_date = None
                div_date = None
                fams[current_fam] = {}
                marr_flag = False
                div_flag = False

            elif level == '1' and current_fam:
                if tag == 'MARR':
                    marr_flag = True
                elif tag == 'DIV':
                    div_flag = True

            elif level == '2' and current_fam and tag == 'DATE':
                date = parse_date(args)
                if date:
                    if marr_flag:
                        marr_date = date
                        fams[current_fam]['married'] = date
                        marr_flag = False
                    elif div_flag:
                        div_date = date
                        fams[current_fam]['divorced'] = date
                        div_flag = False
                        if marr_date and div_date and marr_date > div_date:
                            print(f"Error: {current_fam} - Divorce on {div_date.strftime('%d %b %Y')} "
                                  f"before marriage on {marr_date.strftime('%d %b %Y')}")

        # Final check for last family
        if current_fam and marr_date and div_date and marr_date > div_date:
            print(f"Error: {current_fam} - Divorce on {div_date.strftime('%d %b %Y')} "
                  f"before marriage on {marr_date.strftime('%d %b %Y')}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python us04.py <filename.ged>")
        sys.exit(1)

    process_gedcom(sys.argv[1])
