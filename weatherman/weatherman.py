""" contain functions to display graph and report """
from datetime import datetime
from statistics import mean
import constants as const
import os
import re
import csv
import argparse


class WheatherReadings:
    def __init__(
            self, date, max_temperature, min_temperature,
            max_humidity, mean_humidty
    ):
        self.date = date
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.mean_humity = mean_humidty


class FileHandler:
    """module for all file handling"""

    def get_file_names(self, path_to_files, date):
        """ return files from dir according to month and year"""

        date_dict = parse_date(date)
        files = os.listdir(path_to_files)
        if not date_dict.get("month"):
            regex = re.compile(r'^Murree_weather_' + date_dict.get("year"))
        else:
            month_str = get_month_string(date_dict.get("month"))
            regex = re.compile(r'^Murree_weather_' +
                               date_dict.get("year") + "_" + month_str.capitalize())
        selected_files = list(filter(regex.search, files))
        return selected_files

    def get_list(self, path_to_files, date):
        """return list of data from files in filenames_list"""
        data_list = []
        filenames_list = self.get_file_names(path_to_files, date)
        for file_name in filenames_list:
            file_name = f"{path_to_files}/{file_name}"
            with open(file_name, mode='r') as reader:
                csv_reader = csv.DictReader(reader, delimiter=',')
                for row in csv_reader:
                    record = WheatherReadings(
                        row.get("PKT"),
                        row.get("Max TemperatureC"),
                        row.get("Min TemperatureC"),
                        row.get("Max Humidity"),
                        row.get(" Mean Humidity")
                    )
                    data_list.append(record)
        return data_list


class ReportGenerator:
    """ module to display reports or graph"""
    def display_extremes(self, path, date):
        """
        function to generate extreme report
        :param record_list: list of data
        :return:
        """
        record_list = FileHandler().get_list(path, date)
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

    def display_averages(self, path, date):
        """
        function to generate average report
        :param record_list: list of data
        :return:
        """
        record_list = FileHandler().get_list(path, date)
        result = calculate_average(record_list)
        if result:
            print(f"\nHighest Average: {result.get('max_temperature_avg')}C")
            print(f"Lowest Average: {result.get('min_temperature_avg')}C")
            print(f"Average Mean Humidity: {result.get('mean_humidity_avg')}%")
        else:
            print("\n<< Data is not available")

    def display_graph(self, path, date, oneline):
        """
        function to display grpah of month data
        :param oneline: flag to display one-line or two-line graph
        :return:
        """
        file_handler = FileHandler()
        date_dict = parse_date(date)
        month_str = datetime.strptime(date_dict.get("month"),
                                      "%m").strftime('%B')
        print(f"\n{date_dict.get('year')} {month_str}:")
        month_list = file_handler.get_list(path, date)
        for day in month_list:
            date = datetime.strptime(day.date, '%Y-%m-%d').strftime('%d')
            max_temperature = day.max_temperature
            min_temperature = day.min_temperature
            print(date, end=" ")
            display_graph_line(
                oneline, max_temperature,
                min_temperature, date
            )


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

        generator = ReportGenerator()
        if args.e:
            generator.display_extremes(args.path, args.e)
        if args.d:
            generator.display_graph(args.path, args.d, True)
        if args.a:
            generator.display_averages(args.path, args.a)
        if args.c:
            generator.display_graph(args.path, args.c, False)


def parse_date(date):
    month_year = date.split('/')
    date_dict = {
        "year": month_year[0],
        "month": None
    }
    if(len(month_year) == 2):
        date_dict["month"] = month_year[1]
    return date_dict


def calculate_extremes(rec_list):
    """
    :param rec_list: data for calculation
    :return:
    """
    if len(rec_list) > 0:
        humidity_entry = get_required_entry(rec_list, 0)
        max_temp_entry = get_required_entry(rec_list, 1)
        min_temp_entry = get_required_entry(rec_list, 2)

        result = {
            "max_temperature": max_temp_entry.max_temperature,
            "min_temperature": min_temp_entry.min_temperature,
            "humidity": humidity_entry.max_humidity,
            "max_temperature_date": date_to_display_string(max_temp_entry.date),
            "min_temperature_date": date_to_display_string(min_temp_entry.date),
            "humidity_date": date_to_display_string(humidity_entry.date)
        }
        return result


def calculate_average(rec_list):
    """
    :param rec_list: data for calculations
    :return:
    """
    if len(rec_list) > 0:
        max_temp_data = [int(y.max_temperature) for y in rec_list
                         if y.max_temperature is not None]
        max_temp_avg = mean(max_temp_data)

        min_temp_data = [int(y.min_temperature) for y in rec_list
                         if y.min_temperature is not None]
        min_temp_avg = mean(min_temp_data)

        humidity_data = [int(y.mean_humity) for y in rec_list
                         if y.mean_humity is not None]

        result = {
            "max_temperature_avg": str(round(max_temp_avg, 2)),
            "min_temperature_avg": str(round(min_temp_avg, 2)),
            "mean_humidity_avg": round(mean(humidity_data), 2),
        }
        return result


def get_required_entry(record_list, key):
    """
    return max tempertaure entry, min temperature entry or max humidity entry
    :param record_list: data for calculation
    :param key: 0:humidity, 1:max_temperature and 2 is for min temperature
    :param index: used to idetify either max or min entry is required
    :return:
    """
    if key == 0:
        sorted_list = sorted(([y for y in record_list
                               if y and y.max_humidity is not None]),
                             key=lambda x: int(x.max_humidity))
        return sorted_list[-1]
    elif key == 1:
        sorted_list = sorted(([y for y in record_list
                               if y and y.max_temperature is not None]),
                             key=lambda x: int(x.max_temperature))
        return sorted_list[0]
    elif key == 2:
        sorted_list = sorted(([y for y in record_list
                               if y and y.min_temperature is not None]),
                             key=lambda x: int(x.min_temperature))
        return sorted_list[-1]


def display_graph_line(oneline, max_temperature, min_temperature, date):
    if oneline:
        if max_temperature and min_temperature:
            display_bar(min_temperature, "*", const.CBLUE)
            display_bar(max_temperature, "*", const.CRED)
            print(f" {min_temperature}C - {max_temperature}C")
        else:
            print("-")
    else:
        if max_temperature:
            display_bar(max_temperature, "+", const.CRED)
            print(" " + const.CRED + str(
                max_temperature) + "C" + const.CEND)
        print(date, end=" ")
        if min_temperature:
            display_bar(min_temperature, "+", const.CBLUE)
            print(" " + const.CBLUE + str(
                min_temperature) + "C" + const.CEND)


def display_bar(range_str, sign, code):
    """helping function for graph """
    for _ in range(int(range_str)):
        print(code + sign + const.CEND, end="")


def date_to_display_string(entry):

    """convert date to string"""
    date = datetime.strptime(entry, '%Y-%m-%d')
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
