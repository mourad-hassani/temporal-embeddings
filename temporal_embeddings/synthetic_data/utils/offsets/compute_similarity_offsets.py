from temporal_embeddings.data_utils.utils.extract_integers import extract_integers
from utils.compute_interval_distance import compute_interval_distance_date
from datetime import datetime, timedelta
from temporal_embeddings.synthetic_data.utils.dates.compute_similarity_dates import compute_similarity_dates

def compute_similarity_offsets(first_offset, first_offset_type, second_offset, second_offset_type, first_current_date, second_current_date):
    first_offset_in_days = compute_offset_in_days(first_offset, first_offset_type, first_current_date)
    second_offset_in_days = compute_offset_in_days(second_offset, second_offset_type, second_current_date)

    if len(first_offset_in_days) != len(second_offset_in_days):
        return 0.05
    if len(first_offset_in_days) == 1:
        return compute_similarity_dates(first_offset_in_days[0], second_offset_in_days[0])
    else:
        distance = compute_interval_distance_date(first_offset_in_days, second_offset_in_days)
        if distance == 0:
            return 0.8
        else:
            return 0.5 / distance**2

def compute_offset_in_days(offset, offset_type, current_date):
    date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    if offset_type == "d":
        offset = extract_integers(offset)[0]
        new_date = date_obj + timedelta(days=offset)
        return [new_date.strftime("%Y-%m-%d")]
    elif offset_type == "w":
        offset = extract_integers(offset)[0] * 7
        new_date = date_obj + timedelta(days=offset)
        return [new_date.strftime("%Y-%m-%d")]
    elif offset_type == "m":
        offset = extract_integers(offset)[0] * 30
        new_date = date_obj + timedelta(days=offset)
        return [new_date.strftime("%Y-%m-%d")]
    elif offset_type == "y":
        offset = extract_integers(offset)[0] * 365
        new_date = date_obj + timedelta(days=offset)
        return [new_date.strftime("%Y-%m-%d")]
    elif offset_type == "td":
        offset = extract_integers(offset)[1]
        if offset < 0:
            new_date = date_obj + timedelta(days=offset)
            return [new_date.strftime("%Y-%m-%d"), current_date]
        else:
            new_date = date_obj + timedelta(days=offset)
            return [current_date, new_date.strftime("%Y-%m-%d")]
    elif offset_type == "tw":
        offset = extract_integers(offset)[1] * 7
        if offset < 0:
            new_date = date_obj + timedelta(days=offset)
            return [new_date.strftime("%Y-%m-%d"), current_date]
        else:
            new_date = date_obj + timedelta(days=offset)
            return [current_date, new_date.strftime("%Y-%m-%d")]
    elif offset_type == "tm":
        offset = extract_integers(offset)[1] * 30
        if offset < 0:
            new_date = date_obj + timedelta(days=offset)
            return [new_date.strftime("%Y-%m-%d"), current_date]
        else:
            new_date = date_obj + timedelta(days=offset)
            return [current_date, new_date.strftime("%Y-%m-%d")]
    elif offset_type == "ty":
        offset = extract_integers(offset)[1] * 365
        if offset < 0:
            new_date = date_obj + timedelta(days=offset)
            return [new_date.strftime("%Y-%m-%d"), current_date]
        else:
            new_date = date_obj + timedelta(days=offset)
            return [current_date, new_date.strftime("%Y-%m-%d")]