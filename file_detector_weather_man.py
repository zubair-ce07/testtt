from __future__ import print_function
from argument_handler_weather_man import ArgumentHandler

import calendar
import glob


class FileDetector(ArgumentHandler):
    """This class contains methods to scan the directory passed as input at
    the terminal and fetch the exact path and name of the file to be passed
    for further processing.
    methods : detect_file
    result : absolute path of files for weather analysis"""

    def __init__(self, class_arguments):
        """This __init__ function inherits the processed arguments from the
        ArgumentHandler class and stores then in variables for further processing.
        :param class_arguments: All processes variables in this class
        :returns year : year in numeric for processing
                 month : month in short form 'Jan' for processing
                 location_list : empty dictionary to store all locations """
        self.year = class_arguments.year
        self.month = calendar.month_abbr[int(class_arguments.month)]
        self.path_file = class_arguments.path_file
        self.name = 0
        self.location_list = {}

    def detect_file(self):
        """This function iterations through all the files and before looking
         for absolute paths of the files, concats the keywords
         "Murree_weather" so exact match can be found. Also handles the logic
         on what to do if month is not specified in the terminal
        :return: location_list : consists of all the matching files and
        their path"""
        iteration = 0
        if self.month != 0:
            self.path_file += 'Murree_weather_' + self.year + "_" + \
                          self.month + "*"
        else:
            self.path_file += 'Murree_weather_' + self.year + "*"

        for self.name in glob.glob(self.path_file):
            self.location_list[iteration] = self.name
            iteration += 1
