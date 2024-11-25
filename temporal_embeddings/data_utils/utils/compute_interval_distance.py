from datetime import datetime

def compute_interval_distance(interval1, interval2):
    x, y = sorted((interval1, interval2))

    if x[0] <= x[1] < y[0] and all(y[0] <= y[1] for y in (interval1, interval2)):
        return y[0] - x[1]
    else:
        return 0

def compute_interval_distance_date(interval1, interval2):
    """
    This function needs to take into consideration : 
        - Overlapping.
        - Inclusion.
    """
    
    interval1 = [days_since_base(interval1[0]), days_since_base(interval1[1])]
    interval2 = [days_since_base(interval2[0]), days_since_base(interval2[1])]

    interval1 = sorted(interval1)
    interval2 = sorted(interval2)
    
    start1, end1 = interval1
    start2, end2 = interval2

    if start1 == start2 and end1 == end2:
        return 1.0, True

    if start1 < start2 and end1 > end2:
        return 0.9, True
    
    if end1 >= start2 and end2 >= start1:
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)
        overlap_length = overlap_end - overlap_start + 1
        union_start = min(start1, start2)
        union_end = max(end1, end2)
        union_length = union_end - union_start + 1
        overlap_fraction = overlap_length / union_length
        return min(0.2, overlap_fraction), True
    
    distance = max(start2 - end1, start1 - end2)

    unit = min(abs(interval1[0] - interval1[1]) + 1, abs(interval2[0] - interval2[1]) + 1)

    if (distance / unit) < 10:
        output_distance = distance
    else:
        output_distance = (distance / unit)

    return output_distance, False

def days_since_base(date_string, base_date_string="1000-01-01"):
    date = datetime.strptime(date_string, "%Y-%m-%d")
    base_date = datetime.strptime(base_date_string, "%Y-%m-%d")
    
    days_difference = (date - base_date).days
    return days_difference