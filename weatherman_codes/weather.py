"""
Class and methods for weatherman task
Pylint Score: 10.00
The only issue is: Too few public methods (1/2)
"""

import calendar


class Weather:          # pylint: disable=too-few-public-methods
    """Weather data class"""

    def __init__(self, data):
        """Constructor method"""
        self.year = data[0]
        self.month = data[1]
        self.day = data[2]
        self.max_temp = data[3]
        self.min_temp = data[4]
        self.max_humid = data[5]
        self.mean_humid = data[6]

    @classmethod
    def get_weather(cls, row):
        """Read a row's data and returns attributes"""
        year, month, day = cls.__set_date(row['PKT'])
        max_temp = int(row['Max TemperatureC'])
        min_temp = int(row['Min TemperatureC'])
        mean_humid = int(row['Mean Humidity'])
        max_humid = int(row['Max Humidity'])
        return cls([year, month, day, max_temp, min_temp, max_humid, mean_humid])

    @staticmethod
    def __set_date(date):
        """Extract year, month and day from date"""
        year, month_no, day = date.split('-')
        month = calendar.month_name[int(month_no)]
        if int(day) < 10:
            day = '0{}'.format(day)
        return year, month, day
