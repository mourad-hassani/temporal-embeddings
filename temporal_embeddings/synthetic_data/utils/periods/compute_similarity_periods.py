from temporal_embeddings.data_utils.utils.extract_integers import extract_integers
from utils.compute_interval_distance import compute_interval_distance

def compute_similarity_periods(first_period, first_period_type, second_period, second_period_type):
    if first_period_type != second_period_type:
        return 0.0
    elif first_period == second_period:
        return 1.0
    else:
        first_integers, second_integers = extract_integers(first_period), extract_integers(second_period)
        if first_period_type in ["pdn", "pwn", "pmn", "pyn"]:
            distance = abs(first_integers[1] - second_integers[1])
            if distance == 0.0:
                return 1.0
            return 0.5 / distance**2
        if len(first_integers) == 1:
            distance = abs(first_integers[0] - second_integers[0])
            if distance == 0.0:
                return 1.0
            return 0.5 / distance**2
        else:
            distance = compute_interval_distance(first_integers, second_integers)
            if distance == 0:
                return 0.8
            else:
                return 0.5 / distance**2