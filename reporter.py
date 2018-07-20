import calendar

from validator import Validator


class WeatherReporter:
    red_bar, blue_bar = "\033[91m+\033[00m", "\033[34m+\033[00m"

    @staticmethod
    @Validator.validate_parameter
    def display_chart(weather_readings):
        print(f"{calendar.month_name[weather_readings[0].date.month]}  {weather_readings[0].date.year}")
        for reading in weather_readings:
            print(f'{reading.date.day}{WeatherReporter.blue_bar*reading.min_temperature}'
                  f'{WeatherReporter.red_bar*reading.max_temperature}'
                  f' {reading.min_temperature} C-{reading.max_temperature} C')

    @staticmethod
    @Validator.validate_parameter
    def display_annual_weather(annual_result):
        summary = []

        date = annual_result.max_temp_reading.date
        summary.append(f'\nHighest: {annual_result.max_temp_reading.max_temperature}C on  '
                       f'{calendar.month_name[date.month]} {date.day}')

        date = annual_result.min_temp_reading.date
        summary.append(f'Lowest: {annual_result.min_temp_reading.min_temperature}C on '
                       f'{calendar.month_name[date.month]} {date.day}')

        date = annual_result.max_humid_reading.date
        summary.append(f'Humidity: {annual_result.max_humid_reading.max_humidity}% on'
                       f' {calendar.month_name[date.month]} {date.day}')
        print('\n'.join(summary))

    @staticmethod
    @Validator.validate_parameter
    def display_monthly_weather(monthly_result):
        summary = [
            f'\nHighest Average: {round(monthly_result.max_temp_avg,2)} C',
            f'Lowest Average: {round(monthly_result.min_temp_avg,2)} C',
            f'Humidity Average: {round(monthly_result.mean_humid_avg,2)} %'
        ]
        print('\n'.join(summary))
