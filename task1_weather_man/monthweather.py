import csv
import os
from datetime import datetime

import utils
from dailyweathermodel import DailyWeatherModel


class MonthWeatherModel:
    def __init__(self, file_name):
        self.daily_weather_info = []
        self.populate_model(file_name)

    def populate_model(self, file_name):
        file_path = os.path.join(utils.WEATHER_FILES_PATH, file_name)
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for line in reader:
                current_day_weather = DailyWeatherModel(datetime.strptime(line.get("PKT"), "%Y-%m-%d"),
                                                        int(line.get("Max TemperatureC") or 0),
                                                        int(line.get("Min TemperatureC") or 0),
                                                        int(line.get("Max Humidity") or 0),
                                                        int(line.get(" Mean Humidity") or 0))
                self.daily_weather_info.append(current_day_weather)
