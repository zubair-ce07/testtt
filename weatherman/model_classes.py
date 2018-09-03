"""
this module contain all classes
"""


class DayRecord(object):
    """ class to store full day record """
    def __init__(self, date, max_temperature, mean_temperature,
                 min_temperature, max_humidity, mean_humidity, min_humidity):
        self.max_temperature = max_temperature
        self.mean_temperature = mean_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.date = date


class MonthReport(object):
    """ contain month report """
    def __init__(self, max_temp_avg, min_temp_avg,
                 mean_humidity_avg, month_year):
        self.max_temp_avg = max_temp_avg
        self.min_temp_avg = min_temp_avg
        self.mean_humidity_avg = mean_humidity_avg
        self.month_year = month_year

    def to_string(self):
        """ return all members in a string """
        highest_msg = f"Highest Average: {str(round(self.max_temp_avg, 2))}C"
        lowest_msg = f"Lowest Average: {str(round(self.min_temp_avg, 2))}C"
        avg_humidity_msg = ("Average Mean Humidity: " +
                            f"{str(round(self.mean_humidity_avg, 2))}%")
        ret_str = (
                    highest_msg + "\n" +
                    lowest_msg + "\n" +
                    avg_humidity_msg
                  )
        return ret_str

    def display(self):
        """ display month_report average in correct syntax """
        print("-----MONTH REPORT_" + self.month_year + "-----")
        print(self.to_string())


class YearReport(object):
    """ contain module 1 ie year Report data """
    def __init__(self, max_temp, max_temp_date,
                 min_temp, min_temp_date,
                 humidity, humidity_date):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.humidity = humidity
        self.max_temp_date = max_temp_date
        self.min_temp_date = min_temp_date
        self.humidity_date = humidity_date

    def to_string(self):
        """ return all members in a string """

        highest_temp_date = (self.max_temp_date).strftime('%B %d')
        lowest_temp_date = (self.min_temp_date).strftime('%B %d')
        humidity_date = (self.humidity_date).strftime('%B %d')

        highest_msg = f"Highest: {str(self.max_temp)}C on {highest_temp_date}"
        lowest_msg = f"Lowest: {str(self.min_temp)}C on {lowest_temp_date}"
        humidity_msg = f"Humidity: {str(self.humidity)}% on {humidity_date}"

        ret_str = (
                      highest_msg + "\n" +
                      lowest_msg + "\n" +
                      humidity_msg
                  )
        return ret_str

    def display(self):
        """ print year report in correct syntax """
        year_str = str(self.max_temp_date.strftime('%Y'))
        print("-----YEAR REPORT_" + year_str + "-----")
        print(self.to_string())
