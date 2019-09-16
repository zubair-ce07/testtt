import argparse
import csv
import os
import sys
from datetime import datetime


class Validator:
    @staticmethod
    def validate_date(date):
        try:
            date = date.split('/')
            date = '{}-{}'.format(date[0], date[1][1])
            return date
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(date)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def validate_year(year):
        try:
            datetime.strptime(year, "%Y")
            return year
        except ValueError:
            msg = "Not a valid year: '{0}'.".format(year)
            raise argparse.ArgumentTypeError(msg)


class WeatherParser:
    def __init__(self, path):
        os.chdir(os.getcwd() + '/' + path)
        self.weather_reading_files = os.listdir()
        self.weather_reading = self.read_records()

    def get_headers(self, data_file):
        headers = []
        with open(data_file) as csv_data:
            reader = csv.reader(csv_data)
            for row in reader:
                if row:
                    headers = row
                    break
        return headers

    def read_records(self):
        weather_readings = []

        for readings_file in self.weather_reading_files:
            with open(readings_file, 'r') as readings_csv_file:
                reader = csv.DictReader(readings_csv_file, fieldnames=self.get_headers(readings_file))
                weather_readings += [reading for reading in reader]

        return weather_readings

    def read_report(self, month):
        self.weather_reading = [
            monthly_weather_reading for monthly_weather_reading in self.weather_reading
            if 'PKT' in monthly_weather_reading and month in monthly_weather_reading['PKT']
        ]
        monthly_report = self.format_record(self.weather_reading)
        return monthly_report

    def format_record(self, records):
        monthly_report = []
        for daily_record in records:
            if daily_record['Max TemperatureC'] and daily_record['Min TemperatureC'] \
                    and daily_record['Max Humidity'] and daily_record[' Mean Humidity']:
                daily_record['PKT'] = datetime.strptime(daily_record['PKT'], "%Y-%m-%d")
                daily_record['Max TemperatureC'] = int(daily_record['Max TemperatureC'])
                daily_record['Min TemperatureC'] = int(daily_record['Min TemperatureC'])
                daily_record['Max Humidity'] = int(daily_record['Max Humidity'])
                daily_record[' Mean Humidity'] = int(daily_record[' Mean Humidity'])
                monthly_report.append(daily_record)

        return monthly_report


class WeatherAnalyzer:
    def __init__(self, path):
        self.report_reader = WeatherParser(path)

    def generate_reports(self, arguments):
        if arguments.e:
            self.analyze_yearly_report(arguments.e)
        if arguments.a:
            self.analyze_monthly_report(arguments.a)
        if arguments.c:
            self.analyze_single_bar_chart_report(arguments.c)

    def analyze_monthly_report(self, month):
        records = self.report_reader.read_report(month)
        length = len(records)
        avg_max_temp = round(sum(daily_record['Max TemperatureC'] for daily_record in records) / length)
        avg_min_temp = round(sum(daily_record['Min TemperatureC'] for daily_record in records) / length)
        avg_mean_humidity = round(sum(daily_record[' Mean Humidity'] for daily_record in records) / length)
        WeatherReportGenerator.display_montly_report(avg_max_temp, avg_min_temp, avg_mean_humidity)

    def analyze_yearly_report(self, year):
        records = self.report_reader.read_report(year)
        max_temp = max(records, key=lambda record: record['Max TemperatureC'])
        min_temp = min(records, key=lambda record: record['Min TemperatureC'])
        max_humidity = max(records, key=lambda record: record['Max Humidity'])
        WeatherReportGenerator.display_yearly_report(max_temp, min_temp, max_humidity)

    def analyze_single_bar_chart_report(self, month):
        month_records = self.report_reader.read_report(month)
        if not month_records:
            return

        for daily_record in month_records:
            WeatherReportGenerator.display_single_bar_chart_report(daily_record)


class WeatherReportGenerator:

    @staticmethod
    def display_montly_report(max_temp, min_temp, mean_humidity):
        highest_avg = "Highest Average: {}C".format(max_temp)
        lowest_avg = "Lowest Average: {}C".format(min_temp)
        avg_humidity = "Average Mean Humidity: {}%".format(mean_humidity)
        print(highest_avg, lowest_avg, avg_humidity, sep="\n")

    @staticmethod
    def display_yearly_report(max_temp, min_temp, max_humidity):
        max_temp = "Highest: {}C on {}".format(
            max_temp["Max TemperatureC"],
            max_temp["PKT"].strftime("%B %d")
        )
        min_temp = "Lowest: {}C on {}".format(
            min_temp["Min TemperatureC"],
            min_temp["PKT"].strftime("%B %d")
        )
        max_humidity = "Humidity: {}% on {}".format(
            max_humidity["Max Humidity"],
            max_humidity["PKT"].strftime("%B %d")
        )
        print(max_temp, min_temp, max_humidity, sep="\n")

    @staticmethod
    def display_single_bar_chart_report(daily_record):
        print(daily_record['PKT'].strftime("%d")
              + '+' * daily_record['Max TemperatureC'] + ' '
              + '\033[91m {}C\033[00m'.format(str(daily_record['Max TemperatureC'])) + '\n' +
              daily_record['PKT'].strftime("%d")
              + '+' * daily_record['Min TemperatureC'] + ' '
              + '\033[34m{}C\033[00m'.format(str(daily_record['Min TemperatureC'])))


def parse_arguments():
    parser = argparse.ArgumentParser()
    if len(sys.argv) > 1:
        parser.add_argument("path", type=str)
        parser.add_argument('-e', type=Validator.validate_year)
        parser.add_argument('-a', type=Validator.validate_date)
        parser.add_argument('-c', type=Validator.validate_date)
        args = parser.parse_args()
    else:
        parser.error('No arguments provided.')

    return args


def main():
    arguments = parse_arguments()
    report = WeatherAnalyzer(arguments.path)
    report.generate_reports(arguments)
    


if __name__ == "__main__":
    main()
