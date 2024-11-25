import re

def offset_to_text(annotation):
    day_offset_pattern = r'^OFFSET P(-?\d+)D$'
    week_offset_pattern = r'^OFFSET P(-?\d+)W$'
    month_offset_pattern = r'^OFFSET P(-?\d+)M$'
    year_offset_pattern = r'^OFFSET P(-?\d+)Y$'

    this_day_offset_pattern = r"^THIS P(-?\d+)D OFFSET P(-?\d+)D$"
    this_week_offset_pattern = r"^THIS P(-?\d+)W OFFSET P(-?\d+)W$"
    this_month_offset_pattern = r"^THIS P(-?\d+)M OFFSET P(-?\d+)M$"
    this_year_offset_pattern = r"^THIS P(-?\d+)Y OFFSET P(-?\d+)Y$"

    day_this_pattern = r'^THIS P(-?\d+)D$'
    week_this_pattern = r'^THIS P(-?\d+)W$'
    month_this_pattern = r'^THIS P(-?\d+)M$'
    year_this_pattern = r'^THIS P(-?\d+)Y$'

    day_immediate_pattern = r'^(?:NEXT_IMMEDIATE|PREV_IMMEDIATE) P(-?\d+)D$'
    week_immediate_pattern = r'^(?:NEXT_IMMEDIATE|PREV_IMMEDIATE) P(-?\d+)W$'
    month_immediate_pattern = r'^(?:NEXT_IMMEDIATE|PREV_IMMEDIATE) P(-?\d+)M$'
    year_immediate_pattern = r'^(?:NEXT_IMMEDIATE|PREV_IMMEDIATE) P(-?\d+)Y$'

    if match := re.search(this_day_offset_pattern, annotation):
        first_integer, second_integer = match.group(1), match.group(2)
        first_integer_abs, second_integer_abs = abs(int(first_integer)), abs(int(second_integer))
        
        if first_integer_abs == second_integer_abs:
            if second_integer[0] == "-":
                if second_integer_abs == 1:
                    return "last day"
                
                elif second_integer_abs >= 2:
                    return f"last {second_integer_abs} days"
                
                else:
                    return None
            
            else:
                if second_integer_abs == 1:
                    return "next day"
                
                elif second_integer_abs >= 2:
                    return f"next {second_integer_abs} days"
                
                else:
                    return None
    
    elif match := re.search(this_week_offset_pattern, annotation):
        first_integer, second_integer = match.group(1), match.group(2)
        first_integer_abs, second_integer_abs = abs(int(first_integer)), abs(int(second_integer))
        
        if first_integer_abs == second_integer_abs:
            if second_integer[0] == "-":
                if second_integer_abs == 1:
                    return "last week"
                
                elif second_integer_abs >= 2:
                    return f"last {second_integer_abs} weeks"
                
                else:
                    return None
            
            else:
                if second_integer_abs == 1:
                    return "next week"
                
                elif second_integer_abs >= 2:
                    return f"next {second_integer_abs} weeks"
                
                else:
                    return None
    
    elif match := re.search(this_month_offset_pattern, annotation):
        first_integer, second_integer = match.group(1), match.group(2)
        first_integer_abs, second_integer_abs = abs(int(first_integer)), abs(int(second_integer))
        
        if first_integer_abs == second_integer_abs:
            if second_integer[0] == "-":
                if second_integer_abs == 1:
                    return "last month"
                
                elif second_integer_abs >= 2:
                    return f"last {second_integer_abs} months"
                
                else:
                    return None
            
            else:
                if second_integer_abs == 1:
                    return "next month"
                
                elif second_integer_abs >= 2:
                    return f"next {second_integer_abs} months"
                
                else:
                    return None
    
    elif match := re.search(this_year_offset_pattern, annotation):
        first_integer, second_integer = match.group(1), match.group(2)
        first_integer_abs, second_integer_abs = abs(int(first_integer)), abs(int(second_integer))
        
        if first_integer_abs == second_integer_abs:
            if second_integer[0] == "-":
                if second_integer_abs == 1:
                    return "last year"
                
                elif second_integer_abs >= 2:
                    return f"last {second_integer_abs} years"
                
                else:
                    return None
            
            else:
                if second_integer_abs == 1:
                    return "next year"
                
                elif second_integer_abs >= 2:
                    return f"next {second_integer_abs} years"
                
                else:
                    return None
    
    elif match := re.search(day_offset_pattern, annotation):
        first_integer = match.group(1)
        first_integer_abs = abs(int(first_integer))
        
        if first_integer[0] == "-":
            if first_integer_abs == 1:
                return "yesterday"
            
            elif first_integer_abs >= 2:
                return f"{first_integer_abs} days ago"
            
            else:
                return None
        
        else:
            if first_integer_abs == 1:
                return "tomorrow"
            
            elif first_integer_abs >= 2:
                return f"{first_integer_abs} days later"
            
            else:
                return None
    
    elif match := re.search(week_offset_pattern, annotation):
        first_integer = match.group(1)
        first_integer_abs = abs(int(first_integer))
        
        if first_integer[0] == "-":
            if first_integer_abs == 1:
                return "a week ago"
            
            elif first_integer_abs >= 2:
                return f"{first_integer_abs} weeks ago"
            
            else:
                return None
        
        else:
            if first_integer_abs == 1:
                return "a week later"
            
            elif first_integer_abs >= 2:
                return f"{first_integer_abs} weeks later"
            
            else:
                return None
    
    elif match := re.search(month_offset_pattern, annotation):
        first_integer = match.group(1)
        first_integer_abs = abs(int(first_integer))
        
        if first_integer[0] == "-":
            if first_integer_abs == 1:
                return "a month ago"
            
            elif first_integer_abs >= 2:
                return f"{first_integer_abs} months ago"
            
            else:
                return None
        
        else:
            if first_integer_abs == 1:
                return "a month later"
            
            elif first_integer_abs >= 2:
                return f"{first_integer_abs} months later"
            
            else:
                return None
    
    elif match := re.search(year_offset_pattern, annotation):
        first_integer = match.group(1)
        first_integer_abs = abs(int(first_integer))
        
        if first_integer[0] == "-":
            if first_integer_abs == 1:
                return "a year ago"
            
            elif first_integer_abs >= 2:
                return f"{first_integer_abs} years ago"
            
            else:
                return None
        
        else:
            if first_integer_abs == 1:
                return "a year later"
            
            elif first_integer_abs >= 2:
                return f"{first_integer_abs} years later"
            
            else:
                return None
    
    elif match := re.search(day_this_pattern, annotation):
        first_integer = int(match.group(1))
        
        if first_integer == 1:
            return "today"
        
        elif first_integer > 1:
            return f"these {first_integer} days"
        
        else:
            return None
    
    elif match := re.search(week_this_pattern, annotation):
        first_integer = int(match.group(1))
        
        if first_integer == 1:
            return "this week"
        
        elif first_integer > 1:
            return f"these {first_integer} weeks"
        
        else:
            return None
    
    elif match := re.search(month_this_pattern, annotation):
        first_integer = int(match.group(1))
        
        if first_integer == 1:
            return "this month"
        
        elif first_integer > 1:
            return f"these {first_integer} months"
        
        else:
            return None
    
    elif match := re.search(year_this_pattern, annotation):
        first_integer = int(match.group(1))
        
        if first_integer == 1:
            return "this year"
        
        elif first_integer > 1:
            return f"these {first_integer} years"
        
        else:
            return None
    
    elif match := re.search(day_immediate_pattern, annotation):
        first_integer = int(match.group(1))
        
        if "PREV_IMMEDIATE" in annotation:
            if first_integer == 1:
                return "the last day"
            
            elif first_integer > 1:
                return f"these past {first_integer} days"
        
        if "NEXT_IMMEDIATE" in annotation:
            if first_integer == 1:
                return "the next day"
            
            elif first_integer > 1:
                return f"these next {first_integer} days"
        
        return None
    
    elif match := re.search(week_immediate_pattern, annotation):
        first_integer = int(match.group(1))
        
        if "PREV_IMMEDIATE" in annotation:
            if first_integer == 1:
                return "the last week"
            
            elif first_integer > 1:
                return f"these past {first_integer} weeks"
        
        if "NEXT_IMMEDIATE" in annotation:
            if first_integer == 1:
                return "the next week"
            
            elif first_integer > 1:
                return f"these next {first_integer} weeks"
        
        return None
    
    elif match := re.search(month_immediate_pattern, annotation):
        first_integer = int(match.group(1))
        
        if "PREV_IMMEDIATE" in annotation:
            if first_integer == 1:
                return "the last month"
            
            elif first_integer > 1:
                return f"these past {first_integer} months"
        
        if "NEXT_IMMEDIATE" in annotation:
            if first_integer == 1:
                return "the next month"
            
            elif first_integer > 1:
                return f"these next {first_integer} months"
        
        return None
    
    elif match := re.search(year_immediate_pattern, annotation):
        first_integer = int(match.group(1))
        
        if "PREV_IMMEDIATE" in annotation:
            if first_integer == 1:
                return "the last year"
            
            elif first_integer > 1:
                return f"these past {first_integer} years"
        
        if "NEXT_IMMEDIATE" in annotation:
            if first_integer == 1:
                return "the next year"
            
            elif first_integer > 1:
                return f"these next {first_integer} years"
        
        return None
    
    return None