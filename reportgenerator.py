RED = "\033[1;31m"
BLUE = "\033[1;34m"
RESET = "\033[0;0m"


def generate_year_info_report(results):
    highest_temperature = results[0][0]
    highest_temperature_month = results[0][1]
    highest_temperature_day = results[0][2]
    print(f'Highest: {highest_temperature}C on {highest_temperature_month} {highest_temperature_day}')

    lowest_temperature = results[1][0]
    lowest_temperature_month = results[1][1]
    lowest_temperature_day = results[1][2]
    print(f'Lowest: {lowest_temperature}C on {lowest_temperature_month} {lowest_temperature_day}')

    most_humidity = results[2][0]
    most_humidity_month = results[2][1]
    most_humidity_day = results[2][2]
    print(f'Humidity: {most_humidity}% on {most_humidity_month} {most_humidity_day}\n')


def generate_month_info_report(results):
    highest_average = results[0]
    lowest_average = results[1]
    average_mean_humidity = results[2]

    print(f'Highest Average: {highest_average}C')
    print(f'Lowest Average: {lowest_average}C')
    print(f'Average Mean Humidity: {average_mean_humidity}%\n')


def generate_month_temperature_detailed_report(month, year, results):
    print(f'{month} {year}')

    for day, max_temperature, min_temperature in results:
        print(f'{day:02d} '
              f'\033[1;34m{"+" * min_temperature}'
              f'\033[1;31m{"+" * max_temperature}'
              f'\033[0;0m {min_temperature:02d}C - {max_temperature:02d}C')

    print()
