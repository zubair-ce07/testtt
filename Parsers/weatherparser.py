import csv
import datetime
from os import listdir
from pathlib import Path
from os.path import isfile, join

from Weathers.dailyweather import DailyWeather


class WeatherParser:
    @staticmethod
    def parse_year(dir_path, date):

        if not WeatherParser.file_exists(dir_path):
            return
        files_to_process = WeatherParser.file_list(dir_path, str(date.year))

        return WeatherParser.parse_files(files_to_process)

    @staticmethod
    def parse_month(dir_path, date):
        if not WeatherParser.file_exists(dir_path):
            return

        month_name = "_" + date.strftime('%b')
        sub_name = str(date.year) + month_name

        files_to_process = WeatherParser.file_list(dir_path, sub_name)

        return WeatherParser.parse_files(files_to_process)

    @staticmethod
    def parse_files(files_to_process):
        weather_list = []
        for file in files_to_process:
            input_file = csv.DictReader(open(file))
            for row in input_file:
                date = datetime.datetime.strptime(row.get("PKT"), '%Y-%m-%d').date()
                weather_list.append(WeatherParser.create_daily_weather(date, row))
        return weather_list

    @staticmethod
    def file_exists(dir_path):
        dir_exist = True
        path = Path(dir_path)
        if not path.is_dir():
            print("Directory doesn't exist")
            dir_exist = False
        return dir_exist

    @staticmethod
    def create_daily_weather(day, row):

        max_temp = None
        mean_temp = None
        min_temp = None
        max_humidity = None
        mean_humidity = None
        min_humidity = None

        if row.get("Max TemperatureC"):
            max_temp = int(row.get("Max TemperatureC"))
        if row.get("Mean TemperatureC"):
            mean_temp = int(row.get("Mean TemperatureC"))
        if row.get("Min TemperatureC"):
            min_temp = int(row.get("Min TemperatureC"))
        if row.get("Max Humidity"):
            max_humidity = int(row.get("Max Humidity"))
        if row.get(" Mean Humidity"):
            mean_humidity = int(row.get(" Mean Humidity"))
        if row.get(" Min Humidity"):
            min_humidity = int(row.get(" Min Humidity"))

        daily_weather = DailyWeather(
            day, max_temp, mean_temp, min_temp, max_humidity, mean_humidity, min_humidity)
        return daily_weather

    @staticmethod
    def file_list(dir_path, file_filter):
        files_to_process = [join(dir_path, f) for f in listdir(
            dir_path) if isfile(join(dir_path, f)) and file_filter in f]
        return files_to_process
