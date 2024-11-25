from temporal_embeddings.data_utils.utils.dates.is_date import is_date
import calendar

season_to_months = {
    "WI": ["12", "01", "02"],
    "SP": ["03", "04", "05"],
    "SU": ["06", "07", "08"],
    "FA": ["09", "10", "11"],
}

def to_explicit_date(annotation):
    if not is_date(annotation)[0]:
        return None
    
    date_format = is_date(annotation)[1]

    if date_format == "yyyy":
        return [f"{annotation}-01-01", f"{annotation}-12-31"]
    elif date_format == "yyyy-mm":
        year  = annotation.split("-")[0]
        month = annotation.split("-")[-1]
        if int(month) == 2:
            last_day = 28
        else:
            last_day = 30
        return [f"{year}-{month}-01", f"{year}-{month}-{last_day}"]
    elif date_format == "yyyy-s":
        year = annotation.split("-")[0]
        season = annotation.split("-")[1]
        last_year = int(year)
        if season == "WI":
            last_year = last_year + 1
        first_month = season_to_months[season][0]
        last_month = season_to_months[season][-1]
        last_day = calendar.monthrange(int(last_year), int(last_month))[1]
        return [f"{year}-{first_month}-01", f"{last_year}-{last_month}-{last_day}"]
    else:
        return [annotation]
