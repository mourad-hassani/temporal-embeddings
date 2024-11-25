from typing import List

from temporal_embeddings.data_utils.utils.dates.is_date import is_date
from temporal_embeddings.data_utils.utils.offsets.offset_to_date import offset_to_date
from temporal_embeddings.data_utils.utils.refs.ref_to_date import ref_to_date
from temporal_embeddings.data_utils.utils.intervals.interval_to_date import interval_to_date
from temporal_embeddings.data_utils.utils.dates.to_explicit_date import to_explicit_date

def expression_to_date(expression : str, current_date : str) -> List:
    if is_date(expression)[0]:
        return to_explicit_date(expression)
    
    elif expression_date := offset_to_date(expression, current_date=current_date):
        return expression_date
    
    elif expression_date := ref_to_date(expression, current_date=current_date):
        return expression_date
    
    elif expression_date := interval_to_date(expression):
        return expression_date
    
    return None