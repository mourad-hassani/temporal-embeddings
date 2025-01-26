import re
from temporal_embeddings.data_utils.utils.extract_integers import extract_integers

def is_offset(text):
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

    patterns_dicts = {day_offset_pattern: "d", week_offset_pattern: "w", month_offset_pattern: "m", year_offset_pattern: "y", this_day_offset_pattern: "td", this_week_offset_pattern: "tw", this_month_offset_pattern: "tm", this_year_offset_pattern: "ty", day_this_pattern: "thisd", week_this_pattern: "thisw", month_this_pattern: "thism", year_this_pattern: "thisy", day_immediate_pattern: "immediated", week_immediate_pattern: "immediatew", month_immediate_pattern: "immediatem", year_immediate_pattern: "immediatey"}
    patterns = [k for k, v in patterns_dicts.items()]

    for pattern in patterns:
        if re.match(pattern=pattern, string=text):
            pattern_detected = patterns_dicts[pattern]
            if abs(extract_integers(text)[-1]) < 30:
                return True, pattern_detected
    
    return False, "Invalid format"