from typing import Dict, List
import re
from datetime import datetime

from temporal_embeddings.data_utils.utils.dates.is_date import is_date
from temporal_embeddings.data_utils.utils.intervals.is_interval import is_interval
from temporal_embeddings.data_utils.utils.offsets.is_offset import is_offset
from temporal_embeddings.data_utils.utils.periods.is_period import is_period
from temporal_embeddings.data_utils.utils.refs.is_ref import is_ref
from temporal_embeddings.data_utils.temporal_index.utils.expression_to_date import expression_to_date
from temporal_embeddings.data_utils.utils.dates.generate_random_date import generate_random_date_full
from temporal_embeddings.data_utils.utils.dates.dates_settings import START_DATE, END_DATE
from temporal_embeddings.data_utils.utils.mappings.expression_to_text import expression_to_text

def add_expression(temporal_sentences : Dict, expression : str, sentence_id : int, value : str) -> Dict:
    current_date : str = generate_random_date_full(START_DATE, END_DATE)

    expression_object : Dict = {"sent": sentence_id, "expression": expression, "value": value, "current_date": current_date}

    expression_date_list : List = expression_to_date(value, current_date) if expression_to_date(value, current_date) else value
    
    if isinstance(expression_date_list, list):
        if len(expression_date_list) == 2:
            expression_date : str = "->".join(expression_date_list)

        else:
            expression_date : str = expression_date_list[0]

    else:
        expression_date : str = expression_date_list

    if expression_date in temporal_sentences:
        temporal_sentences[expression_date].append(expression_object)
    
    else:
        temporal_sentences[expression_date] = [expression_object]
        temporal_sentences = dict(sorted(temporal_sentences.items()))
    
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