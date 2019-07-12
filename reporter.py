import calendar

low = "\033[1;34m+"
high = "\033[1;31m+"

def get_extreme_weather(csvfile):

    highest_temp = max([n for n in csvfile.records if isinstance(
        n.highest_temp, int)], key=lambda x: x.highest_temp)
    lowest_temp = min([n for n in csvfile.records if isinstance(
        n.lowest_temp, int)], key=lambda x: x.lowest_temp)
    highest_humidity = max([n for n in csvfile.records if isinstance(
        n.highest_humidity, int)], key=lambda x: x.highest_humidity)

    print_extreme_weather({'highest_temp': highest_temp,
                           'lowest_temp': lowest_temp, 'max_humid_record': highest_humidity})


def print_extreme_weather(extreme_weathers):

    print('Highest: {:02d}C on {} {:02d}'.format(
        extreme_weathers['highest_temp'].highest_temp,
        calendar.month_name[extreme_weathers['highest_temp'].date.month],
        extreme_weathers['highest_temp'].date.day))

    print('Lowest: {:02d}C on {} {:02d}'.format(
        extreme_weathers['lowest_temp'].lowest_temp,
        calendar.month_name[extreme_weathers['lowest_temp'].date.month],
        extreme_weathers['lowest_temp'].date.day))

    print('Humidity: {:02d}% on {} {:02d}'.format(
        extreme_weathers['max_humid_record'].highest_humidity,
        calendar.month_name[extreme_weathers['max_humid_record'].date.month],
        extreme_weathers['max_humid_record'].date.day), end='\n\n')


def get_month_average(csvfile):

    avg_high_temp = [
        n.highest_temp for n in csvfile.records if isinstance(n.highest_temp, int)]

    avg_low_temp = [
        n.lowest_temp for n in csvfile.records if isinstance(n.lowest_temp, int)]

    avg_mean_humid = [
        n.avg_humidity for n in csvfile.records if isinstance(n.avg_humidity, int)]

    print_month_average({'avg_high_temp': avg_high_temp,
                         'avg_low_temp': avg_low_temp, 'avg_mean_humid': avg_mean_humid})


def print_month_average(month_averages):
    print('Highest Average: {:02d}C'.format(
        sum(month_averages['avg_high_temp']) // len(month_averages['avg_high_temp'])))

    print('Lowest Average: {:02d}C'.format(
        sum(month_averages['avg_low_temp']) // len(month_averages['avg_low_temp'])))

    print('Average Mean Humidity: {:02d}%'.format(
        sum(month_averages['avg_mean_humid']) // len(month_averages['avg_mean_humid'])), end='\n\n')


def print_weather_graph(csvfile):
    print(calendar.month_name[csvfile.records[0].date.month],
          csvfile.records[0].date.year)
    for i in csvfile.records:
        if isinstance(i.highest_temp, int):
            print('{:02d} '.format(i.date.day) + low * i.highest_temp
                  + ' {:02d}C\n{:02d} '.format(i.highest_temp, i.date.day) +
                  high * i.lowest_temp
                  + ' {:02d}C'.format(i.lowest_temp))
    print()
    print(calendar.month_name[csvfile.records[0].date.month],
          csvfile.records[0].date.year)
    for i in csvfile.records:
        if isinstance(i.highest_temp, int):
            print('{:02d} '.format(i.date.day) + low * i.lowest_temp
                  + high * i.highest_temp
                  + ' {:02d}C - {:02d}C'.format(i.lowest_temp, i.highest_temp))
    print()