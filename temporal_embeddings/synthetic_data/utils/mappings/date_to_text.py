import re
from typing import Dict

from temporal_embeddings.synthetic_data.utils.dates.is_date import is_date

integer_to_month : Dict = {
    1: "january",
    2: "february",
    3: "march",
    4: "april",
    5: "may",
    6: "june",
    7: "july",
    8: "august",
    9: "september",
    10: "october",
    11: "november",
    12: "december",
}

symbol_to_season : Dict = {
    "FA": "fall",
    "SP": "spring",
    "WI": "winter",
    "SU": "summer",
}

def date_to_text(annotation : str) -> str:
    is_date_bool, date_format = is_date(annotation)
    
    if is_date_bool:
        if date_format == "yyyy":
            return annotation
        
        if date_format == "yyyy-s":
            year : str = annotation.split("-")[0]
            season : str = annotation.split("-")[-1]
            season : str = symbol_to_season[season]
            return f"{season} of {year}"
        
        if date_format == "yyyy-mm":
            year : str = annotation.split("-")[0]
            month : str = annotation.split("-")[-1]
            month : str = integer_to_month[int(month)]
            return f"{month} {year}"
        
        if date_format == "yyyy-mm-dd":
            year : str = annotation.split("-")[0]
            month : str = annotation.split("-")[1]
            day : str = annotation.split("-")[-1]
            month : str = integer_to_month[int(month)]
            return f"{day} {month} {year}"
    
    return None