from temporal_embeddings.synthetic_data.utils.dates.is_date import is_date
from temporal_embeddings.synthetic_data.utils.dates.is_in import is_in
from temporal_embeddings.synthetic_data.utils.dates.compute_distance_dates import compute_distance_dates_same_type, compute_distance_dates
from utils.compute_interval_distance import compute_interval_distance_date
from temporal_embeddings.synthetic_data.utils.dates.dates_settings import START_DATE, END_DATE

def compute_similarity_dates(first_date, second_date):
    first_year = int(first_date.split("-")[0])
    second_year = int(second_date.split("-")[0])
    if first_year < START_DATE or second_year > END_DATE:
        return 0.0

    first_is_date, first_date_type = is_date(first_date)
    second_is_date, second_date_type = is_date(second_date)

    if first_is_date and second_is_date:
        if first_date == second_date:
            return 1.0
        elif first_date_type == second_date_type:
            distance = compute_distance_dates_same_type(first_date=first_date, second_date=second_date, date_type=first_date_type)
            distance = distance**2 if distance < 100 else distance
            return 0.4 / distance
        elif first_date_type != second_date_type and is_in(first_date=first_date, first_date_type=first_date_type, second_date=second_date, second_date_type=second_date_type):
            return 0.5
        else:
            distance = compute_distance_dates(first_date, first_date_type, second_date, second_date_type)
            distance = distance**2 if distance < 100 else distance
            return 0.1 / distance
    else:
        raise ValueError(f"first_date: {first_date}, second_date: {second_date}")

def compute_similarity_dates_intervals(first_date, second_date):
    if len(first_date) == 1 and len(second_date) == 1:
        return compute_similarity_dates(first_date[0], second_date[0])
    
    if len(first_date) == 1:
        first_date = first_date * 2
    if len(second_date) == 1:
        second_date = second_date * 2
    
    distance, overlap = compute_interval_distance_date(first_date, second_date)
    if overlap:
        similarity = distance
        return similarity
    else:
        similarity = 0.5 / distance
        return similarity