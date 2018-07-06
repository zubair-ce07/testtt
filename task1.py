import sys
import csv
import argparse

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

option = 0
file_data = []
year_readings = []
csv_reader = []


class WeatherReading:
    def __init__(self, row):
        self.pkt = row[0]
        self.max_temp = row[1]
        self.mean_temp = row[2]
        self.min_temp = row[3]
        self.dew = row[4]
        self.mean_dew = row[5]
        self.min_dew = row[6]
        self.max_humidity = row[7]
        self.mean_humidity = row[8]
        self.min_humidity = row[9]
        self.max_sea_pressure = row[10]
        self.mean_sea_pressure = row[11]
        self.min_sea_pressure = row[12]
        self.max_visibility = row[13]
        self.mean_visibility = row[14]
        self.min_visibility = row[15]
        self.mean_windSpeed = row[17]
        self.max_gustSpeed = row[18]
        self.precipitation = row[19]
        self.cloudCover = row[20]
        self.events = row[21]
        self.win_dir_degrees = row[22]


class ParseFiles:
    def __init__(self, input_file):

        self.monthreadings = []

        try:

            with open(input_file, "r") as read_file:
                csv_input = csv.reader(read_file)
                header = next(csv_input)
                for row in csv_input:
                    reading = WeatherReading(row)
                    if row[header.index("Max TemperatureC")] != '':
                        self.monthreadings.append(reading)

        except IOError:
            print("file does not exist")

    def __len__(self):
        length = 0
        for i in range(len(self.monthreadings)):
            length += 1
        return length

    def __getitem__(self, key):
        return self.monthreadings[key]


class MonthResultsCalculator:
    def __init__(self, input_readings):
        self.high_average = 0
        self.low_average = 0
        self.mean_humidity_average = 0

        high_sum = 0
        low_sum = 0
        humidity_sum = 0

        for i in range(len(input_readings)):
            high_sum += (int(input_readings[i].max_temp))
            low_sum += (int(input_readings[i].min_temp))
            humidity_sum += (int(input_readings[i].mean_humidity))

        if len(input_readings):
            self.high_average = float(high_sum / len(input_readings))
            self.low_average = float(low_sum / len(input_readings))
            self.mean_humidity_average = float(
                humidity_sum / len(input_readings))


class MonthAveragePrinter:
    def __init__(self, month_data):
        print("Highest Average: {0} {1}".format(month_data.high_average, "C"))
        print("Lowest Average: {0} {1}".format(month_data.low_average, "C"))
        print("Average Mean Humidity: {0} {1}".format
              (month_data.mean_humidity_average, "%"))
        print("---------------------------")


class MonthBarPrinter:
    def __init__(self, input_readings):

        year, month, day = input_readings[0].pkt.split("-")
        month = month_names[int(month) - 1]
        print(month, year)

        for i in range(len(input_readings)):
            max_str = int(input_readings[i].max_temp)
            min_str = int(input_readings[i].min_temp)
            high_val = str(i + 1)
            low_val = str(i + 1)
            high = '+' * abs(max_str)
            low = '+' * abs(min_str)

            print("{0}{1}{2}{3}{4}{5}".format(high_val, u"\u001b[31m", high, u"\u001b[0m", " ",
                  max_str))

            print("{0}{1}{2}{3}{4}{5}".format(low_val, u"\u001b[34m", low, u"\u001b[0m", " ",
                  min_str))

        print("---------------------------")
        print(month, year)

        for i in range(len(input_readings)):
            max_str = int(input_readings[i].max_temp)
            min_str = int(input_readings[i].min_temp)
            low_val = str(i + 1)
            high = '+' * abs(max_str)
            low = '+' * abs(min_str)

            print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}"
                  .format(low_val, u"\u001b[34m", " ", low, u"\u001b[0m", u"\u001b[31m",
                          high, u"\u001b[0m", " ", min_str, "C - ", max_str, "C"))

        print("---------------------------")


class YearResultsCalculator:
    def __init__(self, year_data):
        self.highest = int(year_data[0][0].max_temp)
        self.lowest = int(year_data[0][0].min_temp)
        self.humid = int(year_data[0][0].max_humidity)

        for i in range(len(year_data)):
            for j in range(len(year_data[i])):
                if int(year_data[i][j].max_temp) > int(self.highest):
                    self.highest = year_data[i][j].max_temp
                    self.highest_date = year_data[i][j].pkt

                if int(year_data[i][j].min_temp) < int(self.lowest):
                    self.lowest = year_data[i][j].min_temp
                    self.lowest_date = year_data[i][j].pkt

                if int(year_data[i][j].max_humidity) > int(self.humid):
                    self.humid = year_data[i][j].max_humidity
                    self.humid_date = year_data[i][j].pkt


class YearResultsPrinter:
    def __init__(self, year_results):
        month_names = ['January', 'February', 'March', 'April', 'May',
                       'June', 'July', 'August', 'September', 'October',
                       'November', 'December']
        high_year, high_month, highest_day = year_results.highest_date.split(
            "-")
        lowest_year, lowest_month, lowest_day = year_results.lowest_date.split(
            "-")
        humid_year, humid_month, humid_day = year_results.humid_date.split("-")

        high_temp_month = month_names[int(high_month) - 1]
        lowest_temp_month = month_names[int(lowest_month) - 1]
        most_humid_month = month_names[int(humid_month) - 1]

        print("Highest: {0}{1}{2}{3}{4}".format(year_results.highest, "C on ",
              high_temp_month, " ", highest_day))
        print("Lowest: {0}{1}{2}{3}{4}".format(year_results.lowest, "C on ",
              lowest_temp_month, " ", lowest_day))
        print("Most Humidity: {0}{1}{2}{3}{4}".format(year_results.humid, '% on ',
              most_humid_month, " ", humid_day))
        print("---------------------------")


def parse_arguments():
    parser_instance = argparse.ArgumentParser()
    parser_instance.add_argument("files_directory")
    parser_instance.add_argument("-a", help="Month Averages", action="append")
    parser_instance.add_argument("-c", help="Two Horizontal Bars", action="append")
    parser_instance.add_argument("-e", help="Year Report", action="append")

    return parser_instance.parse_args()


def construct_filename(cons_arguments, current_arg):
    year, month = current_arg.split("/")
    mon = month_names[int(month) - 1]
    filename = '{0}{1}{2}{3}{4}{5}'.format(cons_arguments.files_directory, "/Murree_weather_",
                                           year, "_", mon, ".txt")
    return filename


def run_calculations(arguments):

    for cli_arg in arguments.a or []:
        filename = construct_filename(arguments, cli_arg)
        file_data = ParseFiles(filename)
        month_results = MonthResultsCalculator(file_data)
        MonthAveragePrinter(month_results)

    for cli_arg in arguments.e or []:
        for i in range(12):
            filename = '{0}{1}{2}{3}{4}{5}'.format(arguments.files_directory, "/Murree_weather_",
                                                   cli_arg, "_", month_names[i], ".txt")
            file_data = ParseFiles(filename)
            year_readings.append(file_data.monthreadings)
        year_results = YearResultsCalculator(year_readings)
        YearResultsPrinter(year_results)

    for cli_arg in arguments.c or []:
        filename = construct_filename(arguments, cli_arg)
        file_data = ParseFiles(filename)
        MonthBarPrinter(file_data.monthreadings)


def main():

    cli_arguments = parse_arguments()
    run_calculations(cli_arguments)


if __name__ == "__main__":
    main()
