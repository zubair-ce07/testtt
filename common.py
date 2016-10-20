import constants as const
import w_exceptions as exc


def parse_month(month):
    date = month.split("/")
    if len(date) != 2:
        raise exc.InvalidMonthFormat(month=month)

    validate_year(date[0])
    month = validate_month(date[1])
    return date[0] + '_' + const.MONTHS[month-1]


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


def get_day(date):
    date = date.split("-")
    month = const.MONTHS[int(date[1]) - 1]
    return month + " " + date[2]
