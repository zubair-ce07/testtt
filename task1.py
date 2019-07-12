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


class WeatherReportParse:
    _instance = None

    def __new__(self):

        if not self._instance:
            self._instance = super(WeatherReportParse, self).__new__(self)

        return self._instance

    def read_files_records(self, files):
        records = []
        required_fields = ["Max TemperatureC",
                           "Min TemperatureC", "Max Humidity"]
        for weather_file in files:
            with open(weather_file) as f:

                for weather_record in csv.DictReader(f):

                    key_index = self.get_key(weather_record)

                    if all(weather_record.get(y) for y in required_fields):
                        weather_record = WeatherRecord(weather_record[key_index],
                                                       int(weather_record["Max TemperatureC"]),
                                                       int(weather_record["Min TemperatureC"]),
                                                       int(weather_record["Max Humidity"]))

                        records.append(weather_record)

        return records

    def get_key(self, record):

        if record.get('PKT'):
            return 'PKT'
        return 'PKST'

    def parse_weather_records(self, path, year_month):
        files = glob.glob(f"{path}/{year_month}")
        return self.read_files_records(files)


class WeatherReportsProcess():
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(WeatherReportsProcess, self).__new__(self)

        return self._instance

    def __init__(self):
        self.reports_calculator = CalculateWeatherResults()

    def show_extreme_results(self, report_result, extreme_report_type):
        date_object = datetime.strptime(report_result.date, "%Y-%m-%d")
        print(f"{extreme_report_type}: {report_result.max_temp} C on "
              f"{date_object.strftime('%b %d')}")

    def process_extreme_result(self, records):

        if not records:
            print("Invalid Input, Files doesn't exists")
            return

        highest_temp, lowest_temp, max_humidity = self. \
            reports_calculator.calculate_extreme_report(records)

        self.show_extreme_results(highest_temp, "Highest")
        self.show_extreme_results(lowest_temp, "Lowest")
        self.show_extreme_results(max_humidity, "Max Humidity")

    def process_average_result(self, records):

        if not records:
            print("Invalid Input, Files doesn't exists")
            return

        avg_high_temp, avg_low_temp, avg_hum = self. \
            reports_calculator.calculate_month_report(records)

        print(f"Highest Average: {avg_high_temp} C")
        print(f"Lowest Average: {avg_low_temp} C")
        print(f"Humidity Average: {avg_hum} per")

    def show_seprate_chart(self, records):
        if not records:
            print("Invalid Input, Files doesn't exists")
            return

        for weather_record in records:
            date_object = datetime.strptime(weather_record.date, "%Y-%m-%d")
            print(date_object.strftime("%d"), end="")

            for plus_counter in range(0, int(weather_record.max_temp)):
                print(f"\033[1;31;40m + ", end="")

            print(f"{weather_record.max_temp} C")
            print(date_object.strftime("%d"), end="")

            for plus_counter in range(0, int(weather_record.min_temp)):
                print(f"\033[1;34;40m - ", end="")
            print(f"{weather_record.min_temp} C")

    def show_merge_chart(self, records):
        if not records:
            print("Invalid Input, Files doesn't exists")
            return

        for weather_record in records:
            date_object = datetime.strptime(weather_record.date, "%Y-%m-%d")
            print(f"\033[1;31;40m {date_object.strftime('%d')}", end="\t")
            print(f"\033[1;31;40m {weather_record.max_temp} C", end="")

            for plus_counter in range(0, int(weather_record.max_temp)):
                print("\033[1;31;40m + ", end="")

            for plus_counter in range(0, int(weather_record.min_temp)):
                print("\033[1;34;40m + ", end="")

            print(f"\033[1;34;40m {weather_record.min_temp} C")


class CalculateWeatherResults:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(CalculateWeatherResults, self).__new__(self)

        return self._instance

    def calculate_extreme_report(self, records):
        highest_temp = max(records, key=lambda x: int(x.max_temp))
        lowest_temp = min(records, key=lambda x: int(x.min_temp))
        max_humidity = max(records, key=lambda x: int(x.max_humidity))

        return highest_temp, lowest_temp, max_humidity

    def calculate_month_report(self, records):
        max_temps_avg = sum([int(x.max_temp) for x in records]) / len(records)
        min_temps_avg = sum([int(x.min_temp) for x in records]) / len(records)
        max_humidities_avg = sum([int(x.max_humidity) for x in records]) / len(records)

        return max_temps_avg, min_temps_avg, max_humidities_avg


def check_dir_path(string):
    if not os.path.exists(string):
        error_message = "given path is invalid"
        raise argparse.ArgumentTypeError(error_message)

    return string


def seprate_year_month(year_month):
    date = datetime.strptime(year_month, "%Y/%m")
    return f'Murree_weather_{date.strftime("%Y")}_{date.strftime("%b")}*'


def year_pattren(year):
    return f'Murree_weather_{year}*'


def main():
    parser = argparse.ArgumentParser(description="Calculating and showing "
                                                 "weather reports fetched from the data files")
    parser.add_argument("path", type=check_dir_path, help="Directory Destinantion")
    parser.add_argument("-e", "--year", type=year_pattren, help="Year Parameter")
    parser.add_argument("-a", "--month", type=seprate_year_month, help="Month Parameter")
    parser.add_argument("-c", "--graphsingle", type=seprate_year_month, help="Show single graph")
    parser.add_argument("-m", "--graphmerged", type=seprate_year_month, help="Show merged graph")
    args = parser.parse_args()

    parser = WeatherReportParse()
    process_results = WeatherReportsProcess()

    if args.year:
        records = parser.parse_weather_records(args.path, args.year)
        process_results.process_extreme_result(records)

    if args.month:
        records = parser.parse_weather_records(args.path, args.month)
        process_results.process_average_result(records)

    if args.graphsingle:
        records = parser.parse_weather_records(args.path, args.graphsingle)
        process_results.show_seprate_chart(records)

    if args.graphmerged:
        records = parser.parse_weather_records(args.path, args.graphmerged)
        process_results.show_merge_chart(records)


if __name__ == "__main__":
    main()

