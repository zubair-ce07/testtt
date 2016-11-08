import constants as const
from datetime import datetime
import w_exceptions as exc



def parse_month(month):
    try:
        date = datetime.strptime(month, "%Y/%m")
    except:    
        raise exc.InvalidMonthFormat(month=month)

    validate_year(date.year)
    month = validate_month(date.month)
    return date.strftime("%Y_%b")


def validate_year(year):
    try:
        year = int(year)
    except:
        raise

    if year < 0:
        raise exc.InvalidYearInput(year=year)

    return year


def validate_month(month):
    try:
        month = int(month)
    except:
        raise

    if month < 1 or month > 12:
        raise exc.InvalidMonthRange(month=month)

    return month


def get_month_day(data):
    try:
        date = datetime.strptime(data[const.DATE], const.DATE_FORMAT)
    except:
        date = datetime.strptime(data[const.DATE_ALT], const.DATE_FORMAT)

    return date.strftime("%B %d")
