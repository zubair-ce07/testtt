import csv
import datetime
from os import listdir
from pathlib import Path
from os.path import isfile, join

from Weathers.yearlyweather import YearlyWeather
from Weathers.monthlyweather import MonthlyWeather
from Weathers.dailyweather import DailyWeather


class WeatherParser:
    weather_list = []

    def parse(self, dir_path, date, parse_for_year = False):

        cached = self._cached_result(date, parse_for_year)
        if cached:
            return cached

        self._parse_files(dir_path, date, parse_for_year)

        parsed = self._cached_result(date, parse_for_year)

        return parsed

    def _parse_files(self, dir_path, date, parse_for_year):
        path = Path(dir_path)
        if not path.is_dir():
            print("Directory doesn't exist")
            return
        month_name = ''
        if not parse_for_year:
            month_name = "_" + date.strftime('%b')
        sub_name = str(date.year) + month_name
        files_to_process = [join(dir_path, f) for f in listdir(
            dir_path) if isfile(join(dir_path, f)) and sub_name in f]
        yearly_weathers = [
            weather for weather
            in self.weather_list
            if weather.year == date.year]

        if len(yearly_weathers) == 0:
            yearly_weather = YearlyWeather(date.year)
        else:
            yearly_weather=yearly_weathers[0]

        for file in files_to_process:
            yearly_weather.add_monthly_weather(self._parse(file))

        self.weather_list.append(yearly_weather)

    def _parse(self, file):
        monthly_weather=None
        input_file = csv.DictReader(open(file))
        for row in input_file:
            date = datetime.datetime.strptime(row.get("PKT"), '%Y-%m-%d').date()
            if monthly_weather is None:
                monthly_weather = MonthlyWeather(date)

            monthly_weather.add_daily_weather(
                    self._create_daily_weather(date, row))

        return monthly_weather

    def _create_daily_weather(self, day, row):

        max_temp = int(row.get("Max TemperatureC")) if row.get(
            "Max TemperatureC") != '' else None
        mean_temp = int(row.get("Mean TemperatureC"))if row.get(
            "Mean TemperatureC") != '' else None
        min_temp = int(row.get("Min TemperatureC")) if row.get(
            "Min TemperatureC") != '' else None
        max_humidity = int(row.get("Max Humidity")) if row.get(
            "Max Humidity") != '' else None
        mean_humidity = int(row.get(" Mean Humidity")) if row.get(
            " Mean Humidity") != '' else None
        min_humidity = int(row.get(" Min Humidity")) if row.get(
            " Min Humidity") != '' else None

        daily_weather = DailyWeather(
            day, max_temp, mean_temp, min_temp, max_humidity, mean_humidity, min_humidity)
        return daily_weather

    def _cached_result(self, date, parse_for_year):
        yearly_weathers = [
            weather for weather in self.weather_list if weather.year ==date.year]
        if len(yearly_weathers) == 1:
            if parse_for_year and yearly_weathers[0].is_complete():
                weathers = yearly_weathers
            else:
                weathers = yearly_weathers[0].get_month(date.month)
            if len(weathers) == 1:
                return weathers[0]
        return None
