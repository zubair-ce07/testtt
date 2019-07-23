import argparse
import csv
import calendar
import glob
from colorama import Fore
from colorama import Style
from datetime import datetime


class Validator:
    @staticmethod
    def is_valid_date_month(given_date):
        try:
            return datetime.strptime(given_date, "%Y/%m")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(given_date)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def is_valid_date_year(given_date):
        try:
            return datetime.strptime(given_date, "%Y")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(given_date)
            raise argparse.ArgumentTypeError(msg)


class ReportPrinter:
    @staticmethod
    def print_monthly_report(max_temp, min_temp, mean_humidity):
        highest_avg = "Highest Average: {}C".format(max_temp)
        lowest_avg = "Lowest Average: {}C".format(min_temp)
        avg_humidity = "Average Mean Humidity: {}%".format(mean_humidity)
        print(highest_avg,lowest_avg, avg_humidity, sep="\n")

    @staticmethod
    def print_yearly_report(max_temp, min_temp, max_humidity):
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
    def __init__(self, arguments, path):
        self.arguments = arguments
        self.reader = Reader(path)

    def generate_monthly_report(self, file_name):
        monthly_data = self.reader.read_monthly_records(file_name)
        if not monthly_data:
            return
        length = len(monthly_data)
        avg_max_temp = round(sum(daily_data["max_temp"] for daily_data in monthly_data) / length)
        avg_min_temp = round(sum(daily_data["min_temp"] for daily_data in monthly_data) / length)
        avg_mean_humidity = round(sum(daily_data["mean_humidity"] for daily_data in monthly_data) / length)
        ReportPrinter.print_monthly_report(avg_max_temp, avg_min_temp, avg_mean_humidity)

    def generate_yearly_report(self, given_date):
        yearly_record = self.reader.read_yearly_records(given_date)
        if not yearly_record:
            return
        max_temp = max(yearly_record, key=lambda x: x['max_temp'])
        min_temp = min(yearly_record, key=lambda x: x['min_temp'])
        max_humidity = max(yearly_record, key=lambda x: x['max_humidity'])
        ReportPrinter.print_yearly_report(max_temp, min_temp, max_humidity)

    def generate_monthly_single_bar_chart_report(self, file_name):
        monthly_data = self.reader.read_monthly_records(file_name)
        if not monthly_data:
            return
        for data in monthly_data:
            ReportPrinter.print_single_bar_chart_report(data)

    def generate_monthly_double_bar_chart_report(self, file_name):
        monthly_data = self.reader.read_monthly_records(file_name)
        if not monthly_data:
            return
        for data in monthly_data:
            ReportPrinter.print_double_bar_chart_report(data)

    def generate_reports(self):
        for arg in self.arguments:
            file_name = "Murree_weather_"
            if self.arguments[arg] and arg != "path":
                print()
                date = self.arguments[arg].strftime("%Y_%b")
                file_name = file_name + date + ".txt";
                if arg == "a":
                    self.generate_monthly_report(file_name)
                elif arg == "b":
                    self.generate_monthly_single_bar_chart_report(file_name)
                elif arg == "c":
                    self.generate_monthly_double_bar_chart_report(file_name)
                elif arg == "e":
                    year = self.arguments[arg].strftime("%Y")
                    self.generate_yearly_report(year)


class Reader:

    def __init__(self, path):
        self.files = [f for f in glob.glob(path + "**/*.txt", recursive=True)]
        self.path = path

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

    def read_monthly_records(self, file_name):
        monthly_record = []
        file_name = self.path + file_name
        if file_name in self.files:
            with open(file_name) as weather_file:
                reader = csv.DictReader(weather_file)
                for row in reader:
                    daily_data = Reader.read_daily_records(row)
                    if daily_data:
                        monthly_record.append(daily_data)
            return monthly_record

    def read_yearly_records(self, year):
        yearly_record = []
        for i in range(1, 13):
            file_name = "Murree_weather_"
            given_date = year + "_" + calendar.month_abbr[i]
            file_name = file_name + given_date + ".txt"
            monthly_record = self.read_monthly_records(file_name)
            if monthly_record:
                yearly_record.extend(monthly_record)
        return yearly_record


def get_arguments_list():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("-a", type=Validator.is_valid_date_month)
    parser.add_argument("-b", type=Validator.is_valid_date_month)
    parser.add_argument("-c", type=Validator.is_valid_date_month)
    parser.add_argument("-e", type=Validator.is_valid_date_year)
    args = vars(parser.parse_args())
    if not (args["a"] or args["b"] or args["c"] or args["e"]):
        parser.error('No arguments provided.')
    return args


def main():
    arguments_list = get_arguments_list()
    report = ReportGenerator(arguments_list, arguments_list["path"])
    report.generate_reports()


if __name__ == "__main__":
    main()

