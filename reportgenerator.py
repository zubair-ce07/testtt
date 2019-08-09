import calendar


def parse_date(date):
    y, m, d = date.split('-')
    return int(y), calendar.month_name[int(m)], int(d)


def generate_year_info_report(results):
    highest_temperature = results[0].max_temperature
    _, highest_temperature_month, highest_temperature_day = parse_date(results[0].date)
    print(f'Highest: {highest_temperature}C on {highest_temperature_month} {highest_temperature_day}')

    lowest_temperature = results[1].min_temperature
    _, lowest_temperature_month, lowest_temperature_day = parse_date(results[1].date)
    print(f'Lowest: {lowest_temperature}C on {lowest_temperature_month} {lowest_temperature_day}')

    most_humidity = results[2].mean_humidity
    _, most_humidity_month, most_humidity_day = parse_date(results[2].date)
    print(f'Humidity: {most_humidity}% on {most_humidity_month} {most_humidity_day}\n')


def generate_month_info_report(results):
    highest_average = results[0]
    lowest_average = results[1]
    average_mean_humidity = results[2]

    print(f'Highest Average: {highest_average}C')
    print(f'Lowest Average: {lowest_average}C')
    print(f'Average Mean Humidity: {average_mean_humidity}%\n')


def generate_month_temperature_detailed_report(results):
    year, month, _ = parse_date(results[0].date)
    print(f'{month} {year}')

    for weather_record in results:
        print(f'{parse_date(weather_record.date)[2]:02d} '
              f'\033[1;34m{"+" * weather_record.min_temperature}'
              f'\033[1;31m{"+" * weather_record.max_temperature}'
              f'\033[0;0m {weather_record.min_temperature:02d}C - {weather_record.max_temperature:02d}C')

    print()
