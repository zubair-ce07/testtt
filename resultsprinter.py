

class WeatherReportPrinter(object):

    WHITE = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'

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
            print (date + WeatherReportPrinter.RED + abs(int(record['max_temp']))*'+' +
                   WeatherReportPrinter.WHITE + ' ' + record['max_temp'] + 'C')
            print (date + WeatherReportPrinter.GREEN + abs(int(record['min_temp']))*'+' +
                   WeatherReportPrinter.WHITE + ' ' + record['min_temp'] + 'C')

    @staticmethod
    def display_single_line_chart(records):
        for date, record in records.iteritems():
            print (date + WeatherReportPrinter.RED + abs(int(record['max_temp']))*'+' +
                   WeatherReportPrinter.GREEN + abs(int(record['min_temp']))*'+' +
                   WeatherReportPrinter.WHITE + ' ' + record['max_temp']+'-' +
                   record['min_temp'] + 'C')

    @staticmethod
    def print_yearly_report(report):
        WeatherReportPrinter.highest_temp(report['max_temp'])
        WeatherReportPrinter.lowest_temp(report['min_temp'])
        WeatherReportPrinter.highest_humid(report['max_humid'])

    @staticmethod
    def print_monthly_report(report):
        WeatherReportPrinter.mean_highest_temp(report['avg_max_temp'])
        WeatherReportPrinter.mean_lowest_temp(report['avg_min_temp'])
        WeatherReportPrinter.mean_highest_humid(report['avg_max_humid'])