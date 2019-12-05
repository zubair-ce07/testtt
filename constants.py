import enum


CITY_NAME = 'Murree'


class Colors(enum.Enum):
    RED = 31
    BLUE = 34


class Reports(enum.Enum):
    SHOW_EXTREMES = 1
    SHOW_MEANS = 2
    SHOW_GRAPHS = 3
