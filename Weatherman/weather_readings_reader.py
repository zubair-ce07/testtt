from os import listdir
from os.path import isfile, join
import csv
import calendar
import re

import weather_day_reading
from report_generator import ReportGenerator


class WeatherReadingsReader:

    def __init__(self, args):
        my_path = args.directory
        if args.type_e:
            weather_readings = WeatherReadingsReader.read_readings(my_path, args.type_e)
            if weather_readings:
                ReportGenerator.get_annual_report(weather_readings)
            else:
                ReportGenerator.no_data_found(year=args.type_e)
        if args.type_a:
            year, month_name = WeatherReadingsReader.month_argument_reader(args.type_a)
            weather_readings = WeatherReadingsReader.read_readings(
                my_path, year, month_name)
            if weather_readings:
                ReportGenerator.get_month_report(month_name, year, weather_readings)
            else:
                ReportGenerator.no_data_found(year, month_name)
        if args.type_c:
            year, month_name = WeatherReadingsReader.month_argument_reader(args.type_c)
            weather_readings = WeatherReadingsReader.read_readings(
                my_path, year, month_name)
            if weather_readings:
                ReportGenerator.get_bar_report('c', args.type_c, weather_readings)
            else:
                ReportGenerator.no_data_found(year, month_name)
        if args.type_d:
            year, month_name = WeatherReadingsReader.month_argument_reader(args.type_d)
            weather_readings = WeatherReadingsReader.read_readings(
                my_path, year, month_name)
            if weather_readings:
                ReportGenerator.get_bar_report('d', args.type_d, weather_readings)
            else:
                ReportGenerator.no_data_found(year, month_name)

    @staticmethod
    def month_argument_reader(argument):
        year, month = argument.split('/')
        return int(year), calendar.month_abbr[int(month)]

    @staticmethod
    def read_day_reading(reading):
        reading = {k.strip(): v for k, v in reading.items()}
        day_reading = weather_day_reading.WeatherReading(reading)
        return day_reading

    @staticmethod
    def validate_day_reading(reading):
        reading = {k.strip(): v for k, v in reading.items()}
        required_fields = ['Mean TemperatureC', 'Min TemperatureC', 'Max TemperatureC',
                           'Mean Humidity', 'Max Humidity', 'Min Humidity']
        return all(reading.get(f) for f in required_fields)

    @staticmethod
    def read_file(path):
        weather_readings = []
        month_file = csv.DictReader(open(path))
        for reading in month_file:
            if WeatherReadingsReader.validate_day_reading(reading):
                weather_readings.append(WeatherReadingsReader.read_day_reading(reading))
        return weather_readings

    @staticmethod
    def get_weather_files(directory):
        return [f for f in listdir(directory) if isfile(join(directory, f))]

    @staticmethod
    def file_needs_to_be_read(file_name, year, month):
        regex = '.*' + str(year) + '_' + month + '.txt'
        return bool(re.match(regex, file_name))

    @staticmethod
    def read_readings(dir_path, year, month='.*'):
        weather_readings = []
        file_names = WeatherReadingsReader.get_weather_files(dir_path)
        for file_name in file_names:
            if WeatherReadingsReader.file_needs_to_be_read(file_name, year, month):
                    weather_readings += WeatherReadingsReader.read_file(join(dir_path, file_name))
        return weather_readings
