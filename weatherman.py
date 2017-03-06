import calendar
import os
import argparse
from datetime import datetime
import csv
from termcolor import colored


class WeatherReport:

    def __init__(self, readings, name):
        self.weather_records = readings
        self.report_name = name


class MonthlyReport(WeatherReport):

    def __init__(self, readings):
        super().__init__(readings, "Monthly Report ")
        self.max_avg_temperature = 0
        self.min_avg_temperature = 0
        self.avg_mean_humidity = 0

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

    def __init__(self, readings):
        super().__init__(readings, "Yearly Report ")
        self.max_temperature = 0
        self.min_temperature = 0
        self.max_humidity = 0

        self.max_temperature_date = None
        self.min_temperature_date = None
        self.max_humidity_date = None

    def calculate_statistics(self):

        reading = max(self.weather_records, key=lambda x: x['Max TemperatureC'])
        self.max_temperature = reading['Max TemperatureC']
        self.max_temperature_date = reading['PKT']

        reading = min(self.weather_records, key=lambda x: x['Min TemperatureC'])
        self.min_temperature = reading['Min TemperatureC']
        self.min_temperature_date = reading['PKT']

        reading = max(self.weather_records, key=lambda x: x['Max Humidity'])
        self.max_humidity = reading['Max Humidity']
        self.max_humidity_date = reading['PKT']

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
        super().__init__(records, "Monthly Bar Chart Report ")

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
        super().__init__(records)

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
    report_parameters = ['Max TemperatureC', 'Min TemperatureC',
                         ' Mean Humidity', 'Max Humidity']

    for file in os.listdir(args.FilePath):
        with open(os.path.join(args.FilePath, file)) as csv_file:

            for row in csv.DictReader(csv_file):
                record = {'PKT': row.get('PKT') or row.get('PKST')}

                for param in report_parameters:
                    record[param] = int(row[param]) if row[param] else ''

                if row['Max TemperatureC']:
                    weather_readings.append(record)

    return weather_readings


# concat string in format:"YEAR_MONTH ABRV" for searching string in filename
def concat_year_month(year_month):
    return "{year}-{month}-".format(year=year_month.strftime('%Y'),
                                    month=int(year_month.strftime('%m')))


# criteria = commandline argument passed e.g. year
def build_report_records(criteria, weather_readings):
    weather_records = []
    for reading in weather_readings:
        if criteria in reading['PKT']:
            weather_records.append(reading)

    return weather_records


def build_report():
    weather_reports = []
    weather_readings = read_weather_files()

    if args.e:
        weather_records = build_report_records(args.e, weather_readings)
        report = YearlyReport(weather_records)
        weather_reports.append(report)

    if args.a:
        year_month = concat_year_month(args.a)
        weather_records = build_report_records(year_month, weather_readings)
        report = MonthlyReport(weather_records)
        weather_reports.append(report)

    if args.c:
        year_month = concat_year_month(args.c)
        weather_records = build_report_records(year_month, weather_readings)
        report = MonthlyBarChartReport(weather_records)
        weather_reports.append(report)

    if args.s:
        year_month = concat_year_month(args.s)
        weather_records = build_report_records(year_month, weather_readings)
        report = SingleLineMonthlyReport(weather_records)
        weather_reports.append(report)

    for report in weather_reports:
        if report.weather_records:
            report.calculate_statistics()
            report.display_report()
            print('\n')
        else:
            print("No data found for {0}\n".format(report.report_name))

if __name__ == '__main__':
    args = fetch_arguments()
    build_report()
