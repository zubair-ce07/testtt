import re
import csv
from os import listdir
from pathlib import Path
from os.path import isfile, join

from Weathers.yearlyweather import YearlyWeather
from Weathers.monthlyweather import MonthlyWeather
from Weathers.dailyweather import DailyWeather


class WeatherParser:
    weather_list = []

    def parse(self, dir_path, year, month=-1):

        cached = self._get_cached_result(year, month)
        if cached:
            return cached

        self._parse_files(dir_path, year, month)

        parsed = self._get_cached_result(year, month)

        return parsed

    def _parse_files(self, dir_path, year, month):
        path = Path(dir_path)
        if not path.is_dir():
            print("Directory doesn't exist")
            return
        month_name = ''
        if month != -1:
            month_names = ["Jan", "Feb", "Mar", "Apr", "May",
                           "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            month_name = "_" + month_names[month-1]
        sub_name = year + month_name
        files_to_process = [join(dir_path, f) for f in listdir(
            dir_path) if isfile(join(dir_path, f)) and sub_name in f]
        for file in files_to_process:
            self._parse(file)

    def _parse(self, file):
        input_file = csv.DictReader(open(file))
        for row in input_file:
            dateSplit = row["PKT"].split('-')
            yearly_weathers = [
                    weather for weather
                    in self.weather_list
                    if weather.year == dateSplit[0]]
            if len(yearly_weathers) == 0:
                    yearly_weather = YearlyWeather(dateSplit[0])
                    monthly_weather = MonthlyWeather(int(dateSplit[1]))
                    monthly_weather.add_daily_weather(
                        self._create_daily_weather(dateSplit[2], row))
                    yearly_weather.monthly_weathers.append(monthly_weather)
                    self.weather_list.append(yearly_weather)
            else:
                yearly_weather = yearly_weathers[0]
                monthly_weathers = [
                    weather for weather
                    in yearly_weather.monthly_weathers
                    if weather.month == int(dateSplit[1])]
                if len(monthly_weathers) == 0:
                    monthly_weather = MonthlyWeather(
                        int(dateSplit[1]))
                    monthly_weather.add_daily_weather(
                        self._create_daily_weather(dateSplit[2], row))
                    yearly_weather.monthly_weathers.append(
                        monthly_weather)
                else:
                    monthly_weather = monthly_weathers[0]
                    monthly_weather.add_daily_weather(self._create_daily_weather(dateSplit[2], row))

    def _create_daily_weather(self, day, row):
        daily_weather = DailyWeather()
        daily_weather.day = day
        max_temp = int(row["Max TemperatureC"]) if row[
            "Max TemperatureC"] != '' else -100
        mean_temp = int(row["Mean TemperatureC"])if row[
            "Mean TemperatureC"] != '' else 0
        min_temp = int(row["Min TemperatureC"]) if row[
            "Min TemperatureC"] != '' else 100
        max_humidity = int(row["Max Humidity"]) if row[
            "Max Humidity"] != '' else 0
        mean_humidity = int(row[" Mean Humidity"]) if row[
            " Mean Humidity"] != '' else 50
        min_humidity = int(row[" Min Humidity"]) if row[
            " Min Humidity"] != '' else 100

        daily_weather.highest_temperature = max_temp
        daily_weather.mean_temperature = mean_temp
        daily_weather.lowest_temperature = min_temp
        daily_weather.max_humidity = max_humidity
        daily_weather.mean_humidity = mean_humidity
        daily_weather.min_humidity = min_humidity
        return daily_weather

    def _get_cached_result(self, year, month):
        yearly_weathers = [
            weather for weather in self.weather_list if weather.year == year]
        if len(yearly_weathers) == 1:
            if month == -1:
                weathers = [
                    weather for weather
                    in yearly_weathers
                    if weather.is_complete]
            else:
                weathers = yearly_weathers[0].get_month(month)
            if len(weathers) == 1:
                return weathers[0]
        return None
