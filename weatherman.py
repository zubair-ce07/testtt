import argparse
from weatherman_ds import MonthData
from weatherman_ds import ResultData
from weatherman_calculation import max_temp_cal
from weatherman_calculation import min_temp_cal
from weatherman_calculation import max_humid_cal
from weatherman_calculation import avg_max_temp_cal
from weatherman_calculation import avg_min_temp_cal
from weatherman_calculation import avg_humid_cal


def main():
    weather_data_e = []
    weather_data_a = []
    weather_data_c = []

    parser = argparse.ArgumentParser()

    parser.add_argument('directory')
    parser.add_argument('-e', default='')
    parser.add_argument('-a', default='')
    parser.add_argument('-c', default='')

    args = parser.parse_args()

    if args.e:
        for i in range(0, 12):
            month = MonthData()
            available = month.load_month(args.directory, args.e, i)
            if available != 'not available':
                weather_data_e.append(month)
        minimum_temperature = min_temp_cal(weather_data_e)
        maximum_temperature = max_temp_cal(weather_data_e)
        maximum_humidity = max_humid_cal(weather_data_e)
        result = ResultData(minimum_temperature, maximum_temperature, maximum_humidity)
        option_e_report(result)

    if args.a:
        date_full = args.a
        date = date_full.split('/')
        month = MonthData()
        try:
            available = month.load_month(args.directory, date[0], date[1])
        except IndexError:
            print("Invalid date option -a format :yyyy/mm")
            return
        if available != 'not available':
            weather_data_a.append(month)
        else:
            print("Weather data not available for " + date_full)
            return

        average_maximum = avg_max_temp_cal(weather_data_a)
        average_minimum = avg_min_temp_cal(weather_data_a)
        average_humidity = avg_humid_cal(weather_data_a)

        result = ResultData(average_minimum, average_maximum, average_humidity)
        option_a_report(result)

    if args.c:
        date_full = args.c
        date = date_full.split('/')
        month = MonthData()

        try:
            available = month.load_month(args.directory, date[0], date[1])

        except IndexError:
            print("Invalid date option -c format :yyyy/mm")
            return

        if available != 'not available':
            weather_data_c.append(month)

        else:
            print("Weather data not available for " + date_full)
            return

        option_c_report(weather_data_c, date)


def option_e_report(result):
    """"Displays the highest lowest temperature and highest humidity report"""
    months = ('January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December')

    print("REPORT OPTION -e:")
    print("-"*18)

    date_str = result.temperature_highest[0]
    date = date_str.split('-')
    print("Highest: " + result.temperature_highest[1] +
          "C on " + months[int(date[1])-1] + " " + date[2])

    date_str = result.temperature_lowest[0]
    date = date_str.split('-')
    print("Lowest: " + result.temperature_lowest[1] +
          "C on " + months[int(date[1])-1] + " " + date[2])

    date_str = result.humidity[0]
    date = date_str.split('-')
    print("Humidity: " + result.humidity[1] + "% on " +
          months[int(date[1]) - 1] + " " + date[2])

    print("")


def option_a_report(result):
    """Displays the average highest lowest temperature and humidity of a month"""
    print("REPORT OPTION -a:")
    print("-"*18)

    print("Highest Average: " + result.temperature_highest + "C")
    print("Lowest Average: " + result.temperature_lowest + "C")
    print("Average mean humidity: " + result.humidity + "%")
    print("")


def option_c_report(data, date):
    """"Displays the bar chart for temperatures through the month"""
    months = ('January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December')

    print("REPORT OPTION -c:")
    print("-"*18)

    print(months[int(date[1])-1] + " " + date[0])
    month_data = data.pop()
    day_number = 1
    for day in month_data.days:
            min_temperature = day.readings["Min TemperatureC"]
            if min_temperature:
                reading_value = int(min_temperature)
                if reading_value >= 0:
                    print("\033[35m%02d" % day_number + "\033[34m" +
                          "+" * reading_value + "\033[30m", end="")
                else:
                    reading_value = abs(reading_value)
                    print("\033[35m%02d" % day_number + "\033[34m" +
                          "-" * reading_value + "\033[30m", end="")

            max_temperature = day.readings["Max TemperatureC"]
            if max_temperature:
                reading_value = int(max_temperature)
                if reading_value >= 0:
                    print("\033[31m" + "+"*reading_value + "\033[35m" +
                          min_temperature + "C-" +
                          max_temperature + "C\033[30m")
                else:
                    reading_value = abs(reading_value)
                    print("\033[31m" +
                          "-" * reading_value + "\033[35m" +
                          min_temperature + "C-" +
                          max_temperature + "C\033[30m")

            day_number += 1

    print("")


if __name__ == '__main__':
    main()
