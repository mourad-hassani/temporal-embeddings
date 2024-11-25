import random
import datetime

def generate_random_date(start_year, end_year):
    rand_int = random.randint(0, 3)

    start_date = datetime.datetime(start_year, 1, 1)
    end_date = datetime.datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + datetime.timedelta(days=random_days)
    
    if rand_int == 0:
        return random_date.strftime("%Y")
    elif rand_int == 1:
        seasons = ["SU", "WI", "FA", "SP"]
        return str(random_date.strftime("%Y") + f"-{seasons[random.randint(0, 3)]}")
    elif rand_int == 2:
        return random_date.strftime("%Y-%m")
    elif rand_int == 3:
        return random_date.strftime("%Y-%m-%d")
    
def generate_random_date_full(start_year, end_year, start_month = None, end_month = None, start_day = None, end_day = None):
    if start_day and end_day and start_month and end_month:
        start_date = datetime.datetime(start_year, start_month, start_day)
        end_date = datetime.datetime(end_year, end_month, end_day)
    else:
        start_date = datetime.datetime(start_year, 1, 1)
        end_date = datetime.datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, abs(delta.days))
    random_date = start_date + datetime.timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")