from temporal_embeddings.synthetic_data.utils.offsets.is_offset import is_offset
from temporal_embeddings.data_utils.utils.extract_integers import extract_integers
from datetime import datetime, timedelta
from temporal_embeddings.synthetic_data.utils.dates.date_utils import get_week_dates, get_month_dates, get_year_dates

def offset_to_date(annotation, current_date):
    date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    annotation_type = is_offset(annotation)[1]

    if annotation_type == "d":
        offset = extract_integers(annotation)[0]
        new_date = date_obj + timedelta(days=offset)
        return [new_date.strftime("%Y-%m-%d")]
    elif annotation_type == "w":
        offset = extract_integers(annotation)[0] * 7
        new_date = date_obj + timedelta(days=offset)
        return [new_date.strftime("%Y-%m-%d")]
    elif annotation_type == "m":
        offset = extract_integers(annotation)[0] * 30
        new_date = date_obj + timedelta(days=offset)
        return [new_date.strftime("%Y-%m-%d")]
    elif annotation_type == "y":
        offset = extract_integers(annotation)[0] * 365
        new_date = date_obj + timedelta(days=offset)
        return [new_date.strftime("%Y-%m-%d")]
    elif annotation_type == "td":
        offset = extract_integers(annotation)[1]
        if offset < 0:
            new_date = date_obj + timedelta(days=offset)
            return [new_date.strftime("%Y-%m-%d"), current_date]
        else:
            new_date = date_obj + timedelta(days=offset)
            return [current_date, new_date.strftime("%Y-%m-%d")]
    elif annotation_type == "tw":
        offset = extract_integers(annotation)[1] * 7
        if offset < 0:
            new_date = date_obj + timedelta(days=offset)
            return [new_date.strftime("%Y-%m-%d"), current_date]
        else:
            new_date = date_obj + timedelta(days=offset)
            return [current_date, new_date.strftime("%Y-%m-%d")]
    elif annotation_type == "tm":
        offset = extract_integers(annotation)[1] * 30
        if offset < 0:
            new_date = date_obj + timedelta(days=offset)
            return [new_date.strftime("%Y-%m-%d"), current_date]
        else:
            new_date = date_obj + timedelta(days=offset)
            return [current_date, new_date.strftime("%Y-%m-%d")]
    elif annotation_type == "ty":
        offset = extract_integers(annotation)[1] * 356
        if offset < 0:
            new_date = date_obj + timedelta(days=offset)
            return [new_date.strftime("%Y-%m-%d"), current_date]
        else:
            new_date = date_obj + timedelta(days=offset)
            return [current_date, new_date.strftime("%Y-%m-%d")]
    elif annotation_type == "thisd":
        offset = extract_integers(annotation)[0]
        if offset == 1:
            return [current_date]
        else:
            new_date = date_obj + timedelta(days=(1 - offset))
            return [new_date.strftime("%Y-%m-%d"), current_date]
    elif annotation_type == "thisw":
        offset = extract_integers(annotation)[0]
        return get_week_dates(current_date, 1 - offset, num_weeks=offset)
    elif annotation_type == "thism":
        offset = extract_integers(annotation)[0]
        return get_month_dates(current_date, 1 - offset, num_months=offset)
    elif annotation_type == "thisy":
        offset = extract_integers(annotation)[0]
        return get_year_dates(current_date, 1 - offset, num_years=offset)
    elif annotation_type == "immediated":
        offset = extract_integers(annotation)[0]
        if "PREV_IMMEDIATE" in annotation:
            offset *= -1
        new_date = date_obj + timedelta(days=offset)
        if offset == 1:
            return [new_date.strftime("%Y-%m-%d")]
        else:
            return sorted([new_date.strftime("%Y-%m-%d"), current_date])
    elif annotation_type == "immediatew":
        offset = extract_integers(annotation)[0]
        if "PREV_IMMEDIATE" in annotation:
            offset *= -1
        return get_week_dates(current_date, offset, abs(offset))
    elif annotation_type == "immediatem":
        offset = extract_integers(annotation)[0]
        if "PREV_IMMEDIATE" in annotation:
            offset *= -1
        return get_month_dates(current_date, offset, abs(offset))
    elif annotation_type == "immediatey":
        offset = extract_integers(annotation)[0]
        if "PREV_IMMEDIATE" in annotation:
            offset *= -1
        return get_year_dates(current_date, offset, abs(offset))
    
    return None