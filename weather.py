"""This module store a day weather."""
from datetime import datetime


class Weather:
    """Store and manupulate weather data"""

    def __init__(self, entries):
        self.max_temperaturec = None
        self.min_temperaturec = None
        self.max_humidity = None
        self.mean_temperaturec = None
        self.mean_humidity = None
        self.pkt = None
        self.pkst = None
        if entries:
            self.__dict__.update(entries)
            year, month, day = self.pkt.split("-") if self.pkt != None else self.pkst.split("-")
            self.__date = datetime(int(year), int(month), int(day))

    def get_month_day(self):
        """return date of format Month day i.e Jun 12"""
        return self.__date.strftime('%B %d')

    def get_month_year(self):
        """return date of format month year i.e Jun 2011"""
        return self.__date.strftime('%B %Y')

    def get_day(self):
        """return date of format day i.e 12"""
        return self.__date.strftime('%d')

    @staticmethod
    def get_by_max_temp(first, second):
        """Return Weather with Max Temperature"""
        return Weather.get_max(first, second, "max_temperaturec")

    @staticmethod
    def get_by_low_temp(first, second):
        """Return Weather with Min Temperature"""
        return Weather.get_low(first, second, "min_temperaturec")

    @staticmethod
    def get_by_max_humidity(first, second):
        """Return Weather with Max Humidity"""
        return Weather.get_max(first, second, "max_humidity")

    @staticmethod
    def get_by_average_max_temp(first, second):
        """Return Weather with Average Max Temperature"""
        return Weather.get_max(first, second, "mean_temperaturec")

    @staticmethod
    def get_by_average_low_temp(first, second):
        """Return Weather with Average Low Temperature"""
        return Weather.get_low(first, second, "mean_temperaturec")

    @staticmethod
    def get_by_average_max_humidity(first, second):
        """Return Weather with Average Max Humidity"""
        return Weather.get_max(first, second, "mean_humidity")

    @staticmethod
    def get_max(first, second, attr):
        """Return Weather with Max attribute given as arguments"""
        if not first or (first and getattr(second, attr) and int(getattr(second, attr)) > int(getattr(first, attr))):
            return second
        return first

    @staticmethod
    def get_low(first, second, attr):
        """Return Weather with Min attribute given as arguments"""
        if not first or (first and getattr(second, attr) and int(getattr(second, attr)) < int(getattr(first, attr))):
            return second
        return first
