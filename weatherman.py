
import glob
import argparse
import datetime
from itertools import islice
from colr import Colr as C

from temperature import Temperature
import report


files_directory_path = '/home/tanveer/the-lab/weatherfiles/weatherfiles/*.txt'
all_files_name_list = glob.glob(files_directory_path)
file_record = []

for name in all_files_name_list:
    file_record.append(name[48:])

years_list = list(range(2004, 2017))
months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
yearly_monthly_data_list = []


def read_monthly_file_data(year, month):
    temperature_object_list_for_single_month = []
    # append suffix and prefix to file name
    complete_file_name = '/home/tanveer/the-lab/weatherfiles/weatherfiles/' + 'Murree_weather_' \
                         + repr(year) + '_' + month + '.txt'

    if complete_file_name in all_files_name_list:
        try:
            with open(complete_file_name) as f:
                # for line in f:
                for line in islice(f, 1, None):

                    splitted_line = line.split(',')

                    date_portion_in_splitted_line = splitted_line[0]
                    splitted_date = date_portion_in_splitted_line.split('-')

                    formatted_date = datetime.date(year=int(splitted_date[0]), month=int(splitted_date[1]),
                                          day=int(splitted_date[2]))
                    max_temperature = splitted_line[1]
                    mean_temperature = splitted_line[2]
                    min_temperature = splitted_line[3]
                    max_humidity = splitted_line[7]
                    mean_humidity = splitted_line[8]
                    min_humidity = splitted_line[9]

                    # preparing Temperature object to store in list
                    temperature_object_ready_to_append = Temperature(formatted_date, max_temperature,
                                                                     mean_temperature, min_temperature, max_humidity,
                                                                     mean_humidity, min_humidity)
                    temperature_object_list_for_single_month.append(temperature_object_ready_to_append)
                return temperature_object_list_for_single_month
        except FileNotFoundError as err:
                print(err)
    else:
        return False


def file_exist(year, month):
    file_name = 'Murree_weather_' + repr(year) + '_' + month + '.txt'
    if file_name in file_record:
        return True
    else:
        return False


def read_all_weather_data():
    global yearly_monthly_data_list
    global file_record
    global months_list
    yearly_monthly_data_list = {year: {month: read_monthly_file_data(year, month) for month in months_list
                                       if file_exist(year, month) is True} for year in years_list}

    # for year in years_list:
    #     for month in months_list:
    #         if file_exist(year, month):
    #             yearly_monthly_data_list.append({year: {month: read_monthly_file_data('Murree_weather_' + repr(year) + '_' + month)}})


if __name__ == '__main__':

    # Read all files and store and data structure named yearly_monthly_data_list
    read_all_weather_data()

    # Initialize the parser
    parser = argparse.ArgumentParser(description="My Main Method Execution.....!")

    # Adding the positional parameters into parser
    parser.add_argument('-e', 'operator_1', help="Indication for operation.")
    parser.add_argument('date_1', help="Year/month as input.")
    parser.add_argument('operator_2', help="Indication for operation.", nargs='?')
    parser.add_argument('date_2', help="Year/month as input.", nargs='?')
    parser.add_argument('operator_3', help="Indication for operation.", nargs='?')
    parser.add_argument('date_3', help="Year/month as input.", nargs='?')

    # Parse the arguments coming from terminal
    arguments = parser.parse_args()

# Working on "e"
    if arguments.operator_1 == 'e':
        args = arguments.date_1.split('/')
        year = int(args[0])
        if int(year) in years_list:
            report.yearly_lowest_highest_values(int(year), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{year}{C(') Does Not Exist....!', fore='red')}")
            print('\n')
    elif arguments.operator_2 == 'e':
        args = arguments.date_2.split('/')
        year = int(args[0])
        if int(year) in years_list:
            report.yearly_lowest_highest_values(int(year), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{year}{C(') Does Not Exist....!', fore='red')}")
            print('\n')
    elif arguments.operator_3 == 'e':
        args = arguments.date_3.split('/')
        year = int(args[0])
        if int(year) in years_list:
            report.yearly_lowest_highest_values(int(year), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{year}{C(') Does Not Exist....!', fore='red')}")
            print('\n')

    # Working on "a"
    if arguments.operator_1 == 'a':
        args = arguments.date_1.split('/')
        year = int(args[0])
        month = int(args[1])
        if int(month) in range(1, 12):
            file_name = 'Murree_weather_' + str(year) + '_' + months_list[int(month) - 1] + '.txt'
        else:
            file_name = 'Murree_weather_' + str(year) + '_' + str(month) + '.txt'
            # print(file_name)

        if file_name in file_record:
            report.monthly_average_values(int(year), int(month), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{file_name}{C(') Does Not Exist....!', fore='red')}")
            print('\n')
    elif arguments.operator_2 == 'a':
        args = arguments.date_2.split('/')
        year = int(args[0])
        month = int(args[1])
        if int(month) in range(1, 12):
            file_name = 'Murree_weather_' + str(year) + '_' + months_list[int(month) - 1] + '.txt'
        else:
            file_name = 'Murree_weather_' + str(year) + '_' + str(month) + '.txt'
            # print(file_name)

        if file_name in file_record:
            report.monthly_average_values(int(year), int(month), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{file_name}{C(') Does Not Exist....!', fore='red')}")
            print('\n')
    elif arguments.operator_3 == 'a':
        args = arguments.date_3.split('/')
        year = int(args[0])
        month = int(args[1])
        if int(month) in range(1, 12):
            file_name = 'Murree_weather_' + str(year) + '_' + months_list[int(month) - 1] + '.txt'
        else:
            file_name = 'Murree_weather_' + str(year) + '_' + str(month) + '.txt'
            # print(file_name)

        if file_name in file_record:
            report.monthly_average_values(int(year), int(month), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{file_name}{C(') Does Not Exist....!', fore='red')}")
            print('\n')

    # Working on "c"
    if arguments.operator_1 == 'c':
        args = arguments.date_1.split('/')
        year = int(args[0])
        month = int(args[1])
        if int(month) in range(1, 12):
            file_name = 'Murree_weather_' + str(year) + '_' + months_list[int(month) - 1] + '.txt'
        else:
            file_name = 'Murree_weather_' + str(year) + '_' + str(month) + '.txt'

        if file_name in file_record:
            report.horizontal_bar_for_given_month(int(year), int(month), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{file_name}{C(') Does Not Exist....!', fore='red')}")
            print('\n')
    elif arguments.operator_2 == 'c':
        args = arguments.date_2.split('/')
        year = int(args[0])
        month = int(args[1])
        if int(month) in range(1, 12):
            file_name = 'Murree_weather_' + str(year) + '_' + months_list[int(month) - 1] + '.txt'
        else:
            file_name = 'Murree_weather_' + str(year) + '_' + str(month) + '.txt'

        if file_name in file_record:
            report.horizontal_bar_for_given_month(int(year), int(month), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{file_name}{C(') Does Not Exist....!', fore='red')}")
            print('\n')
    elif arguments.operator_3 == 'c':
        args = arguments.date_3.split('/')
        year = int(args[0])
        month = int(args[1])
        if int(month) in range(1, 12):
            file_name = 'Murree_weather_' + str(year) + '_' + months_list[int(month) - 1] + '.txt'
        else:
            file_name = 'Murree_weather_' + str(year) + '_' + str(month) + '.txt'

        if file_name in file_record:
            report.horizontal_bar_for_given_month(int(year), int(month), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{file_name}{C(') Does Not Exist....!', fore='red')}")
            print('\n')

    # Working on "d"
    if arguments.operator_1 == 'd':
        args = arguments.date_1.split('/')
        year = int(args[0])
        month = int(args[1])
        if int(month) in range(1, 12):
            file_name = 'Murree_weather_' + str(year) + '_' + months_list[int(month) - 1] + '.txt'
        else:
            file_name = 'Murree_weather_' + str(year) + '_' + str(month) + '.txt'

        if file_name in file_record:
            report.mixed_bar_for_given_month(int(year), int(month), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{file_name}{C(') Does Not Exist....!', fore='red')}")
            print('\n')
    elif arguments.operator_2 == 'd':
        args = arguments.date_2.split('/')
        year = int(args[0])
        month = int(args[1])
        if int(month) in range(1, 12):
            file_name = 'Murree_weather_' + str(year) + '_' + months_list[int(month) - 1] + '.txt'
        else:
            file_name = 'Murree_weather_' + str(year) + '_' + str(month) + '.txt'

        if file_name in file_record:
            report.mixed_bar_for_given_month(int(year), int(month), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{file_name}{C(') Does Not Exist....!', fore='red')}")
            print('\n')
    elif arguments.operator_3 == 'd':
        args = arguments.date_3.split('/')
        year = int(args[0])
        month = int(args[1])
        if int(month) in range(1, 12):
            file_name = 'Murree_weather_' + str(year) + '_' + months_list[int(month) - 1] + '.txt'
        else:
            file_name = 'Murree_weather_' + str(year) + '_' + str(month) + '.txt'

        if file_name in file_record:
            report.mixed_bar_for_given_month(int(year), int(month), yearly_monthly_data_list, months_list)
        else:
            print('\n')
            print(f"{C('File (', fore='red')}{file_name}{C(') Does Not Exist....!', fore='red')}")
            print('\n')
