# app/utils/search_utils.py

from difflib import SequenceMatcher

def fuzzy_match(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def compute_score(pharmacy_name, mask_name, keywords):
    score = 0
    for kw in keywords:
        if kw.lower() == pharmacy_name.lower():
            score += 10
        elif kw.lower() in pharmacy_name.lower():
            score += 5
        else:
            score += int(fuzzy_match(kw, pharmacy_name) * 3)

        if kw.lower() == mask_name.lower():
            score += 10
        elif kw.lower() in mask_name.lower():
            score += 5
        else:
            score += int(fuzzy_match(kw, mask_name) * 3)
    return score