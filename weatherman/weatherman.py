import csv

from termcolor import colored

from day_weather import DayWeather


class WeatherReport:
    files_names = []

    MONTHS_KEY_MAP = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep",
                      10: "Oct", 11: "Nov", 12: "Dec"}

    MONTHS_NAMES = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April", "May": "May",
                    "Jun": "June", "Jul": "July", "Aug": "August", "Sep": "September", "Oct": "October",
                    "Nov": "November", "Dec": "December"}

    def __init__(self):
        with open('files_names') as file_:
            self.files_names = file_.read().split('\n')[:-1]

    def __read_month_weather(self, file_path):
        month_data = []
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                month_data.append(row)
        return month_data

    def __get_month_name(self, month_number):
        return self.MONTHS_NAMES[self.MONTHS_KEY_MAP[int(month_number)]]

    def __get_day_weather(self, day_data):
        day_weather = DayWeather()
        day_weather.set_weather(day_data)
        return day_weather

    def __compute_average(self, data):
        average_max_temperature = sum(int(line.max_temperature) for line in data) // len(data)
        average_min_temperature = sum(int(line.min_temperature) for line in data) // len(data)
        average_mean_humidity = sum(int(line.mean_humidity) for line in data) // len(data)
        print('Highest Average: ' + str(average_max_temperature) + 'C')
        print('Lowest Average: ' + str(average_min_temperature) + 'C')
        print('Average Mean Humidity: ' + str(average_mean_humidity) + '%')
        return None

    def get_required_day(self, data, option):
        if option == 1:
            return max(data, key=lambda x: int(x.max_temperature))
        if option == 2:
            return min(data, key=lambda x: int(x.min_temperature))
        if option == 3:
            return max(data, key=lambda x: int(x.max_humidity))
        return data[0]

    def print_yearly_report(self, highest_temp_day, lowest_temp_day, highest_humidity_day):

        print('Highest: ' + highest_temp_day.max_temperature + 'c on '
              + self.__get_month_name(highest_temp_day.get_month())
              + ' ' + highest_temp_day.get_day())

        print('Lowest: ' + lowest_temp_day.min_temperature + 'c on '
              + self.__get_month_name(lowest_temp_day.get_month())
              + ' ' + lowest_temp_day.get_day())

        print('Humidity: ' + highest_humidity_day.max_humidity + '% on '
              + self.__get_month_name(highest_humidity_day.get_month())
              + ' ' + highest_humidity_day.get_day())

    def get_month_data(self, year_and_month, files_path, location):
        month_data = []
        year = year_and_month.split('/')[0]
        month = year_and_month.split('/')[1]
        complete_file_path = files_path + '/' + location + '_weather_' + year \
                             + '_' + self.MONTHS_KEY_MAP[int(month)] + '.txt'
        file_data = self.__read_month_weather(complete_file_path)
        for data in file_data:
            if data['Max TemperatureC'] and data['Min TemperatureC'] and data[' Mean Humidity']:
                month_data.append(self.__get_day_weather(data))
        month_name = self.__get_month_name(month)
        return year, month_name, month_data

    def print_dayily_data(self, year, month_name, month_data):
        print(month_name + ' ' + year)
        for i in range(len(month_data)):
            max_temp = month_data[i].max_temperature
            min_temp = month_data[i].min_temperature
            print(str(i + 1) + ' ' +
                  colored('+' * int(max_temp), 'red') + colored('+' * int(min_temp), 'blue')
                  + ' ' + max_temp + 'C - ' + min_temp + 'C')

    def get_yearly_insights(self, year, files_path):
        year_data = []
        for file_name in self.files_names:
            if year == file_name.split('_')[2]:
                month_data = self.__read_month_weather(files_path + '/' + file_name)
                for data in month_data:
                    if data['Max TemperatureC'] and data['Min TemperatureC'] and data['Max Humidity']:
                        year_data.append(self.__get_day_weather(data))
        highest_temperature_day = self.get_required_day(year_data, 1)
        lowest_temperature_day = self.get_required_day(year_data, 2)
        highest_humidity_day = self.get_required_day(year_data, 3)
        self.print_yearly_report(highest_temperature_day, lowest_temperature_day, highest_humidity_day)

    def get_monthly_insights(self, year_and_month, files_path, location):
        year, month_name, month_data = self.get_month_data(year_and_month, files_path, location)
        self.__compute_average(month_data)

    def get_days_insights(self, year_and_month, files_path, location):
        year, month_name, month_data = self.get_month_data(year_and_month, files_path, location)
        self.print_dayily_data(year, month_name, month_data)
