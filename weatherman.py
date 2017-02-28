import calendar
import os
import argparse
from datetime import datetime
import csv
from termcolor import colored
import re


class WeatherReport:
    report_name = None
    weather_records = []

    def __init__(self, records, name):
        self.weather_records = records
        self.report_name = name


class MonthlyReport(WeatherReport):

    max_avg_temperature = 0
    min_avg_temperature = 0
    avg_mean_humidity = 0

    def __init__(self, records):
        WeatherReport.__init__(self, records, "Monthly Report ")

    # calculating averages of highest temp, lowest temp and mean humidity
    def calculate_statistics(self):
        sum_max_temperature = 0
        sum_min_temperature = 0
        sum_mean_humidity = 0
        records_length = len(self.weather_records)

        for record in self.weather_records:
            sum_max_temperature += record['Max TemperatureC']
            sum_min_temperature += record['Min TemperatureC']
            sum_mean_humidity += record[' Mean Humidity']

        self.max_avg_temperature = int(sum_max_temperature/records_length)
        self.min_avg_temperature = int(sum_min_temperature/records_length)
        self.avg_mean_humidity = int(sum_mean_humidity/records_length)

    def display_report(self):
        print(self.report_name)
        print("Highest Average: {0}{1}".format(self.max_avg_temperature, "C"))
        print("Lowest Average: {0}{1}".format(self.min_avg_temperature, "C"))
        print("Average Mean Humidity: {0}{1}".format(self.avg_mean_humidity, "%"))


class YearlyReport(WeatherReport):

    max_temperature = 0
    min_temperature = 0
    max_humidity = 0

    max_temperature_date = None
    min_temperature_date = None
    max_humidity_date = None

    def __init__(self, records):
        WeatherReport.__init__(self, records, "Yearly Report ")

    def calculate_statistics(self):

        record = max(self.weather_records, key=lambda x: x['Max TemperatureC'])
        self.max_temperature = record['Max TemperatureC']
        self.max_temperature_date = record['PKT']

        record = min(self.weather_records, key=lambda x: x['Min TemperatureC'])
        self.min_temperature = record['Min TemperatureC']
        self.min_temperature_date = record['PKT']

        record = max(self.weather_records, key=lambda x: x['Max Humidity'])
        self.max_humidity = record['Max Humidity']
        self.max_humidity_date = record['PKT']

    def display_report(self):
        print(self.report_name)
        print("Highest: {0}{1} on {2}".format(self.max_temperature, 'C',
              concat_month_day(self.max_temperature_date)))
        print("Lowest: {0}{1} on {2}".format(self.min_temperature, 'C',
              concat_month_day(self.min_temperature_date)))
        print("Humidity: {0}{1} on {2}".format(self.max_humidity, '%',
              concat_month_day(self.max_humidity_date)))


class MonthlyBarChartReport(WeatherReport):
    def __init__(self, records):
        WeatherReport.__init__(self, records, "Monthly Bar Chart Report ")

    def calculate_statistics(self):
        # creating list of tuples with tuple values: day, max and min temp
        report_records = []
        for record in self.weather_records:
            day = datetime.strptime(record['PKT'], '%Y-%m-%d').day
            max_temperature = record['Max TemperatureC']
            min_temperature = record['Min TemperatureC']
            weather_reading = (day, max_temperature, min_temperature)
            report_records.append(weather_reading)

        self.weather_records = report_records

    def display_report(self):
        print(self.report_name)
        for day, max_temperature, min_temperature in self.weather_records:
            print(day, end='')
            print_bar('red', max_temperature)
            print("{0}{1}{2}{3}".format(max_temperature, 'C', '\n', day), end='')
            print_bar('blue', min_temperature)
            print("{0}{1}".format(min_temperature, 'C'))


class SingleLineMonthlyReport(MonthlyBarChartReport):
    def __init__(self, records):
        MonthlyBarChartReport.__init__(self, records)

    def display_report(self):
        print(self.report_name)
        for day, max_temperature, min_temperature in self.weather_records:
            print(day, end='')
            print_bar('blue', min_temperature)
            print_bar('red', max_temperature)
            print("{0}{1}-{2}{1}".format(min_temperature, "C", max_temperature))


# for returning string of format: "MONTH_NAME DAY" for report displaying
def concat_month_day(temperature_date):
    reading_date = datetime.strptime(temperature_date, '%Y-%m-%d')
    month = calendar.month_name[reading_date.month]
    day = reading_date.day
    return "{0} {1}".format(month, day)


def print_bar(colour, temperature):
    for i in range(0, abs(temperature)):
        print(colored('+', colour), end='')


def fetch_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("FilePath", help="Path to file directory", type=str)
    parser.add_argument('-e', help='Yearly Weather Report', type=lambda d:
                        datetime.strptime(d, '%Y').strftime('%Y'))
    parser.add_argument('-a', help='Monthly Weather Report',
                        type=lambda d: datetime.strptime(d, '%Y/%m'))
    parser.add_argument('-c', help='Double Line Bar chart display report',
                        type=lambda d: datetime.strptime(d, '%Y/%m'))
    parser.add_argument('-s', help='Single Line Bar chart display report',
                        type=lambda d: datetime.strptime(d, '%Y/%m'))

    arguments = parser.parse_args()
    return arguments


def read_weather_files():
    weather_readings = []
    report_parameters = ['PKT', 'Max TemperatureC', 'Min TemperatureC',
                         ' Mean Humidity', 'Max Humidity']

    for file in os.listdir(args.FilePath):
        with open(os.path.join(args.FilePath, file)) as csv_file:

            for reading in csv.DictReader(csv_file):
                record = dict()
                record['PKT'] = reading.get('PKT') or reading.get('PKST')

                for param in report_parameters[1:]:
                    record[param] = int(reading[param]) if reading[param] else ''

                if reading['Max TemperatureC']:
                    weather_readings.append(record)

    return weather_readings


# concat string in format:"YEAR_MONTH ABRV" for searching string in filename
def concat_year_month(year_month):
    return "{year}-{month}".format(year=year_month.strftime('%Y'),
                                   month=int(year_month.strftime('%m')))


# criteria = commandline argument passed e.g. year
def build_report_records(criteria, weather_readings):
    report_records = []
    for reading in weather_readings:
        if re.findall('\\b'+criteria+'\\b', reading['PKT']):
            report_records.append(reading)

    return report_records


def build_report():
    reports = []
    weather_readings = read_weather_files()

    if args.e is not None:
        report_records = build_report_records(args.e, weather_readings)
        report = YearlyReport(report_records)
        reports.append(report)

    if args.a is not None:
        year_month = concat_year_month(args.a)
        report_records = build_report_records(year_month, weather_readings)
        report = MonthlyReport(report_records)
        reports.append(report)

    if args.c is not None:
        year_month = concat_year_month(args.c)
        report_records = build_report_records(year_month, weather_readings)
        report = MonthlyBarChartReport(report_records)
        reports.append(report)

    if args.s is not None:
        year_month = concat_year_month(args.s)
        report_records = build_report_records(year_month, weather_readings)
        report = SingleLineMonthlyReport(report_records)
        reports.append(report)

    for report in reports:
        if report.weather_records:
            report.calculate_statistics()
            report.display_report()
            print('\n')
        else:
            print("No data found for {0}\n".format(report.report_name))

if __name__ == '__main__':
    args = fetch_arguments()
    build_report()
