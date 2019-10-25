import datetime
from constants import Constants


def convert_str_to_date(date_time_string, date_format):
    return datetime.datetime.strftime(datetime.datetime.strptime(date_time_string,
                                                                 Constants.DATE_YEAR_AND_MONTH_DAY_FORMAT), date_format)
