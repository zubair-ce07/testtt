import argparse
import sys

from dayinfo import DayInfo


pkt = 'PKT'  # 0
max_temp = 'Max Temp'  # 1
mean_temp = 'Mean Temp'  # 2
min_temp = 'Min Temp'  # 3
mean_humidity = 'Mean Humidity'  # 8

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
          ]


def parser(files_dir, files):
    weather_readings = []

    for file in files:
        with open(files_dir + file) as f:
            next(f)

            # line contains information of a single day of a month
            for line in f:
                line = line.strip().split(',')
                weather_readings.append(DayInfo(line))

    return weather_readings


def main():
    # creating argument parser
    # parser = argparse.ArgumentParser()
    # parser.add_argument('files_dir',
    #                     type=str,
    #                     help='Directory containing weather files')
    # parser.add_argument('-e',
    #                     metavar='e',
    #                     type=str,
    #                     nargs='?',
    #                     help=('For a given year display the highest temperature and day, lowest temperature and day, '
    #                           'most humid day and humidity.'))
    # parser.add_argument('-a',
    #                     metavar='a',
    #                     type=str,
    #                     nargs='?',
    #                     help=('For a given month display the average highest temperature, average lowest temperature, '
    #                           'average mean humidity.'))
    # parser.add_argument('-c',
    #                     metavar='c',
    #                     type=str,
    #                     nargs='?',
    #                     help=(
    #                         'For a given month draw two horizontal bar charts on the console for the highest and '
    #                         'lowest temperature on each day. Highest in red and lowest in blue.'))
    # args = parser.parse_args()

    # extracting arguments
    files_dir = 'weatherfiles/'  # args.files_dir + '/'
    e = None  # args.e
    a = '2005/6'  # args.a
    c = None  # args.c

    if e is not None:
        pass

    if a is not None:
        year, month = a.split('/')
        file_name = 'Murree_weather_' + year + '_' + months[int(month) - 1] + '.txt'
        weather_readings = parser(files_dir, [file_name])

    if c is not None:
        pass


main()
