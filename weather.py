import datetime
import csv


class Parser:
    def read(self, directory):
        weather_readings = []

        for path in directory:
            with open(path, 'r') as f:
                weather_data = csv.DictReader(f)

                [weather_readings.append(dict(reading)) for reading in weather_data]

        return self.clean(weather_readings)

    def clean(self, weather_readings):
        weather_data = []

        for reading in weather_readings:
            keys = reading.keys()

            if 'PKST' in keys:
                reading['PKT'] = reading['PKST']
                del reading['PKST']

            for key in keys:
                if key != key.strip():
                    reading[key.strip()] = reading[key]
                    del reading[key]

            if self.includes_relevant_data(reading):
                weather_data.append(reading)

        return weather_data

    @staticmethod
    def includes_relevant_data(reading):
        required_fields = ['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC',
                           'Max Humidity', 'Mean Humidity', 'Min Humidity']

        return all(reading[field] for field in required_fields)


class Calculator:
    def calculate_annual_result(self, weather_readings, year):
        result = {
            'Lowest Annual Temp':
                self.find_annual_lowest_temp(weather_readings, f"{year}-"),
            'Highest Annual Temp':
                self.find_annual_highest_temp(weather_readings, f"{year}-"),
            'Highest Annual Humidity':
                self.find_annual_highest_humidity(weather_readings, f"{year}-")
        }
        return result

    @staticmethod
    def find_annual_highest_temp(weather_readings, year):
        weather_readings = [r for r in weather_readings if year in r['PKT']]
        if len(weather_readings):
            return max(weather_readings, key=lambda r: int(r['Max TemperatureC']))
        else:
            return {}

    @staticmethod
    def find_annual_highest_humidity(weather_readings, year):
        weather_readings = [r for r in weather_readings if year in r['PKT']]
        if len(weather_readings):
            return max(weather_readings, key=lambda r: int(r['Max Humidity']))
        else:
            return {}

    @staticmethod
    def find_annual_lowest_temp(weather_readings, year):
        weather_readings = [r for r in weather_readings if year in r['PKT']]
        if len(weather_readings):
            return min(weather_readings, key=lambda r: int(r['Min TemperatureC']))
        else:
            return {}

    @staticmethod
    def calculate_monthly_average_report(weather_readings, year, month):
        result = {}
        date = f"{year}-{month}"

        high_temps = []
        low_temps = []
        mean_humidity_val = []

        for reading in weather_readings:
            if date in reading['PKT']:
                if reading['Max TemperatureC']:
                    high_temps.append(int(reading['Max TemperatureC']))
                if reading['Min TemperatureC']:
                    low_temps.append(int(reading['Min TemperatureC']))
                if reading['Max Humidity']:
                    mean_humidity_val.append(int(reading['Mean Humidity']))

        if len(high_temps) == 0 or len(low_temps) == 0 or len(mean_humidity_val) == 0:
            return {}

        result['Average Highest Temp'] = sum(high_temps) / len(high_temps)
        result['Average Lowest Temp'] = sum(low_temps) / len(low_temps)
        result['Average Mean Humidity'] = sum(mean_humidity_val) / len(mean_humidity_val)

        return result

    @staticmethod
    def calculate_daily_extremes_report(weather_readings, year, month):
        result = {}
        date = f"{year}-{month}-"

        dates = []
        min_temps = []
        max_temps = []

        for reading in weather_readings:
            if date in reading['PKT']:
                if reading['Max TemperatureC'] and reading['Min TemperatureC']:
                    dates.append(reading['PKT'])
                    min_temps.append(reading['Min TemperatureC'])
                    max_temps.append(reading['Max TemperatureC'])

        result['Dates'] = dates
        result['Min Temps'] = min_temps
        result['Max Temps'] = max_temps
        return result


class WeatherDisplay:
    @staticmethod
    def str_to_date(string):
        date = string.split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

    def present_annual_report(self, report):
        high = report['Highest Annual Temp']
        low = report['Lowest Annual Temp']
        humid = report['Highest Annual Humidity']

        if humid == {} or low == {} or \
                high == {}:
            print('Invalid data or input')
            return

        date = self.str_to_date(high['PKT'])
        print("Highest: {0}C on {1}".format(high['Max TemperatureC'], date.strftime("%d %B")))

        date = self.str_to_date(low['PKT'])
        print("Lowest: {0}C on {1}".format(low['Min TemperatureC'], date.strftime("%d %B")))

        date = self.str_to_date(humid['PKT'])
        print("Humidity: {0}% on {1}\n".format(
            humid['Max Humidity'], date.strftime("%d %B")))

    @staticmethod
    def present_monthly_average_report(report):

        if 'Average Highest Temp' not in report or \
                'Average Lowest Temp' not in report or \
                'Average Mean Humidity' not in report:
            print('Invalid data or input')
            return

        print('Highest Average: {0}C'.format(
            round(report['Average Highest Temp'])))
        print('Lowest Average: {0}C'.format(
            round(report['Average Lowest Temp'])))
        print('Average Mean Humidity: {0}%\n'.format(
            round(report['Average Mean Humidity'])))

    def present_daily_extremes_report(self, report, horizontal=False):
        dates = report['Dates']
        min_temps = report['Min Temps']
        max_temps = report['Max Temps']

        if len(dates) == 0 or len(dates) != len(min_temps) or \
                len(dates) != len(max_temps):
            print('Invalid data or input')
            return

        date = self.str_to_date(dates[0])
        print(date.strftime('%B %Y'))

        for i in range(0, len(dates)):
            day = dates[i].split(
                '-')[2] if len(dates[i].split('-')[2]) == 2 else f"0{dates[i].split('-')[2]}"

            low = '+' * abs(int(min_temps[i]))
            high = '+' * abs(int(max_temps[i]))

            if not horizontal:
                print(u"{0} \u001b[34m{1}\u001b[0m {2}C".format(day, high, int(max_temps[i])))
                print(u"{0} \u001b[31m{1}\u001b[0m {2}C".format(day, low, int(min_temps[i])))
            else:

                print((("{0} \u001b[31m{1}\u001b[0m\u001b[34m{2}"
                        "\u001b[0m {3}C-{4}C")).format(
                    day, low, high, int(min_temps[i]), int(max_temps[i])))

        print()
