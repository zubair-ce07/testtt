

class WeatherReportPrinter(object):

    W = '\033[0m'
    R = '\033[31m'
    G = '\033[32m'

    @staticmethod
    def highest_temp(temp):
        print ('Highest: ' + next(iter(temp.values()))['max_temp'] + 'C')

    @staticmethod
    def lowest_temp(temp):
        print ('Lowest: ' + next(iter(temp.values()))['min_temp'] + 'C')

    @staticmethod
    def highest_humid(temp):
        print ('Humidity: ' + next(iter(temp.values()))['max_humid'] + 'C')

    @staticmethod
    def mean_highest_temp(temp):
        print ('Highest Average: ' + str(temp) + 'C')

    @staticmethod
    def mean_lowest_temp(temp):
        print ('Lowest Average: ' + str(temp) + 'C')

    @staticmethod
    def mean_highest_humid(temp):
        print ('Average Mean Humidity: ' + str(temp) + 'C')

    @staticmethod
    def display_chart(records):
        for date, record in records.iteritems():
            print (date + WeatherReportPrinter.R + int(record['max_temp'])*'+' +
                   WeatherReportPrinter.W + ' ' + record['max_temp'] + 'C')
            print (date + WeatherReportPrinter.G + int(record['min_temp']) * '+' +
                   WeatherReportPrinter.W + ' ' + record['min_temp'] + 'C')

    @staticmethod
    def display_singleline_chart(records):
        for date, record in records.iteritems():
            print (date + WeatherReportPrinter.R + int(record['max_temp'])*'+' +
                   WeatherReportPrinter.G + int(record['min_temp']) * '+' +
                   WeatherReportPrinter.W + ' ' + record['max_temp'] + '-' +
                   record['min_temp'] + 'C')
