import argparse
from result_data_reader import ResultDataReader
from result_processor import ResultProcessor
from result_reporter import ResultReporter


class Result:
    """
    This class calls the corresponding functions from other classes
    according to the provided arguments to process the result data.
    """
    def parse_arguments(self):
        """
        This function parses and validates the given arguments
        """
        parser = argparse.ArgumentParser("Process Result Information")
        parser.add_argument("-present",
                            action="store_true",
                            help="Percentage of Students who attempted")

        parser.add_argument("-passed",
                            help="Students who passed",
                            action="store_true")

        parser.add_argument("-meritlist",
                            help="Show the selected students",
                            action="store_true")

        parser.add_argument("-passingcriteria",
                            "--threshold",
                            type=int,
                            default=argparse.SUPPRESS,
                            help="Passing Criteria")

        parser.add_argument("-scale",
                            "--scale_ratio",
                            type=int,
                            default=argparse.SUPPRESS,
                            help="Scale the result by given ratio")
        return parser.parse_args()

    def __init__(self):
        """
        This function compares the parsed input parameters
        and calls the respective functions.
        """
        arguments = self.parse_arguments()
        result_data_reader = ResultDataReader("data.csv")
        users = result_data_reader.read_data()

        if arguments.present:
            # task 1: Showing the present students
            present_percentage = ResultProcessor.get_present_percentage(users)
            ResultReporter.show_present_percentage(present_percentage)
        if arguments.meritlist:
            # task 4: Showing the merit list
            groups = ResultProcessor.make_merit_list(users, 50)
            ResultReporter.generate_merit_list_files(groups)

        if arguments.passed:
            # performing task 3, scaled result percentage
            if "threshold" in arguments and "scale_ratio" in arguments:
                scaled_per = ResultProcessor.get_scaled_percentage(
                    users,
                    arguments.threshold,
                    arguments.scale_ratio
                )
                ResultReporter.show_scaled_percentage(
                    scaled_per,
                    arguments.threshold,
                    arguments.scale_ratio
                )
            # task 2, only passing threshold is given
            elif "threshold" in arguments:
                result_per = ResultProcessor.get_passed_percentage(
                    users,
                    arguments.threshold
                )
                ResultReporter.show_passed_percentage(
                    result_per,
                    arguments.threshold
                )
        return

if __name__ == '__main__':
    Result()
