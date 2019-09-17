from weatherman import ReportType
import weathercalculations
import datetime


def generate_report(report_type, weather_readings):

    if report_type == ReportType.YEARLY.value:
        highest_temperature_reading = weathercalculations.get_highest_temperature_reading(weather_readings)
        lowest_temperature_reading = weathercalculations.get_lowest_temperature_reading(weather_readings)
        most_humid_day_reading = weathercalculations.get_most_humid_day(weather_readings)
        highest_temperature_formatted_date = datetime.datetime.strptime(highest_temperature_reading.reading_date, '%Y-%m-%d')
        lowest_temperature_formatted_date = datetime.datetime.strptime(lowest_temperature_reading.reading_date, '%Y-%m-%d')
        most_humid_day_formatted_date = datetime.datetime.strptime(most_humid_day_reading.reading_date, '%Y-%m-%d')
        print('Highest: {}C'.format(highest_temperature_reading.max_temperature_c), 'on',
              highest_temperature_formatted_date.strftime('%B'), highest_temperature_formatted_date.strftime('%d'))
        print('Lowest: {}C'.format(lowest_temperature_reading.min_temperature_c), 'on',
              lowest_temperature_formatted_date.strftime('%B'), lowest_temperature_formatted_date.strftime('%d'))
        print('Humidity: {}%'.format(most_humid_day_reading.max_humidity), 'on',
              most_humid_day_formatted_date.strftime('%B'), most_humid_day_formatted_date.strftime('%d'))
        print('-' * 20)

    if report_type == ReportType.MONTHLY.value:
        average_highest_temperature = weathercalculations.get_highest_temperature_average_reading(weather_readings)
        average_lowest_temperature = weathercalculations.get_lowest_temperature_average_reading(weather_readings)
        average_mean_humidity = weathercalculations.get_mean_humid_day_average(weather_readings)
        print('Highest Average: {}C'.format(average_highest_temperature))
        print('Lowest Average: {}C'.format(average_lowest_temperature))
        print('Average Mean Humidity: {}%'.format(average_mean_humidity))
        print('-'*20)

    if report_type == ReportType.MONTHLY_WITH_CHART.value:
        weathercalculations.draw_chart_for_lowest_and_highest_temperature_each_day_bonus(weather_readings)
        print('-' * 20)
