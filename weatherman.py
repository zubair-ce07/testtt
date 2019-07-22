import argparse
import csv
import os.path
import calendar
from colorama import Fore, Style
from datetime import datetime


class Validator:
    @staticmethod
    def valid_date_with_month(s):
        try:
            return datetime.strptime(s, "%Y/%m")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def valid_date_with_year(s):
        try:
            return datetime.strptime(s, "%Y")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)


class Parser:

    @staticmethod
    def get_arguments_list():
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", type=Validator.valid_date_with_month)
        parser.add_argument("-b", type=Validator.valid_date_with_month)
        parser.add_argument("-c", type=Validator.valid_date_with_month)
        parser.add_argument("-e", type=Validator.valid_date_with_year)
        args = vars(parser.parse_args())
        if not any(args.values()):
            parser.error('No arguments provided.')
        return args


class Reports:
    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def generate_monthly_report(file_name):
        monthly_data = Reader.read_monthly_records(file_name)
        print("\nMonthly Report: ")
        if monthly_data is not None:
            avg_max_temp = round(sum(int(daily_data["maxtemp"]) for daily_data in monthly_data) / len(monthly_data))
            avg_min_temp = round(sum(int(daily_data["mintemp"]) for daily_data in monthly_data) / len(monthly_data))
            avg_mean_humidity = round(sum(int(daily_data["meanhumidity"]) for daily_data in monthly_data) / len(monthly_data))
            print("Highest Average: {}C".format(avg_max_temp))
            print("Lowest Average: {}C".format(avg_min_temp))
            print("Average Mean Humidity: {}%".format(avg_mean_humidity))
        else:
            print("Data not found!")

    @staticmethod
    def generate_yearly_report(given_date):
        print("\nYearly Report")
        yearly_record = Reader.read_yearly_records(given_date)
        if yearly_record != []:
            max_temp = max(yearly_record, key=lambda x: int(x['maxtemp']))
            min_temp = min(yearly_record, key=lambda x: int(x['mintemp']))
            max_humidity = max(yearly_record, key=lambda x: int(x['maxhumidity']))
            print("Highest: {}C on {}".format(max_temp["maxtemp"],  Date.format_date_with_month(max_temp["date"])))
            print("Lowest: {}C on {}".format(min_temp["mintemp"], Date.format_date_with_month(min_temp["date"])))
            print("Humidity: {}% on {}".format(max_humidity["maxhumidity"], Date.format_date_with_month(max_humidity["date"])))
        else:
            print("Data not found!")

    @staticmethod
    def generate_monthly_single_bar_chart_report(file_name):
        monthly_data = Reader.read_monthly_records(file_name)
        print("\nMonthly Single Bar Chart Report:")
        if monthly_data is not None:
            for data in monthly_data:
                print(Date.format_date_with_day(data["date"])
                      + Fore.RED
                      + " "
                      + "+" * int(data["mintemp"])
                      + Fore.BLUE
                      + "+" * (int(data["maxtemp"])-int(data["mintemp"]))
                      + Style.RESET_ALL
                      + data["mintemp"]
                      + " - "
                      + data["maxtemp"])
        else:
            print("Data not found!")

    @staticmethod
    def generate_monthly_double_bar_chart_report(file_name):
        monthly_data = Reader.read_monthly_records(file_name)
        print("\nMonthly Double Bar Chart Report:")
        if monthly_data is not None:
            for data in monthly_data:
                print(Fore.RED + "{} {} {}C".format(Date.format_date_with_day(data["date"]), "+" * int(data["maxtemp"]), data["maxtemp"]))
                print(Fore.BLUE + "{} {} {}C".format(Date.format_date_with_day(data["date"]), "+" * int(data["mintemp"]), data["mintemp"]))
            print(Style.RESET_ALL)
        else:
            print("Data not found!")

    def generate_reports(self):
        for arg in self.arguments:
            file_name = "weatherfiles/weatherfiles/Murree_weather_"
            if self.arguments[arg] is not None:
                date = self.arguments[arg].strftime("%Y_%b")
                file_name = file_name + date + ".txt";
                if arg == "a":
                    Reports.generate_monthly_report(file_name)
                elif arg == "b":
                    Reports.generate_monthly_single_bar_chart_report(file_name)
                elif arg == "c":
                    Reports.generate_monthly_double_bar_chart_report(file_name)
                else:
                    year = self.arguments[arg].strftime("%Y")
                    Reports.generate_yearly_report(year)


class Reader:


    @staticmethod
    def read_monthly_records(file_name):
        monthly_record_list = []
        if os.path.isfile(file_name):
            with open(file_name) as weather_file:
                reader = csv.DictReader(weather_file)
                for row in reader:
                    if row["Max TemperatureC"] != "" and row["Min TemperatureC"] != "" and row["Max Humidity"] != "" and row[" Mean Humidity"] != "":
                        daily_data = {
                            "date": row["PKT"],
                            "maxtemp": row["Max TemperatureC"],
                            "mintemp": row["Min TemperatureC"],
                            "maxhumidity": row["Max Humidity"],
                            "meanhumidity": row[" Mean Humidity"]
                        }
                        monthly_record_list.append(daily_data)
            return monthly_record_list

    @staticmethod
    def read_yearly_records(year):
        yearly_record_list = []
        for i in range(1, 13):
            file_name = "weatherfiles/weatherfiles/Murree_weather_"
            given_date = year + "_" + calendar.month_abbr[i]
            file_name = file_name + given_date + ".txt";
            monthly_record = Reader.read_monthly_records(file_name)
            if monthly_record is not None:
                if yearly_record_list == []:
                    yearly_record_list = monthly_record
                else:
                    yearly_record_list.extend(monthly_record)
        return yearly_record_list


class Date:

    @staticmethod
    def format_date_with_month(given_date):
        required_date = datetime.strptime(given_date, "%Y-%m-%d")
        return required_date.strftime("%B %d")

    @staticmethod
    def format_date_with_day(given_date):
        required_date = datetime.strptime(given_date, "%Y-%m-%d")
        return required_date.strftime("%d")


def main():
    arguments_list = Parser.get_arguments_list()
    report = Reports(arguments_list)
    report.generate_reports()


if __name__ == "__main__":
    main()

