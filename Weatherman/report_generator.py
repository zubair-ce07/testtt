import calendar
from weather_analyzer import WeatherAnalyzer


class ReportGenerator:

    @staticmethod
    def get_annual_report(weather_readings):
        highest_temp = WeatherAnalyzer.highest_temp_of_year(weather_readings)
        lowest_temp = WeatherAnalyzer.lowest_temp_of_year(weather_readings)
        highest_hum = WeatherAnalyzer.highest_hum_of_year(weather_readings)
        ReportGenerator.annual_report(highest_hum, highest_temp, lowest_temp)

    @staticmethod
    def get_month_report(month, year, weather_readings):
        max_avg_temp = WeatherAnalyzer.highest_avg_temp_of_month(weather_readings)
        min_avg_temp = WeatherAnalyzer.lowest_avg_temp_of_month(weather_readings)
        mean_avg_hum = WeatherAnalyzer.average_mean_humidity_of_month(weather_readings)
        ReportGenerator.month_report(month, year, max_avg_temp, min_avg_temp, mean_avg_hum)

    @staticmethod
    def get_bar_report(report_type, argument, weather_readings):
        year, month = [int(a) for a in argument.split('/')]
        if report_type == 'c':
            ReportGenerator.dual_bar_chart_report(year, month, weather_readings)
        elif report_type == 'd':
            ReportGenerator.single_bar_chart_report(year, month, weather_readings)

    @staticmethod
    def annual_report(highest_hum, highest_temp, lowest_temp):
        print(f'-e Annual Report {highest_hum.year}')
        print(f'Highest: {highest_temp.highest_temp}C on {calendar.month_name[highest_temp.month]} '
              f'{highest_temp.day}')
        print(f'Lowest: {lowest_temp.lowest_temp}C on {calendar.month_name[lowest_temp.month]} '
              f'{lowest_temp.day}')
        print(f'Humidity: {highest_hum.highest_hum}% on {calendar.month_name[highest_hum.month]} '
              f'{highest_hum.day} \n')

    @staticmethod
    def month_report(month_name, year, max_avg_temp, min_avg_temp, mean_avg_hum):
        print(f'-a Months Report {month_name} {year}:')
        print(f'Highest Average: {max_avg_temp}C')
        print(f'Lowest Average: {min_avg_temp}C')
        print(f'Mean Average Humidity: {mean_avg_hum}% \n')

    @staticmethod
    def dual_bar_chart_report(year, month, weather_readings):
        print(f'-d {calendar.month_name[month]} {year}')
        for reading in weather_readings:
            print(f'{reading.day:02}', end=' ')
            print(f'\033[94m' + '+' * reading.highest_temp + '\033[0m', end='')
            print(f' {reading.highest_temp:02}C', end='\n')
            print(f'{reading.day:02}', end=' ')
            print(f'\033[91m' + '+' * reading.lowest_temp + '\033[0m', end='')
            print(f' {reading.lowest_temp:02}C', end='\n')
        print('\n')

    @staticmethod
    def single_bar_chart_report(year, month, weather_readings):
        print(f'-c {calendar.month_name[month]} {year}')
        for reading in weather_readings:
            print(f'{reading.day:02}', end=' ')
            print(f'\033[91m' + '+' * reading.lowest_temp + '\033[0m', end='')
            print(f'\033[94m' + '+' * reading.highest_temp + '\033[0m', end='')
            print(f' {reading.lowest_temp:02}C - {reading.highest_temp:02}C', end='\n')
        print('\n')

    @staticmethod
    def no_data_found(year, month_name=None):
        print(f'No data found for {month_name} {year}')
