import argparse


def parse_arguments():
    """
    This function creates and returns an argument parser
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
