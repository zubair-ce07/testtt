from argparse import ArgumentParser

import glob


def get_month(month):
    if month == "Jan":
        return 1
    if month == "Feb":
        return 2
    if month == "Mar":
        return 3
    if month == "Apr":
        return 4
    if month == "May":
        return 5
    if month == "Jun":
        return 6
    if month == "Jul":
        return 7
    if month == "Aug":
        return 8
    if month == "Sep":
        return 9
    if month == "Oct":
        return 10
    if month == "Nov":
        return 11
    if month == "Dec":
        return 12


def get_eng_month(month):
    if month == 1:
        return "Jan"
    if month == 2:
        return "Feb"
    if month == 3:
        return "Mar"
    if month == 4:
        return "Apr"
    if month == 5:
        return "May"
    if month == 6:
        return "June"
    if month == 7:
        return "Jul"
    if month == 8:
        return "Aug"
    if month == 9:
        return "Sep"
    if month == 10:
        return "Oct"
    if month == 11:
        return "Nov"
    if month == 12:
        return "Dec"


def get_dictionary(dictionary,
                   keys):
    for key in keys:
        dictionary = dictionary[key]
    return dictionary


def iterate_dictionary(dictionary,
                       keys,
                       value):
    dictionary = get_dictionary(dictionary,
                                keys[:-1])
    dictionary[keys[-1]] = value


def determine_year(raw_year):
    raw_year = str(raw_year)
    years = raw_year.split('/')
    return years


def daily_high_low(main_dictionary,
                   year,
                   month):
    year = str(year)
    month = str(month)
    month_data = main_dictionary[year][month]
    print()
    for index, days in enumerate(month_data):
        if days[0] != 0.0 and days[2] != 0.0:
            print('\033[1;34m')
            print(index, end=' ')
            for i in range(int(days[0])):
                print('+', end='')
            print('\033[1;31m', end='')
            for i in range(int(days[2])):
                print('+', end='')
            print(' \033[1;34m' + str(int(days[2])) + 'C', '- ', end='')
            print('\033[1;31m' + str(int(days[0])) + 'C')
    print("\033[0;0m")


def monthly_average(main_dictionary,
                    year,
                    month):
    year = str(year)
    month = str(month)
    month_data = main_dictionary[year][month]
    result = [0, 0, 0]
    total = -1
    for total, days in enumerate(month_data):
        result[0] += days[0]
        result[1] += days[2]
        result[2] += days[7]
    result[0] = round(result[0]/total, 3)
    result[1] = round(result[1]/total, 3)
    result[2] = round(result[2]/total, 3)

    print()
    print('Highest Average: ' + str(int(result[0])) + 'C')
    print('Lowest Average: ' + str(int(result[1])) + 'C')
    print('Average Mean: ' + str(int(result[2])) + '%')


def monthly_highest(main_dictionary,
                    year,
                    month):
    year = str(year)
    month = str(month)
    result = []
    month_data = main_dictionary[year][month]
    result.append(month_data[0][0])
    result.append(1)
    result.append(month_data[0][2])
    result.append(1)
    result.append(month_data[0][6])
    result.append(1)
    for index, days in enumerate(month_data):
        if result[0] < days[0]:
            result[0] = days[0]
            result[1] = get_eng_month(int(month)) + " " + str(index + 1)
        if result[2] > days[2]:
            result[2] = days[2]
            result[3] = get_eng_month(int(month)) + " " + str(index + 1)
        if result[4] < days[6]:
            result[4] = days[6]
            result[5] = get_eng_month(int(month)) + " " + str(index + 1)
    return result


def yearly_calculations(main_dictionary,
                        year):
    months = main_dictionary[year]
    once = False
    result = []
    for month in months:
        if once is False:
            result = monthly_highest(main_dictionary, year, month)
        once = True
        new_result = monthly_highest(main_dictionary, year, month)
        if new_result[0] > result[0]:
            result[0] = new_result[0]
            result[1] = new_result[1]
        if new_result[2] < result[2]:
            result[2] = new_result[2]
            result[3] = new_result[3]
        if new_result[4] > result[4]:
            result[4] = new_result[4]
            result[5] = new_result[5]

    print('Highest: ' + str(result[0]) + 'C on ' + str(result[1]))
    print('Lowest: ' + str(result[2]) + 'C on ' + str(result[3]))
    print('humidity: ' + str(result[4]) + '% on ' + str(result[5]))


def str_convert_int(list1):
    new_list = [[element or '0' for element in rows] for rows in list1]
    for rows in new_list:
        for i in range(20):
            rows[i] = float(rows[i])
    return new_list


def parser(main_dictionary,
           dir_name):
    print(dir_name)
    list_already_run = []
    for file_names in glob.iglob(dir_name + '/*.txt',
                                 recursive=True):
        year_and_month = file_names.split('.')
        year_and_month = year_and_month[0].split('_')
        if year_and_month[2] not in list_already_run:
            list_already_run.append(str(year_and_month[2]))
            main_dictionary[str(year_and_month[2])] = {}
        list_month = list(str(year_and_month[2]))
        list_month.append(get_month(str(year_and_month[3])))
        with open(file_names,
                  'r') as file:
            next(file)
            monthly_data = []
            for line_of_file in file:
                day_data = line_of_file.split(',')
                date = day_data[0].split('-')
                iterate_dictionary(main_dictionary, date[0:2], None)
                monthly_data.append(day_data[1:22])
                monthly_data = str_convert_int( monthly_data)
            iterate_dictionary(main_dictionary, date[0:2], monthly_data)
    return main_dictionary


def main():

    arg_parser = ArgumentParser(description='Process some integer')
    arg_parser.add_argument('path', type=str, nargs='+',
                            help='Collect the data from Directory')
    arg_parser.add_argument('-e', type=str, nargs='+',
                            help='Find the highest temperature and day, '
                                 'lowest temperature and day, most humid day '
                                 '(Single Month)')
    arg_parser.add_argument('-a', type=str, nargs='+',
                            help='Find the average highest temperature,'
                                 ' average lowest temperature, average mean '
                                 'humidity (Range of Months)')
    arg_parser.add_argument('-c', type=str, nargs='+',
                            help='Draws two horizontal bar charts for the'
                                 ' highest and lowest temperature on each  '
                                 'day. Highest in  red and lowest in blue. ('
                                 'Range of Months)')
    args = arg_parser.parse_args()
    main_dictionary = {}
    main_dictionary = parser(main_dictionary, args.path[0])
    try:
        if args.e:
            years = determine_year(args.e[0])
            yearly_calculations(main_dictionary,
                                years[0])

        if args.a:
            years = determine_year(args.a[0])
            monthly_average(main_dictionary,
                            years[0],
                            years[1])

        if args.c:
            years = determine_year(args.c[0])
            daily_high_low(main_dictionary,
                           years[0],
                           years[1])
    except KeyError:
        print("Invalid Input")


main()
