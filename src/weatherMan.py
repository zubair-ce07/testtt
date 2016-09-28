import os


class color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'


def get_month_name(self):
    months = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July',
              '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}
    return months[self]


def print_message(message_arguments):
    if message_arguments['temp'] != message_arguments['temp_flag']:
        yr, mn, dt = message_arguments['day'].split('-')
        print(message_arguments['header_value'] + ": " + format(message_arguments['temp'], '02d') +
              message_arguments['temp_sign'] + " on " + get_month_name(mn) + " " + dt)
    else:
        print(message_arguments['header_value'] + " Not Found")


def part_one(file_arguments):
    month_count = 0
    highest_temp = 0
    lowest_temp = 1000
    most_humidity = 0
    highest_temp_day = 'none'
    lowest_temp_day = 'none'
    most_humid_day = 'none'
    for months in range(1, 12):
        path_new = file_arguments['path_to_file'] + get_month_name(str(months))[:3] + '.txt'
        if os.path.isfile(path_new):
            f = open(path_new, 'r+')
            for line in f:
                weather_data = line.split(',')
                if weather_data[0].startswith(file_arguments['year']):
                    weather_data[1] = int(weather_data[1]) if weather_data[1].strip() else 0
                    weather_data[3] = int(weather_data[3]) if weather_data[3].strip() else 1000
                    weather_data[7] = int(weather_data[7]) if weather_data[7].strip() else 0
                    if weather_data[1] > highest_temp:
                        highest_temp = weather_data[1]
                        highest_temp_day = weather_data[0]
                    if weather_data[3] < lowest_temp and weather_data[3] != 1000:
                        lowest_temp = weather_data[3]
                        lowest_temp_day = weather_data[0]
                    if weather_data[7] > most_humidity:
                        most_humidity = weather_data[7]
                        most_humid_day = weather_data[0]
            f.close()
        else:
            month_count += 1
            if month_count >= 12:
                print("invalid file path or file does not exist")

    print_message({'temp': highest_temp, 'day': highest_temp_day, 'header_value': "Highest", 'temp_sign': "C",
                   'temp_flag': 0})
    print_message({'temp': lowest_temp, 'day': lowest_temp_day, 'header_value': "Lowest", 'temp_sign': "C",
                   'temp_flag': 1000})
    print_message({'temp': most_humidity, 'day': most_humid_day, 'header_value': "Humidity", 'temp_sign': "%",
                   'temp_flag': 0})
    return


def part_two(file_arguments):
    """this function will display highest, lowest avrg temprature and Average Mean Humidity"""
    lowest_temp_count = 0
    highest_temp_count = 0
    lowest_temp_sum = 0
    highest_temp_sum = 0
    humidity_count = 0
    humidity_sum = 0

    if os.path.isfile(file_arguments['path_to_file']):
        f = open(file_arguments['path_to_file'], 'r+')
        for line in f:
            weather_data = line.split(',')
            if weather_data[0].startswith(file_arguments['year']):
                if weather_data[1] != '':
                    highest_temp_count += 1
                    highest_temp_sum += int(weather_data[1])

                if weather_data[3] != '':
                    lowest_temp_count += 1
                    lowest_temp_sum += int(weather_data[3])

                if weather_data[8] != '':
                    humidity_count += 1
                    humidity_sum += int(weather_data[8])
        f.close()
    else:
        print('file not found')

    if highest_temp_count != 0:
        print("Highest Average: " + str(round(highest_temp_sum / highest_temp_count, 2)) + "C")
    else:
        print("Highest Average Not Found")

    if lowest_temp_count != 0:
        print("Lowest Average: " + str(round(lowest_temp_sum / lowest_temp_count, 2)) + "C")
    else:
        print("Lowest Average Not Found")

    if humidity_count != 0:
        print("Average Mean Humidity: " + str(round(humidity_sum / humidity_count, 2)) + "%")
    else:
        print("Humidity Not Found")


def part_three(file_arguments):
    if os.path.isfile(file_arguments['path_to_file']):
        f = open(file_arguments['path_to_file'], 'r+')
        day_count = 1
        for line in f:
            weather_data = line.split(',')
            if weather_data[0].startswith(file_arguments['year']):
                maxTemp = 0 if weather_data[1] == '' else int(weather_data[1])
                print(color.PURPLE + format(day_count, '02d') + ' ' + color.RED + (
                    '+' * abs(maxTemp)) + ' ' + color.PURPLE + (
                      '0' if weather_data[1] == '' else weather_data[1]) + 'C')
                minTemp = 0 if weather_data[3] == '' else int(weather_data[3])

                print(format(day_count, '02d') + ' ' + color.BLUE + ('+' * abs(minTemp)) + ' ' + color.PURPLE + (
                    '0' if weather_data[3] == '' else weather_data[3]) + 'C')
                day_count += 1

        f.close()
        print(color.END)

    else:
        print("invalid file path or file does not exist")


def part_four(file_arguments):
    if os.path.isfile(file_arguments['path_to_file']):
        f = open(file_arguments['path_to_file'], 'r+')
        count = 1
        for line in f:
            weather_data = line.split(',')
            if weather_data[0].startswith(file_arguments['year']):
                print(color.PURPLE + format(count, '02d') + ' ' + color.BLUE + (
                    '+' * abs(0 if weather_data[3] == '' else int(weather_data[3]))) + color.RED + (
                          '+' * abs(0 if weather_data[1] == '' else int(weather_data[1]))) + ' ' + color.PURPLE + (
                          '0' if weather_data[3] == '' else weather_data[3]) + 'C - ' + (
                          '0' if weather_data[1] == '' else weather_data[1]) + 'C')
                count += 1
        f.close()
        print(color.END)

    else:
        print("invalid file path or file does not exist")


# if 1996 <= int(year_arg) and 2011 >= int(year_arg):


print('part 1, for year 2002')
part_one({"year": '2002', 'path_to_file': '/root/PycharmProjects/weatherman/weatherdata/lahore_weather_2002_'})
print('\npart 2, for month 2002/6')
part_two({"year": '2002', 'path_to_file': '/root/PycharmProjects/weatherman/weatherdata/lahore_weather_2002_'
                                          + get_month_name('6')[:3] + '.txt'})
print('\npart 3, for month 2002/6')
print(get_month_name('6') + ' 2002')
part_three({"year": '2002', 'path_to_file': '/root/PycharmProjects/weatherman/weatherdata/lahore_weather_2002_'
                                            + get_month_name('6')[:3] + '.txt'})
print('part 4, for month 2002/6')
print(get_month_name('6') + ' 2002')
part_four({"year": '2002', 'path_to_file': '/root/PycharmProjects/weatherman/weatherdata/lahore_weather_2002_'
                                           + get_month_name('6')[:3] + '.txt'})
