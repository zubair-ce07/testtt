import datetime
import csv
import os


def str_to_date(string):
    date = string.split('-')
    return datetime.date(int(date[0]), int(date[1]), int(date[2]))


def filter_by_date(weather_readings, year, month=''):
    if not month:
        return [r for r in weather_readings if r.date.year == int(year)]
    else:
        return [r for r in weather_readings if r.date.year == int(year)
                and r.date.month == int(month)]


class FileParser:
    @staticmethod
    def get_files(directory_path):
        file_names = os.listdir(directory_path)
        file_names = [os.path.join(directory_path, file_name) for file_name in file_names]
        return [x for x in file_names if
                os.path.isfile(x) and 'weather' in x and not x.startswith('.')]

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
        required_fields = ['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC',
                           'Max Humidity', ' Mean Humidity', ' Min Humidity']

        return all(reading[field] for field in required_fields)


class WeatherReading:
    def __init__(self, weather_reading):
        if 'PKT' in weather_reading.keys():
            self.date = str_to_date(weather_reading['PKT'])
        else:
            self.date = str_to_date(weather_reading['PKST'])
        self.max_temp = int(weather_reading['Max TemperatureC'])
        self.min_temp = int(weather_reading['Min TemperatureC'])
        self.mean_humidity = int(weather_reading[' Mean Humidity'])
        self.max_humidity = int(weather_reading['Max Humidity'])


class Calculator:
    def calculate_annual_result(self, weather_readings, year):
        result = {
            'Lowest Annual Temp':
                self.find_annual_lowest_temp(weather_readings, year),
            'Highest Annual Temp':
                self.find_annual_highest_temp(weather_readings, year),
            'Highest Annual Humidity':
                self.find_annual_highest_humidity(weather_readings, year)
        }
        return result

    @staticmethod
    def find_annual_highest_temp(weather_readings, year):
        weather_readings = filter_by_date(weather_readings, year)
        if not weather_readings:
            return {}

        return max(weather_readings, key=lambda r: r.max_temp)

    @staticmethod
    def find_annual_highest_humidity(weather_readings, year):
        weather_readings = filter_by_date(weather_readings, year)
        if not weather_readings:
            return {}

        return max(weather_readings, key=lambda r: r.max_humidity)

    @staticmethod
    def find_annual_lowest_temp(weather_readings, year):
        weather_readings = filter_by_date(weather_readings, year)
        if not weather_readings:
            return {}

        return min(weather_readings, key=lambda r: r.min_temp)

    @staticmethod
    def calculate_monthly_average_report(weather_readings, year, month):
        result = {}

        high_temps = []
        low_temps = []
        mean_humidity_val = []

        weather_readings = filter_by_date(weather_readings, year, month)

        for reading in weather_readings:
            high_temps.append(reading.max_temp)
            low_temps.append(reading.min_temp)
            mean_humidity_val.append(reading.mean_humidity)

        if not any(len(readings) for readings in [high_temps, low_temps, mean_humidity_val]):
            return {}

        result['Average Highest Temp'] = sum(high_temps) / len(high_temps)
        result['Average Lowest Temp'] = sum(low_temps) / len(low_temps)
        result['Average Mean Humidity'] = sum(mean_humidity_val) / len(mean_humidity_val)

        return result

    @staticmethod
    def calculate_daily_extremes_report(weather_readings, year, month):
        result = {}

        dates = []
        min_temps = []
        max_temps = []

        weather_readings = filter_by_date(weather_readings, year, month)

        for reading in weather_readings:
                dates.append(reading.date)
                min_temps.append(reading.min_temp)
                max_temps.append(reading.max_temp)

        result['Dates'] = dates
        result['Min Temps'] = min_temps
        result['Max Temps'] = max_temps
        return result


class WeatherDisplay:
    @staticmethod
    def present_annual_report(report):
        high = report['Highest Annual Temp']
        low = report['Lowest Annual Temp']
        humid = report['Highest Annual Humidity']

        if any(result == {} for result in [humid, low, high]):
            print('Invalid data or input')
            return

        print("Highest: {0}C on {1}".format(
            high.max_temp, high.date.strftime("%d %B")))
        print("Lowest: {0}C on {1}".format(
            low.min_temp, low.date.strftime("%d %B")))
        print("Humidity: {0}% on {1}\n".format(
            humid.max_humidity, humid.date.strftime("%d %B")))

    @staticmethod
    def present_monthly_average_report(report):

        required_fields = ['Average Highest Temp', 'Average Lowest Temp', 'Average Mean Humidity']

        if any(field not in report for field in required_fields):
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
        dates = report['Dates']
        min_temps = report['Min Temps']
        max_temps = report['Max Temps']

        if not any(len(readings) for readings in [dates, min_temps, max_temps]):
            print('Invalid data or input')
            return

        print(dates[0].strftime('%B %Y'))

        for i in range(0, len(dates)):
            low = '+' * abs(min_temps[i])
            high = '+' * abs(max_temps[i])

            if not horizontal:
                print(u"{0} \u001b[34m{1}\u001b[0m {2}C".format(
                    dates[i].strftime('%d'), high, max_temps[i]))
                print(u"{0} \u001b[31m{1}\u001b[0m {2}C".format(
                    dates[i].strftime('%d'), low, min_temps[i]))
            else:
                print((("{0} \u001b[31m{1}\u001b[0m\u001b[34m{2}"
                        "\u001b[0m {3}C-{4}C")).format(
                    dates[i].strftime('%d'), low, high, min_temps[i], max_temps[i]))

        print()
