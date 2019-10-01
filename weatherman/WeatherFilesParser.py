import calendar
import glob
import csv
from temperatureResults import WeatherReading


class WeatherFilesParser:
    def parse_files(self, path, year):
        weather_readings = []
        complete_path = self.get_full_path(path, year)
        self.check_valid_path_name(complete_path)
        for temp_file_of_month in glob.glob(complete_path + "*"):
            temperature_file = open(temp_file_of_month)
            temperature_file_reader = csv.DictReader(temperature_file)
            for day in temperature_file_reader:
                weather_readings += [self.validate_weather_readings(day)]
        return list(filter(None.__ne__, weather_readings))

    def validate_weather_readings(self, weather_reading):
        if weather_reading['Max TemperatureC'] and weather_reading['Min TemperatureC'] and \
                weather_reading['Max Humidity'] and weather_reading[' Mean Humidity']:
            return WeatherReading(weather_reading)

    def get_full_path(self, path, year):
        complete_path = ""
        if len(year.split('/')) > 1:
            complete_path = path + "/Murree_weather_" + year.split('/')[0] + "_" + \
                            calendar.month_abbr[int(year.split('/')[1])]
        else:
            complete_path = path + "/Murree_weather_" + year
        return complete_path

    def check_valid_path_name(self, complete_path):
        if len(glob.glob(complete_path + "*")) <= 0:
            print(f"No File for specified year/month")
            print(f"please provide valid input")
            exit()
