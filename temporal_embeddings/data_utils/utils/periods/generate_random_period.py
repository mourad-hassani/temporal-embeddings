import random
from temporal_embeddings.data_utils.utils.extract_integers import extract_integers

first_type = [("P", "D"), ("P", "W"), ("P", "M"), ("P", "Y")]
second_type = ["P1D-#", "P1W-#", "P1M-#", "P1Y-#"]
third_type = [("P", "D/P", "D"), ("P", "W/P", "W"), ("P", "M/P", "M"), ("P", "Y/P", "Y")]

def generate_random_period():
    rand_int = random.randint(0, 2)
    if rand_int == 0:
        rand_int = random.randint(0, 3)
        rand_per = random.randint(1, 10)
        return first_type[rand_int][0] + str(rand_per) + first_type[rand_int][1]
    elif rand_int == 1:
        rand_int = random.randint(0, 3)
        return second_type[rand_int] + str(random.randint(1, 10))
    elif rand_int == 2:
        rand_int = random.randint(0, 3)
        rand_per = random.randint(1, 10)
        rand_per1 = random.randint(rand_per + 1, rand_per + 10)
        return third_type[rand_int][0] + str(rand_per) + third_type[rand_int][1] + str(rand_per1) + third_type[rand_int][2]

def generate_close_random_period(period, type):
    integers = extract_integers(period)
    first_rand_int = abs(random.randint(integers[0]-5, integers[0]+5))
    second_rand_int = abs(random.randint(max(1, integers[0]-5), integers[0]+5))
    if type == "pd":
        return f"P{first_rand_int}D"
    elif type == "pw":
        return f"P{first_rand_int}W"
    elif type == "pm":
        return f"P{first_rand_int}M"
    elif type == "py":
        return f"P{first_rand_int}Y"
    elif type == "pdn":
        return f"P1D-#{second_rand_int}"
    elif type == "pwn":
        return f"P1W-#{second_rand_int}"
    elif type == "pmn":
        return f"P1M-#{second_rand_int}"
    elif type == "pyn":
        return f"P1Y-#{second_rand_int}"
    elif type == "pdi":
        rand_per = abs(random.randint(max(1, integers[0]-5), integers[0]+5))
        rand_per1 = abs(random.randint(rand_per+1, max(rand_per+1, integers[1] + 5)))
        return f"P{(rand_per)}D/P{rand_per1}D"
    elif type == "pwi":
        rand_per = abs(random.randint(max(1, integers[0]-5), integers[0]+5))
        rand_per1 = abs(random.randint(rand_per+1, max(rand_per+1, integers[1] + 5)))
        return f"P{rand_per}W/P{rand_per1}W"
    elif type == "pmi":
        rand_per = abs(random.randint(max(1, integers[0]-5), integers[0]+5))
        rand_per1 = abs(random.randint(rand_per+1, max(rand_per+1, integers[1] + 5)))
        return f"P{rand_per}M/P{rand_per1}M"
    elif type == "pyi":
        rand_per = abs(random.randint(max(1, integers[0]-5), integers[0]+5))
        rand_per1 = abs(random.randint(rand_per+1, max(rand_per+1, integers[1] + 5)))
        return f"P{rand_per}Y/P{rand_per1}Y"