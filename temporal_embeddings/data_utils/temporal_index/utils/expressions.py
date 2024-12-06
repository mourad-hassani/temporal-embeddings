from typing import Dict, List
import re
from datetime import datetime

import pandas as pd

from temporal_embeddings.data_utils.utils.dates.is_date import is_date
from temporal_embeddings.data_utils.utils.intervals.is_interval import is_interval
from temporal_embeddings.data_utils.utils.offsets.is_offset import is_offset
from temporal_embeddings.data_utils.utils.periods.is_period import is_period
from temporal_embeddings.data_utils.utils.refs.is_ref import is_ref
from temporal_embeddings.data_utils.temporal_index.utils.expression_to_date import expression_to_date
from temporal_embeddings.data_utils.utils.dates.generate_random_date import generate_random_date_full
from temporal_embeddings.data_utils.utils.dates.dates_settings import START_DATE, END_DATE
from temporal_embeddings.data_utils.utils.mappings.expression_to_text import expression_to_text

def add_expression(temporal_sentences : pd.DataFrame, expression : str, sentence : str, value : str) -> pd.DataFrame:
    current_date : str = generate_random_date_full(START_DATE, END_DATE)

    expression_object : Dict = {"sent": sentence, "expression": expression, "value": value, "current_date": current_date}

    expression_date_list : List = expression_to_date(value, current_date) if expression_to_date(value, current_date) else value
    
    if isinstance(expression_date_list, list):
        if len(expression_date_list) == 2:
            expression_date : str = "->".join(expression_date_list)

        else:
            expression_date : str = expression_date_list[0]

    else:
        expression_date : str = expression_date_list

    if expression_date in temporal_sentences.index:
        temporal_sentences.at[expression_date, "sentences"].append(expression_object["sent"])
        temporal_sentences.at[expression_date, "expressions"].append(expression_object["expression"])
        temporal_sentences.at[expression_date, "values"].append(expression_object["value"])
        temporal_sentences.at[expression_date, "current_dates"].append(expression_object["current_date"])
    
    else:
        temporal_sentences.loc[expression_date] = [[expression_object["sent"]], [expression_object["expression"]], [expression_object["value"]], [expression_object["current_date"]]]
    
    return temporal_sentences

def accept_expression(expression : str) -> bool:
    return (is_date(expression) or is_interval(expression) or is_offset(expression) or is_period(expression) or is_ref(expression)) and is_valid_date(expression) and expression_to_text(expression)

def is_valid_date(date_str):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False
    
    return True