import csv
import glob
from datetime import datetime
import argparse

RED_TEXT = "\033[1;31m"
BLUE_TEXT = "\033[1;34m"
WHITE_TEXT = "\033[0;37m"


class ReportGenerator:
    def __init__(self, weather_record, year, month='*'):
        self.weather_record = []
        if month == '*':
            for r in weather_record.records:
                if r.record_date.year == year:
                    self.weather_record.append(r)
        else:
            for r in weather_record.records:
                if r.record_date.year == year and r.record_date.month == month:
                    self.weather_record.append(r)
        self.cal = Calculations()

    def report_for_year(self):
        max_temp, min_temp, max_humidity = self.cal.calculations_for_year(self.weather_record)
        print(f"Highest: {max_temp.max_temperature}C on {max_temp.record_date.strftime('%B %-d')}")
        print(f"Lowest: {min_temp.min_temperature}C on {min_temp.record_date.strftime('%B %-d')}")
        print(f"Humidity: {max_humidity.max_humidity}% on {max_humidity.record_date.strftime('%B %-d')}")

    def report_for_month(self):
        avg_highest_temp, avg_lowest_temp, avg_mean_humidity = self.cal.calculations_for_month(self.weather_record)
        print(f"Highest Average: {avg_highest_temp}C")
        print(f"Lowest Average: {avg_lowest_temp}C")
        print(f"Average Mean Humidity: {avg_mean_humidity}%")

    def bar_charts(self):
        for r in self.weather_record:
            max_t = r.max_temperature
            min_t = r.min_temperature
            bar = "+" * abs(max_t)
            print(f"{r.record_date.strftime('%d')}{RED_TEXT}{bar}{WHITE_TEXT} {r.max_temperature}C")
            bar = "+" * abs(min_t)
            print(f"{r.record_date.strftime('%d')}{BLUE_TEXT}{bar}{WHITE_TEXT}{r.min_temperature}C")


class Calculations:
    def calculations_for_year(self, weather_record):
        max_temp = max([r for r in weather_record if r.max_temperature],
                       key=lambda x: x.max_temperature)
        min_temp = min([r for r in weather_record if r.min_temperature],
                       key=lambda x: x.min_temperature)
        max_humidity = max([r for r in weather_record if r.max_humidity],
                           key=lambda x: x.max_humidity)
        return max_temp, min_temp, max_humidity

    def calculations_for_month(self, weather_record):
        max_temps = [r.max_temperature for r in weather_record if r.max_temperature]
        avg_highest_temp = sum(max_temps) // len(max_temps)
        min_temps = [r.min_temperature for r in weather_record if r.min_temperature]
        avg_lowest_temp = sum(min_temps) // len(min_temps)
        mean_humidity = [r.mean_humidity for r in weather_record if r.mean_humidity]
        avg_mean_humidity = sum(mean_humidity) // len(mean_humidity)
        return avg_highest_temp, avg_lowest_temp, avg_mean_humidity


class WeatherData:
    def __init__(self, row):
        if row.get('PKT'):
            self.record_date = datetime.strptime(row.get('PKT'), '%Y-%m-%d')
        elif row.get('PKST'):
            self.record_date = datetime.strptime(row.get('PKST'), '%Y-%m-%d')
        self.max_temperature = int(row['Max TemperatureC'])
        self.mean_temperature = int(row['Mean TemperatureC'])
        self.min_temperature = int(row['Min TemperatureC'])
        self.max_humidity = int(row['Max Humidity'])
        self.mean_humidity = int(row[' Mean Humidity'])
        self.min_humidity = int(row[' Min Humidity'])


class WeatherRecord:
    def __init__(self, path):
        self.records = []

        for file_name in glob.glob(f"{path}/Murree_weather_{'*'}_{'*'}.txt"):
            for row in csv.DictReader(open(file_name)):
                if self.is_valid_row(row):
                    self.records.append(WeatherData(row))

    @staticmethod
    def is_valid_row(row):
        if (row.get('PKT') or row.get('PKST')) and row.get('Max TemperatureC') and row.get('Mean TemperatureC') and \
                row.get('Min TemperatureC') and row.get('Max Humidity') and row.get(' Mean Humidity') and \
                row.get(' Min Humidity'):
            return True
        return False


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', help="Enter the path to weather files")
    arg_parser.add_argument('-e', nargs='*', type=lambda x: datetime.strptime(x, '%Y'),
                            help="Enter a year to get the max temp, min temp and max humidity")
    arg_parser.add_argument('-a', nargs='*', type=lambda x: datetime.strptime(x, '%Y/%m'),
                            help="Enter a year/month to get the average highest temp, "
                                 "average lowest temp and average mean humidity")
    arg_parser.add_argument('-c', nargs='*', type=lambda x: datetime.strptime(x, '%Y/%m'),
                            help="Enter a year/month to generate bar charts for each day's highest and lowest temp")
    args = arg_parser.parse_args()

    weather_record = WeatherRecord(args.p)

    if args.e:
        for arg in args.e:
            print("For {}:".format(arg.year))
            report = ReportGenerator(weather_record, arg.year)
            report.report_for_year()
            print("\n")

    if args.a:
        for arg in args.a:
            print(f"For {arg.year}/{arg.month}")
            report = ReportGenerator(weather_record, arg.year, arg.month)
            report.report_for_month()
            print("\n")

    if args.c:
        for arg in args.c:
            print(f"For {arg.year}/{arg.month}")
            report = ReportGenerator(weather_record, arg.year, arg.month)
            report.bar_charts()
            print("\n")


if __name__ == '__main__':
    main()
