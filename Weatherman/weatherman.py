import argparse
import os
import sys

from file_parser import FileParser
from report_generator import ReportGenerator
from result_calculations import ResultCalculations


def check_arg_count(arguments):
    """Checks the number of command line arguments"""
    if arguments.e or arguments.a or arguments.c or arguments.b:
        return False
    else:
        return True


def is_actual_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


def parse_arguments():
    """Parse the command line arguments and returns the object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        help="Path to directory containing files (i.e weatherfiles/..)",
        type=is_actual_dir)
    parser.add_argument('-e', help="Enter the year (i.e 2002)")
    parser.add_argument('-a', help="Enter the year/month (i.e 2005/6)")
    parser.add_argument('-c', help="Enter the year/month (i.e 2011/03)")
    parser.add_argument(
        '-b', help="Enter the year/month (i.e 2011/03) -- Bonus")

    # Checking the count of arguments
    if check_arg_count(parser.parse_args()):
        print("Invalid number of arguments")
        sys.exit()
    else:
        print(parser.parse_args())
        return parser.parse_args()


def validate_arguments(argument, file_object, path_to_dir):
    """Validating the command line arguments"""
    if "/" in argument:
            year_and_month = argument.split("/")     # Split year & month
            year_and_month[1] = year_and_month[1].replace("0", "")
    else:
        print("Incorrect argument: ", argument)
        sys.exit()

    file_object.parse_file_monthly(
        path_to_dir, year_and_month[0], year_and_month[1])
    file_details = file_object.read_file()
    if not file_details:
        print(
            "Directory does not contain any file with such argument -> ",
            argument)
        sys.exit()
    else:
        return file_details


def parse_file(arguments):
    """Parsing the file (FileParser class) w.r.t the given arguments"""
    file_object = FileParser()     # File object
    results = ResultCalculations()  # results object
    path_to_dir = arguments.path

    # Condition for -e argument
    if arguments.e:
        if "/" in arguments.e:
            print("Incorrect argument: ", arguments.e)
            sys.exit()
        else:
            file_object.parse_file_yearly(path_to_dir, arguments.e)
            file_details = file_object.read_file()
            if not file_details:
                print(
                    "Directory does not contain any file with \
                    such argument -> ",
                    arguments.e)
            else:
                results.details = file_details
                yearly_details = {
                    "Max Temperature": results.calculate_highest_temp(),
                    "Min Temperature": results.calculate_lowest_temp(),
                    "Max Humidity": results.calculate_highest_humidity()
                }
                report_generator = ReportGenerator()        # Report object
                report_generator.generate_report_for_yearly_details(
                    yearly_details)
                file_details.clear()

    # Condition for -a argument
    if arguments.a:
        file_details = validate_arguments(
            arguments.a, file_object, path_to_dir
            )
        results.details = file_details
        monthly_details = results.calculate_average()
        report_generator = ReportGenerator()
        report_generator.generate_report_for_monthly_details(monthly_details)
        file_details.clear()

    # Condition for -c argument
    if arguments.c:
        file_details = validate_arguments(
            arguments.c, file_object, path_to_dir
            )
        results.details = file_details
        monthly_details = results.get_max_and_min_temperature()
        report_generator = ReportGenerator()
        report_generator.generate_graph(monthly_details)
        file_details.clear()

    # Condition for -b argument (Bonus)
    if arguments.b:
        file_details = validate_arguments(
            arguments.b, file_object, path_to_dir
            )
        results.details = file_details
        monthly_details = results.get_max_and_min_temperature()
        report_generator = ReportGenerator()
        report_generator.generate_horizontal_graph(monthly_details)
        file_details.clear()

if __name__ == "__main__":
    """Main - assembling the code and running the program"""
    arg = parse_arguments()
    parse_file(arg)
