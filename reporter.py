import calendar

low = "\033[1;34m+"
high = "\033[1;31m+"


def get_max_min(data):

    highest_temp = max([files for files in data.records if isinstance(
        files.highest_temp, int)],key=lambda x: x.highest_temp)
    lowest_temp = min([files for files in data.records if isinstance(
        files.lowest_temp, int)], key=lambda x: x.lowest_temp)
    highest_humidity = max([files for files in data.records if isinstance(
        files.highest_humidity, int)], key=lambda x: x.highest_humidity)

    print_max_min(highest_temp,lowest_temp,highest_humidity)


def print_max_min(highest_temp,lowest_temp,highest_humidity):

    print('Highest: {}C on {} {}'.format(highest_temp.highest_temp,
          calendar.month_name[highest_temp.date.month],highest_temp.date.day))

    print('Lowest: {}C on {} {}'.format(lowest_temp.lowest_temp,
          calendar.month_name[lowest_temp.date.month],lowest_temp.date.day))

    print('Humidity: {}% on {} {}'.format(highest_humidity.highest_humidity,
          calendar.month_name[highest_humidity.date.month],highest_humidity.date.day))


def month_average(data):

    avg_high_temp = [files.highest_temp for files in data.records if isinstance(files.highest_temp, int)]

    avg_low_temp = [files.lowest_temp for files in data.records if isinstance(files.lowest_temp, int)]

    avg_mean_humid = [files.avg_humidity for files in data.records if isinstance(files.avg_humidity, int)]

    print_month_average(avg_high_temp,avg_low_temp,avg_mean_humid)


def print_month_average(avg_high_temp,avg_low_temp,avg_mean_humid):

    print('Highest Average: {}C'.format(sum(avg_high_temp) // len(avg_high_temp)))

    print('Lowest Average: {}C'.format(sum(avg_low_temp) // len(avg_low_temp)))

    print('Average Mean Humidity: {}%'.format(sum(avg_mean_humid) // len(avg_mean_humid)))


def print_chart(data):
    for i in data.records:
        if isinstance(i.highest_temp, int):
            print(high * i.highest_temp
                  + ' {}C\n '.format(i.highest_temp) +
                  low * i.lowest_temp
                  + ' {}C'.format(i.lowest_temp))
    print()


def bonus_task(data):
    for i in data.records:
        if isinstance(i.highest_temp, int):
            print('{} '.format(i.date.day) + low * i.lowest_temp
                  + high * i.highest_temp + ' {}C - {}C'.format(i.lowest_temp, i.highest_temp))
    print()
