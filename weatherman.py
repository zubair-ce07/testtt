import csv
import glob
import argparse

from datetime import datetime
from colorama import Fore, Style


class Validator:
    @staticmethod
    def valid_date(date):
        try:
            date = datetime.strptime(date, "%Y/%m")
            date = date.strftime("%Y_%b")
            return date
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(date)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def valid_year(year):
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
        print(highest_avg, lowest_avg, avg_humidity, sep="\n")

    @staticmethod
    def print_year_report(max_temp, min_temp, max_humidity):
        max_temp = "Highest: {}C on {}".format(
            max_temp["max_temp"],
            max_temp["date"].strftime("%B %d")
        )
        min_temp = "Lowest: {}C on {}".format(
            min_temp["min_temp"],
            min_temp["date"].strftime("%B %d")
        )
        max_humidity = "Humidity: {}% on {}".format(
            max_humidity["max_humidity"],
            max_humidity["date"].strftime("%B %d")
        )
        print(max_temp, min_temp, max_humidity, sep="\n")

    @staticmethod
    def print_single_bar_chart_report(daily_record):
        print(daily_record["date"].strftime("%d")
              + Fore.RED
              + " "
              + "+" * daily_record["min_temp"]
              + Fore.BLUE
              + "+" * (daily_record["max_temp"] - daily_record["min_temp"])
              + Style.RESET_ALL
              + str(daily_record["min_temp"])
              + " - "
              + str(daily_record["max_temp"]))

    @staticmethod
    def print_double_bar_chart_report(daily_record):
        print(Fore.RED + "{} {} {}C".format(
            daily_record["date"].strftime("%d"),
            "+" * daily_record["max_temp"],
            daily_record["max_temp"]
        )
              )
        print(Fore.BLUE + "{} {} {}C".format(
            daily_record["date"].strftime("%d"),
            "+" * daily_record["min_temp"],
            daily_record["min_temp"]
        )
              )
        print(Style.RESET_ALL)


class ReportGenerator:
    def __init__(self, path):
        self.report_reader = ReportReader(path)

    def generate_month_report(self, date):
        records = self.report_reader.read_records(date)
        if not records:
            return

        length = len(records)
        avg_max_temp = round(sum(daily_record["max_temp"] for daily_record in records) / length)
        avg_min_temp = round(sum(daily_record["min_temp"] for daily_record in records) / length)
        avg_mean_humidity = round(sum(daily_record["mean_humidity"] for daily_record in records) / length)
        ReportPrinter.print_month_report(avg_max_temp, avg_min_temp, avg_mean_humidity)

    def generate_year_report(self, year):
        records = self.report_reader.read_records(year)
        if not records:
            return

        max_temp = max(records, key=lambda x: x['max_temp'])
        min_temp = min(records, key=lambda x: x['min_temp'])
        max_humidity = max(records, key=lambda x: x['max_humidity'])
        ReportPrinter.print_year_report(max_temp, min_temp, max_humidity)

    def generate_single_bar_chart_report(self, date):
        month_records = self.report_reader.read_records(date)
        if not month_records:
            return

        for daily_record in month_records:
            ReportPrinter.print_single_bar_chart_report(daily_record)

    def generate_double_bar_chart_report(self, date):
        month_records = self.report_reader.read_records(date)
        if not month_records:
            return

        for daily_record in month_records:
            ReportPrinter.print_double_bar_chart_report(daily_record)

    def generate_reports(self, arguments):
        if arguments.a:
            self.generate_month_report(arguments.a)

        if arguments.b:
            self.generate_single_bar_chart_report(arguments.b)

        if arguments.c:
            self.generate_double_bar_chart_report(arguments.c)

        if arguments.e:
            self.generate_year_report(arguments.e)


class ReportReader:
    def __init__(self, path):
        self.path = path
        self.files = [file_ for file_ in glob.glob(path + "**/*.txt", recursive=True)]

    @staticmethod
    def format_records(daily_record):
        if daily_record["Max TemperatureC"] and daily_record["Min TemperatureC"]\
                and daily_record["Max Humidity"] and daily_record[" Mean Humidity"]:
            daily_record = {
                "date": datetime.strptime(daily_record["PKT"], "%Y-%m-%d"),
                "max_temp": int(daily_record["Max TemperatureC"]),
                "min_temp": int(daily_record["Min TemperatureC"]),
                "max_humidity": int(daily_record["Max Humidity"]),
                "mean_humidity": int(daily_record[" Mean Humidity"])
            }
            return daily_record

    def read_records(self, date):
        records = []
        
        file_names = [file_ for file_ in self.files if date in file_]
        for file_ in file_names:
            with open(file_) as weather_file:
                reader = csv.DictReader(weather_file)
                for row in reader:
                    daily_record = self.format_records(row)
                    if daily_record:
                        records.append(daily_record)

            records.extend(records)
        return records


def get_arguments_list():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("-a", type=Validator.valid_date)
    parser.add_argument("-b", type=Validator.valid_date)
    parser.add_argument("-c", type=Validator.valid_date)
    parser.add_argument("-e", type=Validator.valid_year)
    args = parser.parse_args()

    if not (args.a or args.b or args.c or args.e):
        parser.error('No arguments provided.')

    return args


def main():
    arguments = get_arguments_list()
    report_generator = ReportGenerator(arguments.path)
    report_generator.generate_reports(arguments)


if __name__ == "__main__":
    main()

