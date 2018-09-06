""" contain functions to display graph and report """
from datetime import datetime
from statistics import mean
import constants as const
import os
import re
import csv
import argparse


class FileHandler:
    """module for all file handling"""
    def __init__(self, path):
        """constructor"""
        self.path_to_files = path

    def get_file_names(self, year, month):
        """ return files from dir according to month and year"""
        files = os.listdir(self.path_to_files)
        if not month:
            regex = re.compile(r'^Murree_weather_' + year)
        else:
            month_str = get_month_string(month)
            regex = re.compile(r'^Murree_weather_' +
                               year + "_" + month_str.capitalize())
        selected_files = list(filter(regex.search, files))
        return selected_files

    def get_list(self, year, month):
        """return list of data from files in filenames_list"""
        data_list = []
        filenames_list = self.get_file_names(year, month)
        for file_name in filenames_list:
            file_name = f"{self.path_to_files}/{file_name}"
            with open(file_name, mode='r') as reader:
                csv_reader = csv.DictReader(reader, delimiter=',')
                for row in csv_reader:
                    data_list.append(row)
        return data_list


class ReportGenerator:
    """ module to display reports or graph"""
    def display_extremes(self, record_list):
        """
        function to generate extreme report
        :param record_list: list of data
        :return:
        """
        result = calculate_extremes(record_list)
        if result:
            print(f"Highest: {result.get('max_temperature')}C on "
                  f"{result.get('max_temperature_date')}")
            print(f"Lowest: {result.get('min_temperature')}C on "
                  f"{result.get('min_temperature_date')}")
            print(f"Humidity: {result.get('humidity')}% on "
                  f"{result.get('humidity_date')}")
        else:
            print("\n<< Data is not available")

    def display_averages(self, record_list):
        """
        function to generate average report
        :param record_list: list of data
        :return:
        """
        result = calculate_average(record_list)
        if result:
            print(f"\nHighest Average: {result.get('max_temperature_avg')}C")
            print(f"Lowest Average: {result.get('min_temperature_avg')}C")
            print(f"Average Mean Humidity: {result.get('mean_humidity_avg')}%")
        else:
            print("\n<< Data is not available")

    def display_graph(self, year, month, file_handler, oneline):
        """
        function to display grpah of month data
        :param oneline: flag to display one-line or two-line graph
        :return:
        """
        month_str = datetime.strptime(month, "%m").strftime('%B')
        print(f"\n{year} {month_str}:")
        month_list = file_handler.get_list(year, month)
        for day in month_list:
            date = datetime.strptime(day.get("PKT"), '%Y-%m-%d').strftime('%d')
            max_temperature = day.get("Max TemperatureC")
            min_temperature = day.get("Min TemperatureC")
            if oneline:
                print(date, end=" ")
                if max_temperature and min_temperature:
                    display_bar(min_temperature, "*", const.CBLUE)
                    display_bar(max_temperature, "*", const.CRED)
                    print(f" {min_temperature}C - {max_temperature}C")
                else:
                    print("-")
            else:
                print(date, end=" ")
                if max_temperature:
                    display_bar(max_temperature, "+", const.CRED)
                    print(" " + const.CRED + str(
                        max_temperature) + "C" + const.CEND)
                print(date, end=" ")
                if min_temperature:
                    display_bar(min_temperature, "+", const.CBLUE)
                    print(" " + const.CBLUE + str(
                        min_temperature) + "C" + const.CEND)


class Controller:
    """ main controller class that manage all flow """
    def __init__(self):
        """ constructor for the initialization of parser """
        detail_str = "Weatherman: to generate different reports"
        parser = argparse.ArgumentParser(
            description=detail_str
        )
        parser.add_argument("path",
                            help="path to the dir that conatain weatherfiles.")
        parser.add_argument("-e",
                            help=(
                                "display year report the max temperature, min "
                                "temperature and most humid day and humidity"))
        parser.add_argument("-a", type=validate_date,
                            help="display month average report the average "
                                 "max temperature, average min temperature and"
                                 " average mean humidity.")
        parser.add_argument("-c", type=validate_date,
                            help=("display month two line graph of highest " +
                                  "and lowest temperature of each day."))
        parser.add_argument("-d", type=validate_date,
                            help=("display month oneline graph of highest " +
                                  "and lowest temperature of each day."))
        self.parser = parser

    def parse_arguments(self):
        """take actions on the bases of arguments"""
        args = self.parser.parse_args()

        file_handler = FileHandler(args.path)
        generator = ReportGenerator()

        if args.e:
            list = file_handler.get_list(args.e, None)
            generator.display_extremes(list)
        if args.d:
            [year, month] = args.d.split('/')
            generator.display_graph(year, month, file_handler, True)
        if args.a:
            [year, month] = args.a.split('/')
            list = file_handler.get_list(year, month)
            generator.display_averages(list)
        if args.c:
            [year, month] = args.c.split('/')
            generator.display_graph(year, month, file_handler, False)


def calculate_extremes(rec_list):
    """
    :param rec_list: data for calculation
    :return:
    """
    if len(rec_list) > 0:
        max_temp_entry = get_required_entry(
            rec_list, const.MAX_TEMPERATURE_KEY, const.MAX_INDEX
        )
        min_temp_entry = get_required_entry(
            rec_list, const.MIN_TEMPERATURE_KEY, const.MIN_INDEX
        )
        humidity_entry = get_required_entry(
            rec_list, const.MAX_HUMIDITY_KEY, const.MAX_INDEX
        )

        result = {
            "max_temperature": max_temp_entry.get("Max TemperatureC"),
            "min_temperature": min_temp_entry.get("Min TemperatureC"),
            "humidity": humidity_entry.get("Max Humidity"),
            "max_temperature_date": date_to_display_string(max_temp_entry),
            "min_temperature_date": date_to_display_string(min_temp_entry),
            "humidity_date": date_to_display_string(humidity_entry)
        }
        return result


def calculate_average(rec_list):
    """
    :param rec_list: data for calculations
    :return:
    """
    if len(rec_list) > 0:
        max_temp_data = [int(y.get("Max TemperatureC")) for y in rec_list
                         if y.get("Max TemperatureC") is not None]
        max_temp_avg = mean(max_temp_data)

        min_temp_data = [int(y.get("Min TemperatureC")) for y in rec_list
                         if y.get("Min TemperatureC") is not None]
        min_temp_avg = mean(min_temp_data)

        humidity_data = [int(y.get(" Mean Humidity")) for y in rec_list
                         if y.get(" Mean Humidity") is not None]

        result = {
            "max_temperature_avg": str(round(max_temp_avg, 2)),
            "min_temperature_avg": str(round(min_temp_avg, 2)),
            "mean_humidity_avg": round(mean(humidity_data), 2),
        }
        return result


def get_required_entry(record_list, key, index):
    """
    return max tempertaure entry, min temperature entry or max humidity entry
    :param record_list: data for calculation
    :param key: choice for finding
    :param index: used to idetify either max or min entry is required
    :return:
    """
    sorted_list = sorted(([y for y in record_list
                           if y and y.get(key) is not None]),
                         key=lambda x: int(x.get(key)))
    return sorted_list[index]


def display_bar(range_str, sign, code):
    """helping function for graph """
    for _ in range(int(range_str)):
        print(code + sign + const.CEND, end="")


def date_to_display_string(entry):
    """convert date to string"""
    date = datetime.strptime(entry.get("PKT"), '%Y-%m-%d')
    return (date).strftime('%B %d')


def get_month_string(month):
    """return month string from month integer"""
    return datetime.strptime(month, '%m').strftime('%b')


def validate_date(date):
    """ function to validate year/month string """
    try:
        if date != datetime.strptime(date, "%Y/%m").strftime('%Y/%m'):
            raise ValueError
        return date
    except ValueError:
        print("\nInvalid option [Required year/month ie 2011/05]\n")
        return False


if __name__ == '__main__':
    controller = Controller()
    controller.parse_arguments()
