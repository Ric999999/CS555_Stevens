def us20_no_aunt_uncle_marriages(individuals, families):
    errors = []

    parent_map = {}
    for fam_id, fam in families.items():
        for child in fam.get("children", []):
            parent_map[child] = (fam.get("husb"), fam.get("wife"))

    siblings_map = {}
    for fam_id, fam in families.items():
        kids = set(fam.get("children", []))
        for kid in kids:
            siblings_map[kid] = kids - {kid}

    for fam_id, fam in families.items():
        husb = fam.get("husb")
        wife = fam.get("wife")

        if not husb or not wife:
            continue

        # Husb's siblings' kids = nieces/nephews
        husb_nieces_nephews = set()
        for sib in siblings_map.get(husb, set()):
            for child, parents in parent_map.items():
                if sib in parents:
                    husb_nieces_nephews.add(child)

        # Wife's siblings' kids = nieces/nephews
        wife_nieces_nephews = set()
        for sib in siblings_map.get(wife, set()):
            for child, parents in parent_map.items():
                if sib in parents:
                    wife_nieces_nephews.add(child)

        if wife in husb_nieces_nephews:
            errors.append(f"ERROR US20: Uncle {husb} married niece {wife} in family {fam_id}.")
        if husb in wife_nieces_nephews:
            errors.append(f"ERROR US20: Aunt {wife} married nephew {husb} in family {fam_id}.")

    return errors
