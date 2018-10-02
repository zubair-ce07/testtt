"""This file contains the YearReport class
to calculate the Year stats"""
from math import inf
import calendar


class YearReport:
    """This is the class to calculate the YEAR Stats
    given as CLA and print it"""

    def __init__(self):
        self.max_temp_date = ""
        self.max_temp = -inf
        self.min_temp_date = ""
        self.min_temp = +inf
        self.max_humidity_date = ""
        self.max_humidity = -inf

    def set_accurate_date(self, waether_data_dict):
        """This method calculates the yearly stats
        and set to appropriate variable"""

        if waether_data_dict["Max TemperatureC"]:
            if self.max_temp <= int(waether_data_dict["Max TemperatureC"]):
                self.max_temp_date = waether_data_dict["PKT"]
                self.max_temp = int(waether_data_dict["Max TemperatureC"])
        if waether_data_dict["Min TemperatureC"]:
            if self.min_temp >= int(waether_data_dict["Min TemperatureC"]):
                self.min_temp_date = waether_data_dict["PKT"]
                self.min_temp = int(waether_data_dict["Min TemperatureC"])
        if waether_data_dict["Max Humidity"]:
            if self.max_humidity <= int(waether_data_dict["Max Humidity"]):
                self.max_humidity_date = waether_data_dict["PKT"]
                self.max_humidity = int(waether_data_dict["Max Humidity"])

    def print_year_report(self):
        """This method print the YEAR Report
        as required"""

        print(
            "Highest: " + str(self.max_temp) + "C " +
            "on " + str(self.date_format(self.max_temp_date))
            )
        print(
            "Lowest: " + str(self.min_temp) + "C " +
            "on " + str(self.date_format(self.min_temp_date))
            )
        print(
            "Humidity: " + str(self.max_humidity) + "% " +
            "on " + str(self.date_format(self.max_humidity_date))
            )

    def date_format(self, date):
        """This method return the date format
        as required"""

        split_date = date.split("-")
        return calendar.month_name[int(split_date[1])] + " " + split_date[2]
