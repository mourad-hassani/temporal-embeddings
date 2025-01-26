import re
from temporal_embeddings.data_utils.utils.extract_integers import extract_integers

def is_period(text):
    day_pattern = r'^P\d+D$'
    month_pattern = r'^P\d+M$'
    year_pattern = r'^P\d+Y$'
    week_pattern = r'^P\d+W$'

    day_pattern_i = r'^P\d+D/P\d+D$'
    month_pattern_i = r'^P\d+M/P\d+M$'
    year_pattern_i = r'^P\d+Y/P\d+Y$'
    week_pattern_i = r'^P\d+W/P\d+W$'

    day_pattern_n = r'^P1D-#\d+$'
    month_pattern_n = r'^P1M-#\d+$'
    year_pattern_n = r'^P1Y-#\d+$'
    week_pattern_n = r'^P1W-#\d+$'

    patterns_dicts = {day_pattern: "pd", month_pattern: "pm", year_pattern: "py", week_pattern: "pw", day_pattern_i: "pdi", month_pattern_i: "pmi", year_pattern_i: "pyi", week_pattern_i: "pwi", day_pattern_n: "pdn", month_pattern_n: "pmn", year_pattern_n: "pyn", week_pattern_n: "pwn"}
    patterns = [k for k, v in patterns_dicts.items()]

    for pattern in patterns:
        if re.match(pattern=pattern, string=text):
            pattern_detected = patterns_dicts[pattern]
            if pattern_detected in ["pdi", "pwi", "pmi", "pyi"]:
                if extract_integers(text)[0] < 30 and extract_integers(text)[1] < 30:
                    return True, pattern_detected
            else:
                if extract_integers(text)[0] < 30:
                    return True, pattern_detected
    return False, "Invalid format"