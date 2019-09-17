import argparse
import csv
import os
from datetime import datetime
from weatherreading import WeatherReading


class Validator:
    @staticmethod
    def validate_date(date):
        try:
            date = date.split('/')
            date = '{}-{}-01'.format(date[0], int(date[1]))
            date = datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(date)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def validate_year(year):
        try:
            return int(year)
        except ValueError:
            msg = "Not a valid year: '{0}'.".format(year)
            raise argparse.ArgumentTypeError(msg)


class WeatherParser:
    def __init__(self, path):
        os.chdir(os.getcwd() + '/' + path)
        self.weather_readings = []
        for readings_file in os.listdir():
            with open(readings_file, 'r') as readings_csv_file:
                for row in csv.DictReader(readings_csv_file, fieldnames=self.get_headers(readings_file)):
                    if not any(garbage in (row.get('PKT') or row.get('PKST'))
                               for garbage in ['PKT', 'PKST', '<!--']):
                        self.weather_readings.append(WeatherReading(row))

    def get_headers(self, data_file):
        headers = []
        with open(data_file) as csv_data:
            reader = csv.reader(csv_data)
            for row in reader:
                if row:
                    headers = row
                    break
        return headers

    def filter_reports(self, year, month=None):
        filter_readings = []
        for reading in self.weather_readings:
            try:
                if month == reading.date.month and reading.date.year == year:
                    filter_readings.append(reading)
                elif not month and year == reading.date.year:
                    filter_readings.append(reading)
            except AttributeError:
                pass
        return filter_readings


class WeatherAnalyzer:
    def __init__(self, path):
        self.report_reader = WeatherParser(path)

    def analyze_monthly_report(self, date):
        year = date.year
        month = date.month
        monthly_records = self.report_reader.filter_reports(year, month)
        length = len(monthly_records)
        avg_max_temp = round(sum(daily_record.max_temp for daily_record in monthly_records) / length)
        avg_min_temp = round(sum(daily_record.min_temp for daily_record in monthly_records) / length)
        avg_mean_humidity = round(sum(daily_record.mean_humidity for daily_record in monthly_records) / length)
        WeatherReportGenerator.display_monthly_report(avg_max_temp, avg_min_temp, avg_mean_humidity)

    def analyze_yearly_report(self, year):
        yearly_records = self.report_reader.filter_reports(year)
        max_temp_record = max(yearly_records, key=lambda record: record.max_temp)
        min_temp_record = min(yearly_records, key=lambda record: record.min_temp)
        max_humidity_record = max(yearly_records, key=lambda record: record.mean_humidity)
        WeatherReportGenerator.display_yearly_report(max_temp_record, min_temp_record, max_humidity_record)

    def analyze_single_bar_chart_report(self, date):
        year = date.year
        month = date.month
        monthly_records = self.report_reader.filter_reports(year, month)
        if not monthly_records:
            return

        for daily_record in monthly_records:
            WeatherReportGenerator.display_single_bar_chart_report(daily_record)


class WeatherReportGenerator:

    @staticmethod
    def display_monthly_report(max_temp, min_temp, mean_humidity):
        highest_avg = "Highest Average: {}C".format(max_temp)
        lowest_avg = "Lowest Average: {}C".format(min_temp)
        avg_humidity = "Average Mean Humidity: {}%".format(mean_humidity)
        print(highest_avg, lowest_avg, avg_humidity, sep="\n")

    @staticmethod
    def display_yearly_report(max_temp_record, min_temp_record, max_humidity_record):
        max_temp = "Highest: {}C on {}".format(
            max_temp_record.max_temp,
            min_temp_record.date.strftime("%B %d")
        )
        min_temp = "Lowest: {}C on {}".format(
            min_temp_record.min_temp,
            min_temp_record.date.strftime("%B %d")
        )
        max_humidity = "Humidity: {}% on {}".format(
            max_humidity_record.max_humidity,
            max_humidity_record.date.strftime("%B %d")
        )
        print(max_temp, min_temp, max_humidity, sep="\n")

    @staticmethod
    def display_single_bar_chart_report(daily_record):
        print(daily_record.date.strftime("%d")
              + '+' * daily_record.max_temp + ' '
              + '\033[91m {}C\033[00m'.format(daily_record.max_temp) + '\n' +
              daily_record.date.strftime("%d")
              + '+' * daily_record.min_temp + ' '
              + '\033[34m{}C\033[00m'.format(daily_record.min_temp))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument('-e', type=Validator.validate_year, nargs='*')
    parser.add_argument('-a', type=Validator.validate_date, nargs='*')
    parser.add_argument('-c', type=Validator.validate_date, nargs='*')
    args = parser.parse_args()
    return args


def main():
    arguments = parse_arguments()
    report = WeatherAnalyzer(arguments.path)
    if arguments.e:
        for e in arguments.e:
            report.analyze_yearly_report(e)
    if arguments.a:
        for a in arguments.a:
            report.analyze_monthly_report(a)
    if arguments.c:
        for c in arguments.c:
            report.analyze_single_bar_chart_report(c)


if __name__ == "__main__":
    main()
