import random

def generate_random_ref():
    rand_int = random.randint(0, 5)
    annotations = ["PRESENT_REF", "TMO", "TNI", "TEV", "THIS MO", "THIS NI"]

    return annotations[rand_int] 