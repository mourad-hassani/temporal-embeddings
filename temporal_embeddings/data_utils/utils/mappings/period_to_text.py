import re
from temporal_embeddings.data_utils.utils.periods.is_period import is_period
from temporal_embeddings.data_utils.utils.extract_integers import extract_integers

def period_to_text(annotation):
    is_period_bool, period_format = is_period(annotation)
    
    if is_period_bool:
        extracted_integers = extract_integers(annotation)
        
        if period_format == "pd":
            if extracted_integers[0] == 1:
                return "a day"
            
            else:
                return f"{extracted_integers[0]} days"
        
        elif period_format == "pw":
            if extracted_integers[0] == 1:
                return "a week"
            
            else:
                return f"{extracted_integers[0]} weeks"
        
        elif period_format == "pm":
            if extracted_integers[0] == 1:
                return "a month"
            
            else:
                return f"{extracted_integers[0]} months"
        
        elif period_format == "py":
            if extracted_integers[0] == 1:
                return "a year"
            
            else:
                return f"{extracted_integers[0]} years"
        
        elif period_format == "pdi":
            return f"{extracted_integers[0]} to {extracted_integers[1]} days"
        
        elif period_format == "pwi":
            return f"{extracted_integers[0]} to {extracted_integers[1]} weeks"
        
        elif period_format == "pmi":
            return f"{extracted_integers[0]} to {extracted_integers[1]} months"
        
        elif period_format == "pyi":
            return f"{extracted_integers[0]} to {extracted_integers[1]} years"
        
        elif period_format == "pdn":
            if extracted_integers[1] == 1:
                return "first day"
            
            elif extracted_integers[1] == 2:
                return "2nd day"
            
            elif extracted_integers[1] == 3:
                return "3rd day"
            
            else:
                return f"{extracted_integers[1]}th day"
        
        elif period_format == "pwn":
            if extracted_integers[1] == 1:
                return "first week"
            
            elif extracted_integers[1] == 2:
                return "2nd week"
            
            elif extracted_integers[1] == 3:
                return "3rd week"
            
            else:
                return f"{extracted_integers[1]}th week"
        
        elif period_format == "pmn":
            
            if extracted_integers[1] == 1:
                return "first month"
            
            elif extracted_integers[1] == 2:
                return "2nd month"
            
            elif extracted_integers[1] == 3:
                return "3rd month"
            
            else:
                return f"{extracted_integers[1]}th month"
        
        elif period_format == "pyn":
            if extracted_integers[1] == 1:
                return "first year"
            
            elif extracted_integers[1] == 2:
                return "2nd year"
            
            elif extracted_integers[1] == 3:
                return "3rd year"
            
            else:
                return f"{extracted_integers[1]}th year"
    
    return None