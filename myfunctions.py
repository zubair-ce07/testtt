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


def matches_month(m,y):
    def test(data):
        _y = data.date.year
        _m = data.date.month
        return all([_y == y, _m == m])

    return test
    

def map_to_weather_obj(line):
    values = line.split(',')

    return WeatherData(date=values[WeatherDataParser.DATE],
                       max_temp=values[WeatherDataParser.MAX_TEMPERATURE],
                       mean_temp=values[WeatherDataParser.MEAN_TEMPERATURE],
                       min_temp=values[WeatherDataParser.MIN_TEMPERATURE],
                       max_humidity=values[WeatherDataParser.MAX_HUMIDITY],
                       mean_humidity=values[WeatherDataParser.MEAN_HUMIDITY],
                       min_humidity=values[WeatherDataParser.MIN_HUMIDITY])
