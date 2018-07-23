import calendar

from weather_analyzer import WeatherAnalyzer


class ReportGenerator:

    @staticmethod
    def get_annual_report(weather_readings):
        highest_temp = WeatherAnalyzer.highest_temperature(weather_readings)
        lowest_temp = WeatherAnalyzer.lowest_temperature(weather_readings)
        highest_hum = WeatherAnalyzer.highest_humidity(weather_readings)
        ReportGenerator.annual_report(highest_hum, highest_temp, lowest_temp)

    @staticmethod
    def get_month_report(weather_readings):
        max_avg_temp = WeatherAnalyzer.highest_avg_temp(weather_readings)
        min_avg_temp = WeatherAnalyzer.lowest_avg_temp(weather_readings)
        mean_avg_hum = WeatherAnalyzer.average_mean_humidity(weather_readings)
        ReportGenerator.month_report(max_avg_temp, min_avg_temp, mean_avg_hum)

    @staticmethod
    def annual_report(highest_hum, highest_temp, lowest_temp):
        print(f'-e Annual Report {highest_hum.date.tm_year}')
        print(f'Highest: {highest_temp.highest_temp}C on {calendar.month_name[highest_temp.date.tm_mon]} '
              f'{highest_temp.date.tm_mday}')
        print(f'Lowest: {lowest_temp.lowest_temp}C on {calendar.month_name[lowest_temp.date.tm_mon]} '
              f'{lowest_temp.date.tm_mday}')
        print(f'Humidity: {highest_hum.highest_hum}% on {calendar.month_name[highest_hum.date.tm_mon]} '
              f'{highest_hum.date.tm_mday} \n')

    @staticmethod
    def month_report(max_avg_temp, min_avg_temp, mean_avg_hum):
        print(f'Highest Average: {max_avg_temp}C')
        print(f'Lowest Average: {min_avg_temp}C')
        print(f'Mean Average Humidity: {mean_avg_hum}% \n')

    @staticmethod
    def dual_bar_chart_report(weather_readings):
        year = weather_readings[0].date.tm_year
        month = weather_readings[0].date.tm_mon
        print(f'-c {calendar.month_name[month]} {year}')
        for reading in weather_readings:
            print(f'{reading.date.tm_mday:02}', end=' ')
            print(f'\033[94m' + '+' * reading.highest_temp + '\033[0m', end='')
            print(f' {reading.highest_temp:02}C', end='\n')
            print(f'{reading.date.tm_mday:02}', end=' ')
            print(f'\033[91m' + '+' * reading.lowest_temp + '\033[0m', end='')
            print(f' {reading.lowest_temp:02}C', end='\n')
        print('\n')

    @staticmethod
    def single_bar_chart_report(weather_readings):
        year = weather_readings[0].date.tm_year
        month = weather_readings[0].date.tm_mon
        print(f'-d {calendar.month_name[month]} {year}')
        for reading in weather_readings:
            print(f'{reading.date.tm_mday:02}', end=' ')
            print(f'\033[91m' + '+' * reading.lowest_temp + '\033[0m', end='')
            print(f'\033[94m' + '+' * reading.highest_temp + '\033[0m', end='')
            print(f' {reading.lowest_temp:02}C - {reading.highest_temp:02}C', end='\n')
        print('\n')
