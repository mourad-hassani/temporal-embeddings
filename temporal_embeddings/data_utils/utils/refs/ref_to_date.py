def ref_to_date(annotation, current_date):
    if annotation == "PRESENT_REF":
        return [current_date]
    if annotation == "THIS NI":
        return [current_date]
    if annotation == "THIS MO":
        return [current_date]
    
    return None