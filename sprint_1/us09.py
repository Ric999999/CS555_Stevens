from datetime import datetime

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
