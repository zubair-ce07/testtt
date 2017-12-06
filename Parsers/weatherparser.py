import re
from os import listdir
from pathlib import Path
from os.path import isfile, join

from Weathers.yearlyweather import YearlyWeather
from Weathers.monthlyweather import MonthlyWeather
from Weathers.dailyweather import DailyWeather


class WeatherParser:
    line_format = re.compile('''(?P<year>.*?)-(?P<month>.*?)-(?P<day>.*?),
                                (?P<maxTemp>.*?),(?P<meanTemp>.*?),
                                (?P<minTemp>.*?),(?P<maxDew>.*?),(?P<meanDew>.*?),
                                (?P<minDew>.*?),(?P<maxHumidity>.*?),
                                (?P<meanHumidity>.*?),(?P<minHumidity>.*?),''', re.IGNORECASE | re.VERBOSE)
    weather_list = []

    def parse(self, dir_path, year, month=-1):

        cached = self._get_cached_result(year, month)
        if cached is not None:
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
        with open(file) as open_file_object:
            for line in open_file_object:
                matches = re.finditer(self.line_format, line)

                for matchNum, match in enumerate(matches):

                    groups = match.groupdict()
                    yearly_weathers = [
                        weather for weather
                        in self.weather_list
                        if weather.year == groups["year"]]
                    if len(yearly_weathers) == 0:
                        yearly_weather = YearlyWeather(groups["year"])
                        monthly_weather = MonthlyWeather(int(groups["month"]))
                        monthly_weather.add_daily_weather(
                            self._create_daily_weather(groups))
                        yearly_weather.monthly_weathers.append(monthly_weather)
                        self.weather_list.append(yearly_weather)
                    else:
                        yearly_weather = yearly_weathers[0]
                        monthly_weathers = [
                            weather for weather
                            in yearly_weather.monthly_weathers
                            if weather.month == int(groups["month"])]
                        if len(monthly_weathers) == 0:
                            monthly_weather = MonthlyWeather(
                                int(groups["month"]))
                            monthly_weather.add_daily_weather(
                                self._create_daily_weather(groups))
                            yearly_weather.monthly_weathers.append(
                                monthly_weather)
                        else:
                            monthly_weather = monthly_weathers[0]
                            monthly_weather.add_daily_weather(
                                self._create_daily_weather(groups))

    def _create_daily_weather(self, parsed_dictionary):
        daily_weather = DailyWeather()
        daily_weather.day = parsed_dictionary["day"]
        max_temp = int(parsed_dictionary["maxTemp"]) if parsed_dictionary[
            "maxTemp"] != '' else -100
        mean_temp = int(parsed_dictionary["meanTemp"])if parsed_dictionary[
            "meanTemp"] != '' else 0
        min_temp = int(parsed_dictionary["minTemp"]) if parsed_dictionary[
            "minTemp"] != '' else 100
        max_humidity = int(parsed_dictionary["maxHumidity"]) if parsed_dictionary[
            "maxHumidity"] != '' else 0
        mean_humidity = int(parsed_dictionary["meanHumidity"]) if parsed_dictionary[
            "meanHumidity"] != '' else 50
        min_humidity = int(parsed_dictionary["minHumidity"]) if parsed_dictionary[
            "minHumidity"] != '' else 100

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
