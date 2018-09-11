
import csv
import sys
import os
import argparse
from datetime import datetime

class WeatherRecord:
    def __init__(self):
        self._PKT = None
        self._max_temp_c = 0
        self._mean_temp_c = 0
        self._min_temp_c = 0
        self._dew_point_c = 0
        self._mean_dewpoint_c = 0
        self._min_dewpoint_c = 0
        self._max_humidity = 0
        self._mean_humidity = 0
        self._file_weather_record = ""


class FileParser:
    def __init__(self, path):
        self._path = path
        self._readings = []

    def parse_file(self):
        for file in os.listdir(self._path):
            if ("Murree_weather_" in file):
                with open(os.path.join(self._path, file)) as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    for reading in csv_reader:
                        record = WeatherRecord()
                        record._PKT = datetime.strptime(reading["PKT"],'%Y-%m-%d')
                        record._max_temp_c = float(reading["Max TemperatureC"]) if reading["Max TemperatureC"] else 0.0
                        record._mean_temp_c = float(reading["Mean TemperatureC"]) if reading["Mean TemperatureC"] else 0.0
                        record._min_temp_c = float(reading["Min TemperatureC"]) if reading["Min TemperatureC"] else 0.0
                        record._dew_point_c = float(reading["Dew PointC"]) if reading["Dew PointC"] else 0.0
                        record._mean_dewpoint_c = float(reading["MeanDew PointC"]) if reading["MeanDew PointC"] else 0.0
                        record._min_dewpoint_c = float(reading["Min DewpointC"]) if reading["Min DewpointC"] else 0.0
                        record._max_humidity = float(reading["Max Humidity"]) if reading["Max Humidity"] else 0.0
                        record._mean_humidity = float(reading[" Mean Humidity"]) if reading[" Mean Humidity"] else 0.0
                        record._file_weather_record = file
                        self._readings.append(record)

        if self._readings:
            return self._readings
        else:
            print("No weather files exist in this directory or wrong file name entered")

    def filter_weather_records(self, year):
        return [reading for reading in self._readings if year in reading._file_weather_record]
         

class Calculations:
    def __init__(self, _weather_records):
        self._weather_records = _weather_records
        self._calculation_results = {}

    def calculate_hghst_lwst_temp_hmidity(self):
        self._calculation_results["Highest_temp_day"] = max(self._weather_records, key=lambda wr:wr._max_temp_c)
        self._calculation_results["Lowest_temp_day"] = min(self._weather_records, key=lambda wr:wr._min_temp_c)
        self._calculation_results["Max_humidity_day"] = max(self._weather_records, key=lambda wr:wr._max_humidity)
        return self._calculation_results

    def calculate_avg_temp_humidity(self):
        max_temp = [record._max_temp_c for record in self._weather_records]
        min_temp = [record._min_temp_c for record in self._weather_records]
        avg_mean_humidity = [record._mean_humidity for record in self._weather_records]
        self._calculation_results["Avg_highest_temp"] = int(sum(max_temp) / len(max_temp))
        self._calculation_results["Avg_lowest_temp"] = int(sum(min_temp) / len(min_temp))
        self._calculation_results["Avg_mean_humidity"] = int(sum(avg_mean_humidity) / len(avg_mean_humidity))
        return self._calculation_results											   

    def calculate_hghst_lwst_temp_day(self):
        self._calculation_results["Highest_temp_record"] = [record._max_temp_c for record in self._weather_records]
        self._calculation_results["Lowest_temp_record"] = [record._min_temp_c for record in self._weather_records]
        return self._calculation_results


class ReportGenerator:
    def report_for_hghst_lwst_temp_hmidity(self, weather_records):
        readings_calculator = Calculations(weather_records)
        results = readings_calculator.calculate_hghst_lwst_temp_hmidity()
        print("Highest: " + str(results["Highest_temp_day"]._max_temp_c) + "C on", self.convert_date(results["Highest_temp_day"]._PKT))
        print("Lowest: " + str(results["Lowest_temp_day"]._min_temp_c) + "C on", self.convert_date(results["Lowest_temp_day"]._PKT))
        print("Humidity: " + str(results["Max_humidity_day"]._max_humidity) + r"% on", self.convert_date(results["Max_humidity_day"]._PKT))

    def convert_date(self, date):
        return date.strftime("%B %d")

    def report_for_avg_temp_humidity(self, weather_records):
        readings_calculator = Calculations(weather_records)
        results = readings_calculator.calculate_avg_temp_humidity()
        print("Highest Average: " + str(results["Avg_highest_temp"]) + "C")
        print("Lowest Average: " + str(results["Avg_lowest_temp"]) + "C")
        print("Average Mean Humidity: " + str(results["Avg_mean_humidity"]) + r"%")	

    def report_for_hghst_lwst_temp_day(self, weather_records, date):
        readings_calculator = Calculations(weather_records)
        results = readings_calculator.calculate_hghst_lwst_temp_day()
        count = 1
        print(date)
        for record_high, record_low in zip(results["Highest_temp_record"], results["Lowest_temp_record"]): 
            print(count, '+' * int(record_high))
            print(count, '+' * int(record_low))
            count = count + 1


def validate_year_for_temp_and_humidity(year):
    try:
        return datetime.strptime(year, "%Y").strftime("%Y")
    except ValueError:	
        print("Invalid year entered")

def validate_date_for_avg_temp_hmdty_and_charts(date):
    try:
        return datetime.strptime(date, "%Y/%m").strftime("%Y_%b")
    except ValueError:	
        print("Invalid date entered")	

def validate_directory_path(dir_path):
    if not os.path.isdir(dir_path):		
        print("Directory does not exist !")
    return dir_path	

def main():	
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help ="Path to directory", type=str)
    parser.add_argument("-e", help="Prompt an year for highest and lowest temperature, humidity", type=validate_year_for_temp_and_humidity)
    parser.add_argument("-a", help="Prompt a date for average temperature, humidity", type=validate_date_for_avg_temp_hmdty_and_charts)
    parser.add_argument("-c", help="Prompt a date to display bar charts for highest and lowest temperature", type=validate_date_for_avg_temp_hmdty_and_charts)
    args = parser.parse_args()

    report = ReportGenerator()
    file_parser = FileParser(args.path)
    parsed_readings = file_parser.parse_file()
    if args.e:
        if parsed_readings is not None:
            filtered_readings = file_parser.filter_weather_records(args.e) 
            report.report_for_hghst_lwst_temp_hmidity(filtered_readings)
    if args.a:
        if parsed_readings is not None:
            filtered_readings = file_parser.filter_weather_records(args.a)
            report.report_for_avg_temp_humidity(filtered_readings)   
    if args.c:
        if parsed_readings is not None:
            filtered_readings = file_parser.filter_weather_records(args.c)
            date_to_display = datetime.strptime(args.c, "%Y_%b").strftime("%B %Y")
            report.report_for_hghst_lwst_temp_day(filtered_readings, date_to_display)
main()
