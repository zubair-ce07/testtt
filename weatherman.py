import csv
import glob
import calendar
import argparse

from datetime import datetime
from colorama import Fore, Style


FILE_NAME_T = "Murree_weather_{}.txt"


class Validator:
    @staticmethod
    def is_valid_date(date):
        try:
            date = datetime.strptime(date, "%Y/%m")
            date = date.strftime("%Y_%b")
            return date
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(date)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def is_valid_year(year):
        try:
            datetime.strptime(year, "%Y")
            return year
        except ValueError:
            msg = "Not a valid year: '{0}'.".format(year)
            raise argparse.ArgumentTypeError(msg)


class ReportPrinter:
    @staticmethod
    def print_month_report(max_temp, min_temp, mean_humidity):
        highest_avg = "Highest Average: {}C".format(max_temp)
        lowest_avg = "Lowest Average: {}C".format(min_temp)
        avg_humidity = "Average Mean Humidity: {}%".format(mean_humidity)
        print(highest_avg,lowest_avg, avg_humidity, sep="\n")

    @staticmethod
    def print_year_report(max_temp, min_temp, max_humidity):
        max_temp = "Highest: {}C on {}".format(max_temp["max_temp"], max_temp["date"].strftime("%B %d"))
        min_temp = "Lowest: {}C on {}".format(min_temp["min_temp"], min_temp["date"].strftime("%B %d"))
        max_humidity = "Humidity: {}% on {}".format(max_humidity["max_humidity"], max_humidity["date"].strftime("%B %d"))
        print(max_temp, min_temp, max_humidity, sep="\n")

    @staticmethod
    def print_single_bar_chart_report(daily_data):
        print(daily_data["date"].strftime("%d")
              + Fore.RED
              + " "
              + "+" * daily_data["min_temp"]
              + Fore.BLUE
              + "+" * (daily_data["max_temp"] - daily_data["min_temp"])
              + Style.RESET_ALL
              + str(daily_data["min_temp"])
              + " - "
              + str(daily_data["max_temp"]))

    @staticmethod
    def print_double_bar_chart_report(daily_data):
        print(Fore.RED + "{} {} {}C".format(daily_data["date"].strftime("%d"), "+" * daily_data["max_temp"],
                                             daily_data["max_temp"]))
        print(Fore.BLUE + "{} {} {}C".format(daily_data["date"].strftime("%d"), "+" * daily_data["min_temp"],
                                             daily_data["min_temp"]))
        print(Style.RESET_ALL)


class ReportGenerator:

    @staticmethod
    def generate_month_report(file_name, path):
        data = ReportReader.read_month_records(file_name, path)
        if not data:
            return
        length = len(data)
        avg_max_temp = round(sum(daily_data["max_temp"] for daily_data in data) / length)
        avg_min_temp = round(sum(daily_data["min_temp"] for daily_data in data) / length)
        avg_mean_humidity = round(sum(daily_data["mean_humidity"] for daily_data in data) / length)
        ReportPrinter.print_month_report(avg_max_temp, avg_min_temp, avg_mean_humidity)

    @staticmethod
    def generate_year_report(given_date, path):
        data = ReportReader.read_year_records(given_date, path)
        if not data:
            return
        max_temp = max(data, key=lambda x: x['max_temp'])
        min_temp = min(data, key=lambda x: x['min_temp'])
        max_humidity = max(data, key=lambda x: x['max_humidity'])
        ReportPrinter.print_year_report(max_temp, min_temp, max_humidity)

    @staticmethod
    def generate_single_bar_chart_report(file_name, path):
        data = ReportReader.read_month_records(file_name, path)
        if not data:
            return
        for data in data:
            ReportPrinter.print_single_bar_chart_report(data)

    @staticmethod
    def generate_double_bar_chart_report(file_name, path):
        data = ReportReader.read_month_records(file_name, path)
        if not data:
            return
        for data in data:
            ReportPrinter.print_double_bar_chart_report(data)

    @staticmethod
    def generate_reports(arguments):
        path = arguments.path
        if arguments.a:
            file_name = FILE_NAME_T.format(arguments.a)
            ReportGenerator.generate_month_report(file_name, path)
        if arguments.b:
            file_name = FILE_NAME_T.format(arguments.b)
            ReportGenerator.generate_single_bar_chart_report(file_name, path)
        if arguments.c:
            file_name = FILE_NAME_T.format(arguments.c)
            ReportGenerator.generate_double_bar_chart_report(file_name, path)
        if arguments.e:
            ReportGenerator.generate_year_report(arguments.e, path)


class ReportReader:

    @staticmethod
    def get_files(path):
        return [f for f in glob.glob(path + "**/*.txt", recursive=True)]

    @staticmethod
    def read_daily_records(daily_record):
        if daily_record["Max TemperatureC"] and daily_record["Min TemperatureC"] and daily_record["Max Humidity"] and \
                daily_record[" Mean Humidity"]:
            data = {
                "date": datetime.strptime(daily_record["PKT"], "%Y-%m-%d"),
                "max_temp": int(daily_record["Max TemperatureC"]),
                "min_temp": int(daily_record["Min TemperatureC"]),
                "max_humidity": int(daily_record["Max Humidity"]),
                "mean_humidity": int(daily_record[" Mean Humidity"])
            }
            return data

    @staticmethod
    def read_month_records(file_name, path):
        data = []
        file_name = "{}{}".format(path,  file_name)
        if file_name in ReportReader.get_files(path):
            with open(file_name) as weather_file:
                reader = csv.DictReader(weather_file)
                for row in reader:
                    daily_data = ReportReader.read_daily_records(row)
                    if daily_data:
                        data.append(daily_data)
            return data

    @staticmethod
    def read_year_records(year, path):
        data = []
        for i in range(1, 13):
            date = "{}_{}".format(year, calendar.month_abbr[i])
            file_name = FILE_NAME_T.format(date)
            data = ReportReader.read_month_records(file_name, path)
            if data:
                data.extend(data)
        return data


def get_arguments_list():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("-a", type=Validator.is_valid_date)
    parser.add_argument("-b", type=Validator.is_valid_date)
    parser.add_argument("-c", type=Validator.is_valid_date)
    parser.add_argument("-e", type=Validator.is_valid_year)
    args = parser.parse_args()
    if not (args.a or args.b or args.c or args.e):
        parser.error('No arguments provided.')
    return args


def main():
    arguments = get_arguments_list()
    report_generator = ReportGenerator()
    report_generator.generate_reports(arguments)


if __name__ == "__main__":
    main()

