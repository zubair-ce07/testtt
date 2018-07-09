import calendar
from weather_analyzer import WeatherAnalyzer


class ReportGenerator:

    @staticmethod
    def process_annual_report(weather_readings):
        highest_temp = WeatherAnalyzer.highest_temp_of_year(weather_readings)
        lowest_temp = WeatherAnalyzer.lowest_temp_of_year(weather_readings)
        highest_hum = WeatherAnalyzer.highest_hum_of_year(weather_readings)
        ReportGenerator.annual_report(highest_hum, highest_temp, lowest_temp)

    @staticmethod
    def process_month_report(month, year, weather_readings):
        max_avg_temp = WeatherAnalyzer.highest_avg_temp_of_month(weather_readings)
        min_avg_temp = WeatherAnalyzer.lowest_avg_temp_of_month(weather_readings)
        mean_avg_hum = WeatherAnalyzer.average_mean_humidity_of_month(weather_readings)
        ReportGenerator.month_report(month, year, max_avg_temp, min_avg_temp, mean_avg_hum)

    @staticmethod
    def process_dual_bar_report(argument, weather_readings):
        year, month = argument.split('/')
        ReportGenerator.dual_bar_chart_report(int(year), int(month), weather_readings)

    @staticmethod
    def process_single_bar_report(argument, weather_readings):
        year, month = argument.split('/')
        ReportGenerator.single_bar_chart_report(int(year), int(month), weather_readings)

    @staticmethod
    def annual_report(highest_hum, highest_temp, lowest_temp):
        print(f'Highest: {highest_temp.highest_temp}C on {calendar.month_name[highest_temp.month]} '
              f'{highest_temp.day}')
        print(f'Lowest: {lowest_temp.lowest_temp}C on {calendar.month_name[lowest_temp.month]} '
              f'{lowest_temp.day}')
        print(f'Humidity: {highest_hum.highest_hum}% on {calendar.month_name[highest_hum.month]} '
              f'{highest_hum.day} \n')

    @staticmethod
    def month_report(month, year, max_avg_temp, min_avg_temp, mean_avg_hum):
        print(f'-a Months Report {calendar.month_name[month]} {year}:')
        print(f'Highest Average: {int(max_avg_temp)}C')
        print(f'Lowest Average: {int(min_avg_temp)}C')
        print(f'Mean Average Humidity: {int(mean_avg_hum)}% \n')

    @staticmethod
    def dual_bar_chart_report(year, month, weather_readings):
        print(f' -d {calendar.month_name[month]} {year}')
        for day_reading in weather_readings:
            counter = day_reading.day
            print(f'{counter:02}', end=' ')
            print(f'\033[94m' + '+' * int(day_reading.highest_temp) + '\033[0m', end='')
            print(f' {day_reading.highest_temp:02}C', end='\n')
            print(f'{counter:02}', end=' ')
            print(f'\033[91m' + '+' * int(day_reading.lowest_temp) + '\033[0m', end='')
            print(f' {day_reading.lowest_temp:02}C', end='\n')
        print('\n')

    @staticmethod
    def single_bar_chart_report(year, month, weather_readings):
        print(f'-c {calendar.month_name[month]} {year}')
        for day_reading in weather_readings:
            counter = day_reading.day
            print(f'{counter:02}', end=' ')
            print(f'\033[91m' + '+' * day_reading.lowest_temp + '\033[0m', end='')
            print(f'\033[94m' + '+' * day_reading.highest_temp + '\033[0m', end='')
            print(f' {day_reading.lowest_temp:02}C - {day_reading.highest_temp:02}C', end='\n')
        print('\n')
