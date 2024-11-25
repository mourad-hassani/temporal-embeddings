from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta

def get_week_dates(date, offset, num_weeks = 1):
    date = datetime.strptime(date, "%Y-%m-%d").date()

    start_of_week = date - timedelta(days=date.weekday())
    start_of_week += timedelta(days=7 * offset)
    end_of_week = start_of_week + timedelta(days=7 * num_weeks)
    
    return [start_of_week.strftime("%Y-%m-%d"), end_of_week.strftime("%Y-%m-%d")]


def get_month_dates(date, offset, num_months = 1):
    date = datetime.strptime(date, "%Y-%m-%d").date()

    first_date = date + relativedelta(months=offset)
    second_date = first_date + relativedelta(months=(num_months - 1))

    first_year = str(first_date.year)
    first_month = str(first_date.month)

    second_year = str(second_date.year)
    second_month = str(second_date.month)

    if len(first_month) == 1:
        first_month = f"0{first_month}"
    
    if len(first_year) < 4:
        first_year = f"000{first_year}"[-4:]
    
    if len(second_month) == 1:
        second_month = f"0{second_month}"
    
    if len(second_year) < 4:
        second_year = f"000{second_year}"[-4:]
    
    last_day = calendar.monthrange(int(second_year), int(second_month))[1]
    
    return [f"{first_year}-{first_month}-01", f"{second_year}-{second_month}-{last_day}"]

def get_year_dates(date, offset, num_years = 1):
    date = datetime.strptime(date, "%Y-%m-%d").date()

    first_date = date + relativedelta(years=offset)
    second_date = first_date + relativedelta(years=(num_years - 1))

    first_year = str(first_date.year)

    second_year = str(second_date.year)
    
    if len(first_year) < 4:
        first_year = f"000{first_year}"[-4:]
    
    if len(second_year) < 4:
        second_year = f"000{second_year}"[-4:]
    
    return [f"{first_year}-01-01", f"{second_year}-12-31"]