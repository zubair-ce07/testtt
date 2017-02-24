import calendar
import os
import argparse
from datetime import datetime
import csv
from termcolor import colored
import statistics as stats


class WeatherReport:
    report_name = None
    weather_records = []
    max_temperatures = []
    min_temperatures = []

    max_temperature = 0
    min_temperature = 0
    max_humidity = 0

    max_temperature_date = None
    min_temperature_date = None
    max_humidity_date = None

    def __init__(self, records, name):
        self.weather_records = records
        self.report_name = name

    # creates a dictionary with key=date and value = Max temperature
    def set_max_temperatures(self):
        self.max_temperatures = {x['PKT']: int(x['Max TemperatureC']) for x in
                                 self.weather_records if x['Max TemperatureC']}

    # creates a dictionary with key=date and value = Min temperature
    def set_min_temperatures(self):
        self.min_temperatures = {x['PKT']: int(x['Min TemperatureC']) for x in
                                 self.weather_records if x['Min TemperatureC']}


class MonthlyReport(WeatherReport):

    max_avg_temperature = 0
    min_avg_temperature = 0
    mean_humidity_avg = 0

    def __init__(self, records):
        WeatherReport.__init__(self, records, "Monthly Report ")

    # calculating averages of highest temp, lowest temp and mean humidity
    def calculate_statistics(self):

        self.set_max_temperatures()
        self.set_min_temperatures()
        mean_humidity = [int(x[' Mean Humidity']) for x in self.weather_records
                         if x[' Mean Humidity']]

        self.max_avg_temperature = stats.mean(self.max_temperatures.values())
        self.min_avg_temperature = stats.mean(self.min_temperatures.values())
        self.mean_humidity_avg = stats.mean(mean_humidity)

    def display_report(self):
        print(self.report_name)
        print("Highest Average: {0}{1}".format(self.max_avg_temperature, "C"))
        print("Lowest Average: {0}{1}".format(self.min_avg_temperature, "C"))
        print("Average Mean Humidity: {0}{1}".format(self.mean_humidity_avg, "%"))


class YearlyReport(WeatherReport):
    def __init__(self, records):
        WeatherReport.__init__(self, records, "Yearly Report ")

    def calculate_statistics(self):
        self.set_max_temperatures()
        self.set_min_temperatures()
        max_humidity = {x['PKT']: int(x['Max Humidity']) for x in
                        self.weather_records if x['Max Humidity']}

        self.max_temperature_date = max(self.max_temperatures,
                                        key=self.max_temperatures.get)
        self.max_temperature = self.max_temperatures[self.max_temperature_date]

        self.min_temperature_date = min(self.min_temperatures,
                                        key=self.min_temperatures.get)
        self.min_temperature = self.min_temperatures[self.min_temperature_date]

        self.max_humidity_date = max(max_humidity, key=max_humidity.get)
        self.max_humidity = max_humidity[self.max_humidity_date]

    def display_report(self):
        print(self.report_name)
        print("Highest: {0}{1} on {2}".format(self.max_temperature, 'C',
              month_day_concat(self.max_temperature_date)))
        print("Lowest: {0}{1} on {2}".format(self.min_temperature, 'C',
              month_day_concat(self.min_temperature_date)))
        print("Humidity: {0}{1} on {2}".format(self.max_humidity, '%',
              month_day_concat(self.max_humidity_date)))


class MonthlyBarChartReport(WeatherReport):
    def __init__(self, records):
        WeatherReport.__init__(self, records, "Monthly Bar Chart Report ")

    def calculate_statistics(self):
        # creating list of tuples with tuple values: day, max and min temp
        report_records = []
        for record in self.weather_records:
            if record['Max TemperatureC']:

                day = datetime.strptime(record['PKT'], '%Y-%m-%d').day
                max_temperature = int(record['Max TemperatureC'])
                min_temperature = int(record['Min TemperatureC'])
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
def month_day_concat(temperature_date):
    month = calendar.month_name[datetime.strptime(temperature_date,
                                                  '%Y-%m-%d').month]
    day = str(datetime.strptime(temperature_date, '%Y-%m-%d').day)
    return month + " " + day


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


def iterate_directory():
    weather_readings = []
    for file in os.listdir(args.FilePath):
        with open(os.path.join(args.FilePath, file)) as csv_file:
            weather_readings += csv.DictReader(csv_file)
    return weather_readings


# concat string in format:"YEAR_MONTH ABRV" for searching string in filename
def year_month_concat(year_month):
    return "{year}-{month}".format(year=year_month.strftime('%Y'),
                                   month=int(year_month.strftime('%m')))


# criteria = commandline argument passed e.g. year
def build_report_records(criteria, weather_readings):
    reports = []
    for reading in weather_readings:
        reading['PKT'] = reading.get('PKT') or reading.get('PKST')
        if criteria in reading['PKT']:
            reports.append(reading)
    return reports


def build_report():
    reports = []
    weather_readings = iterate_directory()

    if args.e is not None:
        report_records = build_report_records(args.e, weather_readings)
        report = YearlyReport(report_records)
        reports.append(report)

    if args.a is not None:
        year_month = year_month_concat(args.a)
        report_records = build_report_records(year_month, weather_readings)
        report = MonthlyReport(report_records)
        reports.append(report)

    if args.c is not None:
        year_month = year_month_concat(args.c)
        report_records = build_report_records(year_month, weather_readings)
        report = MonthlyBarChartReport(report_records)
        reports.append(report)

    if args.s is not None:
        year_month = year_month_concat(args.s)
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
