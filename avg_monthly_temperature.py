import os
import re

from constants import Constants
from utils import Utils


class AvgMonthlyTemperature:
    def __init__(self):
        self.monthly_report = {
            Constants.HIGHEST: None,
            Constants.LOWEST: None,
            Constants.HUMIDITY: None}

    def show_monthly_report(self, year, month, path):
        matched = False
        for filename in os.listdir(path):
            match_obj = re.match(r"Murree_weather_" + year + "_" + month,
                                 filename,
                                 re.I)
            if match_obj:
                matched = True
                try:
                    with open(path + os.sep + filename, "r", 1) as file:
                        heading_list = file.readline().split(",")
                        heading_list = [item.strip() for item in heading_list]
                        index_max_temp = heading_list.index(
                            Constants.MAX_TEMPERATURE)
                        index_min_temp = heading_list.index(
                            Constants.MIN_TEMPERATURE)
                        index_mean_humidity = heading_list.index(
                            Constants.MEAN_HUMIDITY)
                        average_max_temp = []
                        average_min_temp = []
                        average_mean_humidity = []
                        for line in file:
                            raw_data = line.split(",")
                            max_temp = raw_data[index_max_temp]
                            if Utils.is_int(max_temp):
                                average_max_temp.append(int(max_temp))

                            min_temp = raw_data[index_min_temp]
                            if Utils.is_int(min_temp):
                                average_min_temp.append(int(min_temp))

                            mean_humidity = raw_data[index_mean_humidity]
                            if Utils.is_int(mean_humidity):
                                average_mean_humidity.append(
                                    int(mean_humidity))

                        self._get_average_report(average_max_temp,
                                                 average_min_temp,
                                                 average_mean_humidity)

                except IOError as excp:
                    print(excp)

                break
        return self.monthly_report if matched else None

    def _get_average_report(self, average_max_temp, average_min_temp,
                            average_mean_humidity):
        sum_max_temp = sum(average_max_temp)
        self.monthly_report[Constants.HIGHEST] = sum_max_temp // len(
            average_max_temp) if sum_max_temp > 0 else 0

        sum_min_temp = sum(average_min_temp)
        self.monthly_report[Constants.LOWEST] = sum_min_temp // len(
            average_min_temp) if sum_min_temp > 0 else 0

        sum_mean_humidity = sum(average_mean_humidity)
        self.monthly_report[Constants.MEAN_HUMIDITY] = sum_mean_humidity // len(
            average_mean_humidity) if sum_mean_humidity > 0 else 0
