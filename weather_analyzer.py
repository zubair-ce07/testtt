import os
import re
import csv

from day_weather import DayWeather
from constant import Constant


class WeatherAnalyzer:
    def __init__(self):
        self.day_weather_list = []

    def collect_files(self, files_path):
        """collects all datasets files"""
        list_of_files = []
        for file_name in os.listdir(files_path):
            if not file_name.startswith('.'):
                list_of_files.append(files_path + file_name)
        return list_of_files

    def read_file_data(self, file_path):
        """Reads and return file data"""
        try:
            file_data = []
            with open(file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    file_data.append(row)
            return file_data
        except IOError:
            print("Error: can\'t find file or read data")
            exit()

    def read_files(self, files_path):
        """collects all the data set of and saves in data structure"""
        list_of_files = self.collect_files(files_path)
        for file in list_of_files:
            file_data = self.read_file_data(file)
            for day_data in file_data:
                if len(day_data) > 2:
                    if self.check_valid_record_row(day_data) and \
                            day_data["Max TemperatureC"] and \
                            day_data["Min TemperatureC"] and \
                            day_data["Max Humidity"]:
                        self.day_weather_list.append(DayWeather(
                            self.get_day_date(day_data),
                            day_data["Max TemperatureC"],
                            day_data["Mean TemperatureC"],
                            day_data["Min TemperatureC"],
                            day_data["Dew PointC"], day_data["MeanDew PointC"],
                            day_data["Min DewpointC"],
                            day_data["Max Humidity"],
                            day_data[" Mean Humidity"],
                            day_data[" Min Humidity"],
                            day_data[" Max Sea Level PressurehPa"],
                            day_data[" Mean Sea Level PressurehPa"],
                            day_data[" Min Sea Level PressurehPa"],
                            day_data[" Max VisibilityKm"],
                            day_data[" Mean VisibilityKm"],
                            day_data[" Min VisibilitykM"],
                            day_data[" Max Wind SpeedKm/h"],
                            day_data[" Mean Wind SpeedKm/h"],
                            day_data[" Max Gust SpeedKm/h"],
                            day_data["Precipitationmm"],
                            day_data[" CloudCover"], day_data[" Events"],
                            day_data["WindDirDegrees"]
                        ))

    def collect_month_data(self, year_month):
        month_data_list = []
        for day_data in self.day_weather_list:
            if self.check_valid_year_month_file(day_data.pkt, year_month):
                month_data_list.append(day_data)
        return month_data_list

    def extract_year_data(self, year):
        year_data_list = []
        for day_data in self.day_weather_list:
            if self.check_valid_year_file(day_data.pkt, year):
                year_data_list.append(day_data)
        temp_max_obj = max(year_data_list,
                           key=lambda day_data: int(day_data.max_temperature))
        temp_min_obj = min(year_data_list,
                           key=lambda day_data: int(day_data.min_temperature))
        max_humid_obj = max(year_data_list,
                            key=lambda day_data: int(day_data.max_humidity))
        return temp_max_obj, temp_min_obj, max_humid_obj

    def check_valid_year_file(self, day_date, year):
        match = re.search(r'\d{4}', day_date)
        return match and (year in day_date)

    def compute_month_data_average(self, month_data_list):
        max_temp_avg = 0
        min_temp_avg = 0
        humidity_avg = 0
        count_max_temp = 0
        count_min_temp = 0
        count_humidty = 0
        for day_data in month_data_list:
            if day_data.max_temperature:
                max_temp_avg += int(day_data.max_temperature)
                count_max_temp += 1
            if day_data.min_temperature:
                min_temp_avg += int(day_data.min_temperature)
                count_min_temp += 1
            if day_data.max_humidity:
                humidity_avg += int(day_data.max_humidity)
                count_humidty += 1
        if count_max_temp == 0:
            return Constant.NULL_VALUE.value, Constant.NULL_VALUE.value, \
                   Constant.NULL_VALUE.value
        return (max_temp_avg / count_max_temp,
                min_temp_avg / count_min_temp,
                humidity_avg / count_humidty)

    def check_valid_year_month_file(self, day_date, year_month):
        match = re.search(r'\d{4}', day_date)
        if match:
            day_date_list = day_date.split("-")
            year_month_list = year_month.split("/")
            return day_date_list[0] == year_month_list[0] and day_date_list[
                1] == year_month_list[1]
        return False

    def get_day_date(self, day_obj):
        if day_obj.get("PKT"):
            return day_obj["PKT"]
        return day_obj["PKST"]

    def check_valid_record_row(self, day_obj):
        if day_obj.get("PKT") != "PKT" or day_obj.get("PKST") != "PKST":
            return True
        return False
