import csv
from datetime import datetime
import os


class WeatherRecord:

    def __init__(self, weather_reading):

        self.date = datetime.strptime(weather_reading['PKT'] or
                                      weather_reading['PKST'], '%Y-%m-%d').date()
        self.max_temp = int(weather_reading['Max TemperatureC'])
        self.min_temp = int(weather_reading['Min TemperatureC'])
        self.mean_humidity = int(weather_reading[' Mean Humidity'])
        self.max_humidity = int(weather_reading['Max Humidity'])


class WeatherAnalysis:

    def display_month_bar_chart(self, file_records):
        for file_row in file_records:
            max_value = file_row.max_temp
            min_value = file_row.min_temp
            date = file_row.date
            if min_value < 0:
                print("{}".format(date.day),
                      "\033[1;34m-\033[1;m" * abs(min_value),
                      "\033[1;31m+\033[1;m" * max_value,
                      "{}C - {}C".format(min_value, max_value))
            else:
                print("{}".format(date.day),
                      "\033[1;34m+\033[1;m" * min_value,
                      "\033[1;31m+\033[1;m" * max_value,
                      "{}C - {}C".format(min_value, max_value))

    def display_monthly_report(self, file_records):
        high_temp = self.get_max_temp(file_records)
        print("Highest Average : {}C".format(high_temp))

        low_temp = self.get_min_temp(file_records)
        print("Lowest Average : {}C".format(low_temp))

        mean_humidity = int(self.get_mean_average_humidity(file_records))
        print("Average Mean Humidity : {}% ".format(mean_humidity))

    def display_month_chart_report(self, file_records):
        for file_row in file_records:
                max_temp_value = int(file_row.max_temp)
                min_temp_value = int(file_row.min_temp)
                get_day = file_row.date
                print("{}".format(get_day.day),
                      "\033[1;31m+\033[1;m" * max_temp_value,
                      "{}C".format(max_temp_value))
                if min_temp_value < 0:
                    print("{}".format(get_day.day),
                          "\033[1;34m-\033[1;m" * abs(min_temp_value),
                          "{}C".format(min_temp_value))
                else:
                    print("{}".format(get_day.day),
                          "\033[1;34m+\033[1;m" * abs(min_temp_value),
                          "{}C".format(min_temp_value))

    def display_yearly_report(self, file_records):
        high_temp = self.get_highest_average_temp(file_records)
        date = self.get_required_date(file_records, high_temp,
                                      reverse_flag=True)
        print("Highest: {}C on {} {}".format(
              high_temp, date.strftime("%B"), date.day))
        low_temp = self.get_lowest_average_temp(file_records)
        date = self.get_required_date(file_records, low_temp,
                                      reverse_flag=False)
        print("Lowest: {}C on {} {}".format(
              low_temp, date.strftime("%B"), date.day))
        mean_humidity = self.get_mean_average_humidity(file_records)
        date = self.get_required_date(
               file_records, mean_humidity, reverse_flag=True)
        print("Humidity: {}% on {} {}".format(
              mean_humidity, date.strftime("%B"), date.day))

    def get_max_temp(self, file_records):
        maximum_temperature_list = [file_rows.max_temp
                                    for file_rows in file_records if file_rows]
        return max(maximum_temperature_list)

    def get_min_temp(self, file_records):
        minimum_temperature_list = [file_rows.min_temp
                                    for file_rows in file_records if file_rows]
        return min(minimum_temperature_list)

    def get_mean_average_humidity(self, file_records):
        mean_humidity_list = [file_rows.mean_humidity for file_rows
                              in file_records if file_rows]
        return len(mean_humidity_list)

    def get_highest_average_temp(self, file_records):
        highest_mean_temp_list = [file_rows.max_temp
                                  for file_rows in file_records if file_rows]
        return round(sum(highest_mean_temp_list)/len(highest_mean_temp_list))

    def get_lowest_average_temp(self, file_records):
        lowest_mean_temp_list = [file_rows.min_temp
                                 for file_rows in file_records if file_rows]
        return round(sum(lowest_mean_temp_list)/len(lowest_mean_temp_list))

    def get_required_date(self, file_records, required_value, reverse_flag):
        file_records = [file_row.date for file_row in file_records
                        if required_value]
        file_records.sort(key=lambda x: int(required_value),
                          reverse=reverse_flag)
        return file_records[0]

    def check_file_attributes(self, file_row):
        required_attributes = ['PKT' or 'PKST', 'Max TemperatureC',
                               'Min TemperatureC', 'Max Humidity',
                               ' Mean Humidity']
        return all(file_row.get(attribute) for attribute in required_attributes)

    def check_valid_date(self, file_row, date):
        if str(file_row.get('PKT') or file_row.get('PKST')).find(date):
            return True
        else:
            return False

    def reading_file(self, file_names, date):
        for file_name in file_names:
            with open(file_name, 'r') as csvfile:
                weather_file_readings = csv.DictReader(csvfile)
                weather_readings = [WeatherRecord(file_row) for file_row
                                    in weather_file_readings if
                                    self.check_valid_date(file_row, date) and
                                    self.check_file_attributes(file_row)]
        return weather_readings

    def get_files(self, files_directory):
        file_names = os.listdir(files_directory)
        file_paths = [os.path.join(files_directory, file_name)
                      for file_name in file_names if 'weather' in
                      file_name and not file_name.startswith('.')]
        return [file_path for file_path in file_paths
                if os.path.isfile(file_path)]