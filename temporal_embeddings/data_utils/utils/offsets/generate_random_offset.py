import random
from temporal_embeddings.data_utils.utils.extract_integers import extract_integers

def generate_random_offset():
    rand_int = random.randint(1, 10)
    is_negative = bool(random.getrandbits(1))
    rand_format = random.randint(0, 15)
    rand_bool = bool(random.getrandbits(1))

    if is_negative:
        rand_int *= -1
    
    if rand_bool:
        immediate_text = "NEXT_IMMEDIATE"
    else:
        immediate_text = "PREV_IMMEDIATE"
    
    if rand_format == 0:
        return f"OFFSET P{rand_int}D"
    elif rand_format == 1:
        return f"OFFSET P{rand_int}W"
    elif rand_format == 2:
        return f"OFFSET P{rand_int}M"
    elif rand_format == 3:
        return f"OFFSET P{rand_int}Y"
    elif rand_format == 4:
        return f"THIS P{abs(rand_int)}D OFFSET P{rand_int}D"
    elif rand_format == 5:
        return f"THIS P{abs(rand_int)}W OFFSET P{rand_int}W"
    elif rand_format == 6:
        return f"THIS P{abs(rand_int)}M OFFSET P{rand_int}M"
    elif rand_format == 7:
        return f"THIS P{abs(rand_int)}Y OFFSET P{rand_int}Y"
    elif rand_format == 8:
        return f"THIS P{abs(rand_int)}D"
    elif rand_format == 9:
        return f"THIS P{abs(rand_int)}W"
    elif rand_format == 10:
        return f"THIS P{abs(rand_int)}M"
    elif rand_format == 11:
        return f"THIS P{abs(rand_int)}Y"
    elif rand_format == 12:
        return f"{immediate_text} P{abs(rand_int)}D"
    elif rand_format == 13:
        return f"{immediate_text} P{abs(rand_int)}W"
    elif rand_format == 14:
        return f"{immediate_text} P{abs(rand_int)}M"
    elif rand_format == 15:
        return f"{immediate_text} P{abs(rand_int)}Y"

def generate_close_random_offset(value, type):
    if type in ["td", "tw", "tm", "ty"]:
        value = extract_integers(value)[1]
    else:
        value = extract_integers(value)[0]
        
    is_negative = True if value < 0 else False
    value = abs(value)
    min_value = max(1, value - 5)
    max_value = min(15, value + 5)
    rand_int = random.randint(min_value, max_value)

    if is_negative:
        rand_int *= -1

    rand_bool = bool(random.getrandbits(1))
    
    if rand_bool:
        immediate_text = "NEXT_IMMEDIATE"
    else:
        immediate_text = "PREV_IMMEDIATE"
    
    if type == "d":
        return f"OFFSET P{rand_int}D"
    elif type == "w":
        return f"OFFSET P{rand_int}W"
    elif type == "m":
        return f"OFFSET P{rand_int}M"
    elif type == "y":
        return f"OFFSET P{rand_int}Y"
    elif type == "td":
        return f"THIS P{abs(rand_int)}D OFFSET P{rand_int}D"
    elif type == "tw":
        return f"THIS P{abs(rand_int)}W OFFSET P{rand_int}W"
    elif type == "tm":
        return f"THIS P{abs(rand_int)}M OFFSET P{rand_int}M"
    elif type == "ty":
        return f"THIS P{abs(rand_int)}Y OFFSET P{rand_int}Y"
    elif type == "thisd":
        return f"THIS P{rand_int}D"
    elif type == "thisw":
        return f"THIS P{rand_int}W"
    elif type == "thism":
        return f"THIS P{rand_int}M"
    elif type == "thisy":
        return f"THIS P{rand_int}Y"
    elif type == "immediated":
        return f"{immediate_text} P{rand_int}D"
    elif type == "immediatew":
        return f"{immediate_text} P{rand_int}W"
    elif type == "immediatem":
        return f"{immediate_text} P{rand_int}M"
    elif type == "immediatey":
        return f"{immediate_text} P{rand_int}Y"