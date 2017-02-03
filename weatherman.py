from argparse import ArgumentParser
from weatherman_util import *
from WeatherDataParser import WeatherDataParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('-e', type=int)
    parser.add_argument('-c')
    parser.add_argument('-a')

    args = parser.parse_args()
    return args


def yearly_report(year):
    all_data = w_parser.get_data()

    target_data = list(filter(lambda d: d.date.year == year, all_data))  # Filter relevant data

    # Find highest temperature and date
    temp_map = {d.date: d.max_temp for d in target_data}
    max_temp_date = max(temp_map, key=temp_map.get)
    max_temp = temp_map[max_temp_date]

    print('Highest: {0}C on {1}'.format(max_temp,
                                        format_date(max_temp_date)))

    # Find lowest temperature and date
    temp_map = {d.date: d.min_temp for d in target_data}
    min_temp_date = min(temp_map, key=temp_map.get)
    min_temp = temp_map[min_temp_date]
    print('Lowest: {0}C on {1}'.format(min_temp, format_date(min_temp_date)))

    # Find highest humidity and date
    humidity_map = {d.date: d.max_humidity for d in target_data}
    max_humidity_date = max(humidity_map, key=humidity_map.get)
    max_humidity = humidity_map[max_humidity_date]

    print('Humidity: {0}% on {1}'.format(max_humidity, format_date(max_humidity_date)))


def monthly_report(year, month):
    all_data = w_parser.get_data()
    target_data = list(filter(matches_month(month, year), all_data))
    max_temp = [x.max_temp for x in target_data]
    avg_highest = sum(max_temp) / len(max_temp)
    print('Highest Average: {0}C'.format(avg_highest))

    min_temp = [x.min_temp for x in target_data]
    avg_lowest = sum(min_temp) / len(min_temp)
    print('Lowest Average: {0}C'.format(avg_lowest))

    humidity = [x.mean_humidity for x in target_data]
    avg_humidity = sum(humidity) / len(humidity)
    print('Average Mean Humidity: {0}%'.format(avg_humidity))


def draw_chart(year, month):
    all_data = w_parser.get_data()
    target_data = list(filter(matches_month(month, year), all_data))
    print('{month} {year}'.format(month=month_abbr(args.c), year=year))

    red = '\033[91m'
    blue = '\033[94m'
    for data in target_data:
        max_temp = int(data.max_temp)
        min_temp = int(data.min_temp)

        # Print Maximum temperature for the day
        print(red)
        print('{:02d}  '.format(data.date.day), end=' ')
        print('+' * max_temp, end=' ')
        print(max_temp)

        # Print Minimum temperature for the day
        print(blue)
        print('{:02d}  '.format(data.date.day), end=' ')
        print('+' * min_temp, end=' ')
        print(min_temp)


if __name__ == '__main__':
    args = parse_args()
    directory = args.directory
    w_parser = WeatherDataParser(directory)
    w_parser.parse_data()

    if args.e:
        # Generate report for max temperature, min temperature and most humid day
        year = args.e
        yearly_report(year)

    if args.a:
        # For a given month, display average highest temperature, average lowest temperature
        # and average mean humidity
        s = args.a
        year, month = map(lambda x: int(x), s.split('/'))
        monthly_report(year, month)

    if args.c:
        year, month = map(lambda x: int(x), args.c.split('/'))
        draw_chart(year, month)
