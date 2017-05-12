import csv
from datetime import datetime

import utils
from dailyweathermodel import DailyWeatherModel


class MonthWeatherModel:
    def __init__(self, file_name):
        self.daily_weather_info = []
        self.populate_model(file_name)

    def populate_model(self, file_name):
        file_path = utils.WEATHER_FOLDER_NAME + file_name
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            for line in reader:
                current_day_weather = DailyWeatherModel(datetime.strptime(line.get("PKT"), "%Y-%m-%d"),
                                                        int(line.get("Max TemperatureC") or 0),
                                                        int(line.get("Min TemperatureC") or 0),
                                                        int(line.get("Max Humidity") or 0),
                                                        int(line.get(" Mean Humidity") or 0))
                self.daily_weather_info.append(current_day_weather)
        f.close()
