from input_handler import ArgumentExtractor
import calendar
import glob
import sys


class FileDetector(ArgumentExtractor):
    """This method checks and fetches the list of all the files
    which correspond with the arguments presented at the command line"""

    def __init__(self, argument_handler):

        self.file_path = argument_handler.file_directory
        self.year = argument_handler.year
        self.month = calendar.month_abbr[int(argument_handler.month)]
        self.location_dict = {}
        self.name = 0

    def locate_file(self):
        iteration = 1
        if self.month == '':
            self.month = str(0)

        if self.month != '0':
            self.file_path += 'Murree_weather_' + self.year + "_" + \
                          self.month + "*"

        else:
            self.file_path += 'Murree_weather_' + self.year + "*"

        for self.name in glob.glob(self.file_path):
            self.location_dict[iteration] = self.name
            iteration += 1

        if iteration == 0:
            print("The specific weather file was not found."
                  "Exiting the application.")
            sys.exit()
