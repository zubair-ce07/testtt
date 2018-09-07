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
        month = date_dict.get("month")
        if month:
            month_str = get_month(date_dict.get("month"))
            regex = re.compile(r'^Murree_weather_' +
                               date_dict.get(
                                   "year") + "_" + month_str.capitalize())
        else:
            regex = re.compile(r'^Murree_weather_' + date_dict.get("year"))
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
                        read_date(row),
                        row.get("Max TemperatureC"),
                        row.get("Min TemperatureC"),
                        row.get("Max Humidity"),
                        row.get(" Mean Humidity")
                    )
                    data_list.append(record)
        if len(data_list) > 0:
            return data_list
        else:
            print("\n<< Data is not available")
            return None


class ReportGenerator:
    """ module to display reports or graph"""
    def display_extremes(self, record_list):
        """
        function to generate extreme report
        :param record_list: list of data
        :return:
        """
        result = calculate_extremes(record_list)

        print(f"Highest: {result.get('max_temperature')}C on "
              f"{result.get('max_temperature_date')}")
        print(f"Lowest: {result.get('min_temperature')}C on "
              f"{result.get('min_temperature_date')}")
        print(f"Humidity: {result.get('humidity')}% on "
              f"{result.get('humidity_date')}")

    def display_averages(self, record_list):
        """
        function to generate average report
        :param record_list: list of data
        :return:
        """
        result = calculate_average(record_list)

        print(f"\nHighest Average: {result.get('max_temperature_avg')}C")
        print(f"Lowest Average: {result.get('min_temperature_avg')}C")
        print(f"Average Mean Humidity: {result.get('mean_humidity_avg')}%")


    def display_graph(self, month_list, date, horizontal):
        """
        function to display grpah of month data
        :param horizontal: flag to display one-line or two-line graph
        :return:
        """
        date_dict = parse_date(date)
        month_str = datetime.strptime(date_dict.get("month"),
                                      "%m").strftime('%B')
        print(f"\n{date_dict.get('year')} {month_str}:")

        for day in month_list:
            date = datetime.strptime(day.date, '%Y-%m-%d').strftime('%d')
            max_temperature = day.max_temperature
            min_temperature = day.min_temperature
            print(date, end=" ")
            display_graph_line(
                horizontal, max_temperature,
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
        file_handler = FileHandler()

        if args.e:
            record_list = file_handler.get_list(args.path, args.e)
            if record_list: generator.display_extremes(record_list)
        if args.d:
            month_list = file_handler.get_list(args.path, args.d)
            if month_list: generator.display_graph(month_list, args.d, True)
        if args.a:
            record_list = file_handler.get_list(args.path, args.a)
            if record_list: generator.display_averages(record_list)
        if args.c:
            month_list = file_handler.get_list(args.path, args.c)
            if month_list: generator.display_graph(month_list, args.c, False)


def parse_date(date):
    month_year = date.split('/')
    date_dict = {"year": month_year[0]}
    date_dict["month"] = month_year[1] if len(month_year) == 2 else None
    return date_dict


def calculate_extremes(rec_list):
    """
    :param rec_list: data for calculation
    :return:
    """
    max_temp_entry = WheatherReadings(None,0,0,0,0)
    min_temp_entry =  WheatherReadings(None,0,0,0,0)
    max_humidity_entry =  WheatherReadings(None,0,0,0,0)

    for record in rec_list:
        if (record.max_temperature and
                (int(record.max_temperature)  >
                 int(max_temp_entry.max_temperature))):
            max_temp_entry = record
        if (record.min_temperature and
                (int(record.min_temperature) <
                 int(min_temp_entry.min_temperature))):
            min_temp_entry = record
        if (record.max_humidity and
                (int(record.max_humidity) >
                 int(max_humidity_entry.max_humidity))):
            max_humidity_entry= record

    result = {
        "max_temperature": max_temp_entry.max_temperature,
        "min_temperature": min_temp_entry.min_temperature,
        "humidity": max_humidity_entry.max_humidity,
        "max_temperature_date": change_date_formt(max_temp_entry.date),
        "min_temperature_date": change_date_formt(min_temp_entry.date),
        "humidity_date": change_date_formt(max_humidity_entry.date)
    }
    return result


def calculate_average(rec_list):
    """
    :param rec_list: data for calculations
    :return:
    """

    max_temp_mean_data = {"count": 0, "sum": 0}
    min_temp_mean_data = {"count": 0, "sum": 0}
    humidity_mean_data = {"count": 0, "sum": 0}

    for record in rec_list:
        if record.max_temperature:
            max_temp_mean_data["count"] = max_temp_mean_data.get("count") + 1
            max_temp_mean_data["sum"] += int(record.max_temperature)
        if record.min_temperature:
            min_temp_mean_data["count"] = min_temp_mean_data.get("count") + 1
            min_temp_mean_data["sum"] += int(record.min_temperature)
        if record.mean_humity:
            humidity_mean_data["count"] = humidity_mean_data.get("count") + 1
            humidity_mean_data["sum"] += int(record.mean_humity)

    max_temp_avg =  get_avg(max_temp_mean_data)
    min_temp_avg = get_avg(min_temp_mean_data)
    humidity_avg = get_avg(humidity_mean_data)

    result = {
        "max_temperature_avg": (str(round(max_temp_avg, 2))),
        "min_temperature_avg": str(round(min_temp_avg, 2)),
        "mean_humidity_avg": round(humidity_avg, 2),
    }
    return result


def display_graph_line(horizontal, max_temperature, min_temperature, date):
    if horizontal:
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

def read_date(row):
    return row.get("PKT") if row.get("PKT")  else row.get("PKRT")

def display_bar(range_str, sign, code):
    """helping function for graph """
    for _ in range(int(range_str)):
        print(code + sign + const.CEND, end="")


def change_date_formt(entry):
    """change date string format"""
    date = datetime.strptime(entry, '%Y-%m-%d')
    return (date).strftime('%B %d')


def get_month(month):
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


def get_avg(data):
    return float(data.get("sum")) / data.get("count")

if __name__ == '__main__':
    controller = Controller()
    controller.parse_arguments()
