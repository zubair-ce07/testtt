import argparse
import calendar
from termcolor import colored
import csv


class WeatherMan(object):
    
    def __init__(self):
        self.months = calendar.month_name

    @staticmethod
    def read_file(file_path, year, month, data_fields):
        filename = "{}/lahore_weather_{}_{}.txt".format(file_path, year, month[:3])

        with open(filename) as csvFile:
            return list(csv.DictReader(csvFile, fieldnames=data_fields))[1:]

    def display_highest_lowest(self, params):
        if not params:
            return

        highest_data = {'highest_temp': None, 'highest_day': None, 'highest_month': None}
        lowest_data = {'lowest_temp': None, 'lowest_day': None, 'lowest_month': None}
        humidity_data = {'highest_humidity': None, 'humidity_day': None, 'humidity_month': None}

        data_fields = ['PKT', 'Max TemperatureC',  'Min TemperatureC',  'Max Humidity']

        for month in self.months[1:]:
            file_data = self.read_file(params[1], params[0], month, data_fields)
            for row in file_data:
                date = row[data_fields[0]].split('-')

                if(row[data_fields[1]] and (not highest_data['highest_temp']
                                            or highest_data['highest_temp'] < int(row[data_fields[1]]))):
                    highest_data['highest_temp'] = int(row[data_fields[1]])
                    highest_data['highest_day'] = date[2]
                    highest_data['highest_month'] = month

                if(row[data_fields[2]] and (not lowest_data['lowest_temp']
                                            or lowest_data['lowest_temp'] > int(row[data_fields[2]]))):

                    lowest_data['lowest_temp'] = int(row[data_fields[2]])
                    lowest_data['lowest_day'] = date[2]
                    lowest_data['lowest_month'] = month

                if(row[data_fields[3]] and (not humidity_data['highest_humidity']
                                            or humidity_data['highest_humidity'] < int(row[data_fields[3]]))):
                    humidity_data['highest_humidity'] = int(row[data_fields[3]])
                    humidity_data['humidity_day'] = date[2]
                    humidity_data['humidity_month'] = month

        print('Highest: {}C on {} {} \nLowest: {}C on {} {} \nHumid: {}C on {} {}'.format(
            str(highest_data['highest_temp']), highest_data['highest_month'], highest_data['highest_day'],
            str(lowest_data['lowest_temp']), lowest_data['lowest_month'], lowest_data['lowest_day'],
            str(humidity_data['highest_humidity']), humidity_data['humidity_month'], humidity_data['humidity_day']))

    def display_average(self, params):
        if not params:
            return

        highest_temp = None
        lowest_temp = None
        highest_humidity = None

        data_fields = ['PKT', 'Mean TemperatureC', 'Mean Humidity']

        date = params[0].split('/')

        file_data = self.read_file(params[1], date[0], self.months[int(date[1])], data_fields)
        for row in file_data:
            if (row[data_fields[1]] and (not highest_temp
                                         or highest_temp < int(row[data_fields[1]]))):
                highest_temp = int(row[data_fields[1]])

            if (row[data_fields[1]] and (not lowest_temp
                                         or lowest_temp > int(row[data_fields[1]]))):
                lowest_temp = int(row[data_fields[1]])

            if (row[data_fields[2]] and (not highest_humidity
                                         or highest_humidity < int(row[data_fields[2]]))):
                highest_humidity = int(row[data_fields[2]])

        print('Highest Average: {}C \nLowest Average: {}C \nAverage Humidity: {}%'.format(
            str(highest_temp), str(lowest_temp), str(highest_humidity)))

    def display_bar_charts(self, params):
        if not params:
            return

        data_fields = ['PKT', 'Max TemperatureC', 'Min TemperatureC']

        date = params[0].split('/')
        print('{} {}'.format(self.months[int(date[1])], date[0]))

        file_data = self.read_file(params[1], date[0], self.months[int(date[1])], data_fields)

        for row in file_data:
            cur_date = row[data_fields[0]].split('-')

            if row[data_fields[1]]:
                highest_temp = int(row[data_fields[1]])

                print('{} '.format(cur_date[2]), end='')

                for index in range(highest_temp):
                    print(colored('+', 'red'), end='')
                print(' {}C'.format(str(highest_temp)))

            if row[data_fields[2]]:
                lowest_temp = int(row[data_fields[2]])

                print('{} '.format(cur_date[2]), end='')

                for index in range(lowest_temp):
                    print(colored('+', 'blue'), end='')
                print(' {}C'.format(str(lowest_temp)))

        print('\n')

        for row in file_data:
            highest_temp = None
            lowest_temp = None
            if row[data_fields[2]]:
                lowest_temp = int(row[data_fields[2]])

                print('{} '.format(row[data_fields[0]].split('-')[2]), end='')

                for index in range(lowest_temp):
                    print(colored('+', 'blue'), end='')

            if row[data_fields[1]]:
                highest_temp = int(row[data_fields[1]])

                for index in range(highest_temp):
                    print(colored('+', 'red'), end='')

            if lowest_temp and highest_temp:
                print(' {}C-{}C'.format(str(lowest_temp), str(highest_temp)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', nargs=2)
    parser.add_argument('-a', nargs=2)
    parser.add_argument('-c', nargs=2)
    args = parser.parse_args()

    weatherman = WeatherMan()
    weatherman.display_highest_lowest(args.e)
    weatherman.display_average(args.a)
    weatherman.display_bar_charts(args.c)


if __name__ == "__main__":
    main()

