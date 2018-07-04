from weatherman_ds import MonthData
from weatherman_ds import ResultData
from weatherman_calculation import maximum_temperature_calculate
from weatherman_calculation import minimum_temperature_calculate
from weatherman_calculation import maximum_humidity_calculate
from weatherman_calculation import average_maximum_temperature_calculate
from weatherman_calculation import average_minimum_temperature_calculate
import argparse
import datetime


weather_data_c = []
weather_data_a = []


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('directory')
    parser.add_argument('-e', default='0')
    parser.add_argument('-a', default='0')
    parser.add_argument('-c', default='0')

    args = parser.parse_args()

    if args.e != '0':
        for i in range(0, 12):
            month = MonthData()
            available = month.load_month(args.directory, args.e, i)
            if available != 'not available':
                weather_data_c.append(month)
        minimum_temperature = minimum_temperature_calculate(weather_data_c)
        maximum_temperature = maximum_temperature_calculate(weather_data_c)
        maximum_humidity = maximum_humidity_calculate(weather_data_c)
        result = ResultData(minimum_temperature, maximum_temperature, maximum_humidity)
        option_e_report(result)

    if args.a != '0':
        date_full = args.a
        date = date_full.split('/')
        month = MonthData()
        available = month.load_month(args.directory, date[0], date[1])
        if available != 'not available':
            weather_data_a.append(month)

        print(average_maximum_temperature_calculate(weather_data_a))
        print(average_minimum_temperature_calculate(weather_data_a))


def option_e_report(result):
    months = ('January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December')
    date_str = result.temperature_highest[0]
    date = date_str.split('-')
    print("Highest: "+result.temperature_highest[1]+"C on "+months[int(date[1])-1]+" "+date[2])
    date_str = result.temperature_lowest[0]
    date = date_str.split('-')
    print("Lowest: " + result.temperature_lowest[1] + "C on " + months[int(date[1]) - 1] + " " + date[2])
    date_str = result.humidity[0]
    date = date_str.split('-')
    print("Humidity: " + result.humidity[1] + "% on " + months[int(date[1]) - 1] + " " + date[2])


if __name__ == '__main__':
    main()
