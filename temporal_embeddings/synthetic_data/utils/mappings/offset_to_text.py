import re
import random

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
                    return random.choice(["last day", "yesterday", "the previous day", "one day ago", "the day before"])
                elif second_integer_abs >= 2:
                    return random.choice([
                        f"last {second_integer_abs} days", 
                        f"the previous {second_integer_abs} days", 
                        f"{second_integer_abs} days ago", 
                        f"the past {second_integer_abs} days", 
                        f"the preceding {second_integer_abs} days"
                    ])
            else:
                if second_integer_abs == 1:
                    return random.choice(["next day", "tomorrow", "the following day", "one day later", "the day after"])
                elif second_integer_abs >= 2:
                    return random.choice([
                        f"next {second_integer_abs} days", 
                        f"the following {second_integer_abs} days", 
                        f"{second_integer_abs} days later", 
                        f"the upcoming {second_integer_abs} days", 
                        f"the succeeding {second_integer_abs} days"
                    ])
    
    elif match := re.search(this_week_offset_pattern, annotation):
        first_integer, second_integer = match.group(1), match.group(2)
        first_integer_abs, second_integer_abs = abs(int(first_integer)), abs(int(second_integer))
        
        if first_integer_abs == second_integer_abs:
            if second_integer[0] == "-":
                if second_integer_abs == 1:
                    return random.choice(["last week", "the previous week", "a week ago", "the past week", "the preceding week"])
                elif second_integer_abs >= 2:
                    return random.choice([
                        f"last {second_integer_abs} weeks", 
                        f"the previous {second_integer_abs} weeks", 
                        f"{second_integer_abs} weeks ago", 
                        f"the past {second_integer_abs} weeks", 
                        f"the preceding {second_integer_abs} weeks"
                    ])
            else:
                if second_integer_abs == 1:
                    return random.choice(["next week", "the following week", "a week later", "the upcoming week", "the succeeding week"])
                elif second_integer_abs >= 2:
                    return random.choice([
                        f"next {second_integer_abs} weeks", 
                        f"the following {second_integer_abs} weeks", 
                        f"{second_integer_abs} weeks later", 
                        f"the upcoming {second_integer_abs} weeks", 
                        f"the succeeding {second_integer_abs} weeks"
                    ])
    
    elif match := re.search(this_month_offset_pattern, annotation):
        first_integer, second_integer = match.group(1), match.group(2)
        first_integer_abs, second_integer_abs = abs(int(first_integer)), abs(int(second_integer))
        
        if first_integer_abs == second_integer_abs:
            if second_integer[0] == "-":
                if second_integer_abs == 1:
                    return random.choice(["last month", "the previous month", "a month ago", "the past month", "the preceding month"])
                elif second_integer_abs >= 2:
                    return random.choice([
                        f"last {second_integer_abs} months", 
                        f"the previous {second_integer_abs} months", 
                        f"{second_integer_abs} months ago", 
                        f"the past {second_integer_abs} months", 
                        f"the preceding {second_integer_abs} months"
                    ])
            else:
                if second_integer_abs == 1:
                    return random.choice(["next month", "the following month", "a month later", "the upcoming month", "the succeeding month"])
                elif second_integer_abs >= 2:
                    return random.choice([
                        f"next {second_integer_abs} months", 
                        f"the following {second_integer_abs} months", 
                        f"{second_integer_abs} months later", 
                        f"the upcoming {second_integer_abs} months", 
                        f"the succeeding {second_integer_abs} months"
                    ])
    
    elif match := re.search(this_year_offset_pattern, annotation):
        first_integer, second_integer = match.group(1), match.group(2)
        first_integer_abs, second_integer_abs = abs(int(first_integer)), abs(int(second_integer))
        
        if first_integer_abs == second_integer_abs:
            if second_integer[0] == "-":
                if second_integer_abs == 1:
                    return random.choice(["last year", "the previous year", "a year ago", "the past year", "the preceding year"])
                elif second_integer_abs >= 2:
                    return random.choice([
                        f"last {second_integer_abs} years", 
                        f"the previous {second_integer_abs} years", 
                        f"{second_integer_abs} years ago", 
                        f"the past {second_integer_abs} years", 
                        f"the preceding {second_integer_abs} years"
                    ])
            else:
                if second_integer_abs == 1:
                    return random.choice(["next year", "the following year", "a year later", "the upcoming year", "the succeeding year"])
                elif second_integer_abs >= 2:
                    return random.choice([
                        f"next {second_integer_abs} years", 
                        f"the following {second_integer_abs} years", 
                        f"{second_integer_abs} years later", 
                        f"the upcoming {second_integer_abs} years", 
                        f"the succeeding {second_integer_abs} years"
                    ])
    
    elif match := re.search(day_offset_pattern, annotation):
        first_integer = match.group(1)
        first_integer_abs = abs(int(first_integer))
        
        if first_integer[0] == "-":
            if first_integer_abs == 1:
                return random.choice(["yesterday", "the previous day", "one day ago", "the day before", "a day earlier"])
            elif first_integer_abs >= 2:
                return random.choice([
                    f"{first_integer_abs} days ago", 
                    f"the past {first_integer_abs} days", 
                    f"the preceding {first_integer_abs} days", 
                    f"{first_integer_abs} days earlier", 
                    f"{first_integer_abs} days in the past"
                ])
        else:
            if first_integer_abs == 1:
                return random.choice(["tomorrow", "the next day", "one day later", "the day after", "a day ahead"])
            elif first_integer_abs >= 2:
                return random.choice([
                    f"{first_integer_abs} days later", 
                    f"the next {first_integer_abs} days", 
                    f"the following {first_integer_abs} days", 
                    f"{first_integer_abs} days in the future", 
                    f"{first_integer_abs} days ahead"
                ])
    
    elif match := re.search(week_offset_pattern, annotation):
        first_integer = match.group(1)
        first_integer_abs = abs(int(first_integer))
        
        if first_integer[0] == "-":
            if first_integer_abs == 1:
                return random.choice(["a week ago", "the previous week", "one week ago", "the past week", "the preceding week"])
            elif first_integer_abs >= 2:
                return random.choice([
                    f"{first_integer_abs} weeks ago", 
                    f"the past {first_integer_abs} weeks", 
                    f"the preceding {first_integer_abs} weeks", 
                    f"{first_integer_abs} weeks earlier", 
                    f"{first_integer_abs} weeks in the past"
                ])
        else:
            if first_integer_abs == 1:
                return random.choice(["a week later", "the next week", "one week later", "the following week", "a week ahead"])
            elif first_integer_abs >= 2:
                return random.choice([
                    f"{first_integer_abs} weeks later", 
                    f"the next {first_integer_abs} weeks", 
                    f"the following {first_integer_abs} weeks", 
                    f"{first_integer_abs} weeks in the future", 
                    f"{first_integer_abs} weeks ahead"
                ])
    
    elif match := re.search(month_offset_pattern, annotation):
        first_integer = match.group(1)
        first_integer_abs = abs(int(first_integer))
        
        if first_integer[0] == "-":
            if first_integer_abs == 1:
                return random.choice(["a month ago", "the previous month", "one month ago", "the past month", "the preceding month"])
            elif first_integer_abs >= 2:
                return random.choice([
                    f"{first_integer_abs} months ago", 
                    f"the past {first_integer_abs} months", 
                    f"the preceding {first_integer_abs} months", 
                    f"{first_integer_abs} months earlier", 
                    f"{first_integer_abs} months in the past"
                ])
        else:
            if first_integer_abs == 1:
                return random.choice(["a month later", "the next month", "one month later", "the following month", "a month ahead"])
            elif first_integer_abs >= 2:
                return random.choice([
                    f"{first_integer_abs} months later", 
                    f"the next {first_integer_abs} months", 
                    f"the following {first_integer_abs} months", 
                    f"{first_integer_abs} months in the future", 
                    f"{first_integer_abs} months ahead"
                ])
    
    elif match := re.search(year_offset_pattern, annotation):
        first_integer = match.group(1)
        first_integer_abs = abs(int(first_integer))
        
        if first_integer[0] == "-":
            if first_integer_abs == 1:
                return random.choice(["a year ago", "the previous year", "one year ago", "the past year", "the preceding year"])
            elif first_integer_abs >= 2:
                return random.choice([
                    f"{first_integer_abs} years ago", 
                    f"the past {first_integer_abs} years", 
                    f"the preceding {first_integer_abs} years", 
                    f"{first_integer_abs} years earlier", 
                    f"{first_integer_abs} years in the past"
                ])
        else:
            if first_integer_abs == 1:
                return random.choice(["a year later", "the next year", "one year later", "the following year", "a year ahead"])
            elif first_integer_abs >= 2:
                return random.choice([
                    f"{first_integer_abs} years later", 
                    f"the next {first_integer_abs} years", 
                    f"the following {first_integer_abs} years", 
                    f"{first_integer_abs} years in the future", 
                    f"{first_integer_abs} years ahead"
                ])
    
    elif match := re.search(day_this_pattern, annotation):
        first_integer = int(match.group(1))
        
        if first_integer == 1:
            return random.choice(["today", "this day", "the current day", "the present day", "this very day"])
        elif first_integer > 1:
            return random.choice([
                f"these {first_integer} days", 
                f"the current {first_integer} days", 
                f"the present {first_integer} days", 
                f"these very {first_integer} days", 
                f"this span of {first_integer} days"
            ])
    
    elif match := re.search(week_this_pattern, annotation):
        first_integer = int(match.group(1))
        
        if first_integer == 1:
            return random.choice(["this week", "the current week", "the present week", "this very week", "this span of a week"])
        elif first_integer > 1:
            return random.choice([
                f"these {first_integer} weeks", 
                f"the current {first_integer} weeks", 
                f"the present {first_integer} weeks", 
                f"these very {first_integer} weeks", 
                f"this span of {first_integer} weeks"
            ])
    
    elif match := re.search(month_this_pattern, annotation):
        first_integer = int(match.group(1))
        
        if first_integer == 1:
            return random.choice(["this month", "the current month", "the present month", "this very month", "this span of a month"])
        elif first_integer > 1:
            return random.choice([
                f"these {first_integer} months", 
                f"the current {first_integer} months", 
                f"the present {first_integer} months", 
                f"these very {first_integer} months", 
                f"this span of {first_integer} months"
            ])
    
    elif match := re.search(year_this_pattern, annotation):
        first_integer = int(match.group(1))
        
        if first_integer == 1:
            return random.choice(["this year", "the current year", "the present year", "this very year", "this span of a year"])
        elif first_integer > 1:
            return random.choice([
                f"these {first_integer} years", 
                f"the current {first_integer} years", 
                f"the present {first_integer} years", 
                f"these very {first_integer} years", 
                f"this span of {first_integer} years"
            ])
    
    elif match := re.search(day_immediate_pattern, annotation):
        first_integer = int(match.group(1))
        
        if "PREV_IMMEDIATE" in annotation:
            if first_integer == 1:
                return random.choice(["the last day", "the previous day", "one day ago", "the day before", "a day earlier"])
            elif first_integer > 1:
                return random.choice([
                    f"these past {first_integer} days", 
                    f"the preceding {first_integer} days", 
                    f"{first_integer} days ago", 
                    f"{first_integer} days earlier", 
                    f"{first_integer} days in the past"
                ])
        
        if "NEXT_IMMEDIATE" in annotation:
            if first_integer == 1:
                return random.choice(["the next day", "the following day", "one day later", "the day after", "a day ahead"])
            elif first_integer > 1:
                return random.choice([
                    f"these next {first_integer} days", 
                    f"the succeeding {first_integer} days", 
                    f"{first_integer} days later", 
                    f"{first_integer} days in the future", 
                    f"{first_integer} days ahead"
                ])
        
        return None
    
    elif match := re.search(week_immediate_pattern, annotation):
        first_integer = int(match.group(1))
        
        if "PREV_IMMEDIATE" in annotation:
            if first_integer == 1:
                return random.choice(["the last week", "the previous week", "one week ago", "the week before", "a week earlier"])
            elif first_integer > 1:
                return random.choice([
                    f"these past {first_integer} weeks", 
                    f"the preceding {first_integer} weeks", 
                    f"{first_integer} weeks ago", 
                    f"{first_integer} weeks earlier", 
                    f"{first_integer} weeks in the past"
                ])
        
        if "NEXT_IMMEDIATE" in annotation:
            if first_integer == 1:
                return random.choice(["the next week", "the following week", "one week later", "the week after", "a week ahead"])
            elif first_integer > 1:
                return random.choice([
                    f"these next {first_integer} weeks", 
                    f"the succeeding {first_integer} weeks", 
                    f"{first_integer} weeks later", 
                    f"{first_integer} weeks in the future", 
                    f"{first_integer} weeks ahead"
                ])
        
        return None
    
    elif match := re.search(month_immediate_pattern, annotation):
        first_integer = int(match.group(1))
        
        if "PREV_IMMEDIATE" in annotation:
            if first_integer == 1:
                return random.choice(["the last month", "the previous month", "one month ago", "the month before", "a month earlier"])
            elif first_integer > 1:
                return random.choice([
                    f"these past {first_integer} months", 
                    f"the preceding {first_integer} months", 
                    f"{first_integer} months ago", 
                    f"{first_integer} months earlier", 
                    f"{first_integer} months in the past"
                ])
        
        if "NEXT_IMMEDIATE" in annotation:
            if first_integer == 1:
                return random.choice(["the next month", "the following month", "one month later", "the month after", "a month ahead"])
            elif first_integer > 1:
                return random.choice([
                    f"these next {first_integer} months", 
                    f"the succeeding {first_integer} months", 
                    f"{first_integer} months later", 
                    f"{first_integer} months in the future", 
                    f"{first_integer} months ahead"
                ])
        
        return None
    
    elif match := re.search(year_immediate_pattern, annotation):
        first_integer = int(match.group(1))
        
        if "PREV_IMMEDIATE" in annotation:
            if first_integer == 1:
                return random.choice(["the last year", "the previous year", "one year ago", "the year before", "a year earlier"])
            elif first_integer > 1:
                return random.choice([
                    f"these past {first_integer} years", 
                    f"the preceding {first_integer} years", 
                    f"{first_integer} years ago", 
                    f"{first_integer} years earlier", 
                    f"{first_integer} years in the past"
                ])
        
        if "NEXT_IMMEDIATE" in annotation:
            if first_integer == 1:
                return random.choice(["the next year", "the following year", "one year later", "the year after", "a year ahead"])
            elif first_integer > 1:
                return random.choice([
                    f"these next {first_integer} years", 
                    f"the succeeding {first_integer} years", 
                    f"{first_integer} years later", 
                    f"{first_integer} years in the future", 
                    f"{first_integer} years ahead"
                ])
        
        return None
    
    return None