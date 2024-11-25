def compute_similarity_refs(first_ref, second_ref):
    if first_ref == second_ref:
        return 1.0

    if first_ref == "TMO":
        if second_ref == "TNI":
            return 0.0
        else:
            return 0.1
    
    if first_ref == "TEV":
        return 0.1

    if first_ref == "TNI":
        if second_ref == "TMO":
            return 0.0
        else:
            return 0.1