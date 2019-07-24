import argparse
import csv
from datetime import datetime
import glob
import os


class WeatherRecord:
    def __init__(self, date, max_temp, min_temp, max_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity


class WeatherRecordsParser:
    required_fields = ['Max TemperatureC', 'Min TemperatureC',
                       'Max Humidity']

    def read_files_records(self, file_names_template):
        files = glob.glob(file_names_template, )
        return sum([self.get_records(weather_file)
                    for weather_file in files], [])

    def get_records(self, weather_file):
        records = []
        with open(weather_file) as f:
            for weather_record in csv.DictReader(f):
                if all(weather_record.get(y) for y in self.required_fields):
                    date = weather_record.get('PKT', weather_record.get('PKST'))
                    weather_record = WeatherRecord(date,
                                                   int(weather_record['Max TemperatureC']),
                                                   int(weather_record['Min TemperatureC']),
                                                   int(weather_record['Max Humidity']))

                    records.append(weather_record)

        return records


class CalculateWeatherResults:

    def calculate_extreme_report(self, records):
        highest_temp = max(records, key=lambda x: x.max_temp)
        lowest_temp = min(records, key=lambda x: x.min_temp)
        max_humidity = max(records, key=lambda x: x.max_humidity)

        return highest_temp, lowest_temp, max_humidity

    def calculate_month_report(self, records):
        max_temps_avg = sum([x.max_temp for x in records]) / len(records)
        min_temps_avg = sum([x.min_temp for x in records]) / len(records)
        max_humidities_avg = sum([x.max_humidity for x in records]) / len(records)

        return max_temps_avg, min_temps_avg, max_humidities_avg


class WeatherReportsProcess():
    reports_calculator = CalculateWeatherResults()

    def show_extreme_results(self, report_result, extreme_report_type):
        date_object = datetime.strptime(report_result.date, '%Y-%m-%d')
        print(f'{extreme_report_type}: {report_result.max_temp} C on '
              f'{date_object.strftime("%b %d")}')

    def process_extreme_result(self, records):
        if not records:
            print('Invalid Input, Files doesnot exists')
            return

        highest_temp, lowest_temp, max_humidity = self.reports_calculator.calculate_extreme_report(records)

        self.show_extreme_results(highest_temp, 'Highest')
        self.show_extreme_results(lowest_temp, 'Lowest')
        self.show_extreme_results(max_humidity, 'Max Humidity')

    def process_average_result(self, records):
        if not records:
            print('Invalid Input, Files doesnot exists')
            return

        avg_high_temp, avg_low_temp, avg_hum = self. \
            reports_calculator.calculate_month_report(records)

        print(f'Highest Average: {avg_high_temp} C')
        print(f'Lowest Average: {avg_low_temp} C')
        print(f'Humidity Average: {avg_hum} per')

    def show_seprate_chart(self, records):
        if not records:
            print('Invalid Input, Files doesnot exists')
            return

        for weather_record in records:
            date_object = datetime.strptime(weather_record.date, '%Y-%m-%d')
            print(date_object.strftime('%d'), end='')

            for plus_counter in range(0, weather_record.max_temp):
                print(f'\033[1;31;40m + ', end='')

            print(f'{weather_record.max_temp} C')
            print(date_object.strftime('%d'), end='')

            for plus_counter in range(0, weather_record.min_temp):
                print(f'\033[1;34;40m - ', end='')
            print(f'{weather_record.min_temp} C')

    def show_merge_chart(self, records):
        if not records:
            print('Invalid Input, Files doesnot exists')
            return

        for weather_record in records:
            date_object = datetime.strptime(weather_record.date, '%Y-%m-%d')
            print(f'\033[1;31;40m {date_object.strftime("%d")}', end='\t')
            print(f'\033[1;31;40m {weather_record.max_temp} C', end='')

            for plus_counter in range(0, weather_record.max_temp):
                print('\033[1;31;40m + ', end='')

            for plus_counter in range(0, weather_record.min_temp):
                print('\033[1;34;40m + ', end='')

            print(f'\033[1;34;40m {weather_record.min_temp} C')


def check_dir_path(string):
    if not os.path.exists(string):
        error_message = 'given path is invalid'
        raise argparse.ArgumentTypeError(error_message)

    return string


def seprate_year_month(year_month):
    date = datetime.strptime(year_month, '%Y/%m')
    return f'{date.strftime("%Y")}_{date.strftime("%b")}'


def main():
    record_parser = argparse.ArgumentParser(description='Calculating and showing '
                                                        'weather reports fetched from the data files')
    record_parser.add_argument('path', type=check_dir_path, help='Directory Destinantion')
    record_parser.add_argument('-e', '--year', type=str, help='Year Parameter')
    record_parser.add_argument('-a', '--month', type=seprate_year_month, help='Month Parameter')
    record_parser.add_argument('-c', '--graphsingle', type=seprate_year_month, help='Show single graph')
    record_parser.add_argument('-m', '--graphmerged', type=seprate_year_month, help='Show merged graph')
    args = record_parser.parse_args()

    record_parser = WeatherRecordsParser()
    process_results = WeatherReportsProcess()
    file_names_template = f'{args.path}/Murree_weather_' + '{}*'

    if args.year:
        records = record_parser.read_files_records(file_names_template.format(args.year))
        process_results.process_extreme_result(records)

    if args.month:
        records = record_parser.read_files_records(file_names_template.format(args.month))
        process_results.process_average_result(records)

    if args.graphsingle:
        records = record_parser.read_files_records(file_names_template.format(args.graphsingle))
        process_results.show_seprate_chart(records)

    if args.graphmerged:
        records = record_parser.read_files_records(file_names_template.format(args.graphmerged))
        process_results.show_merge_chart(records)


if __name__ == '__main__':
    main()

