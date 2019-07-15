import calendar

low = "\033[1;34m+"
high = "\033[1;31m+"


def get_extreme_weather(data):

    highest_temp = max([files for files in data.records if isinstance(
        files.highest_temp, int)],key=lambda x: x.highest_temp)
    lowest_temp = min([files for files in data.records if isinstance(
        files.lowest_temp, int)], key=lambda x: x.lowest_temp)
    highest_humidity = max([files for files in data.records if isinstance(
        files.highest_humidity, int)], key=lambda x: x.highest_humidity)

    print('Highest: {}C on {} {}'.format(highest_temp.highest_temp,
        calendar.month_name[highest_temp.date.month],highest_temp.date.day))

    print('Lowest: {}C on {} {}'.format(lowest_temp.lowest_temp,
        calendar.month_name[lowest_temp.date.month],lowest_temp.date.day))

    print('Humidity: {}% on {} {}'.format(highest_humidity.highest_humidity,
        calendar.month_name[highest_humidity.date.month],highest_humidity.date.day))


def get_month_average(data):

    avg_high_temp = [files.highest_temp for files in data.records if isinstance(files.highest_temp, int)]

    avg_low_temp = [files.lowest_temp for files in data.records if isinstance(files.lowest_temp, int)]

    avg_mean_humid = [files.avg_humidity for files in data.records if isinstance(files.avg_humidity, int)]

    print('Highest Average: {}C'.format(sum(avg_high_temp) // len(avg_high_temp)))

    print('Lowest Average: {}C'.format(sum(avg_low_temp) // len(avg_low_temp)))

    print('Average Mean Humidity: {}%'.format(sum(avg_mean_humid) // len(avg_mean_humid)))


def print_weather_graph(data):
    print(calendar.month_name[data.records[0].date.month],
          data.records[0].date.year)
    for i in data.records:
        if isinstance(i.highest_temp, int):
            print('{:02d} '.format(i.date.day) + low * i.highest_temp
                  + ' {:02d}C\n{:02d} '.format(i.highest_temp, i.date.day) +
                  high * i.lowest_temp
                  + ' {:02d}C'.format(i.lowest_temp))
    print()


def bonus_task(data):
    print(calendar.month_name[data.records[0].date.month],
          data.records[0].date.year)
    for i in data.records:
        if isinstance(i.highest_temp, int):
            print('{:02d} '.format(i.date.day) + low * i.lowest_temp
                  + high * i.highest_temp + ' {:}C - {:}C'.format(i.lowest_temp, i.highest_temp))
    print()