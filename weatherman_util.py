from datetime import datetime
from calendar import calendar
import ntpath
import glob
import calendar
from WeatherDataParser import WeatherDataParser
from WeatherData import WeatherData


def file_month(f):
    filename = ntpath.basename(f).split('.')[0]  # get filename and remove extension
    return filename.split('_')[-1]


def file_year(f):
    filename = ntpath.basename(f).split('.')[0]  # get filename and remove extension
    return filename.split('_')[-2]


def month_abbr(month_string):
    # Create dictionary which maps month number to month abbreviation
    abbr_dict = {k: v for k, v in enumerate(calendar.month_abbr)}
    month_number = int(month_string.split('/')[-1])  # Extract month number from string i.e. 2004/6
    return abbr_dict[month_number]


def extract_year(month_string):
    return month_string.split('/')[0]  # Extract year from string i.e. 2004/6


def parse_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d')


def format_date(d):
    return d.strftime('%b %d')


def get_files(directory):
    return glob.glob(directory)


def matches_month(month,year):
    def test(data):
        _year = data.date.year
        _month = data.date.month
        return all([_year == year, _month == month])

    return test
    
