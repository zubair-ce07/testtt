import csv


class color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'


def get_month_name(self):
    months = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July',
              '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}
    return months[self]


def show_highest_values():
    print('not implemented yet')


def show_average_values(highest_temps, lowest_temps, average_humidity):
    print("Highest Average: " + str(round(sum(highest_temps) / len(highest_temps), 2)) + "C")
    print("Lowest Average: " + str(round(sum(lowest_temps) / len(lowest_temps))) + "C")
    print("Average Mean Humidity: " + str(round(sum(average_humidity) / len(average_humidity))) + "%")


def show_bar_charts(highest_temps, lowest_temps, header_line):
    """this function will print bar-charts of given data lists"""
    print(header_line)
    for i in range(len(highest_temps)):
        print(
            color.PURPLE + format(i + 1, '02d') + ' ' + color.RED + ('+' * abs(highest_temps[i])) + ' ' + color.PURPLE
            + str(highest_temps[i]) + 'C')
        print(
            color.PURPLE + format(i + 1, '02d') + ' ' + color.BLUE + ('+' * abs(lowest_temps[i])) + ' ' + color.PURPLE
            + str(lowest_temps[i]) + 'C')
    print(color.END + header_line)

    for i in range(len(highest_temps)):
        print(color.PURPLE + format(i + 1, '02d') + ' ' + color.BLUE + (
            '+' * abs(lowest_temps[i])) + color.RED + (
                  '+' * abs(highest_temps[i])) + ' ' + color.PURPLE + str(lowest_temps[i]) + 'C - ' +
              str(highest_temps[i]) + 'C')


if __name__ == "__main__":
    import sys

    input_argument = sys.argv[1]
    year_argument = sys.argv[2]
    path_to_file_argument = sys.argv[3]
    lowest_tempratures = []
    highest_tempratures = []
    avrg_humidity = []

    with open(path_to_file_argument, newline='') as csvfile:
        weather_file_reader = csv.reader(csvfile, delimiter=',')
        for row in weather_file_reader:
            if len(row) > 0:
                if row[0].startswith(year_argument[:4]):
                    lowest_tempratures.append(int(row[3]) if row[3] != '' else 0)
                    highest_tempratures.append(int(row[1]) if row[1] != '' else 0)
                    avrg_humidity.append(int(row[7]) if row[7] != '' else 0)

    if input_argument == '-c':
        barcharts_header = get_month_name(year_argument[5:]) + " " + year_argument[:4]
        show_bar_charts(highest_tempratures, lowest_tempratures, barcharts_header)
    elif input_argument == '-a':
        show_average_values(highest_tempratures, lowest_tempratures, avrg_humidity)
    else:
        show_highest_values()
