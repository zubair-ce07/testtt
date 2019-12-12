from enum import Enum


CITY_NAME = 'Murree'

COLUMN_NAMES = ['PKT',
                'MAX_TEMP',
                'MEAN_TEMP',
                'MIN_TEMP',
                'MAX_DEW',
                'MEAN_DEW',
                'MIN_DEW',
                'MAX_HUMIDITY',
                'MEAN_HUMIDITY',
                'MIN_HUMIDITY']


class Colors(Enum):
    RED = 31
    BLUE = 34


class ReportTypes(Enum):
    SHOW_EXTREMES = 1
    SHOW_MEANS = 2
    SHOW_GRAPHS = 3
