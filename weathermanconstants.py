class WeatherManConstants:
    READING_TIME_INDEX = 'PKT'
    READING_MAX_TEMP_C_INDEX = 'Max TemperatureC'
    READING_MIN_TEMP_C_INDEX = 'Min TemperatureC'
    READING_MAX_HUMIDITY_INDEX = 'Max Humidity'
    READING_MEAN_HUMIDITY_INDEX = ' Mean Humidity'

    DATE_YEAR_AND_MONTH_DAY_FORMAT = '%Y-%m-%d'
    DATE_YEAR_AND_MONTH_FORMAT = '%Y/%m'
    DATE_YEAR_FORMAT = '%Y'
    DATE_MONTH_FORMAT = '%b'
    DATE_DAY_FORMAT = '%d'
    DATE_MONTH_FULL_NAME_FORMAT = '%B'
    DATE_YEAR_AND_MONTH_SEPARATOR = "_"
    CHART_TEMP_SEPARATOR = "-"
    CHART_TEMP_BAR_ICON = "+"
    CHART_TEMP_BAR_COLD_COLOR = "\033[0;34;2m "
    CHART_TEMP_BAR_HOT_COLOR = "\033[0;31;2m "
    CHART_TEMP_BAR_LABEL_COLOR = "\033[0;35;2m "
    TEMPERATURE_CENTIGRADE_LABEL = 'C'
    PERCENT_LABEL = '%'
    INVALID_DATA = -1

    FILE_READ_MODE = 'r'
    EMPTY_STRING = ''
    SPACE_STRING = ' '
    FILE_PATH_ARGUMENT = 'filepath'
    YEAR_ARGUMENT = '-e'
    MONTH_ARGUMENT = '-a'
    MONTH_CHART_ARGUMENT = '-c'
    DIVIDER_LENGTH = 20

    #   MESSAGES    #

    INVALID_DATA_MESSAGE = "Invalid data entered"
    ON_MESSAGE = "on"
    HIGHEST_LABEL = "Highest: "
    LOWEST_LABEL = "Lowest: "
    HUMIDITY_LABEL = "Humidity: "
    HIGHEST_AVERAGE_LABEL = "Highest Average: "
    LOWEST_AVERAGE_LABEL = "Lowest Average: "
    AVERAGE_MEAN_HUMIDITY_LABEL = "Average Mean Humidity: "
    NO_DATA_FOUND_MESSAGE = 'no data found'
    FILE_PATH_ARGUMENT_MESSAGE = "weather data file path"
    YEAR_ARGUMENT_MESSAGE = "For a given year display the highest temperature and day, "\
                            "lowest temperature and day, most humid day and humidity."
    MONTH_ARGUMENT_MESSAGE = "For a given month display the average highest temperature, "\
                             "average lowest temperature, average mean humidity."
    MONTH_CHART_ARGUMENT_MESSAGE = "For a given month draw two horizontal bar charts on the console for the highest "\
                                   "and lowest temperature on each day. Highest in red and lowest in blue."
