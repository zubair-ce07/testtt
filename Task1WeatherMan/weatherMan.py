import argparse

import helperfile
import task1
import task2
import task3


# task1
def execute_task1(input_string):
    names_of_files = helperfile.get_file_names_for_year(input_string)
    if names_of_files:
        task1.highest_lowest_temperature_and_humidity(input_string)
    else:
        print("Data for year", input_string, "is not available")
        return


# task2
def execute_task2(input_string):
    file_name = helperfile.validate_year_month_input(input_string)
    if file_name:
        task2.print_highest_and_lowest_average_for_month(file_name)


# task3
def execute_task3(input_string):
    file_name = helperfile.validate_year_month_input(input_string)
    if file_name:
        components = helperfile.get_date_components(input_string)
        task3.print_highest_lowest_temperatures(file_name, components)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-e', '--task1', help='use this for task 1')
    parser.add_argument('-a', '--task2', help='use this for task 2')
    parser.add_argument('-c', '--task3', help='use this for task 3')
    args = parser.parse_args(None)

    if args.task1 is not None:
        execute_task1(args.task1)
    if args.task2 is not None:
        execute_task2(args.task2)
    if args.task3 is not None:
        execute_task3(args.task3)
