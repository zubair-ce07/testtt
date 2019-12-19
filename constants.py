from enum import Enum

CITY_NAME = 'Murree'

CSV_HEADERS_MAPPING = {
    'PKT': ['PKT', 'PKST'],
    'Max TemperatureC': ['Max TemperatureC'],
    'Mean TemperatureC': ['Mean TemperatureC'],
    'Min TemperatureC': ['Min TemperatureC'],
    'Max Humidity': ['Max Humidity'],
    'Mean Humidity': ['Mean Humidity'],
    'Min Humidity': ['Min Humidity']}


class Colors(Enum):
    RED = 31
    BLUE = 34


class ReportTypes(Enum):
    SHOW_EXTREMES = 1
    SHOW_MEANS = 2
    SHOW_GRAPHS = 3
