import sys
from FIleGetters import get_file_names, get_file_names_one,get_file_names_two
from Classes import Weather , YearlyWeatherReport, MonthlyReport


def year(args):

    weather_files = get_file_names(args)
    weather_files_count = len(weather_files)

    yearly_report = YearlyWeatherReport()
    count = 0

    for index in range(0, weather_files_count):

        f = open(weather_files[index], "r")

        line = f.readline()
        line = f.readline()

        first_line = line.split(',')

        first_min_temp = int(first_line[3])

        while line:

            split_line = line.split(',')
            weather = Weather(split_line)

            if weather.max_temp and int(weather.max_temp) > yearly_report.highest_temp:
                yearly_report.highest_temp = int(weather.max_temp)
                yearly_report.highest_temp_day = weather.get_month_day()

            if count >= 1:
                    if weather.min_temp and int(weather.max_temp) < yearly_report.lowest_temp:
                        yearly_report.lowest_temp = int(weather.max_temp)
                        yearly_report.lowest_temp_day = weather.get_month_day()
            else:
                    yearly_report.lowest_temp_day = weather.get_month_day()
                    yearly_report.lowest_temp = first_min_temp

            if weather.max_humidity and int(weather.max_humidity) > yearly_report.highest_humidity:
                yearly_report.highest_humidity = int(weather.max_humidity)
                yearly_report.highest_humidity_day = weather.get_month_day()

            count = count + 1
            line = f.readline()

    yearly_report.results()


def month(args):

    files_list = get_file_names_one(args)

    monthly_report = MonthlyReport()

    f = open(files_list[0], "r")

    line = f.readline()
    line = f.readline()

    while line:

        split_line = line.split(',')
        weather = Weather(split_line)

        monthly_report.days_count = monthly_report.days_count + 1

        if weather.max_temp:
            monthly_report.total_max_temp = monthly_report.total_max_temp + int(weather.max_temp)

        if weather.min_temp:
            monthly_report.total_min_temp = monthly_report.total_min_temp + int(weather.min_temp)

        if weather.mean_humidity:
            monthly_report.total_mean_humidity = monthly_report.total_mean_humidity + int(weather.mean_humidity)

        line = f.readline()

    monthly_report.results()


def month_bars(args):

    flag = False
    max_temp_list = []
    min_temp_list = []
    day = []

    file_name = get_file_names_two(args)


    f = open(file_name[0], "r")

    line = f.readline()
    line = f.readline()

    while line:

        split_line = line.split(',')
        weather = Weather(split_line)

        max_temp_list.append(weather.max_temp)
        min_temp_list.append(weather.min_temp)
        day.append(weather.get_day())

        line = f.readline()

    print(weather.get_month_year())

    if len(args.c) == 7:
        for index in range(0,len(day)):

            sys.stdout.write('\033[1;30m' + day[index] + ' ')
            if max_temp_list[index]:
                printer(int(max_temp_list[index]),1)
            else:
                print('N/A')

            sys.stdout.write(day[index] +' ')
            if min_temp_list[index]:
                printer(int(min_temp_list[index]),0)
            else:
                print('N/A')

    else:
        for index in range(0, len(day)):

            sys.stdout.write('\033[1;30m' + day[index] + ' ')
            if max_temp_list[index]:
                printer_two(int(max_temp_list[index]), int(min_temp_list[index]) )
            else:
                print 'N/A'


def printer(temp_value, color):

    if color:
        for i in range(0 , temp_value):

            sys.stdout.write('\033[1;31m+')
    else:

        for i in range(0, temp_value):
            sys.stdout.write('\033[1;34m+')
    sys.stdout.write('\033[1;30m ' + str(temp_value) + 'C')
    sys.stdout.write('\n')


def printer_two(max_temp_value, min_temp_value) :

    for i in range(0 , min_temp_value):

        sys.stdout.write('\033[1;34m+')

    for i in range(0, max_temp_value):
            sys.stdout.write('\033[1;31m+')
    sys.stdout.write('\033[1;30m  ' + str(min_temp_value) + "C - " + str(max_temp_value) + 'C')
    sys.stdout.write('\n')
