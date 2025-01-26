def ref_to_text(annotation):
    mappings = {
        "PRESENT_REF": "now",
        "THIS MO": "this morning",
        "THIS NI": "tonight",
        "TEV": "evening",
        "TMO": "morning",
        "TNI": "night",
    }

    return mappings[annotation]