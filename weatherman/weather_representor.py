import calendar

import constants


class WeatherRepresentor:
    @staticmethod
    def print_temprature_graph(weather):
        if not weather:
            row = 'Record not found!'
        else:
            row = '{}{}{}{}{} {}C - {}C'.format(
                constants.CBLUE, '+' * weather.min_temperature, constants.CRED,
                '+' * weather.max_temperature, constants.CEND,
                weather.min_temperature, weather.max_temperature)

        print('{} {}'.format(str(weather.date.day).zfill(2), row))

    @staticmethod
    def print_not_fount():
        print('No record found!')

    @staticmethod
    def print_date(date):
        print(date.strftime('%B %Y'))

    @staticmethod
    def print_average_of_month(highest_average_temperature,
                               lowest_average_temperature, average_humidity):
        print('Highest Average: {}C'.format(highest_average_temperature))
        print('Lowest Average: {}C'.format(lowest_average_temperature))
        print('Average Humidity: {}%'.format(average_humidity))

    @staticmethod
    def print_summary_of_year(highest, lowest, humid):
        print('Highest: {}C on {}'.format(
            highest.max_temperature, highest.date.strftime('%B %d')))
        print('Lowest: {}C on {}'.format(
            lowest.min_temperature, lowest.date.strftime('%B %d')))
        print('Humid: {}% on {}'.format(
            humid.max_humidity, humid.date.strftime('%B %d')))
