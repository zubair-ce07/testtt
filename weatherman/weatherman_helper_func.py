import csv
import os
from operator import attrgetter

from termcolor import colored

from weatherman_data_struct import *


class FileReader:
    """
    File reading Static class
    """
    @staticmethod
    def read_file(path_to_folder, query_date):
        """
        Reads File data only from query date file
        :param path_to_folder:
        :param query_date:
        :return: list of records
        """
        temp = query_date.split("/")
        query_year = temp[0]
        if len(temp) == 2:
            query_month = calendar.month_abbr[int(temp[1])]
        else:
            query_month = None
        complete_data = []
        for filename in os.listdir(path_to_folder):
            if filename.endswith(".txt"):
                if query_year in filename and (not query_month or query_month in filename):
                    with open(path_to_folder+filename) as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            complete_data.append(Record(row))
        return complete_data


class CalculateResults:
    """
    Static class to process data
    """
    @staticmethod
    def year_result(data):
        """
        Process the data set to find the highest and lowest temperature and highest humidity along with the date
        :param data: data set to process through
        :return: Result data struct populated with the results
        """
        result_data = dict()
        result_data["highest"] = max([row for row in data if row.max_temperature], key=attrgetter("max_temperature"))
        result_data["lowest"] = min([row for row in data if row.min_temperature], key=attrgetter("min_temperature"))
        result_data["humidity"] = max([row for row in data if row.max_humidity], key=attrgetter("max_humidity"))
        return result_data

    @staticmethod
    def month_result(data):
        """
        Process the data set to find the avearge of highest temperature,lowest temperature and mean humidity
        :param data: data set to search through
        :return: Result data struct populated with the results
        """
        max_temperature_total = [row.max_temperature for row in data if row.max_temperature]
        min_temperature_total = [row.min_temperature for row in data if row.min_temperature]
        average_humidity_total = [row.mean_humidity for row in data if row.mean_humidity]
        result_data = {}
        if max_temperature_total:
            result_data["highest_average"] = sum(max_temperature_total)/float(len(max_temperature_total))
        if min_temperature_total:
            result_data["lowest_average"] = sum(min_temperature_total)/float(len(min_temperature_total))
        if average_humidity_total:
            result_data["humidity_average"] = sum(average_humidity_total)/float(len(average_humidity_total))
        return result_data


class PrintReports:
    @staticmethod
    def weather_graph(data):
        print("{} {}".format(calendar.month_name[data[0].date.month], data[0].date.year))
        for record in data:
            temp_str = "{:02d} ".format(record.date.day)
            if not record.min_temperature:
                temp_str += colored("! ", "green")
            else:
                temp_str += colored("+" * record.min_temperature, "blue")
            if not record.max_temperature:
                temp_str += colored("! ", "green")
            else:
                temp_str += colored("+" * record.max_temperature, "red")
            temp_str += " {}C - {}C".format(record.min_temperature, record.max_temperature)
            print(temp_str)
        print(" ")

    @staticmethod
    def month_averages(data):
        print("Highest Average: {}C".format("{:.1f}".format(data["highest_average"])))
        print("Lowest Average: {}C".format("{:.1f}".format(data["lowest_average"])))
        print("Average Mean Humidity: {}%".format("{:.1f}".format(data["humidity_average"])))
        print(" ")

    @staticmethod
    def year_stats(data):
        print("Highest {}C on {} {}".format(data["highest"].max_temperature,
                                            calendar.month_name[data["highest"].date.month],
                                            data["highest"].date.day))
        print("Lowest {}C on {} {}".format(data["lowest"].min_temperature,
                                           calendar.month_name[data["lowest"].date.month],
                                           data["lowest"].date.day))
        print("Humidity {}% on {} {}".format(data["humidity"].max_humidity,
                                             calendar.month_name[data["humidity"].date.month],
                                             data["humidity"].date.day))
        print(" ")
