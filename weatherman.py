import csv
import glob
from datetime import datetime
import argparse

RED_TEXT = "\033[1;31m"
BLUE_TEXT = "\033[1;34m"
WHITE_TEXT = "\033[0;37m"


class ReportGenerator:
    def __init__(self, weather_record, year, month='*'):
        self.year = year
        self.month = month
        self.weather_record = []
        if self.month == '*':
            for r in weather_record.records:
                if r.PKT.year == int(self.year):
                    self.weather_record.append(r)
        else:
            for r in weather_record.records:
                if r.PKT.year == int(self.year) and r.PKT.month == int(self.month):
                    self.weather_record.append(r)
        self.cal = Calculations()

    def report_for_year(self):
        self.cal.calculations_for_year(self.weather_record)
        print(f"Highest: {self.cal.maxTemp.MaxTemperature}C on {self.cal.maxTemp.PKT.strftime('%B %-d')}")
        print(f"Lowest: {self.cal.minTemp.MinTemperature}C on {self.cal.minTemp.PKT.strftime('%B %-d')}")
        print(f"Humidity: {self.cal.maxHumidity.MaxHumidity}% on {self.cal.maxHumidity.PKT.strftime('%B %-d')}")

    def report_for_month(self):
        self.cal.calculations_for_month(self.weather_record)
        print(f"Highest Average: {self.cal.avgHighestTemp}C")
        print(f"Lowest Average: {self.cal.avgLowestTemp}C")
        print(f"Average Mean Humidity: {self.cal.avgMeanHumidity}%")

    def bar_charts(self):
        for r in self.weather_record:
            max_t = r.MaxTemperature
            min_t = r.MinTemperature
            if max_t:
                bar = "+" * abs(max_t)
                print(r.PKT.strftime('%d') + RED_TEXT + bar + WHITE_TEXT + str(r.MaxTemperature)+"C")
            if min_t:
                bar = "+" * abs(min_t)
                print(r.PKT.strftime('%d') + BLUE_TEXT + bar + WHITE_TEXT + str(r.MinTemperature)+"C")


class Calculations:

    def __init__(self):
        # FOR yearly reports
        self.maxTemp = None
        self.minTemp = None
        self.maxHumidity = None
        # FOR monthly reports
        self.avgHighestTemp = None
        self.avgLowestTemp = None
        self.avgMeanHumidity = None

    def calculations_for_year(self, weather_record):
        self.maxTemp = max([r for r in weather_record if r.MaxTemperature],
                           key=lambda x: x.MaxTemperature)
        self.minTemp = min([r for r in weather_record if r.MinTemperature],
                           key=lambda x: x.MinTemperature)
        self.maxHumidity = max([r for r in weather_record if r.MaxHumidity],
                               key=lambda x: x.MaxHumidity)

    def calculations_for_month(self, weather_record):
        readings1 = [r.MaxTemperature for r in weather_record if r.MaxTemperature]
        self.avgHighestTemp = sum(readings1)//len(readings1)
        readings2 = [r.MinTemperature for r in weather_record if r.MinTemperature]
        self.avgLowestTemp = sum(readings2)//len(readings2)
        readings3 = [r.MeanHumidity for r in weather_record if r.MeanHumidity]
        self.avgMeanHumidity = sum(readings3)//len(readings3)


class WeatherData:

    def __init__(self, row):
        if row.get('PKT'):
            self.PKT = datetime.strptime(row.get('PKT'), '%Y-%m-%d')
        elif row.get('PKST'):
            self.PKT = datetime.strptime(row.get('PKST'), '%Y-%m-%d')
        self.MaxTemperature = int(row['Max TemperatureC'])
        self.MeanTemperature = int(row['Mean TemperatureC'])
        self.MinTemperature = int(row['Min TemperatureC'])
        self.MaxHumidity = int(row['Max Humidity'])
        self.MeanHumidity = int(row[' Mean Humidity'])
        self.MinHumidity = int(row[' Min Humidity'])


class WeatherRecord:

    def __init__(self, path):
        self.records = []

        for file_name in glob.glob(f"{path}/Murree_weather_{'*'}_{'*'}.txt"):
            for row in csv.DictReader(open(file_name)):
                if self.is_valid_row(row):
                    self.records.append(WeatherData(row))

    @staticmethod
    def is_valid_row(row):
        if not row.get('PKT') and not row.get('PKST'):
            return False
        if not row.get('Max TemperatureC'):
            return False
        if not row['Mean TemperatureC']:
            return False
        if not row.get('Min TemperatureC'):
            return False
        if not row.get('Max Humidity'):
            return False
        if not row.get(' Mean Humidity'):
            return False
        if not row.get(' Min Humidity'):
            return False
        return True


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p')
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
            report = ReportGenerator(weather_record, year=str(arg.year))
            report.report_for_year()
            print("\n")

    if args.a:
        for arg in args.a:
            my_date = str(arg.year)+"/"+str(arg.month)
            print(f"For {my_date}")
            year, month = my_date.split("/")
            report = ReportGenerator(weather_record, year, month)
            report.report_for_month()
            print("\n")

    if args.c:
        for arg in args.c:
            my_date = str(arg.year)+"/"+str(arg.month)
            print(f"For {my_date}")
            year, month = my_date.split("/")
            report = ReportGenerator(weather_record, year, month)
            report.bar_charts()
            print("\n")


if __name__ == '__main__':
    main()
