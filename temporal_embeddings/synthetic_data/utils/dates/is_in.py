season_to_months = {
    "WI": ["12", "01", "02"],
    "SP": ["03", "04", "05"],
    "SU": ["06", "07", "08"],
    "FA": ["09", "10", "11"],
}

def is_in(first_date, first_date_type, second_date, second_date_type):
    if first_date_type != second_date_type:
        if (first_date in second_date) or (second_date in first_date):
            return True
        elif first_date_type == "yyyy-s":
            if first_date[:4] == second_date[:4]:
                months = season_to_months[first_date[-2:]]
                month = second_date[5:7]
                if month in months:
                    return True
                else:
                    return False
            else:
                return False
        elif second_date_type == "yyyy-s":
            if first_date[:4] == second_date[:4]:
                months = season_to_months[second_date[-2:]]
                month = first_date[5:7]
                if month in months:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        raise TypeError()