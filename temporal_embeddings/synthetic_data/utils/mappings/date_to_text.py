from typing import Dict
import random

from temporal_embeddings.synthetic_data.utils.dates.is_date import is_date

integer_to_month: Dict = {
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

symbol_to_season: Dict = {
    "FA": "fall",
    "SP": "spring",
    "WI": "winter",
    "SU": "summer",
}

def date_to_text(annotation: str) -> str:
    is_date_bool, date_format = is_date(annotation)
    
    if is_date_bool:
        if date_format == "yyyy":
            return random.choice([
                annotation,
                f"The year {annotation}",
                f"In the year {annotation}",
                f"{annotation}, a notable year",
                f"The year of {annotation}",
                f"{annotation}, a historic year",
                f"{annotation}, a remarkable year",
                f"The events of {annotation}",
                f"{annotation}, a year to remember",
                f"{annotation}, a year in history"
            ])
        
        if date_format == "yyyy-s":
            year: str = annotation.split("-")[0]
            season: str = annotation.split("-")[-1]
            season: str = symbol_to_season[season]
            return random.choice([
                f"{season} of {year}",
                f"The {season} season in {year}",
                f"During {season} {year}",
                f"In the {season} of {year}",
                f"The {season} of the year {year}",
                f"{season}, {year}",
                f"The {season} months of {year}",
                f"{season} season, {year}",
                f"{season}time in {year}",
                f"The {season} period of {year}"
            ])
        
        if date_format == "yyyy-mm":
            year: str = annotation.split("-")[0]
            month: str = annotation.split("-")[-1]
            month: str = integer_to_month[int(month)]
            return random.choice([
                f"{month} {year}",
                f"The month of {month} in {year}",
                f"In {month} {year}",
                f"{month}, {year}",
                f"The {month} of {year}",
                f"{month} in the year {year}",
                f"The month {month} of {year}",
                f"{month} during {year}",
                f"{month}, a part of {year}",
                f"{month} in history, {year}"
            ])
        
        if date_format == "yyyy-mm-dd":
            year: str = annotation.split("-")[0]
            month: str = annotation.split("-")[1]
            day: str = annotation.split("-")[-1]
            month: str = integer_to_month[int(month)]
            return random.choice([
                f"{day} {month} {year}",
                f"The {day}th of {month}, {year}",
                f"On {day} {month} {year}",
                f"{month} {day}, {year}",
                f"The date {day} {month} {year}",
                f"{day}th day of {month}, {year}",
                f"{day}/{month}/{year}",
                f"{month} {day} in the year {year}",
                f"{day} of {month}, {year}",
                f"{day} {month}, a day in {year}"
            ])
    
    return None