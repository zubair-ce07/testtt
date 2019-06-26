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

    def required_files(self, path, date_object):
        if isinstance(date_object, datetime):
            files_names = glob.glob("{}/Murree_weather_{}.txt".format(
                path, date_object.strftime("%Y_%b")))
        else:
            files_names = glob.glob("{}/Murree_weather_{}_*.txt".format(
                path, date_object))

        return [x for x in files_names]

    def read_files_record(self, weather_files):
        clean_record = []
        required_fields = ["Max TemperatureC",
                           "Min TemperatureC", "Max Humidity"]
        for weather_file in weather_files:
            with open(weather_file) as f:
                weather_records = csv.DictReader(f)

                for weather_record in weather_records:
                    key_index = list(weather_record)[0]

                    if all(weather_record.get(y) for y in required_fields):

                        weather_record = WeatherRecord(weather_record[key_index],
                                                       int(weather_record["Max TemperatureC"]),
                                                       int(weather_record["Min TemperatureC"]),
                                                       int(weather_record["Max Humidity"]))

                        clean_record.append(weather_record)

        return clean_record

    def parse_weather_records(self, path, year_month):
        weather_files = self.required_files(path, year_month)
        return self.read_files_record(weather_files)


class ProcessWeatherReports():
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(ProcessWeatherReports, self).__new__(self)

        return self._instance

    def __init__(self):
        self.record_calculations = CalculateWeatherResults()

    def show_extreme_results(self, report_result, extreme_report_type):
        date_object = datetime.strptime(report_result.date, "%Y-%m-%d")
        print(f"{extreme_report_type}: {report_result.max_temp} C on "
              f"{date_object.strftime('%b %d')}")

    def process_extreme_result(self, weather_record):

        if weather_record:
            highest_temp, lowest_temp, max_humidity = self. \
                record_calculations.calculate_extreme_report(weather_record)

            self.show_extreme_results(highest_temp, "Highest")
            self.show_extreme_results(lowest_temp, "Lowest")
            self.show_extreme_results(max_humidity, "Max Humidity")
        else:
            print("Invalid Input, Files doesn't exists")

    def process_average_result(self, weather_record):

        if weather_record:
            avg_high_temp, avg_low_temp, avg_hum = self. \
                record_calculations.calculate_month_report(weather_record)

            print(f"Highest Average: {avg_high_temp} C")
            print(f"Lowest Average: {avg_low_temp} C")
            print(f"Humidity Average: {avg_hum} per")
        else:
            print("Invalid Input, Files doesn't exists")

    def show_seprate_chart(self, clean_record):
        if clean_record:
            for weather_record in clean_record:
                date_object = datetime.strptime(weather_record.date, "%Y-%m-%d")
                print(date_object.strftime("%d"), end="")

                for plus_counter in range(0, int(weather_record.max_temp)):
                    print("\033[1;31;40m + ", end="")

                print(f"{weather_record.max_temp} C")
                print(date_object.strftime("%d"), end="")

                for plus_counter in range(0, int(weather_record.min_temp)):
                    print("\033[1;34;40m - ", end="")
                print(f"{weather_record.min_temp} C")
        else:
            print("Invalid Input, Files doesn't exists")

    def show_merge_chart(self, clean_record):
        if clean_record:
            for weather_record in clean_record:
                date_object = datetime.strptime(weather_record.date, "%Y-%m-%d")
                print(f"\033[1;31;40m {date_object.strftime('%d')}", end="\t")
                print(f"\033[1;31;40m {weather_record.max_temp} C", end="")

                for plus_counter in range(0, int(weather_record.max_temp)):
                    print("\033[1;31;40m + ", end="")

                for plus_counter in range(0, int(weather_record.min_temp)):
                    print("\033[1;34;40m + ", end="")

                print(f"\033[1;34;40m {weather_record.min_temp} C")
        else:
            print("Invalid Input, Files doesn't exists")


class CalculateWeatherResults:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(CalculateWeatherResults, self).__new__(self)

        return self._instance

    def calculate_extreme_report(self, weather_record):
        highest_temp = max(weather_record, key=lambda x: int(x.max_temp))
        lowest_temp = min(weather_record, key=lambda x: int(x.min_temp))
        max_humidity = max(weather_record, key=lambda x: int(x.max_humidity))

        return highest_temp, lowest_temp, max_humidity

    def calculate_month_report(self, clean_record):
        max_temps_avg = sum([int(x.max_temp) for x in clean_record]) / len(clean_record)
        min_temps_avg = sum([int(x.min_temp) for x in clean_record]) / len(clean_record)
        max_humidities_avg = sum([int(x.max_humidity) for x in clean_record]) / len(clean_record)

        return max_temps_avg, min_temps_avg, max_humidities_avg


def check_dir_path(string):
    if not os.path.exists(string):
        error_message = "given path is invalid"
        raise argparse.ArgumentTypeError(error_message)

    return string


def seprate_year_month(year_month):
    date_object = datetime.strptime(year_month, "%Y/%m")
    return date_object


def main():
    parser = argparse.ArgumentParser(description="Calculating and showing "
                                                 "weather reports fetched from the data files")
    parser.add_argument("path", type=check_dir_path, help="Directory Destinantion")
    parser.add_argument("-e", "--year", type=str, help="Year Parameter")
    parser.add_argument("-a", "--month", type=seprate_year_month, help="Month Parameter")
    parser.add_argument("-c", "--graphsingle", type=seprate_year_month, help="Show single graph")
    parser.add_argument("-m", "--graphmerged", type=seprate_year_month, help="Show merged graph")
    args = parser.parse_args()

    parser = WeatherReportParse()
    process_results = ProcessWeatherReports()

    if args.year:
        weather_record = parser.parse_weather_records(args.path, args.year)
        process_results.process_extreme_result(weather_record)

    if args.month:
        weather_record = parser.parse_weather_records(args.path, args.month)
        process_results.process_average_result(weather_record)

    if args.graphsingle:
        weather_record = parser.parse_weather_records(args.path, args.graphsingle)
        process_results.show_seprate_chart(weather_record)

    if args.graphmerged:
        weather_record = parser.parse_weather_records(args.path, args.graphmerged)
        process_results.show_merge_chart(weather_record)


if __name__ == "__main__":
    main()

