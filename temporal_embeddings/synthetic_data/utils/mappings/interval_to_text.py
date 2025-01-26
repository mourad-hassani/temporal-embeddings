import random

from temporal_embeddings.synthetic_data.utils.mappings.date_to_text import date_to_text

date_intervals = [
    "from {} to {}",
    "ranging from {} to {}",
    "between {} and {}",
    "starting on {} and ending on {}",
    "in the period from {} to {}",
    "spanning from {} to {}",
    "over the time frame of {} to {}",
    "covering the period from {} to {}",
    "during the interval from {} to {}",
    "from the {} until the {}",
    "over the span of {} to {}",
    "from {} through {}",
    "within the range of {} to {}",
    "beginning on {} and concluding on {}",
    "extending from {} to {}",
    "throughout the duration of {} to {}",
    "for the dates {} to {}",
    "across the dates from {} to {}"
]

def interval_to_text(annotation : str) -> str:
    first_date, second_date = annotation.split(",")
    
    first_text : str = date_to_text(first_date)
    second_text : str = date_to_text(second_date)

    random_pattern : str = date_intervals[random.randint(0, len(date_intervals)-1)]
    
    return random_pattern.format(first_text, second_text)