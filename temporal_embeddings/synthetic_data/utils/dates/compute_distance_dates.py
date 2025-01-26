from temporal_embeddings.synthetic_data.utils.dates.is_in import season_to_months
from datetime import datetime

def compute_distance_dates_same_type(first_date, second_date, date_type):
    if date_type == "yyyy":
        return abs(int(first_date) - int(second_date))
    elif date_type == "yyyy-s":
        first_months = season_to_months[first_date[-2:]]
        second_months = season_to_months[second_date[-2:]]
        distance = (datetime(int(first_date[:4]), int(first_months[0]), 1) - datetime(int(second_date[:4]), int(second_months[0]), 1)).days
        distance = int(distance / 30)
        return int(distance / 3)
    elif date_type == "yyyy-mm":
        distance = (datetime(int(first_date[:4]), int(first_date[-2:]), 1) - datetime(int(second_date[:4]), int(second_date[-2:]), 1)).days
        distance = int(distance / 30)
        if distance == 0:
            distance = 1
        return abs(distance)
    elif date_type == "yyyy-mm-dd":
        distance = (datetime(int(first_date[:4]), int(first_date[5:7]), int(first_date[-2:])) - datetime(int(second_date[:4]), int(second_date[5:7]), int(second_date[-2:]))).days
        return abs(distance)

def compute_distance_dates(first_date, first_date_type, second_date, second_date_type):
    if first_date_type == "yyyy" or second_date_type == "yyyy":
        distance = abs(int(first_date[:4]) - int(second_date[:4]))
        return distance
    elif first_date_type == "yyyy-mm":
        if second_date_type == "yyyy-s":
            month = season_to_months[second_date[-2:]][1]
            distance = (datetime(int(first_date[:4]), int(first_date[-2:]), 1) - datetime(int(second_date[:4]), int(month), 1)).days
            distance = int(distance / 30)
            if distance == 0:
                distance = 1
            return abs(distance)
        else:
            distance = (datetime(int(first_date[:4]), int(first_date[-2:]), 1) - datetime(int(second_date[:4]), int(second_date[5:7]), 1)).days
            distance = int(distance / 30)
            if distance == 0:
                distance = 1
            return abs(distance)
    elif second_date_type == "yyyy-mm":
        if first_date_type == "yyyy-s":
            month = season_to_months[first_date[-2:]][1]
            distance = (datetime(int(first_date[:4]), int(month), 1) - datetime(int(second_date[:4]), int(second_date[-2:]), 1)).days
            distance = int(distance / 30)
            if distance == 0:
                distance = 1
            return abs(distance)
        else:
            distance = (datetime(int(first_date[:4]), int(first_date[5:7]), 1) - datetime(int(second_date[:4]), int(second_date[-2:]), 1)).days
            distance = int(distance / 30)
            if distance == 0:
                distance = 1
            return abs(distance)
    elif first_date_type == "yyyy-mm-dd":
        month = season_to_months[second_date[-2:]][1]
        distance = (datetime(int(first_date[:4]), int(first_date[5:7]), 1) - datetime(int(second_date[:4]), int(month), 1)).days
        distance = int(distance / 30)
        if distance == 0:
            distance = 1
        return abs(distance)
    elif second_date_type == "yyyy-mm-dd":
        month = season_to_months[first_date[-2:]][1]
        distance = (datetime(int(first_date[:4]), int(month), 1) - datetime(int(second_date[:4]), int(second_date[5:7]), 1)).days
        distance = int(distance / 30)
        if distance == 0:
            distance = 1
        return abs(distance)
    else:
        month = season_to_months[first_date[-2:]][1]
        distance = (datetime(int(first_date[:4]), int(month), 1) - datetime(int(second_date[:4]), int(second_date[5:7]), 1)).days
        distance = int(distance / 30)
        if distance == 0:
            distance = 1
        return abs(distance)