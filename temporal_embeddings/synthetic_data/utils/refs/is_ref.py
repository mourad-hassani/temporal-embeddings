import re

def is_ref(annotation):
    patterns_dicts = {"PRESENT_REF": "p", "TMO": "m", "TNI": "n", "TEV": "e", "THIS MO": "tm", "THIS NI": "tn"}
    patterns = [k for k, v in patterns_dicts.items()]

    for pattern in patterns:
        if annotation == pattern:
            return True, patterns_dicts[pattern]
    
    return False, "Invalid format"