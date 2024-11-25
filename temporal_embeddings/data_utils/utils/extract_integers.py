import re

def extract_integers(text):
    pattern = r"-?\d+"
    return [int(match) for match in re.findall(pattern, text)]