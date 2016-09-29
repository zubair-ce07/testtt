import calendar
import csv
import datetime
import os
import collections

WeatherData = collections.namedtuple("WeatherData",
                                     'date min_temp max_temp max_humidity '
                                     'min_humidity min_avg_temp '
                                     'max_avg_temp max_avg_humidty')


class WeatherDataReader(object):
    """ This weather_data_parser class reads a file,
        and stores the results """

    def __init__(self, report_date, weather_data_dir):
        """ Class constructor that takes file path as an argument """
        self.report_date = report_date
        self.weather_data_dir = weather_data_dir

    def __to_int(self, string):
        """ Converts string to int. """
        if string:
            return int(string)

    def is_date_valid(self, date_text):
        """ Returns if the date_text is a valid date value """
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def __get_weather_files(self):
        """ Returns the list of all files which need to be read """
        date_components = self.report_date.split('/')

        file_name_prefix = 'lahore_weather_' + date_components[0]
        months = [int(date_components[1])] if len(date_components) > 1 \
            else range(1, 13)
        for month_no in months:
            file_name = os.path.join(self.weather_data_dir,
                                     file_name_prefix + '_' +
                                     calendar.month_abbr[month_no] + '.txt')
            yield file_name

    def get_weather_data(self):
        """ Reads the file row by row and records mean min/max
        Temperatures and humidity """
        weather_files = self.__get_weather_files()
        weather_data = []

        for file_path in weather_files:
            with open(file_path) as csvfile:
                # Skipping the first blank line of the file
                next(csvfile)
                csv_reader = csv.DictReader(csvfile)
                monthly_weather_data = []
                date_key = 'PKT' if 'PKT' in csv_reader.fieldnames else 'PKST'

                for row in csv_reader:
                    date_string = row[date_key]
                    if not self.is_date_valid(date_string):
                        continue
                    monthly_weather_data.append(
                        WeatherData(date=date_string,
                                    min_temp=self.__to_int(
                                        row['Min TemperatureC']),
                                    max_temp=self.__to_int(
                                        row['Max TemperatureC']),
                                    max_humidity=self.__to_int(
                                        row['Max Humidity']),
                                    min_humidity=self.__to_int(
                                        row[' Min Humidity']),
                                    min_avg_temp=self.__to_int(
                                        row['Mean TemperatureC']),
                                    max_avg_temp=self.__to_int(
                                        row['Mean TemperatureC']),
                                    max_avg_humidty=self.__to_int(
                                        row[' Mean Humidity'])
                                    ))
                weather_data.extend(monthly_weather_data)
        return weather_data
