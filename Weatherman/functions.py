import sys
import csv
from FIleGetters import get_file_names
from Classes import WeatherReadings , YearlyWeatherReport, MonthlyReport


def get_yearly_record(filename, args):

    weather_files = get_file_names(filename,args)
    weather_files_count = len(weather_files)
    flag = False

    if weather_files:

        yearly_report = YearlyWeatherReport()

        for index in range(0, weather_files_count):

            input_file = csv.DictReader(open(weather_files[index]))

            for row in input_file:

                weather = WeatherReadings(row)

                if weather.max_temp and int(weather.max_temp) > yearly_report.highest_temp:
                    yearly_report.highest_temp = int(weather.max_temp)
                    yearly_report.highest_temp_day = weather.get_month_day()

                if flag:
                        if weather.min_temp and int(weather.max_temp) < yearly_report.lowest_temp:
                            yearly_report.lowest_temp = int(weather.max_temp)
                            yearly_report.lowest_temp_day = weather.get_month_day()
                else:
                        yearly_report.lowest_temp_day = weather.get_month_day()
                        yearly_report.lowest_temp = row.get('Min TemperatureC')
                        flag = True

                if weather.max_humidity and int(weather.max_humidity) > yearly_report.highest_humidity:
                    yearly_report.highest_humidity = int(weather.max_humidity)
                    yearly_report.highest_humidity_day = weather.get_month_day()

        yearly_report.results()

    else:
        error_msg(args.e)


def get_monthly_average(filename,args):

    file_name = get_file_names(filename,args)

    monthly_report = MonthlyReport()

    if file_name:

        input_file = csv.DictReader(open(file_name[0]))

        for row in input_file:

            weather = WeatherReadings(row)

            monthly_report.days_count = monthly_report.days_count + 1

            if weather.max_temp:
                monthly_report.total_max_temp = monthly_report.total_max_temp + int(weather.max_temp)

            if weather.min_temp:
                monthly_report.total_min_temp = monthly_report.total_min_temp + int(weather.min_temp)

            if weather.mean_humidity:
                monthly_report.total_mean_humidity = monthly_report.total_mean_humidity + int(weather.mean_humidity)

        monthly_report.results()

    else:
        error_msg(args.a)


def get_monthly_record_bars(filename, args):

    max_temp_values = []
    min_temp_values = []
    days = []

    file_name = get_file_names(filename,args)

    if file_name:

        input_file = csv.DictReader(open(file_name[0]))

        for row in input_file:

                weather = WeatherReadings(row)
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
    else:
        error_msg(args.c)


def get_monthly_single_line_bars(filename, args):

    max_temp_values = []
    min_temp_values = []
    days = []

    file_name = get_file_names(filename,args)

    if file_name:

        input_file = csv.DictReader(open(file_name[0]))

        for row in input_file:

                weather = WeatherReadings(row)
                max_temp_values.append(weather.max_temp)
                min_temp_values.append(weather.min_temp)
                days.append(weather.get_day())

        print(weather.get_month_year())

        for index in range(0, len(days)):

            sys.stdout.write('\033[1;30m' + days[index] + ' ')
            if max_temp_values[index]:
                printer_single_line_chart(int(max_temp_values[index]), int(min_temp_values[index]) )
            else:
                print 'N/A'
    else:
        error_msg(args.d)


def printer_bars_charts(temp_value, color):

    if color:
        for i in range(0 , temp_value):

            sys.stdout.write('\033[1;31m+')
    else:

        for i in range(0, temp_value):
            sys.stdout.write('\033[1;34m+')
    sys.stdout.write('\033[1;30m ' + str(temp_value) + 'C')
    sys.stdout.write('\n')


def printer_single_line_chart(max_temp_value, min_temp_value) :

    for i in range(0 , min_temp_value):

        sys.stdout.write('\033[1;34m+')

    for i in range(0, max_temp_value):
            sys.stdout.write('\033[1;31m+')
    sys.stdout.write('\033[1;30m  ' + str(min_temp_value) + "C - " + str(max_temp_value) + 'C')
    sys.stdout.write('\n')


def error_msg(arg):
    print "File Not Found For Argument {}".format(arg)
    print "Enter Year Between 2004 to 2016 \n"
