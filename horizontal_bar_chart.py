import datetime
import os
import re

from constants import Constants
from utils import Utils


class HorizontalBarChart:
    def show_min_max_multi_bar_chart(self, year, month, path):
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
                        index_date = heading_list.index(
                            Constants.PKT)

                        for line in file:
                            raw_data = line.split(",")
                            self._print_multi_bar_chart(
                                index_date,
                                index_max_temp,
                                index_min_temp, raw_data)
                    break
                except IOError as excp:
                    print(excp)

        if not matched:
            print("No file found with such name!!")

    def show_min_max_single_bar_chart(self, year, month, path):
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
                        index_date = heading_list.index(
                            Constants.PKT)

                        for line in file:
                            raw_data = line.split(",")
                            HorizontalBarChart._print_single_bar_chart(
                                index_date,
                                index_max_temp,
                                index_min_temp,
                                raw_data)
                    break
                except IOError as excp:
                    print(excp)

        if not matched:
            print("No file found with such name!!")

    @staticmethod
    def _print_multi_bar_chart(index_date, index_max_temp, index_min_temp,
                               raw_data):
        max_temp = raw_data[index_max_temp]
        day = datetime.datetime.strptime(
            raw_data[index_date], "%Y-%m-%d").strftime("%d")
        day = "\033[1;33m" + day + "\033[1;m"
        if Utils.is_int(max_temp):
            max_temp = int(max_temp)
            bars = "\033[1;31m" + "+" * max_temp + "\033[1;m"
            value = "\033[1;33m%sC\033[1;m" % max_temp
            print(day, bars, value)
        min_temp = raw_data[index_min_temp]
        if Utils.is_int(min_temp):
            min_temp = int(min_temp)
            bars = "\033[1;36m" + "+" * min_temp + \
                   "\033[1;m" if min_temp > 0 else ""
            value = "\033[1;33m%sC\033[1;m" % min_temp
            print(day, bars, value)

    @staticmethod
    def _print_single_bar_chart(
            index_date,
            index_max_temp,
            index_min_temp,
            raw_data):
        max_temp = raw_data[index_max_temp]
        day = datetime.datetime.strptime(
            raw_data[index_date], "%Y-%m-%d").strftime("%d")
        day = "\033[1;33m" + day + "\033[1;m"
        if Utils.is_int(max_temp):
            max_temp = int(max_temp)
            bars_max = "\033[1;31m" + "+" * max_temp + \
                       "\033[1;m"

            min_temp = raw_data[index_min_temp]
            min_temp = int(min_temp)
            bars_min = "\033[1;36m" + "+" * min_temp + \
                       "\033[1;m" if min_temp > 0 else ""
            value = "\033[1;33m%dC - %dC\033[1;m" % (
                min_temp, max_temp)
            print(day, bars_min + bars_max, value)
