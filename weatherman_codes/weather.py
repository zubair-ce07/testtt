"""
Class and methods for weatherman task
Pylint Score: 9.58
The only issue is: Too few public methods (1/2)
"""

import calendar


class Weather:
    """Weather data class"""

    def __init__(self):
        """Constructor method"""
        self.year = ''
        self.month = ''
        self.day = ''
        self.max_temp = 0
        self.min_temp = 0
        self.max_humid = 0
        self.mean_humid = 0

    def get_row(self, row):
        """Read a row's data and sets attributes"""
        self.__set_date(row['PKT'])
        self.max_temp = int(row['Max TemperatureC'])
        self.min_temp = int(row['Min TemperatureC'])
        self.mean_humid = int(row['Mean Humidity'])
        self.max_humid = int(row['Max Humidity'])

    def __set_date(self, date):
        """Method to set year, month and day by extracting from date"""
        year, month_no, day = date.split('-')
        month = calendar.month_name[int(month_no)]
        if int(day) < 10:
            day = '0{}'.format(day)
        self.year = year
        self.month = month
        self.day = day
