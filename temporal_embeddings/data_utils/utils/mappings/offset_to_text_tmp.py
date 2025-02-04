import re

def offset_to_text(annotation):
    pattern_dict = {
        r'^OFFSET P(1)D$': ['tomorrow', 'the next day', 'the following day', 'in a day', 'one day later'],
        r'^OFFSET P(1)W$': ['a week later', 'in a week', 'the next week', 'seven days later', 'one week from now'],
        r'^OFFSET P(1)M$': ['a month later', 'in a month', 'the next month', 'four weeks later', 'one month from now'],
        r'^OFFSET P(1)Y$': ['a year later', 'in a year', 'the next year', 'twelve months later', 'one year from now'],

        r'^OFFSET P(\d+)D$': ['{} days later', 'in {} days', '{} days from now', 'after {} days', 'following {} days'],
        r'^OFFSET P(\d+)W$': ['{} weeks later', 'in {} weeks', '{} weeks from now', 'after {} weeks', 'following {} weeks'],
        r'^OFFSET P(\d+)M$': ['{} months later', 'in {} months', '{} months from now', 'after {} months', 'following {} months'],
        r'^OFFSET P(\d+)Y$': ['{} years later', 'in {} years', '{} years from now', 'after {} years', 'following {} years'],

        r'^OFFSET P(-1)D$': ['yesterday', 'the previous day', 'the day before', 'one day ago', 'a day earlier'],
        r'^OFFSET P(-1)W$': ['a week ago', 'the previous week', 'one week earlier', 'seven days ago', 'last week'],
        r'^OFFSET P(-1)M$': ['a month ago', 'the previous month', 'one month earlier', 'four weeks ago', 'last month'],
        r'^OFFSET P(-1)Y$': ['a year ago', 'the previous year', 'one year earlier', 'twelve months ago', 'last year'],

        r'^OFFSET P(-\d+)D$': ['{} days ago', '{} days earlier', '{} days before', '{} days in the past'],
        r'^OFFSET P(-\d+)W$': ['{} weeks ago', '{} weeks earlier', '{} weeks before', '{} weeks in the past'],
        r'^OFFSET P(-\d+)M$': ['{} months ago', '{} months earlier', '{} months before', '{} months in the past'],
        r'^OFFSET P(-\d+)Y$': ['{} years ago', '{} years earlier', '{} years before', '{} years in the past'],

        r'^THIS P1D OFFSET P(1)D$': ['next day', 'the following day', 'the day after', 'in one day', 'tomorrow'],
        r'^THIS P1W OFFSET P(1)W$': ['next week', 'the following week', 'a week after', 'seven days after', 'in a week'],
        r'^THIS P1M OFFSET P(1)M$': ['next month', 'the following month', 'a month after', 'four weeks after', 'in a month'],
        r'^THIS P1Y OFFSET P(1)Y$': ['next year', 'the following year', 'a year after', 'twelve months after', 'in a year'],

        r'^THIS P1D OFFSET P(\d+)D$': ['next {} days', 'the following {} days', '{} days after', 'in the coming {} days'],
        r'^THIS P1W OFFSET P(\d+)W$': ['next {} weeks', 'the following {} weeks', '{} weeks after', 'in the coming {} weeks'],
        r'^THIS P1M OFFSET P(\d+)M$': ['next {} months', 'the following {} months', '{} months after', 'in the coming {} months'],
        r'^THIS P1Y OFFSET P(\d+)Y$': ['next {} years', 'the following {} years', '{} years after', 'in the coming {} years'],

        r'^THIS P1D OFFSET P(-1)D$': ['last day', 'the previous day', 'the day before', 'yesterday', 'one day earlier'],
        r'^THIS P1W OFFSET P(-1)W$': ['last week', 'the previous week', 'the week before', 'seven days earlier', 'a week ago'],
        r'^THIS P1M OFFSET P(-1)M$': ['last month', 'the previous month', 'the month before', 'four weeks earlier', 'a month ago'],
        r'^THIS P1Y OFFSET P(-1)Y$': ['last year', 'the previous year', 'the year before', 'twelve months earlier', 'a year ago'],

        r'^THIS P1D OFFSET P(-\d+)D$': ['last {} days', 'the previous {} days', '{} days before', '{} days earlier'],
        r'^THIS P1W OFFSET P(-\d+)W$': ['last {} weeks', 'the previous {} weeks', '{} weeks before', '{} weeks earlier'],
        r'^THIS P1M OFFSET P(-\d+)M$': ['last {} months', 'the previous {} months', '{} months before', '{} months earlier'],
        r'^THIS P1Y OFFSET P(-\d+)Y$': ['last {} years', 'the previous {} years', '{} years before', '{} years earlier'],

        r'^THIS P(1)D$': ['today', 'this day', 'current day', 'the present day'],
        r'^THIS P(1)W$': ['this week', 'current week', 'the present week', 'the ongoing week'],
        r'^THIS P(1)M$': ['this month', 'current month', 'the present month', 'the ongoing month'],
        r'^THIS P(1)Y$': ['this year', 'current year', 'the present year', 'the ongoing year'],

        r'^THIS P(\d+)D$': ['these {} days', 'the next {} days', 'the coming {} days', '{} days from now'],
        r'^THIS P(\d+)W$': ['these {} weeks', 'the next {} weeks', 'the coming {} weeks', '{} weeks from now'],
        r'^THIS P(\d+)M$': ['these {} months', 'the next {} months', 'the coming {} months', '{} months from now'],
        r'^THIS P(\d+)Y$': ['these {} years', 'the next {} years', 'the coming {} years', '{} years from now'],

        r'^NEXT_IMMEDIATE P(1)D$': ['the next day', 'tomorrow', 'the following day', 'one day later'],
        r'^NEXT_IMMEDIATE P(1)W$': ['the next week', 'the following week', 'a week later', 'seven days later'],
        r'^NEXT_IMMEDIATE P(1)M$': ['the next month', 'the following month', 'a month later', 'four weeks later'],
        r'^NEXT_IMMEDIATE P(1)Y$': ['the next year', 'the following year', 'a year later', 'twelve months later'],

        r'^NEXT_IMMEDIATE P(\d+)D$': ['the next {} days', '{} days from now', 'the coming {} days', 'after {} days'],
        r'^NEXT_IMMEDIATE P(\d+)W$': ['the next {} weeks', '{} weeks from now', 'the coming {} weeks', 'after {} weeks'],
        r'^NEXT_IMMEDIATE P(\d+)M$': ['the next {} months', '{} months from now', 'the coming {} months', 'after {} months'],
        r'^NEXT_IMMEDIATE P(\d+)Y$': ['the next {} years', '{} years from now', 'the coming {} years', 'after {} years'],

        r'^PREV_IMMEDIATE P(1)D$': ['the last day', 'yesterday', 'the previous day', 'one day earlier'],
        r'^PREV_IMMEDIATE P(1)W$': ['the last week', 'the previous week', 'a week ago', 'seven days earlier'],
        r'^PREV_IMMEDIATE P(1)M$': ['the last month', 'the previous month', 'a month ago', 'four weeks earlier'],
        r'^PREV_IMMEDIATE P(1)Y$': ['the last year', 'the previous year', 'a year ago', 'twelve months earlier'],

        r'^PREV_IMMEDIATE P(\d+)D$': ['these past {} days', '{} days ago', '{} days earlier', '{} days before'],
        r'^PREV_IMMEDIATE P(\d+)W$': ['these past {} weeks', '{} weeks ago', '{} weeks earlier', '{} weeks before'],
        r'^PREV_IMMEDIATE P(\d+)M$': ['these past {} months', '{} months ago', '{} months earlier', '{} months before'],
        r'^PREV_IMMEDIATE P(\d+)Y$': ['these past {} years', '{} years ago', '{} years earlier', '{} years before'],
    }

    for pattern, text in pattern_dict.items():
        match = re.search(pattern, annotation)
        
        if match:
            value: int = abs(int(match.group(1)))

            return text.format(value)

    return None