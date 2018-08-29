"""
this module contain all classes
"""

class Temperature(object):
    """ class to store temperature data"""
    def __init__(self, max_temp, mean_temp, min_temp):
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n Max TemperatureC: " + str(self.max_temp)
        ret_str = ret_str + "\n Min TemperatureC: " + str(self.min_temp)
        ret_str = ret_str + "\n Mean TemperatureC: " + str(self.mean_temp)
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class Humidity(object):
    """ class to store humidity data """
    def __init__(self, max_humidity, mean_humidity, min_humidity):
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n Max Humidity: " + str(self.max_humidity)
        ret_str = ret_str + "\n Min Humidity: " + str(self.min_humidity)
        ret_str = ret_str + "\n Mean Humidity: " + str(self.mean_humidity)
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class DayRecord(object):
    """ class to store full day record """
    def __init__(self, date, temp, humidity):
        self.date = date
        self.temp = temp
        self.humidity = humidity

    def to_string(self):
        """ return all members in a string """
        ret_str = (self.temp.to_string() +
                   self.humidity.to_string())
        return ret_str

    def display(self):
        """ print all members """
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
        ret_str = (" Highest: " + str(self.max_temp) + "C on " +
                   (self.max_temp_date).strftime('%B %d') +
                   "\n Lowest: " + str(self.min_temp) + "C on " +
                   (self.min_temp_date).strftime('%B %d') +
                   "\n Humidity: " + str(self.humidity) + "% on " +
                   (self.humidity_date).strftime('%B %d'))
        return ret_str

    def display(self):
        """ print year report in correct syntax """
        year_str = str(self.max_temp_date.strftime('%Y'))
        if year_str != "1970":
            print(28 * "-", " YEAR REPORT_" + year_str + " ", 28 * "-")
            print(self.to_string())
            print((72 + len(year_str)) * "-", "\n")
        else:
            print("<< Invalid year -  Data is not available for given year\n")



class MonthAvgReport(object):
    """ contain month report """
    def __init__(self, max_temp_avg, min_temp_avg,
                 mean_humidity_avg, month_year):
        self.max_temp_avg = max_temp_avg
        self.min_temp_avg = min_temp_avg
        self.mean_humidity_avg = mean_humidity_avg
        self.month_year = month_year

    def to_string(self):
        """ return all members in a string """
        ret_str = (" Highest Average: " +
                   str(round(self.max_temp_avg, 2)) + "C" +
                   "\n Lowest Average: " +
                   str(round(self.min_temp_avg, 2)) + "C" +
                   "\n Average Mean Humidity: " +
                   str(round(self.mean_humidity_avg, 2)) + "%")
        return ret_str

    def display(self):
        """ display month_report average in correct syntax """
        print(28 * "-", " MONTH REPORT_" + self.month_year + " ", 28 * "-")
        print(self.to_string())
        print((73 + len(self.month_year)) * "-", "\n")
