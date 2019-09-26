import csv
import glob
from datetime import datetime


class WeatherData:

    def __init__(self, weather_reading):
        if weather_reading:
            if 'PKT' in weather_reading:
                self.full_date = datetime.strptime(
                     weather_reading['PKT'], '%Y-%m-%d').date()
            if 'Max TemperatureC' in weather_reading:
                self.max_temp = int(weather_reading['Max TemperatureC'])
            if weather_reading['Min TemperatureC']:
                self.min_temp = int(weather_reading['Min TemperatureC'])
            if weather_reading[' Mean Humidity']:
                self.mean_humidity = int(weather_reading[' Mean Humidity'])
            if weather_reading['Max Humidity']:
                self.max_humidity = int(weather_reading['Max Humidity'])


class WeatherAnalyze:

    def display_month_bar_chart(self, file_data):
        for data_row in file_data:
            max_value = data_row.max_temp
            min_value = data_row.min_temp
            date = data_row.full_date
            print(date.day, end="")
            if min_value < 0:
                for lowest_value in range(abs(min_value)):
                    print("\033[1;34m-\033[1;m", end="")
            for lowest_value in range(min_value):
                print("\033[1;34m+\033[1;m", end="")
            for highest_value in range(max_value):
                print("\033[1;31m+\033[1;m", end="")
            print(min_value, end="")
            print("C- ", end="")
            print(max_value, end="")
            print("C")

    def display_monthly_report(self, file_data):
        high_temp = self.get_max_temp(file_data)
        print("Highest Average : {}C".format(high_temp))

        low_temp = self.get_min_temp(file_data)
        print("Lowest Average : {}C".format(low_temp))

        mean_humidity = int(self.get_mean_average_humidity(file_data))
        print("Average Mean Humidity : {}% ".format(mean_humidity))

    def display_month_chart_report(self, file_data):
        self.file_data = file_data
        for file_row in file_data:
                max_value = int(file_row.max_temp)
                min_value = int(file_row.min_temp)
                get_day = file_row.full_date
                print(get_day.day, end="")
                for max_temp_count in range(max_value):
                    print("\033[1;31m+\033[1;m", end="")
                print(" ", max_value, "C")
                get_day = file_row.full_date
                print(get_day.day, end="")
                if min_value < 0:
                    for min_temp_count in range(abs(min_value)):
                        print("\033[1;34m-\033[1;m", end="")
                    print(" {}C".format(min_value))
                else:
                    for min_temp_count in range(min_value):
                        print("\033[1;34m+\033[1;m", end="")
                    print(" {}C".format(min_value))

    def display_yearly_report(self, file_data):
        high_temp = self.get_highest_average_temp(file_data)
        date = self.get_required_date(file_data, high_temp, reverse_flag=True)
        print("Highest: {}C on {} {}".format(
              high_temp, date.strftime("%B"), date.day))
        low_temp = self.get_lowest_average_temp(file_data)
        date = self.get_required_date(file_data, low_temp, reverse_flag=False)
        print("Lowest: {}C on {} {}".format(
              low_temp, date.strftime("%B"), date.day))
        mean_humidity = self.get_mean_average_humidity(file_data)
        date = self.get_required_date(
               file_data, mean_humidity, reverse_flag=True)
        print("Humidity: {}% on {} {}".format(
              mean_humidity, date.strftime("%B"), date.day))

    def get_max_temp(self, file_data):
        max_list = [file_rows.max_temp for file_rows in file_data if file_rows]
        return max(max_list)

    def get_min_temp(self, file_data):
        min_list = [file_rows.min_temp for file_rows in file_data if file_rows]
        return min(min_list)

    def get_mean_average_humidity(self, file_data):
        humidity_mean_list = [file_rows.mean_humidity for file_rows
                              in file_data if file_rows]
        return len(humidity_mean_list)

    def get_highest_average_temp(self, file_data):
        mean_list_max = [file_rows.max_temp for file_rows in file_data
                         if file_rows]
        return round(sum(mean_list_max)/len(mean_list_max))

    def get_lowest_average_temp(self, file_data):
        mean_list_min = [file_rows.min_temp for file_rows in file_data
                         if file_rows]
        return round(sum(mean_list_min)/len(mean_list_min))

    def get_required_date(self, file_data, required_value, reverse_flag):
        file_data = [file_row.full_date for file_row in file_data
                     if required_value]
        file_data.sort(key=lambda x: int(required_value), reverse=reverse_flag)
        return file_data[0]

    def reading_file(self, file_names):
        for file_name in file_names:
            with open(file_name, 'r') as csvfile:
                weather_file_readings = csv.DictReader(csvfile)
                weather_readings = [WeatherData(file_row) for file_row
                                    in weather_file_readings]
        return weather_readings

    def get_file_name(self, arguments, file_name, file_path):
        pattern = "*{}_{}*.txt"
        if arguments == "a" or arguments == "c":
            file_month = datetime.strptime(file_name, "%Y/%m").strftime("%b")
            pattern = pattern.format(file_name.split("/")[0], file_month)
        elif arguments == "e":
            pattern = pattern.format(file_name, "")
        return glob.glob(file_path + pattern)
