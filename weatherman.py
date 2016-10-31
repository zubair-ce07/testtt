import os
import fnmatch
import csv


class WeatherMan:
    def __init__(self):
        self.main_data = self.get_data()

    @staticmethod
    def find_files(path, custom_filter):
        for root, dirs, files in os.walk(path):
            for file in fnmatch.filter(files, custom_filter):
                yield os.path.join(root, file)

    def get_data(self, data=None):
        if data is None:
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
        return int(value) if value != "" else None

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
            return print("Sorry, no data :(")
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
        year_data_list = self.filter_year(self.main_data, "PKT", year)
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
        month_data_list = self.filter_month(self.main_data, "PKT", year, month)
        return month_data_list

    def month_average_report(self, year, month):
        month_data = self.get_month_data(year, month)

        if not month_data:
            return print("Sorry no data :(")

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
                             d["Max TemperatureC"])) if d["Max TemperatureC"] is not None else print("Sorry no data :(")
            print("\033[95m{} \033[94m{} \033[95m{}C".format(current, "+" * d["Min TemperatureC"],
                             d["Min TemperatureC"])) if d["Min TemperatureC"] is not None else print("Sorry no data :(")

    def month_report_single_line(self, year, month, current=0):
        month_data = self.get_month_data(year, month)

        for d in month_data:
            current += 1
            print("\033[95m{} \033[94m{}\033[91m{} \033[95m{}C - {}C".format(current, "+" * d["Min TemperatureC"],
                         "+" * d["Max TemperatureC"],d["Min TemperatureC"],d["Max TemperatureC"])) if \
                        d[ "Max TemperatureC"] and d["Min TemperatureC"] is not None else print("Sorry no data :(")


def main():
    program_id = input("Please enter 1 to see the results of your desired year \n"
                       "Please enter 2 to see the average results of your desired year and month \n"
                       "Please enter 3 to see the results in the form of horizontal bars of your desired year"
                       " and month \n"
                       "Please enter 4 to see the results in the form of a single bar of your desired year and month = ")

    month = None
    wm = WeatherMan()

    if program_id != "1":
        year = input("Please enter a year = ")
        month = input("Please enter a month = ")
    else:
        year = input("Please enter a year = ")

    if program_id == "1":
        wm.year_report(year)
    elif program_id == "2":
        wm.month_average_report(year, month)
    elif program_id == "3":
        wm.month_report_two_charts(year, month)
    elif program_id == "4":
        wm.month_report_single_line(year, month)
    else:
        "Sorry, numbers other than 1, 2, 3, 4 are not acceptable"


if __name__ == "__main__":
    main()
