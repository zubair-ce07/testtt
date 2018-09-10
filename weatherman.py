
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
                        record = WeatherRecord() #store single reading 
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

        if (self._readings):
            return self._readings
        else:
            print("No weather files exist in this directory or wrong file name entered")
            return None

    def filter_weather_records(self, year):
        filtered_readings = []
        for reading in self._readings:
            if year in reading._file_weather_record:
                filtered_readings.append(reading)
        return filtered_readings		


class Calculations:
    def __init__(self, _weather_records):
        self._weather_records = _weather_records
        self._calculation_results = {} 
        self._max_temps = [record._max_temp_c for record in self._weather_records]
        self._min_temps = [record._min_temp_c for record in self._weather_records]
        self._avg_mean_humidity = [record._mean_humidity for record in self._weather_records]

    def calculate_hghst_lwst_temp_hmidity(self):
        #Highest temperature and day
        self._calculation_results["Highest_temp"] = max(self._max_temps)
        self._calculation_results["Highest_temp_day(s)"] = [record._PKT for record in self._weather_records if
                                                            record._max_temp_c == self._calculation_results["Highest_temp"]]
        #Lowest temperature and day
        self._calculation_results["Lowest_temp"] = min(self._min_temps)
        self._calculation_results["Lowest_temp_day(s)"] = [record._PKT for record in self._weather_records if
                                                           record._min_temp_c == self._calculation_results["Lowest_temp"]]
        #Most humidity and day
        self._calculation_results["Max_humidity"] = max(record._max_humidity for record in self._weather_records)
        self._calculation_results["Max_humidity_day(s)"] = [record._PKT for record in self._weather_records if 
                                                            record._max_humidity == self._calculation_results["Max_humidity"]]
        return self._calculation_results

    def calculate_avg_temp_humidity(self):
        #Average highest temperature
        self._calculation_results["Avg_highest_temp"] = int(sum(self._max_temps) / len(self._max_temps))
        #Average lowest temperature
        self._calculation_results["Avg_lowest_temp"] = int(sum(self._min_temps) / len(self._min_temps))
        #Average Mean Humidity
        self._calculation_results["Avg_mean_humidity"] = int(sum(self._avg_mean_humidity) / len(self._avg_mean_humidity))
        return self._calculation_results											   

    def calculate_hghst_lwst_temp_day(self):
        #List of Highest Temperature on each day
        self._calculation_results["Highest_temp_record"] = self._max_temps
        #List of Lowest Temperatures on each day
        self._calculation_results["Lowest_temp_record"] = self._min_temps
        return self._calculation_results


class ReportGenerator:
    def report_for_hghst_lwst_temp_hmidity(self, weather_records):
        readings_calculator = Calculations(weather_records)
        results = readings_calculator.calculate_hghst_lwst_temp_hmidity()

        print("Highest: " + str(results["Highest_temp"]) + "C on ", end='')
        print(','.join(str(x) for x in self.convert_date(results["Highest_temp_day(s)"])))

        print("Lowest: " + str(results["Lowest_temp"]) + "C on ", end='')
        print(','.join(str(x) for x in self.convert_date(results["Lowest_temp_day(s)"])))

        print("Humidity: " + str(results["Max_humidity"]) + r"% on ", end='')
        print(','.join(str(x) for x in self.convert_date(results["Max_humidity_day(s)"])))

    def convert_date(self, dates):
        formatted_dates = []
        for date in dates:
            formatted_dates.append(date.strftime("%B")+ " "+ date.strftime("%d"))
        return formatted_dates

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


def validate_year_for_temp_and_humidity(command_e):
    try:
        datetime.strptime(command_e, "%Y").strftime("%Y")
        return command_e
    except ValueError:	
        print("Invalid year entered")

def validate_date_for_avg_temp_hmdty_and_charts(command_a_c):
    try:
        datetime.strptime(command_a_c, "%Y/%m").strftime("%Y_%b")
        return command_a_c
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
        year = datetime.strptime(args.e, "%Y").strftime("%Y")
        if parsed_readings is not None:
            filtered_readings = file_parser.filter_weather_records(year)
            report.report_for_hghst_lwst_temp_hmidity(filtered_readings)
    if args.a:
        year_month = datetime.strptime(args.a, "%Y/%m").strftime("%Y_%b")
        if parsed_readings is not None:
            filtered_readings = file_parser.filter_weather_records(year_month)
            report.report_for_avg_temp_humidity(filtered_readings)   
    if args.c:
        year_month = datetime.strptime(args.c, "%Y/%m").strftime("%Y_%b")
        if parsed_readings is not None:
            filtered_readings = file_parser.filter_weather_records(year_month)
            date_to_display = datetime.strptime(args.c, "%Y/%m").strftime("%B %Y")
            report.report_for_hghst_lwst_temp_day(filtered_readings, date_to_display)
main()
