import os
import re

from constants import Constants
from utils import Utils

"""For a given year display the highest temperature and day, lowest temperature
and day, most humid day and humidity."""


class TemperatureObserver:
    def __init__(self):
        self.annual_report = {
            Constants.HIGHEST: {Constants.VALUE: None, Constants.DATE: None},
            Constants.LOWEST: {Constants.VALUE: None, Constants.DATE: None},
            Constants.HUMIDITY: {Constants.VALUE: None, Constants.DATE: None}}

    def show_annual_report(self, year, directory):
        matched = False
        for filename in os.listdir(directory):
            match_obj = re.match(r"Murree_weather_" + year + ".*", filename,
                                 re.I)
            if match_obj:
                matched = True
                try:
                    with open(directory + os.sep + filename, "r",
                              1) as file:
                        heading_list = file.readline().split(",")
                        index_date = heading_list.index(Constants.PKT)
                        index_max_temp = heading_list.index(
                            Constants.MAX_TEMPERATURE)
                        index_min_temp = heading_list.index(
                            Constants.MIN_TEMPERATURE)
                        index_max_humidity = heading_list.index(
                            Constants.MAX_HUMIDITY)
                        for line in file:
                            raw_data = line.split(",")

                            self._get_max_temperature(
                                raw_data[index_max_temp],
                                raw_data[index_date])
                            self._get_min_temperature(
                                raw_data[index_min_temp],
                                raw_data[index_date])
                            self._get_max_humidity(
                                raw_data[index_max_humidity],
                                raw_data[index_date])

                except IOError as excp:
                    print(excp)
        return self.annual_report if matched else None

    def _get_max_temperature(self, value, date):
        if value.isdigit():
            previous_max_tem = self.annual_report.get(
                Constants.HIGHEST).get(Constants.VALUE)
            if (previous_max_tem is None or int(value) > int(
                    previous_max_tem)):
                self.annual_report.get(Constants.HIGHEST)[
                    Constants.VALUE] = value
                self.annual_report.get(Constants.HIGHEST)[
                    Constants.DATE] = date

    def _get_min_temperature(self, value, date):
        if Utils.is_int(value):
            previous_min_temp = self.annual_report.get(
                Constants.LOWEST).get(Constants.VALUE)
            if (previous_min_temp is None or int(value) < int(
                    previous_min_temp)):
                self.annual_report.get(Constants.LOWEST)[
                    Constants.VALUE] = value
                self.annual_report.get(Constants.LOWEST)[Constants.DATE] = date

    def _get_max_humidity(self, value, date):
        if Utils.is_int(value):
            previous_max_humidity = self.annual_report.get(
                Constants.HIGHEST).get(Constants.VALUE)
            if (previous_max_humidity is None or int(value) > int(
                    previous_max_humidity)):
                self.annual_report.get(Constants.HUMIDITY)[
                    Constants.VALUE] = value
                self.annual_report.get(Constants.HUMIDITY)[
                    Constants.DATE] = date
