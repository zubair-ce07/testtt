"""Some common methods for handling cmdline arguments"""
from datetime import date
import logging
import re
import constants

OPERATIONS = {
    "-e": constants.YEARLY_TEMPERATURE,
    "-a": constants.AVERAGE_TEMPERATURE,
    "-c": constants.ONE_LINE_CHART,
    "-d": constants.TWO_LINE_CHART
}


def display_usage_help():
    """Displays help message if wrong input is given."""
    message = ("weatherman.py <path/to/files>/ -[acde] <date> [-[acde] <date>]*"
               "\n\nParameters :-\n"
               "\t-e = Displays minimum and highest temperatures and highest"
               "humidity for given year\n"
               "\n\t-a = Displays average minimum temperature, maximum"
               "temperature and averagehumidity for given month\n"
               "\n\t-c = Displays one line chart for minimum and highest"
               "temperatures of given month\n"
               "\n\t-d = Displays two line chart for minimum and highest"
               "temperatures of given month\n"
               )
    print(message)


def validate_input(args):
    """ validate command line arguments

    :param args: command line args
    :return: true if input is correct else false
    """
    if len(args) < 4 or len(args) % 2 != 0:
        return False

    input_args = " ".join(args[2:])
    print(input_args)
    if not re.match(r"^(((-e \d{4})|(-[acd] \d{4}/((1[0-2])|(0?[1-9])))) ?)+$",
                    input_args):
        return False

    return True


def generate_date(year, month=1, day=1):
    """Generate and return datetime.date object"""
    try:
        return date(int(year), int(month), int(day))
    except ValueError as err:
        logging.error("Cannot convert values %d-%d-%d to date object.\n%s",
                      year,
                      month,
                      day,
                      str(err))



def parse_input(args):
    """Parse the input to decide what to do."""

    path_to_files = args[1]

    report_operations = []

    for arg_index in range(2, len(args), 2):
        report_type = OPERATIONS[args[arg_index]]
        if report_type == constants.YEARLY_TEMPERATURE:
            report_date = generate_date(args[arg_index + 1])
        else:
            report_date = generate_date(args[arg_index + 1][:4],
                                        args[arg_index + 1][5:])
        report_operations.append({
            "report_type": report_type,
            "report_date": report_date
        })

    return {
        "path_to_files": path_to_files,
        "report_operations": report_operations
    }
