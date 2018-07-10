import calendar as cal
import csv
import argparse
import glob as gb
import os


class DayForecast:

    def __init__(self, read_list):
        self.date = read_list[0]
        self.max_temp = read_list[1]
        self.mean_temp = read_list[2]
        self.min_temp = read_list[3]
        self.max_humidity = read_list[7]
        self.mean_humidity = read_list[8]
        self.min_humidity = read_list[9]


def get_year(action):
    year = 0
    for i in action or []:
        year = i
    return year


def print_blue(text, n):
    print("\033[96m{}\033[00m".format(text) * n, end="")


def print_red(text, n):
    print("\033[31m{}\033[00m".format(text) * n, end="")


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("directory", help="Directory to all weather files", type=str)
    parser.add_argument("-c", "--chart",
                        help="Display bar charts for provided month in C (YY/MM)",
                        action="append")
    parser.add_argument("-e", "--extreme",
                        help="Calculate max temp, humidity and min temp for year E (YY)",
                        action="append")
    parser.add_argument("-a", "--average",
                        help="Calculate average of max temp, min temp, mean humidity for month in A (YY/MM)",
                        action="append")

    return parser.parse_args()


def parse_files(directory):
    weather_records = []
    os.chdir(directory)

    for file in gb.glob("*.txt"):
        weather_file = open(file, "r")
        reader = csv.reader(weather_file)
        temp_readings = list(reader)

        for j in range(1, len(temp_readings)):
            single_day_record = DayForecast(temp_readings[j])

            if not (single_day_record.max_temp == '' or
                    single_day_record.min_temp == '' or
                    single_day_record.max_humidity == '' or
                    single_day_record.mean_humidity == ''):
                weather_records.append(DayForecast(temp_readings[j]))

    return weather_records


def calculate_results(args, weather_records):
    weather_record_subset = []
    if args.extreme:
        year = get_year(args.extreme)
        for i in weather_records:
            if year in i.date:
                weather_record_subset.append(i)

        maximum_temperature = max(weather_record_subset, key=lambda DayForecast: int(DayForecast.max_temp))
        minimum_temperature = min(weather_record_subset, key=lambda DayForecast: int(DayForecast.min_temp))
        maximum_humidity = max(weather_record_subset, key=lambda DayForecast: int(DayForecast.max_humidity))

        generate_yearly_report(maximum_temperature, minimum_temperature, maximum_humidity)
        weather_record_subset.clear()

    if args.average:
        temp = get_year(args.average).split("/")
        single_month = temp[0] + "-" + temp[1]

        for i in weather_records:
            if single_month in i.date:
                weather_record_subset.append(i)

        avg_maximum_temp = round(sum(int(DayForecast.max_temp)
                                     for DayForecast in weather_record_subset) / len(weather_record_subset))

        avg_minimum_temp = round(sum(int(DayForecast.min_temp)
                                     for DayForecast in weather_record_subset) / len(weather_record_subset))

        avg_mean_humidity = round(sum(int(DayForecast.mean_humidity)
                                      for DayForecast in weather_record_subset) / len(weather_record_subset))

        generate_monthly_report(avg_maximum_temp, avg_minimum_temp, avg_mean_humidity)
        weather_record_subset.clear()

    if args.chart:
        day_index = 1
        temp = get_year(args.chart).split("/")
        single_month = temp[0] + "-" + temp[1][1:]

        print(cal.month_name[int(temp[1])], temp[0])
        for i in weather_records:
            if single_month in i.date:
                # UNCOMMENT ONE OF ANY BAR CHART FORMATS
                display_single_bar_chart(day_index, i.min_temp, i.max_temp)
                # display_separate_bar_charts(day_index, i.min_temp, i.max_temp)

                day_index += 1


def display_single_bar_chart(day, minimum_temp, maximum_temp):
    print("%d " % day, end="")
    print_blue("+", int(minimum_temp))
    print_red("+", int(maximum_temp))
    print(" %sC - %sC" % (minimum_temp, maximum_temp))


def display_separate_bar_charts(day, minimum_temp, maximum_temp):
    print("%d " % day, end="")
    print_red("+", int(maximum_temp))
    print(" %sC" % maximum_temp)

    print("%d " % day, end="")
    print_blue("+", int(minimum_temp))
    print(" %sC" % minimum_temp)


def get_date_params(date_str):
    date_str = date_str.split("-")
    return [date_str[0], date_str[1], date_str[2]]


def generate_yearly_report(maximum_temperature, minimum_temperature, maximum_humidity):
    year_max, month_max, date_max = get_date_params(maximum_temperature.date)
    year_min, month_min, date_min = get_date_params(minimum_temperature.date)
    year_humid, month_humid, date_humid = get_date_params(maximum_humidity.date)

    print("\nHighest: %sC on %s %s" % (maximum_temperature.max_temp,
                                     cal.month_name[int(month_max)],
                                     date_max))
    print("Lowest: %sC on %s %s" % (minimum_temperature.min_temp,
                                    cal.month_name[int(month_min)],
                                    date_min))
    print("Humidity: %s%% on %s %s\n" % (maximum_humidity.max_humidity,
                                         cal.month_name[int(month_humid)],
                                         date_humid))


def generate_monthly_report(avg_max_temp, avg_lowest_temp, avg_mean_humidity):
    print("Highest Average: %dC" % avg_max_temp)
    print("Lowest Average: %dC" % avg_lowest_temp)
    print("Average Mean Humidity: %d%%\n" % avg_mean_humidity)


def main(arguments):
    weather_records = parse_files(arguments.directory)
    calculate_results(arguments, weather_records)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
