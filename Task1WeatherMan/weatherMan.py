import argparse
import Task1
import Task2
import Task3


# task1
def execute_task1(input_flag):
    Task1.highest_lowest_temperature_and_humidity(input_flag)


# task2
def execute_task2(input_flag):
    Task2.print_highest_and_lowest_average_for_month(input_flag)


# task3
def execute_task3(input_flag):
    Task3.print_highest_lowest_temperatures(input_flag)


parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-e', '--task1', help='use this for task 1')
parser.add_argument('-a', '--task2', help='use this for task 2')
parser.add_argument('-c', '--task3', help='use this for task 3')
args = parser.parse_args(None)


if __name__ == '__main__':
    if args.task1 is not None:
        execute_task1(args.task1)
    if args.task2 is not None:
        execute_task2(args.task2)
    if args.task3 is not None:
        execute_task3(args.task3)
