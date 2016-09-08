from datetime import datetime
import csv
import sys
import argparse


class Weather(object):
    __date_format = "%Y-%m-%d"

    def __init__(self, path, year, month=0):
        if path[0] == "\\":
            path = path[1:]
        if path[0] == "/":
            path = path[1:]
        self.path = path
        self.year = year
        self.month = month
        self.file_names = []
        self.file_data = []
        self.parse_file_names()
        self.get_rows()

    def get_lowest(self, column_num):
        sorted_list = sorted([row for row in self.file_data if row[column_num] != ''],
                             key=lambda row: int(row[column_num]), reverse=False)
        return sorted_list[0][0], sorted_list[0][column_num]

    def get_highest(self, column_num):
        sorted_list = sorted([row for row in self.file_data if row[column_num] != ''],
                             key=lambda row: int(row[column_num]), reverse=True)
        return sorted_list[0][0], sorted_list[0][column_num]

    def get_average(self, column_num):
        sum = 0
        count = 0
        for row in self.file_data:
            if row[column_num] != '':
                count += 1
                sum += int(row[column_num])
        if count == 0:
            return 0
        return sum/count

    def parse_file_names(self):
        if self.month:
            self.file_names.append("/lahore_weather_" + str(self.year) + "_" + Util.get_month_name(self.month) + ".txt")
        else:
            for i in range(1, 13):
                self.file_names.append("/lahore_weather_" + str(self.year) + "_" + Util.get_month_name(i) + ".txt")

    def get_rows(self):
        file_not_found_count = 0
        for file_name in self.file_names:
            try:
                csv_file = open(self.path + file_name, "r")
                reader = csv.DictReader(csv_file, delimiter=',')
                for row in Weather.get_next_row(reader):
                    self.file_data.append(row)
            except:
                file_not_found_count += 1
                if file_not_found_count == len(self.file_names):
                    raise

    @staticmethod
    def get_next_row(reader):
        prev = None
        is_first = True
        for row in reader:
            if len(row) == 0:
                continue
            if prev:
                yield prev[None]
            if is_first:
                is_first = False
                continue
            prev = row

    def generate_yearly_report(self):
        current = self.get_highest(1)
        date_object = Util.get_formatted_date(current[0])
        print("Highest: ", str(current[1]) + "C", " on", date_object.strftime("%B"), " ", date_object.strftime("%d"))
        current = self.get_lowest(3)
        date_object = Util.get_formatted_date(current[0])
        print("Lowest: ", str(current[1]) + "C", " on", date_object.strftime("%B"), " ", date_object.strftime("%d"))
        current = self.get_highest(7)
        date_object = Util.get_formatted_date(current[0])
        print("Humid: ", str(current[1]) + "%", " on", date_object.strftime("%B"), " ", date_object.strftime("%d"))

    def generate_monthly_report(self):
        current = self.get_highest(2)
        print("Highest Average: ", str(current[1]) + "C")
        current = self.get_lowest(2)
        print("Lowest Average: ", str(current[1]) + "C")
        current = self.get_average(8)
        print("Average Humidity: ", str(current) + "%")

    def separate_bar_chart_monthly(self):
        date_object = Util.get_formatted_date(str(self.year)+"-" + str(self.month) + "-01")
        print(date_object.strftime("%B"),self.year)
        for row in self.file_data:
            date_object = Util.get_formatted_date(row[0])
            try:
                max = int(row[1])
                print(date_object.strftime("%d"), end="")
                for temp in range(0, max):
                    print("\033[91m+", end="")
                print("\033[0m", max, "C")
                min = int(row[3])
                print(date_object.strftime("%d"), end="")
                for temp in range(0, min):
                    print("\033[94m+", end="")
                print("\033[0m", str(min) + "C")
            except Exception as e:
                print(e)

    def single_bar_chart_monthly(self):
        date_object = Util.get_formatted_date(str(self.year)+"-" + str(self.month) + "-01")
        print(date_object.strftime("%B"),self.year)
        for row in self.file_data:
            date_object = Util.get_formatted_date(row[0])
            try:
                max = int(row[1])
                min = int(row[3])
                print(date_object.strftime("%d"), end="")
                for temp in range(0, min):
                    print("\033[94m+", end="")
                for temp in range(1, max):
                    print("\033[91m+", end="")
                print("\033[0m", str(min) + "C-" + str(max) + "C")
            except:
                pass


class Util(object):
    @staticmethod
    def get_formatted_date(date_str=""):
        date_format = "%Y-%m-%d"
        from datetime import datetime
        if not date_str:
            return datetime.today().date()
        return datetime.strptime(date_str, date_format).date()

    @staticmethod
    def get_month_name(month):
        return Util.get_formatted_date("2000-" + str(month) + "-01").strftime("%b")


def main():
    parser = argparse.ArgumentParser(description='Description of your program')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', nargs=2)
    group.add_argument('-b', nargs=2)
    group.add_argument('-c', nargs=2)
    group.add_argument('-e', nargs=2)
    parsed = parser.parse_args()
    try:
        if parsed.e:
            weather_data = Weather(parsed.e[1], parsed.e[0])
            weather_data.generate_yearly_report()
        elif parsed.a:
            temp = parsed.a[0].split("/")
            weather_data = Weather(parsed.a[1], temp[0], int(temp[1]))
            weather_data.generate_monthly_report()
        elif parsed.c:
            temp = parsed.c[0].split("/")
            weather_data = Weather(parsed.c[1], temp[0], int(temp[1]))
            weather_data.separate_bar_chart_monthly()
        elif parsed.b:
            temp = parsed.b[0].split("/")
            weather_data = Weather(parsed.b[1], temp[0], int(temp[1]))
            weather_data.single_bar_chart_monthly()
    except FileNotFoundError:
        print("No Such File Exists!!")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()