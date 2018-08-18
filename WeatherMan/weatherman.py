import argparse
import os
from FileParser import FileParser
from WeatherReport import WeatherReport


def parse_arguments():
    """This Function checks for command line arguments and parse it"""
    arg = argparse.ArgumentParser()
    arg.add_argument("-r", "--report", required=True,
                     help="Report Number You Want")
    arg.add_argument("-d", "--directory", required=True,
                     help="Directory in which data is placed")
    arg_values = vars(arg.parse_args())
    return int(arg_values["report"]), arg_values["directory"]


def validate_arguments(report, directory):
    """This function will be called after parsing of system arguments

    this function will check whether the argument recived is valid or not"""
    if report in [1, 2]:
        if not os.path.isdir(directory):
            print("Please Enter Valid Path of Directory")
            return False
        if not os.listdir(directory):
            print("Directory is Empty! Please Enter Valid Path")
            return False
        return True
    else:
        print("Please Enter Valid Report Number")
        print("1. For Annual Max/Min Temperature")
        print("2. For Hottest day of each year")
        return False


def generate_and_print_report():
    """This function will generate and print the report"""
    reporttype, directory = parse_arguments()
    if validate_arguments(reporttype, directory):
        parser = FileParser(directory)
        data = parser.file_reader()

        calculate = WeatherReport(data)
        annual_data = calculate.calculate(reporttype)


if __name__ == "__main__":
    generate_and_print_report()
