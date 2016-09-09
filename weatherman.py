from datetime import datetime
import csv
import argparse
import fnmatch
import os


class Weather(object):
    __date_format = "%Y-%m-%d"

    def __init__(self, weather_records):
        self.weather_records = weather_records

    def get_lowest(self, column_name):
        condition = [row for row in self.weather_records if row[column_name]]
        sorted_list = sorted(condition, key=lambda row: int(row[column_name]), reverse=False)
        if len(sorted_list) is 0:
            raise EmptyFileException
        return sorted_list[0][Util.get_date_key(sorted_list[0])], sorted_list[0][column_name]

    def get_highest(self, column_name):
        condition = [row for row in self.weather_records if row[column_name]]
        sorted_list = sorted(condition, key=lambda row: int(row[column_name]), reverse=True)
        if len(sorted_list) is 0:
            raise EmptyFileException
        return sorted_list[0][Util.get_date_key(sorted_list[0])], sorted_list[0][column_name]

    def get_average(self, column_name):
        sum = 0
        count = 0
        for row in self.weather_records:
            if row[column_name]:
                count += 1
                sum += int(row[column_name])
        if count == 0:
            return 0
        return sum/count


class WeatherParser(object):

    def __init__(self, user_input):
        self.file_names = []
        self.user_input = user_input
        self.parse_file_names()

    def parse_file_names(self):
        if self.user_input.month:
            pattern = "*" + str(self.user_input.year) + "*"
            pattern += Util.get_month_name(self.user_input.month) + '.txt'
            for file in os.listdir(os.path.basename(self.user_input.path)):
                if fnmatch.fnmatch(file, pattern):
                    self.file_names.append(file)
        else:
            for file in os.listdir(os.path.basename(self.user_input.path)):
                if fnmatch.fnmatch(file, "*"+str(self.user_input.year) + '_*.txt'):
                    self.file_names.append(file)

    def get_rows(self):
        file_not_found_count = 0
        weather_records = []
        if len(self.file_names) == 0:
            raise FileNotFoundError
        for file_name in self.file_names:
            try:
                full_path = os.path.join(os.path.basename(self.user_input.path), file_name)
                csv_file = open(full_path, "r")
                next(csv_file)
                reader = csv.DictReader(csv_file, delimiter=',')
                for row in WeatherParser.get_next_row(reader):
                    single_row = {}
                    for key in row.keys():
                        single_row.update({key: row[key]})
                    weather_records.append(single_row)
            except:
                file_not_found_count += 1
                if file_not_found_count == len(self.file_names):
                    raise
        return weather_records

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
    def __init__(self, user_input):
        self.user_input = user_input
        weather_parser = WeatherParser(user_input)
        self.weather_records = weather_parser.get_rows()
        self.weather = Weather(self.weather_records)

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
        date_str = str(self.user_input.year)+"-" + str(self.user_input.month) + "-01"
        date_object = Util.get_formatted_date(date_str)
        print(date_object.strftime("%B"), self.user_input.year)
        for row in self.weather_records:
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
        date_str = str(self.user_input.year) + "-" + str(self.user_input.month) + "-01"
        date_object = Util.get_formatted_date(date_str)
        print(date_object.strftime("%B"), self.user_input.year)
        for row in self.weather_records:
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


class EmptyFileException(Exception):
    def __init___(self, error):
        pass


class UserInput(object):
    def __init__(self, path, year, month=0):
        self.path = path
        self.year = year
        self.month = month


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
            user_input = UserInput(parsed.e[1], parsed.e[0])
            report_generator = ReportGenerator(user_input)
            report_generator.generate_extreme_condition_report()
        elif parsed.a:
            temp = parsed.a[0].split("/")
            user_input = UserInput(parsed.a[1], temp[0], int(temp[1]))
            report_generator = ReportGenerator(user_input)
            report_generator.generate_average_condition_report()
        elif parsed.c:
            temp = parsed.c[0].split("/")
            user_input = UserInput(parsed.c[1], temp[0], int(temp[1]))
            report_generator = ReportGenerator(user_input)
            report_generator.generate_multi_line_bar_chart()
        elif parsed.s:
            temp = parsed.s[0].split("/")
            user_input = UserInput(parsed.s[1], temp[0], int(temp[1]))
            report_generator = ReportGenerator(user_input)
            report_generator.generate_single_line_bar_chart()
    except FileNotFoundError:
        print("No Such File Exists!!")
    except EmptyFileException as e:
        print("Given Data Files are empty for selected column")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
