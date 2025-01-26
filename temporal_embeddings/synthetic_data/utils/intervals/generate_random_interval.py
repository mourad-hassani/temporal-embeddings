from temporal_embeddings.synthetic_data.utils.dates.generate_random_date import generate_random_date_full, generate_random_date
from temporal_embeddings.synthetic_data.utils.dates.is_date import is_date

def generate_random_interval_full(start_date, end_date):
    start_year = int(start_date.split("-")[0])
    end_year = int(end_date.split("-")[0])
    start_month = int(start_date.split("-")[1])
    end_month = int(end_date.split("-")[1])
    start_day = int(start_date.split("-")[2])
    end_day = int(end_date.split("-")[2])

    random_dates = sorted([generate_random_date_full(start_year, end_year, start_month, end_month, start_day, end_day), generate_random_date_full(start_year, end_year, start_month, end_month, start_day, end_day)])

    return f"{random_dates[0]},{random_dates[1]}"

def generate_random_interval(start_date, end_date):
    if "-" in start_date and "-" in end_date:
        return generate_random_interval_full(start_date, end_date)
    else:
        start_year = int(start_date.split("-")[0])
        end_year = int(end_date.split("-")[0])
        first_random_date = generate_random_date(start_year, end_year)
        first_type = is_date(first_random_date)[1]
        second_random_date = generate_random_date(start_year, end_year)
        second_type = is_date(second_random_date)[1]
        while second_type != first_type:
            second_random_date = generate_random_date(start_year, end_year)
            second_type = is_date(second_random_date)[1]
        return f"{first_random_date},{second_random_date}"