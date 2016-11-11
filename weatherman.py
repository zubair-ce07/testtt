from argparse import ArgumentParser
from myfunctions import *
from WeatherDataParser import WeatherDataParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-e', type=int)
    parser.add_argument('-c')
    parser.add_argument('-a')

    args = parser.parse_args()

    w_parser = WeatherDataParser('/home/abdul/Downloads/weatherfiles/weatherfiles/*.txt')
    w_parser.parse_data()

    if args.e:
        # Generate report for max temperature, min temperature and most humid day
        year = args.e

        all_data = w_parser.get_data()

        target_data = list(filter(lambda d: d.date.year == year, all_data))  # Filter relevant data

        # Find highest temperature and date
        temp_map = {d.date: d.max_temp for d in target_data}
        max_temp_date = max(temp_map, key=temp_map.get)
        max_temp = temp_map[max_temp_date]

        print('Highest: %dC on %s' % (max_temp,
                                      format_date(max_temp_date)))

        # Find lowest temperature and date
        temp_map = {d.date: d.min_temp for d in target_data}
        min_temp_date = min(temp_map, key=temp_map.get)
        min_temp = temp_map[min_temp_date]
        print('Lowest: %dC on %s' % (min_temp, format_date(min_temp_date)))

        # Find highest humidity and date
        humidity_map = {d.date: d.max_humidity for d in target_data}
        max_humidity_date = max(humidity_map, key=humidity_map.get)
        max_humidity = humidity_map[max_humidity_date]

        print('Humidity: %d%% on %s' % (max_humidity, format_date(max_humidity_date)))

    if args.a:
        # For a given month, display average highest temperature, average lowest temperature
        # and average mean humidity
        s = args.a
        year, month = map(lambda x: int(x), s.split('/'))

        all_data = w_parser.get_data()
        target_data = list(filter(matches_month(month,year), all_data))
        max_temp = [x.max_temp for x in target_data]
        avg_highest = sum(max_temp) / len(max_temp)
        print('Highest Average: %sC' % avg_highest)

        min_temp = [x.min_temp for x in target_data]
        avg_lowest = sum(min_temp) / len(min_temp)
        print('Lowest Average: %sC' % avg_lowest)

        humidity = [x.mean_humidity for x in target_data]
        avg_humidity = sum(humidity) / len(humidity)
        print('Average Mean Humidity: %d%%' % avg_humidity)

    if args.c:
        year, month = map(lambda x: int(x), args.c.split('/'))
        all_data = w_parser.get_data()
        target_data = list(filter(matches_month(month, year), all_data))
        print('%s %d' % (month_abbr(args.c), year))

        red = '\033[91m'
        blue = '\033[94m'
        for data in target_data:
            max_temp = int(data.max_temp)
            min_temp = int(data.min_temp)

            # Print Maximum temperature for the day
            print(red)
            print('%02d  ' % data.date.day, end=' ')
            print('+' * max_temp, end=' ')
            print(max_temp)

            # Print Minimum temperature for the day
            print(blue)
            print('%02d  ' % data.date.day, end=' ')
            print('+' * min_temp, end=' ')
            print(min_temp)
