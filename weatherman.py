import calendar
import os
import argparse
from datetime import datetime
import csv
from termcolor import colored


class WeatherReport:
    reports = []
    max_temperatures = []
    min_temperatures = []
    highest = 0
    lowest = 0
    humidity = 0

    highest_temp_date = None
    lowest_temp_date = None
    max_humidity_date = None

    def __init__(self, reports):
        self.reports = reports

    # creates a dictionary with key=date and value = Max temperature
    def set_max_temperatures(self):
        self.max_temperatures = {x['PKT']: int(x['Max TemperatureC']) for x in
                                 self.reports if x['Max TemperatureC']}

    # creates a dictionary with key=date and value = Min temperature
    def set_min_temperatures(self):
        self.min_temperatures = {x['PKT']: int(x['Min TemperatureC']) for x in
                                 self.reports if x['Min TemperatureC']}


class MonthlyReport(WeatherReport):
    def __init__(self, reports):
        WeatherReport.__init__(self, reports)

    # calculating averages of highest temp, lowest temp and mean humidity
    def calculate_statistics(self):
        self.set_max_temperatures()
        self.set_min_temperatures()
        self.highest = sum([i for i in self.max_temperatures.values()])/len(
                            self.max_temperatures)
        self.lowest = sum([i for i in self.min_temperatures.values()])/len(
                            self.min_temperatures)
        mean_humidity = [int(x[' Mean Humidity']) for x in self.reports
                         if x[' Mean Humidity']]
        self.humidity = sum(i for i in mean_humidity)/len(mean_humidity)

    def display_report(self):
        print("Monthly Report:")
        print("Highest Average: {0}{1}".format(self.highest, "C"))
        print("Lowest Average: {0}{1}".format(self.lowest, "C"))
        print("Average Mean Humidity: {0}{1}".format(self.humidity, "%"))


# for returning string of format: "MONTH_NAME DAY" for report displaying
def month_day_concat(temperature_date):
    month = calendar.month_name[datetime.strptime(temperature_date,
                                                  '%Y-%m-%d').month]
    day = str(datetime.strptime(temperature_date, '%Y-%m-%d').day)
    return month + " " + day


class YearlyReport(WeatherReport):
    def __init__(self, reports):
        WeatherReport.__init__(self, reports)

    # calculating the highest temperature, lowest temperature and highest
    # humidity of the year along with their respective dates
    def calculate_statistics(self):
        self.set_max_temperatures()
        self.set_min_temperatures()

        self.highest_temp_date = max(self.max_temperatures,
                                     key=self.max_temperatures.get)
        self.highest = self.max_temperatures[self.highest_temp_date]
        self.lowest_temp_date = min(self.min_temperatures,
                                    key=self.min_temperatures.get)
        self.lowest = self.min_temperatures[self.lowest_temp_date]
        max_humidity = {x['PKT']: int(x['Max Humidity']) for x in
                        self.reports if x['Max Humidity']}
        self.max_humidity_date = max(max_humidity, key=max_humidity.get)
        self.humidity = max_humidity[self.max_humidity_date]

    def display_report(self):
        print("Yearly Report:")
        print("Highest: {0}{1} on {2}".format(self.highest, 'C',
              month_day_concat(self.highest_temp_date)))
        print("Lowest: {0}{1} on {2}".format(self.lowest, 'C',
              month_day_concat(self.lowest_temp_date)))
        print("Humidity: {0}{1} on {2}".format(self.humidity, '%',
              month_day_concat(self.max_humidity_date)))


class MonthlyBarChartReport(WeatherReport):
    def __init__(self, reports):
        WeatherReport.__init__(self, reports)

    def calculate_statistics(self):
        # creating list of tuples with tuple values: day, max and min temp
        reports = []
        for report in self.reports:
            if report['Max TemperatureC']:
                day = datetime.strptime(report['PKT'], '%Y-%m-%d').day
                max_temperature = int(report['Max TemperatureC'])
                min_temperature = int(report['Min TemperatureC'])
                weather_reading = (day, max_temperature, min_temperature)
                reports.append(weather_reading)

        self.reports = reports

    def display_report(self):
        print("Monthly Two line Bar chart Report:")
        for day, max_temperature, min_temperature in self.reports:
            print(day, end='')
            print_bar('red', max_temperature)
            print("{0}{1}{2}{3}".format(max_temperature, 'C', '\n', day),end='')
            print_bar('blue', min_temperature)
            print("{0}{1}".format(min_temperature, 'C'))


class SingleLineMonthlyReport(MonthlyBarChartReport):
    def __init__(self, reports):
        MonthlyBarChartReport.__init__(self, reports)

    def display_report(self):
        print("Monthly Single Line Bar chart Report:")
        for day, max_temperature, min_temperature in self.reports:
            print(day, end='')
            print_bar('blue', max_temperature)
            print_bar('red', min_temperature)
            print("{0}{1}-{2}{1}".format(max_temperature, "C", min_temperature))


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
    parser.add_argument('-c', help='Monthly Weather Report display Bar Chart',
                        type=lambda d: datetime.strptime(d, '%Y/%m'))
    parser.add_argument('-s', help='Single Line Monthly Weather Report display'
                                   ' Bar Chart',
                        type=lambda d: datetime.strptime(d, '%Y/%m'))

    arguments = parser.parse_args()
    return arguments


def iterate_directory():
    reports = []
    for file in os.listdir(args.FilePath):
        with open(os.path.join(args.FilePath, file)) as csv_file:
            weather_readings = csv.DictReader(csv_file)
            for reading in weather_readings:
                reports.append(reading)
    return reports  # contains a list of dictionaries built from all the files


# concat string in format:"YEAR_MONTH ABRV" for searching string in filename
def year_mon_concat(year_month):
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
        year_month = year_mon_concat(args.a)
        report_records = build_report_records(year_month, weather_readings)
        report = MonthlyReport(report_records)
        reports.append(report)

    if args.c is not None:
        year_month = year_mon_concat(args.c)
        report_records = build_report_records(year_month, weather_readings)
        report = MonthlyBarChartReport(report_records)
        reports.append(report)

    if args.s is not None:
        year_month = year_mon_concat(args.s)
        report_records = build_report_records(year_month, weather_readings)
        report = SingleLineMonthlyReport(report_records)
        reports.append(report)

    for report in reports:
        if report.reports:
            report.calculate_statistics()
            report.display_report()
            print('\n')
        else:
            print("No data found for the specified year.")

if __name__ == '__main__':
    args = fetch_arguments()
    build_report()
