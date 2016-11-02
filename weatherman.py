import os
import fnmatch
import csv
import argparse


class WeatherMan:
    def __init__(self):
        self.weather_data = self.load_data()

    @staticmethod
    def find_files(path, custom_filter):
        for root, dirs, files in os.walk(path):
            for file in fnmatch.filter(files, custom_filter):
                yield os.path.join(root, file)

    def load_data(self):
        data = []
        for textFile in self.find_files("weatherfiles", "*.txt"):
            with open(textFile) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row["Max TemperatureC"] = self.to_integer(row["Max TemperatureC"])
                    row["Min TemperatureC"] = self.to_integer(row["Min TemperatureC"])
                    row["Max Humidity"] = self.to_integer(row["Max Humidity"])
                    row[" Mean Humidity"] = self.to_integer(row[" Mean Humidity"])
                    data.append(row)
        return data

    @staticmethod
    def to_integer(value):
        return int(value) if value else None

    @staticmethod
    def filter_year(data, key, year):
        return [item for item in data if item.get(key, None) and item["PKT"][:4] == year]

    @staticmethod
    def filter_month(data, key, year, month):
        return [item for item in data if
                item.get(key, None) and (item["PKT"][:4] == year and item["PKT"][5] == month)]

    @staticmethod
    def print_statement(message, value1, value2):
        if value1 == 0:
            return print("No Data!")
        else:
            return print(message.format(value1, value2))

    @staticmethod
    def print_dashes(dash="="):
        return print(dash * 26)

    @staticmethod
    def remove_none(data, key):
        return filter(lambda x: x[key], data)

    def min_max(self, func, data, key):
        data = self.remove_none(data, key)
        return func(data, key=lambda x: x[key])

    def get_average(self, data, key):
        data = list(self.remove_none(data, key))
        return round(sum(d[key] for d in data) / len(data), 2)

    def get_year_data(self, year):
        year_data_list = self.filter_year(self.weather_data, "PKT", year)
        return year_data_list

    def year_report(self, year):
        year_data = self.get_year_data(year)

        max_value = self.min_max(max, year_data, "Max TemperatureC")
        min_value = self.min_max(min, year_data, "Min TemperatureC")
        max_humidity = self.min_max(max, year_data, " Mean Humidity")

        print()
        self.print_dashes()
        self.print_statement("Highest: {}C on {}", max_value["Max TemperatureC"], max_value["PKT"])
        self.print_dashes()
        self.print_statement("Lowest: {}C on {}", min_value["Min TemperatureC"], min_value["PKT"])
        self.print_dashes()
        self.print_statement("Humidity: {}% on {}", max_humidity[" Mean Humidity"], max_humidity["PKT"])
        self.print_dashes()

    def get_month_data(self, year, month):
        month_data_list = self.filter_month(self.weather_data, "PKT", year, month)
        return month_data_list

    def month_average_report(self, year, month):
        month_data = self.get_month_data(year, month)

        if not month_data:
            return print("No Data!")

        highest_average = self.get_average(month_data, "Max TemperatureC")
        lowest_average = self.get_average(month_data, "Min TemperatureC")
        mean_humidity_average = self.get_average(month_data, " Mean Humidity")

        print()
        self.print_dashes()
        self.print_statement("Highest Average: {}C", highest_average, None)
        self.print_dashes()
        self.print_statement("Lowest Average: {}C", lowest_average, None)
        self.print_dashes()
        self.print_statement("Average Mean Humidity: {}%", mean_humidity_average, None)
        self.print_dashes()

    def month_report_two_charts(self, year, month, current=0):
        month_data = self.get_month_data(year, month)

        for d in month_data:
            current += 1
            print("\033[95m{} \033[91m{} \033[95m{}C".format(current, "+" * d["Max TemperatureC"],
                                                             d["Max TemperatureC"])) if d[
                "Max TemperatureC"] else print("No Data!")
            print("\033[95m{} \033[94m{} \033[95m{}C".format(current, "+" * d["Min TemperatureC"],
                                                             d["Min TemperatureC"])) if d[
                "Min TemperatureC"] else print("No Data!")

    def month_report_single_line(self, year, month, current=0):
        month_data = self.get_month_data(year, month)

        for d in month_data:
            current += 1
            print("\033[95m{} \033[94m{}\033[91m{} \033[95m{}C - {}C".format(current, "+" * d["Min TemperatureC"],
                                                                             "+" * d["Max TemperatureC"],
                                                                             d["Min TemperatureC"],
                                                                             d["Max TemperatureC"])) if \
                d["Max TemperatureC"] and d["Min TemperatureC"] else print("No Data!")


def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--section")
    parser.add_argument("-y", "--year")
    parser.add_argument("-m", "--month")

    args = parser.parse_args()

    return {
        "section": args.section,
        "year": args.year,
        "month": args.month
    }


def main():
    wm = WeatherMan()

    values = arguments()

    if values["section"] == "1":
        wm.year_report(values["year"])
    elif values["section"] == "2":
        wm.month_average_report(values["year"], values["month"])
    elif values["section"] == "3":
        wm.month_report_two_charts(values["year"], values["month"])
    elif values["section"] == "4":
        wm.month_report_single_line(values["year"], values["month"])
    else:
        print("Invalid Args!")


if __name__ == "__main__":
    main()
