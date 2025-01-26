from temporal_embeddings.synthetic_data.utils.dates.is_date import is_date

def is_interval(annotation):
    if "," in annotation:
        annotation = annotation.split(",")
        return is_date(annotation[0])[0] and is_date(annotation[1])[0], "interval"
    return False, "interval"