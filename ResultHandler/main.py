import argparse
from result_data_reader import ResultDataReader
from result_processor import ResultProcessor
from result_reporter import ResultReporter


def parse_arguments():
    """
    This function parses and validates the given arguments
    """
    result_parser = argparse.ArgumentParser("Process Result Information")
    result_parser.add_argument("-present",
                               "-pr",
                               action="store_true",
                               help="Percentage of Students who attempted")

    result_parser.add_argument("-passed",
                               "-pa",
                               help="Students who passed",
                               action="store_true")

    result_parser.add_argument("-meritlist",
                               "-m",
                               help="Show the selected students",
                               action="store_true")

    result_parser.add_argument("-pc",
                               "-passingcriteria",
                               "--threshold",
                               type=int,
                               default=argparse.SUPPRESS,
                               help="Passing Criteria")

    result_parser.add_argument("-s",
                               "-scale",
                               "--scale_ratio",
                               type=int,
                               default=argparse.SUPPRESS,
                               help="Scale the result by given ratio")
    return result_parser.parse_args()


if __name__ == '__main__':
    """
            This function compares the parsed input parameters
            and calls the respective functions.
            """
    cmd_arguments = parse_arguments()
    result_data_reader = ResultDataReader("data.csv")
    users = result_data_reader.read_data()

    if cmd_arguments.present:
        # task 1: Showing the present students
        present_percentage = ResultProcessor.get_present_percentage(users)
        ResultReporter.show_present_percentage(present_percentage)
    if cmd_arguments.meritlist:
        # task 4: Showing the merit list
        groups = ResultProcessor.create_merit_list(users, 50)
        ResultReporter.generate_merit_list_files(groups)

    if cmd_arguments.passed:
        # performing task 3, scaled result percentage
        if "threshold" in cmd_arguments and "scale_ratio" in cmd_arguments:
            scaled_per = ResultProcessor.get_scaled_percentage(
                users,
                cmd_arguments.threshold,
                cmd_arguments.scale_ratio
            )
            ResultReporter.show_scaled_percentage(
                scaled_per,
                cmd_arguments.threshold,
                cmd_arguments.scale_ratio
            )
        # task 2, only passing threshold is given
        elif "threshold" in cmd_arguments:
            result_per = ResultProcessor.get_passed_percentage(
                users,
                cmd_arguments.threshold
            )
            ResultReporter.show_passed_percentage(
                result_per,
                cmd_arguments.threshold
            )
