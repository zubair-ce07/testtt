import argparse
import result_data_reader
import result_processor
import result_reporter


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
    users = result_data_reader.read_data()

    if cmd_arguments.present:
        # task 1: Showing the present students
        present_percentage = result_processor.get_percentage(users)
        result_reporter.show_percentage(present_percentage)
    if cmd_arguments.meritlist:
        # task 4: Showing the merit list
        groups = result_processor.create_merit_list(users, 50)
        result_reporter.generate_merit_list_files(groups)

    if cmd_arguments.passed:
        # performing task 3, scaled result percentage
        if "threshold" in cmd_arguments and "scale_ratio" in cmd_arguments:
            scaled_per = result_processor.get_percentage(
                users,
                cmd_arguments.threshold,
                cmd_arguments.scale_ratio
            )
            result_reporter.show_percentage(
                scaled_per,
                cmd_arguments.threshold,
                cmd_arguments.scale_ratio
            )
        # task 2, only passing threshold is given
        elif "threshold" in cmd_arguments:
            result_per = result_processor.get_percentage(
                users,
                cmd_arguments.threshold
            )
            result_reporter.show_percentage(
                result_per,
                cmd_arguments.threshold
            )
