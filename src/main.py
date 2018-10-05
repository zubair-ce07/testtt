#!/usr/bin/python3
import argparse
from data_holder import WeatherData
import output_generator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=str)
    parser.add_argument("-e", type=str, nargs='*')
    parser.add_argument("-a", type=str, nargs='*')
    parser.add_argument("-c", type=str, nargs="*")
    args = parser.parse_args()

    weather_data = WeatherData()
    all_data = weather_data.all_weather_record(args.dir_path)

    output_writer = output_generator.OutputGenerator()

    if args.e:
        for month in args.e:
            output_writer.print_extreme_record(
                weather_data.year_record(all_data, month))
    if args.a:
        for month in args.a:
            output_writer.print_average_record(
                weather_data.month_record(all_data, month))
    if args.c:
        for month in args.c:
            output_writer.print_temp_chart_bounus(
                weather_data.month_record(all_data, month))


if __name__ == '__main__':
    main()
