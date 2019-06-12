import os
import re
import csv

from day_weather import DayWeather


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
                csv_reader = csv.reader(csv_file, delimiter=',')
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
                    if day_data[0] != "PKT" and day_data[0] != "PKST" and day_data[1] and day_data[3] \
                            and day_data[8]:
                        self.day_weather_list.append(DayWeather(
                            day_data[0], day_data[1],
                            day_data[2], day_data[3],
                            day_data[4], day_data[5],
                            day_data[6], day_data[7],
                            day_data[8], day_data[9],
                            day_data[10], day_data[11],
                            day_data[12], day_data[13],
                            day_data[14], day_data[15],
                            day_data[16], day_data[17],
                            day_data[18], day_data[19],
                            day_data[20], day_data[21],
                            day_data[22]
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
        max_humid_obj = min(year_data_list,
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
