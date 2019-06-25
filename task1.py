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

    def get_file_names(self, path, date_object):
        if isinstance(date_object, datetime):
            files_names = glob.glob("{}/Murree_weather_{}_{}.txt".format(
                path, date_object.strftime("%Y"), date_object.strftime("%b")))
        else:
            files_names = glob.glob("{}/Murree_weather_{}_*.txt".format(
                path, date_object))

        return [x[18:] for x in files_names]

    def read_files_record(self, weather_file_names, path):
        clean_data = []
        for weather_file in weather_file_names:
            weather_data = csv.DictReader(open(os.path.join(path, weather_file)))

            for weather_record in weather_data:

                if all(weather_record[y] for y in ["Max TemperatureC", "Min TemperatureC", "Max Humidity"]):
                    clean_data.append(WeatherRecord(weather_record["PKT"], int(weather_record["Max TemperatureC"]),
                                                    int(weather_record["Min TemperatureC"]),
                                                    int(weather_record["Max Humidity"])))

        return clean_data

    def parse_weather_data(self, path, year_month):
        weather_file_names = self.get_file_names(path, year_month)
        return self.read_files_record(weather_file_names, path)


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
        print("{}: {} C on {} {}".format(extreme_report_type, report_result.max_temp, date_object.strftime("%b"),
                                         date_object.strftime("%d")))

    def process_extreme_result(self, clean_weather_record):

        if clean_weather_record:
            highest_temp, lowest_temp, max_humidity = self.record_calculations.calculate_extreme_report(
                clean_weather_record)
            self.show_extreme_results(highest_temp, "Highest")
            self.show_extreme_results(lowest_temp, "Lowest")
            self.show_extreme_results(max_humidity, "Max Humidity")
        else:
            print("Invalid Input, Files doesn't exists")

    def process_average_result(self, clean_weather_record):

        if clean_weather_record:
            avg_high_temp, avg_low_temp, avg_hum = self.record_calculations.calculate_month_report(clean_weather_record)
            print("Highest Average: {} C".format(avg_high_temp))
            print("Lowest Average: {} C".format(avg_low_temp))
            print("Humidity Average: {} per".format(avg_hum))
        else:
            print("Invalid Input, Files doesn't exists")

    def show_seprate_chart(self, clean_data):
        if clean_data:
            for weather_record in clean_data:
                date_object = datetime.strptime(weather_record.date, "%Y-%m-%d")
                print(date_object.strftime("%d"), end="")

                for i in range(0, int(weather_record.max_temp)):
                    print("\033[1;31;40m + ", end="")

                print("{} C".format(weather_record.max_temp))
                print(date_object.strftime("%d"), end="")

                for j in range(0, int(weather_record.min_temp)):
                    print("\033[1;34;40m - ", end="")
                print("{} C".format(weather_record.min_temp))
        else:
            print("Invalid Input, Files doesn't exists")

    def show_merge_chart(self, clean_data):
        if clean_data:
            for weather_record in clean_data:
                date_object = datetime.strptime(weather_record.date, "%Y-%m-%d")
                print("\033[1;31;40m {}".format(date_object.strftime("%d")), end="\t")
                print("\033[1;31;40m {} C".format(weather_record.max_temp), end="")

                for i in range(0, int(weather_record.max_temp)):
                    print("\033[1;31;40m + ", end="")

                for j in range(0, int(weather_record.min_temp)):
                    print("\033[1;34;40m + ", end="")

                print("\033[1;34;40m {} C".format(weather_record.min_temp))
        else:
            print("Invalid Input, Files doesn't exists")


class CalculateWeatherResults:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(CalculateWeatherResults, self).__new__(self)

        return self._instance

    def calculate_extreme_report(self, clean_data):
        highest_temp = max(clean_data, key=lambda x: int(x.max_temp))
        lowest_temp = min(clean_data, key=lambda x: int(x.min_temp))
        max_humidity = max(clean_data, key=lambda x: int(x.max_humidity))

        return highest_temp, lowest_temp, max_humidity

    def calculate_month_report(self, clean_data):
        max_temps_avg = sum([int(x.max_temp) for x in clean_data]) / len(clean_data)
        min_temps_avg = sum([int(x.min_temp) for x in clean_data]) / len(clean_data)
        max_humidities_avg = sum([int(x.max_humidity) for x in clean_data]) / len(clean_data)

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
        clean_weather_record = parser.parse_weather_data(args.path, args.year)
        process_results.process_extreme_result(clean_weather_record)

    if args.month:
        clean_weather_record = parser.parse_weather_data(args.path, args.month)
        process_results.process_average_result(clean_weather_record)

    if args.graphsingle:
        clean_weather_record = parser.parse_weather_data(args.path, args.graphsingle)
        process_results.show_seprate_chart(clean_weather_record)

    if args.graphmerged:
        clean_weather_record = parser.parse_weather_data(args.path, args.graphmerged)
        process_results.show_merge_chart(clean_weather_record)


if __name__ == "__main__":
    main()

