import argparse
import os
import calendar

import reader
import extractor
import reportgenerator


def get_file_name(files_dir, year, month=None):
    if month is not None:
        return [f'{files_dir}Murree_weather_{year}_{calendar.month_abbr[int(month)]}.txt']
    else:
        files_prefix = f'Murree_weather_{year}_'
        return [files_dir + file for file in os.listdir(files_dir) if file.startswith(files_prefix)]


def main():
    # creating argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('files_dir', type=str, help='Directory containing weather files')
    parser.add_argument('-e', metavar='e', type=str, nargs='?',
                        help=('For a given year display the highest temperature and day, lowest temperature and day, '
                              'most humid day and humidity.'))
    parser.add_argument('-a', metavar='a', type=str, nargs='?',
                        help=('For a given month display the average highest temperature, average lowest temperature, '
                              'average mean humidity.'))
    parser.add_argument('-c', metavar='c', type=str, nargs='?',
                        help=('For a given month draw two horizontal bar charts on the console for the highest and '
                              'lowest temperature on each day. Highest in red and lowest in blue.'))
    args = parser.parse_args()

    # extracting arguments
    files_dir = args.files_dir + '/'
    e = args.e
    a = args.a
    c = args.c

    if e is not None:
        print(f'-e {e}')

        year = e
        year_file_names = get_file_name(files_dir, year)
        weather_readings = reader.reader(year_file_names)
        results = extractor.extract_year_info(weather_readings)
        reportgenerator.generate_year_info_report(results)

    if a is not None:
        print(f'-a {a}')

        year, month = a.split('/')
        file_name = get_file_name(files_dir, year, month)
        weather_readings = reader.reader(file_name)
        results = extractor.extract_month_info(weather_readings)
        reportgenerator.generate_month_info_report(results)

    if c is not None:
        print(f'-c {c}')

        year, month = c.split('/')
        file_name = get_file_name(files_dir, year, month)
        weather_readings = reader.reader(file_name)
        reportgenerator.generate_month_temperature_detailed_report(weather_readings)


if __name__ == "__main__":
    main()
