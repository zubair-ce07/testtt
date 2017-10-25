import sys
import csv
from FIleGetters import get_file_names
from Classes import WeatherReading , YearlyWeatherReport, MonthlyReport


def get_yearly_record(directory_path, args):

    weather_files = get_file_names(directory_path,args)
    if not weather_files:
        error_msg(args.e)
    yearly_report = YearlyWeatherReport()

    for files in weather_files:
        input_file = csv.DictReader(open(files))

        for row in input_file:
            weather = WeatherReading(row)
            yearly_report.complete_records.append(weather)

    yearly_report.print_report()


def get_monthly_average(directory_path,args):

    file_name = get_file_names(directory_path,args)

    monthly_report = MonthlyReport()

    if not file_name:
        error_msg(args.a)

    input_file = csv.DictReader(open(file_name[0]))

    for row in input_file:

        weather = WeatherReading(row)

        monthly_report.days_count = monthly_report.days_count + 1

        if weather.max_temp:
            monthly_report.total_max_temp = monthly_report.total_max_temp + weather.max_temp

        if weather.min_temp:
            monthly_report.total_min_temp = monthly_report.total_min_temp + weather.min_temp

        if weather.mean_humidity:
            monthly_report.total_mean_humidity = monthly_report.total_mean_humidity + weather.mean_humidity

    monthly_report.print_report()


def get_monthly_record_bars(directory_path, args):

    max_temp_values = []
    min_temp_values = []
    days = []

    file_name = get_file_names(directory_path,args)

    if not file_name:
        error_msg(args.c)

    input_file = csv.DictReader(open(file_name[0]))

    for row in input_file:

            weather = WeatherReading(row)
            max_temp_values.append(weather.max_temp)
            min_temp_values.append(weather.min_temp)
            days.append(weather.get_day())

    print(weather.get_month_year())

    for index in range(0,len(days)):

        sys.stdout.write('\033[1;30m' + days[index] + ' ')
        if max_temp_values[index]:
            printer_bars_charts(int(max_temp_values[index]),1)
        else:
            print('N/A')

        sys.stdout.write(days[index] +' ')
        if min_temp_values[index]:
            printer_bars_charts(int(min_temp_values[index]),0)
        else:
            print('N/A')


def get_monthly_single_line_bars(directory_path, args):

    max_temp_values = []
    min_temp_values = []
    days = []

    file_name = get_file_names(directory_path,args)

    if not file_name:
        error_msg(args.d)
        
    input_file = csv.DictReader(open(file_name[0]))

    for row in input_file:

            weather = WeatherReading(row)
            max_temp_values.append(weather.max_temp)
            min_temp_values.append(weather.min_temp)
            days.append(weather.get_day())
    print '\n'
    print(weather.get_month_year())

    for index in range(0, len(days)):
        sys.stdout.write('\033[1;30m' + days[index] + ' ')
        if max_temp_values[index]:
            printer_single_line_chart(int(max_temp_values[index]), int(min_temp_values[index]) )
        else:
            print 'N/A'


def printer_bars_charts(temperature_value, color):

    if color:
        for i in range(0 , temperature_value):

            sys.stdout.write('\033[1;31m+')
    else:

        for i in range(0, temperature_value):
            sys.stdout.write('\033[1;34m+')
    sys.stdout.write('\033[1;30m ' + str(temperature_value) + 'C')
    sys.stdout.write('\n')


def printer_single_line_chart(max_temp_value, min_temp_value) :

    for values in range(0 , min_temp_value):

        sys.stdout.write('\033[1;34m+')

    for i in range(0, max_temp_value):
            sys.stdout.write('\033[1;31m+')
    sys.stdout.write('\033[1;30m  ' + str(min_temp_value) + "C - " + str(max_temp_value) + 'C')
    sys.stdout.write('\n')


def error_msg(arg):
    print "File Not Found For Argument {}".format(arg)
    print "Enter Year Between 2004 to 2016 \n"
