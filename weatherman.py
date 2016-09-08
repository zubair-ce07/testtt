from datetime import datetime
import csv
import sys
import argparse
import fnmatch
import os
import os.path


class Weather(object):
    __date_format = "%Y-%m-%d"

    def __init__(self, path, year, month=0):
        self.path = path
        self.year = year
        self.month = month
        self.file_names = []
        self.file_rows = []
        self.parse_file_names()
        self.get_rows()

    def get_lowest(self, column_name):
        condition = [row for row in self.file_rows if row[column_name] != '']
        sorted_list = sorted(condition, key=lambda row: int(row[column_name]), reverse=False)
        return sorted_list[0][Util.get_date_key(sorted_list[0])], sorted_list[0][column_name]

    def get_highest(self, column_name):
        condition = [row for row in self.file_rows if row[column_name] != '']
        sorted_list = sorted(condition, key=lambda row: int(row[column_name]), reverse=True)
        return sorted_list[0][Util.get_date_key(sorted_list[0])], sorted_list[0][column_name]

    def get_average(self, column_name):
        sum = 0
        count = 0
        for row in self.file_rows:
            if row[column_name] is not None:
                count += 1
                sum += int(row[column_name])
        if count == 0:
            return 0
        return sum/count

    def parse_file_names(self):
        if self.month:
            pattern = "*" + str(self.year) + "*"
            pattern += Util.get_month_name(self.month) + '.txt'
            for file in os.listdir(os.path.basename(self.path)):
                if fnmatch.fnmatch(file, pattern):
                    self.file_names.append(file)
        else:
            for file in os.listdir(os.path.basename(self.path)):
                if fnmatch.fnmatch(file, "*"+str(self.year) + '_*.txt'):
                    self.file_names.append(file)

    def get_rows(self):
        file_not_found_count = 0
        if len(self.file_names) == 0:
            raise FileNotFoundError
        for file_name in self.file_names:
            try:
                full_path = os.path.join(os.path.basename(self.path), file_name)
                csv_file = open(full_path, "r")
                next(csv_file)
                reader = csv.DictReader(csv_file, delimiter=',')
                for row in Weather.get_next_row(reader):
                    self.file_rows.append(row)
            except:
                file_not_found_count += 1
                if file_not_found_count == len(self.file_names):
                    raise

    @staticmethod
    def get_next_row(reader):
        prev = None
        for row in reader:
            if len(row) == 0:
                continue
            if prev:
                yield prev
            prev = row


class ReportGenerator(object):
    def __init__(self, weather):
        self.weather = weather

    def generate_extreme_condition_report(self):
        current = self.weather.get_highest('Max TemperatureC')
        date_object = Util.get_formatted_date(current[0])
        result = "Highest: " + str(current[1]) + "C on"
        result += date_object.strftime("%B")
        result += " "
        result += date_object.strftime("%d")
        print(result)
        current = self.weather.get_lowest('Min TemperatureC')
        date_object = Util.get_formatted_date(current[0])
        result = "Lowest: " + str(current[1]) + "C on"
        result += date_object.strftime("%B")
        result += " "
        result += date_object.strftime("%d")
        print(result)
        current = self.weather.get_highest("Max Humidity")
        date_object = Util.get_formatted_date(current[0])
        result = "Humid: " + str(current[1]) + "%" + " on"
        result += date_object.strftime("%B")
        result += " "
        result += date_object.strftime("%d")
        print(result)

    def generate_average_condition_report(self):
        current = self.weather.get_highest('Mean TemperatureC')
        print("Highest Average: ", str(current[1]) + "C")
        current = self.weather.get_lowest('Mean TemperatureC')
        print("Lowest Average: ", str(current[1]) + "C")
        current = self.weather.get_average(' Mean Humidity')
        print("Average Humidity: ", str(current) + "%")

    def generate_multi_line_bar_chart(self):
        date_str = str(self.weather.year)+"-" + str(self.weather.month) + "-01"
        date_object = Util.get_formatted_date(date_str)
        print(date_object.strftime("%B"), self.weather.year)
        for row in self.weather.file_rows:
            date_object = Util.get_formatted_date(row[Util.get_date_key(row)])
            try:
                max = int(row['Max TemperatureC'])
                print(date_object.strftime("%d"), end="")
                for temp in range(0, max):
                    print("\033[91m+", end="")
                print("\033[0m", max, "C")
                min = int(row['Min TemperatureC'])
                print(date_object.strftime("%d"), end="")
                for temp in range(0, min):
                    print("\033[94m+", end="")
                print("\033[0m", str(min) + "C")
            except:
                pass

    def generate_single_line_bar_chart(self):
        date_str = str(self.weather.year) + "-" + str(self.weather.month) + "-01"
        date_object = Util.get_formatted_date(date_str)
        print(date_object.strftime("%B"), self.weather.year)
        for row in self.weather.file_rows:
            date_object = Util.get_formatted_date(row[Util.get_date_key(row)])
            try:
                max = int(row['Max TemperatureC'])
                min = int(row['Min TemperatureC'])
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
        date_str = "2000-" + str(month) + "-01"
        return Util.get_formatted_date(date_str).strftime("%b")

    @staticmethod
    def get_date_key(row):
        if 'PKT' in row.keys():
            return 'PKT'
        else:
            return 'PKST'


def main():
    parser = argparse.ArgumentParser(description='Weather Data Analyser')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', help='Averages', nargs=2)
    group.add_argument('-s', help='Single Line Charts', nargs=2)
    group.add_argument('-c', help='Charts', nargs=2)
    group.add_argument('-e', help='Extremes', nargs=2)
    parsed = parser.parse_args()
    try:
        if parsed.e:
            weather = Weather(parsed.e[1], parsed.e[0])
            report_generator = ReportGenerator(weather)
            report_generator.generate_extreme_condition_report()
        elif parsed.a:
            temp = parsed.a[0].split("/")
            weather = Weather(parsed.a[1], temp[0], int(temp[1]))
            report_generator = ReportGenerator(weather)
            report_generator.generate_average_condition_report()
        elif parsed.c:
            temp = parsed.c[0].split("/")
            weather = Weather(parsed.c[1], temp[0], int(temp[1]))
            report_generator = ReportGenerator(weather)
            report_generator.generate_multi_line_bar_chart()
        elif parsed.s:
            temp = parsed.s[0].split("/")
            weather = Weather(parsed.s[1], temp[0], int(temp[1]))
            report_generator = ReportGenerator(weather)
            report_generator.generate_single_line_bar_chart()
    except FileNotFoundError:
        print("No Such File Exists!!")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
