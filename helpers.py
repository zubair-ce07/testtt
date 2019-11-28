from datetime import datetime
from weathermanconstants import WeatherManConstants


def convert_str_to_date(date_time_string, date_format):
    return datetime.strftime(datetime.strptime(date_time_string,
                                               WeatherManConstants.DATE_YEAR_AND_MONTH_DAY_FORMAT), date_format)
