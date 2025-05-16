import re
import random
from temporal_embeddings.synthetic_data.utils.periods.is_period import is_period
from temporal_embeddings.data_utils.utils.extract_integers import extract_integers

def period_to_text(annotation):
    is_period_bool, period_format = is_period(annotation)
    
    if is_period_bool:
        extracted_integers = extract_integers(annotation)
        
        if period_format == "pd":
            options = [
                "a day", "one day", "just a day", "a single day", "1 day",
                "a full day", "a single 24-hour period", "one full day", "a single calendar day", "a day-long period"
            ] if extracted_integers[0] == 1 else [
                f"{extracted_integers[0]} days", f"{extracted_integers[0]} full days", f"{extracted_integers[0]} calendar days",
                f"{extracted_integers[0]} day-long periods", f"about {extracted_integers[0]} days", f"nearly {extracted_integers[0]} days",
                f"approximately {extracted_integers[0]} days", f"{extracted_integers[0]} consecutive days", f"{extracted_integers[0]} 24-hour periods", f"{extracted_integers[0]} days in total"
            ]
            return random.choice(options)
        
        elif period_format == "pw":
            options = [
                "a week", "one week", "just a week", "a single week", "1 week",
                "a full week", "a seven-day period", "one full week", "a single calendar week", "a week-long period"
            ] if extracted_integers[0] == 1 else [
                f"{extracted_integers[0]} weeks", f"{extracted_integers[0]} full weeks", f"{extracted_integers[0]} calendar weeks",
                f"{extracted_integers[0]} week-long periods", f"about {extracted_integers[0]} weeks", f"nearly {extracted_integers[0]} weeks",
                f"approximately {extracted_integers[0]} weeks", f"{extracted_integers[0]} consecutive weeks", f"{extracted_integers[0]} seven-day periods", f"{extracted_integers[0]} weeks in total"
            ]
            return random.choice(options)
        
        elif period_format == "pm":
            options = [
                "a month", "one month", "just a month", "a single month", "1 month",
                "a full month", "a 30-day period", "one full month", "a single calendar month", "a month-long period"
            ] if extracted_integers[0] == 1 else [
                f"{extracted_integers[0]} months", f"{extracted_integers[0]} full months", f"{extracted_integers[0]} calendar months",
                f"{extracted_integers[0]} month-long periods", f"about {extracted_integers[0]} months", f"nearly {extracted_integers[0]} months",
                f"approximately {extracted_integers[0]} months", f"{extracted_integers[0]} consecutive months", f"{extracted_integers[0]} 30-day periods", f"{extracted_integers[0]} months in total"
            ]
            return random.choice(options)
        
        elif period_format == "py":
            options = [
                "a year", "one year", "just a year", "a single year", "1 year",
                "a full year", "a 12-month period", "one full year", "a single calendar year", "a year-long period"
            ] if extracted_integers[0] == 1 else [
                f"{extracted_integers[0]} years", f"{extracted_integers[0]} full years", f"{extracted_integers[0]} calendar years",
                f"{extracted_integers[0]} year-long periods", f"about {extracted_integers[0]} years", f"nearly {extracted_integers[0]} years",
                f"approximately {extracted_integers[0]} years", f"{extracted_integers[0]} consecutive years", f"{extracted_integers[0]} 12-month periods", f"{extracted_integers[0]} years in total"
            ]
            return random.choice(options)
        
        elif period_format == "pdi":
            options = [
                f"{extracted_integers[0]} to {extracted_integers[1]} days", f"between {extracted_integers[0]} and {extracted_integers[1]} days",
                f"from {extracted_integers[0]} to {extracted_integers[1]} days", f"around {extracted_integers[0]}-{extracted_integers[1]} days",
                f"approximately {extracted_integers[0]} to {extracted_integers[1]} days", f"nearly {extracted_integers[0]}-{extracted_integers[1]} days",
                f"{extracted_integers[0]}-{extracted_integers[1]} days range", f"about {extracted_integers[0]} to {extracted_integers[1]} days",
                f"{extracted_integers[0]}-{extracted_integers[1]} days in total", f"roughly {extracted_integers[0]} to {extracted_integers[1]} days"
            ]
            return random.choice(options)
        
        elif period_format == "pwi":
            options = [
                f"{extracted_integers[0]} to {extracted_integers[1]} weeks", f"between {extracted_integers[0]} and {extracted_integers[1]} weeks",
                f"from {extracted_integers[0]} to {extracted_integers[1]} weeks", f"around {extracted_integers[0]}-{extracted_integers[1]} weeks",
                f"approximately {extracted_integers[0]} to {extracted_integers[1]} weeks", f"nearly {extracted_integers[0]}-{extracted_integers[1]} weeks",
                f"{extracted_integers[0]}-{extracted_integers[1]} weeks range", f"about {extracted_integers[0]} to {extracted_integers[1]} weeks",
                f"{extracted_integers[0]}-{extracted_integers[1]} weeks in total", f"roughly {extracted_integers[0]} to {extracted_integers[1]} weeks"
            ]
            return random.choice(options)
        
        elif period_format == "pmi":
            options = [
                f"{extracted_integers[0]} to {extracted_integers[1]} months", f"between {extracted_integers[0]} and {extracted_integers[1]} months",
                f"from {extracted_integers[0]} to {extracted_integers[1]} months", f"around {extracted_integers[0]}-{extracted_integers[1]} months",
                f"approximately {extracted_integers[0]} to {extracted_integers[1]} months", f"nearly {extracted_integers[0]}-{extracted_integers[1]} months",
                f"{extracted_integers[0]}-{extracted_integers[1]} months range", f"about {extracted_integers[0]} to {extracted_integers[1]} months",
                f"{extracted_integers[0]}-{extracted_integers[1]} months in total", f"roughly {extracted_integers[0]} to {extracted_integers[1]} months"
            ]
            return random.choice(options)
        
        elif period_format == "pyi":
            options = [
                f"{extracted_integers[0]} to {extracted_integers[1]} years", f"between {extracted_integers[0]} and {extracted_integers[1]} years",
                f"from {extracted_integers[0]} to {extracted_integers[1]} years", f"around {extracted_integers[0]}-{extracted_integers[1]} years",
                f"approximately {extracted_integers[0]} to {extracted_integers[1]} years", f"nearly {extracted_integers[0]}-{extracted_integers[1]} years",
                f"{extracted_integers[0]}-{extracted_integers[1]} years range", f"about {extracted_integers[0]} to {extracted_integers[1]} years",
                f"{extracted_integers[0]}-{extracted_integers[1]} years in total", f"roughly {extracted_integers[0]} to {extracted_integers[1]} years"
            ]
            return random.choice(options)
        
        elif period_format == "pdn":
            options = [
                "first day", "day one", "the initial day", "the first 24 hours", "the starting day",
                "day 1", "the first calendar day", "the first day of the period", "the first day in sequence", "the first day overall"
            ] if extracted_integers[1] == 1 else [
                f"{extracted_integers[1]}th day", f"day {extracted_integers[1]}", f"the {extracted_integers[1]}th calendar day",
                f"the {extracted_integers[1]}th day of the period", f"the {extracted_integers[1]}th day in sequence", f"the {extracted_integers[1]}th day overall",
                f"day {extracted_integers[1]} in total", f"the {extracted_integers[1]}th day of the timeline", f"the {extracted_integers[1]}th day in order", f"the {extracted_integers[1]}th day of the range"
            ]
            return random.choice(options)
        
        elif period_format == "pwn":
            options = [
                "first week", "week one", "the initial week", "the first 7 days", "the starting week",
                "week 1", "the first calendar week", "the first week of the period", "the first week in sequence", "the first week overall"
            ] if extracted_integers[1] == 1 else [
                f"{extracted_integers[1]}th week", f"week {extracted_integers[1]}", f"the {extracted_integers[1]}th calendar week",
                f"the {extracted_integers[1]}th week of the period", f"the {extracted_integers[1]}th week in sequence", f"the {extracted_integers[1]}th week overall",
                f"week {extracted_integers[1]} in total", f"the {extracted_integers[1]}th week of the timeline", f"the {extracted_integers[1]}th week in order", f"the {extracted_integers[1]}th week of the range"
            ]
            return random.choice(options)
        
        elif period_format == "pmn":
            options = [
                "first month", "month one", "the initial month", "the first 30 days", "the starting month",
                "month 1", "the first calendar month", "the first month of the period", "the first month in sequence", "the first month overall"
            ] if extracted_integers[1] == 1 else [
                f"{extracted_integers[1]}th month", f"month {extracted_integers[1]}", f"the {extracted_integers[1]}th calendar month",
                f"the {extracted_integers[1]}th month of the period", f"the {extracted_integers[1]}th month in sequence", f"the {extracted_integers[1]}th month overall",
                f"month {extracted_integers[1]} in total", f"the {extracted_integers[1]}th month of the timeline", f"the {extracted_integers[1]}th month in order", f"the {extracted_integers[1]}th month of the range"
            ]
            return random.choice(options)
        
        elif period_format == "pyn":
            options = [
                "first year", "year one", "the initial year", "the first 12 months", "the starting year",
                "year 1", "the first calendar year", "the first year of the period", "the first year in sequence", "the first year overall"
            ] if extracted_integers[1] == 1 else [
                f"{extracted_integers[1]}th year", f"year {extracted_integers[1]}", f"the {extracted_integers[1]}th calendar year",
                f"the {extracted_integers[1]}th year of the period", f"the {extracted_integers[1]}th year in sequence", f"the {extracted_integers[1]}th year overall",
                f"year {extracted_integers[1]} in total", f"the {extracted_integers[1]}th year of the timeline", f"the {extracted_integers[1]}th year in order", f"the {extracted_integers[1]}th year of the range"
            ]
            return random.choice(options)
    
    return None