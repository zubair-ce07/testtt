import argparse
import os
from weather_reports import WeatherReports

def main():
    """ Main Function """
    # Read Command Line arguments and proceed if the arguments are valid.
    parser = argparse.ArgumentParser(
        description='A utility for processing weather data of Lahore.')
    parser.add_argument('-e', action='store_true',
                        help='Sets the year for the annual report')
    parser.add_argument('-a', action='store_true',
                        help="Sets the month for average highest "
                             "temperature,\ average lowest temperature,"
                             "average humidity.")
    parser.add_argument('-c', action='store_true',
                        help="Sets the month for bar charts for daily "
                             "highest and lowest temperatures")
    parser.add_argument('-s', action='store_true',
                        help="Sets the month for stack chart for daily "
                             "highest and lowest temperatures")
    parser.add_argument('-b', action='store_true',
                        help="Sets the month for graphical bar chart for "
                             "daily highest and lowest temperatures")
    parser.add_argument('date', action="store",
                        help='Report date in YYYY/MM format')
    parser.add_argument('data_dir', action="store",
                        help='Path of directory containing weather data files')

    args = parser.parse_args()
    data_directory_path = args.data_dir

    if not os.path.isdir(data_directory_path):
        exit('Specified directory does not exist')
    if args.e:
        WeatherReports.annual_extrema(args.date, data_directory_path)
    if args.a:
        WeatherReports.monthly_averages(args.date, data_directory_path)
    if args.c:
        WeatherReports.monthly_console_bar_chart(args.date, data_directory_path)
    if args.s:
        WeatherReports.monthly_console_stack_chart(args.date, data_directory_path)
    if args.b:
        WeatherReports.monthly_gui_bar_chart(args.date, data_directory_path)

if __name__ == "__main__":
    main()
