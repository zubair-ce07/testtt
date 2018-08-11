import csv
import sys
import re


"""These constants are used to identify type of the operation
to be performed.
"""
HIGHEST_LOWEST_HUMID = 1
AVERAGE_TEMPERATURE = 2
TWO_LINE_CHART = 3
ONE_LINE_CHART = 4


class Weatherman:
    """This class is for the weatherman object which is used
    to read data from a csv file and then print the required
    formation depending the parameters and date provided
    """

    """Attributes:
        path_to_files = path to the all csv files for weather information
    """

    def __init__(self, path_to_files: "path to the directory containing all csv files"):
        self.path_to_files = path_to_files
