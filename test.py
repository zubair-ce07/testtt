import sys
import csv
import calendar
from WeatherDS import WeatherDS
from _datetime import datetime


print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
if sys.argv[2].lower() == '-a'.lower():
    # mnth = {
    #     "1": "Jan",
    #     "2": "Feb",
    #     "3": "Mar",
    #     "4": "Apr",
    #     "5": "May",
    #     "6": "Jun",
    #     "7": "Jul",
    #     "8": "Aug",
    #     "9": "Sep",
    #     "10": "Oct",
    #     "11": "Nov",
    #     "12": "Dec"
    #
    # }
    raw = sys.argv[3].split('/')
    inp = raw[0] + '_' + calendar.month_abbr[int(raw[1])]
    wds = list()
    with open(sys.argv[1] + '/weatherfiles/Murree_weather_' + inp + '.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_reader.__next__()
        for row in csv_reader:
            ds = WeatherDS((row[0]), int(0 if not row[1] else row[1]), int(1000 if not row[3] else row[3]),
                           int(0 if not row[7] else row[7]), int(0 if not row[8] else row[8]))
            wds.append(ds)
    res_highest = wds[0]
    res_lowest = wds[0]
    res_humidity = wds[0]

    for item in wds:
        if item.highest > res_highest.highest:
            res_highest = item
        if item.lowest < res_lowest.lowest:
            res_lowest = item
        if item.max_humidity > res_humidity.max_humidity:
            res_humidity = item

    print(f'Highest: {res_highest.highest}C on '
          f'{calendar.month_name[datetime.strptime(res_highest.date, "%Y-%m-%d").month]} {datetime.strptime(res_highest.date, "%Y-%m-%d").day}')

    print(f'Lowest: {res_lowest.lowest}C on '
          f'{calendar.month_name[datetime.strptime(res_lowest.date, "%Y-%m-%d").month]} {datetime.strptime(res_lowest.date, "%Y-%m-%d").day}')

    print(f'humidity: {res_humidity.max_humidity}% on '
          f'{calendar.month_name[datetime.strptime(res_humidity.date, "%Y-%m-%d").month]} {datetime.strptime(res_humidity.date, "%Y-%m-%d").day}')

# elif sys.argv[2].lower() == '-e'.lower():

