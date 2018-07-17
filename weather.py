import datetime
import csv
import os


class FileParser:
    @staticmethod
    def get_files(directory_path):
        file_names = os.listdir(directory_path)
        file_paths = [os.path.join(directory_path, file_name) for file_name in file_names if
                      'weather' in file_name and not file_name.startswith('.')]
        return [file_path for file_path in file_paths if os.path.isfile(file_path)]

    def read(self, file_names):
        weather_readings = []

        for file_name in file_names:
            with open(file_name, 'r') as f:
                weather_file_readings = csv.DictReader(f)
                weather_readings += [WeatherReading(r) for r in weather_file_readings
                                     if self.is_valid_reading(r)]

        return weather_readings

    @staticmethod
    def is_valid_reading(reading):
        required_fields = ['Max TemperatureC', 'Min TemperatureC', 'Max Humidity', ' Mean Humidity']
        return all(reading[field] for field in required_fields)


class WeatherReading:
    def __init__(self, weather_reading):
        self.date = self.str_to_date(weather_reading.get('PKST') or weather_reading.get('PKT'))
        self.max_temp = int(weather_reading['Max TemperatureC'])
        self.min_temp = int(weather_reading['Min TemperatureC'])
        self.mean_humidity = int(weather_reading[' Mean Humidity'])
        self.max_humidity = int(weather_reading['Max Humidity'])

    @staticmethod
    def str_to_date(string):
        date = string.split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))


class WeatherAnalyzer:
    @staticmethod
    def filter_readings_by_date(weather_readings, year, month=None):
        year = int(year)
        if not month:
            return [r for r in weather_readings if r.date.year == year]

        month = int(month)
        return [r for r in weather_readings if r.date.year == year
                and r.date.month == month]

    def calculate_annual_result(self, weather_readings, year):
        weather_readings = self.filter_readings_by_date(weather_readings, year)

        if not weather_readings:
            return {}

        result = {
            'Lowest Annual Temp':
                self.find_lowest_temp(weather_readings),
            'Highest Annual Temp':
                self.find_highest_temp(weather_readings),
            'Highest Annual Humidity':
                self.find_highest_humidity(weather_readings)
        }
        return result

    @staticmethod
    def find_highest_temp(weather_readings):
        return max(weather_readings, key=lambda r: r.max_temp)

    @staticmethod
    def find_highest_humidity(weather_readings):
        return max(weather_readings, key=lambda r: r.max_humidity)

    @staticmethod
    def find_lowest_temp(weather_readings):
        return min(weather_readings, key=lambda r: r.min_temp)

    def calculate_monthly_average_report(self, weather_readings, year, month):
        result = {}
        weather_readings = self.filter_readings_by_date(weather_readings, year, month)

        if not weather_readings:
            return {}

        total_readings = len(weather_readings)
        result['Average Highest Temp'] = sum(
            (r.max_temp for r in weather_readings)) / total_readings
        result['Average Lowest Temp'] = sum(
            (r.min_temp for r in weather_readings)) / total_readings
        result['Average Mean Humidity'] = sum(
            (r.mean_humidity for r in weather_readings)) / total_readings

        return result

    def calculate_daily_extremes_report(self, weather_readings, year, month):
        weather_readings = self.filter_readings_by_date(weather_readings, year, month)
        if not weather_readings:
            return {}

        return weather_readings


class WeatherDisplay:
    @staticmethod
    def present_annual_report(report):
        if not report:
            print('Invalid data or input')
            return

        high = report['Highest Annual Temp']
        low = report['Lowest Annual Temp']
        humid = report['Highest Annual Humidity']

        print("Highest: {0}C on {1}".format(
            high.max_temp, high.date.strftime("%d %B")))
        print("Lowest: {0}C on {1}".format(
            low.min_temp, low.date.strftime("%d %B")))
        print("Humidity: {0}% on {1}\n".format(
            humid.max_humidity, humid.date.strftime("%d %B")))

    @staticmethod
    def present_monthly_average_report(report):
        if not report:
            print('Invalid data or input')
            return

        print('Highest Average: {0}C'.format(
            round(report['Average Highest Temp'])))
        print('Lowest Average: {0}C'.format(
            round(report['Average Lowest Temp'])))
        print('Average Mean Humidity: {0}%\n'.format(
            round(report['Average Mean Humidity'])))

    @staticmethod
    def present_daily_extremes_report(report, horizontal=False):
        if not report:
            print('Invalid data or input')
            return

        print(report[0].date.strftime('%B %Y'))

        for reading in report:
            low = '+' * abs(reading.min_temp)
            high = '+' * abs(reading.max_temp)

            if not horizontal:
                print(u"{0} \u001b[34m{1}\u001b[0m {2}C".format(
                    reading.date.strftime('%d'), high, reading.max_temp))
                print(u"{0} \u001b[31m{1}\u001b[0m {2}C".format(
                    reading.date.strftime('%d'), low, reading.min_temp))
            else:
                print((("{0} \u001b[31m{1}\u001b[0m\u001b[34m{2}"
                        "\u001b[0m {3}C-{4}C")).format(
                    reading.date.strftime('%d'), low, high, reading.min_temp, reading.max_temp))

        print()
