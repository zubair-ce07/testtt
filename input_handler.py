import calendar
import glob
import sys


class ArgumentExtractor:

    total_arguments = len(sys.argv)

    def __init__(self):
        self.file_directory = ''
        self.date = 0
        self.year = 0
        self.month = 0
        self.mode = ''
        self.location_dict = {}

    def initialization(self, date, mode):

        if ArgumentExtractor.total_arguments < 4:
            print("The number of arguments provided is invalid. Exiting")
            sys.exit()
        else:
            self.file_directory = sys.argv[1]
            self.date = str(sys.argv[3])
            self.year = self.date[:4]
            self.month = self.date[5:]
            self.mode = sys.argv[2]

            if self.month is '':
                self.month = 0
            else:
                if int(self.month) < 1 or int(self.month) > 12:
                    print("The month provided is out of bound. Exiting")
                    sys.exit()

        if date == 0:
            sys.exit()
        else:
            self.year = date[:4]
            self.month = date[5:]
            self.mode = mode
            if self.month is '':
                self.month = 0


class FileHandler(ArgumentExtractor):

    def __init__(self, argument_handler):

        self.file_path = argument_handler.file_directory
        self.year = argument_handler.year
        self.month = calendar.month_abbr[int(argument_handler.month)]
        self.location_dict = {}
        self.name = 0
        self.global_directory = []

    def file_extraction(self, argument_handler):
        file_path = argument_handler.file_directory
        file_path += 'Murree_weather_' + "*"
        iteration = 0
        for self.name in glob.glob(file_path):
            self.global_directory.append(self.name)
            iteration += 1

    def locate_file(self, argument_handler):
        iteration = 1
        file_path = argument_handler.file_directory
        if self.month == '':
            self.month = str(0)
        if self.month != '0':
            file_path += 'Murree_weather_' + str(self.year) + "_" + \
                         self.month
        else:
            file_path += 'Murree_weather_' + str(self.year)

        for name in self.global_directory:

            if file_path in name:
                argument_handler.location_dict[iteration] = name
                self.location_dict[iteration] = name
                iteration += 1

        if iteration == 0:
            print("The specific weather file was not found."
                  "Exiting the application.")
            sys.exit()
