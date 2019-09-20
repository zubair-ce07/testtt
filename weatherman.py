import re
import sys
import csv
import glob
import argparse
from collections import OrderedDict
from datetime import datetime


class WeatherReporting:

    def chart_report_bonus(self, data):

        for row in data:
            file_value = 0
            file_value2 = 0
            if row["Max TemperatureC"] != "":
                to_convert = row["Max TemperatureC"]
                file_value = int(to_convert)
                split_date = row["PKT"].split("-")
                get_day = split_date[2]
                print(get_day, end="")
                for value in range(file_value):
                    print("\033[1;31m+\033[1;m", end="")
            if row["Min TemperatureC"] != "":
                to_convert = row["Min TemperatureC"]
                file_value2 = int(to_convert)
                if file_value2 < 0:
                    for value in range(abs(file_value2)):
                        print("\033[1;34m-\033[1;m", end="")
                    
                for value in range(file_value2):
                    print("\033[1;34m+\033[1;m", end="")
            print(file_value, end="")
            print("C- ", end="")
            print(file_value2, end="")
            print("C")

    def monthly_report(self, data):
        high_temp = self.needed_row(data, "Mean TemperatureC", True)
        print("Highest Average : ", high_temp["Mean TemperatureC"], "C")

        low_temp = self.needed_row(data, "Mean TemperatureC", False)
        print("Lowest Average : ", low_temp["Mean TemperatureC"], "C")

        mean_humidity = self.needed_row(data, " Mean Humidity", True)
        print("Average Mean Humidity: ", mean_humidity[" Mean Humidity"] + "%")

    def chart_report(self, data):
        self.data = data
        for row in data:
            if row["Max TemperatureC"] != "":
                to_convert = row["Max TemperatureC"]
                file_value = int(to_convert)
                split_date = row["PKT"].split("-")
                get_day = split_date[2]
                print(get_day, end="")
                for value in range(file_value):
                    print("\033[1;31m+\033[1;m", end="")
                print(" ", file_value, "C")

            if row["Min TemperatureC"] != "":
                to_convert = row["Min TemperatureC"]
                file_value2 = int(to_convert)
                split_date = row["PKT"].split("-")
                get_day = split_date[2]
                print(get_day, end="")
                if file_value2 < 0:
                    for value in range(abs(file_value2)):
                        print("\033[1;34m-\033[1;m", end="")
                    print(" ", file_value2, "C")
                else:
                    for value in range(file_value2):
                        print("\033[1;34m+\033[1;m", end="")
                    print(" ", file_value2, "C")
        
    def yearly_report(self, data):

        high_temp = self.needed_row(
            data, "Max TemperatureC", reverse_flag=True
        )
        temperature = high_temp["Max TemperatureC"]
        key = "PKT" if "PKT" in high_temp else "PKST"
        date_to_parse = high_temp.get(key)
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Highest : ", temperature, "C on", date.strftime("%B"), date.day)

        low_temp = self.needed_row(
            data, "Min TemperatureC", reverse_flag=False
        )
        temperature = low_temp["Min TemperatureC"]
        key = "PKT" if "PKT" in high_temp else "PKST"
        date_to_parse = high_temp.get(key)
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Lowest : ", temperature, "C on", date.strftime("%B"), date.day)

        mean_humidity = self.needed_row(
            data, " Mean Humidity", reverse_flag=True
        )
        temperature = mean_humidity[" Mean Humidity"]
        key = "PKT" if "PKT" in high_temp else "PKST"
        date_to_parse = high_temp.get(key)
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print(
            "Average Mean Humidity: ",
            temperature,
            "C on",
            date.strftime("%B"),
            date.day,
        )

    def needed_row(self, data, col_name, reverse_flag):
        data = [row for row in data if row[col_name] != ""]

        data.sort(key=lambda x: int(x[col_name]), reverse=reverse_flag)
        return data[0]


def reading_file(file_names):
    files_data = []
    for file in file_names:
        with open(file, newline="") as csvfile:
            file_data = csv.DictReader(csvfile)
            for row in file_data:
                files_data.append(row)
    return files_data


def get_file_name(arguments, file_name, file_path):
    pattern = "*{}_{}*.txt"

    if arguments == "a" or arguments == "c":
        file_month = datetime.strptime(file_name, "%Y/%m").strftime("%b")
        pattern = pattern.format(file_name.split("/")[0], file_month)
    elif arguments == "e":
        pattern = pattern.format(file_name, "")

    return glob.glob(file_path + pattern)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("-a")
    parser.add_argument("-e")
    parser.add_argument("-c")
    parser.add_argument("-b")
    args = parser.parse_args()

    report = WeatherReporting()
    if args.a:
        file_names = get_file_name("a", args.a, args.path)
        if file_names:
            data = reading_file(file_names)
            report.monthly_report(data)
        else:
            print("File may not be available against -a argument!")

    if args.c:
        file_names = get_file_name("c", args.c, args.path)
        if file_names:
            data = reading_file(file_names)
            report.chart_report(data)
            report.chart_report_bonus(data)
        else:
            print("File may not be available against -c argument!")

    if args.e:
        file_names = get_file_name("e", args.e, args.path)
        if file_names:
            data = reading_file(file_names)
            report.yearly_report(data)
        else:
            print("File may not be available against -e argument!")


if __name__ == "__main__":
    main()
