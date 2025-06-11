from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None

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
